# -*- coding: utf-8 -*-
"""Sinh "SRS - Vấn đề.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/issues/index.vue · components/{CreateIssueModal,IssueHistoryModal}.vue
      components/V2BaseSmartFilterPanel.vue · components/modal/{filter-customization-modal,
      column-customization-modal,export-fields-modal,base-confirm-modal}.vue
      components/comments/{CommentThread,CommentNode,CommentEditor}.vue · components/assign/SystemInfoSection.vue
      components/menu-sidebar.js (menuItemsAssign › Nhiệm vụ) · components/subsystem-menu/presale.js
  BE  Modules/Assign/Routes/api.php (prefix assign/issues) · IssueController · IssueCommentController
      Services/IssueService · Entities/Issue (canEdit/canDelete/canHandle/getAllowedNextStatuses)
      Http/Requests/Issue/* · Transformers/IssueResource/* · app/ExcelExport/ExportColumnRegistry ('issues')
      app/Http/Middleware/CheckSolutionMemberActive (alias solutionMemberActive)
  Quyền: PermissionsTableSeeder id 1099–1102 (nhóm "Vấn đề")
Ảnh chụp thật (headless, 1440x900, client :3002): shots/ — chỉ để local.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, 'shots')


def shot(name):
    return os.path.join(SHOTS, name)


TEN_MAN = 'Vấn đề'
MENU_CV = 'Phân hệ Công việc => Nhiệm vụ => Vấn đề'
MENU_CSKH = 'Phân hệ CSKH trước bán => Vấn đề'
ACTOR = 'Người dùng'
TACNHAN = 'Nhân viên, trưởng nhóm, quản lý dự án / giải pháp; Người dùng đã đăng nhập'
DK_LIST = 'Người dùng đã đăng nhập (màn không yêu cầu quyền thao tác riêng; dữ liệu theo phạm vi quyền V1–V4 và vai trò trên Vấn đề).'
ICONS = {
    'Phân hệ Công việc': 'icon_phanhe_cv.png',
    'Nhiệm vụ': 'icon_nhom_nv.png',
    'Vấn đề': 'icon_man_cv.png',
    'Phân hệ CSKH trước bán': 'icon_phanhe_cskh.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Lọc nhanh theo vai trò': 'icon_scope.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Cấu hình cột hiển thị': 'icon_cot.png',
    'Tạo Vấn đề': 'icon_taomoi.png',
    'Mã Vấn đề': 'icon_ma.png',
    'Sửa': 'icon_sua.png',
    'Xử lý': 'icon_xuly.png',
    'Xóa': 'icon_xoa.png',
    'Lịch sử': 'icon_lichsu.png',
    'Gửi': 'icon_gui.png',
    'Xuất Excel': 'icon_xuat.png',
    'Xuất file': 'icon_xuatfile.png',
}
NO_ROLE = ('– Nếu không đủ điều kiện → nút không hiển thị trên dòng; gọi thẳng chức năng thì hệ thống trả lỗi và '
           'dừng xử lý.')

OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN)
d = SrsDoc(out=OUT, menu=MENU_CV, route='', full_url='', img_prefix='vande_')
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})
d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Vấn đề (Quản lý Vấn đề), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn Vấn đề.',
    'Làm rõ luồng ghi nhận – phân công – xử lý – duyệt đóng – mở lại một Vấn đề phát sinh trong quá trình làm '
    'giải pháp / dự án hoặc trong nội bộ phòng ban, cùng 8 trạng thái và điều kiện chuyển trạng thái.',
    'Làm rõ ai được sửa, xử lý, duyệt, xóa từng Vấn đề (theo vai trò trên Vấn đề) và ai nhìn thấy Vấn đề nào '
    '(theo quyền phạm vi dữ liệu).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Vấn đề', 'Sự cố, vướng mắc, rủi ro hoặc yêu cầu thay đổi cần được xử lý (trên hệ thống còn gọi là issue). '
               'Mã tự sinh dạng ISS-YYYYMM-NNNN.'),
    ('Người tạo', 'Người lập Vấn đề trên hệ thống.'),
    ('Người phụ trách xử lý', 'Người được giao xử lý Vấn đề (cột Người xử lý trên danh sách).'),
    ('Người duyệt đóng', 'Người xác nhận kết quả xử lý: chấp nhận (Hoàn thành) hoặc trả lại (Từ chối).'),
    ('Phòng ban / Bộ phận xử lý', 'Đơn vị được giao Vấn đề khi chưa chỉ định đích danh Người phụ trách xử lý.'),
    ('Người theo dõi / Người phối hợp', 'Những người liên quan được gắn vào Vấn đề để theo dõi hoặc hỗ trợ.'),
    ('Giải pháp / Hạng mục', 'Giải pháp kỹ thuật và hạng mục (module) của giải pháp mà Vấn đề phát sinh.'),
    ('Version giải pháp', 'Phiên bản hiện hành của giải pháp tại thời điểm tạo Vấn đề (hệ thống tự ghi).'),
    ('Tình trạng hạn', 'Trong hạn / Quá hạn — so Hạn xử lý (ngày + giờ) với thời điểm hiện tại.'),
    ('Q / V', 'Ký hiệu vai trò thao tác (Q) và quyền phạm vi dữ liệu (V) ở Phần 2.'),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.p('Màn Vấn đề KHÔNG có quyền thao tác riêng trong danh mục phân quyền: mọi người dùng đã đăng nhập đều thấy menu, '
    'được tạo Vấn đề, xem, bình luận, xem lịch sử và xuất Excel. Thao tác ghi trên một Vấn đề do VAI TRÒ của người '
    'dùng trên chính Vấn đề đó quyết định:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Vai trò Người tạo Vấn đề',
     'Sửa Vấn đề khi chưa ở trạng thái Đã đóng / Hoàn thành (kể cả đổi trạng thái theo luồng); xóa khi Vấn đề còn '
     '“Mới ghi nhận”; mở lại Vấn đề đã Hoàn thành.'),
    ('Q2', 'Vai trò Người phụ trách xử lý',
     'Nút Xử lý hiện khi Vấn đề ở Đã phân công / Đang xử lý / Từ chối / Mở lại / Hoàn thành; chuyển trạng thái xử lý, '
     'thêm tệp đính kèm.'),
    ('Q3', 'Vai trò Người duyệt đóng',
     'Nút Xử lý hiện khi Vấn đề ở “Đã xử lý xong”; duyệt Hoàn thành hoặc Từ chối (bắt buộc nhập lý do).'),
    ('Q4', 'Người xem khác',
     'Người phát hiện, người theo dõi, người phối hợp, thành viên giải pháp / dự án, quản lý theo cấp (V1–V4): chỉ xem, '
     'bình luận, xem lịch sử, xuất Excel.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem danh sách Vấn đề theo tổng công ty',
     'Toàn bộ Vấn đề. Bộ lọc hiện ô Công ty, Phòng ban, Bộ phận.'),
    ('V2', 'Xem danh sách Vấn đề theo công ty',
     'Vấn đề có ít nhất 1 người giữ vai trò (hoặc phòng ban / bộ phận xử lý) thuộc công ty đang làm việc. Bộ lọc hiện ô '
     'Phòng ban, Bộ phận.'),
    ('V3', 'Xem danh sách Vấn đề theo phòng ban',
     'Vấn đề có người giữ vai trò / đơn vị xử lý thuộc phòng ban hoặc bộ phận người dùng quản lý. Bộ lọc hiện ô Phòng '
     'ban, Bộ phận.'),
    ('V4', 'Xem danh sách Vấn đề theo bộ phận',
     'Vấn đề có người giữ vai trò / đơn vị xử lý thuộc bộ phận người dùng quản lý. Bộ lọc hiện ô Bộ phận.'),
    ('Không có quyền nào', '–',
     'Chỉ Vấn đề mà người dùng là Người tạo, Người phát hiện, Người phụ trách xử lý, Người duyệt đóng, Người theo dõi '
     'hoặc Người phối hợp; cộng Vấn đề thuộc giải pháp / dự án người dùng là thành viên. Bộ lọc không hiện ô Công ty, '
     'Phòng ban, Bộ phận.'),
], widths=[0.8, 2.0, 3.2])
d.p('Phạm vi V2–V4 được CỘNG thêm vào phạm vi “Không có quyền nào”; có nhiều quyền thì lấy phạm vi rộng nhất theo thứ tự '
    'V1 → V2 → V3 → V4. Ghi chú: tên quyền trong danh mục phân quyền vẫn giữ chữ “issue” (vd “Xem danh sách issue theo '
    'tổng công ty”).')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Q4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách Vấn đề', '✅', '✅', '✅', '✅', '✅ (theo phạm vi)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo mới Vấn đề', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Xem chi tiết Vấn đề', '✅', '✅', '✅', '✅', '✅'),
    ('FR-07 Chỉnh sửa Vấn đề', '✅', '❌', '❌', '❌', '❌'),
    ('FR-08 Xử lý Vấn đề', '❌ (đổi trạng thái qua Sửa)', '✅', '❌', '❌', '❌'),
    ('FR-09 Duyệt đóng / Từ chối', '❌', '❌', '✅', '❌', '❌'),
    ('FR-10 Mở lại Vấn đề', '✅', '✅', '❌', '❌', '❌'),
    ('FR-11 Xóa Vấn đề', '✅ (Mới ghi nhận)', '❌', '❌', '❌', '❌'),
    ('FR-12 Trao đổi bình luận', '✅', '✅', '✅', '✅', '✅'),
    ('FR-13 Xem lịch sử', '✅', '✅', '✅', '✅', '✅'),
    ('FR-14 Xuất Excel', '✅', '✅', '✅', '✅', '✅'),
], widths=[2.2, 0.8, 0.6, 0.6, 0.6, 1.2])
d.p('“Không có quyền nào” = người dùng không giữ vai trò nào trên Vấn đề nhưng vẫn thấy Vấn đề nhờ quyền phạm vi '
    'hoặc là thành viên giải pháp / dự án.')

# ========================================================= PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR, [0, 1, 2, 3, 4, 5, 6, 7, 8])],
    [('FR-01', 'Xem danh sách Vấn đề', 'view'),
     ('FR-05', 'Tạo mới Vấn đề', 'crud'),
     ('FR-07', 'Chỉnh sửa Vấn đề', 'crud'),
     ('FR-08', 'Xử lý Vấn đề', 'action'),
     ('FR-09', 'Duyệt đóng / Từ chối', 'action'),
     ('FR-10', 'Mở lại Vấn đề', 'action'),
     ('FR-11', 'Xóa Vấn đề', 'action'),
     ('FR-12', 'Trao đổi bình luận', 'crud'),
     ('FR-14', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết Vấn đề', 'view', 'extend', [0], None),
     ('FR-13', 'Xem lịch sử', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

_no = [0]


def menu_lines(suffix=''):
    """Liệt kê đủ 2 lối vào; icon chặng 'Vấn đề' khác nhau giữa 2 phân hệ."""
    d.p('Đường dẫn màn hình:')
    d._menu_para(MENU_CV + suffix)
    keep = d.menu_icons['Vấn đề']
    d.menu_icons['Vấn đề'] = shot('icon_man_cskh.png')
    d._menu_para(MENU_CSKH + suffix)
    d.menu_icons['Vấn đề'] = keep


def fn(ten, code=None, group='view', rule=None, intro=None, suffix='', note=None, shots=(), ui=None, ui_kw=None,
       ev=None):
    if not ui or not ev:
        raise ValueError('Chức năng "%s" thiếu bảng giao diện / event' % ten)
    _no[0] += 1
    n = _no[0]
    d.h3('2.%d %s' % (n, ten))
    k = 0
    if code:
        k += 1
        d.p('2.%d.%d Biểu đồ Usecase' % (n, k))
        d.uc_figure(code, ten, group, actor=ACTOR)
    k += 1
    d.p('2.%d.%d Giới thiệu' % (n, k))
    d.rule_ref(rule[0], anchor=rule[1])
    d.intro_table(**intro)
    k += 1
    d.p('2.%d.%d Layout màn hình' % (n, k))
    menu_lines(suffix)
    if note:
        d.p(note)
    for s, cap in shots:
        d.figure(shot(s), cap, width_in=6.2)
    k += 1
    d.p('2.%d.%d Mô tả chi tiết giao diện' % (n, k))
    d.ui_table(ui, **(ui_kw or {}))
    k += 1
    d.p('2.%d.%d Danh sách event và xử lý event' % (n, k))
    d.event_table(ev)


MODAL_NOTE = 'Popup %s được mở ngay trên màn hình danh sách Vấn đề theo đường dẫn ở trên.'

# ------------------------------------------------------------------ 2.1 Xem danh sách
fn('Xem danh sách Vấn đề',
   rule=('- Màn Danh sách, Phân trang và UI/UX. Chỉ bổ sung các quy tắc riêng của màn Vấn đề tại phần mô tả chi tiết.',
         'list'),
   intro=dict(
       ten='Xem danh sách Vấn đề',
       mota='Hiển thị danh sách Vấn đề trong phạm vi người dùng được xem, kèm số tổng, số Vấn đề quá hạn, tình trạng hạn, '
            'mức độ ưu tiên, trạng thái và các nút thao tác trên từng dòng.',
       tacnhan=TACNHAN,
       dieukien=DK_LIST,
       chinh='1. Người dùng vào menu Vấn đề (từ phân hệ Công việc hoặc CSKH trước bán).\n'
             '2. Hệ thống khôi phục bộ lọc lần trước (nếu quay lại màn trong vòng 10 phút) và tải trang 1, 20 dòng/trang, '
             'sắp xếp Ngày tạo mới nhất trước.\n'
             '3. Hệ thống hiển thị “Tổng: n”, “Quá hạn: n”, bảng Vấn đề và thanh phân trang.\n'
             '4. Người dùng bấm tiêu đề cột có biểu tượng ⇅ để sắp xếp, chuyển trang hoặc đổi số dòng/trang.',
       phu='• Không có Vấn đề nào → “Không có Vấn đề nào được tìm thấy.”\n'
           '• Lỗi khi tải → thông báo “Không thể tải danh sách Vấn đề”, bảng rỗng.\n'
           '• Vào màn từ liên kết trong thông báo → hệ thống mở thẳng popup chi tiết Vấn đề tương ứng (cuộn tới bình '
           'luận nếu liên kết trỏ tới bình luận).'),
   note='Hai lối vào mở cùng một màn, cùng phạm vi dữ liệu. Cuộn ngang bảng để xem các cột còn lại và cột Hành động:',
   shots=[('01-ds.png', 'Màn danh sách Vấn đề lúc mới vào'),
          ('01b-ds-phai.png', 'Các cột cuối bảng và cột Hành động sau khi cuộn ngang')],
   ui=[
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Quản lý Vấn đề', 'Hiển thị trên thanh tiêu đề.'),
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Danh sách Vấn đề', '–'),
       ('Nút Tạo Vấn đề', 'Button', 'Enable', '–', 'Hiển thị', 'Xem FR-05.'),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', 'Khoá trong lúc đang xuất. Xem FR-14.'),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Xem FR-04.'),
       ('Tổng', 'Badge', 'Read-only', '≥ 0', 'Theo dữ liệu', 'Tổng số Vấn đề khớp bộ lọc.'),
       ('Quá hạn', 'Badge', 'Read-only', '≥ 0', 'Theo dữ liệu',
        'Số Vấn đề khớp bộ lọc đã quá Hạn xử lý mà chưa ở Đã xử lý xong / Đã đóng / Hoàn thành.'),
       ('4 nút lọc nhanh theo vai trò', 'Icon Button', 'Enable', '–', 'Không chọn', 'Xem FR-02.'),
       ('Bảng Vấn đề', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Thanh cuộn ngang ở cả trên và dưới; cột STT và Mã Vấn đề ghim bên trái. Mặc định hiện mọi cột.'),
       ('STT', 'Text', 'Read-only', '–', 'Theo trang', 'Đánh số liên tục theo trang.'),
       ('Mã Vấn đề', 'Text (link)', 'Enable', 'ISS-YYYYMM-NNNN', 'Theo dữ liệu',
        'Bấm mở popup chi tiết (FR-06). Có sắp xếp.'),
       ('Tiêu đề Vấn đề', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Tối đa 2 dòng, rê chuột xem đầy đủ.'),
       ('Nhãn', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Hiện tối đa 3 nhãn, còn lại “+n”.'),
       ('Giải pháp', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“Mã - Tên giải pháp”.'),
       ('Version giải pháp', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Version giải pháp lúc tạo Vấn đề, vd V2.'),
       ('Dự án', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Tên dự án TKT.'),
       ('Hạng mục/Module', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
       ('Loại Vấn đề', 'Text', 'Read-only', 'Danh sách 9 giá trị', 'Theo dữ liệu', '–'),
       ('Người xử lý', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Người phụ trách xử lý.'),
       ('Bộ phận xử lý', 'Text', 'Read-only', '–', 'Theo dữ liệu',
        'Tên bộ phận xử lý, không có thì tên phòng ban xử lý, không có thì “—”.'),
       ('Hạn xử lý', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Ngày kèm giờ hạn (nếu có). Có sắp xếp.'),
       ('Tình trạng hạn', 'Badge', 'Read-only', 'Trong hạn / Quá hạn', 'Theo dữ liệu',
        'Xanh “Trong hạn”, đỏ “Quá hạn”; trống khi Vấn đề đã Đã xử lý xong / Đã đóng / Hoàn thành.'),
       ('Mức độ ưu tiên', 'Badge', 'Read-only', 'Thấp / Trung bình / Cao / Khẩn cấp', 'Theo dữ liệu', 'Màu do hệ thống trả về.'),
       ('Người theo dõi / Người phối hợp', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Danh sách tên, ngăn cách dấu phẩy.'),
       ('Người duyệt', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Người duyệt đóng.'),
       ('Nguồn phát hiện', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
       ('Người phát hiện / Ngày phát hiện', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Ngày phát hiện có sắp xếp.'),
       ('Người cập nhật / Ngày cập nhật', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Ngày cập nhật có sắp xếp.'),
       ('Người tạo / Ngày tạo', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Ngày tạo có sắp xếp.'),
       ('Trạng thái', 'Badge', 'Read-only', 'Danh sách 8 giá trị', 'Theo dữ liệu',
        'Mới ghi nhận (xám) · Đã phân công (xanh trời) · Đang xử lý (xanh dương) · Đã xử lý xong (xanh lá) · Hoàn thành '
        '(xanh lá) · Từ chối (đỏ) · Mở lại (cam) · Đã đóng (xám).'),
       ('Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo vai trò',
        'Sửa (FR-07) · Xóa (FR-11) · Xử lý (FR-08/09/10) · Lịch sử (FR-13). Nút không đủ điều kiện thì ẩn hẳn; cột '
        'luôn ở cuối bảng.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có Vấn đề nào được tìm thấy.”'),
       ('Thanh phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', '20', '“Hiển thị a–b / n”.'),
   ], ui_kw=dict(required=False),
   ev=[
       ('Mở màn hình', 'System',
        'After:\n– Khôi phục bộ lọc đã lưu (hết hạn sau 10 phút), tải danh sách + số Quá hạn, nạp cấu hình cột.\n'
        '– Có tham số mở Vấn đề từ thông báo → mở popup chi tiết Vấn đề đó.\n'
        '– Lỗi → “Không thể tải danh sách Vấn đề”.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'After:\n– Đổi chiều sắp xếp tăng / giảm, về trang 1 và tải lại. Cột không hợp lệ → mặc định Ngày tạo giảm dần.'),
       ('Chuyển trang / đổi số dòng mỗi trang', 'Click / Change',
        'After:\n– Tải lại danh sách (đổi số dòng thì về trang 1).'),
   ])

# ------------------------------------------------------------------ 2.2 Tìm kiếm và lọc
fn('Tìm kiếm và lọc',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Vấn đề tại phần mô tả chi tiết.',
         'search'),
   intro=dict(
       ten='Tìm kiếm và lọc',
       mota='Tìm nhanh theo mã / tiêu đề Vấn đề / tên người tạo; lọc nâng cao theo đơn vị, giải pháp, dự án, hạng mục, '
            'version, loại, người thực hiện, người tạo, người duyệt, trạng thái, mức độ ưu tiên, ngày tạo; lọc nhanh theo '
            'vai trò của chính người dùng.',
       tacnhan=TACNHAN,
       dieukien=DK_LIST,
       chinh='1. Người dùng gõ từ khoá vào ô tìm nhanh rồi bấm “Tìm kiếm” hoặc nhấn Enter.\n'
             '2. Người dùng bấm “Tìm kiếm nâng cao” để mở khối lọc, chọn điều kiện — chọn tới đâu danh sách tự tải lại '
             'tới đó.\n'
             '3. Người dùng bấm 1 trong 4 nút lọc nhanh: Tôi phụ trách xử lý / Tôi phát hiện / Tôi theo dõi / Tôi duyệt '
             'đóng.\n'
             '4. Hệ thống về trang 1 và tải lại danh sách theo điều kiện.',
       phu='• Bấm “Làm mới” → xoá mọi điều kiện (kể cả lọc nhanh, sắp xếp), tải lại 1 lần.\n'
           '• Chưa chọn Giải pháp → ô Dự án, Hạng mục/Module, Version giải pháp không có lựa chọn; đổi Giải pháp → xoá '
           'giá trị 3 ô này.\n'
           '• Bấm lại nút lọc nhanh đang bật hoặc dấu × ở nhãn “Đang lọc: …” → bỏ lọc nhanh.\n'
           '• Danh mục của khối lọc chỉ được nạp lần đầu mở khối (hoặc khi bộ lọc khôi phục có sẵn giá trị).'),
   suffix=' => Tìm kiếm nâng cao',
   note='Lọc nhanh theo vai trò là 4 nút biểu tượng ngay trên bảng (cạnh số Tổng, Quá hạn):',
   shots=[('02-loc.png', 'Khối Tìm kiếm nâng cao đang mở'),
          ('02b-loc-nhanh.png', 'Lọc nhanh “Tôi phụ trách xử lý” đang bật')],
   ui=[
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Tự do', 'Không', 'Trống',
        'Gợi ý “Tìm theo mã Vấn đề, tiêu đề Vấn đề, người tạo”; có nút × xoá nhanh. Chỉ tìm khi bấm Tìm kiếm / Enter.'),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Tìm kiếm nâng cao',
        'Mở / đóng khối lọc; mặc định đóng.'),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống', 'Chỉ hiện với V1.'),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống', 'Hiện với V1 / V2 / V3.'),
       ('Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
        'Hiện với V1–V4. Lọc Công ty / Phòng ban / Bộ phận: giữ Vấn đề có ít nhất 1 người giữ vai trò (hoặc đơn vị xử '
        'lý) thuộc đơn vị đã chọn.'),
       ('Giải pháp', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Hiển thị “Mã - Tên giải pháp”.'),
       ('Dự án', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Chỉ dự án gắn với giải pháp đã chọn.'),
       ('Hạng mục/Module', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Chỉ hạng mục của giải pháp đã chọn.'),
       ('Version giải pháp', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Các version của giải pháp đã chọn, vd V2.'),
       ('Loại Vấn đề', 'Dropdown', 'Enable', 'Danh sách 9 giá trị', 'Không', 'Trống',
        'Lỗi phần mềm · Vướng nghiệp vụ · Yêu cầu thay đổi · Thiếu dữ liệu · Rủi ro · Hạ tầng / tích hợp · Thiếu thông '
        'tin đầu vào · Yêu cầu thay đổi từ phía khách hàng · Khác.'),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Lọc theo Người phụ trách xử lý.'),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', '–'),
       ('Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Lọc theo Người duyệt đóng.'),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 8 giá trị', 'Không', 'Trống', '–'),
       ('Mức độ ưu tiên', 'Dropdown', 'Enable', 'Thấp / Trung bình / Cao / Khẩn cấp', 'Không', 'Trống', '–'),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống', 'Khoảng ngày trong 1 ô.'),
       ('Nút lọc nhanh Tôi phụ trách xử lý / Tôi phát hiện / Tôi theo dõi / Tôi duyệt đóng', 'Icon Button', 'Enable',
        '–', 'Không', 'Không chọn', 'Chỉ bật được 1 nút; nút đang bật tô màu.'),
       ('Nhãn “Đang lọc: <tên lọc nhanh>”', 'Label', 'Enable / Ẩn', '–', '–', 'Ẩn', 'Có nút × bỏ lọc nhanh.'),
   ],
   ev=[
       ('Gõ ô tìm nhanh + bấm Tìm kiếm / Enter', 'Click / Keypress',
        'After:\n– Tìm theo mã, tiêu đề Vấn đề hoặc tên người tạo (gần đúng), về trang 1, tải lại.'),
       ('Chọn / xoá giá trị ở ô lọc nâng cao', 'Change',
        'After:\n– Tự tải lại danh sách từ trang 1 (không cần bấm Tìm kiếm).\n'
        '– Đổi Giải pháp → xoá Dự án, Hạng mục/Module, Version giải pháp; nạp lại danh sách version.'),
       ('Bấm nút lọc nhanh', 'Click',
        'After:\n– Bỏ lọc nhanh đang có, gán điều kiện tương ứng = người đang đăng nhập, hiện nhãn “Đang lọc”, tải lại.\n'
        '– Bấm lại đúng nút đang bật → tắt lọc nhanh.'),
       ('Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện, về trang 1, tải lại đúng 1 lần.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'After:\n– Mở / đóng khối lọc; lần mở đầu nạp danh mục giải pháp, dự án, nhân viên.'),
   ])

# ------------------------------------------------------------------ 2.3 Cài đặt bộ lọc
fn('Cài đặt bộ lọc', code='FR-03', group='crud',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'search'),
   intro=dict(
       ten='Cài đặt bộ lọc',
       mota='Cho từng người dùng chọn trường lọc nào hiển thị và thứ tự các trường trong khối Tìm kiếm nâng cao của màn '
            'Vấn đề.',
       tacnhan=TACNHAN,
       dieukien=DK_LIST,
       chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
             '2. Hệ thống mở popup liệt kê 12 trường lọc, đánh số thứ tự.\n'
             '3. Người dùng tích / bỏ tích trường, kéo biểu tượng ⋮⋮ để đổi thứ tự.\n'
             '4. Người dùng bấm “Lưu”.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại khối lọc.',
       phu='• Bấm “Khôi phục mặc định” → về thứ tự gốc, hiện đủ trường (chỉ ghi nhận khi bấm Lưu).\n'
           '• Bấm “Đóng” / × → đóng popup, không lưu.\n'
           '• Lưu lỗi → “Thao tác thất bại”.\n'
           '• Trường bị ẩn đang có giá trị lọc → giá trị đó bị xoá để không lọc ngầm (ẩn nhóm Công ty – Phòng ban – Bộ '
           'phận thì xoá cả 3 ô).',
       dacbiet='Cấu hình lưu theo tài khoản người dùng và theo màn; người khác không bị ảnh hưởng.'),
   suffix=' => Cài đặt bộ lọc', note=MODAL_NOTE % 'Cài đặt bộ lọc',
   shots=[('03-cai-dat-loc.png', 'Popup Cài đặt bộ lọc')],
   ui=[
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', 'Kèm biểu tượng bánh răng.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo ⋮⋮ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách trường lọc', 'Checkbox', 'Enable', '12 trường', 'Không', 'Theo cấu hình đã lưu',
        'Công ty – Phòng ban – Bộ phận, Giải pháp, Dự án, Hạng mục/Module, Version giải pháp, Loại Vấn đề, Người thực '
        'hiện, Người tạo, Người duyệt, Trạng thái, Mức độ ưu tiên, Ngày tạo.'),
       ('Biểu tượng kéo ⋮⋮', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo thả để đổi thứ tự.'),
       ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khoá trong lúc đang lưu.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở popup với cấu hình đã lưu (chưa có thì hiện đủ trường).'),
       ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đưa danh sách về thứ tự khai báo gốc, tích đủ mọi trường.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Người dùng đã đăng nhập.\n'
        'After:\n– Lưu cấu hình theo người dùng + màn; xoá giá trị lọc của trường vừa bị ẩn.\n'
        '– Hiển thị “Cập nhật thành công”, đóng popup, vẽ lại khối lọc.\n– Lỗi → “Thao tác thất bại”.'),
       ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------------ 2.4 Tùy chỉnh cột
fn('Tùy chỉnh cột', code='FR-04', group='crud',
   rule=('- Màn Danh sách, Cấu hình cột. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột',
       mota='Cho từng người dùng ẩn / hiện và sắp xếp lại thứ tự các cột của bảng Vấn đề.',
       tacnhan=TACNHAN,
       dieukien=DK_LIST,
       chinh='1. Người dùng bấm biểu tượng “Cấu hình cột hiển thị” cạnh nút Xuất Excel.\n'
             '2. Hệ thống mở popup “Tuỳ chỉnh cột” liệt kê đủ 26 cột theo thứ tự đang dùng.\n'
             '3. Người dùng tích / bỏ tích cột, kéo biểu tượng ☰ để đổi vị trí.\n'
             '4. Người dùng bấm “Lưu”.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công”, bảng vẽ lại theo cấu hình mới.',
       phu='• Cột khoá (STT, Mã Vấn đề, Hành động) có biểu tượng ổ khoá: luôn hiện, không bỏ tích, không kéo được.\n'
           '• Bấm “Đóng” / × → danh sách cột trả về cấu hình đang áp dụng, không lưu.\n'
           '• Lưu lỗi → “Thao tác thất bại”.',
       dacbiet='Cấu hình lưu theo tài khoản người dùng và theo màn. Mặc định hiện tất cả các cột.'),
   suffix=' => Cấu hình cột hiển thị', note=MODAL_NOTE % 'Tuỳ chỉnh cột',
   shots=[('04-cot.png', 'Popup Tuỳ chỉnh cột')],
   ui=[
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', 'Kèm biểu tượng cột.'),
       ('Danh sách cột', 'Checkbox', 'Enable', '26 cột', 'Không', 'Theo cấu hình đã lưu',
        'STT, Mã Vấn đề, Tiêu đề Vấn đề, Nhãn, Giải pháp, Version giải pháp, Dự án, Hạng mục/Module, Loại Vấn đề, Người '
        'xử lý, Bộ phận xử lý, Hạn xử lý, Tình trạng hạn, Mức độ ưu tiên, Người theo dõi, Người phối hợp, Người duyệt, '
        'Nguồn phát hiện, Người phát hiện, Ngày phát hiện, Người cập nhật, Ngày cập nhật, Người tạo, Ngày tạo, Trạng '
        'thái, Hành động.'),
       ('Cột khoá STT / Mã Vấn đề / Hành động', 'Checkbox', 'Disable', '–', '–', 'Luôn tích',
        'Xám, biểu tượng ổ khoá, rê chuột: “Cột bắt buộc — không thể ẩn hoặc đổi vị trí”.'),
       ('Biểu tượng kéo ☰', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo thả để đổi thứ tự cột.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click', 'After:\n– Mở popup với cấu hình cột đang áp dụng.'),
       ('Kéo thả 1 cột', 'Change', 'After:\n– Đổi vị trí cột trong danh sách (cột khoá đứng yên).'),
       ('Bấm Lưu', 'Click',
        'After:\n– Lưu cấu hình cột theo người dùng + màn, “Cập nhật thành công”, bảng vẽ lại.\n'
        '– Lỗi → “Thao tác thất bại”.'),
       ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup, trả danh sách cột về cấu hình đang áp dụng.'),
   ])

# ------------------------------------------------------------------ 2.5 Tạo mới
FORM_UI = [
    ('Tiêu đề Vấn đề', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Gợi ý “VD: Popup tạo nhiệm vụ bị mất dữ liệu khi chuyển tab”.'),
    ('Giải pháp', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Tìm theo mã / tên. Chỉ liệt kê giải pháp ở trạng thái Chờ Leader duyệt, Đang triển khai, Chờ duyệt giải pháp, Đã '
     'duyệt giải pháp, Chờ làm giá, Đã duyệt giá. Chọn giải pháp → tự điền Dự án/Nhóm của giải pháp, xoá Hạng mục.'),
    ('Dự án/Nhóm', 'Dropdown', 'Enable', 'Danh sách dự án TKT', 'Không', 'Trống', 'Tìm theo mã / tên.'),
    ('Hạng mục / Module', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Có khi giải pháp có hạng mục', 'Trống',
     'Chỉ mở khi đã chọn giải pháp có hạng mục; liệt kê hạng mục ở trạng thái Đang triển khai / Chờ duyệt hồ sơ trình '
     'duyệt.'),
    ('Loại Vấn đề', 'Dropdown', 'Enable', 'Danh sách 9 giá trị', 'Có', 'Lỗi phần mềm', '–'),
    ('Nhóm nguyên nhân', 'Dropdown', 'Enable', 'Danh sách 9 giá trị', 'Không', 'Trống',
     'Thiếu validate · Sai đặc tả · Thiếu dữ liệu · Lỗi tích hợp · Lỗi logic · Danh mục sản phẩm · Bản vẽ sản phẩm · '
     'Thông số kỹ thuật sản phẩm · Thay đổi về công nghệ.'),
    ('Mức độ ưu tiên', 'Dropdown', 'Enable', 'Thấp / Trung bình / Cao / Khẩn cấp', 'Có', 'Trung bình', '–'),
    ('Mức độ ảnh hưởng', 'Dropdown', 'Enable', 'Danh sách 8 giá trị', 'Có', 'Cá nhân',
     'Cá nhân · Nhóm nhỏ · Toàn module · Toàn dự án · Khách hàng · Ít · Nhiều · Trung bình.'),
    ('Mô tả Vấn đề', 'Textarea', 'Enable', 'Tự do', 'Có', 'Trống', '5 dòng.'),
    ('Nguồn phát hiện', 'Dropdown', 'Enable', 'Danh sách 7 giá trị', 'Có', 'Tự phát hiện',
     'Tự phát hiện · PM phát hiện · Leader phát hiện · Tester phát hiện · Khách hàng phản ánh · Từ meeting · Nhân viên '
     'phát hiện.'),
    ('Người phát hiện', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', '“Tên - Mã phòng - Mã nhân viên”.'),
    ('Ngày giờ phát hiện', 'Datepicker', 'Enable', 'dd/mm/yyyy hh:mm', 'Không', 'Thời điểm mở form', '–'),
    ('Nhiệm vụ chính liên kết', 'Dropdown', 'Enable', 'Danh sách nhiệm vụ', 'Không', 'Trống', 'Tìm theo mã / tiêu đề.'),
    ('Hạn xử lý', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', '–'),
    ('Giờ hạn', 'Textbox', 'Enable', 'hh:mm', 'Không', '17:00', 'Bỏ trống giờ thì hạn tính tới 23:59:59.'),
    ('Người duyệt đóng', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Có người duyệt đóng → Vấn đề phải qua bước duyệt (Đã xử lý xong → Hoàn thành / Từ chối).'),
    ('Ảnh hưởng tiến độ / chất lượng / khách hàng', 'Dropdown', 'Enable',
     'Không đáng kể / Ảnh hưởng nhẹ / Ảnh hưởng lớn', 'Không', 'Không đáng kể', '3 ô riêng.'),
    ('Ghi chú ảnh hưởng', 'Textarea', 'Enable', 'Tự do', 'Không', 'Trống', '–'),
    ('Bảng Tệp đính kèm / chứng cứ', 'Table/Grid', 'Enable', '–', 'Không', '“Chưa có tệp đính kèm”',
     'Cột STT · Tên tài liệu · Loại tài liệu (danh mục Loại tài liệu) · Upload / File · Dung lượng · nút xoá dòng.'),
    ('Nút Thêm tài liệu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thêm 1 dòng tài liệu trống.'),
    ('Nút Chọn tệp / Tải xuống / Thay đổi', 'Button', 'Enable', 'jpg, jpeg, png, doc, docx, xls, xlsx, pdf, ppt, pptx; '
     '≤ 20MB', 'Không', 'Hiển thị', 'Tệp tải lên ngay khi chọn, hiện “Đang tải lên...”; dòng không có tệp bị bỏ qua khi lưu.'),
    ('Trạng thái Vấn đề', 'Dropdown', 'Enable', 'Mới ghi nhận / Đã phân công', 'Có', 'Mới ghi nhận',
     'Khi Sửa / Xử lý: chỉ liệt kê trạng thái hiện tại + các trạng thái được phép chuyển (BR-02).'),
    ('Phòng ban xử lý', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Có khi chưa chọn Người phụ trách xử lý', 'Trống',
     'Ghi chú dưới ô: “Để trống Người phụ trách xử lý thì Vấn đề sẽ được gửi tới Trưởng bộ phận của phòng ban đã chọn.” '
     'Đổi phòng ban → xoá Bộ phận xử lý.'),
    ('Bộ phận xử lý', 'Dropdown', 'Enable / Disable', 'Bộ phận của phòng ban đã chọn', 'Không', 'Trống',
     'Chỉ mở khi đã chọn Phòng ban xử lý.'),
    ('Người phụ trách xử lý', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Có khi Trạng thái = Đã phân công', 'Trống', '–'),
    ('Người theo dõi / Người phối hợp', 'Dropdown', 'Enable', 'Chọn nhiều', 'Không', 'Trống', 'Hiển thị dạng thẻ.'),
    ('SLA xử lý', 'Dropdown', 'Enable', '4 giờ / 8 giờ / 1 ngày / 2 ngày / Theo deadline riêng', 'Không', '1 ngày', '–'),
    ('Tags', 'Textbox', 'Enable', 'Tự do', 'Không', 'Trống',
     'Gõ rồi nhấn Enter để thêm thẻ (không thêm trùng); bấm × trên thẻ để bỏ; nút “Xóa” bỏ hết thẻ.'),
    ('Kế hoạch xử lý / Điều kiện đóng Vấn đề', 'Textarea', 'Enable', 'Tự do', 'Không', 'Trống', '2 ô riêng.'),
    ('Nút Làm mới (đầu popup)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đưa form về giá trị mặc định.'),
    ('Nút Lưu thông tin', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khoá trong lúc đang lưu.'),
    ('Nút Đóng / ×', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng popup, không lưu.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Chữ đỏ ngay dưới ô sai.'),
]

SAVE_DURING = (
    'During:\n'
    '– Tiêu đề trống → “Tiêu đề không được để trống”.\n'
    '– Chưa chọn Người phụ trách xử lý lẫn Phòng ban xử lý → “Vui lòng chọn Bộ phận xử lý hoặc Người phụ trách xử lý.”\n'
    '– Giải pháp có hạng mục mà chưa chọn Hạng mục → “Module không được để trống”.\n'
    '– Loại / Mức độ ưu tiên / Mức độ ảnh hưởng / Mô tả / Nguồn phát hiện / Trạng thái trống → “Loại Vấn đề không được '
    'để trống” / “Mức độ ưu tiên không được để trống” / “Mức độ ảnh hưởng không được để trống” / “Mô tả không được để '
    'trống” / “Nguồn phát hiện không được để trống” / “Trạng thái không được để trống”.\n'
    '– Trạng thái Đã phân công mà chưa có Người phụ trách xử lý → “Người phụ trách xử lý không được để trống khi trạng '
    'thái là \"Đã phân công\"”.\n'
    '– Còn lỗi → không gọi máy chủ. Máy chủ trả lỗi theo trường → hiện dưới ô + thông báo “Vui lòng kiểm tra lại thông '
    'tin.”')

fn('Tạo mới Vấn đề', code='FR-05', group='crud',
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.',
         'create'),
   intro=dict(
       ten='Tạo mới Vấn đề',
       mota='Ghi nhận 1 Vấn đề mới: thông tin Vấn đề, ghi nhận phát sinh, đánh giá ảnh hưởng, tệp chứng cứ, đơn vị / người '
            'xử lý, liên kết và kế hoạch xử lý.',
       tacnhan=TACNHAN,
       dieukien='Người dùng đã đăng nhập; nếu chọn giải pháp thì người dùng không bị khoá khỏi giải pháp đó.',
       chinh='1. Người dùng bấm “Tạo Vấn đề”.\n'
             '2. Hệ thống mở popup “Thêm mới Vấn đề” với giá trị mặc định.\n'
             '3. Người dùng nhập Tiêu đề, Mô tả, chọn Giải pháp / Hạng mục (nếu có), Phòng ban xử lý hoặc Người phụ '
             'trách xử lý và các thông tin khác; thêm tệp đính kèm nếu cần.\n'
             '4. Người dùng bấm “Lưu thông tin”.\n'
             '5. Hệ thống kiểm tra, sinh mã ISS-YYYYMM-NNNN, lưu Vấn đề, báo “Lưu Vấn đề thành công”, đóng popup và tải '
             'lại danh sách.',
       phu='• Thiếu / sai dữ liệu → báo lỗi dưới từng ô, không lưu.\n'
           '• Tệp sai định dạng → “Định dạng không hợp lệ. Chỉ chấp nhận: jpg, jpeg, png, doc, docx, xls, xlsx, pdf, ppt, '
           'pptx”; tệp > 20MB → “File quá lớn. Không được tải lên file lớn hơn 20MB.”; tải lên lỗi → “Upload thất bại. '
           'File có thể vượt quá giới hạn cho phép của server (20MB).”\n'
           '• Người dùng đã bị khoá khỏi giải pháp đã chọn → “Bạn đã bị khóa khỏi giải pháp này nên không thao tác được. '
           'Vui lòng liên hệ PM hoặc Trưởng phòng giải pháp.”\n'
           '• Lỗi khác → hiển thị nội dung lỗi hoặc “Có lỗi xảy ra”.',
       dacbiet='Vấn đề nội bộ phòng ban được phép không gắn giải pháp / dự án. Hệ thống tự ghi Version giải pháp / hạng mục '
               'hiện hành của giải pháp tại thời điểm tạo.'),
   suffix=' => Tạo Vấn đề', note=MODAL_NOTE % 'Thêm mới Vấn đề',
   shots=[('05-tao-a.png', 'Popup Thêm mới Vấn đề — phần đầu'),
          ('05-tao-b.png', 'Popup Thêm mới Vấn đề — phần cuối (đánh giá ảnh hưởng, tệp đính kèm, kế hoạch xử lý)'),
          ('05-tao-loi.png', 'Báo lỗi dưới từng ô khi bấm Lưu thông tin mà thiếu dữ liệu bắt buộc')],
   ui=FORM_UI,
   ev=[
       ('Bấm Tạo Vấn đề', 'Click',
        'After:\n– Mở popup với giá trị mặc định; nạp danh sách dự án, giải pháp, nhiệm vụ, loại tài liệu.'),
       ('Chọn Giải pháp', 'Change',
        'After:\n– Tự điền Dự án/Nhóm theo giải pháp, xoá Hạng mục; Hạng mục bắt buộc nếu giải pháp có hạng mục.'),
       ('Chọn tệp ở dòng tài liệu', 'Change',
        'During:\n– Kiểm tra định dạng và dung lượng ≤ 20MB.\nAfter:\n– Tải tệp lên ngay, hiện tên tệp + dung lượng.'),
       ('Bấm Lưu thông tin', 'Click',
        'Before:\n– Người dùng đã đăng nhập; nếu có giải pháp → kiểm tra người dùng không bị khoá khỏi giải pháp.\n'
        + SAVE_DURING + '\n'
        'After:\n– Sinh mã, lưu Vấn đề (Người tạo = người đang đăng nhập), ghi người theo dõi / phối hợp, thẻ, tệp đính kèm.\n'
        '– Ghi lịch sử “Tạo mới Vấn đề”.\n'
        '– Chỉ chọn Phòng ban / Bộ phận xử lý (chưa có người phụ trách) → gửi thông báo “[ISSUE] Tạo mới: <tiêu đề>. Giao '
        'xử lý cho <đơn vị>.” cho Trưởng bộ phận (bộ phận chưa có trưởng thì Trưởng phòng ban).\n'
        '– Hiển thị “Lưu Vấn đề thành công”, đóng popup, tải lại danh sách.'),
       ('Bấm Làm mới / Đóng', 'Click', 'After:\n– Làm mới: đưa form về mặc định. Đóng: đóng popup, không lưu.'),
   ])

# ------------------------------------------------------------------ 2.6 Xem chi tiết
fn('Xem chi tiết Vấn đề',
   rule=('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'detail'),
   intro=dict(
       ten='Xem chi tiết Vấn đề',
       mota='Popup chỉ đọc hiển thị toàn bộ thông tin của 1 Vấn đề, khu vực Bình luận và mục Lịch sử.',
       tacnhan=TACNHAN,
       dieukien='Vấn đề nằm trong phạm vi người dùng được xem.',
       chinh='1. Người dùng bấm Mã Vấn đề trên dòng (hoặc bấm liên kết trong thông báo).\n'
             '2. Hệ thống mở popup “<Mã> — Chi tiết Vấn đề” kèm nhãn trạng thái và nạp dữ liệu mới nhất.\n'
             '3. Các ô hiển thị ở chế độ chỉ đọc; cuối popup có Bình luận (FR-12) và Lịch sử (FR-13).',
       phu='• Lỗi khi tải → “Lỗi khi tải chi tiết Vấn đề”.\n'
           '• Vấn đề Từ chối → hiện khung “Lý do từ chối: …”; Vấn đề Hoàn thành → hiện khung “Hoàn thành lúc: …”.'),
   suffix=' => Mã Vấn đề', note=MODAL_NOTE % 'Chi tiết Vấn đề',
   shots=[('06-chitiet-a.png', 'Popup Chi tiết Vấn đề — phần đầu'),
          ('06-chitiet-b.png', 'Popup Chi tiết Vấn đề — phần cuối (tệp đính kèm, Bình luận, Lịch sử)')],
   ui=[
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '<Mã> — Chi tiết Vấn đề', 'Kèm biểu tượng và nhãn trạng thái có chấm màu.'),
       ('Nhóm Thông tin Vấn đề', 'Text', 'Read-only', '–', 'Theo dữ liệu',
        'Tiêu đề, Giải pháp, Dự án/Nhóm, Hạng mục / Module, Loại Vấn đề, Nhóm nguyên nhân, Mức độ ưu tiên, Mức độ ảnh '
        'hưởng, Mô tả.'),
       ('Nhóm Ghi nhận phát sinh', 'Text', 'Read-only', '–', 'Theo dữ liệu',
        'Nguồn phát hiện, Người phát hiện, Ngày giờ phát hiện, Nhiệm vụ chính liên kết, Hạn xử lý, Giờ hạn, Người duyệt '
        'đóng.'),
       ('Nhóm Đánh giá ảnh hưởng', 'Text', 'Read-only', '–', 'Theo dữ liệu', '3 mức ảnh hưởng + Ghi chú ảnh hưởng.'),
       ('Bảng Tệp đính kèm / chứng cứ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Có nút Tải xuống từng tệp; không có thì “Chưa có tệp đính kèm”.'),
       ('Nhóm Thông tin xử lý', 'Text', 'Read-only', '–', 'Theo dữ liệu',
        'Trạng thái, Phòng ban / Bộ phận xử lý, Người phụ trách xử lý, Người theo dõi, Người phối hợp, SLA xử lý.'),
       ('Khung Lý do từ chối / Hoàn thành lúc', 'Label', 'Enable / Ẩn', '–', 'Ẩn', 'Chỉ hiện ở trạng thái tương ứng.'),
       ('Nhóm Liên kết & phân loại / Kế hoạch xử lý', 'Text', 'Read-only', '–', 'Theo dữ liệu',
        'Tags, Kế hoạch xử lý, Điều kiện đóng Vấn đề.'),
       ('Khu vực Bình luận', 'Table/Grid', 'Enable', '–', 'Theo dữ liệu', 'Xem FR-12.'),
       ('Mục Lịch sử', 'Table/Grid', 'Enable', '–', 'Thu gọn', 'Xem FR-13.'),
       ('Nút Đóng / ×', 'Button', 'Enable', '–', 'Hiển thị', 'Chân popup chỉ có nút Đóng.'),
   ], ui_kw=dict(required=False),
   ev=[
       ('Bấm Mã Vấn đề', 'Click',
        'After:\n– Mở popup chỉ đọc, nạp chi tiết Vấn đề; lỗi → “Lỗi khi tải chi tiết Vấn đề”.'),
       ('Bấm Tải xuống ở dòng tệp', 'Click', 'After:\n– Mở tệp ở tab mới.'),
       ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup.'),
   ])

# ------------------------------------------------------------------ 2.7 Chỉnh sửa
fn('Chỉnh sửa Vấn đề', code='FR-07', group='crud',
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - '
         'Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Chỉnh sửa Vấn đề',
       mota='Người tạo cập nhật thông tin Vấn đề và có thể chuyển trạng thái theo luồng được phép (vd giao Đã phân công, '
            'Đã đóng).',
       tacnhan='Người tạo Vấn đề (Q1)',
       dieukien='Người dùng là Người tạo; Vấn đề chưa ở trạng thái Đã đóng / Hoàn thành.',
       chinh='1. Người dùng bấm biểu tượng bút “Sửa” trên dòng.\n'
             '2. Hệ thống mở popup “<Mã> — Chỉnh sửa Vấn đề” với dữ liệu hiện tại.\n'
             '3. Người dùng sửa thông tin, có thể đổi Trạng thái trong danh sách trạng thái được phép.\n'
             '4. Người dùng bấm “Lưu thông tin”.\n'
             '5. Hệ thống kiểm tra, lưu, ghi lịch sử, báo “Lưu Vấn đề thành công”, đóng popup và tải lại danh sách.',
       phu='• Thiếu / sai dữ liệu → báo lỗi dưới ô như FR-05.\n'
           '• Vấn đề đã đóng / không còn quyền → “Bạn không có quyền chỉnh sửa Vấn đề này hoặc Vấn đề đã đóng.”\n'
           '• Đổi Phòng ban / Bộ phận xử lý khi chưa có Người phụ trách → gửi lại thông báo cho Trưởng đơn vị mới.',
       dacbiet='Popup Sửa có thêm khu vực Bình luận và mục Lịch sử như popup Chi tiết.'),
   suffix=' => Sửa', note=MODAL_NOTE % 'Chỉnh sửa Vấn đề',
   shots=[('07-sua-a.png', 'Popup Chỉnh sửa Vấn đề với dữ liệu thật')],
   ui=[('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', '<Mã> — Chỉnh sửa Vấn đề', 'Kèm nhãn trạng thái.'),
       ('Các trường của form', '(như FR-05)', 'Enable', 'Như FR-05', 'Như FR-05', 'Theo dữ liệu',
        'Cùng bộ trường, ràng buộc và thông báo lỗi với popup Tạo mới.'),
       ('Trạng thái Vấn đề', 'Dropdown', 'Enable', 'Trạng thái hiện tại + trạng thái được phép', 'Có', 'Theo dữ liệu',
        'Danh sách do hệ thống tính theo vai trò người dùng (BR-02).'),
       ('Khu vực Bình luận / Mục Lịch sử', 'Table/Grid', 'Enable', '–', '–', 'Hiển thị', 'Xem FR-12, FR-13.'),
       ('Nút Lưu thông tin / Làm mới / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Như FR-05.')],
   ev=[
       ('Bấm Sửa trên dòng', 'Click',
        'Before:\n– Nút chỉ hiện khi người dùng là Người tạo và Vấn đề chưa Đã đóng / Hoàn thành.\n' + NO_ROLE + '\n'
        'After:\n– Mở popup, nạp chi tiết mới nhất.'),
       ('Bấm Lưu thông tin', 'Click',
        'Before:\n– Kiểm tra người dùng còn quyền sửa hoặc quyền xử lý; không → “Bạn không có quyền chỉnh sửa Vấn đề này '
        'hoặc Vấn đề đã đóng.”\n' + SAVE_DURING + '\n'
        'After:\n– Lưu thông tin, người theo dõi / phối hợp, thẻ, tệp đính kèm.\n'
        '– Trạng thái thay đổi → ghi thời điểm tương ứng (đóng / xử lý xong / hoàn thành / từ chối), ghi lịch sử “Thay '
        'đổi trạng thái”, gửi thông báo theo BR-05.\n'
        '– Ghi lịch sử “Cập nhật thông tin” (giá trị cũ → mới).\n'
        '– Hiển thị “Lưu Vấn đề thành công”, đóng popup, tải lại danh sách.'),
   ])

# ------------------------------------------------------------------ 2.8 Xử lý
HANDLE_UI = [
    ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', '<Mã> — Chi tiết Vấn đề', 'Kèm nhãn trạng thái (đổi theo lựa chọn).'),
    ('Các trường thông tin Vấn đề', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'Chỉ đọc như FR-06.'),
    ('Trạng thái Vấn đề', 'Dropdown', 'Enable', 'Trạng thái hiện tại + trạng thái được phép', 'Có', 'Trạng thái hiện tại',
     'Danh sách do hệ thống tính theo vai trò (BR-02).'),
    ('Lý do từ chối', 'Textarea', 'Enable / Ẩn', 'Tự do', 'Có khi chọn Từ chối', 'Ẩn', 'Chỉ hiện khi chọn Từ chối.'),
    ('Bảng Tệp đính kèm / Nút Thêm tài liệu', 'Table/Grid', 'Enable', 'Như FR-05', 'Không', 'Theo dữ liệu',
     'Ở chế độ xử lý vẫn được thêm / thay / xoá tệp.'),
    ('Khu vực Bình luận / Mục Lịch sử', 'Table/Grid', 'Enable', '–', '–', 'Hiển thị', 'Xem FR-12, FR-13.'),
    ('Nút Lưu thông tin', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khoá trong lúc đang lưu.'),
    ('Nút Đóng / ×', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
]


def handle_save(extra_during, after):
    return ('Before:\n– Kiểm tra người dùng còn quyền xử lý hoặc quyền sửa; không → “Bạn không có quyền chỉnh sửa Vấn đề '
            'này hoặc Vấn đề đã đóng.”\n'
            'During:\n' + extra_during + '– Còn lỗi bắt buộc của form (như FR-05) → báo dưới ô, không lưu.\n'
            'After:\n' + after +
            '– Người dùng chỉ có quyền xử lý (không phải Người tạo) → chỉ Trạng thái, Người phụ trách và tệp đính kèm được '
            'ghi nhận.\n'
            '– Ghi lịch sử “Thay đổi trạng thái” (cũ → mới) và “Cập nhật thông tin”.\n'
            '– Hiển thị “Lưu Vấn đề thành công”, đóng popup, tải lại danh sách.')


fn('Xử lý Vấn đề', code='FR-08', group='action',
   rule=('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch '
         'sử.', 'history'),
   intro=dict(
       ten='Xử lý Vấn đề',
       mota='Người phụ trách xử lý cập nhật tiến trình: nhận xử lý (Đang xử lý), báo đã xử lý xong (Đã xử lý xong — gửi '
            'người duyệt) hoặc tự Hoàn thành khi Vấn đề không có người duyệt đóng, làm lại sau khi bị Từ chối, hoặc Đã đóng.',
       tacnhan='Người phụ trách xử lý (Q2)',
       dieukien='Người dùng là Người phụ trách xử lý; Vấn đề ở Đã phân công / Đang xử lý / Từ chối / Mở lại.',
       chinh='1. Người dùng bấm biểu tượng “Xử lý” trên dòng.\n'
             '2. Hệ thống mở popup ở chế độ xử lý: thông tin chỉ đọc, mở ô Trạng thái và tệp đính kèm.\n'
             '3. Người dùng chọn trạng thái mới trong danh sách được phép, đính kèm tệp kết quả nếu cần.\n'
             '4. Người dùng bấm “Lưu thông tin”.\n'
             '5. Hệ thống lưu, báo “Lưu Vấn đề thành công”, đóng popup và tải lại danh sách.',
       phu='• Đang xử lý → chọn “Đã xử lý xong” khi Vấn đề có Người duyệt đóng (gửi thông báo “[ISSUE] Chờ duyệt: <tiêu '
           'đề>. <Tên> gửi bạn duyệt.” cho người duyệt), hoặc “Hoàn thành” khi không có người duyệt.\n'
           '• Từ chối → chọn “Đang xử lý” để làm lại.\n'
           '• Chọn “Đã đóng” → Vấn đề kết thúc, không còn thao tác nào ngoài xem.\n'
           '• Giữ nguyên trạng thái và bấm Lưu → chỉ cập nhật tệp đính kèm.'),
   suffix=' => Xử lý', note=MODAL_NOTE % 'xử lý Vấn đề',
   shots=[('08-xuly.png', 'Popup xử lý Vấn đề “Đang xử lý” — danh sách trạng thái được phép')],
   ui=HANDLE_UI,
   ev=[
       ('Bấm Xử lý trên dòng', 'Click',
        'Before:\n– Nút chỉ hiện khi người dùng có quyền xử lý ở trạng thái hiện tại (BR-03).\n' + NO_ROLE + '\n'
        'After:\n– Mở popup ở chế độ xử lý, nạp chi tiết mới nhất.'),
       ('Bấm Lưu thông tin', 'Click',
        handle_save('',
                    '– Cập nhật trạng thái, ghi thời điểm xử lý xong / hoàn thành / đóng tương ứng.\n'
                    '– Chuyển sang Đã xử lý xong → gửi thông báo cho Người duyệt đóng.\n')),
   ])

# ------------------------------------------------------------------ 2.9 Duyệt đóng / Từ chối
fn('Duyệt đóng / Từ chối', code='FR-09', group='action',
   rule=('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch '
         'sử.', 'history'),
   intro=dict(
       ten='Duyệt đóng / Từ chối',
       mota='Người duyệt đóng xác nhận kết quả xử lý: chấp nhận (Hoàn thành) hoặc trả lại người xử lý (Từ chối, kèm lý do).',
       tacnhan='Người duyệt đóng (Q3)',
       dieukien='Người dùng là Người duyệt đóng; Vấn đề ở trạng thái “Đã xử lý xong”.',
       chinh='1. Người dùng bấm “Xử lý” trên dòng Vấn đề Đã xử lý xong (hoặc mở từ thông báo “Chờ duyệt”).\n'
             '2. Hệ thống mở popup ở chế độ xử lý, ô Trạng thái liệt kê: Đã xử lý xong, Hoàn thành, Từ chối.\n'
             '3. Người dùng chọn “Hoàn thành” để duyệt đóng, hoặc “Từ chối” rồi nhập Lý do từ chối.\n'
             '4. Người dùng bấm “Lưu thông tin”.\n'
             '5. Hệ thống lưu, báo “Lưu Vấn đề thành công”, đóng popup và tải lại danh sách.',
       phu='• Chọn Từ chối mà bỏ trống lý do → “Vui lòng nhập lý do từ chối”, không lưu.\n'
           '• Từ chối → gửi thông báo “[ISSUE] Từ chối: <tiêu đề>. Lý do: <lý do>” cho Người phụ trách xử lý; Vấn đề quay '
           'về hàng đợi của người xử lý.\n'
           '• Hoàn thành → ghi thời điểm hoàn thành, popup chi tiết hiện “Hoàn thành lúc: …”.'),
   suffix=' => Xử lý', note=MODAL_NOTE % 'xử lý Vấn đề',
   shots=[('09-duyet.png', 'Người duyệt mở Vấn đề “Đã xử lý xong” — lựa chọn Hoàn thành / Từ chối'),
          ('09-duyet-chon.png', 'Chọn Từ chối — hiện ô Lý do từ chối bắt buộc')],
   ui=HANDLE_UI,
   ev=[
       ('Bấm Xử lý trên dòng Đã xử lý xong', 'Click',
        'Before:\n– Nút chỉ hiện với Người duyệt đóng khi Vấn đề ở Đã xử lý xong.\n' + NO_ROLE + '\n'
        'After:\n– Mở popup ở chế độ xử lý.'),
       ('Chọn trạng thái Từ chối', 'Change', 'After:\n– Hiện ô “Lý do từ chối *”.'),
       ('Bấm Lưu thông tin', 'Click',
        handle_save('– Từ chối mà Lý do trống → “Vui lòng nhập lý do từ chối”.\n',
                    '– Hoàn thành → lưu trạng thái + thời điểm hoàn thành.\n'
                    '– Từ chối → lưu trạng thái, thời điểm và lý do từ chối; gửi thông báo cho Người phụ trách xử lý.\n')),
   ])

# ------------------------------------------------------------------ 2.10 Mở lại
fn('Mở lại Vấn đề', code='FR-10', group='action',
   rule=('- Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo SRS Các quy tắc chung - Quy tắc ghi lịch '
         'sử.', 'history'),
   intro=dict(
       ten='Mở lại Vấn đề',
       mota='Đưa Vấn đề đã Hoàn thành trở lại trạng thái “Mở lại” khi Vấn đề tái diễn hoặc xử lý chưa đạt.',
       tacnhan='Người tạo (Q1), Người phụ trách xử lý (Q2)',
       dieukien='Vấn đề ở trạng thái Hoàn thành; người dùng là Người tạo hoặc Người phụ trách xử lý.',
       chinh='1. Người dùng bấm “Xử lý” trên dòng Vấn đề Hoàn thành.\n'
             '2. Hệ thống mở popup, ô Trạng thái liệt kê: Hoàn thành, Mở lại.\n'
             '3. Người dùng chọn “Mở lại”, bấm “Lưu thông tin”.\n'
             '4. Hệ thống lưu, ghi lịch sử, báo “Lưu Vấn đề thành công”.\n'
             '5. Từ “Mở lại”: Người tạo giao lại (Đã phân công), Người phụ trách nhận làm (Đang xử lý), hoặc Đã đóng.',
       phu='• Vấn đề Đã đóng không mở lại được (không còn nút Xử lý / Sửa).'),
   suffix=' => Xử lý', note=MODAL_NOTE % 'xử lý Vấn đề',
   shots=[('10-molai.png', 'Vấn đề Hoàn thành — lựa chọn Mở lại')],
   ui=HANDLE_UI,
   ev=[
       ('Bấm Xử lý trên dòng Hoàn thành', 'Click',
        'Before:\n– Nút chỉ hiện với Người tạo / Người phụ trách xử lý khi Vấn đề Hoàn thành.\n' + NO_ROLE + '\n'
        'After:\n– Mở popup ở chế độ xử lý.'),
       ('Bấm Lưu thông tin', 'Click', handle_save('', '– Cập nhật trạng thái Mở lại.\n')),
   ])

# ------------------------------------------------------------------ 2.11 Xóa
fn('Xóa Vấn đề', code='FR-11', group='action',
   rule=('- Thông báo, Quy tắc Xóa. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'delete'),
   intro=dict(
       ten='Xóa Vấn đề',
       mota='Xóa hẳn 1 Vấn đề vừa ghi nhận nhầm, chưa được xử lý.',
       tacnhan='Người tạo Vấn đề (Q1)',
       dieukien='Người dùng là Người tạo; Vấn đề ở trạng thái “Mới ghi nhận”.',
       chinh='1. Người dùng bấm biểu tượng thùng rác “Xóa” trên dòng.\n'
             '2. Hệ thống hiện hộp “Xác nhận xóa Vấn đề”: “Bạn có chắc muốn xóa Vấn đề \'<tiêu đề>\'? Hành động này không '
             'thể hoàn tác.”\n'
             '3. Người dùng bấm “Xóa”.\n'
             '4. Hệ thống xóa, báo “Xóa Vấn đề thành công” và tải lại danh sách.',
       phu='• Bấm “Hủy” / × → đóng hộp, không xóa.\n'
           '• Vấn đề đã chuyển trạng thái / người dùng không phải Người tạo → “Bạn không có quyền xóa Vấn đề này hoặc Vấn '
           'đề không còn ở trạng thái Mới.”\n'
           '• Lỗi khác → nội dung lỗi hoặc “Lỗi khi xóa Vấn đề”.'),
   suffix=' => Xóa', note='Hộp xác nhận được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
   shots=[('11-xoa.png', 'Hộp Xác nhận xóa Vấn đề')],
   ui=[('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận xóa Vấn đề', 'Kèm biểu tượng cảnh báo đỏ.'),
       ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
        '“Bạn có chắc muốn xóa Vấn đề \'<tiêu đề>\'? Hành động này không thể hoàn tác.”'),
       ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Màu đỏ.'),
       ('Nút Hủy / ×', 'Button', 'Enable', 'Hiển thị', '–')],
   ui_kw=dict(required=False, scope=False),
   ev=[
       ('Bấm Xóa trên dòng', 'Click',
        'Before:\n– Nút chỉ hiện khi người dùng là Người tạo và Vấn đề Mới ghi nhận.\n' + NO_ROLE + '\n'
        'After:\n– Mở hộp xác nhận.'),
       ('Bấm Xóa trong hộp', 'Click',
        'Before:\n– Máy chủ kiểm tra lại: Người tạo + Mới ghi nhận; không đạt → “Bạn không có quyền xóa Vấn đề này hoặc '
        'Vấn đề không còn ở trạng thái Mới.”\n'
        'After:\n– Xóa hẳn Vấn đề, “Xóa Vấn đề thành công”, tải lại danh sách.'),
       ('Bấm Hủy / ×', 'Click', 'After:\n– Đóng hộp, không xóa.'),
   ])

# ------------------------------------------------------------------ 2.12 Bình luận
fn('Trao đổi bình luận', code='FR-12', group='crud',
   rule=('- Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'create'),
   intro=dict(
       ten='Trao đổi bình luận',
       mota='Trao đổi trực tiếp trên Vấn đề: viết bình luận, trả lời, nhắc tên đồng nghiệp bằng @, đính kèm tệp, thả cảm '
            'xúc, sửa / xóa bình luận của mình.',
       tacnhan=TACNHAN,
       dieukien='Người dùng mở được popup Chi tiết / Sửa / Xử lý của Vấn đề.',
       chinh='1. Người dùng mở Vấn đề, cuộn tới khu vực “Bình luận”.\n'
             '2. Người dùng gõ nội dung vào ô “Viết bình luận…”, gõ @ để chọn nhân viên cần nhắc, bấm “Đính kèm” để thêm '
             'tệp.\n'
             '3. Người dùng bấm “Gửi” hoặc nhấn Enter.\n'
             '4. Hệ thống lưu bình luận, hiển thị vào luồng, tăng số đếm và gửi thông báo.',
       phu='• Bấm “Trả lời” dưới 1 bình luận → mở ô trả lời ngay dưới (cây trả lời tối đa 3 cấp).\n'
           '• Bình luận của chính mình có “Sửa”, “Xóa”; xóa phải xác nhận “Bạn có chắc muốn xóa bình luận này?”.\n'
           '• Gửi lỗi → “Gửi bình luận thất bại. Thử lại sau.”; sửa lỗi → “Lưu thất bại, vui lòng thử lại.”; xóa lỗi → '
           '“Xóa thất bại, vui lòng thử lại.”\n'
           '• Chưa có bình luận → “Chưa có bình luận nào.”',
       dacbiet='Bình luận gốc → thông báo cho những người giữ vai trò trên Vấn đề; trả lời → thông báo cho người được trả '
               'lời; người được @ nhận thông báo riêng; thả cảm xúc → thông báo cho người viết bình luận.'),
   suffix=' => Mã Vấn đề => Gửi', note='Khu vực Bình luận nằm cuối popup Chi tiết / Sửa / Xử lý Vấn đề.',
   shots=[('12-binhluan.png', 'Khu vực Bình luận trong popup Chi tiết Vấn đề')],
   ui=[('Tiêu đề khu vực + số đếm', 'Label', 'Hiển thị', '–', '–', 'Bình luận n', '–'),
       ('Luồng bình luận', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        'Ảnh đại diện, tên, nội dung, thời điểm, các cảm xúc đã thả; trả lời thụt vào dưới bình luận cha.'),
       ('Ô Viết bình luận…', 'Textarea', 'Enable', '1–5000 ký tự', 'Có', 'Trống',
        'Gõ @ để mở danh sách nhân viên (↑↓ chọn, Enter chèn). Enter = Gửi, Shift+Enter = xuống dòng.'),
       ('Nút Đính kèm', 'Button', 'Enable', 'Nhiều tệp, mỗi tệp ≤ 50MB', 'Không', 'Hiển thị', 'Tệp chọn hiện ngay dưới ô.'),
       ('Nút Xoá (ô soạn)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá nội dung đang soạn và tệp đã chọn.'),
       ('Nút Gửi', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khoá khi chưa có nội dung; “Đang gửi...” khi gửi.'),
       ('Nút Thả cảm xúc', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn emoji; bấm lại đúng emoji để bỏ.'),
       ('Nút Trả lời / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở / đóng ô trả lời.'),
       ('Nút Sửa / Xóa bình luận', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không phải bình luận của mình', '–')],
   ev=[
       ('Gõ @ trong ô bình luận', 'Keypress',
        'After:\n– Tìm nhân viên theo chữ gõ sau @, hiện danh sách; chọn → chèn thẻ tên vào nội dung.'),
       ('Bấm Gửi / Enter', 'Click / Keypress',
        'During:\n– Nội dung trống → không gửi. Nội dung > 5000 ký tự / tệp > 50MB → máy chủ báo lỗi, hiện dưới ô.\n'
        'After:\n– Lưu bình luận (và tệp), thêm vào luồng, gửi thông báo theo Yêu cầu đặc biệt.\n'
        '– Lỗi → “Gửi bình luận thất bại. Thử lại sau.”'),
       ('Bấm Sửa → Lưu', 'Click',
        'Before:\n– Chỉ người viết; người khác → “Bạn không có quyền sửa comment này”.\n'
        'After:\n– Cập nhật nội dung; lỗi → “Lưu thất bại, vui lòng thử lại.”'),
       ('Bấm Xóa → xác nhận', 'Click',
        'Before:\n– Chỉ người viết; người khác → “Bạn không có quyền xoá comment này”.\n'
        'After:\n– Xóa bình luận, tải lại luồng; lỗi → “Xóa thất bại, vui lòng thử lại.”'),
       ('Bấm Thả cảm xúc', 'Click', 'After:\n– Thêm / đổi / bỏ cảm xúc của người dùng trên bình luận.'),
   ])

# ------------------------------------------------------------------ 2.13 Lịch sử
fn('Xem lịch sử',
   rule=('- Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'history'),
   intro=dict(
       ten='Xem lịch sử',
       mota='Xem các lần tạo, cập nhật thông tin và chuyển trạng thái của 1 Vấn đề: ai làm, lúc nào, giá trị cũ → mới.',
       tacnhan=TACNHAN,
       dieukien='Vấn đề nằm trong phạm vi người dùng được xem (không cần quyền riêng).',
       chinh='1. Người dùng bấm biểu tượng đồng hồ “Lịch sử” trên dòng.\n'
             '2. Hệ thống mở popup “Lịch sử chỉnh sửa <Mã>” dạng dòng thời gian, mới nhất ở trên cùng thứ tự ghi.\n'
             '3. Mỗi mốc gồm thời điểm, loại hành động (Tạo mới Vấn đề / Cập nhật thông tin / Thay đổi trạng thái), người '
             'thực hiện và các trường thay đổi (cũ màu đỏ → mới màu xanh).\n'
             '4. Ngoài ra trong popup Chi tiết / Sửa / Xử lý có mục “Lịch sử” thu gọn; bấm “Xem lịch sử” để mở, có Bộ lọc '
             'theo loại hành động, người thực hiện, khoảng ngày.',
       phu='• Chưa có lịch sử → “Chưa có lịch sử thao tác nào.”\n'
           '• Lỗi khi tải → “Lỗi khi tải lịch sử”.\n'
           '• Mục Lịch sử trong popup: lọc không ra kết quả → “Không có lịch sử phù hợp bộ lọc.”; bấm “Làm mới” để tải lại, '
           '“Thu gọn” để đóng.'),
   suffix=' => Lịch sử', note=MODAL_NOTE % 'Lịch sử chỉnh sửa' + ' Mục Lịch sử trong popup Chi tiết:',
   shots=[('13-lichsu.png', 'Popup Lịch sử chỉnh sửa Vấn đề'),
          ('13b-lichsu-chitiet.png', 'Mục Lịch sử mở trong popup Chi tiết Vấn đề')],
   ui=[('Tiêu đề popup', 'Label', 'Hiển thị', '–', 'Lịch sử chỉnh sửa <Mã>', 'Kèm biểu tượng đồng hồ.'),
       ('Dòng thời gian', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Chấm xanh lá = Tạo mới, vàng = Cập nhật thông tin, xanh dương = Thay đổi trạng thái.'),
       ('Thời điểm', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm:ss', 'Theo dữ liệu', '–'),
       ('Người thực hiện', 'Text', 'Read-only', '–', 'Theo dữ liệu', '“— <Tên>”.'),
       ('Trường thay đổi', 'Text', 'Read-only', '–', 'Theo dữ liệu',
        '“<Tên trường>: cũ → mới”; trường danh sách (người theo dõi, phối hợp, tệp) liệt kê dòng bỏ “−” và thêm “+”.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thao tác nào.”'),
       ('Mục Lịch sử (trong popup chi tiết)', 'Table/Grid', 'Enable', '–', 'Thu gọn',
        'Nút Xem lịch sử / Thu gọn, Làm mới, Bộ lọc (Loại hành động, Người thực hiện, Từ ngày, Đến ngày, Làm mới).'),
       ('Nút Đóng / ×', 'Button', 'Enable', '–', 'Hiển thị', '–')],
   ui_kw=dict(required=False),
   ev=[('Bấm Lịch sử trên dòng', 'Click',
        'After:\n– Mở popup, nạp lịch sử của Vấn đề; lỗi → “Lỗi khi tải lịch sử”.'),
       ('Bấm Xem lịch sử (trong popup chi tiết)', 'Click',
        'After:\n– Mở mục, nạp lịch sử lần đầu; chọn bộ lọc → lọc ngay, không cần bấm Tìm.'),
       ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup.')])

# ------------------------------------------------------------------ 2.14 Xuất Excel
fn('Xuất Excel', code='FR-14', group='io',
   rule=('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'excel'),
   intro=dict(
       ten='Xuất Excel',
       mota='Tải về file Excel danh sách Vấn đề theo đúng bộ lọc / sắp xếp đang áp dụng (tất cả các trang), với các cột '
            'người dùng chọn.',
       tacnhan=TACNHAN,
       dieukien=DK_LIST,
       chinh='1. Người dùng bấm “Xuất Excel”.\n'
             '2. Hệ thống mở popup “Chọn trường xuất file”, tích sẵn các cột đang hiện trên bảng.\n'
             '3. Người dùng tích / bỏ tích, kéo ☰ để đổi thứ tự cột trong file.\n'
             '4. Người dùng bấm “Xuất file”.\n'
             '5. Hệ thống tải về file danh_sach_issue.xlsx và báo “Xuất Excel thành công”.',
       phu='• Bấm “Chọn tất cả” / “Bỏ chọn hết” → tích / bỏ toàn bộ; chưa chọn trường nào → nút Xuất file bị khoá.\n'
           '• Lỗi → “Lỗi khi xuất Excel”.\n'
           '• Đang xuất → nút Xuất Excel bị khoá, không bấm lặp được.',
       dacbiet='File gồm tiêu đề “Danh sách issue”, cột STT và các cột đã chọn theo đúng thứ tự.'),
   suffix=' => Xuất Excel => Xuất file', note=MODAL_NOTE % 'Chọn trường xuất file',
   shots=[('14-xuat.png', 'Popup Chọn trường xuất file')],
   ui=[('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất file', 'Kèm biểu tượng tải xuống.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Checkbox', 'Enable', '25 trường', 'Có (≥ 1)', 'Tích các cột đang hiện trên bảng',
        'Mã Vấn đề, Tiêu đề Vấn đề, Mã giải pháp, Tên giải pháp, Version giải pháp, Dự án, Hạng mục/Module, Loại issue, '
        'Nhãn, Người xử lý, Hạn xử lý, Giờ hạn xử lý, Tình trạng hạn, Mức độ ưu tiên, Người theo dõi, Người phối hợp, '
        'Người duyệt, Nguồn phát hiện, Người phát hiện, Ngày phát hiện, Người cập nhật, Ngày cập nhật, Người tạo, Ngày '
        'tạo, Trạng thái.'),
       ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Đang chọn n/25 trường', '–'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khoá khi chưa chọn trường nào / đang xuất.'),
       ('Nút Đóng / ×', 'Button', 'Enable', '–', '–', 'Hiển thị', '–')],
   ev=[('Bấm Xuất Excel', 'Click', 'After:\n– Mở popup, tích sẵn các cột đang hiển thị trên bảng.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được chọn.\n'
        'After:\n– Lấy toàn bộ Vấn đề khớp bộ lọc + sắp xếp hiện tại (không phân trang, vẫn theo phạm vi quyền), dựng file '
        'với các cột đã chọn, tải về danh_sach_issue.xlsx.\n'
        '– “Xuất Excel thành công”; lỗi → “Lỗi khi xuất Excel”.'),
       ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng popup, không xuất.')])

# ========================================================= PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Vấn đề; không lặp lại các quy tắc đã có trong SRS quy tắc '
           'chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi dữ liệu xem được', [
        '– Luôn thấy Vấn đề mình giữ 1 trong 6 vai trò: Người tạo, Người phát hiện, Người phụ trách xử lý, Người duyệt '
        'đóng, Người theo dõi, Người phối hợp.',
        '– Thấy thêm Vấn đề thuộc giải pháp / hạng mục mình là thành viên và dự án TKT mình tham gia (phòng ban hỗ trợ '
        'hoặc qua giải pháp).',
        '– V1 thấy toàn bộ; V2 / V3 / V4 thấy thêm Vấn đề có ít nhất 1 người giữ vai trò hoặc đơn vị xử lý thuộc công ty / '
        'phòng ban – bộ phận / bộ phận mình quản lý.',
    ], ['Xem danh sách', 'Xuất Excel']),
    ('BR-02', 'Luồng 8 trạng thái và người được chuyển', [
        '– Mới ghi nhận: Người tạo → Đã phân công; Người phụ trách → Đang xử lý; Người tạo / Người phụ trách → Đã đóng.',
        '– Đã phân công: Người phụ trách → Đang xử lý; Người tạo / Người phụ trách → Đã đóng.',
        '– Đang xử lý: Người phụ trách → Đã xử lý xong (có Người duyệt đóng) hoặc Hoàn thành (không có người duyệt); '
        'Người tạo / Người phụ trách → Đã đóng.',
        '– Đã xử lý xong: có người duyệt → Người duyệt đóng → Hoàn thành / Từ chối; không có người duyệt → Người tạo / '
        'Người phụ trách → Đang xử lý; Người tạo / Người phụ trách → Đã đóng.',
        '– Từ chối: Người phụ trách → Đang xử lý (xoá lý do từ chối cũ); Người tạo / Người phụ trách → Đã đóng.',
        '– Hoàn thành: Người tạo / Người phụ trách → Mở lại.',
        '– Mở lại: Người tạo → Đã phân công; Người phụ trách → Đang xử lý; Người tạo / Người phụ trách → Đã đóng.',
        '– Đã đóng: trạng thái kết thúc, không chuyển tiếp.',
        '– Tạo mới chỉ được chọn Mới ghi nhận hoặc Đã phân công.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xử lý', 'Duyệt đóng / Từ chối', 'Mở lại']),
    ('BR-03', 'Hiện nút thao tác theo vai trò', [
        '– Sửa: Người tạo, Vấn đề chưa Đã đóng / Hoàn thành.',
        '– Xóa: Người tạo, Vấn đề Mới ghi nhận (xóa hẳn, không khôi phục).',
        '– Xử lý: Người phụ trách khi Đã phân công / Đang xử lý / Từ chối / Mở lại; Người duyệt đóng khi Đã xử lý xong; '
        'Người tạo / Người phụ trách khi Hoàn thành.',
        '– Lịch sử: luôn hiện. Nút không đủ điều kiện thì ẩn hẳn; máy chủ kiểm tra lại khi lưu / xóa.',
    ], ['Xem danh sách', 'Chỉnh sửa', 'Xử lý', 'Xóa']),
    ('BR-04', 'Phải giao cho người hoặc đơn vị', [
        '– Bắt buộc có Người phụ trách xử lý HOẶC Phòng ban xử lý.',
        '– Trạng thái Đã phân công bắt buộc có Người phụ trách xử lý; Từ chối bắt buộc có lý do.',
        '– Giải pháp có hạng mục thì bắt buộc chọn Hạng mục; Vấn đề nội bộ được bỏ trống Giải pháp / Dự án.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xử lý']),
    ('BR-05', 'Thông báo tự động', [
        '– Giao cho đơn vị (chưa có người phụ trách) khi tạo hoặc khi đổi đơn vị: “[ISSUE] Tạo mới: <tiêu đề>. Giao xử lý '
        'cho <đơn vị>.” tới Trưởng bộ phận (không có thì Trưởng phòng ban); bỏ qua nếu trưởng đơn vị chính là người tạo.',
        '– Chuyển Đã xử lý xong: “[ISSUE] Chờ duyệt: <tiêu đề>. <Tên> gửi bạn duyệt.” tới Người duyệt đóng.',
        '– Từ chối: “[ISSUE] Từ chối: <tiêu đề>. Lý do: <lý do>” tới Người phụ trách xử lý.',
        '– Bấm thông báo → mở màn Vấn đề và popup chi tiết Vấn đề đó.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xử lý', 'Duyệt đóng / Từ chối']),
    ('BR-06', 'Hạn xử lý và quá hạn', [
        '– Hạn = Hạn xử lý + Giờ hạn (bỏ trống giờ = 23:59:59).',
        '– Quá hạn khi thời điểm hiện tại đã qua hạn và Vấn đề chưa ở Đã xử lý xong / Đã đóng / Hoàn thành; 3 trạng thái '
        'này không hiện Tình trạng hạn và không tính vào số “Quá hạn”.',
    ], ['Xem danh sách', 'Xuất Excel']),
    ('BR-07', 'Mã và version tự sinh', [
        '– Mã Vấn đề = ISS-<năm><tháng>-<số thứ tự 4 chữ số trong tháng>, vd ISS-202610-0003.',
        '– Khi tạo, nếu có Giải pháp / Hạng mục → ghi lại version hiện hành của giải pháp / hạng mục, không đổi theo '
        'version sau này.',
    ], 'Tạo mới'),
    ('BR-08', 'Thành viên bị khoá khỏi giải pháp', [
        '– Người dùng đã bị khoá khỏi giải pháp thì không tạo được Vấn đề gắn giải pháp đó.',
    ], 'Tạo mới'),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')
