# -*- coding: utf-8 -*-
"""Sinh "SRS - Dự án.docx" (màn Dự án tiền khả thi) theo FORM CHUẨN (2026-09-24).

Chạy:  SRS_NO_WORD=1 /opt/homebrew/bin/python3 gen_srs.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/prospective-projects/{index,add}.vue · _id/{edit,manager}.vue · components/*
      pages/assign/request-solution/components/{TktTab,RequestTab,MeetingsTab}.vue
      pages/assign/solutions/components/manager/{IssueTab,FilesTab,HumanResourceTab,SolutionApprovalModal}.vue
      components/assign/task/TaskListTab.vue · components/assign/prospective-project/{Close,Extend,
      FinalizeSolution,FinalizeQuotation}Modal.vue · components/modals/{QuickAddCustomer,ChooseErpCustomer}Modal.vue
      components/subsystem-menu/presale.js (Dự án TKT)
  BE  Modules/Assign/Routes/api.php (prefix prospective-projects) · Http/Requests/ProspectiveProject/*
      Services/{ProspectiveProject,ProspectiveProjectExtension,ProspectiveProjectAutoClose,Quotation,
      SolutionAdjustmentRequest}Service.php · Entities/ProspectiveProject.php · Transformers/ProspectiveProjectResource/*
      app/Console/Commands/Assign/AutoCloseProspectiveProjectsCommand.php · app/ExcelExport/ExportColumnRegistry.php
  Quyền: PermissionsTableSeeder id 992–995, 1182, 1183, 1080, 1091, 1092; CustomerPermissionHelper 'Thêm khách hàng'
Ảnh: shots/ (Playwright headless 1440x900, client :3002) — dữ liệu tạo thêm ghi ở data_created.md.
"""
import os
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
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, 'shots')


def shot(name):
    return os.path.join(SHOTS, name)


TEN_MAN = 'Dự án'
MENU = 'Phân hệ CSKH trước bán => Dự án TKT'
DET = MENU + ' => Mã dự án'

A_ALL = 'Người dùng đã đăng nhập'
A_KD = 'NV KD phụ trách dự án'
A_PM = 'PM giải pháp / Quản lý phòng tiếp nhận'

ICONS = {
    'Phân hệ CSKH trước bán': 'icon_phanhe_presale.png',
    'Dự án TKT': 'icon_menu_duan.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png',
    'Cài đặt bộ lọc': 'icon_caidat.png',
    'Tuỳ chỉnh cột': 'icon_cot.png',
    'Xuất Excel': 'icon_xuat.png',
    'Tạo mới': 'icon_taomoi.png',
    'Thêm nhanh khách hàng': 'icon_themnhanhkh.png',
    'Sửa': 'icon_sua.png',
    'Xóa': 'icon_xoa.png',
    'Tạo giải pháp': 'icon_taogp.png',
    'Tạo yêu cầu làm giải pháp': 'icon_taoycgp.png',
    'Mở rộng dự án cha': 'icon_morong.png',
    'Mã dự án': 'icon_ma.png',
    'Tab Dự án': 'icon_tab_duan.png',
    'Tab Thông tin chung': 'icon_tab_ttchung.png',
    'Tab Yêu cầu': 'icon_tab_yeucau.png',
    'Tab Giải pháp': 'icon_tab_giaiphap.png',
    'Yêu cầu điều chỉnh GP': 'icon_subtab_dc.png',
    'Tạo yêu cầu': 'icon_taoyc.png',
    'Tab Nhiệm vụ': 'icon_tab_nhiemvu.png',
    'Tab Vấn đề giải pháp': 'icon_tab_vande.png',
    'Tab Meetings': 'icon_tab_meetings.png',
    'Tab Files': 'icon_tab_files.png',
    'Tab Hồ sơ': 'icon_tab_hoso.png',
    'Tab Báo giá': 'icon_tab_baogia.png',
    'Tab Dự án con': 'icon_tab_duancon.png',
    'Thêm dự án con': 'icon_themdac.png',
    'Tab Gia hạn': 'icon_tab_giahan.png',
    'Tab Thu thập thông tin': 'icon_tab_thuthap.png',
    'Lịch sử thay đổi': 'icon_lsphieu.png',
    'Lưu phiếu': 'icon_luuphieu.png',
    'Xem mẫu in': 'icon_xemmauin.png',
    'Chốt giải pháp': 'icon_ft_chotgp.png',
    'Gia hạn': 'icon_ft_giahan.png',
    'Đóng dự án': 'icon_ft_dong.png',
}
ICONS = {k: v for k, v in ICONS.items() if os.path.exists(shot(v))}
MISSING = [k for k, v in ICONS.items() if not os.path.exists(shot(v))]

out = os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN)
d = SrsDoc(out=out, menu=MENU, route='', full_url='', img_prefix='pp_')
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})

NO_SHOW = '– Không thỏa điều kiện → nút không hiển thị.'
SCOPE = '– Chỉ lấy dự án trong phạm vi được xem của người dùng (BR-01).'


# ------------------------------------------------------------------ helper
def fn(no, title, intro, menus, shots_, ui, events, uc=None, ui_mode='input', modal=None, note=None,
       rule=('- Màn Danh sách, Phân trang và UI/UX.', 'list')):
    """Một chức năng 2.x — đủ 5 (hoặc 4) mục con, 2 bảng giao diện/event bắt buộc."""
    assert ui and events, 'Thiếu bảng giao diện / event ở %s' % title
    d.h3('2.%d %s' % (no, title))
    k = 0
    if uc:
        k += 1
        d.p('2.%d.%d Biểu đồ Usecase' % (no, k))
        code, ucname, group, actor = uc
        d.uc_figure(code, ucname, group, actor=actor, caption='Biểu đồ Use Case — %s %s' % (code, ucname))
    k += 1
    d.p('2.%d.%d Giới thiệu' % (no, k))
    d.rule_ref(rule[0] + ' Chỉ bổ sung các quy tắc riêng của màn Dự án tại phần mô tả chi tiết.', anchor=rule[1])
    d.intro_table(**intro)
    k += 1
    d.p('2.%d.%d Layout màn hình' % (no, k))
    d.p('Đường dẫn màn hình:')
    for m in menus:
        d._menu_para(m)
    if modal:
        d.p(modal)
    if note:
        d.p(note)
    for png, cap in shots_:
        d.figure(shot(png), cap, width_in=6.2)
    k += 1
    d.p('2.%d.%d Mô tả chi tiết giao diện' % (no, k))
    if ui_mode == 'input':
        d.ui_table(ui)
    elif ui_mode == 'read':
        d.ui_table(ui, required=False)
    else:
        d.ui_table(ui, required=False, scope=False)
    k += 1
    d.p('2.%d.%d Danh sách event và xử lý event' % (no, k))
    d.event_table(events)


d.title_block('Dự án tiền khả thi')
d.h2('Mục lục')
d.toc()

# ======================================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn Dự án (dự án tiền khả thi – Dự án TKT) thuộc phân hệ CSKH '
    'trước bán, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu các chức năng của màn danh sách: xem, tìm kiếm/lọc, cài đặt bộ lọc, tuỳ chỉnh cột, xuất '
    'Excel, tạo mới (kèm thêm nhanh khách hàng, khách hàng thương mại dịch vụ, cách triển khai, dự án cha/con), '
    'chỉnh sửa, xóa và các lối tắt Tạo giải pháp / Tạo yêu cầu làm giải pháp.',
    'Là căn cứ nghiệm thu màn chi tiết dự án nhiều tab: Dự án, Yêu cầu, Giải pháp, Nhiệm vụ, Vấn đề giải pháp, '
    'Meetings, Files, Hồ sơ, Báo giá, Gia hạn, Thu thập thông tin (dự án cha: Thông tin chung, Dự án con, Báo giá, '
    'Meetings) cùng các thao tác Chốt giải pháp, Gia hạn, Đóng dự án.',
    'Làm rõ vòng đời trạng thái (Tiến trình nội bộ) của dự án, ai được thao tác gì ở bước nào và ai nhận thông báo.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Dự án TKT', 'Dự án tiền khả thi — cơ hội kinh doanh với một khách hàng, đi từ thu thập thông tin tới làm giải '
     'pháp, báo giá và hợp đồng.'),
    ('Dự án độc lập', 'Dự án không phải dự án cha và không thuộc dự án cha nào.'),
    ('Dự án cha / Dự án con', 'Dự án cha gom nhiều dự án con của cùng một khách hàng (mã dạng ...DAC...); dự án con '
     'kế thừa khách hàng, tiền tệ, giảm giá, bảng giá từ dự án cha.'),
    ('KH thương mại dịch vụ', 'Khách hàng trực tiếp chỉ là trung gian thương mại; khi tích, form có thêm khối '
     '“Khách hàng thụ hưởng cuối” (KH cuối).'),
    ('NV KD phụ trách', 'Nhân viên KD chính của dự án — mặc định là người lập dự án.'),
    ('KD hỗ trợ', 'Nhân viên được gán tên trong khối “Phòng KD hỗ trợ & KD hỗ trợ”.'),
    ('Cách triển khai', 'Tự triển khai / Triển khai theo Phòng / Liên phòng ban — quyết định có gửi yêu cầu làm '
     'giải pháp cho bộ phận giải pháp hay KD tự làm.'),
    ('YCGP', 'Yêu cầu làm giải pháp.'),
    ('YCXD giá / YCBG', 'Yêu cầu xây dựng giá (yêu cầu tính giá bán) gửi cho người làm giá.'),
    ('Phiếu thu thập thông tin', 'Bộ câu hỏi khảo sát theo Ứng dụng của dự án, bản chụp riêng cho từng dự án.'),
    ('Hạn đóng tự động', 'Mốc ngày hệ thống tự đóng dự án nếu chưa chuyển sang hợp đồng; lùi được bằng đề xuất '
     'Gia hạn đã duyệt.'),
    ('Tiến trình nội bộ', 'Trạng thái của dự án (12 bước với dự án thường/con, 8 bước với dự án cha).'),
], widths=[1.8, 4.2])

# ======================================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Thêm khách hàng', 'Hiện nút “Thêm nhanh khách hàng” trên form Tạo mới / Sửa dự án.'),
    ('Q2', 'Xây dựng giá bán theo phòng', 'Hiện nút “Sao chép báo giá” với báo giá lập từ yêu cầu xây dựng giá, '
     'khi dự án Triển khai theo Phòng.'),
    ('Q3', 'Xây dựng giá bán theo công ty', 'Như Q2, khi dự án Tự triển khai hoặc Liên phòng ban.'),
    ('Q4', 'Xem giá vốn hàng hoá', 'Quyết định file Excel báo giá xuất từ tab Báo giá có cột giá vốn hay không.'),
    ('Q5', 'Trưởng phòng duyệt gia hạn dự án TKT', 'Nhận thông báo khi có đề xuất gia hạn; duyệt ở màn “Gia hạn dự '
     'án TKT” (đặc tả ở tài liệu riêng).'),
    ('Q6', 'Ban giám đốc duyệt gia hạn dự án TKT', 'Như Q5, ở cấp Ban giám đốc.'),
], widths=[0.8, 2.0, 3.2])
d.p('Hệ thống KHÔNG có quyền riêng cho Thêm / Sửa / Xóa / Đóng dự án. Các thao tác này do VAI TRÒ của người dùng '
    'trên từng dự án quyết định:')
d.table(['Ký hiệu', 'Vai trò', 'Tác dụng trên màn hình'], [
    ('R1', 'Người tạo dự án', 'Thấy dự án (kể cả bản nháp của mình); Sửa; Xóa khi dự án Đang tạo và chưa có dự án '
     'con; Tạo yêu cầu làm giải pháp; Tạo meeting; Lưu phiếu thu thập thông tin.'),
    ('R2', 'NV KD phụ trách (NV KD chính)', 'Chốt giải pháp, Gia hạn, Đóng dự án; tạo/chốt/hủy chốt báo giá, sửa '
     'ghi chú kinh doanh, đồng bộ hàng tạm; tạo yêu cầu điều chỉnh giải pháp; tạo báo giá tổng (dự án cha).'),
    ('R3', 'KD hỗ trợ được gán tên', 'Chỉ XEM dự án; được tạo meeting.'),
    ('R4', 'PM giải pháp / Quản lý phòng tiếp nhận', 'Tiếp nhận / Từ chối yêu cầu điều chỉnh giải pháp; PM giải '
     'pháp được tạo meeting.'),
    ('R5', 'Người lập báo giá', 'Sửa / Xóa báo giá Đang tạo; lập hợp đồng ERP từ báo giá trúng thầu.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem danh sách dự án tiền khả thi theo tổng công ty', 'Toàn bộ dự án (trừ bản nháp của người khác).'),
    ('V2', 'Xem danh sách dự án tiền khả thi theo công ty', 'Dự án thuộc công ty đang làm việc.'),
    ('V3', 'Xem danh sách dự án tiền khả thi theo phòng ban',
     'Dự án thuộc phòng ban hoặc bộ phận mình quản lý, cộng dự án mình tạo.'),
    ('V4', 'Xem danh sách dự án tiền khả thi theo bộ phận', 'Dự án thuộc bộ phận mình quản lý, cộng dự án mình tạo.'),
    ('–', 'Không có quyền nào', 'Chỉ dự án mình tạo.'),
], widths=[0.8, 2.4, 2.8])
d.p('Cộng thêm vào phạm vi trên, người dùng luôn thấy dự án mình được gán tên là KD hỗ trợ. '
    'Công ty / phòng ban / bộ phận của dự án lấy theo NGƯỜI TẠO lúc tạo dự án.')

d.h2('2 Ma trận phân quyền')
Y, N = '✅', '❌'
d.table(['Chức năng', 'R1', 'R2', 'R3', 'V1–V4', 'Không vai trò, không quyền'], [
    ('FR-01 Xem danh sách dự án', Y, Y, Y, '✅ (theo phạm vi)', '✅ (dự án mình tạo)'),
    ('FR-02 Tìm kiếm và lọc', Y, Y, Y, Y, Y),
    ('FR-03 Cài đặt bộ lọc', Y, Y, Y, Y, Y),
    ('FR-04 Tuỳ chỉnh cột', Y, Y, Y, Y, Y),
    ('FR-05 Xuất Excel', Y, Y, Y, '✅ (theo phạm vi)', Y),
    ('FR-06 Tạo mới dự án', Y, Y, Y, Y, Y),
    ('FR-07 Thêm nhanh khách hàng', '✅ (cần Q1)', '✅ (cần Q1)', '✅ (cần Q1)', '✅ (cần Q1)', N),
    ('FR-08 Chỉnh sửa dự án', Y, N, N, Y, N),
    ('FR-09 Xóa dự án', '✅ (Đang tạo, chưa có con)', N, N, N, N),
    ('FR-10 Tạo giải pháp / Tạo yêu cầu làm giải pháp', Y, '✅ (Tạo giải pháp)', '✅ (Tạo giải pháp)',
     '✅ (Tạo giải pháp)', N),
    ('FR-11 Xem chi tiết dự án', Y, Y, Y, Y, N),
    ('FR-12 → FR-13, FR-15 → FR-19 Xem các tab', Y, Y, Y, Y, N),
    ('FR-14 Yêu cầu điều chỉnh giải pháp', 'Xem', '✅ (Tạo)', 'Xem', 'Xem', N),
    ('FR-20 Báo giá của dự án', 'Xem', '✅ (Tạo báo giá, ghi chú KD)', 'Xem', 'Xem', N),
    ('FR-21 Chốt / Hủy chốt báo giá trúng thầu', N, Y, N, N, N),
    ('FR-22 Đồng bộ hàng tạm & lập hợp đồng ERP', N, '✅ (Gửi duyệt, cập nhật)', N, N, N),
    ('FR-23 Báo giá của dự án cha', 'Xem', '✅ (Tạo báo giá tổng)', 'Xem', 'Xem', N),
    ('FR-24 Dự án con', Y, Y, Y, Y, N),
    ('FR-25 Xem đề xuất gia hạn', Y, Y, Y, Y, N),
    ('FR-26 Nhập phiếu thu thập thông tin', Y, 'Xem', 'Xem', Y, N),
    ('FR-27 Lịch sử thay đổi phiếu', Y, Y, Y, Y, N),
    ('FR-28 Xem mẫu in phiếu', Y, Y, Y, Y, N),
    ('FR-29 Chốt giải pháp', N, Y, N, N, N),
    ('FR-30 Gửi đề xuất gia hạn', N, Y, N, N, N),
    ('FR-31 Đóng dự án', N, Y, N, N, N),
], widths=[2.4, 0.8, 0.9, 0.6, 0.7, 0.8])
d.p('R4 (PM giải pháp / quản lý phòng tiếp nhận) được Tiếp nhận / Từ chối yêu cầu điều chỉnh ở FR-14; R5 (người lập '
    'báo giá) được Sửa / Xóa báo giá Đang tạo và Lập hợp đồng ERP ở FR-20, FR-22. Thường người tạo dự án (R1) cũng '
    'là NV KD phụ trách (R2) vì ô NV KD chính tự gán người lập và bị khoá. Nút không dùng được thì ẩn hẳn.')

# ======================================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
MAINS = [
    ('FR-01', 'Xem danh sách dự án', 'view'),          # 0
    ('FR-05', 'Xuất Excel', 'io'),                      # 1
    ('FR-06', 'Tạo mới dự án', 'crud'),                 # 2
    ('FR-08', 'Chỉnh sửa dự án', 'crud'),               # 3
    ('FR-09', 'Xóa dự án', 'action'),                   # 4
    ('FR-10', 'Tạo giải pháp / YC làm GP', 'action'),   # 5
    ('FR-14', 'Yêu cầu điều chỉnh GP', 'action'),       # 6
    ('FR-20', 'Báo giá của dự án', 'crud'),             # 7
    ('FR-21', 'Chốt / Hủy chốt báo giá', 'action'),     # 8
    ('FR-22', 'Đồng bộ hàng tạm & HĐ ERP', 'io'),       # 9
    ('FR-23', 'Báo giá dự án cha', 'crud'),             # 10
    ('FR-24', 'Thêm dự án con', 'crud'),                # 11
    ('FR-26', 'Nhập phiếu thu thập', 'crud'),           # 12
    ('FR-29', 'Chốt giải pháp', 'action'),              # 13
    ('FR-30', 'Gửi đề xuất gia hạn', 'action'),         # 14
    ('FR-31', 'Đóng dự án', 'action'),                  # 15
]
d.overview_figure2(
    [(A_ALL, [0, 1, 2, 3, 4, 5, 11, 12]), (A_KD, [6, 7, 8, 9, 10, 13, 14, 15]), (A_PM, [6])],
    MAINS,
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-11', 'Xem chi tiết dự án', 'view', 'extend', [0], None),
     ('FR-07', 'Thêm nhanh khách hàng', 'crud', 'extend', [2], None)],
    'Sơ đồ Use Case tổng quan màn Dự án tiền khả thi')
d.p('Các tab chỉ xem của màn chi tiết (FR-12, FR-13, FR-15 → FR-19, FR-25, FR-27, FR-28) là một phần của chức '
    'năng Xem chi tiết dự án (FR-11) nên không vẽ riêng trên sơ đồ.')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1
fn(1, 'Xem danh sách dự án', dict(
    ten='Xem danh sách dự án tiền khả thi',
    mota='Hiển thị bảng dự án người dùng được xem: dự án cha và dự án độc lập ở cấp 1, dự án con nằm dưới dự án '
         'cha (mở rộng để xem); mỗi dòng có các nút thao tác theo vai trò của người dùng.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập hệ thống.',
    chinh='1. Người dùng vào menu Dự án TKT của phân hệ CSKH trước bán.\n'
          '2. Hệ thống nạp danh sách trong phạm vi được xem (BR-01), mới tạo trước, 10 dòng/trang.\n'
          '3. Dòng dự án cha có nút mũi tên ở cột STT kèm số dự án con; bấm để mở/thu gọn các dòng dự án con.\n'
          '4. Mỗi dòng hiển thị các nút thao tác người dùng được phép (Sửa, Xóa, Tạo giải pháp, Tạo yêu cầu làm '
          'giải pháp).',
    phu='• Không có dự án khớp → bảng hiển thị “Không có dữ liệu phù hợp bộ lọc.”.\n'
        '• Lỗi khi nạp → thông báo “Lỗi khi tải dữ liệu”.\n'
        '• Lỗi khi mở dự án con → thông báo “Lỗi khi tải danh sách dự án con”.\n'
        '• Dự án Đang tạo (bản nháp) chưa có mã → ô Mã dự án để trống; mở bản nháp bằng nút Sửa.\n'
        '• Quay lại màn trong vòng 10 phút → khôi phục bộ lọc đã dùng.'),
    [MENU], [('01-danh-sach.png', 'Danh sách dự án tiền khả thi lúc mới mở'),
             ('01d-cay-cha-con.png', 'Dự án cha đang mở rộng, hiện các dự án con'),
             ('01b-danh-sach-phai.png', 'Các cột cuối bảng: người tạo/cập nhật, Tiến trình nội bộ, Hành động')],
    [
        ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Danh sách dự án tiền khả thi', '–'),
        ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', 'Mở form Tạo mới dự án (FR-06).'),
        ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', 'Khoá trong lúc đang xuất (FR-05).'),
        ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Mở popup Tuỳ chỉnh cột (FR-04).'),
        ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo trang',
         'Ghim trái. Dòng dự án cha có con: nút mũi tên (“Xem dự án con” / “Thu gọn”); dòng con hiện ký hiệu “└”.'),
        ('Cột Mã dự án', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         'Ghim trái, là liên kết mở màn chi tiết (FR-11); trống với dự án Đang tạo. Có sắp xếp.'),
        ('Cột Tên dự án TKT', 'Table/Grid', 'Read-only', '0–255 ký tự', 'Theo dữ liệu', 'Tối đa 2 dòng. Có sắp xếp.'),
        ('Cột Loại dự án', 'Badge', 'Read-only', 'Danh sách 3 giá trị', 'Theo dữ liệu',
         '“Dự án cha” (kèm “n DA con”) / “Dự án con” / “Độc lập”.'),
        ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         '“Mã - Tên khách hàng”, dòng phụ “Người liên hệ: tên • SĐT”.'),
        ('Cột Khách hàng cuối', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         'Chỉ có giá trị khi dự án là KH thương mại dịch vụ; kèm người liên hệ.'),
        ('Cột Giải pháp / Version giải pháp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         '“Mã - Tên giải pháp”; version dạng badge.'),
        ('Cột Giai đoạn dự án KH / Quy mô dự án / Phân loại đầu tư / Nguồn vốn', 'Table/Grid', 'Read-only', '–',
         'Theo dữ liệu', '–'),
        ('Cột Tổng số ngày hoàn thành', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu', '“n ngày”. Có sắp xếp.'),
        ('Cột Phòng làm GP / PM giải pháp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'PM kèm dòng “SĐT:”.'),
        ('Cột Ngày KH cần GP / Ngày dự kiến chốt GP', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
         'Có sắp xếp.'),
        ('Cột Ứng dụng / Lĩnh vực kinh doanh khách hàng / Loại hình hoạt động khách hàng', 'Table/Grid',
         'Read-only', '–', 'Theo dữ liệu', '–'),
        ('Cột KD phụ trách', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '“Tên NV - Phòng ban - Bộ phận”.'),
        ('Cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only',
         'dd/mm/yyyy hh:mm', 'Theo dữ liệu', 'Ngày tạo, Ngày cập nhật có sắp xếp.'),
        ('Cột Tiến trình nội bộ', 'Badge', 'Read-only', 'Danh sách 12 giá trị (dự án cha 8)', 'Theo dữ liệu',
         'Chữ và màu theo trạng thái (BR-04).'),
        ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo vai trò',
         'Sửa · Xóa · Tạo giải pháp · Tạo yêu cầu làm giải pháp; 2 nút đầu hiện trực tiếp, còn lại gom vào '
         'menu “⋮”. Nút không đủ điều kiện thì ẩn.'),
        ('Phân trang', 'Pagination', 'Enable', '10 / 20 / 50 / 100', '10 dòng/trang', 'Đơn vị “dự án”.'),
        ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
    ],
    [
        ('Mở màn Dự án TKT', 'System', 'During:\n' + SCOPE + '\n– Bản nháp của người khác không bao giờ hiện.\n'
         '– Chỉ trả dự án cha và dự án độc lập; dự án con nạp khi mở rộng.\nAfter:\n– Hiển thị bảng; khôi phục '
         'bộ lọc nếu quay lại trong 10 phút.\n– Lỗi → “Lỗi khi tải dữ liệu”.'),
        ('Bấm mũi tên ở cột STT của dự án cha', 'Click',
         'After:\n– Lần đầu nạp danh sách dự án con, chèn ngay dưới dòng cha (nền khác màu); bấm lại để thu gọn.\n'
         '– Lỗi → “Lỗi khi tải danh sách dự án con”.'),
        ('Bấm Mã dự án', 'Click', 'After:\n– Mở màn chi tiết dự án (FR-11); chuột phải mở được tab mới.'),
        ('Bấm tiêu đề cột có sắp xếp', 'Click', 'After:\n– Sắp xếp tăng/giảm, về trang 1.'),
        ('Đổi trang / số dòng mỗi trang', 'Click', 'After:\n– Nạp lại đúng trang; đổi số dòng thì về trang 1.'),
    ], ui_mode='read')

# ------------------------------------------------------------------ 2.2
fn(2, 'Tìm kiếm và lọc', dict(
    ten='Tìm kiếm và lọc dự án',
    mota='Tìm nhanh theo từ khoá và lọc nâng cao theo 13 ô lọc.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách dự án.',
    chinh='1. Người dùng gõ từ khoá vào ô tìm nhanh rồi bấm “Tìm kiếm” (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc và chọn giá trị ở các ô lọc.\n'
          '3. Chọn giá trị ở ô chọn thì hệ thống lọc ngay; ô gõ tay chỉ lọc khi bấm “Tìm kiếm”.\n'
          '4. Hệ thống nạp lại danh sách theo điều kiện, về trang 1.',
    phu='• Bấm “Làm mới” → xoá hết điều kiện lọc, nạp lại danh sách.\n'
        '• Có từ khoá → kết quả trả phẳng (gồm cả dự án con), không còn dạng cây.\n'
        '• Đổi Công ty / Phòng ban / Bộ phận → ô Nhân viên KD phụ trách bị xoá và danh sách chọn thu hẹp theo.\n'
        '• Chọn Ứng dụng → ô Loại hình / Lĩnh vực chỉ còn giá trị thuộc các ứng dụng đã chọn và ngược lại.'),
    [MENU + ' => Tìm kiếm nâng cao'], [('02-loc.png', 'Khối Tìm kiếm nâng cao đang mở')],
    [
        ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
         'Placeholder “Tìm theo tên dự án, mã KH, tên KH”; hệ thống tìm gần đúng theo Tên dự án, Mã dự án, Mã KH, '
         'Tên KH.'),
        ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tìm theo điều kiện / xoá điều kiện.'),
        ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn', 'Mở / ẩn khối lọc (“Ẩn tìm kiếm nâng cao”).'),
        ('Công ty / Phòng ban / Bộ phận', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Không', 'Theo quyền',
         'Mở theo quyền xem theo cấp; ô vượt quyền bị khoá (biểu tượng ổ khoá).'),
        ('Nhân viên KD phụ trách', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
         '“Tên - Mã phòng - Mã NV”; chỉ nhân viên trong phạm vi quyền và đơn vị đang chọn.'),
        ('Khách hàng / Khách hàng cuối', 'Dropdown', 'Enable', 'Gõ tối thiểu 2 ký tự', 'Không', 'Trống',
         'Tìm theo mã hoặc tên khách hàng, tối đa 20 kết quả; hiển thị “Mã - Tên”.'),
        ('Giai đoạn dự án KH', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
         'Kèm icon ⓘ mô tả từng giai đoạn.'),
        ('Loại dự án', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Trống',
         'Dự án cha / Dự án con / Dự án độc lập.'),
        ('Nguồn vốn', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống',
         'Vốn tự có / Vốn vay ngân hàng / Ngân sách nhà nước / Kết hợp nhiều nguồn / Khác.'),
        ('Phân loại đầu tư', 'Dropdown', 'Enable', 'Danh sách 7 giá trị', 'Không', 'Trống',
         'Dự án mới / Mở rộng nâng cấp / Thay thế thiết bị / Bổ sung thiết bị / Sửa chữa thiết bị / Cung cấp '
         'dịch vụ đi kèm / Khác.'),
        ('Quy mô dự án', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Trống', 'Nhỏ / Vừa / Lớn / Trọng điểm.'),
        ('Tiến trình nội bộ', 'Dropdown', 'Enable', 'Danh sách 12 giá trị', 'Không', 'Trống', 'Xem BR-04.'),
        ('Ứng dụng', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
         'Chọn nhiều, có ô tìm và “chọn tất cả”.'),
        ('Loại hình hoạt động – Lĩnh vực kinh doanh khách hàng', 'Dropdown', 'Enable', 'Danh sách', 'Không',
         'Trống', 'Cặp ô cha – con chọn nhiều; chọn Loại hình riêng (không kèm Lĩnh vực) thì lọc theo Loại hình.'),
        ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Khoảng từ ngày – đến ngày.'),
    ],
    [
        ('Gõ ô tìm nhanh rồi Enter / bấm Tìm kiếm', 'Keypress / Click',
         'During:\n' + SCOPE + '\nAfter:\n– Lọc gần đúng theo Tên dự án, Mã dự án, Mã KH, Tên KH; về trang 1.'),
        ('Chọn giá trị ở ô lọc', 'Change', 'After:\n– Lọc ngay, về trang 1; lưu bộ lọc để khôi phục khi quay lại.'),
        ('Gõ ô Khách hàng / Khách hàng cuối', 'Keypress',
         'Before:\n– Chưa đủ 2 ký tự → không tìm.\nAfter:\n– Hiện tối đa 20 khách hàng khớp mã hoặc tên.'),
        ('Bấm Làm mới', 'Click', 'After:\n– Xoá toàn bộ điều kiện, nạp lại danh sách đúng 1 lần.'),
    ], rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'))

# ------------------------------------------------------------------ 2.3
fn(3, 'Cài đặt bộ lọc', dict(
    ten='Cài đặt bộ lọc',
    mota='Chọn ô lọc nào hiển thị trong khối Tìm kiếm nâng cao và thứ tự của chúng.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách dự án.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n2. Tích / bỏ tích ô lọc, kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '3. Bấm “Lưu” → khối lọc hiển thị theo cài đặt mới.',
    phu='• Bấm “Khôi phục mặc định” → trả về đủ 13 ô theo thứ tự gốc.\n• Bấm “Đóng” → không lưu thay đổi.'),
    [MENU + ' => Cài đặt bộ lọc'], [('03-cai-dat-loc.png', 'Popup Cài đặt bộ lọc')],
    [
        ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc',
         'Dòng mô tả: “Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng '
         'màn hình.”'),
        ('Danh sách 13 ô lọc', 'Checkbox', 'Enable', '13 giá trị', 'Không', 'Đã tích hết',
         'Công ty – Phòng ban – Bộ phận, Nhân viên KD phụ trách, Khách hàng, Khách hàng cuối, Giai đoạn dự án KH, '
         'Loại dự án, Nguồn vốn, Phân loại đầu tư, Quy mô dự án, Tiến trình nội bộ, Ứng dụng, Loại hình hoạt động – '
         'Lĩnh vực kinh doanh khách hàng, Ngày tạo. Kéo thả để đổi thứ tự.'),
        ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình theo người dùng và màn hình.'),
        ('Nút Khôi phục mặc định / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ],
    [
        ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở popup với cấu hình đang dùng.'),
        ('Tích / bỏ tích, kéo thả', 'Change', 'After:\n– Cập nhật danh sách trong popup, chưa áp dụng.'),
        ('Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình riêng của người dùng cho màn này, khối lọc hiển thị lại theo '
         'cấu hình.'),
        ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đưa danh sách về 13 ô mặc định.'),
    ], rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'))

# ------------------------------------------------------------------ 2.4
fn(4, 'Tuỳ chỉnh cột', dict(
    ten='Tuỳ chỉnh cột hiển thị',
    mota='Ẩn / hiện và sắp xếp lại các cột của bảng danh sách; cấu hình lưu theo từng người dùng.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách dự án.',
    chinh='1. Người dùng bấm nút “Cấu hình cột hiển thị” cạnh nút Xuất Excel.\n2. Tích / bỏ tích cột, kéo ≡ để '
          'đổi thứ tự.\n3. Bấm “Lưu” → bảng hiển thị theo cấu hình mới.',
    phu='• Cột STT, Mã dự án, Hành động bị khoá (xám, biểu tượng ổ khoá): luôn hiện, không kéo được.\n'
        '• Mặc định hiện tất cả các cột.\n• Bấm “Đóng” → không lưu.'),
    [MENU + ' => Tuỳ chỉnh cột'], [('04-tuy-chinh-cot.png', 'Popup Tuỳ chỉnh cột')],
    [
        ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', '–'),
        ('Cột bị khoá: STT, Mã dự án, Hành động', 'Checkbox', 'Disable', '–', '–', 'Đã tích', 'Không bỏ tích được.'),
        ('Các cột còn lại', 'Checkbox', 'Enable', '23 cột', 'Không', 'Đã tích',
         'Tên dự án TKT, Loại dự án, Khách hàng, Khách hàng cuối, Giải pháp, Version giải pháp, Giai đoạn dự án KH, '
         'Quy mô dự án, Phân loại đầu tư, Nguồn vốn, Tổng số ngày hoàn thành, Phòng làm GP, PM giải pháp, Ngày KH '
         'cần GP, Ngày dự kiến chốt GP, Ứng dụng, Lĩnh vực kinh doanh khách hàng, Loại hình hoạt động khách hàng, KD '
         'phụ trách, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật, Tiến trình nội bộ. Kéo ≡ để đổi thứ tự.'),
        ('Nút Lưu / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ],
    [
        ('Bấm Cấu hình cột hiển thị', 'Click', 'After:\n– Mở popup với cấu hình đang dùng.'),
        ('Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình theo người dùng, bảng hiển thị lại đúng cột và thứ tự.'),
    ], rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'))

# ------------------------------------------------------------------ 2.5
fn(5, 'Xuất Excel', dict(
    ten='Xuất Excel danh sách dự án',
    mota='Xuất toàn bộ dự án khớp bộ lọc đang áp dụng ra file Excel, người dùng chọn cột cần xuất.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách dự án.',
    chinh='1. Người dùng bấm “Xuất Excel”.\n2. Popup “Chọn trường xuất file” mở, tích sẵn đúng các cột đang hiện '
          'trên bảng.\n3. Người dùng tích/bỏ tích, kéo ≡ để đổi thứ tự cột trong file.\n4. Bấm “Xuất file” → '
          'tải file danh_sach_du_an_tien_kha_thi.xlsx, thông báo “Xuất Excel thành công”.',
    phu='• Lỗi → “Lỗi khi xuất Excel”.\n• Bấm “Chọn tất cả” / “Bỏ chọn hết” để chọn nhanh.\n'
        '• File lấy TẤT CẢ dòng (không phân trang) và có cả dự án con.'),
    [MENU + ' => Xuất Excel'], [('20-xuat.png', 'Popup Chọn trường xuất file')],
    [
        ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất file',
         'Dòng mô tả: “Tích chọn trường cần xuất, kéo ≡ để đổi thứ tự cột trong file.”'),
        ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
        ('Danh sách 32 trường', 'Checkbox', 'Enable', '32 giá trị', 'Có (≥ 1)', 'Các cột đang hiện',
         'Mã dự án, Tên dự án TKT, Loại dự án, Mã/Tên khách hàng, Người liên hệ KH, SĐT người liên hệ KH, Mã/Tên '
         'khách hàng cuối, Mã/Tên giải pháp, Version giải pháp, Giai đoạn dự án, Quy mô dự án, Phân loại đầu tư, '
         'Nguồn vốn, Tổng số ngày hoàn thành, Phòng làm GP, PM giải pháp, Ngày KH cần GP, Ngày dự kiến chốt GP, Ứng '
         'dụng, Lĩnh vực / Loại hình khách hàng, NV KD phụ trách, Phòng ban, Bộ phận, Tiến trình nội bộ, Người tạo, '
         'Ngày tạo, Người cập nhật, Ngày cập nhật.'),
        ('Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Theo lựa chọn', '“Đang chọn a/32 trường”.'),
        ('Nút Xuất file / Đóng', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khoá trong lúc đang xuất.'),
    ],
    [
        ('Bấm Xuất Excel', 'Click', 'After:\n– Mở popup, tích sẵn cột đang hiện trên bảng.'),
        ('Bấm Xuất file', 'Click',
         'During:\n' + SCOPE + '\n– Áp đúng bộ lọc và sắp xếp đang dùng, lấy mọi dòng kể cả dự án con.\n'
         'After:\n– Tải file “danh_sach_du_an_tien_kha_thi.xlsx” tiêu đề “Danh sách dự án tiền khả thi”, cột theo '
         'thứ tự đã chọn; ngày dd/mm/yyyy, ngày tạo/cập nhật dd/mm/yyyy hh:mm.\n– Thông báo “Xuất Excel thành công”; '
         'lỗi → “Lỗi khi xuất Excel”.'),
    ], uc=('FR-05', 'Xuất Excel danh sách dự án', 'io', A_ALL), rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'))

# ------------------------------------------------------------------ 2.6 Tạo mới
ERR_TOAST = ('– Lỗi nhập liệu → thông báo “Bạn chưa nhập đầy đủ thông tin”, tô đỏ và ghi lỗi dưới từng ô, cuộn '
             'tới ô lỗi đầu tiên.\n– Không có quyền → “Bạn không có quyền thực hiện chức năng này”.\n'
             '– Ứng dụng / Giai đoạn vừa bị khoá → “Thao tác không thành công. Dữ liệu đã được thay đổi hoặc chuyển '
             'trạng thái bởi người dùng khác. Vui lòng tải lại trang để cập nhật thông tin mới nhất.”\n'
             '– Lỗi khác → “Có lỗi xảy ra”.')
FORM_UI = [
    # Khối 1
    ('Khối “1. Thông tin khách hàng” – Khách hàng trực tiếp', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Khách hàng', 'Textbox', 'Enable / Read-only', 'Danh sách', 'Có', 'Trống',
     'Bấm vào ô (placeholder “Nhấn vào đây để chọn thông tin khách hàng”) mở popup “Chọn khách hàng”. Khoá với '
     'dự án con (kế thừa từ cha) và khi mở từ báo cáo CSKH tiềm năng (“Khách hàng theo nhu cầu đã chọn”).'),
    ('Nút “+ Thêm nhanh khách hàng”', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi thiếu quyền',
     'Chỉ hiện khi có quyền “Thêm khách hàng” và ô Khách hàng không bị khoá (FR-07).'),
    ('Popup “Chọn khách hàng”', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Ô lọc Tên / Mã khách hàng, Mã số thuế, Số điện thoại + nút Tìm kiếm / Làm mới; bảng STT, Mã KH - Tên khách '
     'hàng, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP; phân trang 10/25/50/100; nút Đóng. Chỉ liệt kê KH '
     'đang hoạt động. Bấm 1 dòng để chọn → “Chọn khách hàng thành công”; KH đang được Sales khác đăng ký → “Đã có '
     'người đăng ký nên bạn không được phép chọn”.'),
    ('KH thương mại dịch vụ', 'Checkbox', 'Enable', '–', 'Không', 'Bỏ tích',
     'Tích → hiện khối “Khách hàng thụ hưởng cuối”, ẩn Loại hình / Lĩnh vực ở khối KH trực tiếp (BR-06).'),
    ('Khung thông tin KH', 'Text', 'Read-only', '–', '–', 'Ẩn',
     'Hiện sau khi chọn KH: Mã khách hàng, MST, SĐT, Họ và tên, Địa chỉ, Email, Liên hệ (ô trống hiện “-”).'),
    ('Đối tượng tổ chức', 'Text', 'Read-only', '–', '–', 'Theo KH',
     'Cá nhân / Doanh nghiệp tư nhân / Doanh nghiệp nước ngoài / Tổ chức phi chính phủ / Cơ quan nhà nước.'),
    ('Loại hình hoạt động khách hàng', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Có khi không tích KH TMDV',
     'Tự chọn nếu KH chỉ khai 1 giá trị',
     'Có ô tìm “Tìm loại hình hoạt động...”, nút “Bỏ chọn”; giá trị đã có trong hồ sơ KH gắn dấu tích (“Đã có trong '
     'hồ sơ khách hàng”). Ẩn khi tích KH TMDV hoặc là dự án cha.'),
    ('Lĩnh vực kinh doanh khách hàng', 'Dropdown', 'Enable / Ẩn', 'Danh sách 2 cấp', 'Có khi không tích KH TMDV',
     'Tự chọn nếu KH chỉ khai 1 giá trị',
     'Chọn Lĩnh vực → tự gán Loại hình cha; đổi Loại hình → xoá Lĩnh vực không thuộc. Rỗng: “Không tìm thấy kết '
     'quả phù hợp.”'),
    ('Email khách hàng', 'Textbox', 'Enable', '0–255 ký tự, định dạng email', 'Không', 'Email của KH',
     'Lỗi: “Email khách hàng không đúng định dạng.” / “Email khách hàng không quá 255 ký tự.”'),
    ('Người liên hệ', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Có với KH doanh nghiệp (trừ dự án con)', 'Trống',
     'Placeholder “Chọn liên hệ (gõ SĐT đầy đủ để tìm liên hệ khác)”; hiển thị “Tên — Chức vụ”. Ẩn với KH cá nhân. '
     'Liên hệ đang bị Sales khác đăng ký hiện “— 🔒 Đã có người đăng ký”, chọn thì báo “Đã có người đăng ký nên bạn '
     'không được phép chọn”. Chọn xong hiện khung Tên / Chức vụ / Điện thoại / Email.'),
    ('Nút “Thêm nhanh liên hệ”', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi chưa chọn KH',
     'Mở khung nhập Họ tên (*), Chức vụ (*), SĐT (*) (placeholder “VD: Nguyễn Văn A”, “VD: Trưởng phòng CNTT”, '
     '“VD: 098xxxxxxx”) + nút “Lưu & chọn”, “Hủy”. SĐT phải bắt đầu bằng 0, 10–12 chữ số.'),
    ('Nhu cầu khách hàng', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Không', 'Trống',
     'Chỉ ở khối KH trực tiếp. Placeholder theo tình huống: “Chọn Khách hàng trước” / “Đang tải nhu cầu...” / '
     '“Khách hàng chưa có nhu cầu đang theo dõi” / “Chọn Nhu cầu khách hàng”. Chỉ liệt kê nhu cầu “Đang theo dõi” '
     'từ meeting giới thiệu sản phẩm đã hoàn thành do chính người dùng chủ trì.'),
    ('Khối “Khách hàng thụ hưởng cuối”', 'Label', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Chỉ hiện khi tích KH TMDV; gồm Khách hàng (bắt buộc), Thêm nhanh khách hàng, Đối tượng tổ chức, Loại hình / '
     'Lĩnh vực (bắt buộc), “Email khách hàng thụ hưởng cuối” (bắt buộc khi Lưu), Người liên hệ (không bắt buộc), '
     'Thêm nhanh liên hệ. Không có ô Nhu cầu khách hàng.'),
    # Khối 2
    ('Tên dự án TKT', 'Textbox', 'Enable', '0–255 ký tự', 'Có (kể cả Lưu nháp)', 'Trống',
     'Placeholder “Nhập tên dự án tiền khả thi”.'),
    ('Loại dự án', 'Dropdown', 'Enable / Disable', 'Danh sách 3 giá trị', 'Có', 'Dự án độc lập',
     'Dự án độc lập / Dự án cha / Dự án con (thuộc 1 dự án cha). Khoá khi mở từ nút “Thêm dự án con”. Chọn “Dự án '
     'cha” → tiêu đề đổi thành “Tạo mới dự án cha” và form rút gọn (BR-07).'),
    ('Chọn dự án cha', 'Dropdown', 'Enable / Ẩn', 'Danh sách (tối đa 200)', 'Có khi Loại = Dự án con', 'Trống',
     'Placeholder “Tìm dự án cha theo mã / tên / khách hàng...”; chỉ dự án cha đã lưu chính thức, chưa đóng. Lỗi '
     'thiếu: “Vui lòng chọn dự án cha cho dự án con.”. Chọn xong kế thừa ngay KH, KH cuối, tiền tệ, giảm giá, bảng '
     'giá, NV KD chính của cha.'),
    ('Ứng dụng (+ icon mẫu phiếu ⓘ)', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Có', 'Trống',
     'Placeholder “Chọn ứng dụng”, hiển thị “mã - tên”; lọc theo Loại hình + Lĩnh vực của KH cuối. Không có ứng '
     'dụng phù hợp → “Hãy liên hệ với bộ phận quản lý để yêu cầu khởi tạo ứng dụng phù hợp”. Icon mẫu phiếu: '
     '“Xem chi tiết mẫu phiếu thu thập thông tin” (bấm mở mẫu phiếu ở tab mới) hoặc “Chưa cấu hình mẫu phiếu thu '
     'thập thông tin cho ứng dụng này”. Ẩn ở dự án cha.'),
    ('Nút “Xem giải pháp”', 'Button', 'Enable / Disable', '–', '–', 'Mờ khi chưa chọn Ứng dụng',
     'Mở popup “Danh sách giải pháp” của ứng dụng đang chọn: ô tìm “Tìm theo mã, tên giải pháp, mã, tên khách hàng”, '
     'lọc Tiến trình giải pháp, Ngày cập nhật; bảng 19 cột (Mã-Tên giải pháp, Mã-Tên yêu cầu làm GP, Mã-Tên dự án, '
     'Khách hàng, Tiến trình GP, Version hiện tại…). Rỗng: “Không có giải pháp nào thuộc ứng dụng này.”'),
    ('Nhóm ngành', 'Dropdown', 'Enable', 'Danh sách (dự án cha: chọn nhiều)', 'Có', 'Trống',
     'Placeholder “Chọn nhóm ngành”. Rỗng: “Chưa khai báo nhóm ngành hoặc nhóm ngành đang thuộc dự án khác.” Đổi '
     'Ứng dụng / Nhóm ngành không còn khớp nhau → hộp xác nhận “Ứng dụng đang chọn không còn phù hợp” / “Nhóm ngành '
     'đang chọn không còn phù hợp” (nút Tiếp tục) rồi xoá giá trị cũ (BR-08).'),
    ('Quy mô dự án', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Có', 'Trống',
     'Nhỏ (dưới 5 tỷ) / Vừa (từ trên 5 tỷ đến dưới 20 tỷ) / Lớn (từ trên 20 tỷ đến dưới 50 tỷ) / Trọng điểm (từ 50 '
     'tỷ trở lên).'),
    ('Phân loại đầu tư', 'Dropdown', 'Enable / Ẩn', 'Danh sách 7 giá trị', 'Có', 'Trống', 'Ẩn ở dự án cha.'),
    ('Cách triển khai dự án', 'Dropdown', 'Enable / Disable / Ẩn', 'Danh sách 3 giá trị', 'Có (dấu *)',
     'Liên phòng ban', 'Tự triển khai / Triển khai theo Phòng / Liên phòng ban (BR-05). Ẩn ở dự án cha.'),
    ('Địa điểm triển khai', 'Textbox', 'Enable / Ẩn', '0–255 ký tự', 'Có', 'Trống',
     'Placeholder “Nhập địa điểm triển khai dự án”. Ẩn ở dự án cha.'),
    ('Mô tả chi tiết', 'Textarea', 'Enable', '–', 'Không', 'Trống',
     'Placeholder “Mô tả chi tiết về dự án, yêu cầu, phạm vi...”'),
    # Khối 3
    ('Giai đoạn dự án KH (+ ⓘ)', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Có', 'Trống',
     'Placeholder “Chọn giai đoạn dự án KH”; icon ⓘ mô tả từng giai đoạn. Ẩn ở dự án cha.'),
    ('Mức độ ưu tiên giải pháp', 'Dropdown', 'Disable', 'Danh sách', 'Có', 'Theo Giai đoạn',
     'Luôn khoá, tự điền theo Giai đoạn dự án KH. Ẩn ở dự án cha.'),
    ('Ngày bắt đầu dự án TKT', 'Datepicker', 'Disable', 'dd/mm/yyyy', 'Có ở dự án cha', 'Ngày hiện tại',
     'Luôn khoá, hệ thống gán bằng ngày tạo.'),
    ('Ngày kết thúc dự án TKT (+ ⓘ)', 'Datepicker', 'Enable', 'dd/mm/yyyy, ≥ ngày bắt đầu', 'Có ở dự án cha',
     'Trống', 'ⓘ “Ngày dự kiến chốt báo giá cuối cùng để chuyển sang giai đoạn ký hợp đồng”. Lỗi: “Ngày kết thúc '
     'dự án TKT phải lớn hơn hoặc bằng ngày hiện tại.” / “Ngày kết thúc dự án TKT phải lớn hơn hoặc bằng ngày bắt '
     'đầu dự án TKT.”'),
    ('Ngày KH cần nhận giải pháp', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy, ≥ hôm nay', 'Không', 'Trống',
     'Lỗi: “Ngày KH cần nhận giải pháp phải lớn hơn hoặc bằng ngày hiện tại.” / “Ngày KH cần nhận giải pháp phải '
     'lớn hơn hoặc bằng ngày chốt GP nội bộ.” Ẩn ở dự án cha.'),
    ('Ngày chốt GP nội bộ', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lỗi: “Ngày chốt GP nội bộ phải lớn hơn hoặc bằng ngày hiện tại.” / “Ngày chốt GP nội bộ phải nhỏ hơn hoặc '
     'bằng ngày KH cần nhận giải pháp.” Ẩn ở dự án cha.'),
    ('Tổng số ngày thực hiện', 'Number', 'Disable', '≥ 0', '–', 'Tự tính', '= Ngày kết thúc − Ngày bắt đầu + 1.'),
    # Cột phải
    ('Nhân viên KD chính', 'Dropdown', 'Disable', 'Danh sách', 'Có', 'Người đang đăng nhập',
     'Luôn khoá; dự án con lấy theo dự án cha. Khung Họ tên / SĐT / Email chỉ đọc.'),
    ('Phòng KD phụ trách chính', 'Textbox', 'Disable', '–', 'Có', 'Phòng của NV KD chính', '–'),
    ('Nút “Thêm phòng” (Phòng KD hỗ trợ & KD hỗ trợ)', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Thêm khối “Phòng hỗ trợ #n” (có nút X xoá khối); chưa có khối nào hiện “—”.'),
    ('Chọn phòng hỗ trợ', 'Dropdown', 'Enable', 'Danh sách', 'Có (trong khối)', 'Trống',
     'Một phòng không chọn trùng ở 2 khối. Lỗi: “Bắt buộc phải nhập”.'),
    ('Chọn KD hỗ trợ (thuộc phòng đã chọn)', 'Dropdown', 'Enable', 'Danh sách, chọn nhiều', 'Có (≥ 1)', 'Trống',
     'Placeholder “Tìm KD theo tên / mã / SĐT / email...”; chưa chọn phòng: “Vui lòng chọn phòng hỗ trợ.”. Danh '
     'sách đã chọn hiện “• Tên — SĐT — Email”.'),
    ('Có cần làm GP? (khối 5. Giải pháp)', 'Radio', 'Enable / Disable / Ẩn', 'Có / Không', 'Không',
     'Có (theo Cách triển khai)',
     'Tự chọn “Có” và khoá khi Cách triển khai là Theo Phòng / Liên phòng ban. Ẩn ở dự án cha.'),
    ('Chọn meeting khởi tạo (có thể nhiều)', 'Dropdown', 'Enable', 'Danh sách, chọn nhiều', 'Không', 'Trống',
     'Placeholder “Tìm meeting theo mã / tên...”; chỉ meeting của KH đang chọn do người tạo dự án chủ trì. Đổi KH '
     '→ xoá meeting đã chọn.'),
    ('Nguồn vốn', 'Dropdown', 'Enable / Ẩn', 'Danh sách 5 giá trị', 'Không', 'Trống', 'Ẩn ở dự án cha.'),
    ('Loại tiền tệ', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Có', 'VNĐ', 'Khoá ở dự án con.'),
    ('Giảm giá', 'Dropdown', 'Enable / Disable / Ẩn', 'Danh sách 3 giá trị', 'Có (dấu *)', 'Không giảm giá',
     'Chỉ hiện ở dự án cha / con; con bị khoá. Không giảm giá / Giảm giá theo mặt hàng / Giảm giá theo tổng.'),
    ('Bảng giá', 'Dropdown', 'Enable / Disable / Ẩn', 'Danh sách', 'Có ở dự án cha', 'Trống',
     'Chỉ hiện ở dự án cha / con; con bị khoá.'),
    ('Ngân sách dự kiến (dự án cha: Tổng ngân sách dự kiến)', 'Number', 'Enable', '≥ 0', 'Có', 'Trống',
     'Ô tiền, định dạng 1,234,567.'),
    ('Ngân sách đã phân bổ', 'Number', 'Disable / Ẩn', '≥ 0', '–', '0',
     'Chỉ dự án cha; tự cộng ngân sách các dự án con.'),
    ('Giá trị HĐ kỳ vọng / Lợi nhuận kỳ vọng', 'Number', 'Enable / Ẩn', '≥ 0', 'Không', 'Trống', 'Ẩn ở dự án cha.'),
    ('Nút Lưu nháp / Lưu / Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu nháp: lưu trạng thái Đang tạo. Lưu: lưu chính thức (Thu thập thông tin dự án). Quay lại: về nơi đi vào.'),
]
fn(6, 'Tạo mới dự án', dict(
    ten='Tạo mới dự án tiền khả thi',
    mota='Lập dự án mới (độc lập, dự án cha hoặc dự án con) với thông tin khách hàng, thông tin dự án, timeline, '
         'phụ trách KD, giải pháp, liên kết meeting và tài chính; lưu nháp hoặc lưu chính thức.',
    tacnhan='Nhân viên kinh doanh; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập (không cần quyền riêng).',
    chinh='1. Người dùng bấm “Tạo mới” ở màn danh sách.\n'
          '2. Chọn Khách hàng trong popup “Chọn khách hàng” (hoặc Thêm nhanh khách hàng – FR-07), chọn Người liên '
          'hệ, Loại hình / Lĩnh vực, Nhu cầu khách hàng (nếu có).\n'
          '3. Nhập Tên dự án TKT, chọn Loại dự án, Ứng dụng, Nhóm ngành, Quy mô, Phân loại đầu tư, Cách triển khai, '
          'Địa điểm triển khai.\n'
          '4. Chọn Giai đoạn dự án KH (Mức độ ưu tiên tự điền), các ngày timeline.\n'
          '5. Thêm phòng / KD hỗ trợ (nếu có), chọn meeting khởi tạo, nhập Nguồn vốn, Ngân sách dự kiến…\n'
          '6. Bấm “Lưu” → hệ thống kiểm tra, lưu dự án ở trạng thái “Thu thập thông tin dự án”, sinh mã, thông báo '
          '“Đã lưu thành công!” và quay về danh sách.',
    phu='• Bấm “Lưu nháp” → chỉ bắt buộc Tên dự án, lưu trạng thái “Đang tạo”, chưa sinh mã, thông báo “Đã lưu '
        'nháp thành công”.\n'
        '• Tích “KH thương mại dịch vụ” → nhập thêm Khách hàng thụ hưởng cuối (BR-06).\n'
        '• Chọn Loại dự án “Dự án cha” → form rút gọn: ẩn Ứng dụng, Phân loại đầu tư, Cách triển khai, Địa điểm, '
        'Giai đoạn, Mức độ ưu tiên, các ngày giải pháp, khối Giải pháp, Nguồn vốn, Giá trị HĐ / Lợi nhuận; bắt buộc '
        'Ngày bắt đầu, Ngày kết thúc, Bảng giá; Nhóm ngành chọn nhiều.\n'
        '• Chọn “Dự án con” → bắt buộc chọn dự án cha, kế thừa thông tin từ cha (BR-07).\n'
        '• Khách hàng có nhu cầu đang theo dõi mà chưa chọn → hộp xác nhận “Chưa chọn nhu cầu khách hàng”: “Khách '
        'hàng này đang có {N} nhu cầu chưa gắn dự án. Vẫn lưu dự án mà không chọn nhu cầu?” (nút “Tiếp tục lưu”).\n'
        '• Khung “Thêm nhanh liên hệ” còn gõ dở → chặn lưu, thông báo “Người liên hệ vừa nhập chưa được lưu”.\n'
        '• Thoát khi chưa lưu → hộp “Thông tin chưa lưu”: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” '
        '(Thoát / Ở lại).\n'
        '• Mở từ báo cáo CSKH tiềm năng → điền sẵn và khoá Khách hàng + Nhu cầu, điền Ngân sách dự kiến và Nhóm '
        'ngành; lưu xong quay về màn Nhu cầu khách hàng.',
    dacbiet='Ô Khách hàng không gõ tay được, chỉ chọn qua popup. Màn mở từ nút “Thêm dự án con” (FR-24) chọn sẵn '
            'và khoá Loại dự án / Dự án cha.'),
    [MENU + ' => Tạo mới'],
    [('05-tao-moi.png', 'Form Tạo mới dự án tiền khả thi (dự án độc lập)'),
     ('06-chon-kh.png', 'Popup Chọn khách hàng'),
     ('08-them-lien-he.png', 'Đã chọn khách hàng, đang mở khung Thêm nhanh liên hệ'),
     ('05b-kh-tmdv.png', 'Tích KH thương mại dịch vụ: thêm khối Khách hàng thụ hưởng cuối'),
     ('05c-du-an-cha.png', 'Loại dự án = Dự án cha: form rút gọn'),
     ('05d-du-an-con.png', 'Loại dự án = Dự án con: thêm ô Chọn dự án cha'),
     ('09-ds-giai-phap.png', 'Popup Danh sách giải pháp mở từ nút Xem giải pháp'),
     ('05f-loi.png', 'Bấm Lưu khi thiếu thông tin: lỗi hiện dưới từng ô')],
    FORM_UI,
    [
        ('Bấm Tạo mới', 'Click', 'After:\n– Mở form, Loại dự án = Dự án độc lập, Cách triển khai = Liên phòng ban, '
         'Loại tiền tệ = VNĐ, Ngày bắt đầu = hôm nay, NV KD chính = người đang đăng nhập.'),
        ('Chọn Khách hàng', 'Change',
         'After:\n– Nạp thông tin KH, người liên hệ, nhu cầu, Loại hình / Lĩnh vực đã khai; tự chọn nếu chỉ có 1.\n'
         '– Xoá Ứng dụng không còn phù hợp, xoá meeting và dự án cha đã chọn.'),
        ('Bấm Lưu & chọn (Thêm nhanh liên hệ)', 'Click',
         'During:\n– Họ tên, Chức vụ, SĐT trống → “Bắt buộc phải nhập”; SĐT sai → “Không hợp lệ”.\nAfter:\n– Lưu '
         'liên hệ vào hồ sơ KH và chọn luôn; “Thêm liên hệ thành công”. Thiếu thông tin → “Bạn chưa nhập đầy đủ '
         'thông tin”; lỗi khác → “Thêm liên hệ thất bại”.'),
        ('Đổi Cách triển khai', 'Change',
         'After:\n– Theo Phòng / Liên phòng ban → “Có cần làm GP?” = Có và khoá; Tự triển khai → mở khoá.'),
        ('Chọn Giai đoạn dự án KH', 'Change', 'After:\n– Tự điền Mức độ ưu tiên giải pháp.'),
        ('Đổi các ngày timeline', 'Change', 'During:\n– Kiểm tra ngay các ràng buộc ngày (BR-17), hiện lỗi dưới ô.'),
        ('Bấm Lưu nháp', 'Click',
         'Before:\n– Còn khung Thêm nhanh liên hệ gõ dở → “Người liên hệ vừa nhập chưa được lưu”, dừng.\n– KH có nhu '
         'cầu chưa chọn → hộp xác nhận, bấm huỷ thì dừng.\nDuring:\n– Tên dự án TKT trống → “Bắt buộc phải nhập”; '
         'chỉ kiểm định dạng các ô khác.\nAfter:\n– Lưu trạng thái Đang tạo, chưa sinh mã.\n– “Đã lưu nháp thành '
         'công”, về danh sách.\n' + ERR_TOAST),
        ('Bấm Lưu', 'Click',
         'Before:\n– Như Lưu nháp.\nDuring:\n– Ô bắt buộc trống → “Bắt buộc phải nhập” dưới ô.\n– Email sai → '
         '“Email khách hàng không đúng định dạng.”.\n– Nhóm ngành trùng / không khớp Ứng dụng / không thuộc cha → '
         'câu lỗi BR-08.\n– Dự án cha không hợp lệ → “Dự án cha không hợp lệ.” / “Dự án cha đã đóng, không thể gán '
         'thêm dự án con.” / “Dự án cha chưa lưu chính thức (đang ở trạng thái Đang tạo). Vui lòng hoàn tất thông '
         'tin khách hàng và bấm Lưu trước khi thêm dự án con.”\n– Nhu cầu KH → “Nhu cầu này vừa được gắn cho dự án '
         'khác. Vui lòng chọn lại.” / “Nhu cầu này đã quá hạn xử lý và bị đóng tự động. Không thể tạo Dự án tiền khả '
         'thi.” / “Nhu cầu không thuộc khách hàng của dự án.”\n– Có lỗi → không thực hiện After.\nAfter:\n– Lưu '
         'trạng thái “Thu thập thông tin dự án”, sinh mã (BR-03), tạo phiếu thu thập theo Ứng dụng (BR-09), tính '
         'Hạn đóng tự động, gắn nhu cầu KH (→ Đã lập dự án), bổ sung Loại hình / Lĩnh vực vào hồ sơ KH.\n– Lưu dự án '
         'con đầu tiên → dự án cha chuyển “Đang thực hiện”.\n– “Đã lưu thành công!”, về danh sách.\n' + ERR_TOAST),
        ('Bấm Quay lại / rời màn', 'Click',
         'After:\n– Có thay đổi chưa lưu → hộp “Thông tin chưa lưu”; ngược lại về danh sách.'),
    ], uc=('FR-06', 'Tạo mới dự án', 'crud', A_ALL),
    rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'))

# ------------------------------------------------------------------ 2.7 Thêm nhanh KH
fn(7, 'Thêm nhanh khách hàng', dict(
    ten='Thêm nhanh khách hàng ngay trên form dự án',
    mota='Tạo khách hàng mới trong popup mà không rời form dự án; lưu xong tự chọn khách hàng đó vào khối đang '
         'thao tác (KH trực tiếp hoặc KH thụ hưởng cuối).',
    tacnhan='Nhân viên kinh doanh có quyền “Thêm khách hàng”',
    dieukien='Người dùng đang ở form Tạo mới / Sửa dự án; có quyền “Thêm khách hàng”; ô Khách hàng không bị khoá.',
    chinh='1. Người dùng bấm “+ Thêm nhanh khách hàng” cạnh nhãn Khách hàng.\n'
          '2. Popup “Thêm nhanh khách hàng” mở form khách hàng đầy đủ.\n'
          '3. Nhập Tên khách hàng, Loại hình tổ chức và các thông tin theo loại (cá nhân / tổ chức), địa chỉ, người '
          'liên hệ.\n4. Bấm “Lưu” → “Tạo khách hàng thành công”, popup đóng, khách hàng vừa tạo được chọn vào form.',
    phu='• Thiếu thông tin → lỗi dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.\n'
        '• Lỗi khác → “Tạo khách hàng thất bại”.\n• Bấm “Đóng” → không tạo khách hàng.',
    dacbiet='Form trong popup dùng chung với màn Khách hàng (cùng quy tắc kiểm tra). Mã khách hàng tự sinh khi lưu.'),
    [MENU + ' => Tạo mới => Thêm nhanh khách hàng'], [('07-them-nhanh-kh.png', 'Popup Thêm nhanh khách hàng')],
    [
        ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Thêm nhanh khách hàng', '–'),
        ('Là nhà cung cấp / Là khách hãng', 'Checkbox', 'Enable', '–', 'Không', 'Bỏ tích',
         'Tích “Là khách hãng” thì bắt buộc Hãng xe.'),
        ('Tên khách hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống', 'Placeholder “Nhập tên khách hàng”.'),
        ('Loại hình tổ chức', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Có', 'Trống',
         'Cá nhân / Doanh nghiệp tư nhân / Doanh nghiệp nước ngoài / Tổ chức phi chính phủ / Cơ quan nhà nước; quyết '
         'định hiện khối “Thông tin cá nhân” hay “Thông tin tổ chức”.'),
        ('Loại hình hoạt động / Lĩnh vực kinh doanh khách hàng', 'Dropdown', 'Enable', 'Danh sách, chọn nhiều',
         'Không', 'Trống', '–'),
        ('Nhóm khách hàng / Hãng xe', 'Dropdown', 'Enable', 'Danh sách', 'Hãng xe: có khi là khách hãng', 'Trống',
         '–'),
        ('Khối Thông tin cá nhân / Thông tin tổ chức', 'Label', 'Enable / Ẩn', '–', '–', 'Ẩn',
         'Hiện sau khi chọn Loại hình tổ chức: SĐT, email, MST (bắt buộc khi không có công ty mẹ), Địa chỉ xuất hoá '
         'đơn, Quốc gia / Tỉnh, Thành phố / Phường, Xã (bắt buộc)…'),
        ('Khối Người liên hệ (*)', 'Label', 'Enable / Ẩn', '–', 'Có với tổ chức', 'Ẩn',
         'Họ tên, Chức vụ, Số điện thoại bắt buộc; thêm được nhiều người liên hệ.'),
        ('Nút Lưu / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ],
    [
        ('Bấm + Thêm nhanh khách hàng', 'Click',
         'Before:\n– Không có quyền “Thêm khách hàng” → nút không hiển thị.\nAfter:\n– Mở popup với form trống.'),
        ('Bấm Lưu', 'Click',
         'During:\n– Trường bắt buộc trống → “Bắt buộc phải nhập” dưới ô, thông báo “Bạn chưa nhập đầy đủ thông '
         'tin”.\nAfter:\n– Tạo khách hàng, sinh mã; “Tạo khách hàng thành công”; đóng popup; tìm lại khách hàng theo '
         'mã và chọn vào khối đang thao tác.\n– Lỗi khác → “Tạo khách hàng thất bại”.'),
        ('Bấm Đóng', 'Click', 'After:\n– Đóng popup, không lưu.'),
    ], uc=('FR-07', 'Thêm nhanh khách hàng', 'crud', A_ALL),
    rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'))

# ------------------------------------------------------------------ 2.8 Sửa
fn(8, 'Chỉnh sửa dự án', dict(
    ten='Chỉnh sửa dự án tiền khả thi',
    mota='Sửa thông tin dự án trên cùng form với Tạo mới; một số ô bị khoá theo trạng thái và dữ liệu đã phát sinh.',
    tacnhan='Người tạo dự án; Người có quyền xem theo cấp (V1–V4)',
    dieukien='Người dùng là người tạo dự án, hoặc dự án nằm trong phạm vi quyền xem theo cấp của người dùng '
             '(BR-10). Người chỉ thấy dự án vì là KD hỗ trợ thì không được sửa.',
    chinh='1. Người dùng bấm nút Sửa (bút) ở cột Hành động, hoặc nút “Sửa” ở chân màn chi tiết.\n'
          '2. Hệ thống mở form “Chỉnh sửa dự án tiền khả thi” (dự án cha: “Chỉnh sửa dự án cha”) với dữ liệu hiện '
          'tại.\n3. Người dùng sửa thông tin, bấm “Lưu”.\n4. Hệ thống kiểm tra như Tạo mới, lưu, thông báo “Đã lưu '
          'thành công!” và quay về danh sách.',
    phu='• Dự án đang ở “Đang tạo” → có thêm nút “Lưu nháp”; bấm “Lưu” chuyển sang “Thu thập thông tin dự án” và '
        'sinh mã.\n• Dự án đã qua “Đang tạo” → bấm Lưu giữ nguyên trạng thái hiện tại (không lùi, không tiến).\n'
        '• Mở thẳng đường dẫn sửa khi không được sửa → hệ thống chuyển sang màn chi tiết.\n'
        '• Không tải được dự án → “Không tải được thông tin dự án”.\n'
        '• Dữ liệu vừa bị người khác thay đổi / xoá → “Dữ liệu đã thay đổi, vui lòng tải lại”.',
    dacbiet='Các ô bị khoá khi sửa: Loại dự án / Dự án cha (khi trạng thái khác Đang tạo hoặc đã có dự án con); '
            'Khách hàng (dự án cha đã có con); Cách triển khai (đã có giải pháp / yêu cầu làm GP, hoặc trạng thái '
            'khác Đang tạo / Thu thập thông tin); Có cần làm GP? (trạng thái khác Đang tạo / Thu thập thông tin); '
            'Loại tiền tệ (đã có giá trị); Tổng ngân sách dự kiến của dự án cha (từ Trình duyệt hợp đồng trở đi). '
            'Dự án đã qua Đang tạo được chọn ngày quá khứ.'),
    [MENU + ' => Sửa', DET + ' => Sửa'],
    [('08-sua-nhap.png', 'Form Chỉnh sửa dự án đang ở trạng thái Đang tạo (có nút Lưu nháp)'),
     ('08b-sua-chinh-thuc.png', 'Form Chỉnh sửa dự án đã lưu chính thức (dự án con, các ô kế thừa bị khoá)')],
    [
        ('Tiêu đề màn', 'Label', 'Hiển thị', '–', '–', 'Chỉnh sửa dự án tiền khả thi', 'Dự án cha: “Chỉnh sửa dự án cha”.'),
        ('Các ô của form', '–', 'Enable / Disable', 'Như FR-06', 'Như FR-06', 'Theo dữ liệu',
         'Giống bảng giao diện FR-06; các ô khoá theo “Yêu cầu đặc biệt”.'),
        ('Loại dự án', 'Dropdown', 'Enable / Disable', 'Danh sách 3 giá trị', 'Có', 'Theo dữ liệu',
         'Khoá kèm ghi chú “Chỉ được đổi loại dự án khi dự án còn ở trạng thái "Đang tạo" và chưa có dự án con trực '
         'thuộc.”'),
        ('Cách triển khai dự án', 'Dropdown', 'Enable / Disable', 'Danh sách 3 giá trị', 'Có', 'Theo dữ liệu',
         'Khoá khi đã có giải pháp / yêu cầu làm GP.'),
        ('Hạn đóng tự động (+ ⓘ)', 'Textbox', 'Disable / Ẩn', 'dd/mm/yyyy', '–', 'Theo dữ liệu',
         'Hiện khi dự án có hạn: “dd/mm/yyyy (đã gia hạn N ngày)”; ⓘ “Quá ngày này mà dự án chưa chuyển sang hợp '
         'đồng thì hệ thống tự đóng. Muốn lùi mốc này thì gửi đề xuất Gia hạn.”'),
        ('File xác nhận chốt giải pháp', 'Table/Grid', 'Read-only / Ẩn', '–', '–', 'Ẩn',
         'Khối 5. Giải pháp, chỉ hiện khi dự án đã Chốt giải pháp.'),
        ('Nút Lưu nháp', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi đã qua Đang tạo', '–'),
        ('Nút Lưu / Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Quay lại về danh sách.'),
    ],
    [
        ('Mở màn Sửa', 'System',
         'Before:\n– Không được sửa (BR-10) → chuyển sang màn chi tiết.\nAfter:\n– Nạp dữ liệu, khoá các ô theo '
         'trạng thái; giữ đúng giá trị danh mục đã bị khoá (hiện 🔒).'),
        ('Bấm Lưu nháp / Lưu', 'Click',
         'Before:\n– Không được sửa → “Bạn không có quyền thực hiện chức năng này”, dừng.\n– KH có nhu cầu chưa chọn '
         '→ hộp “Chưa chọn nhu cầu khách hàng”.\nDuring:\n– Kiểm tra như FR-06.\n– Đổi loại dự án sai điều kiện → '
         '“Chỉ được đổi loại dự án khi dự án còn ở trạng thái "Đang tạo" và chưa có dự án con trực thuộc.”\n– Đổi '
         'Cách triển khai khi đã có GP → “Không thể đổi cách triển khai khi dự án đã có giải pháp hoặc yêu cầu làm '
         'GP.”\n– Đổi tổng ngân sách dự án cha đã sang hợp đồng → “Dự án đã sang bước hợp đồng nên không đổi được '
         'tổng ngân sách dự kiến.”\n– Ứng dụng / Giai đoạn bị khoá → “Ứng dụng đã ngừng hoạt động, vui lòng chọn ứng '
         'dụng khác.” / “Giai đoạn dự án đã ngừng hoạt động, vui lòng chọn giai đoạn khác.”\nAfter:\n– Lưu; đổi Ứng '
         'dụng thì tạo phiếu thu thập mới (BR-09); tính lại Hạn đóng tự động.\n– “Đã lưu thành công!”, về danh sách.\n'
         '– Lỗi nhập liệu có ô đỏ → “Bạn chưa nhập đầy đủ thông tin”; không có ô đỏ → “Dữ liệu đã thay đổi, vui lòng '
         'tải lại”.'),
    ], uc=('FR-08', 'Chỉnh sửa dự án', 'crud', A_ALL),
    rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'))

# ------------------------------------------------------------------ 2.9 Xóa
fn(9, 'Xóa dự án', dict(
    ten='Xóa dự án',
    mota='Xoá hẳn một dự án nháp chưa có dự án con.',
    tacnhan='Người tạo dự án',
    dieukien='Người dùng là người tạo; dự án ở trạng thái “Đang tạo” và chưa có dự án con.',
    chinh='1. Người dùng bấm nút Xóa (thùng rác) ở cột Hành động hoặc nút “Xóa” ở chân màn chi tiết.\n'
          '2. Hệ thống hiện hộp xác nhận “Xác nhận xóa”.\n3. Người dùng bấm “Xóa”.\n'
          '4. Hệ thống xoá dự án cùng phòng/KD hỗ trợ và liên kết meeting, thông báo “Xóa dự án thành công”, nạp lại '
          'danh sách (từ màn chi tiết thì quay về danh sách).',
    phu='• Bấm “Hủy” → đóng hộp, không xoá.\n• Lỗi → thông báo lỗi hoặc “Lỗi khi xóa dự án”.'),
    [MENU + ' => Xóa', DET + ' => Xóa'], [('09-xoa.png', 'Hộp xác nhận xóa dự án')],
    [
        ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận xóa', '–'),
        ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
         '“Bạn có chắc muốn xóa dự án \'{Tên dự án}\'?” (không có tên: “Bạn có chắc muốn xóa dự án này?”).'),
        ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Màu đỏ.'),
        ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '–'),
    ],
    [
        ('Bấm nút Xóa ở dòng / chân màn', 'Click',
         'Before:\n– Nút chỉ hiện khi đủ điều kiện (BR-10).\nAfter:\n– Mở hộp xác nhận.'),
        ('Bấm Xóa trong hộp', 'Click',
         'After:\n– Xoá dự án, phòng / KD hỗ trợ, liên kết meeting.\n– “Xóa dự án thành công”; nạp lại danh sách '
         'hoặc về danh sách.\n– Lỗi → “Lỗi khi xóa dự án”.'),
        ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp.'),
    ], uc=('FR-09', 'Xóa dự án', 'action', A_ALL), ui_mode='confirm',
    rule=('- Thông báo, Quy tắc Xóa.', 'delete'))

# ------------------------------------------------------------------ 2.10 Tạo GP / YCGP
fn(10, 'Tạo giải pháp / Tạo yêu cầu làm giải pháp', dict(
    ten='Lối tắt Tạo giải pháp / Tạo yêu cầu làm giải pháp từ dự án',
    mota='Từ dòng dự án (hoặc chân màn chi tiết) chuyển sang màn tạo Giải pháp hoặc tạo Yêu cầu làm giải pháp với '
         'dự án đã được chọn sẵn.',
    tacnhan='Nhân viên kinh doanh; Người tạo dự án',
    dieukien='Tạo giải pháp: dự án Tự triển khai, đang “Thu thập thông tin dự án”, có cần làm GP = Có, chưa có giải '
             'pháp, phiếu thu thập đã nhập đủ câu bắt buộc. Tạo yêu cầu làm giải pháp: dự án không Tự triển khai, '
             'không phải dự án cha, người dùng là người tạo dự án, dự án chưa có yêu cầu làm giải pháp.',
    chinh='1. Người dùng mở menu “⋮” ở cột Hành động (hoặc chân màn chi tiết).\n'
          '2. Bấm “Tạo giải pháp” hoặc “Tạo yêu cầu làm giải pháp”.\n'
          '3. Hệ thống chuyển sang màn tạo tương ứng, dự án đã được chọn sẵn.',
    phu='• Không đủ điều kiện → nút không hiển thị.\n• Chuột phải vào nút mở được tab mới.'),
    [MENU + ' => Tạo giải pháp', MENU + ' => Tạo yêu cầu làm giải pháp'],
    [('10-tao-giai-phap-icon.png', 'Cột Hành động: nút Tạo giải pháp (dòng dự án con) và Tạo yêu cầu làm giải pháp')],
    [
        ('Nút Tạo giải pháp', 'Icon Button', 'Enable / Ẩn', 'Ẩn khi không đủ điều kiện',
         'Chuyển sang màn Tạo giải pháp, chọn sẵn dự án.'),
        ('Nút Tạo yêu cầu làm giải pháp', 'Icon Button', 'Enable / Ẩn', 'Ẩn khi không đủ điều kiện',
         'Chuyển sang màn Tạo yêu cầu làm giải pháp, chọn sẵn dự án.'),
    ],
    [
        ('Bấm Tạo giải pháp', 'Click', 'After:\n– Mở màn Tạo giải pháp của dự án (đặc tả ở SRS Giải pháp).'),
        ('Bấm Tạo yêu cầu làm giải pháp', 'Click',
         'After:\n– Mở màn Tạo yêu cầu làm giải pháp của dự án (đặc tả ở SRS Yêu cầu giải pháp). Gửi yêu cầu khi '
         'phiếu thu thập chưa đủ → hệ thống chặn “Phiếu thu thập thông tin chưa đủ các trường yêu cầu”.'),
    ], ui_mode='confirm')

# ------------------------------------------------------------------ 2.11 Xem chi tiết
fn(11, 'Xem chi tiết dự án', dict(
    ten='Xem chi tiết dự án (màn quản lý nhiều tab)',
    mota='Màn chi tiết gồm thanh tab theo loại dự án, tab đầu “Dự án” (dự án cha: “Thông tin chung”) hiển thị '
         'toàn bộ thông tin dự án ở chế độ chỉ đọc, và chân màn có các nút thao tác.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng thấy dự án trong danh sách.',
    chinh='1. Người dùng bấm Mã dự án ở màn danh sách.\n2. Tiêu đề màn là tên dự án kèm badge Tiến trình nội bộ.\n'
          '3. Hệ thống hiện thanh tab theo loại dự án và mở tab “Dự án” với các khối 1 → 7 chỉ đọc.\n'
          '4. Chân màn hiện các nút người dùng được phép: Sửa, Xóa, Chốt giải pháp, Gia hạn, Đóng dự án, Quay lại.',
    phu='• Dự án thường: tab Dự án, Yêu cầu, Giải pháp, Nhiệm vụ, Vấn đề giải pháp, Meetings, Files, Hồ sơ, Báo giá, '
        'Gia hạn, Thu thập thông tin.\n'
        '• Dự án Tự triển khai và không làm GP: chỉ tab Dự án, Nhiệm vụ, Meetings, Báo giá, Gia hạn, Thu thập thông '
        'tin.\n• Dự án cha: tab Thông tin chung, Dự án con, Báo giá, Meetings.\n'
        '• Dự án đã đóng: banner đỏ “Dự án đã đóng” (Lý do, Ghi chú, “Đóng ngày … bởi …”) và ẩn mọi nút ở chân màn '
        'trừ Quay lại.\n• Trong lúc nạp dữ liệu hiện khung chờ (skeleton).'),
    [DET],
    [('m151-tkt.png', 'Màn chi tiết dự án thường – tab Dự án'),
     ('m157-tkt.png', 'Màn chi tiết dự án cha – tab Thông tin chung'),
     ('m154-tkt.png', 'Dự án Tự triển khai không làm giải pháp – thanh tab rút gọn')],
    [
        ('Tiêu đề màn', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', 'Tên dự án + badge Tiến trình nội bộ (màu theo BR-04).'),
        ('Banner “Dự án đã đóng”', 'Toast / Alert', 'Hiển thị / Ẩn', '–', 'Ẩn',
         'Chỉ khi dự án Đóng/Không thực hiện: “Lý do:”, “Ghi chú:” (nếu có), “Đóng ngày … bởi …”.'),
        ('Thanh tab', 'Button', 'Enable', 'Danh sách tab theo loại dự án', 'Tab Dự án',
         'Tab đang mở biến mất (dự án đổi loại) → tự về tab đầu.'),
        ('Khối 1. Thông tin khách hàng', 'Text', 'Read-only', '–', 'Theo dữ liệu',
         'KH trực tiếp (+ KH thụ hưởng cuối nếu KH TMDV): thông tin KH, Đối tượng tổ chức, Loại hình, Lĩnh vực, '
         'Email, Người liên hệ, Nhu cầu khách hàng.'),
        ('Khối 2. Thông tin dự án', 'Text', 'Read-only', '–', 'Theo dữ liệu',
         'Tên, Loại dự án, Dự án cha, Ứng dụng (+ icon mẫu phiếu, nút Xem giải pháp vẫn bấm được), Nhóm ngành, Quy '
         'mô, Phân loại đầu tư, Cách triển khai, Địa điểm, Mô tả.'),
        ('Khối 3. Timeline', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
         'Giai đoạn, Mức độ ưu tiên, Ngày bắt đầu / kết thúc, Hạn đóng tự động (nếu có), Ngày KH cần nhận GP, Ngày '
         'chốt GP nội bộ, Tổng số ngày thực hiện.'),
        ('Khối 4 → 7', 'Text', 'Read-only', '–', 'Theo dữ liệu',
         'Phụ trách KD nội bộ, Phòng KD hỗ trợ & KD hỗ trợ, Giải pháp (Có cần làm GP?, File xác nhận chốt giải '
         'pháp), Liên kết dữ liệu (meeting), Nguồn vốn & kỳ vọng tài chính.'),
        ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không được sửa', 'FR-08.'),
        ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không được xoá', 'FR-09.'),
        ('Nút Chốt giải pháp / Gia hạn / Đóng dự án', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
         'FR-29, FR-30, FR-31.'),
        ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn trước.'),
    ],
    [
        ('Mở màn chi tiết', 'System',
         'After:\n– Nạp dự án, yêu cầu làm GP, giải pháp (nếu có), danh sách hồ sơ chốt được; dựng thanh tab theo '
         'loại dự án.\n– Lỗi tải tham chiếu → “Không thể tải dữ liệu tham chiếu” / “Không thể tải danh sách dự án '
         'tiền khả thi”.'),
        ('Bấm một tab', 'Click', 'After:\n– Hiện nội dung tab (FR-12 → FR-28); tab Meetings nạp lại danh sách khi mở.'),
        ('Bấm nút ở chân màn', 'Click', 'After:\n– Mở chức năng tương ứng; dự án đã đóng thì các nút này bị ẩn.'),
    ], ui_mode='read', rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'))

# ------------------------------------------------------------------ 2.12 Tab Yêu cầu
fn(12, 'Tab Yêu cầu', dict(
    ten='Xem yêu cầu làm giải pháp của dự án',
    mota='Hiển thị chỉ đọc phiếu yêu cầu làm giải pháp gắn với dự án.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn chi tiết dự án thường (không phải Tự triển khai không làm GP).',
    chinh='1. Người dùng bấm tab “Yêu cầu”.\n2. Hệ thống hiện thông tin yêu cầu và khối Phụ trách KD nội bộ.',
    phu='• Dự án chưa có yêu cầu → “Dự án chưa có yêu cầu giải pháp tương ứng”.\n'
        '• Lỗi tải → “Không thể tải dữ liệu yêu cầu”.\n• Tab không có nút thao tác.'),
    [DET + ' => Tab Yêu cầu'], [('m153-yeucau.png', 'Tab Yêu cầu của dự án đã gửi yêu cầu làm giải pháp')],
    [
        ('Mã yêu cầu + Trạng thái', 'Badge', 'Read-only', '–', 'Theo dữ liệu', 'Màu trạng thái theo yêu cầu.'),
        ('Tên yêu cầu, Phòng tiếp nhận yêu cầu, Ứng dụng, Nhóm ngành, Nhóm giải pháp, Giai đoạn dự án', 'Text',
         'Read-only', '–', 'Theo dữ liệu', '–'),
        ('Ngày KH cần giải pháp, Ngày KH cần báo giá, Ngày cần nhận GP nội bộ, Hạn hoàn thành tiếp nhận', 'Text',
         'Read-only', 'dd/mm/yyyy (hạn: dd/mm/yyyy hh:mm)', 'Theo dữ liệu', 'Hạn hoàn thành chỉ hiện khi có.'),
        ('Mô tả / ghi chú yêu cầu, Lý do từ chối, Lý do hủy', 'Text', 'Read-only', '–', 'Theo dữ liệu',
         'Lý do chỉ hiện khi có.'),
        ('Bảng File gửi kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         'STT / Tên tài liệu / File đính kèm / Dung lượng; nút Xem trước (file xem được) và Tải xuống.'),
        ('Khối Phụ trách KD nội bộ', 'Text', 'Read-only', '–', 'Theo dữ liệu',
         'Phòng KD phụ trách chính, KD phụ trách chính (Họ tên, SĐT, Email), Phòng hỗ trợ #n + danh sách người.'),
        ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Dự án chưa có yêu cầu giải pháp tương ứng”.'),
    ],
    [('Bấm tab Yêu cầu', 'Click', 'After:\n– Hiện yêu cầu chỉ đọc hoặc trạng thái rỗng.'),
     ('Bấm Xem trước / Tải xuống file', 'Click', 'After:\n– Xem trước trong trình duyệt / tải file về máy.')],
    ui_mode='read', rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'))

# ------------------------------------------------------------------ 2.13 Tab Giải pháp
fn(13, 'Tab Giải pháp – Thông tin giải pháp', dict(
    ten='Xem thông tin giải pháp của dự án',
    mota='Tab con “Thông tin giải pháp” hiển thị giải pháp gắn với dự án và đội nhân sự làm giải pháp (chỉ đọc).',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn chi tiết dự án thường có tab Giải pháp.',
    chinh='1. Người dùng bấm tab “Giải pháp” (mở sẵn tab con “Thông tin giải pháp”).\n'
          '2. Hệ thống hiện khối Thông tin giải pháp và khối Quản lý nhân sự.',
    phu='• Chưa có giải pháp → “Dự án chưa có giải pháp tương ứng”.\n'
        '• Chưa có nhân sự → “Chưa có nhân sự nào trong dự án”; sơ đồ: “Chưa có dữ liệu nhân sự. Hãy thêm nhân sự '
        'trong các hạng mục.” / “Chưa có dữ liệu sơ đồ. Hãy chọn Leader và phân công nhân sự.”\n'
        '• Không có nút thao tác (Phân công / Thêm nhân sự bị ẩn).'),
    [DET + ' => Tab Giải pháp'], [('m151-02.png', 'Tab Giải pháp – Thông tin giải pháp')],
    [
        ('Khối Thông tin giải pháp', 'Text', 'Read-only', '–', 'Theo dữ liệu',
         'Mã giải pháp, Tên giải pháp, Trạng thái (badge), Version hiện tại, PM làm giải pháp, Phòng tiếp nhận; '
         'trống hiện “—”.'),
        ('Bảng Quản lý nhân sự', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         'STT, Thành viên (tên + email), Hạng mục, Vai trò, Ngày bắt đầu, Ngày kết thúc, Nhiệm vụ đang phụ trách, '
         'Trạng thái.'),
        ('Sơ đồ cấu trúc nhân sự', 'Text', 'Read-only', '–', 'Theo dữ liệu', 'Badge “PM: …”, “Hạng mục: n”, “Nhân sự: n”.'),
        ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Dự án chưa có giải pháp tương ứng”.'),
    ],
    [('Bấm tab Giải pháp', 'Click', 'After:\n– Hiện tab con Thông tin giải pháp.')],
    ui_mode='read', rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'))

# ------------------------------------------------------------------ 2.14 YC điều chỉnh GP
fn(14, 'Yêu cầu điều chỉnh giải pháp', dict(
    ten='Tạo và xử lý yêu cầu điều chỉnh giải pháp',
    mota='Tab con “Yêu cầu điều chỉnh GP” của tab Giải pháp: NV KD phụ trách gửi yêu cầu điều chỉnh giải pháp đã '
         'duyệt; PM giải pháp / quản lý phòng tiếp nhận tiếp nhận hoặc từ chối.',
    tacnhan='NV KD phụ trách dự án; PM giải pháp / Quản lý phòng tiếp nhận',
    dieukien='Dự án đã có giải pháp. Tạo yêu cầu: người dùng là NV KD phụ trách và giải pháp ở trạng thái Đã duyệt '
             'giải pháp / Đã duyệt giá / Chờ làm giá / Chốt giải pháp.',
    chinh='1. Người dùng mở tab Giải pháp → tab con “Yêu cầu điều chỉnh GP”.\n'
          '2. NV KD phụ trách bấm “Tạo yêu cầu”, nhập Nội dung điều chỉnh, đính kèm file, bấm “Gửi”.\n'
          '3. Hệ thống sinh mã YCDCGP.NNNNN, trạng thái “Đã gửi”, gửi thông báo cho PM giải pháp và quản lý phòng '
          'tiếp nhận; thông báo “Gửi yêu cầu điều chỉnh thành công”.\n'
          '4. PM / quản lý phòng tiếp nhận mở yêu cầu, bấm “Tiếp nhận” (xác nhận) hoặc “Từ chối” (nhập lý do).',
    phu='• Chưa có giải pháp → “Dự án chưa có giải pháp tương ứng”.\n'
        '• Bảng rỗng → “Chưa có yêu cầu điều chỉnh giải pháp nào.”\n'
        '• Lỗi tải → “Không thể tải danh sách yêu cầu điều chỉnh”.\n'
        '• Người xem là NV KD phụ trách → không có cột Hành động (chỉ bấm mã để xem).'),
    [DET + ' => Tab Giải pháp => Yêu cầu điều chỉnh GP', DET + ' => Tab Giải pháp => Yêu cầu điều chỉnh GP => Tạo yêu cầu'],
    [('14-yc-dieu-chinh.png', 'Tab con Yêu cầu điều chỉnh GP'),
     ('14b-tao-yc-dieu-chinh.png', 'Popup Tạo yêu cầu điều chỉnh giải pháp')],
    [
        ('Nút Tạo yêu cầu', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', 'Mở popup tạo yêu cầu.'),
        ('Bảng “Yêu cầu điều chỉnh giải pháp”', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
         'STT / Mã yêu cầu (liên kết mở popup chi tiết) / Version / Người yêu cầu / Ngày gửi (dd/mm/yyyy) / Trạng '
         'thái (Đã gửi – xanh dương, Tiếp nhận – xanh lá, Từ chối – đỏ) / Hành động.'),
        ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn với NV KD phụ trách',
         'Xem chi tiết; Tiếp nhận và Từ chối chỉ khi yêu cầu “Đã gửi” và người xem là PM giải pháp hoặc quản lý '
         'phòng tiếp nhận.'),
        ('Popup Tạo – Giải pháp', 'Textbox', 'Disable', '–', '–', '“Mã - Tên (Vversion)”', '–'),
        ('Popup Tạo – Nội dung điều chỉnh', 'Textarea', 'Enable', '–', 'Có', 'Trống',
         'Placeholder “Nhập nội dung cần điều chỉnh...”; trống → “Nội dung điều chỉnh không được để trống”.'),
        ('Popup Tạo – File đính kèm', 'Table/Grid', 'Enable', '–', 'Không', 'Trống', '–'),
        ('Popup Tạo – Nút Gửi / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
        ('Popup Chi tiết', 'Modal', 'Read-only', '–', '–', 'Ẩn',
         'Mã yêu cầu, Giải pháp, Người yêu cầu, Ngày gửi, Trạng thái, Nội dung điều chỉnh, Người tiếp nhận / Người '
         'từ chối (tên — ngày), Lý do từ chối, File đính kèm; nút Tiếp nhận / Từ chối (theo điều kiện) / Đóng.'),
        ('Hộp xác nhận Tiếp nhận', 'Modal', 'Enable', '–', '–', 'Ẩn',
         'Tiêu đề “Phê duyệt yêu cầu điều chỉnh”, nội dung “Bạn có chắc muốn tiếp nhận yêu cầu điều chỉnh này?”.'),
        ('Popup Từ chối – Lý do từ chối', 'Textarea', 'Enable', '–', 'Có', 'Trống',
         'Placeholder “Nhập lý do từ chối...”; trống → “Lý do từ chối không được để trống”. Nút Gửi / Đóng.'),
    ],
    [
        ('Bấm Gửi (popup Tạo)', 'Click',
         'Before:\n– Chỉ NV KD phụ trách thấy nút Tạo yêu cầu.\nDuring:\n– Nội dung trống → “Nội dung điều chỉnh '
         'không được để trống”.\n– Máy chủ chặn: “Giải pháp không thuộc dự án này.” / “Giải pháp chưa được duyệt, '
         'không thể tạo yêu cầu điều chỉnh.” / “Chỉ nhân viên KD phụ trách dự án mới được tạo yêu cầu điều chỉnh.”\n'
         'After:\n– Tạo yêu cầu “Đã gửi”, mã YCDCGP.NNNNN.\n– Thông báo cho PM giải pháp + quản lý phòng tiếp nhận: '
         '“Yêu cầu điều chỉnh giải pháp mới” – “Có yêu cầu điều chỉnh giải pháp: {mã} - GP: {mã GP} - {tên GP}”.\n'
         '– “Gửi yêu cầu điều chỉnh thành công”; lỗi → “Có lỗi xảy ra, vui lòng thử lại”.'),
        ('Bấm Tiếp nhận → xác nhận', 'Click',
         'After:\n– Yêu cầu chuyển “Tiếp nhận”.\n– Mọi yêu cầu xây dựng giá của dự án đang Chờ / Đang XD giá chuyển '
         '“Dừng”; báo giá liên quan đang Đang tạo / Chờ TP duyệt / Chờ BGĐ duyệt chuyển “Dừng”, người lập nhận thông '
         'báo “Báo giá tạm dừng” – “Báo giá {mã} tạm dừng do có yêu cầu điều chỉnh giải pháp mới ({mã YC})”.\n'
         '– “Đã tiếp nhận yêu cầu điều chỉnh”.'),
        ('Bấm Từ chối → Gửi', 'Click',
         'During:\n– Lý do trống → “Lý do từ chối không được để trống”.\nAfter:\n– Yêu cầu chuyển “Từ chối”, lưu lý '
         'do; “Đã từ chối yêu cầu điều chỉnh”.'),
    ], uc=('FR-14', 'Yêu cầu điều chỉnh giải pháp', 'action', A_KD),
    rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'))

# ------------------------------------------------------------------ 2.15 Nhiệm vụ
fn(15, 'Tab Nhiệm vụ', dict(
    ten='Danh sách nhiệm vụ của dự án',
    mota='Hiển thị các nhiệm vụ gắn với dự án (kể cả nhiệm vụ của giải pháp thuộc dự án, phân biệt bằng cột Giải '
         'pháp) và cho tạo nhiệm vụ mới gắn sẵn dự án.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn chi tiết dự án thường.',
    chinh='1. Người dùng bấm tab “Nhiệm vụ”.\n2. Hệ thống hiện bộ lọc và bảng “Danh sách nhiệm vụ” (theo phạm vi '
          'xem nhiệm vụ của người dùng).\n3. Bấm “Tạo mới” → popup “Thêm mới nhiệm vụ” với Dự án/Nhóm khoá sẵn dự án '
          'hiện tại.\n4. Các thao tác trên dòng (Sửa, Xóa, Nhập kết quả, Duyệt, Lịch sử) theo quy tắc của màn Nhiệm vụ.',
    phu='• Dự án đã đóng → không có nút Tạo mới.\n• Rỗng → “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Chi tiết từng thao tác nhiệm vụ: xem SRS Nhiệm vụ.'),
    [DET + ' => Tab Nhiệm vụ'], [('m151-03.png', 'Tab Nhiệm vụ của dự án')],
    [
        ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Theo dữ liệu', 'Placeholder “Tìm theo mã, tên nhiệm vụ, tên, mã khách hàng”.'),
        ('Bộ lọc nâng cao', 'Dropdown', 'Enable', 'Danh sách', 'Trống',
         'Loại nhiệm vụ, Trạng thái, Mức độ ưu tiên, Người thực hiện, Người giao, Người duyệt kết quả, Hạn hoàn thành '
         '(khoảng ngày); chọn là lọc ngay.'),
        ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi dự án đã đóng', 'Mở popup Thêm mới nhiệm vụ.'),
        ('Ô Quá hạn', 'Badge', 'Hiển thị', '≥ 0', 'Theo dữ liệu', '“Quá hạn: n”.'),
        ('Bảng “Danh sách nhiệm vụ”', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         'STT / Mã nhiệm vụ (bấm mở popup xem) / Tên nhiệm vụ / Loại nhiệm vụ / Giải pháp / Người thực hiện / Hạn hoàn '
         'thành / Ưu tiên / Người tạo / Ngày tạo / Trạng thái / Hành động.'),
        ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo vai trò',
         'Sửa, Xóa (hộp “Xác nhận xoá”), Nhập kết quả, Duyệt, Lịch sử — theo quyền trên từng nhiệm vụ.'),
        ('Phân trang', 'Pagination', 'Enable', '10 / 20 / 50 / 100', '10 dòng/trang', '–'),
    ],
    [
        ('Bấm tab Nhiệm vụ', 'System', 'After:\n– Nạp nhiệm vụ của dự án trong phạm vi xem nhiệm vụ của người dùng.'),
        ('Bấm Tạo mới', 'Click', 'After:\n– Mở popup “Thêm mới nhiệm vụ”, Dự án/Nhóm = dự án hiện tại (khoá).'),
        ('Bấm Xóa → Xóa', 'Click', 'After:\n– “Xóa nhiệm vụ thành công”; lỗi → “Lỗi khi xóa nhiệm vụ”.'),
    ], ui_mode='read', rule=('- Màn Danh sách, Phân trang và UI/UX.', 'list'))

# ------------------------------------------------------------------ 2.16 Vấn đề
fn(16, 'Tab Vấn đề giải pháp', dict(
    ten='Danh sách vấn đề của giải pháp thuộc dự án',
    mota='Hiển thị các vấn đề (issue) phát sinh trên giải pháp của dự án; tạo, sửa, xử lý, xuất Excel.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn chi tiết dự án thường đã có giải pháp.',
    chinh='1. Người dùng bấm tab “Vấn đề giải pháp”.\n2. Hệ thống hiện bộ lọc và bảng “Danh sách Vấn đề”.\n'
          '3. Người dùng lọc, bấm Tạo mới / Sửa / Xử lý / Xem / Lịch sử / Xóa theo quyền trên từng vấn đề.',
    phu='• Chưa có giải pháp → “Dự án chưa có giải pháp tương ứng”.\n'
        '• Rỗng → “Không có Vấn đề nào phù hợp bộ lọc.”\n'
        '• Nút “Tạo mới” chỉ hiện khi giải pháp đang Chờ Leader duyệt / Đang triển khai / Chờ duyệt giải pháp / Đã '
        'duyệt giải pháp / Chờ làm giá / Đã duyệt giá.'),
    [DET + ' => Tab Vấn đề giải pháp'], [('m151-04.png', 'Tab Vấn đề giải pháp')],
    [
        ('Ô tìm nhanh + Bộ lọc', 'Textbox', 'Enable', '–', 'Trống',
         '“Tìm theo mã, tên vấn đề”; lọc Hạng mục/Module, Người xử lý, Người tạo, Người duyệt, Trạng thái, Mức độ ưu '
         'tiên, Ngày tạo, Version giải pháp.'),
        ('Ô Quá hạn + 3 nút lọc nhanh', 'Icon Button', 'Enable', '–', 'Không bật',
         '“Vấn đề tôi làm” / “Vấn đề tôi báo cáo” / “Vấn đề tôi theo dõi”.'),
        ('Nút Tạo mới / Xuất Excel / Tùy chỉnh cột', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
         'Xuất Excel tải file danh_sach_van_de.'),
        ('Bảng “Danh sách Vấn đề”', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         'STT / Mã-Tên Vấn đề (Cập nhật, Bởi, Trong hạn / Quá hạn) / Dự án / Module / Version giải pháp / Người xử lý '
         '/ Ưu tiên / Trạng thái.'),
        ('Hành động trên dòng', 'Icon Button', 'Enable / Ẩn', '–', 'Theo quyền',
         'Xem, Sửa, Lịch sử, Xử lý, Xóa (“Bạn có chắc muốn xoá issue "{tên}" không?”).'),
    ],
    [
        ('Bấm Tạo mới', 'Click', 'After:\n– Mở popup “Thêm mới Vấn đề”, Giải pháp và Dự án chọn sẵn; lưu → “Lưu Vấn '
         'đề thành công” (đặc tả ở SRS Vấn đề).'),
        ('Bấm Xuất Excel', 'Click', 'After:\n– Tải file; “Xuất Excel thành công” / “Lỗi khi xuất Excel”.'),
        ('Bấm Xóa → Xóa', 'Click', 'After:\n– “Xóa Vấn đề thành công” / “Lỗi khi xóa Vấn đề”.'),
    ], ui_mode='read', rule=('- Màn Danh sách, Phân trang và UI/UX.', 'list'))

# ------------------------------------------------------------------ 2.17 Meetings
fn(17, 'Tab Meetings', dict(
    ten='Danh sách meeting của dự án',
    mota='Hiển thị các cuộc họp gắn với dự án và lối tạo meeting mới cho dự án.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn chi tiết dự án (cả dự án cha).',
    chinh='1. Người dùng bấm tab “Meetings”.\n2. Hệ thống nạp bảng “Danh sách Meetings”, 5 dòng/trang.\n'
          '3. Gõ mã / tên meeting vào ô “Tìm nhanh Meeting” rồi Enter để lọc.\n'
          '4. Bấm “Tạo mới” → chuyển sang màn tạo meeting, chọn sẵn dự án.',
    phu='• Rỗng → “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Nút “Tạo mới” chỉ hiện khi dự án không ở Đang tạo / Đóng và người dùng là người tạo dự án, PM giải pháp '
        'hoặc KD hỗ trợ.'),
    [DET + ' => Tab Meetings'], [('m151-05.png', 'Tab Meetings')],
    [
        ('Ô Tìm nhanh Meeting', 'Textbox', 'Enable', '–', 'Trống', 'Placeholder “Nhập mã / tên meeting...”; Enter để tìm.'),
        ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', 'Mở màn tạo meeting của dự án.'),
        ('Bảng “Danh sách Meetings”', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         'STT / Mã / Tên Meeting (mở chi tiết meeting ở tab mới; Người tạo, Ngày tạo, Cập nhật) / Thời gian / Thời '
         'lượng họp (n phút) / Loại & Hình thức (Trực tiếp / Online) / Khách hàng (+ người liên hệ) / Thành phần tham '
         'dự (Phía Công ty, Phía KH) / Trạng thái (Lưu nháp, Lên lịch hẹn, Đã chốt lịch, Đã hoàn thành, Huỷ) / Biên '
         'bản (“Chưa lập biên bản” hoặc liên kết “Biên bản cuộc họp_({mã})”).'),
        ('Phân trang', 'Pagination', 'Enable', '–', '5 dòng/trang', '–'),
    ],
    [
        ('Bấm tab Meetings', 'Click', 'After:\n– Nạp lại danh sách meeting của dự án.'),
        ('Enter ở ô tìm', 'Keypress', 'After:\n– Lọc theo mã / tên meeting.'),
        ('Bấm Tạo mới', 'Click', 'After:\n– Chuyển sang màn Tạo meeting với dự án chọn sẵn (đặc tả ở SRS Meeting).'),
        ('Bấm mã meeting / biên bản', 'Click', 'After:\n– Mở chi tiết meeting / tab biên bản ở tab trình duyệt mới.'),
    ], ui_mode='read', rule=('- Màn Danh sách, Phân trang và UI/UX.', 'list'))

# ------------------------------------------------------------------ 2.18 Files
fn(18, 'Tab Files', dict(
    ten='Tổng hợp file của giải pháp thuộc dự án',
    mota='Liệt kê (chỉ xem) mọi file phát sinh từ nhiệm vụ, vấn đề và hồ sơ trình duyệt của giải pháp.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn chi tiết dự án thường đã có giải pháp.',
    chinh='1. Người dùng bấm tab “Files”.\n2. Hệ thống hiện bộ lọc và bảng “Danh sách Files”.\n'
          '3. Người dùng xem trước hoặc tải file.',
    phu='• Chưa có giải pháp → “Dự án chưa có giải pháp tương ứng”.\n• Rỗng → “Không có file phù hợp bộ lọc.”\n'
        '• File chưa có đường dẫn → “File chưa có đường dẫn tải xuống”.'),
    [DET + ' => Tab Files'], [('m151-06.png', 'Tab Files')],
    [
        ('Ô tìm nhanh + Bộ lọc', 'Textbox', 'Enable', '–', 'Trống',
         '“Tìm theo tên file, tên tài liệu, mã liên kết”; lọc Nguồn (Nhiệm vụ / Vấn đề / HSTD giải pháp / HSTD hạng '
         'mục), Nhóm tài liệu, Hạng mục, Version, Người tạo.'),
        ('Bảng “Danh sách Files”', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         'STT / Tên tài liệu / File / Nguồn (badge) / Nhóm tài liệu / Hạng mục / Version / Liên kết (mở chi tiết nhiệm '
         'vụ / vấn đề) / Người tạo / Ngày tạo / Dung lượng / Thao tác (Xem trước, Tải xuống).'),
    ],
    [('Bấm Xem trước / Tải xuống', 'Click', 'After:\n– Xem file trong trình duyệt / mở file ở tab mới.'),
     ('Bấm Liên kết', 'Click', 'After:\n– Mở popup chi tiết nhiệm vụ hoặc chi tiết vấn đề (chỉ xem).')],
    ui_mode='read', rule=('- Màn Danh sách, Phân trang và UI/UX.', 'list'))

# ------------------------------------------------------------------ 2.19 Hồ sơ
fn(19, 'Tab Hồ sơ', dict(
    ten='Hồ sơ trình duyệt giải pháp đã duyệt',
    mota='Liệt kê hồ sơ trình duyệt giải pháp ở trạng thái Đã duyệt / Hết hiệu lực / Đã chốt; từ hồ sơ gửi yêu cầu '
         'xây dựng giá (dự án không tự triển khai) hoặc tạo báo giá từ BOM (dự án tự triển khai).',
    tacnhan='Người dùng đã đăng nhập; NV KD phụ trách dự án',
    dieukien='Đang ở màn chi tiết dự án thường đã có giải pháp.',
    chinh='1. Người dùng bấm tab “Hồ sơ”.\n2. Hệ thống hiện bảng “Danh sách hồ sơ trình duyệt đã duyệt”.\n'
          '3. Bấm “Xem chi tiết hồ sơ” → popup “Xem hồ sơ trình duyệt {mã}” (chỉ đọc, nút Đóng).\n'
          '4. NV KD phụ trách, với hồ sơ Đã duyệt: bấm “Yêu cầu xây dựng giá” (dự án không tự triển khai) hoặc “Tạo '
          'báo giá” (dự án tự triển khai, hồ sơ có BOM).\n'
          '5. Mở rộng cột “Yêu cầu XD Giá” để xem các yêu cầu xây dựng giá của hồ sơ.',
    phu='• Chưa có giải pháp → “Dự án chưa có giải pháp tương ứng”.\n'
        '• Tạo báo giá thành công → “Đã tạo báo giá”, chuyển sang màn sửa báo giá; lỗi → “Hồ sơ chưa có BOM” / '
        '“Không thể tạo báo giá”.\n'
        '• Yêu cầu xây dựng giá rỗng → “Chưa có yêu cầu xây dựng giá nào.”\n'
        '• Xoá yêu cầu xây dựng giá nháp (người tạo) → hộp “Xác nhận xoá” – “Bạn có chắc muốn xoá yêu cầu xây dựng '
        'giá \'{mã}\'?”; “Đã xoá yêu cầu xây dựng giá” / “Xoá thất bại”.'),
    [DET + ' => Tab Hồ sơ'], [('m151-07.png', 'Tab Hồ sơ'), ('m150-hoso.png', 'Tab Hồ sơ của dự án có hồ sơ Đã duyệt')],
    [
        ('Ô “Tìm theo mã hồ sơ” + Version GP + Ngày duyệt', 'Textbox', 'Enable', '–', 'Trống', 'Bấm Tìm kiếm để lọc.'),
        ('Bảng hồ sơ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         'Yêu cầu XD Giá (nút mở rộng + số) / STT / Mã hồ sơ / Tên hồ sơ / Version GP / Trạng thái / BOM list (liên '
         'kết mở BOM) / Ngày duyệt.'),
        ('Nút Xem chi tiết hồ sơ', 'Icon Button', 'Enable', '–', 'Hiển thị',
         'Popup chỉ đọc: Tên hồ sơ, Nội dung trình duyệt, Danh sách các file, BOM tổng hợp, bình luận, thông tin '
         'tham chiếu (Dự án, Giải pháp, PM, Ngày trình duyệt, Hạn duyệt, Người phê duyệt).'),
        ('Nút Yêu cầu xây dựng giá', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
         'Mở popup gửi yêu cầu xây dựng giá (đặc tả ở SRS Yêu cầu tính giá bán).'),
        ('Nút Tạo báo giá', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện', 'Tạo báo giá từ BOM của hồ sơ.'),
        ('Bảng con Yêu cầu xây dựng giá', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
         'STT / Mã YCBG / Người gửi / Ngày gửi / Deadline / Trạng thái / Báo giá / Ngày duyệt báo giá / Action (Xem '
         'yêu cầu, Sửa nháp, Xoá).'),
    ],
    [
        ('Bấm Xem chi tiết hồ sơ', 'Click', 'After:\n– Mở popup xem hồ sơ.'),
        ('Bấm Tạo báo giá', 'Click', 'After:\n– Tạo báo giá từ BOM; “Đã tạo báo giá”; chuyển sang màn sửa báo giá.'),
        ('Bấm Yêu cầu xây dựng giá', 'Click', 'After:\n– Mở popup yêu cầu xây dựng giá của hồ sơ.'),
    ], ui_mode='read', rule=('- Màn Danh sách, Phân trang và UI/UX.', 'list'))

# ------------------------------------------------------------------ 2.20 Báo giá
fn(20, 'Báo giá của dự án', dict(
    ten='Danh sách và thao tác báo giá của dự án',
    mota='Tab Báo giá (dự án thường / con): liệt kê báo giá của dự án, tạo báo giá, xem, sửa, sao chép, sửa ghi chú '
         'kinh doanh, xem lịch sử phê duyệt, xuất Excel, xoá.',
    tacnhan='NV KD phụ trách dự án; Người lập báo giá',
    dieukien='Đang ở màn chi tiết dự án thường / con.',
    chinh='1. Người dùng bấm tab “Báo giá”.\n2. Hệ thống hiện bảng “Danh sách báo giá”, mới tạo trước, 10 dòng/trang.\n'
          '3. NV KD phụ trách bấm “Tạo báo giá” → chuyển sang màn tạo báo giá cho dự án.\n'
          '4. Trên từng dòng: Xem chi tiết, Sửa / Làm giá, Sao chép, Sửa ghi chú kinh doanh, Lịch sử phê duyệt, Xuất '
          'Excel, Xoá theo điều kiện.',
    phu='• Rỗng → “Dự án chưa có báo giá nào.”\n'
        '• Sao chép: hệ thống kiểm tra thay đổi giá từ ERP; không có thay đổi → sang màn tạo báo giá bản sao; có → '
        'popup “Phát hiện thay đổi dữ liệu từ ERP” (nút “Xác nhận Sao chép báo giá” / “Hủy bỏ”); lỗi → “Không kiểm '
        'tra được thay đổi từ ERP”.\n'
        '• Xuất Excel lỗi → “Xuất Excel chưa được triển khai đầy đủ”.'),
    [DET + ' => Tab Báo giá'], [('m151-08.png', 'Tab Báo giá – danh sách báo giá của dự án')],
    [
        ('Nút Tạo báo giá', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không phải NV KD phụ trách',
         'Chuyển sang màn Tạo báo giá cho dự án.'),
        ('Bảng “Danh sách báo giá”', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
         'STT / Mã BG (“Mã BG - Tên BOM”, dòng phụ “YCBG: mã”) / Loại (Từ BOM / Tự nhập) / Version GP / BOM (liên kết '
         'mở BOM) / Khách hàng / Loại tiền tệ / Tổng giá trị báo giá / Người lập / Trạng thái (Đang tạo, Chờ TP '
         'duyệt, Chờ BGĐ duyệt, Đã duyệt, Đóng, Dừng, Trúng thầu) / Ngày duyệt (dd/mm/yyyy hh:mm).'),
        ('Nút Xem chi tiết', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Mở màn chi tiết báo giá.'),
        ('Nút Sửa / Làm giá', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện',
         'Báo giá Đang tạo và người xem là người lập.'),
        ('Nút Sao chép báo giá', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện',
         'Báo giá từ yêu cầu xây dựng giá: cần quyền Q2 (Triển khai theo Phòng) hoặc Q3 (loại khác); báo giá tự '
         'lập: NV KD phụ trách.'),
        ('Nút Sửa ghi chú kinh doanh', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện',
         'Báo giá Đã duyệt và người xem là NV KD phụ trách; popup ô “Ghi chú” (placeholder “Nhập ghi chú...”), nút '
         'Lưu / Đóng.'),
        ('Nút Lịch sử phê duyệt', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
         'Popup “Lịch sử báo giá” dạng dòng thời gian; rỗng “Chưa có lịch sử”.'),
        ('Nút Xuất Excel', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
         'Tải file BaoGia_<mã>.xlsx; cột giá vốn theo quyền Q4.'),
        ('Nút Xoá', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện',
         'Báo giá Đang tạo và người xem là người lập.'),
        ('Phân trang', 'Pagination', 'Enable', '–', '–', '10 dòng/trang', '–'),
    ],
    [
        ('Bấm Tạo báo giá', 'Click', 'After:\n– Chuyển sang màn Tạo báo giá của dự án (đặc tả ở SRS Báo giá).'),
        ('Bấm Lưu (Ghi chú kinh doanh)', 'Click',
         'During:\n– Máy chủ chặn: “Chỉ có thể sửa ghi chú khi báo giá đã duyệt.” / “Chỉ NV Kinh doanh phụ trách dự '
         'án mới có thể cập nhật ghi chú.”\nAfter:\n– Lưu ghi chú, ghi lịch sử; “Đã lưu ghi chú”; lỗi → “Lỗi lưu”.'),
        ('Bấm Xoá → Xoá', 'Click',
         'Before:\n– Hộp “Xác nhận xoá”: “Bạn có chắc muốn xoá báo giá "{mã}"?” (Xoá / Huỷ).\nDuring:\n– “Báo giá không '
         'ở trạng thái Đang tạo, không thể sửa.” / “Chỉ người tạo báo giá mới có thể sửa.”\nAfter:\n– Xoá báo giá; '
         'yêu cầu xây dựng giá không còn báo giá thì về “Chờ XD giá”; “Đã xoá báo giá”.'),
        ('Bấm Sao chép báo giá', 'Click', 'After:\n– Không có thay đổi → mở màn tạo báo giá bản sao; có thay đổi → '
         'popup so sánh (Loại thay đổi, Mã / Tên vật tư, Thông tin cũ (V1), Thông tin mới (Cập nhật), Hành động hệ '
         'thống).'),
    ], uc=('FR-20', 'Báo giá của dự án', 'crud', A_KD), rule=('- Màn Danh sách, Phân trang và UI/UX.', 'list'))

# ------------------------------------------------------------------ 2.21 Chốt / Hủy chốt
fn(21, 'Chốt / Hủy chốt báo giá trúng thầu', dict(
    ten='Chốt báo giá trúng thầu và hủy chốt',
    mota='NV KD phụ trách chốt một báo giá Đã duyệt thành “Trúng thầu” (mỗi dự án 1 báo giá) hoặc hủy chốt để quay '
         'lại “Đã duyệt”.',
    tacnhan='NV KD phụ trách dự án',
    dieukien='Chốt: báo giá Đã duyệt, dự án chưa có báo giá trúng thầu. Hủy chốt: báo giá đang Trúng thầu.',
    chinh='1. Ở tab Báo giá, NV KD phụ trách bấm “Chốt báo giá (Trúng thầu)” trên dòng báo giá Đã duyệt.\n'
          '2. Popup xác nhận: “Chốt báo giá {mã} thành Trúng thầu? Mỗi dự án chỉ có 1 báo giá trúng thầu.”, đính kèm '
          '“File xác nhận của khách hàng” (bắt buộc).\n3. Bấm “Chốt” → báo giá chuyển Trúng thầu, dự án tiến lên '
          '“Thương thảo hợp đồng”; thông báo “Đã chốt báo giá (Trúng thầu)”.\n'
          '4. Hủy chốt: bấm “Hủy chốt” trên dòng Trúng thầu, nhập Lý do hủy chốt, bấm “Xác nhận hủy chốt”.',
    phu='• Thiếu file → “Vui lòng đính kèm file xác nhận của khách hàng”.\n'
        '• Lý do hủy chốt trống → “Vui lòng nhập lý do hủy chốt.”\n'
        '• Hủy chốt thành công → báo giá về “Đã duyệt”, xoá file chốt; dự án đang “Thương thảo hợp đồng” thì lùi về '
        '“Thương thảo giá và giải pháp”; “Đã hủy chốt báo giá”.',
    dacbiet='Sau khi chốt, tab Báo giá hiện thêm khối Đồng bộ hàng tạm và Lập hợp đồng ERP (FR-22).'),
    [DET + ' => Tab Báo giá'],
    [('m144-baogia.png', 'Tab Báo giá của dự án đã có báo giá Trúng thầu (người xem không phải NV KD phụ trách nên không có nút Chốt / Hủy chốt)')],
    [
        ('Nút Chốt báo giá (Trúng thầu)', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện', '–'),
        ('Popup Chốt – nội dung', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu',
         'Dòng phụ “Báo giá: {mã}”; câu xác nhận như Dòng sự kiện chính.'),
        ('Popup Chốt – File xác nhận của khách hàng', 'Table/Grid', 'Enable', '–', 'Có', 'Trống', 'Bảng đính kèm file.'),
        ('Popup Chốt – Nút Chốt / Huỷ', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Đang xử lý: “Đang chốt...”.'),
        ('Nút Hủy chốt', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện', 'Dòng báo giá Trúng thầu.'),
        ('Popup Hủy chốt – Lý do hủy chốt', 'Textarea', 'Enable', '0–1000 ký tự', 'Có', 'Trống',
         'Mô tả “Hủy chốt báo giá {mã} — báo giá sẽ quay lại trạng thái "Đã duyệt".”; placeholder “Nhập lý do hủy '
         'chốt...”.'),
        ('Popup Hủy chốt – Nút Xác nhận hủy chốt / Huỷ', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ],
    [
        ('Bấm Chốt', 'Click',
         'Before:\n– Chỉ NV KD phụ trách thấy nút.\nDuring:\n– Thiếu file → “Vui lòng đính kèm file xác nhận của '
         'khách hàng”.\n– Máy chủ chặn: “Chỉ chốt được báo giá đã duyệt.” / “Dự án đã có báo giá trúng thầu, vui '
         'lòng hủy chốt trước.” / “File chưa tải lên xong, vui lòng thử lại”.\nAfter:\n– Báo giá → Trúng thầu, lưu '
         'file; dự án tiến lên “Thương thảo hợp đồng” (không lùi).\n– “Đã chốt báo giá (Trúng thầu)”.'),
        ('Bấm Xác nhận hủy chốt', 'Click',
         'During:\n– Lý do trống → “Vui lòng nhập lý do hủy chốt.”; máy chủ chặn “Báo giá chưa ở trạng thái trúng '
         'thầu.”\nAfter:\n– Báo giá → Đã duyệt; dự án lùi về “Thương thảo giá và giải pháp” nếu đang ở “Thương thảo '
         'hợp đồng”.\n– “Đã hủy chốt báo giá”.'),
    ], uc=('FR-21', 'Chốt / Hủy chốt báo giá', 'action', A_KD),
    rule=('- Thông báo, Quy tắc Xóa.', 'notice'))

# ------------------------------------------------------------------ 2.22 Đồng bộ ERP
fn(22, 'Đồng bộ hàng tạm & lập hợp đồng ERP', dict(
    ten='Đồng bộ hàng tạm sang ERP và lập hợp đồng ERP từ báo giá trúng thầu',
    mota='Khi dự án có báo giá Trúng thầu, tab Báo giá hiện 2 khối: gửi duyệt hàng tạm (hàng chưa có mã ERP) sang '
         'ERP và lập hợp đồng bên ERP từ báo giá đó.',
    tacnhan='NV KD phụ trách dự án; Người lập báo giá',
    dieukien='Dự án có báo giá Trúng thầu.',
    chinh='1. Khối “Báo giá trúng thầu {mã} — Đồng bộ hàng tạm sang ERP” (chỉ khi báo giá có hàng tạm): NV KD phụ '
          'trách bấm “Gửi duyệt hàng tạm” → xác nhận “Gửi duyệt hàng tạm của báo giá trúng thầu sang ERP?” (Gửi '
          'duyệt / Huỷ).\n2. Sau khi ERP duyệt, bấm “Cập nhật kết quả duyệt” để kéo kết quả về.\n'
          '3. Khối “Lập hợp đồng ERP từ báo giá {mã}”: khi đủ điều kiện, người lập báo giá bấm “Lập hợp đồng ERP” → '
          'mở màn tạo hợp đồng bên ERP ở tab mới.',
    phu='• Mở tab khi đang đồng bộ → hệ thống tự cập nhật kết quả duyệt 1 lần.\n'
        '• Có hàng tạm bị từ chối → thông báo đỏ “Có {n} hàng tạm bị từ chối”; ngược lại “Đã cập nhật kết quả '
        'duyệt”.\n• Badge khối hợp đồng: Đã lập hợp đồng ERP / Báo giá ngoại tệ — chưa hỗ trợ / Báo giá có cấp con — '
        'chưa hỗ trợ lập HĐ / Chờ đồng bộ hết hàng sang ERP / Sẵn sàng lập hợp đồng / Đã đồng bộ — chỉ người lập báo '
        'giá mới lập được HĐ.'),
    [DET + ' => Tab Báo giá'], [('m144-baogia.png', 'Khối Lập hợp đồng ERP ở đầu tab Báo giá (báo giá có cấp con — chưa hỗ trợ lập HĐ)')],
    [
        ('Badge trạng thái đồng bộ', 'Badge', 'Hiển thị', 'Danh sách 3 giá trị', '–', 'Theo dữ liệu',
         'Chưa đồng bộ / Đang đồng bộ sang ERP / Đã đồng bộ; dòng tiến độ “n hàng tạm chờ gửi” / “a/t hàng tạm đã '
         'duyệt” / “t/t hàng tạm đã tạo trên ERP”; liên kết “Mã phiếu: {mã}” mở phiếu bên ERP.'),
        ('Nút Gửi duyệt hàng tạm', 'Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện',
         'NV KD phụ trách, chưa đồng bộ, còn hàng tạm chưa gửi.'),
        ('Nút Cập nhật kết quả duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện',
         'NV KD phụ trách, đang đồng bộ.'),
        ('Khối Lập hợp đồng ERP', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
         'Badge trạng thái; Mã hợp đồng ERP (liên kết); Trạng thái đồng bộ (Đã đồng bộ / Đồng bộ lỗi / Chưa đồng '
         'bộ); Thời gian đồng bộ.'),
        ('Nút Lập hợp đồng ERP', 'Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện',
         'Đã đồng bộ hết hàng, tiền VND, chưa có hợp đồng, người xem là người lập báo giá, báo giá không có dòng con.'),
    ],
    [
        ('Bấm Gửi duyệt hàng tạm → Gửi duyệt', 'Click',
         'During:\n– Máy chủ chặn: “Bạn không phải Sale phụ trách dự án này” / “Không có báo giá trúng thầu cần gửi '
         'duyệt hàng tạm.”\nAfter:\n– Gửi phiếu hàng tạm sang ERP; “Đã gửi duyệt hàng tạm sang ERP”.'),
        ('Bấm Cập nhật kết quả duyệt', 'Click',
         'During:\n– “Không có báo giá đang đồng bộ.”\nAfter:\n– Cập nhật mã ERP cho hàng đã duyệt; thông báo kết '
         'quả như Dòng sự kiện phụ.'),
        ('Bấm Lập hợp đồng ERP', 'Click', 'After:\n– Mở màn tạo hợp đồng bên ERP ở tab mới, gắn báo giá.'),
    ], uc=('FR-22', 'Đồng bộ hàng tạm & HĐ ERP', 'io', A_KD), rule=('- Thông báo, Quy tắc Xóa.', 'notice'))

# ------------------------------------------------------------------ 2.23 Báo giá dự án cha
fn(23, 'Báo giá của dự án cha', dict(
    ten='Báo giá từ dự án con và báo giá tổng',
    mota='Tab Báo giá của dự án cha gồm 2 khu vực: báo giá của các dự án con và báo giá tổng gộp từ báo giá con.',
    tacnhan='NV KD phụ trách dự án cha',
    dieukien='Đang ở màn chi tiết dự án cha.',
    chinh='1. Người dùng bấm tab “Báo giá” của dự án cha.\n2. Khu vực “Báo giá từ dự án con” liệt kê báo giá của mọi '
          'dự án con.\n3. Khu vực “Báo giá tổng”: NV KD phụ trách bấm “Tạo báo giá tổng” → chuyển sang màn tạo báo giá '
          'tổng, chọn báo giá nguồn (mỗi dự án con 1 báo giá).\n4. Trên dòng báo giá tổng: Xem, Sửa, Tải Excel, In, '
          'Sao chép, Xoá theo điều kiện.',
    phu='• Khu vực 1 rỗng → “Các dự án con chưa có báo giá nào.”\n'
        '• Khu vực 2 rỗng → “Chưa có báo giá tổng nào. Bấm [Tạo báo giá tổng] để gộp báo giá của các dự án con.”\n'
        '• Sao chép báo giá tổng → xác nhận “Sao chép "{mã}" thành bản mới? Bản hiện tại sẽ chuyển sang Hết hiệu '
        'lực.”; thành công “Đã sao chép báo giá tổng”.\n'
        '• Xoá báo giá tổng → xác nhận “Xoá báo giá tổng "{mã}"? Các báo giá nguồn KHÔNG bị ảnh hưởng.”; “Đã xoá báo '
        'giá tổng”.'),
    [DET + ' => Tab Báo giá'], [('m157-02.png', 'Tab Báo giá của dự án cha')],
    [
        ('Bảng Báo giá từ dự án con', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
         'STT / Mã báo giá / Dự án con (nút “Mở dự án con”) / Người phụ trách / Người làm giá / Người phê duyệt / Tổng '
         'giá trị / Trạng thái / Trạng thái sử dụng (Đã lên hợp đồng / Đã gộp BG Tổng / Chưa dùng) / Mã hợp đồng ERP.'),
        ('Nút dòng báo giá con', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện',
         'Xem chi tiết báo giá, Sửa / làm giá (Đang tạo + người lập), Tải Excel (“Không xuất được file Excel”), In '
         'báo giá (“Không tải được dữ liệu để in”), Sao chép, Xoá (“Không xoá được báo giá”).'),
        ('Nút Tạo báo giá tổng', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không phải NV KD phụ trách', '–'),
        ('Bảng Báo giá tổng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
         'STT / Mã báo giá tổng / Báo giá nguồn / Tổng tiền / Người tạo / Trạng thái (Đang tạo, Chờ duyệt, Đã duyệt, '
         'Trúng thầu, Đã tạo hợp đồng, Hết hiệu lực, Đóng).'),
        ('Nút dòng báo giá tổng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện',
         'Xem; Sửa và Xoá (Đang tạo + NV KD phụ trách); Tải Excel / In (Đã duyệt, Trúng thầu, Đã tạo hợp đồng); Sao '
         'chép (các trạng thái đó + NV KD phụ trách).'),
    ],
    [
        ('Bấm Tạo báo giá tổng', 'Click', 'After:\n– Chuyển sang màn tạo báo giá tổng của dự án cha (đặc tả riêng).'),
        ('Bấm Sao chép / Xoá báo giá tổng', 'Click',
         'During:\n– Máy chủ chặn: “Chỉ sửa được báo giá tổng ở trạng thái Đang tạo.” / “Chỉ NV KD phụ trách chính '
         'của dự án cha mới được thao tác báo giá tổng.”\nAfter:\n– Thông báo như Dòng sự kiện phụ; sao chép xong mở '
         'chi tiết bản mới.'),
    ], uc=('FR-23', 'Báo giá dự án cha', 'crud', A_KD), rule=('- Màn Danh sách, Phân trang và UI/UX.', 'list'))

# ------------------------------------------------------------------ 2.24 Dự án con
fn(24, 'Dự án con', dict(
    ten='Danh sách dự án con và thêm dự án con',
    mota='Tab “Dự án con” của dự án cha: tóm tắt ngân sách, liệt kê dự án con và tạo dự án con mới.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn chi tiết dự án cha.',
    chinh='1. Người dùng bấm tab “Dự án con”.\n2. Hệ thống hiện Tổng ngân sách dự kiến, Đã phân bổ cho dự án con, '
          'Còn lại, Số dự án con và bảng “Danh sách dự án con”.\n'
          '3. Bấm “Thêm dự án con” → mở form Tạo mới với Loại dự án = Dự án con và dự án cha chọn sẵn, khoá; thông '
          'tin kế thừa từ cha được điền (FR-06).',
    phu='• Rỗng → “Dự án cha này chưa có dự án con nào.”\n'
        '• Dự án cha còn Đang tạo → thay nút bằng dòng “Dự án cha chưa lưu chính thức (đang ở trạng thái Đang tạo). '
        'Vui lòng hoàn tất thông tin khách hàng và bấm Lưu trước khi thêm dự án con.”\n'
        '• Dự án cha đã Đóng / Kết thúc → không có nút Thêm dự án con.\n• Còn lại âm → hiển thị màu đỏ.'),
    [DET + ' => Tab Dự án con', DET + ' => Tab Dự án con => Thêm dự án con'],
    [('m157-01.png', 'Tab Dự án con của dự án cha'),
     ('24b-them-dac.png', 'Form tạo dự án con mở từ nút Thêm dự án con')],
    [
        ('Khối tóm tắt ngân sách', 'Number', 'Read-only', '–', '–', 'Theo dữ liệu',
         'Tổng ngân sách dự kiến, Đã phân bổ cho dự án con, Còn lại (xanh nếu ≥ 0, đỏ nếu âm), Số dự án con.'),
        ('Nút Thêm dự án con', 'Button', 'Enable / Ẩn', '–', '–', 'Theo trạng thái dự án cha', '–'),
        ('Bảng “Danh sách dự án con”', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
         'STT / Tên dự án TKT (KD phụ trách, Phòng ban, Bộ phận, Ngày tạo, Ngày cập nhật) / Tiến trình nội bộ / Giải '
         'pháp / Version / Khách hàng / Khách hàng cuối / Giai đoạn / Quy mô / Phân loại đầu tư / Nguồn vốn / Tổng số '
         'ngày hoàn thành / Phòng làm GP / PM giải pháp / Ngày KH cần GP / Ngày dự kiến chốt GP / Ứng dụng / Lĩnh '
         'vực / Loại hình / Ngân sách dự kiến / Thời gian (“bắt đầu đến kết thúc”). Không phân trang.'),
        ('Thao tác dòng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
         'Xem (mở chi tiết dự án con ở tab mới), Sửa (mở form sửa ở tab mới).'),
    ],
    [
        ('Bấm Thêm dự án con', 'Click',
         'After:\n– Mở form Tạo mới dự án con; kế thừa Khách hàng, KH cuối, tiền tệ, giảm giá, bảng giá, NV KD chính.'),
        ('Lưu dự án con', 'Click', 'After:\n– Như FR-06; ngân sách đã phân bổ của cha cộng thêm; cha đang Đang tạo '
         'không cho thêm con.'),
    ], uc=('FR-24', 'Thêm dự án con', 'crud', A_ALL), rule=('- Màn Danh sách, Phân trang và UI/UX.', 'list'))

# ------------------------------------------------------------------ 2.25 Tab Gia hạn
fn(25, 'Tab Gia hạn', dict(
    ten='Xem đề xuất gia hạn của dự án',
    mota='Liệt kê (chỉ xem) các đề xuất gia hạn Hạn đóng tự động của dự án và kết quả duyệt.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn chi tiết dự án thường / con.',
    chinh='1. Người dùng bấm tab “Gia hạn”.\n2. Hệ thống hiện bảng “Đề xuất gia hạn dự án”.',
    phu='• Rỗng → “Dự án chưa có đề xuất gia hạn nào.”\n'
        '• Duyệt / từ chối đề xuất thực hiện ở màn “Gia hạn dự án TKT” (người có quyền Q5 / Q6), không ở tab này.'),
    [DET + ' => Tab Gia hạn'], [('25-tab-gia-han.png', 'Tab Gia hạn có đề xuất đang chờ Trưởng phòng duyệt')],
    [
        ('Bảng “Đề xuất gia hạn dự án”', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         'STT / Mã đề xuất (GHDA.NNNNN) / Số ngày xin gia hạn (“n ngày”) / Hạn đóng tự động (“cũ → mới”, chưa duyệt '
         'kèm “(chờ duyệt)”) / Lý do gia hạn / Cấp duyệt (“Cấp 1 — TP duyệt” / “Cấp 2 — TP + BGĐ duyệt”) / Người đề '
         'xuất / Ngày gửi / Người xử lý / Lý do từ chối / Trạng thái (Chờ TP duyệt / Chờ BGĐ duyệt / Đã duyệt / Từ '
         'chối).'),
        ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Dự án chưa có đề xuất gia hạn nào.”'),
    ],
    [('Bấm tab Gia hạn', 'Click', 'After:\n– Nạp danh sách đề xuất của dự án (không phân trang).')],
    ui_mode='read', rule=('- Màn Danh sách, Phân trang và UI/UX.', 'list'))

# ------------------------------------------------------------------ 2.26 Thu thập thông tin
fn(26, 'Nhập phiếu thu thập thông tin', dict(
    ten='Nhập và lưu phiếu thu thập thông tin dự án',
    mota='Tab “Thu thập thông tin”: nhập câu trả lời cho phiếu khảo sát của dự án (bản chụp theo Ứng dụng) và lưu.',
    tacnhan='Người tạo dự án; Người có quyền xem theo cấp',
    dieukien='Đang ở màn chi tiết dự án thường / con; dự án đã có phiếu (đã chọn Ứng dụng có mẫu phiếu Published).',
    chinh='1. Người dùng bấm tab “Thu thập thông tin”.\n2. Hệ thống hiện phiếu: tên mẫu phiếu, mục “1. Thông tin '
          'chọn” (Ứng dụng – khoá), các phần A, B, C… → nhóm I, II… → câu hỏi 1, 2… → câu con 3.1, 3.2….\n'
          '3. Người dùng trả lời từng câu, ghi chú (nếu có), bấm “Lưu phiếu”.\n'
          '4. Hệ thống lưu, ghi lịch sử thay đổi, thông báo “Lưu phiếu thu thập thông tin thành công”.',
    phu='• Chưa có phiếu → “Chưa có phiếu thu thập thông tin cho dự án này”.\n'
        '• Đang tải → “Đang tải phiếu thu thập thông tin...”.\n'
        '• Người không được sửa dự án → không có nút “Lưu phiếu”.\n'
        '• Lỗi → “Có lỗi xảy ra khi lưu phiếu thu thập thông tin”; thiếu phiếu → “Dự án chưa có snapshot của phiếu”.\n'
        '• Câu hỏi có điều kiện hiển thị chỉ hiện khi câu phụ thuộc thoả điều kiện.',
    dacbiet='Không có bước chốt phiếu; sửa lại được không giới hạn. Phiếu chưa đủ câu bắt buộc sẽ chặn Tạo giải pháp '
            '/ gửi Yêu cầu làm giải pháp (BR-09).'),
    [DET + ' => Tab Thu thập thông tin => Lưu phiếu'], [('26-thu-thap.png', 'Tab Thu thập thông tin')],
    [
        ('Nút Lịch sử thay đổi / Lưu phiếu / Xem mẫu in', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị khi có phiếu',
         'Lưu phiếu có ở đầu và cuối phiếu, ẩn khi không được sửa dự án.'),
        ('Ứng dụng (mục 1. Thông tin chọn)', 'Textbox', 'Disable', '–', '–', 'Ứng dụng của dự án', '–'),
        ('Câu hỏi Text ngắn / Text dài', 'Textbox / Textarea', 'Enable', '–', 'Theo cấu hình câu (*)', 'Đáp án đã lưu',
         'Placeholder “Nhập...” / “Nhập chi tiết...”.'),
        ('Câu hỏi Số', 'Number', 'Enable', 'Số', 'Theo cấu hình', 'Đáp án đã lưu', '–'),
        ('Câu hỏi Ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Theo cấu hình', 'Đáp án đã lưu', '“Chọn ngày...”.'),
        ('Câu hỏi Có/Không, Radio, Checkbox, Dropdown', 'Radio / Checkbox / Dropdown', 'Enable', 'Danh sách đáp án',
         'Theo cấu hình', 'Đáp án đã lưu', 'Checkbox chọn nhiều.'),
        ('Câu hỏi File', 'Table/Grid', 'Enable', '–', 'Theo cấu hình', 'File đã lưu', '“Chọn tệp...”, nhiều file.'),
        ('Nhóm câu hỏi (câu cha)', 'Label', 'Hiển thị', '–', '–', '–',
         'Chứa câu con thụt lề; rỗng “Chưa có câu hỏi con nào.”'),
        ('Ghi chú của câu', 'Textarea', 'Enable', '–', 'Không', 'Trống',
         'Liên kết “Ghi chú” dưới câu (trừ text / textarea / câu cha); placeholder “Nhập ghi chú (nếu có)...”.'),
        ('Phần “Thông tin bổ sung”', 'Textarea', 'Enable', '–', 'Không', 'Đáp án đã lưu',
         'Câu hỏi bộ phận giải pháp yêu cầu bổ sung; “Nhập câu trả lời...”.'),
    ],
    [
        ('Bấm Lưu phiếu', 'Click',
         'Before:\n– Không được sửa dự án → nút không hiển thị; gọi thẳng → “Bạn không có quyền sửa dự án này.”\n'
         'During:\n– Không chặn câu bắt buộc khi lưu.\nAfter:\n– Lưu toàn bộ đáp án, ghi lịch sử “Cập nhật câu trả '
         'lời” (chỉ khi có thay đổi); nạp lại phiếu.\n– “Lưu phiếu thu thập thông tin thành công”; lỗi → “Có lỗi xảy '
         'ra khi lưu phiếu thu thập thông tin”.'),
        ('Bấm “Ghi chú”', 'Click', 'After:\n– Mở ô ghi chú 2 dòng; Enter / rời ô thì thu gọn.'),
    ], uc=('FR-26', 'Nhập phiếu thu thập thông tin', 'crud', A_ALL),
    rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'))

# ------------------------------------------------------------------ 2.27 Lịch sử phiếu
fn(27, 'Lịch sử thay đổi phiếu thu thập', dict(
    ten='Xem lịch sử thay đổi phiếu thu thập thông tin',
    mota='Dòng thời gian các lần tạo phiếu, cập nhật câu trả lời, bổ sung câu hỏi.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Dự án đã có phiếu thu thập thông tin.',
    chinh='1. Ở tab Thu thập thông tin, người dùng bấm “Lịch sử thay đổi”.\n2. Popup “Lịch sử thay đổi phiếu thu '
          'thập thông tin” hiện các lần thay đổi, mới nhất trước.\n3. Bấm “Đóng”.',
    phu='• Chưa có lịch sử → “Chưa có lịch sử thay đổi nào.”\n• Lỗi → “Lỗi khi tải lịch sử”.'),
    [DET + ' => Tab Thu thập thông tin => Lịch sử thay đổi'], [('27-ls-phieu.png', 'Popup Lịch sử thay đổi phiếu')],
    [
        ('Mục lịch sử', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
         'Chấm màu + thời điểm + hành động (“Tạo mới phiếu thu thập thông tin” / “Cập nhật câu trả lời” / “Yêu cầu '
         'bổ sung câu hỏi”) + “— tên người thực hiện”.'),
        ('Chi tiết thay đổi', 'Text', 'Read-only', '–', 'Theo dữ liệu',
         '“Nhãn câu hỏi: giá trị cũ → giá trị mới”, giá trị trống hiện “(trống)”; bổ sung câu hỏi liệt kê câu được thêm.'),
        ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '–'),
    ],
    [('Bấm Lịch sử thay đổi', 'Click', 'After:\n– Nạp lịch sử, mở popup; lỗi → “Lỗi khi tải lịch sử”.')],
    ui_mode='read', rule=('- Quy tắc ghi lịch sử.', 'history'))

# ------------------------------------------------------------------ 2.28 Xem mẫu in
fn(28, 'Xem mẫu in phiếu thu thập', dict(
    ten='Xem mẫu in và in phiếu thu thập thông tin',
    mota='Xem trước bản in “PHIẾU THU THẬP THÔNG TIN DỰ ÁN” kèm đáp án và in.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Dự án đã có phiếu thu thập thông tin.',
    chinh='1. Ở tab Thu thập thông tin, bấm “Xem mẫu in”.\n2. Popup “Xem mẫu in phiếu thu thập thông tin” hiện bản '
          'in: letterhead, Tên khách hàng, Tên dự án, Mã dự án, Ứng dụng, Ngày khảo sát, Người khảo sát và bảng “NỘI '
          'DUNG KHẢO SÁT”.\n3. Bấm “In” → mở hộp thoại in của trình duyệt.',
    phu='• Phiếu chưa tải xong → “Chưa tải xong phiếu thu thập thông tin”.\n'
        '• Trình duyệt chặn cửa sổ mới → “Không thể mở cửa sổ in. Vui lòng cho phép popup.”'),
    [DET + ' => Tab Thu thập thông tin => Xem mẫu in'], [('28-mau-in.png', 'Popup Xem mẫu in phiếu thu thập thông tin')],
    [
        ('Bản in', 'Text', 'Read-only', '–', 'Theo dữ liệu',
         'Tiêu đề “PHIẾU THU THẬP THÔNG TIN DỰ ÁN”; bảng STT | NỘI DUNG | LOẠI CÂU HỎI | GIÁ TRỊ LỰA CHỌN ĐI KÈM | ĐÁP '
         'ÁN / GIÁ TRỊ THU THẬP.'),
        ('Nút In / Đóng', 'Button', 'Enable', '–', 'Hiển thị', '–'),
    ],
    [('Bấm Xem mẫu in', 'Click', 'After:\n– Mở popup xem trước.'),
     ('Bấm In', 'Click', 'After:\n– Mở cửa sổ “Phiếu thu thập thông tin” và hộp thoại in; lỗi như Dòng sự kiện phụ.')],
    ui_mode='read', rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'))

# ------------------------------------------------------------------ 2.29 Chốt giải pháp
fn(29, 'Chốt giải pháp', dict(
    ten='Chốt giải pháp của dự án',
    mota='NV KD phụ trách chọn hồ sơ giải pháp đã duyệt mà khách hàng chấp nhận, đính kèm file xác nhận, chốt giải '
         'pháp và gửi thông báo.',
    tacnhan='NV KD phụ trách dự án',
    dieukien='Dự án chưa đóng; người dùng là NV KD phụ trách; dự án có ít nhất 1 hồ sơ giải pháp Đã duyệt / Hết hiệu '
             'lực.',
    chinh='1. Ở chân màn chi tiết, bấm “Chốt giải pháp”.\n2. Popup “Chốt giải pháp” (dòng phụ “Dự án: {mã - tên}”) '
          'liệt kê hồ sơ chốt được.\n3. Chọn 1 hồ sơ, nhập Ghi chú chốt giải pháp, đính kèm File xác nhận của khách '
          'hàng.\n4. Bấm “Lưu & gửi thông báo” → hệ thống chốt, thông báo “Đã chốt giải pháp thành công”.',
    phu='• Không có hồ sơ → “Không có hồ sơ nào ở trạng thái Đã duyệt / Hết hiệu lực.”\n'
        '• Chưa chọn hồ sơ → “Vui lòng chọn hồ sơ giải pháp”.\n'
        '• Lỗi → “Chốt giải pháp thất bại. Vui lòng thử lại.”'),
    [DET + ' => Chốt giải pháp'], [('29-chot-gp.png', 'Popup Chốt giải pháp')],
    [
        ('Bảng “Chọn hồ sơ giải pháp”', 'Table/Grid', 'Enable', 'Danh sách', 'Có', 'Chưa chọn',
         'Chọn 1 dòng; cột Mã hồ sơ / Version GP / Trạng thái / Ngày duyệt. Đang tải: “Đang tải danh sách hồ sơ...”.'),
        ('Ghi chú chốt giải pháp', 'Textarea', 'Enable', '0–1000 ký tự', 'Không', 'Trống',
         'Placeholder “Nhập ghi chú (tối đa 1000 ký tự)”.'),
        ('File xác nhận của khách hàng', 'Table/Grid', 'Enable', '–', 'Có', 'Trống', 'Bảng đính kèm file.'),
        ('Nút Lưu & gửi thông báo / Đóng', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
         'Đang xử lý: “Đang chốt...”.'),
    ],
    [
        ('Bấm Chốt giải pháp', 'Click', 'Before:\n' + NO_SHOW + '\nAfter:\n– Mở popup, nạp danh sách hồ sơ chốt được.'),
        ('Bấm Lưu & gửi thông báo', 'Click',
         'During:\n– Chưa chọn hồ sơ → “Vui lòng chọn hồ sơ giải pháp”.\n– Máy chủ chặn: “Chỉ NV KD phụ trách mới '
         'được chốt giải pháp.” / “Dự án chưa có giải pháp.” / “Hồ sơ không hợp lệ hoặc không ở trạng thái Đã duyệt / '
         'Hết hiệu lực.”\nAfter:\n– Hồ sơ → Đã chốt, lưu file; yêu cầu làm GP → Đã làm GP; giải pháp → Chốt giải '
         'pháp; dự án tiến lên “Lập dự toán” (nếu đang ở bước thấp hơn).\n– Gửi thông báo cho PM và người tạo giải '
         'pháp: “{Người thao tác} đã chốt giải pháp dự án {tên}. Hồ sơ: {mã}.”\n– “Đã chốt giải pháp thành công”, '
         'nạp lại màn, ẩn nút.'),
    ], uc=('FR-29', 'Chốt giải pháp', 'action', A_KD), rule=('- Thông báo, Quy tắc Xóa.', 'notice'))

# ------------------------------------------------------------------ 2.30 Gia hạn
fn(30, 'Gửi đề xuất gia hạn', dict(
    ten='Gửi đề xuất gia hạn dự án',
    mota='NV KD phụ trách xin lùi Hạn đóng tự động thêm một số ngày; đề xuất chờ Trưởng phòng (và Ban giám đốc nếu '
         'vượt ngưỡng) duyệt.',
    tacnhan='NV KD phụ trách dự án',
    dieukien='Người dùng là NV KD phụ trách; dự án không ở Thực hiện hợp đồng / Nghiệm thu và thanh lý hợp đồng / '
             'Đóng; chưa quá Hạn đóng tự động; không có đề xuất nào đang chờ duyệt.',
    chinh='1. Ở chân màn chi tiết, bấm “Gia hạn”.\n2. Popup hiện Hạn đóng tự động hiện tại và số ngày đã gia hạn.\n'
          '3. Nhập Số ngày gia hạn dự kiến và Lý do gia hạn, bấm “Gửi đề xuất”.\n'
          '4. Hệ thống tạo đề xuất GHDA.NNNNN “Chờ TP duyệt”, gửi thông báo, hiện “Đã gửi đề xuất gia hạn”; nút Gia '
          'hạn ẩn đi, tab Gia hạn nạp lại.',
    phu='• Dự án chưa có hạn → hiện “Không áp dụng”.\n'
        '• Kết quả duyệt / từ chối được báo lại cho người gửi; duyệt xong Hạn đóng tự động lùi thêm số ngày đã duyệt.'),
    [DET + ' => Gia hạn'], [('30-gia-han.png', 'Popup Gia hạn dự án'),
                            ('30b-gia-han-loi.png', 'Bấm Gửi đề xuất khi chưa nhập: lỗi dưới từng ô')],
    [
        ('Hạn đóng tự động / Đã gia hạn', 'Text', 'Read-only', 'dd/mm/yyyy', '–', 'Theo dữ liệu',
         'Chưa có hạn: “Không áp dụng”; “Đã gia hạn n ngày”.'),
        ('Số ngày gia hạn dự kiến', 'Number', 'Enable', '1 – 3650', 'Có', 'Trống',
         'Placeholder “Nhập số ngày gia hạn”. Lỗi: “Vui lòng nhập số ngày gia hạn” / “Số ngày gia hạn phải là số '
         'nguyên lớn hơn 0” / “Số ngày gia hạn tối đa 3650 ngày”.'),
        ('Lý do gia hạn', 'Textarea', 'Enable', '0–1000 ký tự', 'Có', 'Trống',
         'Placeholder “Nhập lý do gia hạn (tối đa 1000 ký tự)”. Lỗi: “Vui lòng nhập lý do gia hạn”.'),
        ('Nút Gửi đề xuất / Đóng', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Đang gửi: “Đang gửi...”.'),
    ],
    [
        ('Bấm Gia hạn', 'Click', 'Before:\n' + NO_SHOW + '\nAfter:\n– Mở popup.'),
        ('Bấm Gửi đề xuất', 'Click',
         'During:\n– Số ngày / lý do không hợp lệ → lỗi dưới ô.\n– Máy chủ chặn: “Chỉ NV KD phụ trách mới được gửi '
         'đề xuất gia hạn dự án.” / “Dự án đang ở trạng thái không cho phép gia hạn.” / “Dự án đã quá hạn đóng, không '
         'gửi được đề xuất gia hạn.” / “Dự án đang có đề xuất gia hạn chờ duyệt.”\nAfter:\n– Tạo đề xuất; số ngày ≤ '
         'ngưỡng cấu hình → cấp 1 (Trưởng phòng duyệt), vượt ngưỡng → cấp 2 (Trưởng phòng rồi Ban giám đốc).\n'
         '– Gửi thông báo cho người có quyền duyệt: “[DATKT] Chờ duyệt: {tên}. Xin gia hạn n ngày.”\n'
         '– “Đã gửi đề xuất gia hạn”.'),
    ], uc=('FR-30', 'Gửi đề xuất gia hạn', 'action', A_KD),
    rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'))

# ------------------------------------------------------------------ 2.31 Đóng dự án
fn(31, 'Đóng dự án', dict(
    ten='Đóng / không thực hiện dự án',
    mota='NV KD phụ trách đóng dự án kèm nguyên nhân thất bại; hệ thống đóng dây chuyền giải pháp, yêu cầu, báo giá '
         '(và dự án con nếu là dự án cha).',
    tacnhan='NV KD phụ trách dự án',
    dieukien='Người dùng là NV KD phụ trách; dự án chưa đóng; dự án cha phải đang “Đang thực hiện”.',
    chinh='1. Ở chân màn chi tiết, bấm “Đóng dự án”.\n2. Popup hiện cảnh báo các dữ liệu sẽ bị đóng.\n'
          '3. Chọn Nguyên nhân thất bại, nhập Ghi chú bổ sung, tích “Tôi xác nhận muốn đóng dự án này.”.\n'
          '4. Bấm “Xác nhận đóng” → dự án chuyển “Đóng/Không thực hiện dự án”, thông báo “Đã đóng dự án” (dự án cha: '
          '“Đã đóng dự án cha và {n} dự án con”); màn hiện banner “Dự án đã đóng”, ẩn các nút.',
    phu='• Chưa chọn nguyên nhân hoặc chưa tích xác nhận → nút “Xác nhận đóng” bị khoá.\n'
        '• Lỗi → “Đóng dự án thất bại. Vui lòng thử lại.”',
    dacbiet='Thao tác không khôi phục được. Hệ thống còn tự đóng dự án quá hạn (BR-12).'),
    [DET + ' => Đóng dự án'], [('31-dong-du-an.png', 'Popup Đóng dự án')],
    [
        ('Khối cảnh báo', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
         '“Đóng dự án sẽ huỷ toàn bộ công việc:” + (dự án cha) “{n} dự án con trực thuộc sẽ bị đóng theo.”, “Các giải '
         'pháp chuyển sang Đóng.”, “Các hạng mục giải pháp chuyển sang Đóng.”, “Các yêu cầu xây dựng giá chuyển sang '
         'Đóng.”, “Các báo giá đang soạn/chờ duyệt chuyển sang Đóng.”, “Hành động này KHÔNG THỂ khôi phục.”'),
        ('Nguyên nhân thất bại', 'Dropdown', 'Enable', 'Danh mục Lý do thất bại đang hoạt động', 'Có', 'Trống',
         'Placeholder “-- Chọn nguyên nhân --”.'),
        ('Ghi chú bổ sung', 'Textarea', 'Enable', '0–500 ký tự', 'Không', 'Trống',
         'Placeholder “Nhập ghi chú bổ sung (tối đa 500 ký tự)”.'),
        ('Tôi xác nhận muốn đóng dự án này.', 'Checkbox', 'Enable', '–', 'Có', 'Bỏ tích', '–'),
        ('Nút Xác nhận đóng', 'Button', 'Enable / Disable', '–', '–', 'Disable',
         'Mở khi đã chọn nguyên nhân và tích xác nhận.'),
        ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng popup, không thực hiện.'),
    ],
    [
        ('Bấm Đóng dự án', 'Click', 'Before:\n' + NO_SHOW + '\nAfter:\n– Mở popup, nạp danh mục lý do thất bại.'),
        ('Bấm Xác nhận đóng', 'Click',
         'During:\n– Máy chủ chặn: “Chỉ NV KD phụ trách mới được đóng dự án.” / “Dự án đã đóng.” / “Nguyên nhân thất '
         'bại không hợp lệ.” / “Vui lòng chọn nguyên nhân” / “Ghi chú tối đa 500 ký tự”.\nAfter:\n– Dự án → Đóng/Không '
         'thực hiện dự án, lưu lý do, ghi chú, người và thời điểm đóng; ghi lịch sử “Đóng dự án”.\n– Đóng dây chuyền '
         '(BR-11); dự án cha đóng thêm báo giá tổng và từng dự án con.\n– Gửi thông báo cho người tạo / PM giải pháp, '
         'người đang làm giá, Trưởng phòng / Ban giám đốc duyệt giá liên quan: “{Người} đã đóng dự án {tên}. Lý do: '
         '… Ghi chú: …”.\n– “Đã đóng dự án” / “Đã đóng dự án cha và {n} dự án con”.'),
    ], uc=('FR-31', 'Đóng dự án', 'action', A_KD), rule=('- Thông báo, Quy tắc Xóa.', 'notice'))

# ======================================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.p('Quy tắc áp dụng: các quy tắc chung (danh sách, tìm kiếm, thêm mới, thông báo, xoá, lịch sử) theo SRS Các quy '
    'tắc chung; bảng dưới chỉ ghi quy tắc đặc thù của màn Dự án.')
d.rule_table([
    ('BR-01', 'Phạm vi dữ liệu xem',
     ['– Tổng công ty: mọi dự án; Công ty: dự án thuộc công ty đang làm việc; Phòng ban: dự án thuộc phòng ban / bộ '
      'phận mình quản lý + dự án mình tạo; Bộ phận: dự án thuộc bộ phận mình quản lý + dự án mình tạo; không có '
      'quyền: dự án mình tạo.',
      '– Luôn cộng thêm dự án mình được gán tên là KD hỗ trợ.',
      '– Đơn vị của dự án lấy theo người tạo lúc tạo.'], ['Xem danh sách', 'Xuất Excel']),
    ('BR-02', 'Bản nháp',
     ['– Lưu nháp: trạng thái “Đang tạo”, chỉ bắt buộc Tên dự án, chưa sinh mã.',
      '– Bản nháp của người khác không bao giờ hiện trong danh sách, kể cả với quyền tổng công ty.'],
     ['Tạo mới', 'Chỉnh sửa', 'Xem danh sách']),
    ('BR-03', 'Sinh mã dự án',
     ['– Sinh khi dự án rời trạng thái Đang tạo lần đầu (bấm Lưu) và đã có Ứng dụng.',
      '– Dự án thường / con: {Mã phòng}.{Mã ứng dụng}.{Năm}.DA{3 số}; dự án cha: {Mã phòng}.{Năm}.DAC{3 số}.',
      '– Mã phòng lấy theo người bấm Lưu; mã không sửa được.'], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-04', 'Tiến trình nội bộ (trạng thái)',
     ['– Dự án thường / con: Đang tạo → Thu thập thông tin dự án → Chờ tiếp nhận làm giải pháp → Đang làm giải pháp → '
      'Trao đổi giải pháp với khách hàng → Lập dự toán → Thương thảo giá và giải pháp → Thương thảo hợp đồng → Thực '
      'hiện hợp đồng → Nghiệm thu và thanh lý hợp đồng → Đóng/Không thực hiện dự án → Kết thúc và lưu trữ.',
      '– Dự án cha: Đang tạo → Đang thực hiện (khi lưu dự án con đầu tiên) → Trình duyệt hợp đồng → Thương thảo hợp '
      'đồng → HĐ đủ điều kiện thực hiện → Nghiệm thu & Thanh lý → Đóng/Không thực hiện dự án → Kết thúc & lưu trữ.',
      '– Chuyển tự động theo luồng: gửi yêu cầu làm GP, giải pháp đang làm / đã duyệt, chốt giải pháp hoặc gửi yêu '
      'cầu báo giá (→ Lập dự toán), báo giá được duyệt (→ Thương thảo giá và giải pháp), chốt báo giá trúng thầu (→ '
      'Thương thảo hợp đồng; hủy chốt lùi lại). Yêu cầu làm GP bị từ chối / hủy / yêu cầu bổ sung → lùi về Thu thập '
      'thông tin dự án.',
      '– Chữ và màu trạng thái do hệ thống quy định; mọi lần đổi trạng thái đều ghi nhận.'],
     ['Xem danh sách', 'Xem chi tiết']),
    ('BR-05', 'Cách triển khai và Có cần làm GP?',
     ['– Tự triển khai: KD tự làm, không được gửi yêu cầu làm giải pháp; được chọn Có / Không làm GP; Tạo giải pháp '
      'trực tiếp từ dự án.',
      '– Triển khai theo Phòng: phòng nhận yêu cầu làm GP cố định là phòng KD phụ trách chính; Liên phòng ban: người '
      'dùng tự chọn phòng nhận. Hai lựa chọn này luôn “Có cần làm GP? = Có”.',
      '– Chỉ đổi Cách triển khai / Có cần làm GP? khi dự án ở Đang tạo hoặc Thu thập thông tin dự án và chưa có giải '
      'pháp / yêu cầu làm GP.',
      '– Dự án Tự triển khai không làm GP ẩn các tab Yêu cầu, Giải pháp, Vấn đề giải pháp, Files, Hồ sơ.'],
     ['Tạo mới', 'Chỉnh sửa', 'Xem chi tiết']),
    ('BR-06', 'KH thương mại dịch vụ',
     ['– Không tích: Loại hình / Lĩnh vực / Ứng dụng tính theo KH trực tiếp; KH cuối = KH trực tiếp.',
      '– Tích: bắt buộc Khách hàng thụ hưởng cuối, Loại hình / Lĩnh vực và Email của KH cuối; Ứng dụng lọc theo KH '
      'cuối; người liên hệ KH cuối không bắt buộc.',
      '– Người liên hệ KH trực tiếp bắt buộc với KH doanh nghiệp, ẩn với KH cá nhân.'], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-07', 'Dự án cha / dự án con',
     ['– Dự án con kế thừa Khách hàng, KH cuối, Loại tiền tệ, Giảm giá, Bảng giá (và NV KD chính khi chưa có) từ dự '
      'án cha, không sửa được; chỉ gắn được vào dự án cha đã lưu chính thức, chưa đóng; ngày bắt đầu / kết thúc phải '
      'nằm trong khung thời gian của cha; Nhóm ngành phải thuộc nhóm ngành của cha.',
      '– Ngân sách đã phân bổ của cha = tổng ngân sách dự án con; tổng ngân sách cha không đổi được từ Trình duyệt hợp '
      'đồng trở đi.',
      '– Chỉ đổi Loại dự án khi dự án đang Đang tạo và chưa có dự án con; dự án cha đã có con không đổi được Khách '
      'hàng.',
      '– Đóng dự án cha thì đóng theo toàn bộ dự án con và báo giá tổng.'],
     ['Tạo mới', 'Chỉnh sửa', 'Dự án con', 'Đóng dự án']),
    ('BR-08', 'Nhóm ngành và Ứng dụng',
     ['– Mỗi cặp Khách hàng + Nhóm ngành chỉ có 1 dự án đang chạy (trạng thái Đang tạo → Thương thảo giá và giải '
      'pháp): “Nhóm ngành "X" đang thuộc dự án {mã} của khách hàng này. Chỉ được chọn lại khi dự án đó đã đóng, hủy '
      'hoặc chuyển sang làm hợp đồng.”',
      '– Nhóm ngành phải thuộc Ứng dụng: “Nhóm ngành "X" không thuộc ứng dụng "Y". Vui lòng chọn lại Ứng dụng hoặc '
      'Nhóm ngành.”; dự án con: “Nhóm ngành "X" không nằm trong nhóm ngành của dự án cha. Vui lòng chọn lại.”',
      '– Dự án cha chọn được nhiều nhóm ngành.'], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-09', 'Phiếu thu thập thông tin',
     ['– Khi lưu dự án có Ứng dụng, hệ thống chụp mẫu phiếu đang Published của Ứng dụng thành phiếu riêng của dự án; '
      'sửa mẫu gốc sau đó không ảnh hưởng.',
      '– Đổi Ứng dụng → tạo phiếu mới, đáp án cũ không chuyển sang.',
      '– Phiếu chưa trả lời đủ câu bắt buộc → không Tạo giải pháp / không gửi được Yêu cầu làm giải pháp.',
      '– Mọi lần lưu có thay đổi đều ghi lịch sử phiếu.'], ['Tạo mới', 'Chỉnh sửa', 'Nhập phiếu thu thập']),
    ('BR-10', 'Quyền sửa / xoá dự án',
     ['– Sửa: người tạo dự án, hoặc dự án nằm trong phạm vi quyền xem theo cấp; KD hỗ trợ chỉ được xem.',
      '– Xoá: người tạo, dự án Đang tạo, chưa có dự án con; xoá hẳn khỏi hệ thống.',
      '– Dự án đã đóng: ẩn mọi nút thao tác ở chân màn chi tiết.'], ['Chỉnh sửa', 'Xóa', 'Xem chi tiết']),
    ('BR-11', 'Đóng dự án',
     ['– Chỉ NV KD phụ trách; dự án cha chỉ đóng khi đang Đang thực hiện.',
      '– Đóng dây chuyền: giải pháp và hạng mục → Đóng; yêu cầu làm GP (trừ Từ chối / Đã làm GP) → Đóng; yêu cầu xây '
      'dựng giá đang Chờ / Đang xây dựng → Đóng; báo giá chưa đóng → Đóng.',
      '– Gửi thông báo cho người liên quan; không khôi phục được.'], ['Đóng dự án']),
    ('BR-12', 'Hạn đóng tự động và nhắc hạn',
     ['– Hạn đóng = ngày duyệt báo giá gần nhất + số tháng theo Giai đoạn dự án (chưa có báo giá duyệt: ngày tạo + '
      'số tháng cấu hình theo công ty), cộng số ngày đã được gia hạn; giai đoạn chưa cấu hình thì không tự đóng.',
      '– Hằng ngày 01:30: còn ≤ N ngày tới hạn → nhắc NV KD phụ trách 1 lần “[DATKT] Sắp đến hạn: {tên}. Còn x ngày '
      'tới hạn đóng (dd/mm/yyyy). Bạn còn theo dõi dự án này không?”; quá hạn thêm M ngày → tự đóng với lý do “Hệ '
      'thống tự đóng do quá thời gian thực hiện” và báo “[DATKT] Quá hạn: {tên}. Hệ thống tự đóng do quá thời gian '
      'thực hiện.”'], ['Đóng dự án', 'Gửi đề xuất gia hạn']),
    ('BR-13', 'Gia hạn dự án',
     ['– Mỗi dự án chỉ 1 đề xuất chờ duyệt; số ngày 1–3650.',
      '– Số ngày ≤ ngưỡng cấu hình: Trưởng phòng quản lý phòng của đề xuất duyệt; vượt ngưỡng: Trưởng phòng rồi Ban '
      'giám đốc cùng công ty duyệt.',
      '– Duyệt xong: cộng số ngày vào hạn đóng, ghi lịch sử “Gia hạn”, báo người gửi “[DATKT] Đã duyệt: … Hạn đóng mới '
      'dd/mm/yyyy.” hoặc “[DATKT] Từ chối: … Lý do: …”. Ngày kết thúc dự án không đổi.'],
     ['Gửi đề xuất gia hạn', 'Tab Gia hạn']),
    ('BR-14', 'Chốt giải pháp',
     ['– Chỉ NV KD phụ trách, chọn 1 hồ sơ Đã duyệt / Hết hiệu lực, bắt buộc file xác nhận của khách hàng.',
      '– Kết quả: hồ sơ Đã chốt, giải pháp Chốt giải pháp, yêu cầu làm GP Đã làm GP, dự án tiến lên Lập dự toán.'],
     ['Chốt giải pháp']),
    ('BR-15', 'Báo giá trúng thầu',
     ['– Mỗi dự án chỉ 1 báo giá Trúng thầu; chỉ chốt báo giá Đã duyệt, bắt buộc file xác nhận của khách hàng.',
      '– Chỉ NV KD phụ trách được tạo báo giá, chốt / hủy chốt, sửa ghi chú kinh doanh, đồng bộ hàng tạm; chỉ người '
      'lập báo giá được sửa / xoá báo giá Đang tạo và lập hợp đồng ERP.'],
     ['Báo giá của dự án', 'Chốt / Hủy chốt', 'Đồng bộ ERP']),
    ('BR-16', 'Yêu cầu điều chỉnh giải pháp',
     ['– Chỉ NV KD phụ trách tạo, khi giải pháp Đã duyệt giải pháp / Đã duyệt giá / Chờ làm giá / Chốt giải pháp.',
      '– PM giải pháp hoặc quản lý phòng tiếp nhận xử lý yêu cầu “Đã gửi”.',
      '– Tiếp nhận → dừng các yêu cầu xây dựng giá và báo giá đang làm của dự án.'], ['Yêu cầu điều chỉnh GP']),
    ('BR-17', 'Ràng buộc ngày',
     ['– Ngày bắt đầu dự án = ngày tạo, không sửa.',
      '– Khi dự án còn Đang tạo: Ngày kết thúc, Ngày KH cần nhận GP, Ngày chốt GP nội bộ ≥ hôm nay.',
      '– Ngày kết thúc ≥ Ngày bắt đầu; Ngày chốt GP nội bộ ≤ Ngày KH cần nhận GP.',
      '– Tổng số ngày thực hiện = Ngày kết thúc − Ngày bắt đầu + 1.'], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-18', 'Nhu cầu khách hàng',
     ['– Chỉ gắn nhu cầu “Đang theo dõi” của đúng khách hàng, chưa gắn dự án khác; gắn → nhu cầu chuyển “Đã lập dự '
      'án”, bỏ gắn → trả về “Đang theo dõi”.',
      '– Khách hàng có nhu cầu mà không chọn: chỉ cảnh báo, không chặn; nhu cầu không được gắn sẽ bị hệ thống đóng khi '
      'quá hạn.'], ['Tạo mới', 'Chỉnh sửa']),
])

d.save(update_fields=os.environ.get('SRS_NO_WORD') != '1')
print('OK ->', out)
