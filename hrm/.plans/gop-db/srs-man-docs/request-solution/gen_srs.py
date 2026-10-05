# -*- coding: utf-8 -*-
"""Sinh "SRS - Yêu cầu làm giải pháp.docx" theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/request-solution/{index,add}.vue · _id/{index,edit}.vue
      components/{RequestSolutionForm,RequestTab,TktTab,MeetingsTab,SalesDeptPanel}.vue
      components/{V2BaseSmartFilterPanel,V2BaseRowActions,V2Footer,FileAttachmentTable}.vue
      components/modal/{filter-customization-modal,column-customization-modal,export-fields-modal,
      base-confirm-modal,V2BaseRejectApproveModal}.vue · components/assign/SystemInfoSection.vue
      Menu: components/subsystem-menu/presale.js (Yêu cầu giải pháp, Dự án TKT)
      Lối vào phụ: pages/assign/prospective-projects/index.vue (hành động dòng) + _id/index.vue (chân màn)
  BE  Modules/Assign/Routes/api.php (prefix assign/request-solutions) · RequestSolutionController
      Services/RequestSolutionService · Services/RequestSolutionHistoryService
      Entities/RequestSolution (STATUSES, generateCode, isCanEdit/Delete/Cancel/Receive)
      Http/Requests/RequestSolution/{RequestSolutionRequest,RequestSolutionCancelRequest}.php
      Transformers/RequestSolutionResource/{RequestSolutionResource,DetailRequestSolutionResource}.php
      app/ExcelExport/ExportColumnRegistry ('request_solutions') · app/Helper/PermissionHelper
      (checkPermissionListWithColumn) · ProspectiveProjectService (getAll forRequestSolution)
  Quyền: PermissionsTableSeeder id 1007–1010, 1012 (nhóm "Yêu cầu làm giải pháp")
Màn Phê duyệt (chờ tiếp nhận) có SRS riêng: "SRS - Phê duyệt yêu cầu giải pháp".
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


TEN_MAN = 'Yêu cầu làm giải pháp'
MENU = 'Phân hệ CSKH trước bán => Yêu cầu giải pháp'
MENU_TKT = 'Phân hệ CSKH trước bán => Dự án TKT'
A_KD = 'Nhân viên kinh doanh (người tạo yêu cầu)'
A_TN = 'Người tiếp nhận yêu cầu (Q1)'
TAC_KD = 'Nhân viên kinh doanh phụ trách dự án TKT; Người dùng đã đăng nhập'
TAC_ALL = 'Nhân viên kinh doanh, người tiếp nhận, quản lý theo phạm vi V1–V4; Người dùng đã đăng nhập'
SRS_PD = 'SRS - Phê duyệt yêu cầu giải pháp'

ICONS = {
    'Phân hệ CSKH trước bán': 'icon_phanhe_cskh.png',
    'Yêu cầu giải pháp': 'icon_man_ycgp.png',
    'Dự án TKT': 'icon_man_tkt.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Cấu hình cột hiển thị': 'icon_cot.png',
    'Xuất Excel': 'icon_xuat.png',
    'Xuất file': 'icon_xuatfile.png',
    'Tạo mới': 'icon_taomoi.png',
    'Lưu nháp': 'icon_luunhap.png',
    'Lưu và gửi': 'icon_luuvagui.png',
    'Tạo yêu cầu làm giải pháp': 'icon_taoycgp_row.png',
    'Mã yêu cầu': 'icon_ma.png',
    'Sửa': 'icon_row_0.png',
    'Xóa': 'icon_row_1.png',
    'Hủy yêu cầu': 'icon_row_2.png',
    'Hủy yêu cầu làm giải pháp': 'icon_huy_ft.png',
    'Làm giải pháp': 'icon_lamgp_row.png',
    'Xem lịch sử': 'icon_xemlichsu.png',
    'Tiếp nhận': 'icon_tiepnhan_ft.png',
    'Từ chối': 'icon_tuchoi_ft.png',
}

NO_OWNER = ('– Không phải người tạo hoặc sai trạng thái → nút không hiển thị; gọi thẳng chức năng thì hệ thống '
            'báo lỗi và dừng xử lý.')

OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN)
d = SrsDoc(out=OUT, menu=MENU, route='', full_url='', img_prefix='ycgp_')
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})
d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Yêu cầu làm giải pháp (danh sách, tạo mới, sửa, xem chi '
    'tiết và các thao tác trên yêu cầu), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn Yêu cầu làm giải pháp.',
    'Làm rõ luồng nhân viên kinh doanh lập yêu cầu từ một dự án tiền khả thi, lưu nháp hoặc gửi sang phòng '
    'giải pháp, sửa / gửi lại sau khi được yêu cầu bổ sung, hủy hoặc xóa yêu cầu.',
    'Làm rõ vòng đời trạng thái của yêu cầu, phạm vi dữ liệu mỗi người được xem và các tác động sang dự án '
    'tiền khả thi (trạng thái dự án, giai đoạn dự án).',
    'Các thao tác của người tiếp nhận (Tiếp nhận, Yêu cầu bổ sung thông tin, Từ chối) được đặc tả đầy đủ ở '
    '%s; tài liệu này chỉ ghi phần nút nằm trên màn Chi tiết yêu cầu.' % SRS_PD,
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Yêu cầu làm giải pháp (YC)', 'Phiếu do nhân viên kinh doanh lập từ một dự án tiền khả thi, gửi sang '
     'phòng giải pháp để làm giải pháp kỹ thuật. Mỗi dự án chỉ có tối đa 1 yêu cầu.'),
    ('GP', 'Giải pháp.'),
    ('Dự án TKT', 'Dự án tiền khả thi — dự án gốc của yêu cầu.'),
    ('KD', 'Kinh doanh — người / phòng lập yêu cầu.'),
    ('Phòng tiếp nhận', 'Phòng giải pháp được chọn trên yêu cầu để nhận và xử lý yêu cầu.'),
    ('Người tiếp nhận', 'Người có quyền Tiếp nhận yêu cầu làm giải pháp, đã bấm Tiếp nhận yêu cầu.'),
    ('Hạn tiếp nhận', 'Thời điểm muộn nhất phòng giải pháp phải phản hồi yêu cầu (cột “Ngày cần tiếp nhận '
     'YC”), hệ thống tự tính khi yêu cầu được gửi.'),
    ('Hình thức triển khai', 'Thuộc tính của dự án TKT: Tự triển khai / Triển khai theo phòng / Liên phòng ban.'),
    ('Phiếu thu thập thông tin', 'Bộ câu hỏi khảo sát gắn với dự án TKT; phải trả lời đủ câu bắt buộc mới gửi '
     'được yêu cầu.'),
    ('Trạng thái (Tiến trình YC)', 'Nháp · Chờ tiếp nhận · Yêu cầu bổ sung · Đã tiếp nhận · Từ chối · Đã hủy · '
     'Đang thực hiện · Đã hoàn thành · Đóng · Đã chốt giải pháp.'),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Tiếp nhận yêu cầu làm giải pháp',
     'Hiện nút Tiếp nhận, Từ chối và tab Phiếu thu thập thông tin ở màn Chi tiết đối với yêu cầu đang Chờ '
     'tiếp nhận thuộc phòng người dùng quản lý (đặc tả ở %s).' % SRS_PD),
], widths=[0.8, 2.0, 3.2])
d.p('Các chức năng còn lại (xem danh sách, tìm kiếm, cấu hình bộ lọc / cột, xuất Excel, tạo mới, xem chi tiết, '
    'lịch sử) KHÔNG gắn quyền thao tác riêng — mọi người dùng đã đăng nhập vào được menu. Sửa, Xóa, Hủy, Gửi '
    'lại chỉ dành cho NGƯỜI TẠO yêu cầu và phụ thuộc trạng thái (xem Phần 4).')
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem danh sách yêu cầu làm giải pháp theo tổng công ty',
     'Toàn bộ yêu cầu. Hiện đủ 3 ô lọc Công ty, Phòng ban, Bộ phận.'),
    ('V2', 'Xem danh sách yêu cầu làm giải pháp theo công ty',
     'Yêu cầu lập tại công ty đang làm việc + yêu cầu mình là người tiếp nhận. Hiện ô lọc Phòng ban, Bộ phận.'),
    ('V3', 'Xem danh sách yêu cầu làm giải pháp theo phòng ban',
     'Yêu cầu do phòng ban / bộ phận mình quản lý lập + yêu cầu mình tạo + yêu cầu mình là người tiếp nhận. '
     'Hiện ô lọc Phòng ban, Bộ phận.'),
    ('V4', 'Xem danh sách yêu cầu làm giải pháp theo bộ phận',
     'Yêu cầu do bộ phận mình quản lý lập + yêu cầu mình tạo + yêu cầu mình là người tiếp nhận. Hiện ô lọc '
     'Bộ phận.'),
], widths=[0.8, 2.6, 2.6])
d.p('Không có quyền V nào → chỉ thấy yêu cầu do chính mình tạo hoặc mình là người tiếp nhận. Có nhiều quyền V '
    'thì áp quyền rộng nhất. Ở mọi phạm vi, yêu cầu trạng thái Nháp chỉ hiển thị với người tạo.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách yêu cầu làm giải pháp', '✅', '✅ (dữ liệu theo V1–V4)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅'),
    ('FR-04 Tuỳ chỉnh cột', '✅', '✅'),
    ('FR-05 Xuất Excel', '✅', '✅'),
    ('FR-06 Tạo mới yêu cầu làm giải pháp', '✅', '✅ (dự án TKT do mình tạo)'),
    ('FR-07 Xem chi tiết yêu cầu', '✅', '✅'),
    ('FR-08 Sửa yêu cầu', '✅ (chỉ người tạo)', '✅ (chỉ người tạo)'),
    ('FR-09 Cập nhật bổ sung và gửi lại', '✅ (chỉ người tạo)', '✅ (chỉ người tạo)'),
    ('FR-10 Xóa yêu cầu', '✅ (chỉ người tạo)', '✅ (chỉ người tạo)'),
    ('FR-11 Hủy yêu cầu', '✅ (chỉ người tạo)', '✅ (chỉ người tạo)'),
    ('FR-12 Xem lịch sử thay đổi', '✅', '✅'),
    ('FR-13 Làm giải pháp (lối tắt)', '✅ (người đã tiếp nhận)', '❌'),
    ('FR-14 Tiếp nhận / Từ chối tại màn chi tiết', '✅', '❌'),
], widths=[3.0, 1.5, 1.5])

# ========================================================= PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_KD, [0, 1, 2, 3, 4, 5, 6]), (A_TN, [0, 7, 8])],
    [('FR-01', 'Xem danh sách yêu cầu', 'view'),
     ('FR-05', 'Xuất Excel', 'io'),
     ('FR-06', 'Tạo mới yêu cầu', 'crud'),
     ('FR-08', 'Sửa yêu cầu', 'crud'),
     ('FR-09', 'Cập nhật bổ sung và gửi lại', 'crud'),
     ('FR-10', 'Xóa yêu cầu', 'action'),
     ('FR-11', 'Hủy yêu cầu', 'action'),
     ('FR-13', 'Làm giải pháp (lối tắt)', 'action'),
     ('FR-14', 'Tiếp nhận / Từ chối', 'action')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-07', 'Xem chi tiết yêu cầu', 'view', 'extend', [0], None),
     ('FR-12', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

_no = [0]


def menu_lines(suffix='', tkt=None):
    d.p('Đường dẫn màn hình:')
    d._menu_para(MENU + suffix)
    if tkt:
        for t in tkt:
            d._menu_para(MENU_TKT + t)


def fn(ten, code=None, group='view', actor=A_KD, rule=None, intro=None, suffix='', tkt=None, note=None,
       shots=(), ui=None, ui_kw=None, ev=None):
    if not ui or not ev:
        raise ValueError('Chức năng "%s" thiếu bảng giao diện / event' % ten)
    _no[0] += 1
    n = _no[0]
    d.h3('2.%d %s' % (n, ten))
    k = 0
    if code:
        k += 1
        d.p('2.%d.%d Biểu đồ Usecase' % (n, k))
        d.uc_figure(code, ten, group, actor=actor)
    k += 1
    d.p('2.%d.%d Giới thiệu' % (n, k))
    d.rule_ref(rule[0], anchor=rule[1])
    d.intro_table(**intro)
    k += 1
    d.p('2.%d.%d Layout màn hình' % (n, k))
    menu_lines(suffix, tkt)
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


MODAL = 'Cửa sổ %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'

# ------------------------------------------------------------------ 2.1 Xem danh sách
fn('Xem danh sách yêu cầu làm giải pháp',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của '
         'màn Yêu cầu làm giải pháp tại phần mô tả chi tiết.', 'list'),
   intro=dict(
       ten='Xem danh sách yêu cầu làm giải pháp',
       mota='Hiển thị các yêu cầu làm giải pháp trong phạm vi người dùng được xem, kèm tiến trình, nhãn hạn xử lý, '
            'người tiếp nhận, mã giải pháp đã sinh và các nút thao tác trên từng dòng.',
       tacnhan=TAC_ALL,
       dieukien='Người dùng đã đăng nhập.',
       chinh='1. Người dùng vào menu Yêu cầu giải pháp của phân hệ CSKH trước bán.\n'
             '2. Hệ thống khôi phục bộ lọc lần trước (nếu quay lại màn trong vòng 10 phút) và nạp trang 1, '
             '10 dòng/trang, yêu cầu mới tạo lên đầu.\n'
             '3. Bảng hiển thị đủ các cột (mặc định hiện hết), dòng “Hiển thị a–b / N” và thanh phân trang.\n'
             '4. Người dùng bấm tiêu đề cột có biểu tượng sắp xếp, chuyển trang hoặc đổi số dòng/trang.',
       phu='• Không có dữ liệu → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
           '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”, bảng rỗng.\n'
           '• Bấm Mã yêu cầu → mở màn Chi tiết (FR-07); bấm Mã GP → mở màn chi tiết giải pháp.'),
   shots=[('01-ds.png', 'Màn danh sách yêu cầu làm giải pháp lúc mới truy cập'),
          ('01c-ds-hanhdong.png', 'Phần bên phải bảng: cột Tiến trình YC và cột Hành động (nút hiện theo trạng thái và vai trò)')],
   ui=[
       ('Tiêu đề bảng “Danh sách yêu cầu làm giải pháp”', 'Label', 'Hiển thị', '–', 'Hiển thị', '–'),
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', 'Mở màn Tạo yêu cầu (FR-06).'),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        'Mở cửa sổ Chọn trường xuất file (FR-05); khóa trong lúc đang xuất.'),
       ('Nút Cấu hình cột hiển thị (biểu tượng cột)', 'Icon Button', 'Enable', '–', 'Hiển thị',
        'Mở cửa sổ Tuỳ chỉnh cột (FR-04).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự', 'Đánh số liên tục qua các trang; cố định khi cuộn ngang.'),
       ('Cột Mã yêu cầu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Liên kết mở màn Chi tiết (chuột phải mở tab mới); sắp xếp được; cố định khi cuộn ngang.'),
       ('Cột Tên yêu cầu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Tối đa 2 dòng; dòng dưới là nhãn hạn xử lý (xem BR-07). Sắp xếp được.'),
       ('Cột Dự án TKT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '“Mã dự án - Tên dự án”.'),
       ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '“Mã khách hàng - Tên khách hàng”.'),
       ('Cột Giai đoạn dự án', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Giai đoạn chọn trên yêu cầu.'),
       ('Cột Mức độ ưu tiên', 'Badge', 'Read-only', '–', 'Theo dữ liệu',
        'Mức độ ưu tiên theo giai đoạn của dự án TKT; màu theo danh mục mức độ ưu tiên.'),
       ('Cột Ngày gửi YC', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
        'Dòng dưới là giờ gửi (hh:mm:ss). Trống khi chưa gửi. Sắp xếp được.'),
       ('Cột Ngày cần tiếp nhận YC', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
        'Hạn tiếp nhận; dòng dưới là giờ. Sắp xếp được.'),
       ('Cột Ngày chốt GP', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
        'Ngày dự kiến xong GP do người tiếp nhận chọn. Sắp xếp được.'),
       ('Cột Ngày KH cần GP', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Sắp xếp được.'),
       ('Cột Phòng KD', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Phòng của người tạo yêu cầu.'),
       ('Cột Phòng tiếp nhận YC', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
       ('Cột Người tiếp nhận YC', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Họ tên người tiếp nhận (chưa có thì hiện PM làm GP); dòng dưới là số điện thoại.'),
       ('Cột Mã GP', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Mã giải pháp sinh từ yêu cầu, là liên kết mở giải pháp; trống khi chưa có.'),
       ('Cột PM làm GP', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'PM của giải pháp kèm số điện thoại.'),
       ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        'Người tạo hiển thị “Tên - Mã phòng”. Ngày tạo sắp xếp được (mặc định giảm dần).'),
       ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        'Ngày cập nhật sắp xếp được.'),
       ('Cột Tiến trình YC', 'Badge', 'Read-only', '–', 'Theo dữ liệu', 'Chữ và màu trạng thái do hệ thống trả (BR-01).'),
       ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
        'Tối đa 3 nút trên dòng, nhiều hơn thì 2 nút + nút “⋮ Hành động khác”: Sửa (FR-08/FR-09), Xóa (FR-10), '
        'Làm giải pháp (FR-13), Hủy yêu cầu (FR-11). Nút không đủ điều kiện bị ẩn hẳn.'),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả', 'N là tổng số yêu cầu khớp bộ lọc.'),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách', '10', 'Đổi thì quay về trang 1.'),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Về đầu / lùi / số trang / tiến / về cuối.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
       ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Hiển thị', 'Hiện trong lúc nạp dữ liệu.'),
   ], ui_kw=dict(required=False),
   ev=[
       ('Mở màn hình', 'System',
        'During:\n– Khôi phục bộ lọc đã lưu (nếu rời màn chưa quá 10 phút).\n'
        '– Lấy yêu cầu theo phạm vi V1–V4 (Phần 2); yêu cầu Nháp chỉ lấy của chính người dùng.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, Ngày tạo giảm dần; tính nhãn hạn và các nút thao tác cho từng dòng.'),
       ('Bấm tiêu đề cột sắp xếp được', 'Click', 'After:\n– Sắp xếp theo cột đó, bấm lại để đảo chiều; quay về trang 1.'),
       ('Bấm số trang / đổi Số dòng/trang', 'Click / Change',
        'After:\n– Nạp lại dữ liệu, giữ bộ lọc và thứ tự sắp xếp; đổi số dòng/trang thì về trang 1.'),
       ('Bấm Mã yêu cầu / Mã GP', 'Click', 'After:\n– Mở màn Chi tiết yêu cầu (FR-07) / màn chi tiết giải pháp.'),
       ('Bấm nút trên cột Hành động', 'Click', 'After:\n– Thực hiện FR-08 / FR-09 / FR-10 / FR-11 / FR-13 tương ứng.'),
   ])

# ------------------------------------------------------------------ 2.2 Tìm kiếm và lọc
fn('Tìm kiếm và lọc',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu làm giải pháp '
         'tại phần mô tả chi tiết.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc yêu cầu làm giải pháp',
       mota='Tìm nhanh theo mã / tên yêu cầu và lọc nâng cao theo đơn vị người tạo, nhân viên gửi, tiến trình, '
            'phòng / người tiếp nhận, giai đoạn dự án, khoảng ngày tạo — luôn trong phạm vi dữ liệu của người dùng.',
       tacnhan=TAC_ALL,
       dieukien='Đang ở màn danh sách.',
       chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
             '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc và chọn điều kiện.\n'
             '3. Đổi một ô chọn trong khối lọc → hệ thống tự lọc lại ngay, không cần bấm Tìm kiếm.\n'
             '4. Bảng hiển thị kết quả từ trang 1.',
       phu='• Bấm Làm mới → xóa mọi điều kiện (kể cả ô tìm nhanh), nạp lại danh sách 1 lần từ trang 1.\n'
           '• Đổi Công ty / Phòng ban → các ô cấp dưới đã chọn bị xóa.\n'
           '• Không có kết quả → “Không có dữ liệu phù hợp bộ lọc.”\n'
           '• Bấm “Ẩn tìm kiếm nâng cao” → thu gọn khối lọc, điều kiện đang chọn vẫn giữ.'),
   suffix=' => Tìm kiếm nâng cao',
   shots=[('02-loc.png', 'Khối Tìm kiếm nâng cao đang mở')],
   ui=[
       ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
        'Placeholder “Tìm theo mã yêu cầu, tên yêu cầu”. Tìm gần đúng theo Mã hoặc Tên yêu cầu; chỉ áp dụng khi '
        'bấm Tìm kiếm / Enter.'),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
       ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
        'Mở / đóng khối lọc nâng cao.'),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (FR-03).'),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Trống',
        'Chỉ mở với quyền V1. Lọc theo công ty của NGƯỜI TẠO yêu cầu.'),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Phòng ban của công ty đã chọn', 'Không', 'Trống',
        'Mở với V1, V2, V3. Lọc theo phòng ban của người tạo.'),
       ('Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Bộ phận của phòng đã chọn', 'Không', 'Trống',
        'Mở với V1–V4. Lọc theo bộ phận của người tạo.'),
       ('Nhân viên gửi yêu cầu', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        'Lọc đúng theo người tạo yêu cầu.'),
       ('Tiến trình yêu cầu', 'Dropdown', 'Enable', 'Danh sách 9 giá trị', 'Không', 'Trống',
        'Nháp, Chờ tiếp nhận, Yêu cầu bổ sung, Đã tiếp nhận, Từ chối, Đã hủy, Đang thực hiện, Đã hoàn thành, Đóng.'),
       ('Phòng tiếp nhận YC', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Không', 'Trống', '–'),
       ('Người tiếp nhận YC', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        'Lọc theo người đã bấm Tiếp nhận.'),
       ('Giai đoạn dự án', 'Dropdown', 'Enable', 'Danh sách giai đoạn dự án', 'Không', 'Trống',
        'Có icon ⓘ mô tả giai đoạn; giai đoạn đã khóa đang được lọc vẫn hiển thị kèm 🔒.'),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống',
        'Một ô chọn khoảng ngày; lọc ngày tạo trong khoảng (tính cả 2 đầu).'),
   ],
   ev=[
       ('Bấm Tìm kiếm / Enter ở ô tìm nhanh', 'Click / Keypress',
        'After:\n– Lọc gần đúng theo Mã hoặc Tên yêu cầu kết hợp điều kiện lọc nâng cao; hiển thị trang 1.'),
       ('Đổi giá trị một ô lọc nâng cao', 'Change',
        'After:\n– Tự lọc lại ngay theo toàn bộ điều kiện, quay về trang 1.\n'
        '– Lưu bộ lọc để khôi phục khi quay lại màn trong 10 phút.'),
       ('Bấm Làm mới', 'Click',
        'After:\n– Xóa mọi điều kiện, trả sắp xếp về Ngày tạo giảm dần, nạp lại trang 1 (1 lần).'),
   ])

# ------------------------------------------------------------------ 2.3 Cài đặt bộ lọc
fn('Cài đặt bộ lọc',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Yêu cầu làm giải pháp '
         'tại phần mô tả chi tiết.', 'search'),
   intro=dict(
       ten='Cài đặt bộ lọc',
       mota='Cho người dùng chọn tiêu chí lọc nào hiển thị trong khối Tìm kiếm nâng cao và sắp xếp thứ tự các '
            'tiêu chí. Cài đặt lưu riêng cho từng người dùng, theo màn này.',
       tacnhan=TAC_ALL,
       dieukien='Đang ở màn danh sách.',
       chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 7 tiêu chí kèm ô tích.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng ⠿ để đổi thứ tự.\n'
             '4. Bấm Lưu → hệ thống lưu cấu hình, thông báo “Cập nhật thành công”, khối lọc cập nhật theo.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ 7 tiêu chí theo thứ tự gốc; phải bấm Lưu mới ghi nhận.\n'
           '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
           '• Bỏ tích một tiêu chí đang có giá trị lọc → giá trị đó bị xóa khỏi bộ lọc.\n'
           '• Lỗi khi lưu → “Thao tác thất bại”.'),
   suffix=' => Cài đặt bộ lọc', note=MODAL % 'Cài đặt bộ lọc',
   shots=[('03-cai-dat-loc.png', 'Cửa sổ Cài đặt bộ lọc')],
   ui=[
       ('Tiêu đề “Cài đặt bộ lọc”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        'Kèm hướng dẫn “Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo '
        'từng màn hình.”'),
       ('Tiêu chí Công ty – Phòng ban – Bộ phận', 'Checkbox', 'Enable', '–', 'Không', 'Tích', 'Kéo thả được.'),
       ('Tiêu chí Nhân viên gửi yêu cầu', 'Checkbox', 'Enable', '–', 'Không', 'Tích', 'Kéo thả được.'),
       ('Tiêu chí Tiến trình yêu cầu', 'Checkbox', 'Enable', '–', 'Không', 'Tích', 'Kéo thả được.'),
       ('Tiêu chí Phòng tiếp nhận YC', 'Checkbox', 'Enable', '–', 'Không', 'Tích', 'Kéo thả được.'),
       ('Tiêu chí Người tiếp nhận YC', 'Checkbox', 'Enable', '–', 'Không', 'Tích', 'Kéo thả được.'),
       ('Tiêu chí Giai đoạn dự án', 'Checkbox', 'Enable', '–', 'Không', 'Tích', 'Kéo thả được.'),
       ('Tiêu chí Ngày tạo', 'Checkbox', 'Enable', '–', 'Không', 'Tích', 'Kéo thả được.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình và đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Trả về 7 tiêu chí theo thứ tự gốc.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở cửa sổ với cấu hình đang áp dụng.'),
       ('Bấm Lưu', 'Click',
        'During:\n– Ghi cấu hình tiêu chí lọc cho người dùng, riêng màn Yêu cầu làm giải pháp.\n'
        'After:\n– Khối lọc hiển thị theo cấu hình mới; thông báo “Cập nhật thành công”.\n'
        '– Lỗi → “Thao tác thất bại”.'),
       ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Tích lại đủ 7 tiêu chí theo thứ tự gốc trong cửa sổ.'),
       ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------------ 2.4 Tuỳ chỉnh cột
fn('Tuỳ chỉnh cột',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của '
         'màn Yêu cầu làm giải pháp tại phần mô tả chi tiết.', 'list'),
   intro=dict(
       ten='Tuỳ chỉnh cột hiển thị',
       mota='Cho người dùng ẩn / hiện và đổi thứ tự các cột của bảng. Cấu hình lưu riêng cho người dùng, theo màn '
            'này (không ảnh hưởng màn Phê duyệt yêu cầu giải pháp).',
       tacnhan=TAC_ALL,
       dieukien='Đang ở màn danh sách.',
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị (biểu tượng cột, góc phải phía trên bảng).\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê đủ 21 cột kèm ô tích.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng ☰ để đổi vị trí.\n'
             '4. Bấm Lưu → bảng hiển thị theo cấu hình mới, thông báo “Cập nhật thành công”.',
       phu='• Cột STT, Mã yêu cầu, Hành động bị khóa: không bỏ tích, không kéo đổi vị trí được (hiện ổ khóa).\n'
           '• Bấm Đóng / dấu × → không lưu, danh sách cột trở về cấu hình đang áp dụng.\n'
           '• Lỗi khi lưu → “Thao tác thất bại”.'),
   suffix=' => Cấu hình cột hiển thị', note=MODAL % 'Tuỳ chỉnh cột',
   shots=[('04-cot.png', 'Cửa sổ Tuỳ chỉnh cột')],
   ui=[
       ('Tiêu đề “Tuỳ chỉnh cột”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
       ('Dòng cột STT, Mã yêu cầu, Hành động', 'Checkbox', 'Disable', '–', '–', 'Tích',
        'Cột bắt buộc, có biểu tượng ổ khóa, không ẩn / không đổi vị trí được.'),
       ('Dòng các cột còn lại (Tên yêu cầu … Tiến trình YC)', 'Checkbox', 'Enable', '18 cột', 'Không', 'Tích',
        'Mặc định hiện hết; kéo ☰ để đổi vị trí.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình và đóng cửa sổ.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
   ],
   ev=[
       ('Bấm nút Cấu hình cột hiển thị', 'Click', 'After:\n– Mở cửa sổ với cấu hình cột đang áp dụng.'),
       ('Bấm Lưu', 'Click',
        'During:\n– Ghi cấu hình cột cho người dùng, riêng màn Yêu cầu làm giải pháp.\n'
        'After:\n– Bảng hiển thị theo cấu hình mới; thông báo “Cập nhật thành công”.\n– Lỗi → “Thao tác thất bại”.'),
       ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, trả danh sách cột về cấu hình đang áp dụng.'),
   ])

# ------------------------------------------------------------------ 2.5 Xuất Excel
fn('Xuất Excel', code='FR-05', group='io',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất Excel danh sách yêu cầu làm giải pháp',
       mota='Tải về tệp danh_sach_yeu_cau_lam_giai_phap.xlsx gồm TẤT CẢ yêu cầu khớp bộ lọc đang áp dụng (không '
            'giới hạn theo trang), với các trường người dùng chọn.',
       tacnhan=TAC_ALL,
       dieukien='Đang ở màn danh sách.',
       chinh='1. Người dùng (tuỳ chọn) đặt bộ lọc trên màn danh sách.\n'
             '2. Bấm Xuất Excel → hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn các trường ứng với cột '
             'đang hiện trên bảng.\n'
             '3. Người dùng tích / bỏ tích trường, kéo ☰ để đổi thứ tự cột trong tệp.\n'
             '4. Bấm Xuất file → trình duyệt tải tệp về, thông báo “Xuất Excel thành công”.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích toàn bộ 25 trường.\n'
           '• Không chọn trường nào → nút Xuất file bị khóa.\n'
           '• Lỗi khi dựng tệp → “Lỗi khi xuất Excel”, không tải tệp.',
       dacbiet='Tệp có tiêu đề “Danh sách yêu cầu làm giải pháp”, cột STT ở đầu, thứ tự cột theo thứ tự trong cửa '
               'sổ. Phạm vi dữ liệu giống hệt màn danh sách (V1–V4, Nháp chỉ của mình). Trong lúc đang xuất, nút '
               'Xuất Excel bị khóa để tránh bấm lặp.'),
   suffix=' => Xuất Excel => Xuất file', note=MODAL % 'Chọn trường xuất file',
   shots=[('05-xuat.png', 'Cửa sổ Chọn trường xuất file')],
   ui=[
       ('Tiêu đề “Chọn trường xuất file”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        'Kèm hướng dẫn “Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file.”'),
       ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích / bỏ tích mọi trường.'),
       ('Danh sách trường', 'Checkbox', 'Enable', '25 trường', 'Có (≥ 1)', 'Tích sẵn các cột đang hiện',
        'Mã yêu cầu, Tên yêu cầu, Mã / Tên dự án TKT, Mã / Tên khách hàng, Giai đoạn dự án, Mức độ ưu tiên, '
        'Tiến trình yêu cầu, Ngày gửi yêu cầu, Ngày cần tiếp nhận, Ngày chốt giải pháp, Ngày KH cần giải pháp, '
        'Phòng kinh doanh, Phòng tiếp nhận, Người tiếp nhận, SĐT người tiếp nhận, Mã giải pháp, PM làm giải '
        'pháp, Lý do từ chối, Lý do hủy, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. Các trường đang '
        'hiện trên bảng xếp lên đầu, tích sẵn (mặc định 20/25).'),
       ('Dòng “Đang chọn x/y trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', 'Đếm số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        'Khóa khi chưa chọn trường nào hoặc đang xuất.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện.'),
       ('Bấm Xuất file', 'Click',
        'During:\n– Lấy toàn bộ yêu cầu theo phạm vi dữ liệu, bộ lọc và thứ tự sắp xếp đang áp dụng (bỏ qua '
        'phân trang).\n– Chỉ xuất các trường đã chọn, theo thứ tự đã kéo.\n'
        'After:\n– Tải tệp danh_sach_yeu_cau_lam_giai_phap.xlsx; thông báo “Xuất Excel thành công”.\n'
        '– Lỗi → “Lỗi khi xuất Excel”.'),
       ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
   ])

# ------------------------------------------------------------------ 2.6 Tạo mới
FORM_UI = [
    ('Thanh tab', 'Tab', 'Enable', '3 tab', '–', 'Thông tin yêu cầu',
     'Thông tin yêu cầu · Dự án tiền khả thi (chỉ đọc, đổ theo dự án đã chọn) · Meetings (meeting của dự án).'),
    ('Dự án tiền khả thi', 'Dropdown', 'Enable', 'Danh sách dự án hợp lệ', 'Có', 'Trống',
     'Placeholder “-- Chọn dự án --”. Chỉ liệt kê dự án do chính người dùng tạo, chưa có yêu cầu, không phải '
     'dự án Tự triển khai, không phải dự án cha, phiếu thu thập đã trả lời đủ câu bắt buộc (BR-02).'),
    ('Tên yêu cầu', 'Textbox', 'Enable', '1–255 ký tự, không trùng', 'Có', 'Trống',
     'Placeholder “VD: Yêu cầu làm giải pháp dây chuyền gara...”.'),
    ('Phòng tiếp nhận yêu cầu', 'Dropdown', 'Enable / Disable', 'Danh sách phòng ban', 'Có', 'Trống',
     'Placeholder “-- Chọn phòng tiếp nhận --”. Dự án Triển khai theo phòng → tự gán phòng KD phụ trách dự án '
     'và khóa ô (BR-04).'),
    ('Ứng dụng', 'Textbox', 'Read-only', '–', '–', 'Theo dự án', 'Kế thừa từ dự án TKT, có icon ⓘ mô tả.'),
    ('Nhóm ngành', 'Dropdown', 'Enable', 'Nhóm ngành thuộc Ứng dụng', 'Không', 'Theo dự án',
     'Placeholder “Chọn nhóm ngành”. Tự điền theo dự án; chỉ chọn được nhóm ngành khai trong Ứng dụng.'),
    ('Nhóm giải pháp', 'Dropdown', 'Enable', 'Nhóm giải pháp thuộc Ứng dụng', 'Không', 'Theo dự án',
     'Placeholder “Chọn nhóm giải pháp”. Tự điền theo dự án.'),
    ('Giai đoạn dự án', 'Dropdown', 'Enable', 'Danh sách giai đoạn', 'Có khi Lưu và gửi', 'Giai đoạn hiện tại của dự án',
     'Có icon ⓘ mô tả giai đoạn. Khi gửi đi sẽ đồng bộ về dự án TKT (BR-05).'),
    ('Ngày KH cần giải pháp', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Theo dự án',
     'Tự điền “Ngày KH cần giải pháp” của dự án TKT nếu đang trống.'),
    ('Ngày KH cần báo giá', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Trống', '–'),
    ('Ngày cần nhận GP nội bộ', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Theo dự án',
     'Tự điền “Ngày chốt GP nội bộ” của dự án TKT nếu đang trống.'),
    ('Mô tả / ghi chú yêu cầu', 'Textarea', 'Enable', '0–1.000 ký tự', 'Không', 'Trống',
     'Placeholder “Mô tả ngắn nội dung yêu cầu, phạm vi, tài liệu đầu vào...”.'),
    ('Bảng File gửi kèm', 'Table/Grid', 'Enable', '.jpg .jpeg .png .doc .docx .xls .xlsx .pdf, ≤ 20MB/tệp',
     'Không', 'Chưa có tệp', 'Nút “Thêm file”; cột STT, Tên tài liệu, File đính kèm, Dung lượng, Thao tác. '
     'Trống hiện “Chưa có tài liệu đính kèm. Bấm Thêm file để bắt đầu.”'),
    ('Khối Phụ trách KD nội bộ', 'Label', 'Read-only', '–', '–', 'Theo dự án',
     'Phòng KD phụ trách chính, KD phụ trách chính (họ tên, SĐT, email), Phòng KD hỗ trợ & KD hỗ trợ.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Chữ đỏ ngay dưới ô bị lỗi.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu ở trạng thái Nháp.'),
    ('Nút Lưu và gửi', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi “Xác nhận lưu và gửi” – “Bạn đồng ý lưu và gửi?” (nút Xác nhận / Hủy) rồi gửi đi.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn danh sách, không lưu.'),
]

SAVE_DURING = ('During:\n– Dự án trống → “Bắt buộc phải nhập”; dự án đã có yêu cầu → “Dự án tiền khả thi này đã '
               'tồn tại yêu cầu làm giải pháp.”; dự án không tồn tại → “Dự án tiền khả thi không tồn tại.”\n'
               '– Dự án cha → “Dự án cha không làm giải pháp kỹ thuật. Vui lòng tạo yêu cầu trên dự án con.”; '
               'dự án Tự triển khai → “Dự án tự triển khai không cần tạo yêu cầu làm giải pháp.”\n'
               '– Tên yêu cầu trống → “Bắt buộc phải nhập”; quá 255 ký tự → “Tiêu đề không được vượt quá 255 ký '
               'tự.”; trùng → “Tiêu đề đã tồn tại.”\n'
               '– Phòng tiếp nhận / Ngày KH cần giải pháp / Ngày KH cần báo giá trống → “Bắt buộc phải nhập”.\n'
               '– Nhóm ngành / Nhóm giải pháp không thuộc Ứng dụng → “Nhóm ngành không thuộc Ứng dụng của dự án.” '
               '/ “Nhóm giải pháp không thuộc Ứng dụng của dự án.”\n'
               '– Mô tả quá 1.000 ký tự → “Ghi chú không được vượt quá 1000 ký tự.”\n'
               '– Có lỗi → báo đỏ dưới từng ô + thông báo “Vui lòng kiểm tra lại thông tin”, không lưu.\n')
SEND_DURING = ('– (Chỉ khi Lưu và gửi) Giai đoạn dự án trống → “Vui lòng chọn giai đoạn dự án.”; phiếu thu thập '
               'thông tin của dự án còn câu bắt buộc chưa trả lời → “Phiếu thu thập thông tin chưa đủ các trường '
               'yêu cầu”, không lưu.\n')
SEND_AFTER = ('– Lưu và gửi: trạng thái Chờ tiếp nhận; ghi Ngày gửi = thời điểm hiện tại; tính Hạn tiếp nhận '
              '(BR-06); đồng bộ Giai đoạn dự án về dự án TKT; dự án TKT chuyển sang bước chờ tiếp nhận làm giải '
              'pháp; gửi thông báo “Bạn có yêu cầu làm giải pháp mới cần tiếp nhận: <Mã> - <Tên>” cho người có '
              'quyền Q1 thuộc phòng tiếp nhận và người quản lý phòng đó.\n')

fn('Tạo mới yêu cầu làm giải pháp', code='FR-06', group='crud',
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo mới yêu cầu làm giải pháp',
       mota='Nhân viên kinh doanh lập yêu cầu làm giải pháp cho một dự án tiền khả thi do mình phụ trách; lưu nháp '
            'để hoàn thiện sau, hoặc lưu và gửi ngay sang phòng giải pháp.',
       tacnhan=TAC_KD,
       dieukien='Người dùng đã đăng nhập; có ít nhất 1 dự án TKT hợp lệ do chính mình tạo (BR-02).',
       chinh='1. Người dùng bấm “Tạo mới” trên màn danh sách (hoặc nút “Tạo yêu cầu làm giải pháp” ở dòng / chân màn '
             'chi tiết dự án TKT — khi đó ô Dự án tiền khả thi được chọn sẵn).\n'
             '2. Hệ thống mở màn “Tạo yêu cầu giải pháp”, tab Thông tin yêu cầu.\n'
             '3. Người dùng chọn Dự án tiền khả thi → hệ thống tự điền Ứng dụng, Nhóm ngành, Nhóm giải pháp, '
             'Giai đoạn dự án, Ngày KH cần giải pháp, Ngày cần nhận GP nội bộ, khối Phụ trách KD nội bộ, tab Dự án '
             'tiền khả thi và tab Meetings theo dự án.\n'
             '4. Người dùng nhập Tên yêu cầu, chọn Phòng tiếp nhận, nhập Ngày KH cần báo giá, Mô tả, đính kèm tệp.\n'
             '5. Bấm “Lưu nháp”, hoặc bấm “Lưu và gửi” rồi bấm Xác nhận ở hộp thoại.\n'
             '6. Hệ thống kiểm tra, sinh mã yêu cầu, lưu, thông báo “Đã lưu thành công!” và quay về màn danh sách.',
       phu='• Thiếu / sai dữ liệu → báo đỏ dưới ô, thông báo “Vui lòng kiểm tra lại thông tin”.\n'
           '• Phiếu thu thập thông tin của dự án chưa trả lời đủ khi Lưu và gửi → “Phiếu thu thập thông tin chưa '
           'đủ các trường yêu cầu”.\n'
           '• Đổi sang dự án khác → Nhóm ngành / Nhóm giải pháp không thuộc Ứng dụng mới bị xóa.\n'
           '• Bấm Hủy ở hộp thoại xác nhận → không gửi.\n'
           '• Lỗi khác → “Đã xảy ra lỗi. Vui lòng thử lại.”',
       dacbiet='Mã yêu cầu tự sinh dạng <Mã công ty>.YCP.<CN|TC>.<2 số cuối năm>.<STT 4 chữ số> (BR-03). Mỗi dự án '
               'TKT chỉ có 1 yêu cầu. Màn không cảnh báo khi rời đi lúc chưa lưu.'),
   suffix=' => Tạo mới => Lưu nháp / Lưu và gửi',
   tkt=[' => Tạo yêu cầu làm giải pháp => Lưu nháp / Lưu và gửi'],
   note='Lối vào thứ 2: nút “Tạo yêu cầu làm giải pháp” trên dòng của danh sách Dự án TKT, hoặc ở chân màn chi '
        'tiết Dự án TKT — chỉ hiện với dự án hợp lệ do chính người dùng tạo (BR-02).',
   shots=[('06-tao-trong.png', 'Màn Tạo yêu cầu giải pháp lúc mới mở'),
          ('06b-tao-loi.png', 'Lỗi dưới ô khi bấm Lưu nháp lúc chưa nhập dữ liệu'),
          ('08-tkt-ds.png', 'Lối vào từ danh sách Dự án TKT — nút Tạo yêu cầu làm giải pháp trên dòng'),
          ('09-tao-tu-tkt.png', 'Màn Tạo yêu cầu mở từ Dự án TKT, dự án được chọn sẵn và dữ liệu đã nhập'),
          ('09b-xac-nhan-gui.png', 'Hộp thoại Xác nhận lưu và gửi')],
   ui=FORM_UI,
   ev=[
       ('Mở màn Tạo mới', 'System',
        'After:\n– Nạp danh sách dự án hợp lệ, danh mục; mở từ Dự án TKT thì chọn sẵn dự án đó.'),
       ('Chọn Dự án tiền khả thi', 'Change',
        'After:\n– Đổ thông tin dự án vào các ô kế thừa, khối Phụ trách KD nội bộ, tab Dự án tiền khả thi và '
        'tab Meetings.\n– Dự án Triển khai theo phòng → gán và khóa Phòng tiếp nhận.\n'
        '– Bỏ chọn dự án → xóa dữ liệu đã đổ.'),
       ('Bấm Lưu nháp', 'Click', SAVE_DURING +
        'After:\n– Sinh mã yêu cầu, lưu trạng thái Nháp, lưu tệp đính kèm; ghi 1 dòng lịch sử “Tạo mới”.\n'
        '– Không đồng bộ giai đoạn / trạng thái về dự án TKT.\n'
        '– Thông báo “Đã lưu thành công!”, quay về danh sách.'),
       ('Bấm Lưu và gửi → Xác nhận', 'Click', SAVE_DURING + SEND_DURING +
        'After:\n– Sinh mã yêu cầu, lưu tệp đính kèm, ghi lịch sử “Tạo mới”.\n' + SEND_AFTER +
        '– Thông báo “Đã lưu thành công!”, quay về danh sách.'),
       ('Bấm Quay lại', 'Click', 'After:\n– Về màn danh sách, không lưu.'),
   ])

# ------------------------------------------------------------------ 2.7 Xem chi tiết
fn('Xem chi tiết yêu cầu',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết yêu cầu làm giải pháp',
       mota='Xem toàn bộ thông tin của một yêu cầu ở chế độ chỉ đọc: thông tin yêu cầu, dự án tiền khả thi, '
            'meetings, phiếu thu thập thông tin (người tiếp nhận) và lịch sử; chân màn có các nút thao tác theo '
            'trạng thái và vai trò.',
       tacnhan=TAC_ALL,
       dieukien='Yêu cầu đang hiển thị trên màn danh sách của người dùng.',
       chinh='1. Người dùng bấm Mã yêu cầu trên dòng (chuột phải để mở tab mới), hoặc bấm thông báo về yêu cầu.\n'
             '2. Hệ thống mở màn “Chi tiết yêu cầu giải pháp: <Mã> (<Trạng thái>)” ở tab Thông tin yêu cầu.\n'
             '3. Người dùng chuyển giữa các tab; mở mục Lịch sử nếu cần (FR-12).\n'
             '4. Chân màn hiển thị các nút: Sửa, Xóa, Hủy yêu cầu làm giải pháp, Tiếp nhận, Từ chối (theo điều '
             'kiện) và Quay lại.',
       phu='• Tab Phiếu thu thập thông tin chỉ hiện khi người dùng được phép tiếp nhận yêu cầu (Q1, yêu cầu Chờ '
           'tiếp nhận thuộc phòng mình quản lý).\n'
           '• Yêu cầu bị Từ chối / Đã hủy → hiện thêm ô Lý do từ chối / Lý do hủy (chỉ đọc).\n'
           '• Tab Meetings: tìm nhanh theo mã / tên meeting (Enter); nút Tạo mới mở màn tạo meeting gắn sẵn dự án.\n'
           '• Không tải được dữ liệu → “Không thể tải dữ liệu yêu cầu”.'),
   suffix=' => Mã yêu cầu',
   shots=[('10-ct-nhap.png', 'Chi tiết yêu cầu Nháp của người tạo — tab Thông tin yêu cầu'),
          ('10c-tab-1.png', 'Tab Dự án tiền khả thi'),
          ('10d-tab-2.png', 'Tab Meetings'),
          ('10e-tab-3.png', 'Tab Phiếu thu thập thông tin (người tiếp nhận)')],
   ui=[
       ('Tiêu đề “Chi tiết yêu cầu giải pháp: <Mã> (<Trạng thái>)”', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
        'Trạng thái theo màu trạng thái.'),
       ('Thanh tab', 'Tab', 'Enable', '3–4 tab', 'Thông tin yêu cầu',
        'Thông tin yêu cầu · Dự án tiền khả thi · Meetings · Phiếu thu thập thông tin (chỉ người tiếp nhận).'),
       ('Tên yêu cầu, Phòng tiếp nhận yêu cầu', 'Textbox / Dropdown', 'Read-only', '–', 'Theo dữ liệu', '–'),
       ('Ứng dụng / Nhóm ngành / Nhóm giải pháp', 'Textbox / Dropdown', 'Read-only', '–', 'Theo dữ liệu',
        'Ứng dụng kế thừa từ dự án TKT.'),
       ('Giai đoạn dự án', 'Dropdown', 'Read-only', '–', 'Theo dữ liệu', 'Có icon ⓘ mô tả giai đoạn.'),
       ('Ngày KH cần giải pháp / Ngày KH cần báo giá / Ngày cần nhận GP nội bộ', 'Datepicker', 'Read-only',
        'dd/mm/yyyy', 'Theo dữ liệu', '–'),
       ('Hạn hoàn thành tiếp nhận', 'Textbox', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        'Chỉ hiện khi yêu cầu đã gửi; = Ngày gửi + số ngày / giờ phản hồi của mức độ ưu tiên.'),
       ('Mô tả / ghi chú yêu cầu', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
       ('Lý do từ chối / Lý do hủy', 'Textarea', 'Read-only', '–', 'Ẩn', 'Chỉ hiện khi có dữ liệu.'),
       ('Bảng File gửi kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tải xuống được; không thêm / xóa.'),
       ('Khối Phụ trách KD nội bộ', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'KD phụ trách chính và nhóm hỗ trợ.'),
       ('Tab Dự án tiền khả thi', 'Section', 'Read-only', '–', 'Theo dự án',
        'Thông tin khách hàng, thông tin dự án, tiến độ, đội KD, phòng hỗ trợ, giải pháp, dự án liên quan, tài chính.'),
       ('Tab Meetings — ô Tìm nhanh Meeting', 'Textbox', 'Enable', '–', 'Trống',
        'Placeholder “Nhập mã / tên meeting...”; Enter để tìm; nút × xóa từ khóa.'),
       ('Tab Meetings — bảng “Danh sách Meetings”', 'Table/Grid', 'Read-only', '–', '5 dòng/trang',
        'STT, Mã / Tên Meeting (mở tab mới), Thời gian, Thời lượng họp, Loại & Hình thức, Khách hàng, Thành phần '
        'tham dự, Trạng thái, Biên bản.'),
       ('Tab Meetings — nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', 'Mở màn tạo meeting gắn sẵn dự án TKT.'),
       ('Mục Lịch sử', 'Section', 'Enable', '–', 'Thu gọn', 'Xem FR-12.'),
       ('Nút Sửa / Xóa', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
        'Hiện khi yêu cầu ở trạng thái Nháp hoặc Yêu cầu bổ sung (FR-08/FR-09/FR-10).'),
       ('Nút Hủy yêu cầu làm giải pháp', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
        'Chỉ người tạo, yêu cầu Nháp / Chờ tiếp nhận / Yêu cầu bổ sung (FR-11).'),
       ('Nút Tiếp nhận / Từ chối', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu', 'Xem FR-14.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về nơi người dùng đi vào.'),
   ], ui_kw=dict(required=False),
   ev=[
       ('Bấm Mã yêu cầu', 'Click', 'After:\n– Mở màn chi tiết ở chế độ chỉ đọc, tab Thông tin yêu cầu.'),
       ('Bấm một tab', 'Click', 'After:\n– Hiển thị nội dung tab; tab Meetings nạp meeting của dự án TKT.'),
       ('Enter ở ô Tìm nhanh Meeting / bấm ×', 'Keypress / Click',
        'After:\n– Lọc meeting theo mã / tên, về trang 1 / xóa từ khóa và nạp lại.'),
       ('Bấm Tạo mới (tab Meetings)', 'Click', 'After:\n– Mở màn tạo meeting, chọn sẵn dự án TKT của yêu cầu.'),
       ('Bấm Quay lại', 'Click', 'After:\n– Trở về màn trước đó.'),
   ])

# ------------------------------------------------------------------ 2.8 Sửa
fn('Sửa yêu cầu', code='FR-08', group='crud',
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Sửa yêu cầu làm giải pháp',
       mota='Người tạo chỉnh sửa yêu cầu đang ở trạng thái Nháp (hoặc Yêu cầu bổ sung — xem FR-09); có thể tiếp '
            'tục lưu nháp hoặc lưu và gửi đi.',
       tacnhan=TAC_KD,
       dieukien='Người dùng là người tạo yêu cầu; yêu cầu ở trạng thái Nháp hoặc Yêu cầu bổ sung.',
       chinh='1. Người dùng bấm nút Sửa (biểu tượng bút) trên dòng, hoặc nút Sửa ở chân màn Chi tiết.\n'
             '2. Hệ thống mở màn “Sửa yêu cầu giải pháp” với dữ liệu hiện tại.\n'
             '3. Người dùng sửa các trường như màn Tạo mới (FR-06).\n'
             '4. Bấm “Lưu nháp” (chỉ có khi đang Nháp), hoặc “Lưu và gửi” → Xác nhận.\n'
             '5. Hệ thống kiểm tra, lưu, thông báo “Đã cập nhật thành công!” và quay về màn danh sách.',
       phu='• Thiếu / sai dữ liệu → báo đỏ dưới ô, “Vui lòng kiểm tra lại thông tin”.\n'
           '• Yêu cầu không còn ở Nháp / Yêu cầu bổ sung (đã gửi, đã bị xử lý) → hệ thống từ chối lưu, thông báo '
           '“Đã xảy ra lỗi. Vui lòng thử lại.”\n'
           '• Yêu cầu đã Đóng theo dự án → không cho sửa.',
       dacbiet='Dự án Triển khai theo phòng: khi lưu, hệ thống tự gán Phòng tiếp nhận = phòng của người tạo dự án '
               'TKT, bỏ qua giá trị trên form. Trường Nhóm ngành / Nhóm giải pháp đang trống được điền hộ theo dự án.'),
   suffix=' => Sửa => Lưu nháp / Lưu và gửi',
   shots=[('01c-ds-hanhdong.png', 'Các nút Sửa, Xóa, Hủy yêu cầu trên dòng yêu cầu Nháp'),
          ('11-sua-nhap.png', 'Màn Sửa yêu cầu đang Nháp — chân màn có Lưu nháp và Lưu và gửi')],
   ui=[r for r in FORM_UI if not r[0].startswith('Nút Lưu nháp')] + [
       ('Nút Lưu nháp', 'Button', 'Enable / Ẩn', '–', '–', 'Hiện khi đang Nháp', 'Lưu, giữ trạng thái Nháp.'),
   ],
   ev=[
       ('Bấm Sửa', 'Click',
        'Before:\n– Nút chỉ hiện với người tạo khi yêu cầu Nháp / Yêu cầu bổ sung.\n' + NO_OWNER + '\n'
        'After:\n– Mở màn Sửa với dữ liệu hiện tại.'),
       ('Bấm Lưu nháp', 'Click',
        'Before:\n– Yêu cầu phải đang Nháp / Yêu cầu bổ sung.\n' + SAVE_DURING +
        'After:\n– Cập nhật yêu cầu; đồng bộ tệp đính kèm (thêm / bỏ tệp).\n'
        '– Ghi 1 dòng lịch sử “Chỉnh sửa” gồm các trường thay đổi (giá trị cũ → mới).\n'
        '– Thông báo “Đã cập nhật thành công!”, quay về danh sách.'),
       ('Bấm Lưu và gửi → Xác nhận', 'Click',
        'Before:\n– Yêu cầu phải đang Nháp / Yêu cầu bổ sung.\n' + SAVE_DURING + SEND_DURING +
        'After:\n– Cập nhật yêu cầu, đồng bộ tệp; ghi lịch sử “Chỉnh sửa” và dòng “Đổi trạng thái”.\n' + SEND_AFTER +
        '– Thông báo “Đã cập nhật thành công!”, quay về danh sách.'),
   ])

# ------------------------------------------------------------------ 2.9 Cập nhật bổ sung và gửi lại
fn('Cập nhật bổ sung và gửi lại', code='FR-09', group='crud',
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Cập nhật bổ sung thông tin và gửi lại yêu cầu',
       mota='Khi phòng giải pháp yêu cầu bổ sung thông tin (trạng thái Yêu cầu bổ sung), người tạo trả lời câu hỏi '
            'bổ sung trong phiếu thu thập thông tin của dự án TKT, cập nhật yêu cầu nếu cần rồi gửi lại.',
       tacnhan=TAC_KD,
       dieukien='Người dùng là người tạo; yêu cầu ở trạng thái Yêu cầu bổ sung (do người tiếp nhận thực hiện ở %s).'
                % SRS_PD,
       chinh='1. Người tạo nhận thông báo “Bạn có yêu cầu bổ sung câu hỏi mới của yêu cầu làm giải pháp: <Mã> - <Tên>”.\n'
             '2. Người tạo vào Dự án TKT, trả lời các câu hỏi ở mục “Thông tin bổ sung” của phiếu thu thập thông '
             'tin và lưu phiếu (chức năng của màn Dự án TKT).\n'
             '3. Người tạo bấm Sửa trên dòng yêu cầu (hoặc ở chân màn Chi tiết).\n'
             '4. Màn Sửa chỉ còn nút “Lưu và gửi” (không còn Lưu nháp); người dùng cập nhật nếu cần, bấm “Lưu và '
             'gửi” → Xác nhận.\n'
             '5. Hệ thống kiểm tra, chuyển yêu cầu về Chờ tiếp nhận, tính lại hạn từ lần gửi mới, thông báo “Đã '
             'cập nhật thành công!”.',
       phu='• Phiếu thu thập còn câu bắt buộc chưa trả lời → “Phiếu thu thập thông tin chưa đủ các trường yêu '
           'cầu”, không gửi.\n'
           '• Thiếu / sai dữ liệu → báo đỏ dưới ô, “Vui lòng kiểm tra lại thông tin”.',
       dacbiet='Lần gửi lại: Ngày gửi = thời điểm gửi lại, Hạn tiếp nhận tính lại, kết quả phản hồi trước đó bị '
               'xóa để tính hạn lần mới.'),
   suffix=' => Sửa => Lưu và gửi',
   shots=[('12b-ct-bosung.png', 'Chi tiết yêu cầu đang ở trạng thái Yêu cầu bổ sung'),
          ('12-sua-bosung.png', 'Màn Sửa yêu cầu Yêu cầu bổ sung — chỉ còn nút Lưu và gửi')],
   ui=[r for r in FORM_UI if not r[0].startswith('Nút Lưu nháp')] + [
       ('Nút Lưu nháp', 'Button', 'Ẩn', '–', '–', 'Ẩn', 'Không hiện khi yêu cầu ở trạng thái Yêu cầu bổ sung.'),
   ],
   ev=[
       ('Bấm Sửa trên yêu cầu Yêu cầu bổ sung', 'Click',
        'Before:\n– Nút chỉ hiện với người tạo.\n' + NO_OWNER + '\nAfter:\n– Mở màn Sửa, chỉ có Lưu và gửi.'),
       ('Bấm Lưu và gửi → Xác nhận', 'Click', SAVE_DURING + SEND_DURING +
        'After:\n– Chuyển yêu cầu về Chờ tiếp nhận; Ngày gửi = thời điểm gửi lại; tính lại Hạn tiếp nhận; xóa kết '
        'quả phản hồi cũ.\n– Ghi lịch sử “Chỉnh sửa” (nếu có thay đổi) và “Đổi trạng thái: Yêu cầu bổ sung → Chờ '
        'tiếp nhận”.\n– Đồng bộ giai đoạn và trạng thái dự án TKT; gửi lại thông báo cho phòng tiếp nhận.\n'
        '– Thông báo “Đã cập nhật thành công!”, quay về danh sách.'),
   ])

# ------------------------------------------------------------------ 2.10 Xóa
fn('Xóa yêu cầu', code='FR-10', group='action',
   rule=('- Thông báo và Quy tắc Xóa.', 'delete'),
   intro=dict(
       ten='Xóa yêu cầu làm giải pháp',
       mota='Người tạo xóa hẳn một yêu cầu còn ở trạng thái Nháp (chưa từng gửi đi).',
       tacnhan=TAC_KD,
       dieukien='Người dùng là người tạo; yêu cầu ở trạng thái Nháp và chưa sinh giải pháp.',
       chinh='1. Người dùng bấm nút Xóa (thùng rác) trên dòng, hoặc nút Xóa ở chân màn Chi tiết.\n'
             '2. Hệ thống hỏi “Xác nhận xóa” – “Bạn có chắc muốn xóa yêu cầu \'<Mã> - <Tên>\'?” (ở màn Chi tiết: '
             '“Bạn có chắc muốn xóa yêu cầu làm giải pháp \'<Mã>\'?”).\n'
             '3. Người dùng bấm Xóa.\n'
             '4. Hệ thống xóa yêu cầu, thông báo “Xóa yêu cầu thành công”; ở danh sách thì nạp lại bảng, ở màn Chi '
             'tiết thì quay về danh sách.',
       phu='• Bấm Hủy → đóng hộp thoại, không xóa.\n'
           '• Yêu cầu không còn ở Nháp → hệ thống từ chối, thông báo “Không có quyền!”.\n'
           '• Yêu cầu đã Đóng theo dự án → không cho xóa.\n'
           '• Lỗi khác → “Lỗi khi xóa yêu cầu”.',
       dacbiet='Xóa hẳn khỏi hệ thống (không xóa mềm). Dự án TKT được giải phóng để lập yêu cầu mới.'),
   suffix=' => Xóa', note=MODAL % 'Xác nhận xóa' + ' Cũng mở được bằng nút Xóa ở chân màn Chi tiết.',
   shots=[('13-xoa-ds.png', 'Hộp thoại Xác nhận xóa mở từ danh sách')],
   ui=[
       ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
       ('Nội dung xác nhận', 'Label', 'Read-only', 'Theo dữ liệu',
        'Danh sách: “Bạn có chắc muốn xóa yêu cầu \'<Mã> - <Tên>\'?”; màn Chi tiết: “Bạn có chắc muốn xóa yêu cầu '
        'làm giải pháp \'<Mã>\'?”.'),
       ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Màu đỏ; thực hiện xóa.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
   ], ui_kw=dict(required=False, scope=False),
   ev=[
       ('Bấm nút Xóa', 'Click',
        'Before:\n– Danh sách: nút chỉ hiện với người tạo, yêu cầu Nháp, chưa sinh giải pháp. Màn Chi tiết: nút '
        'hiện khi yêu cầu Nháp / Yêu cầu bổ sung.\n' + NO_OWNER + '\nAfter:\n– Mở hộp thoại Xác nhận xóa.'),
       ('Bấm Xóa (hộp thoại)', 'Click',
        'Before:\n– Yêu cầu không ở trạng thái Nháp → “Không có quyền!”, dừng.\n'
        'After:\n– Xóa yêu cầu; thông báo “Xóa yêu cầu thành công”; nạp lại danh sách / quay về danh sách.\n'
        '– Lỗi → hiển thị nội dung lỗi hoặc “Lỗi khi xóa yêu cầu”.'),
       ('Bấm Hủy (hộp thoại)', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
   ])

# ------------------------------------------------------------------ 2.11 Hủy
fn('Hủy yêu cầu', code='FR-11', group='action',
   rule=('- Quy tắc ghi lịch sử, Khóa / Mở khóa và Thông báo.', 'history'),
   intro=dict(
       ten='Hủy yêu cầu làm giải pháp',
       mota='Người tạo hủy yêu cầu chưa được tiếp nhận, bắt buộc ghi lý do; yêu cầu chuyển sang Đã hủy và dự án '
            'TKT quay về bước thu thập thông tin.',
       tacnhan=TAC_KD,
       dieukien='Người dùng là người tạo; yêu cầu ở trạng thái Nháp, Chờ tiếp nhận hoặc Yêu cầu bổ sung.',
       chinh='1. Người dùng bấm “Hủy yêu cầu” (trong cột Hành động) hoặc “Hủy yêu cầu làm giải pháp” ở chân màn '
             'Chi tiết.\n'
             '2. Hệ thống mở cửa sổ “Xác nhận hủy yêu cầu làm giải pháp”.\n'
             '3. Người dùng nhập Lý do hủy, bấm Đồng ý.\n'
             '4. Hệ thống chuyển yêu cầu sang Đã hủy, thông báo “Hủy yêu cầu thành công”, đóng cửa sổ và nạp lại '
             'danh sách / màn Chi tiết (hiện Lý do hủy, ẩn các nút thao tác).',
       phu='• Bỏ trống lý do → “Vui lòng nhập lý do hủy” dưới ô.\n'
           '• Yêu cầu đã được tiếp nhận / xử lý trước đó → “Yêu cầu đã được tiếp nhận hoặc xử lý, không thể hủy”.\n'
           '• Không phải người tạo → “Chỉ người tạo yêu cầu mới được hủy”.\n'
           '• Bấm Không / dấu × → đóng cửa sổ, không đổi dữ liệu.',
       dacbiet='Hai thao tác hủy cùng lúc trên một yêu cầu chỉ thực hiện 1 lần.'),
   suffix=' => Hủy yêu cầu', note=MODAL % 'Xác nhận hủy yêu cầu làm giải pháp' +
   ' Cũng mở được bằng nút Hủy yêu cầu làm giải pháp ở chân màn Chi tiết.',
   shots=[('14-huy.png', 'Cửa sổ Xác nhận hủy yêu cầu làm giải pháp'),
          ('14b-huy-loi.png', 'Lỗi khi bấm Đồng ý lúc chưa nhập lý do hủy'),
          ('14c-da-huy.png', 'Màn Chi tiết sau khi hủy — hiện Lý do hủy')],
   ui=[
       ('Tiêu đề “Xác nhận hủy yêu cầu làm giải pháp”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
       ('Lý do hủy', 'Textarea', 'Enable', '1–1.000 ký tự', 'Có', 'Trống', 'Placeholder “Nhập lý do hủy”.'),
       ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Chữ đỏ ngay dưới ô.'),
       ('Nút Đồng ý', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khóa trong lúc xử lý.'),
       ('Nút Không', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không hủy.'),
   ],
   ev=[
       ('Bấm Hủy yêu cầu', 'Click',
        'Before:\n– Nút chỉ hiện với người tạo khi yêu cầu Nháp / Chờ tiếp nhận / Yêu cầu bổ sung.\n' + NO_OWNER +
        '\nAfter:\n– Mở cửa sổ với ô lý do trống.'),
       ('Bấm Đồng ý', 'Click',
        'During:\n– Lý do trống → “Vui lòng nhập lý do hủy”; quá 1.000 ký tự → “Lý do hủy không được vượt quá '
        '1000 ký tự”.\n– Không phải người tạo → “Chỉ người tạo yêu cầu mới được hủy”.\n'
        '– Yêu cầu đã rời các trạng thái được hủy → “Yêu cầu đã được tiếp nhận hoặc xử lý, không thể hủy”.\n'
        '– Có lỗi → không thực hiện bước After.\n'
        'After:\n– Chuyển yêu cầu sang Đã hủy; lưu lý do, người và thời điểm hủy.\n'
        '– Ghi lịch sử “Đổi trạng thái” kèm lý do hủy.\n'
        '– Dự án TKT quay về bước “Thu thập thông tin dự án” (mở lại quyền sửa dự án).\n'
        '– Gửi thông báo cho phòng tiếp nhận: “[YCG] Hủy: <Tên yêu cầu>. Người thực hiện: <họ tên>”.\n'
        '– Thông báo “Hủy yêu cầu thành công”, nạp lại dữ liệu.'),
       ('Bấm Không / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, không thay đổi dữ liệu.'),
   ])

# ------------------------------------------------------------------ 2.12 Lịch sử
fn('Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng tại phần mô tả chi tiết.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi yêu cầu',
       mota='Mục “Lịch sử” cuối màn Chi tiết liệt kê các lần tạo, chỉnh sửa, đổi trạng thái của yêu cầu, mới nhất '
            'ở trên, kèm người thực hiện và giá trị cũ → mới.',
       tacnhan=TAC_ALL,
       dieukien='Đang ở màn Chi tiết yêu cầu.',
       chinh='1. Người dùng bấm “Xem lịch sử” ở mục Lịch sử (thu gọn mặc định).\n'
             '2. Hệ thống nạp và hiển thị dòng thời gian: thời điểm, loại hành động, người thực hiện — phòng, các '
             'trường thay đổi.\n'
             '3. Người dùng bấm “Bộ lọc” để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.\n'
             '4. Bấm “Thu gọn” để đóng mục.',
       phu='• Chưa có lịch sử → “Chưa có lịch sử thao tác nào.”\n'
           '• Không có dòng khớp bộ lọc → “Không có lịch sử phù hợp bộ lọc.”\n'
           '• Lỗi tải → hiển thị lỗi và nút “Thử lại”; nút “Làm mới” nạp lại lịch sử.'),
   suffix=' => Mã yêu cầu => Xem lịch sử',
   shots=[('16-lichsu.png', 'Mục Lịch sử đang mở ở màn Chi tiết yêu cầu')],
   ui=[
       ('Tiêu đề mục “Lịch sử”', 'Label', 'Hiển thị', '–', 'Hiển thị', 'Kèm số dòng lịch sử sau khi nạp.'),
       ('Nút Xem lịch sử / Thu gọn', 'Button', 'Enable', '–', 'Xem lịch sử', 'Mở / đóng mục; chỉ nạp dữ liệu ở lần mở đầu.'),
       ('Nút Làm mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi đang thu gọn', 'Nạp lại lịch sử.'),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Mở / đóng 4 ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Tạo mới / Chỉnh sửa / Đổi trạng thái', 'Trống',
        'Placeholder “Chọn loại hành động”; chọn là lọc ngay.'),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Người có trong lịch sử', 'Trống', 'Placeholder “Chọn người thực hiện”.'),
       ('Từ ngày / Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', 'Lọc theo ngày thao tác.'),
       ('Dòng lịch sử', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        'Thời điểm; loại hành động (Tạo mới / Chỉnh sửa / Đổi trạng thái); “Người thực hiện: … — phòng”; từng '
        'trường: giá trị cũ → giá trị mới; lý do hủy / từ chối nếu có.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Chưa có lịch sử thao tác nào.”'),
   ], ui_kw=dict(required=False),
   ev=[
       ('Bấm Xem lịch sử', 'Click', 'After:\n– Nạp lịch sử (lần đầu) và hiển thị dòng thời gian, mới nhất trước.'),
       ('Đổi ô lọc lịch sử', 'Change', 'After:\n– Lọc ngay các dòng đang có; Làm mới trong bộ lọc xóa điều kiện.'),
       ('Bấm Thu gọn', 'Click', 'After:\n– Đóng mục Lịch sử.'),
   ])

# ------------------------------------------------------------------ 2.13 Làm giải pháp
fn('Làm giải pháp (lối tắt)', code='FR-13', group='action', actor=A_TN,
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Làm giải pháp từ yêu cầu (lối tắt)',
       mota='Người đã tiếp nhận yêu cầu mở thẳng màn tạo giải pháp, dữ liệu yêu cầu được đổ sẵn.',
       tacnhan='Người tiếp nhận yêu cầu làm giải pháp; Người dùng đã đăng nhập',
       dieukien='Người dùng chính là người tiếp nhận của yêu cầu; yêu cầu ở trạng thái Đã tiếp nhận.',
       chinh='1. Người dùng bấm nút “Làm giải pháp” (biểu tượng bóng đèn) trên dòng yêu cầu.\n'
             '2. Hệ thống mở màn Tạo giải pháp, gắn sẵn yêu cầu làm giải pháp này (chức năng của màn Giải pháp).',
       phu='• Yêu cầu chưa / không còn ở trạng thái Đã tiếp nhận, hoặc người dùng không phải người tiếp nhận → nút ẩn.'),
   suffix=' => Làm giải pháp',
   shots=[('17-lamgp.png', 'Nút Làm giải pháp trên dòng yêu cầu Đã tiếp nhận của người tiếp nhận')],
   ui=[
       ('Nút Làm giải pháp (biểu tượng bóng đèn)', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
        'Hiện khi người dùng là người tiếp nhận và yêu cầu Đã tiếp nhận; chuột phải mở tab mới được.'),
   ], ui_kw=dict(required=False),
   ev=[
       ('Bấm Làm giải pháp', 'Click',
        'Before:\n– Nút chỉ hiện khi đủ điều kiện.\nAfter:\n– Mở màn Tạo giải pháp kèm yêu cầu làm giải pháp đã chọn.'),
   ])

# ------------------------------------------------------------------ 2.14 Tiếp nhận / Từ chối
fn('Tiếp nhận / Từ chối tại màn chi tiết', code='FR-14', group='action', actor=A_TN,
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tiếp nhận hoặc Từ chối yêu cầu tại màn Chi tiết',
       mota='Người có quyền Q1 mở Chi tiết yêu cầu đang Chờ tiếp nhận từ màn này sẽ thấy 2 nút Tiếp nhận và Từ chối '
            'ở chân màn. Toàn bộ nghiệp vụ, dữ liệu nhập và thông báo được đặc tả ở %s (chức năng Tiếp nhận yêu '
            'cầu và Từ chối yêu cầu).' % SRS_PD,
       tacnhan='Trưởng phòng / người phụ trách tiếp nhận yêu cầu làm giải pháp; Người dùng đã đăng nhập',
       dieukien='Có quyền Q1; yêu cầu đang Chờ tiếp nhận và phòng tiếp nhận thuộc phòng người dùng quản lý.',
       chinh='1. Người dùng mở Chi tiết yêu cầu (FR-07).\n'
             '2. Bấm “Tiếp nhận” → cửa sổ Tiếp nhận yêu cầu làm GP (chọn Ngày dự kiến xong GP, PM làm GP…); sau '
             'khi xác nhận, hệ thống quay về màn danh sách Yêu cầu làm giải pháp.\n'
             '3. Hoặc bấm “Từ chối” → cửa sổ Xác nhận từ chối, nhập Lý do từ chối, bấm Đồng ý; hệ thống báo “Từ '
             'chối yêu cầu thành công” và nạp lại màn Chi tiết.',
       phu='• Yêu cầu đã được người khác xử lý → “Phiếu đã được tiếp nhận, vui lòng tải lại dữ liệu” / “Phiếu đã '
           'được xử lý, vui lòng tải lại dữ liệu”.\n'
           '• Không đủ điều kiện → 2 nút ẩn.'),
   suffix=' => Mã yêu cầu => Tiếp nhận / Từ chối',
   shots=[('10b-ct-cho.png', 'Chi tiết yêu cầu Chờ tiếp nhận với người có quyền Q1 — nút Tiếp nhận, Từ chối'),
          ('15-tiepnhan.png', 'Cửa sổ Tiếp nhận yêu cầu làm GP'),
          ('15b-tuchoi.png', 'Cửa sổ Xác nhận từ chối')],
   ui=[
       ('Nút Tiếp nhận', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
        'Mở cửa sổ Tiếp nhận yêu cầu làm GP (đặc tả ở %s).' % SRS_PD),
       ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
        'Màu đỏ; mở cửa sổ Xác nhận từ chối (đặc tả ở %s).' % SRS_PD),
       ('Tab Phiếu thu thập thông tin', 'Tab', 'Enable / Ẩn', '–', 'Theo dữ liệu',
        'Cùng điều kiện; nơi người tiếp nhận thêm câu hỏi Yêu cầu bổ sung (đặc tả ở %s).' % SRS_PD),
   ], ui_kw=dict(required=False),
   ev=[
       ('Mở Chi tiết yêu cầu', 'System',
        'Before:\n– Kiểm tra quyền Q1, trạng thái Chờ tiếp nhận và phòng tiếp nhận thuộc phạm vi quản lý.\n'
        'After:\n– Đủ điều kiện → hiện nút Tiếp nhận, Từ chối và tab Phiếu thu thập thông tin.'),
       ('Bấm Tiếp nhận → Xác nhận tiếp nhận', 'Click',
        'After:\n– Xử lý theo %s; thành công thì quay về màn danh sách Yêu cầu làm giải pháp.' % SRS_PD),
       ('Bấm Từ chối → Đồng ý', 'Click',
        'After:\n– Xử lý theo %s; thành công thì nạp lại màn Chi tiết (hiện Lý do từ chối).' % SRS_PD),
   ])

# ==================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Yêu cầu làm giải pháp; không lặp lại các quy tắc đã '
           'có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Vòng đời trạng thái', [
        '– Nháp (xám) → Lưu và gửi → Chờ tiếp nhận (cam).',
        '– Chờ tiếp nhận → Đã tiếp nhận (xanh dương) / Yêu cầu bổ sung (vàng) / Từ chối (đỏ) — do người tiếp nhận.',
        '– Yêu cầu bổ sung → người tạo gửi lại → Chờ tiếp nhận.',
        '– Nháp / Chờ tiếp nhận / Yêu cầu bổ sung → người tạo hủy → Đã hủy (xám).',
        '– Sau tiếp nhận, trạng thái đi theo giải pháp: Đang thực hiện, Đã hoàn thành (xanh lá), Đã chốt giải pháp '
        '(tím), Đóng (xám, đóng theo dự án).',
    ], ['Xem danh sách', 'Tìm kiếm và lọc']),
    ('BR-02', 'Dự án được lập yêu cầu', [
        '– Chỉ dự án TKT do chính người dùng tạo; chưa có yêu cầu nào (kể cả yêu cầu đã hủy / từ chối); không '
        'phải Tự triển khai; không phải dự án cha.',
        '– Ô chọn dự án ở màn Tạo mới ẩn dự án có phiếu thu thập chưa trả lời đủ câu bắt buộc.',
        '– Cùng điều kiện quyết định nút “Tạo yêu cầu làm giải pháp” ở màn Dự án TKT.',
    ], ['Tạo mới']),
    ('BR-03', 'Mã yêu cầu', [
        '– Tự sinh khi lưu lần đầu: <Mã công ty người tạo>.YCP.<CN nếu khách hàng cá nhân, TC nếu tổ chức>.<2 số '
        'cuối năm>.<STT 4 chữ số>.',
        '– STT tăng liên tục theo công ty trong năm, không phân biệt CN / TC.',
    ], ['Tạo mới']),
    ('BR-04', 'Phòng tiếp nhận', [
        '– Dự án Liên phòng ban: người tạo chọn phòng tiếp nhận.',
        '– Dự án Triển khai theo phòng: khi tạo, tự gán phòng KD phụ trách chính của dự án; khi sửa, tự gán '
        'phòng của người tạo dự án; ô bị khóa trên form.',
    ], ['Tạo mới', 'Sửa']),
    ('BR-05', 'Kiểm tra khi gửi', [
        '– Lưu nháp: chỉ cần dự án, tên, phòng tiếp nhận, Ngày KH cần giải pháp, Ngày KH cần báo giá.',
        '– Lưu và gửi: bắt buộc thêm Giai đoạn dự án và phiếu thu thập thông tin của dự án phải trả lời đủ câu bắt buộc.',
        '– Tên yêu cầu không trùng toàn hệ thống; Nhóm ngành / Nhóm giải pháp phải thuộc Ứng dụng của dự án.',
        '– Chỉ khi rời Nháp mới đồng bộ Giai đoạn dự án và trạng thái về dự án TKT.',
    ], ['Tạo mới', 'Sửa', 'Gửi lại']),
    ('BR-06', 'Hạn tiếp nhận', [
        '– Tính khi gửi / gửi lại: Ngày gửi + số ngày và số giờ phản hồi của Mức độ ưu tiên (theo giai đoạn dự án TKT).',
        '– Chỉ đếm ngày có phân ca của trưởng phòng tiếp nhận, bỏ qua ngày nghỉ lễ; không có trưởng phòng thì chỉ '
        'bỏ qua ngày nghỉ lễ.',
        '– Mức độ ưu tiên không có số ngày phản hồi → không có hạn.',
    ], ['Tạo mới', 'Sửa', 'Gửi lại']),
    ('BR-07', 'Nhãn hạn xử lý trên danh sách', [
        '– Chờ tiếp nhận: Quá hạn (đỏ) khi đã qua hạn; Sắp đến hạn (cam) khi đã gửi cảnh báo hoặc tới mốc lùi 1 '
        'ngày làm việc trước hạn; còn lại Trong hạn (xanh).',
        '– Đã phản hồi: “Đã xử lý (Trong hạn)” / “Đã xử lý (Quá hạn)”.',
    ], ['Xem danh sách']),
    ('BR-08', 'Phạm vi dữ liệu', [
        '– Theo quyền V1–V4 (Phần 2); không có quyền V → chỉ yêu cầu mình tạo hoặc mình tiếp nhận.',
        '– Yêu cầu Nháp chỉ người tạo nhìn thấy. Xuất Excel áp cùng phạm vi.',
    ], ['Xem danh sách', 'Xuất Excel']),
    ('BR-09', 'Quyền thao tác của người tạo', [
        '– Sửa: người tạo, trạng thái Nháp / Yêu cầu bổ sung. Lưu nháp chỉ có khi đang Nháp.',
        '– Xóa: người tạo, trạng thái Nháp, chưa sinh giải pháp. Xóa hẳn.',
        '– Hủy: người tạo, trạng thái Nháp / Chờ tiếp nhận / Yêu cầu bổ sung; bắt buộc lý do ≤ 1.000 ký tự.',
        '– Yêu cầu Đóng theo dự án không sửa, không xóa được.',
    ], ['Sửa', 'Xóa', 'Hủy']),
    ('BR-10', 'Tác động sang dự án TKT', [
        '– Gửi / gửi lại → dự án sang bước chờ tiếp nhận làm giải pháp.',
        '– Hủy (và Từ chối của người tiếp nhận) → dự án quay về Thu thập thông tin dự án.',
    ], ['Tạo mới', 'Gửi lại', 'Hủy']),
    ('BR-11', 'Thông báo', [
        '– Gửi / gửi lại → người có quyền Q1 thuộc phòng tiếp nhận và người quản lý phòng đó.',
        '– Hủy → cùng nhóm người nhận: “[YCG] Hủy: <Tên>. Người thực hiện: <họ tên>”.',
        '– Bấm thông báo mở màn Chi tiết yêu cầu.',
    ], ['Tạo mới', 'Gửi lại', 'Hủy']),
    ('BR-12', 'Lịch sử', [
        '– Tạo mới: 1 dòng “Tạo mới”. Chỉnh sửa: 1 dòng gồm đúng các trường đổi giá trị; không đổi thì không ghi.',
        '– Đổi trạng thái ghi dòng riêng, kèm lý do hủy / từ chối.',
        '– Ghi theo tên hiển thị (dự án, phòng, nhóm ngành, PM…), đổi tên danh mục sau này không làm sai lịch sử.',
    ], ['Xem lịch sử']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')
