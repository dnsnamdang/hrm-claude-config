# -*- coding: utf-8 -*-
"""Sinh "SRS - Phê duyệt yêu cầu giải pháp.docx" theo FORM CHUẨN (bản mẫu 2026-09-24).

Chạy (từ bất kỳ đâu, BỌC KHOÁ WORD nếu có agent khác cũng sinh SRS):
    python3 .plans/phe-duyet-ycgp-hdsd/gen_srs.py
Thư viện dùng chung: .claude/skills/srs-documenter/assets/{srs_docx_lib,srs_uml_render}.py
Ảnh chụp thật (Playwright Python, 1440x900, nhánh develop, local): ycgp_pending_shots/ — chỉ để local.

Nguồn đối chiếu code:
  FE  pages/assign/request-solution/pending.vue · _id/index.vue · components/RequestSolutionForm.vue
      components/assign-components/RequestSolutionReceiveModal.vue
      components/modal/{V2BaseRejectApproveModal,export-fields-modal,column-customization-modal,
      filter-customization-modal}.vue · pages/assign/prospective-projects/components/formTabInput.vue
      pages/assign/form-templates/components/FormPreview.vue (khối "Thông tin bổ sung")
      Menu: components/menu-sidebar.js (hub Phê duyệt) · components/subsystem-menu/sale-hub.js
  BE  Modules/Assign/Routes/api.php (nhóm /assign/request-solutions, form-templates/snapshot)
      Http/Controllers/Api/V1/RequestSolutionController.php (pending, exportPending, receive, reject)
      Http/Controllers/Api/V1/FormTemplateController.php::storeAdditionalQuestions
      Services/RequestSolutionService.php (pending, receive, reject, calculate*)
      Http/Requests/RequestSolution/{RequestSolutionReceiveRequest,RequestSolutionRejectRequest}.php
      Entities/RequestSolution.php (STATUSES, isCanReceive, isCanReject)
      Transformers/RequestSolutionResource/RequestSolutionResource.php (getDeadlineStatus)
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 1007–1010, 1012)
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

OUT = os.path.join(HERE, 'SRS - Phê duyệt yêu cầu giải pháp.docx')
SHOTS = os.path.join(HERE, 'ycgp_pending_shots')

# 2 lối vào menu của CÙNG một màn (cùng phạm vi dữ liệu)
M1 = 'Phân hệ Công việc => Phê duyệt => Giải pháp - Dự án => Yêu cầu làm giải pháp'
M2 = 'Phân hệ Bán hàng => Phê Duyệt => Dự án TKT => Yêu cầu giải pháp chờ duyệt'

ACT = 'Người tiếp nhận yêu cầu làm giải pháp (Q1)'
TAC = 'Trưởng phòng / người phụ trách tiếp nhận yêu cầu làm giải pháp; Người dùng đã đăng nhập'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=M1, route='', full_url='', img_prefix='ycgp_pending_')

d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ Công việc': 'phanhe_cv', 'Phê duyệt': 'pheduyet_cv', 'Giải pháp - Dự án': 'gpda',
    'Yêu cầu làm giải pháp': 'ycgp_item',
    'Phân hệ Bán hàng': 'phanhe_bh', 'Phê Duyệt': 'pheduyet_bh', 'Dự án TKT': 'duantkt',
    'Yêu cầu giải pháp chờ duyệt': 'ycgp_cd',
    'Tìm kiếm nâng cao': 'timkiem', 'Cài đặt bộ lọc': 'caidat', 'Tuỳ chỉnh cột': 'cot',
    'Xuất Excel': 'xuat', 'Mã yêu cầu': 'xem', 'Tiếp nhận': 'tiepnhan',
    'Yêu cầu bổ sung thông tin': 'bosung', 'Thêm câu hỏi': 'themcauhoi',
    'Yêu cầu bổ sung': 'guibosung', 'Từ chối': 'tuchoi',
}.items()})


def layout2(suffix='', shot_name=None, caption=None, note=None, extra=()):
    """Mục Layout: ghi ĐỦ 2 lối vào menu (cùng màn, cùng phạm vi dữ liệu) + ảnh chụp thật."""
    d.p('Đường dẫn màn hình (2 lối vào, mở cùng một màn hình):')
    d._menu_para(M1 + suffix)
    d._menu_para(M2 + suffix)
    d.p('Hai lối vào hiển thị cùng một danh sách và cùng phạm vi dữ liệu (xem Phần 2).')
    if note:
        d.p(note)
    d.figure(shot(shot_name), caption, width_in=6.2)
    for name, cap in extra:
        d.figure(shot(name), cap, width_in=6.2)


d.title_block('Phê duyệt yêu cầu giải pháp')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phê duyệt yêu cầu làm giải pháp (danh sách '
    'yêu cầu làm giải pháp chờ tiếp nhận), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ phạm vi yêu cầu mà mỗi người tiếp nhận nhìn thấy (theo phòng tiếp nhận và hình thức '
    'triển khai của dự án tiền khả thi).',
    'Làm rõ 3 cách xử lý một yêu cầu đang chờ: Tiếp nhận, Yêu cầu bổ sung thông tin, Từ chối — '
    'điều kiện, dữ liệu phải nhập và kết quả sau xử lý.',
    'Làm rõ cách hệ thống tính hạn tiếp nhận và gắn nhãn Trong hạn / Sắp đến hạn / Quá hạn.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Yêu cầu làm giải pháp (YC)', 'Phiếu do nhân viên kinh doanh lập từ một dự án tiền khả thi, '
     'gửi sang phòng giải pháp để làm giải pháp kỹ thuật.'),
    ('GP', 'Giải pháp.'),
    ('Dự án TKT', 'Dự án tiền khả thi — dự án gốc của yêu cầu làm giải pháp.'),
    ('KD', 'Kinh doanh — người / phòng gửi yêu cầu.'),
    ('PM làm GP', 'Nhân viên được người tiếp nhận chỉ định chịu trách nhiệm làm giải pháp.'),
    ('Chờ tiếp nhận', 'Trạng thái của yêu cầu đã được gửi và đang chờ phòng giải pháp xử lý. Màn '
     'hình này chỉ hiển thị yêu cầu ở trạng thái này.'),
    ('Phòng tiếp nhận', 'Phòng giải pháp được chọn trên yêu cầu để nhận và xử lý yêu cầu.'),
    ('Hạn tiếp nhận', 'Thời điểm muộn nhất phòng giải pháp phải phản hồi yêu cầu (cột “Ngày cần tiếp '
     'nhận YC”).'),
    ('Phản hồi', 'Một trong 3 thao tác Tiếp nhận, Yêu cầu bổ sung thông tin, Từ chối. Sau khi phản '
     'hồi, yêu cầu rời khỏi màn hình này.'),
    ('Phiếu thu thập thông tin', 'Bộ câu hỏi khảo sát gắn với dự án TKT; người tiếp nhận thêm câu '
     'hỏi vào mục “Thông tin bổ sung” của phiếu khi cần kinh doanh bổ sung thông tin.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Tiếp nhận yêu cầu làm giải pháp',
     'Hiện mục menu và cho vào màn hình; xem danh sách, tìm kiếm, lọc, tuỳ chỉnh cột, xuất Excel, '
     'xem chi tiết; được Tiếp nhận, Yêu cầu bổ sung thông tin và Từ chối yêu cầu.'),
], widths=[0.8, 2.0, 3.2])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem danh sách yêu cầu làm giải pháp theo tổng công ty',
     'Hiện đủ 3 ô lọc Công ty, Phòng ban, Bộ phận trong khối Tìm kiếm nâng cao.'),
    ('V2', 'Xem danh sách yêu cầu làm giải pháp theo công ty', 'Hiện ô lọc Phòng ban và Bộ phận.'),
    ('V3', 'Xem danh sách yêu cầu làm giải pháp theo phòng ban', 'Hiện ô lọc Phòng ban và Bộ phận.'),
    ('V4', 'Xem danh sách yêu cầu làm giải pháp theo bộ phận', 'Hiện ô lọc Bộ phận.'),
], widths=[0.8, 2.6, 2.6])
d.p('Lưu ý: V1–V4 chỉ quyết định ô lọc theo đơn vị nào được hiển thị, KHÔNG mở rộng dữ liệu. Phạm vi '
    'yêu cầu thực sự hiển thị luôn do hệ thống tính theo phòng tiếp nhận của yêu cầu:')
d.bullets([
    'Dự án TKT triển khai Liên phòng ban (hoặc dự án cũ chưa khai hình thức triển khai): yêu cầu có '
    'phòng tiếp nhận thuộc các phòng người dùng được giao quản lý hoặc chính phòng của người dùng.',
    'Dự án TKT triển khai Theo phòng: yêu cầu có phòng tiếp nhận đúng bằng phòng của người dùng.',
    'Dự án TKT Tự triển khai không phát sinh yêu cầu làm giải pháp.',
])

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách yêu cầu chờ tiếp nhận', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '❌'),
    ('FR-03 Cài đặt bộ lọc', '✅', '❌'),
    ('FR-04 Tuỳ chỉnh cột', '✅', '❌'),
    ('FR-05 Xuất Excel', '✅', '❌'),
    ('FR-06 Xem chi tiết yêu cầu', '✅', '❌'),
    ('FR-07 Tiếp nhận yêu cầu', '✅', '❌'),
    ('FR-08 Yêu cầu bổ sung thông tin', '✅', '❌'),
    ('FR-09 Từ chối yêu cầu', '✅', '❌'),
], widths=[3.6, 1.0, 1.4])
d.p('Người dùng thiếu Q1 mở màn hình (kể cả qua lối vào ở phân hệ Bán hàng hoặc gõ thẳng đường dẫn) → '
    'hệ thống chuyển sang trang “Không tìm thấy trang yêu cầu – Không tìm thấy hoặc không được cấp quyền '
    'truy cập trang”.')

# ================================================================ PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACT, [0, 1, 2, 3, 4])],
    [('FR-01', 'Xem danh sách yêu cầu chờ tiếp nhận', 'view'),
     ('FR-05', 'Xuất Excel', 'io'),
     ('FR-07', 'Tiếp nhận yêu cầu', 'action'),
     ('FR-08', 'Yêu cầu bổ sung thông tin', 'action'),
     ('FR-09', 'Từ chối yêu cầu', 'action')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết yêu cầu', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Phê duyệt yêu cầu giải pháp')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách yêu cầu chờ tiếp nhận')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của màn Phê duyệt yêu cầu giải pháp tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách yêu cầu làm giải pháp chờ tiếp nhận',
    mota='Hiển thị hàng đợi các yêu cầu làm giải pháp đang ở trạng thái Chờ tiếp nhận thuộc phạm vi '
         'phòng của người dùng, kèm nhãn hạn xử lý, để người tiếp nhận phản hồi kịp hạn.',
    tacnhan=TAC,
    dieukien='Người dùng đã đăng nhập và có quyền Q1.',
    chinh='1. Hệ thống nạp trang 1, 10 dòng/trang, yêu cầu mới tạo lên đầu.\n'
          '2. Bảng hiển thị đủ các cột (mặc định hiện hết), dòng “Hiển thị a–b / N” và thanh phân trang.\n'
          '3. Dưới Tên yêu cầu hiển thị nhãn hạn: Trong hạn (xanh), Sắp đến hạn (cam), Quá hạn (đỏ).\n'
          '4. Cột Hành động có 2 nút: Tiếp nhận và Yêu cầu bổ sung thông tin.',
    phu='• Không có yêu cầu nào trong phạm vi → bảng hiện “Không có yêu cầu chờ duyệt.”\n'
        '• Bấm tiêu đề cột có biểu tượng sắp xếp → sắp xếp tăng / giảm theo cột đó.\n'
        '• Vào lại màn trong vòng 10 phút sau khi rời đi → hệ thống khôi phục bộ lọc đã dùng.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.\n'
        '• Yêu cầu đã được phản hồi (Tiếp nhận / Yêu cầu bổ sung / Từ chối) → không còn hiển thị.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
layout2('', '01-danh-sach.png', 'Màn danh sách yêu cầu làm giải pháp chờ duyệt lúc mới truy cập',
        extra=[('01b-danh-sach-hanh-dong.png', 'Phần bên phải bảng: cột Tiến trình YC và cột Hành động'),
               ('00-menu-cong-viec.png', 'Lối vào 1: Phân hệ Công việc → Phê duyệt → Giải pháp - Dự án'),
               ('00b-menu-ban-hang.png', 'Lối vào 2: Phân hệ Bán hàng → Phê Duyệt → Dự án TKT')])
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Yêu cầu làm giải pháp chờ duyệt”', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Tiêu đề cố định phía trên bảng.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Chọn trường xuất file (FR-05).'),
    ('Nút Tuỳ chỉnh cột (biểu tượng cột)', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-04).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự', 'Đánh số liên tục qua các trang; cố định khi '
     'cuộn ngang.'),
    ('Cột Mã yêu cầu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Là liên kết mở màn Chi tiết (FR-06); sắp xếp được; cố định khi cuộn ngang.'),
    ('Cột Tên yêu cầu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tối đa 2 dòng. Dòng dưới là nhãn hạn: Trong hạn / Sắp đến hạn / Quá hạn (màu do hệ thống trả). '
     'Sắp xếp được.'),
    ('Cột Dự án TKT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '“Mã dự án - Tên dự án”.'),
    ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '“Mã khách hàng - Tên khách hàng”.'),
    ('Cột Giai đoạn dự án', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tên giai đoạn của yêu cầu.'),
    ('Cột Mức độ ưu tiên', 'Badge', 'Read-only', '–', 'Theo dữ liệu',
     'Mức độ ưu tiên của giai đoạn dự án, màu theo danh mục mức độ ưu tiên.'),
    ('Cột Ngày gửi YC', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
     'Dòng dưới là giờ gửi (hh:mm:ss). Sắp xếp được.'),
    ('Cột Ngày cần tiếp nhận YC', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
     'Hạn tiếp nhận; dòng dưới là giờ. Sắp xếp được.'),
    ('Cột Ngày chốt GP', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Sắp xếp được.'),
    ('Cột Ngày KH cần GP', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Sắp xếp được.'),
    ('Cột Phòng KD', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Phòng của người gửi yêu cầu.'),
    ('Cột Phòng tiếp nhận YC', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Phòng giải pháp nhận yêu cầu.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Ngày tạo sắp xếp được (mặc định giảm dần).'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Ngày cập nhật sắp xếp được.'),
    ('Cột Tiến trình YC', 'Badge', 'Read-only', '–', 'Chờ tiếp nhận', 'Trạng thái yêu cầu, màu cam.'),
    ('Nút Tiếp nhận (biểu tượng hộp thư)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Mở cửa sổ Tiếp nhận (FR-07). Chỉ hiện khi người dùng được phép tiếp nhận yêu cầu đó.'),
    ('Nút Yêu cầu bổ sung thông tin (biểu tượng tệp +)', 'Icon Button', 'Enable / Ẩn', '–', 'Theo dữ liệu',
     'Mở màn Chi tiết tại tab Phiếu thu thập thông tin (FR-08). Cùng điều kiện hiện với nút Tiếp nhận.'),
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả', 'N là tổng số yêu cầu khớp bộ lọc.'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách', '10', 'Đổi thì quay về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Về đầu / lùi / số trang / tiến / về cuối.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có yêu cầu chờ duyệt.”'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Hiển thị', 'Hiện trong lúc nạp dữ liệu.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền Q1.\n– Không có quyền → chuyển sang trang “Không tìm thấy trang yêu cầu – '
     'Không tìm thấy hoặc không được cấp quyền truy cập trang”.\n'
     'During:\n– Khôi phục bộ lọc đã lưu (nếu rời màn chưa quá 10 phút).\n'
     '– Lấy yêu cầu đang Chờ tiếp nhận trong phạm vi phòng tiếp nhận của người dùng (Phần 2).\n'
     'After:\n– Hiển thị trang 1, 10 dòng, yêu cầu mới tạo lên đầu; tính nhãn hạn cho từng dòng.'),
    ('Bấm tiêu đề cột sắp xếp được', 'Click',
     'After:\n– Sắp xếp theo cột đó, bấm lại để đảo chiều; quay về trang 1.'),
    ('Bấm số trang / đổi Số dòng/trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\n'
     'After:\n– Nạp lại dữ liệu; đổi số dòng/trang thì quay về trang 1.'),
    ('Bấm Mã yêu cầu', 'Click', 'After:\n– Mở màn Chi tiết yêu cầu (FR-06).'),
    ('Bấm nút Tiếp nhận / Yêu cầu bổ sung thông tin', 'Click',
     'After:\n– Thực hiện FR-07 / FR-08.'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Phê duyệt '
           'yêu cầu giải pháp tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc yêu cầu chờ tiếp nhận',
    mota='Tìm nhanh theo mã / tên yêu cầu và lọc nâng cao theo đơn vị người gửi, nhân viên gửi, giai '
         'đoạn dự án, khoảng ngày tạo — luôn trong phạm vi yêu cầu Chờ tiếp nhận của người dùng.',
    tacnhan=TAC,
    dieukien='Đang ở màn danh sách; có quyền Q1.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc và chọn điều kiện.\n'
          '3. Đổi một ô chọn trong khối lọc → hệ thống tự lọc lại ngay, không cần bấm Tìm kiếm.\n'
          '4. Bảng hiển thị kết quả từ trang 1.',
    phu='• Bấm Làm mới → xóa mọi điều kiện (kể cả ô tìm nhanh), nạp lại danh sách từ trang 1.\n'
        '• Đổi Công ty / Phòng ban → các ô cấp dưới đã chọn bị xóa.\n'
        '• Không có kết quả → “Không có yêu cầu chờ duyệt.”\n'
        '• Bấm “Ẩn tìm kiếm nâng cao” → thu gọn khối lọc, điều kiện đang chọn vẫn giữ.',
    dacbiet=None)
d.p('2.2.2 Layout màn hình')
layout2(' => Tìm kiếm nâng cao', '02-bo-loc.png', 'Khối Tìm kiếm nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Placeholder “Tìm theo mã yêu cầu, tên yêu cầu”. Tìm gần đúng theo Mã hoặc Tên yêu cầu; chỉ áp '
     'dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (FR-03).'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Trống',
     'Chỉ hiện với quyền V1. Lọc theo công ty của NGƯỜI GỬI yêu cầu.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Phòng ban của công ty đã chọn', 'Không', 'Trống',
     'Hiện với V1, V2, V3. Lọc theo phòng ban của người gửi.'),
    ('Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Bộ phận của phòng đã chọn', 'Không', 'Trống',
     'Hiện với V1–V4. Lọc theo bộ phận của người gửi.'),
    ('Nhân viên gửi yêu cầu', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc đúng theo người tạo yêu cầu. Hiển thị “Tên - Mã phòng - Mã nhân viên”.'),
    ('Giai đoạn dự án', 'Dropdown', 'Enable', 'Danh sách giai đoạn dự án', 'Không', 'Trống',
     'Có icon ⓘ mô tả giai đoạn. Giai đoạn đã khóa đang được lọc vẫn hiển thị kèm 🔒.'),
    ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy → dd/mm/yyyy', 'Không', 'Trống',
     'Một ô chọn khoảng ngày; lọc ngày tạo yêu cầu trong khoảng (tính cả 2 đầu).'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm / Enter ở ô tìm nhanh', 'Click / Keypress',
     'After:\n– Lọc gần đúng theo Mã hoặc Tên yêu cầu kết hợp các điều kiện lọc nâng cao; hiển thị '
     'trang 1.'),
    ('Đổi giá trị một ô lọc nâng cao', 'Change',
     'After:\n– Tự lọc lại ngay theo toàn bộ điều kiện đang chọn, quay về trang 1.\n'
     '– Lưu bộ lọc để khôi phục khi quay lại màn trong 10 phút.'),
    ('Bấm Làm mới', 'Click',
     'After:\n– Xóa mọi điều kiện, trả sắp xếp về Ngày tạo giảm dần, nạp lại trang 1 (1 lần).'),
])

# ---------------------------------------------------------------- 2.3
d.h3('2.3 Cài đặt bộ lọc')
d.p('2.3.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Phê duyệt '
           'yêu cầu giải pháp tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc',
    mota='Cho người dùng chọn tiêu chí lọc nào được hiển thị trong khối Tìm kiếm nâng cao và sắp xếp '
         'thứ tự các tiêu chí. Cài đặt lưu riêng cho màn này.',
    tacnhan=TAC,
    dieukien='Đang ở màn danh sách; có quyền Q1.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc”.\n'
          '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 4 tiêu chí kèm ô tích.\n'
          '3. Người dùng tích / bỏ tích, kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Bấm Lưu → hệ thống lưu cấu hình, thông báo “Cập nhật thành công”, khối lọc cập nhật theo.',
    phu='• Bấm Khôi phục mặc định → tích lại đủ 4 tiêu chí theo thứ tự gốc; phải bấm Lưu mới ghi nhận.\n'
        '• Bấm Đóng / dấu × → không lưu thay đổi.\n'
        '• Bỏ tích một tiêu chí đang có giá trị lọc → giá trị đó bị xóa khỏi bộ lọc.\n'
        '• Lỗi khi lưu → “Thao tác thất bại”.',
    dacbiet=None)
d.p('2.3.2 Layout màn hình')
layout2(' => Cài đặt bộ lọc', '03-cai-dat-bo-loc.png', 'Cửa sổ Cài đặt bộ lọc',
        note='Cửa sổ Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.')
d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Cài đặt bộ lọc”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     'Kèm dòng hướng dẫn “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu '
     'theo từng màn hình.”'),
    ('Tiêu chí Công ty – Phòng ban – Bộ phận', 'Checkbox', 'Enable', '–', 'Không', 'Tích', 'Kéo thả được.'),
    ('Tiêu chí Nhân viên gửi yêu cầu', 'Checkbox', 'Enable', '–', 'Không', 'Tích', 'Kéo thả được.'),
    ('Tiêu chí Giai đoạn dự án', 'Checkbox', 'Enable', '–', 'Không', 'Tích', 'Kéo thả được.'),
    ('Tiêu chí Ngày tạo', 'Checkbox', 'Enable', '–', 'Không', 'Tích', 'Kéo thả được.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình và đóng cửa sổ.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đưa về cấu hình gốc (chưa lưu).'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
])
d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc', 'Click', 'After:\n– Mở cửa sổ với cấu hình đang áp dụng.'),
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi cấu hình tiêu chí (bật/tắt, thứ tự) cho riêng người dùng và màn này.\n'
     'After:\n– Thông báo “Cập nhật thành công”, khối lọc hiển thị theo cấu hình mới.\n'
     '– Lỗi → “Thao tác thất bại”.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Tích lại đủ 4 tiêu chí theo thứ tự gốc trong cửa sổ.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ---------------------------------------------------------------- 2.4
d.h3('2.4 Tuỳ chỉnh cột')
d.p('2.4.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các quy tắc '
           'riêng của màn Phê duyệt yêu cầu giải pháp tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Tuỳ chỉnh cột hiển thị',
    mota='Cho người dùng ẩn / hiện và đổi thứ tự các cột của bảng. Cấu hình lưu riêng cho màn này, '
         'không ảnh hưởng màn Yêu cầu làm giải pháp.',
    tacnhan=TAC,
    dieukien='Đang ở màn danh sách; có quyền Q1.',
    chinh='1. Người dùng bấm nút Tuỳ chỉnh cột (biểu tượng cột, góc phải phía trên bảng).\n'
          '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê các cột kèm ô tích.\n'
          '3. Người dùng tích / bỏ tích, kéo biểu tượng ☰ để đổi vị trí.\n'
          '4. Bấm Lưu → bảng hiển thị theo cấu hình mới, thông báo “Cập nhật thành công”.',
    phu='• Cột STT, Mã yêu cầu, Hành động bị khóa: không bỏ tích, không kéo đổi vị trí được (hiện ổ khóa).\n'
        '• Bấm Đóng / dấu × → không lưu, danh sách cột trở về cấu hình đang áp dụng.\n'
        '• Lỗi khi lưu → “Thao tác thất bại”.',
    dacbiet=None)
d.p('2.4.2 Layout màn hình')
layout2(' => Tuỳ chỉnh cột', '04-tuy-chinh-cot.png', 'Cửa sổ Tuỳ chỉnh cột',
        note='Cửa sổ Tuỳ chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.')
d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Tuỳ chỉnh cột”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Dòng cột STT, Mã yêu cầu, Hành động', 'Checkbox', 'Disable', '–', '–', 'Tích',
     'Cột bắt buộc, có biểu tượng ổ khóa, không ẩn / không đổi vị trí được.'),
    ('Dòng các cột còn lại (Tên yêu cầu … Tiến trình YC)', 'Checkbox', 'Enable', '16 cột', 'Không',
     'Tích (mặc định hiện hết)', 'Bỏ tích để ẩn cột; kéo ☰ để đổi vị trí.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình và đóng cửa sổ.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu.'),
])
d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tuỳ chỉnh cột', 'Click', 'After:\n– Mở cửa sổ với cấu hình cột đang áp dụng.'),
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi cấu hình cột cho người dùng, khóa riêng của màn chờ duyệt.\n'
     'After:\n– Bảng hiển thị theo cấu hình mới; thông báo “Cập nhật thành công”.\n'
     '– Lỗi → “Thao tác thất bại”.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, trả danh sách cột về cấu hình đang áp dụng.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Xuất Excel')
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Xuất Excel', 'io', actor=ACT, caption='Biểu đồ Use Case — FR-05 Xuất Excel')
d.p('2.5.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách yêu cầu chờ tiếp nhận',
    mota='Tải về tệp yeu_cau_lam_giai_phap_cho_duyet.xlsx gồm TẤT CẢ yêu cầu khớp bộ lọc đang áp dụng '
         '(không giới hạn theo trang), với các cột người dùng chọn.',
    tacnhan=TAC,
    dieukien='Đang ở màn danh sách; có quyền Q1.',
    chinh='1. Người dùng (tuỳ chọn) đặt bộ lọc trên màn danh sách.\n'
          '2. Bấm Xuất Excel → hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn các cột đang hiện trên '
          'bảng.\n'
          '3. Người dùng tích / bỏ tích trường, kéo ☰ để đổi thứ tự cột trong tệp.\n'
          '4. Bấm Xuất file → hệ thống dựng tệp, trình duyệt tải về, thông báo “Xuất Excel thành công”.',
    phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích toàn bộ trường.\n'
        '• Không chọn trường nào → nút Xuất file bị khóa.\n'
        '• Lỗi khi dựng tệp → thông báo “Lỗi khi xuất Excel”, không tải tệp.',
    dacbiet='Tệp có tiêu đề “Danh sách yêu cầu làm giải pháp chờ duyệt”; thứ tự cột theo thứ tự trong '
            'cửa sổ chọn trường. Trong lúc đang xuất, nút Xuất Excel bị khóa để tránh bấm lặp.')
d.p('2.5.3 Layout màn hình')
layout2(' => Xuất Excel', '05-xuat-excel.png', 'Cửa sổ Chọn trường xuất file',
        note='Cửa sổ Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.')
d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Chọn trường xuất file”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     'Kèm hướng dẫn “Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file.”'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích / bỏ tích mọi trường.'),
    ('Danh sách trường', 'Checkbox', 'Enable', '19 trường', 'Có (≥ 1)', 'Tích sẵn các cột đang hiện',
     'Xếp các cột đang hiện lên đầu theo thứ tự trên bảng: Mã yêu cầu, Tên yêu cầu, Tên dự án TKT, Tên '
     'khách hàng, Giai đoạn dự án, Mức độ ưu tiên, Ngày gửi yêu cầu, Ngày cần tiếp nhận, Ngày chốt giải '
     'pháp, Ngày KH cần giải pháp, Phòng kinh doanh, Phòng tiếp nhận, Người tạo, Ngày tạo, Người cập '
     'nhật, Ngày cập nhật, Tiến trình yêu cầu (17 trường, tích sẵn); tiếp theo là Mã dự án TKT, Mã khách '
     'hàng (không tích sẵn). Kéo ☰ để đổi thứ tự.'),
    ('Dòng “Đang chọn x/y trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', 'Đếm số trường đang tích.'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Khóa khi chưa chọn trường nào hoặc đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
])
d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click', 'After:\n– Mở cửa sổ Chọn trường xuất file, tích sẵn các cột đang hiện.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Q1; không có quyền → tệp không có dòng dữ liệu nào.\n'
     'During:\n– Lấy toàn bộ yêu cầu Chờ tiếp nhận trong phạm vi người dùng, theo bộ lọc và thứ tự sắp '
     'xếp đang áp dụng (bỏ qua phân trang).\n– Chỉ xuất các trường đã chọn, theo thứ tự đã kéo.\n'
     'After:\n– Tải tệp yeu_cau_lam_giai_phap_cho_duyet.xlsx; thông báo “Xuất Excel thành công”.\n'
     '– Lỗi → “Lỗi khi xuất Excel”.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xem chi tiết yêu cầu')
d.p('2.6.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết yêu cầu làm giải pháp',
    mota='Xem toàn bộ thông tin của một yêu cầu ở chế độ chỉ đọc (thông tin yêu cầu, dự án TKT, '
         'meetings, phiếu thu thập thông tin, lịch sử) trước khi quyết định xử lý.',
    tacnhan=TAC,
    dieukien='Có quyền Q1; yêu cầu đang hiển thị trên màn danh sách chờ duyệt.',
    chinh='1. Người dùng bấm Mã yêu cầu trên dòng (chuột phải để mở tab mới).\n'
          '2. Hệ thống mở màn “Chi tiết yêu cầu giải pháp: <Mã> (<Trạng thái>)” ở tab Thông tin yêu cầu.\n'
          '3. Người dùng chuyển giữa các tab Thông tin yêu cầu, Dự án tiền khả thi, Meetings, Phiếu thu '
          'thập thông tin; mở mục Lịch sử (bấm Xem lịch sử) nếu cần.\n'
          '4. Chân trang hiển thị các nút xử lý Tiếp nhận, Từ chối và nút Quay lại.',
    phu='• Tab Phiếu thu thập thông tin chỉ hiện khi người dùng được phép tiếp nhận yêu cầu.\n'
        '• Mục Lịch sử thu gọn mặc định, chỉ nạp dữ liệu khi người dùng mở.\n'
        '• Bấm Quay lại → trở về màn trước đó.',
    dacbiet=None)
d.p('2.6.2 Layout màn hình')
layout2(' => Mã yêu cầu', '07-chi-tiet.png', 'Màn Chi tiết yêu cầu — tab Thông tin yêu cầu')
d.p('2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Chi tiết yêu cầu giải pháp: <Mã> (<Trạng thái>)”', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Trạng thái in nghiêng theo màu trạng thái.'),
    ('Thanh tab', 'Tab', 'Enable', '4 tab', 'Thông tin yêu cầu',
     'Thông tin yêu cầu · Dự án tiền khả thi · Meetings · Phiếu thu thập thông tin (chỉ khi được tiếp nhận).'),
    ('Tên yêu cầu', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Phòng tiếp nhận yêu cầu', 'Dropdown', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Ứng dụng / Nhóm ngành / Nhóm giải pháp', 'Textbox / Dropdown', 'Read-only', '–', 'Theo dữ liệu',
     'Ứng dụng kế thừa từ dự án TKT; có icon ⓘ mô tả.'),
    ('Giai đoạn dự án', 'Dropdown', 'Read-only', '–', 'Theo dữ liệu', 'Có icon ⓘ mô tả giai đoạn.'),
    ('Ngày KH cần giải pháp / Ngày KH cần báo giá / Ngày cần nhận GP nội bộ', 'Datepicker', 'Read-only',
     'dd/mm/yyyy', 'Theo dữ liệu', '–'),
    ('Hạn hoàn thành tiếp nhận', 'Textbox', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Chỉ hiện khi yêu cầu có hạn tiếp nhận.'),
    ('Mô tả / ghi chú yêu cầu', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Bảng File gửi kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'STT, Tên tài liệu, File đính kèm, '
     'Dung lượng; tải xuống được.'),
    ('Khối phòng kinh doanh', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Nhân viên KD chính và nhóm hỗ trợ.'),
    ('Mục Lịch sử', 'Section', 'Enable', '–', 'Thu gọn', 'Bấm “Xem lịch sử” để mở danh sách thay đổi.'),
    ('Nút Tiếp nhận', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu', 'Mở cửa sổ Tiếp nhận (FR-07). Cùng '
     'điều kiện với nút Tiếp nhận ở danh sách.'),
    ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Theo dữ liệu', 'Mở cửa sổ Xác nhận từ chối (FR-09).'),
    ('Nút Hủy yêu cầu làm giải pháp', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện với NGƯỜI TẠO yêu cầu khi chưa được tiếp nhận (thuộc SRS Yêu cầu làm giải pháp).'),
    ('Nút Sửa / Xóa', 'Button', 'Ẩn', '–', 'Ẩn', 'Chỉ hiện khi yêu cầu ở trạng thái Nháp hoặc Yêu cầu bổ '
     'sung — luôn ẩn với yêu cầu Chờ tiếp nhận.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Trở về màn trước đó.'),
], required=False)
d.p('2.6.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Mã yêu cầu', 'Click',
     'Before:\n– Kiểm tra quyền xem yêu cầu.\n' + NO_PERM + '\n'
     'After:\n– Mở màn chi tiết ở chế độ chỉ đọc, tab Thông tin yêu cầu.'),
    ('Bấm một tab', 'Click', 'After:\n– Hiển thị nội dung tab tương ứng.'),
    ('Bấm Xem lịch sử', 'Click', 'After:\n– Nạp và hiển thị lịch sử thay đổi của yêu cầu.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Trở về màn trước đó.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Tiếp nhận yêu cầu')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Tiếp nhận yêu cầu', 'action', actor=ACT,
            caption='Biểu đồ Use Case — FR-07 Tiếp nhận yêu cầu')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Tiếp nhận yêu cầu làm giải pháp',
    mota='Phòng giải pháp nhận yêu cầu, chỉ định PM làm giải pháp và ngày dự kiến xong giải pháp; yêu '
         'cầu chuyển sang trạng thái Đã tiếp nhận.',
    tacnhan=TAC,
    dieukien='Có quyền Q1; yêu cầu đang Chờ tiếp nhận và phòng tiếp nhận thuộc phạm vi của người dùng.',
    chinh='1. Người dùng bấm nút Tiếp nhận trên dòng (hoặc nút Tiếp nhận ở chân màn Chi tiết).\n'
          '2. Hệ thống mở cửa sổ “Tiếp nhận yêu cầu làm GP: <Mã> - <Tên>” gồm khối Thông tin tóm tắt '
          'yêu cầu (chỉ đọc) và khối Thông tin người tiếp nhận cần nhập.\n'
          '3. Người dùng chọn Ngày dự kiến xong GP (v1), chọn PM làm GP (SĐT PM tự điền), nhập Ghi chú '
          '(nếu có).\n'
          '4. Bấm Xác nhận tiếp nhận.\n'
          '5. Hệ thống kiểm tra dữ liệu, chuyển yêu cầu sang Đã tiếp nhận, thông báo “Thao tác thành công”.\n'
          '6. Mở từ danh sách: đóng cửa sổ, nạp lại danh sách (yêu cầu biến khỏi danh sách). Mở từ màn '
          'Chi tiết: chuyển về màn Yêu cầu làm giải pháp.',
    phu='• Thiếu Ngày dự kiến xong GP hoặc PM làm GP → báo “Bắt buộc phải nhập” dưới ô, thông báo “Lỗi '
        'khi tiếp nhận yêu cầu”.\n'
        '• Yêu cầu đã được người khác tiếp nhận / xử lý trước → “Phiếu đã được tiếp nhận, vui lòng tải lại '
        'dữ liệu”, đóng cửa sổ.\n'
        '• Bấm Đóng / dấu × → đóng cửa sổ, không lưu.',
    dacbiet='Ô Ngày dự kiến xong GP (v1) không cho chọn ngày sau Ngày KH cần GP của yêu cầu. Hai người '
            'bấm tiếp nhận cùng lúc thì chỉ người đầu tiên thành công.')
d.p('2.7.3 Layout màn hình')
layout2(' => Tiếp nhận', '06-tiep-nhan.png', 'Cửa sổ Tiếp nhận yêu cầu làm GP',
        note='Cửa sổ Tiếp nhận được mở ngay trên màn hình danh sách theo đường dẫn ở trên; cũng mở được '
             'bằng nút Tiếp nhận ở chân màn Chi tiết yêu cầu.')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Tiếp nhận yêu cầu làm GP: <Mã> - <Tên>”', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu', '–'),
    ('KD gửi yêu cầu', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', 'Người tạo yêu cầu.'),
    ('Ngày gửi yêu cầu', 'Label', 'Read-only', 'dd/mm/yyyy hh:mm', '–', 'Theo dữ liệu',
     'Hiển thị ngày giờ tạo yêu cầu.'),
    ('Tên dự án', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', 'Tên dự án TKT.'),
    ('Mã - Tên khách hàng', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '–'),
    ('Giai đoạn dự án', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '–'),
    ('Mức độ ưu tiên', 'Badge', 'Read-only', '–', '–', 'Theo dữ liệu', 'Màu theo danh mục mức độ ưu tiên.'),
    ('Ngày cần nhận GP nội bộ', 'Label', 'Read-only', 'dd/mm/yyyy', '–', 'Theo dữ liệu',
     'Hiện đang hiển thị giá trị Ngày KH cần giải pháp của yêu cầu.'),
    ('Phòng tiếp nhận', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '–'),
    ('Ngày cần tiếp nhận YC', 'Label', 'Read-only', 'dd/mm/yyyy', '–', 'Theo dữ liệu',
     'Hiện đang hiển thị giá trị Ngày cần nhận GP nội bộ của yêu cầu.'),
    ('Ngày dự kiến xong GP (v1)', 'Datepicker', 'Enable', 'dd/mm/yyyy, ≤ Ngày KH cần GP', 'Có', 'Trống',
     'Các ngày sau Ngày KH cần GP bị mờ, không chọn được.'),
    ('PM làm GP', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Có', 'Trống',
     'Placeholder “-- Chọn PM --”; không có nút xóa chọn.'),
    ('SĐT PM', 'Textbox', 'Disable', '–', 'Không', 'Trống', 'Tự điền theo số điện thoại của PM đã chọn.'),
    ('Ghi chú', 'Textarea', 'Enable', '0–1.000 ký tự', 'Không', 'Trống', '–'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Chữ đỏ ngay dưới ô bị lỗi.'),
    ('Nút Xác nhận tiếp nhận', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Khóa và hiện vòng quay trong lúc xử lý.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
])
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tiếp nhận', 'Click',
     'Before:\n– Nút chỉ hiện khi có quyền Q1, yêu cầu đang Chờ tiếp nhận và thuộc phạm vi phòng.\n'
     'After:\n– Mở cửa sổ với khối tóm tắt yêu cầu và form trống.'),
    ('Chọn PM làm GP', 'Change', 'After:\n– Tự điền SĐT PM theo nhân viên đã chọn.'),
    ('Bấm Xác nhận tiếp nhận', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Ngày dự kiến xong GP (v1) trống → “Bắt buộc phải nhập”; sai định dạng → “Ngày dự kiến '
     'xong GP không hợp lệ”.\n'
     '– PM làm GP trống → “Bắt buộc phải nhập”; không hợp lệ → “PM không hợp lệ”.\n'
     '– SĐT PM quá 20 ký tự → “Số điện thoại PM không được vượt quá 20 ký tự”.\n'
     '– Ghi chú quá 1.000 ký tự → “Ghi chú PM không được vượt quá 1000 ký tự”.\n'
     '– Có lỗi validate → thông báo “Lỗi khi tiếp nhận yêu cầu”, không thực hiện bước After.\n'
     '– Yêu cầu không còn ở trạng thái Chờ tiếp nhận → “Phiếu đã được tiếp nhận, vui lòng tải lại dữ '
     'liệu”, đóng cửa sổ.\n'
     'After:\n– Chuyển yêu cầu sang Đã tiếp nhận; ghi người tiếp nhận, PM làm GP, SĐT PM, Ghi chú, '
     'thời điểm phản hồi và kết quả phản hồi Trong hạn / Quá hạn; Ngày chốt GP của yêu cầu = Ngày dự kiến '
     'xong GP (v1) người dùng đã chọn.\n'
     '– Ghi lịch sử: 1 dòng đổi trạng thái + 1 dòng nội dung vừa nhập.\n'
     '– Thông báo “Thao tác thành công”; nạp lại danh sách (hoặc chuyển về màn Yêu cầu làm giải pháp '
     'nếu thao tác từ màn Chi tiết).'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, xóa dữ liệu đang nhập.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Yêu cầu bổ sung thông tin')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Yêu cầu bổ sung thông tin', 'action', actor=ACT,
            caption='Biểu đồ Use Case — FR-08 Yêu cầu bổ sung thông tin')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Yêu cầu bổ sung thông tin',
    mota='Khi thông tin trên yêu cầu chưa đủ để làm giải pháp, người tiếp nhận thêm câu hỏi vào mục '
         '“Thông tin bổ sung” của phiếu thu thập thông tin và gửi lại cho kinh doanh; yêu cầu chuyển sang '
         'trạng thái Yêu cầu bổ sung.',
    tacnhan=TAC,
    dieukien='Có quyền Q1; yêu cầu đang Chờ tiếp nhận, thuộc phạm vi phòng; dự án TKT đã có phiếu thu '
             'thập thông tin.',
    chinh='1. Người dùng bấm nút Yêu cầu bổ sung thông tin trên dòng → hệ thống mở màn Chi tiết tại tab '
          '“Phiếu thu thập thông tin”.\n'
          '2. Ở mục “Thông tin bổ sung” cuối phiếu, bấm “Thêm câu hỏi”.\n'
          '3. Nhập Nội dung câu hỏi, bấm Thêm (hoặc Enter) → câu hỏi vào danh sách chờ gửi.\n'
          '4. Lặp lại bước 2–3 nếu cần thêm câu hỏi.\n'
          '5. Bấm “Yêu cầu bổ sung”.\n'
          '6. Hệ thống lưu các câu hỏi mới, chuyển yêu cầu sang Yêu cầu bổ sung, thông báo “Đã lưu yêu cầu '
          'bổ sung câu hỏi thành công!”.',
    phu='• Bấm Hủy ở ô nhập câu hỏi → bỏ câu đang gõ.\n'
        '• Bấm biểu tượng thùng rác trên câu hỏi chưa gửi → xóa câu hỏi khỏi danh sách chờ gửi.\n'
        '• Dự án TKT chưa có phiếu thu thập → tab hiện “Chưa có phiếu thu thập thông tin cho dự án này”, '
        'không thêm được câu hỏi.\n'
        '• Lỗi khi gửi → “Có lỗi xảy ra khi gửi yêu cầu bổ sung!”.',
    dacbiet='Nút “Yêu cầu bổ sung” chỉ hiện khi đã có ít nhất 1 câu hỏi; chỉ các câu hỏi CHƯA gửi được '
            'gửi đi. Câu hỏi đã gửi không xóa được.')
d.p('2.8.3 Layout màn hình')
layout2(' => Yêu cầu bổ sung thông tin => Thêm câu hỏi => Yêu cầu bổ sung', '08-phieu-thu-thap.png',
        'Màn Chi tiết mở tại tab Phiếu thu thập thông tin',
        extra=[('08b-nhap-cau-hoi.png', 'Ô nhập nội dung câu hỏi bổ sung'),
               ('08c-cau-hoi-cho-gui.png', 'Câu hỏi chờ gửi và nút Yêu cầu bổ sung')])
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tab “Phiếu thu thập thông tin”', 'Tab', 'Enable / Ẩn', '–', '–', 'Được chọn sẵn',
     'Chỉ hiện khi người dùng được phép tiếp nhận yêu cầu.'),
    ('Nút Lịch sử thay đổi', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xem lịch sử thay đổi của phiếu.'),
    ('Nút Lưu phiếu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu câu trả lời của phiếu (chức năng của dự án TKT).'),
    ('Nút Xem mẫu in', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xem bản in của phiếu.'),
    ('Các mục câu hỏi của phiếu', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', 'Nội dung phiếu thu thập.'),
    ('Mục “Thông tin bổ sung”', 'Section', 'Hiển thị', '–', '–', 'Hiển thị',
     'Mục cuối phiếu, chứa các câu hỏi bổ sung đã gửi và đang chờ gửi.'),
    ('Nút Thêm câu hỏi', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở ô nhập câu hỏi.'),
    ('Nội dung câu hỏi', 'Textbox', 'Enable', '–', 'Có', 'Trống', 'Placeholder “Nhập nội dung câu hỏi...”.'),
    ('Nút Thêm', 'Button', 'Enable / Disable', '–', '–', 'Disable khi ô trống', 'Đưa câu hỏi vào danh sách chờ gửi.'),
    ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng ô nhập, bỏ nội dung đang gõ.'),
    ('Danh sách câu hỏi bổ sung', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Đánh số; mỗi câu có ô “Nhập câu trả lời...” để kinh doanh trả lời.'),
    ('Nút xóa câu hỏi (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo dữ liệu',
     'Chỉ hiện với câu hỏi chưa gửi.'),
    ('Nút Yêu cầu bổ sung', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi chưa có câu hỏi',
     'Gửi các câu hỏi mới; khóa và hiện vòng quay trong lúc gửi.'),
])
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Yêu cầu bổ sung thông tin trên dòng', 'Click',
     'Before:\n– Nút chỉ hiện khi có quyền Q1, yêu cầu đang Chờ tiếp nhận và thuộc phạm vi phòng.\n'
     'After:\n– Mở màn Chi tiết, chọn sẵn tab Phiếu thu thập thông tin.'),
    ('Bấm Thêm / Enter ở ô câu hỏi', 'Click / Keypress',
     'During:\n– Nội dung trống (chỉ khoảng trắng) → không thêm.\n'
     'After:\n– Thêm câu hỏi vào danh sách chờ gửi, đóng ô nhập.'),
    ('Bấm nút xóa câu hỏi', 'Click', 'After:\n– Xóa câu hỏi chưa gửi khỏi danh sách.'),
    ('Bấm Yêu cầu bổ sung', 'Click',
     'Before:\n– Chỉ gửi các câu hỏi chưa gửi; không có câu hỏi mới → không xử lý.\n'
     'During:\n– Không tìm thấy phiếu / yêu cầu → “Có lỗi xảy ra khi gửi yêu cầu bổ sung!”.\n'
     'After:\n– Lưu câu hỏi vào mục “Thông tin bổ sung” của phiếu (tạo mục nếu chưa có); ghi lịch sử '
     'phiếu thu thập (thêm câu hỏi).\n'
     '– Chuyển yêu cầu sang Yêu cầu bổ sung; ghi thời điểm phản hồi và kết quả Trong hạn / Quá hạn.\n'
     '– Dự án TKT đang ở bước “Chờ tiếp nhận làm giải pháp” → quay về “Thu thập thông tin dự án”.\n'
     '– Gửi thông báo cho người tạo yêu cầu: “Bạn có yêu cầu bổ sung câu hỏi mới của yêu cầu làm giải '
     'pháp: <Mã> - <Tên>”.\n'
     '– Thông báo “Đã lưu yêu cầu bổ sung câu hỏi thành công!”, nạp lại phiếu.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Từ chối yêu cầu')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Từ chối yêu cầu', 'action', actor=ACT,
            caption='Biểu đồ Use Case — FR-09 Từ chối yêu cầu')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa và Thông báo.', anchor='history')
d.intro_table(
    ten='Từ chối yêu cầu làm giải pháp',
    mota='Phòng giải pháp không nhận làm giải pháp cho yêu cầu, bắt buộc ghi lý do; yêu cầu chuyển '
         'sang Từ chối và dự án TKT quay về bước thu thập thông tin.',
    tacnhan=TAC,
    dieukien='Có quyền Q1; yêu cầu đang Chờ tiếp nhận và thuộc phạm vi phòng; đang ở màn Chi tiết.',
    chinh='1. Người dùng mở Chi tiết yêu cầu (FR-06), bấm nút Từ chối ở chân màn.\n'
          '2. Hệ thống mở cửa sổ “Xác nhận từ chối”.\n'
          '3. Người dùng nhập Lý do từ chối, bấm Đồng ý.\n'
          '4. Hệ thống chuyển yêu cầu sang Từ chối, thông báo “Từ chối yêu cầu thành công”, đóng cửa sổ và '
          'nạp lại màn Chi tiết (hiện Lý do từ chối, ẩn các nút xử lý).',
    phu='• Bỏ trống lý do → “Vui lòng nhập lý do từ chối” dưới ô.\n'
        '• Yêu cầu đã được người khác xử lý trước → “Phiếu đã được xử lý, vui lòng tải lại dữ liệu”.\n'
        '• Bấm Không / dấu × → đóng cửa sổ, không đổi dữ liệu.',
    dacbiet='Nút Từ chối chỉ có ở màn Chi tiết (không đặt ở danh sách) để người xử lý đọc nội dung trước '
            'khi từ chối.')
d.p('2.9.3 Layout màn hình')
layout2(' => Mã yêu cầu => Từ chối', '09-tu-choi.png', 'Cửa sổ Xác nhận từ chối',
        note='Cửa sổ Xác nhận từ chối được mở ngay trên màn Chi tiết yêu cầu.')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận từ chối”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–'),
    ('Lý do từ chối', 'Textarea', 'Enable', '1–1.000 ký tự', 'Có', 'Trống',
     'Placeholder “Nhập lý do từ chối”.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Chữ đỏ ngay dưới ô.'),
    ('Nút Đồng ý', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khóa trong lúc xử lý.'),
    ('Nút Không', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không từ chối.'),
])
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Từ chối', 'Click',
     'Before:\n– Nút chỉ hiện khi có quyền Q1, yêu cầu đang Chờ tiếp nhận và thuộc phạm vi phòng.\n'
     'After:\n– Mở cửa sổ Xác nhận từ chối với ô lý do trống.'),
    ('Bấm Đồng ý', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Lý do trống → “Vui lòng nhập lý do từ chối”; quá 1.000 ký tự → “Lý do từ chối không được '
     'vượt quá 1000 ký tự”.\n'
     '– Yêu cầu không còn Chờ tiếp nhận → “Phiếu đã được xử lý, vui lòng tải lại dữ liệu”.\n'
     '– Có lỗi → không thực hiện bước After.\n'
     'After:\n– Chuyển yêu cầu sang Từ chối; lưu lý do, người và thời điểm từ chối, kết quả phản hồi '
     'Trong hạn / Quá hạn.\n'
     '– Ghi lịch sử đổi trạng thái kèm lý do từ chối.\n'
     '– Dự án TKT quay về bước “Thu thập thông tin dự án”.\n'
     '– Gửi thông báo cho người tạo yêu cầu: “[YCG] Từ chối: <Tên yêu cầu>. Lý do: <lý do>”.\n'
     '– Thông báo “Từ chối yêu cầu thành công”, nạp lại màn Chi tiết.'),
    ('Bấm Không / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, không thay đổi dữ liệu.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phê duyệt yêu cầu giải pháp; không lặp lại các '
           'quy tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Màn hình là hàng đợi Chờ tiếp nhận', [
        '– Chỉ hiển thị yêu cầu ở trạng thái Chờ tiếp nhận.',
        '– Sau khi Tiếp nhận / Yêu cầu bổ sung / Từ chối, yêu cầu rời khỏi màn; kinh doanh gửi lại sau '
        'khi bổ sung thì yêu cầu xuất hiện lại.',
    ], ['Xem danh sách', 'Xuất Excel']),
    ('BR-02', 'Phạm vi dữ liệu theo phòng tiếp nhận', [
        '– Dự án Liên phòng ban (hoặc chưa khai hình thức): phòng tiếp nhận thuộc các phòng người dùng '
        'quản lý hoặc phòng của chính người dùng.',
        '– Dự án Triển khai theo phòng: phòng tiếp nhận = phòng của người dùng.',
        '– Quyền V1–V4 chỉ quyết định ô lọc đơn vị, không mở rộng dữ liệu.',
    ], ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),
    ('BR-03', 'Điều kiện được xử lý yêu cầu', [
        '– Có quyền Tiếp nhận yêu cầu làm giải pháp, yêu cầu đang Chờ tiếp nhận và phòng tiếp nhận '
        'thuộc phòng người dùng quản lý hoặc phòng của người dùng.',
        '– Không thỏa → ẩn nút Tiếp nhận, Yêu cầu bổ sung thông tin, Từ chối và tab Phiếu thu thập '
        'thông tin.',
    ], ['Tiếp nhận', 'Yêu cầu bổ sung', 'Từ chối', 'Xem chi tiết']),
    ('BR-04', 'Hạn tiếp nhận', [
        '– Hạn = ngày gửi yêu cầu + số ngày và số giờ phản hồi của Mức độ ưu tiên (theo Giai đoạn dự án).',
        '– Chỉ đếm ngày làm việc theo lịch phân ca của trưởng phòng tiếp nhận, bỏ qua ngày nghỉ lễ.',
        '– Kinh doanh gửi lại yêu cầu sau khi bổ sung → tính lại hạn từ lần gửi mới.',
    ], ['Xem danh sách']),
    ('BR-05', 'Nhãn hạn xử lý', [
        '– Quá hạn (đỏ): đã qua hạn tiếp nhận.',
        '– Sắp đến hạn (cam): đã tới mốc lùi 1 ngày làm việc trước hạn, hoặc hệ thống đã gửi cảnh báo '
        'sắp đến hạn.',
        '– Trong hạn (xanh): các trường hợp còn lại.',
    ], ['Xem danh sách']),
    ('BR-06', 'Chốt kết quả phản hồi', [
        '– Khi Tiếp nhận / Yêu cầu bổ sung / Từ chối, hệ thống ghi thời điểm phản hồi và chốt kết quả '
        'Trong hạn (phản hồi ≤ hạn) hoặc Quá hạn — dùng cho báo cáo hiệu suất.',
        '– Sau khi phản hồi, nhãn hạn hiển thị “Đã xử lý (Trong hạn)” / “Đã xử lý (Quá hạn)”.',
    ], ['Tiếp nhận', 'Yêu cầu bổ sung', 'Từ chối']),
    ('BR-07', 'Chống xử lý trùng', [
        '– Hai người cùng xử lý một yêu cầu: chỉ người đầu tiên thành công; người sau nhận thông báo '
        'yêu cầu đã được tiếp nhận / đã được xử lý và phải tải lại.',
    ], ['Tiếp nhận', 'Từ chối']),
    ('BR-08', 'Dữ liệu tiếp nhận', [
        '– Bắt buộc Ngày dự kiến xong GP (v1) và PM làm GP; Ghi chú tối đa 1.000 ký tự.',
        '– Ngày dự kiến xong GP không được sau Ngày KH cần GP (áp dụng cả khi tiếp nhận từ màn Chi tiết).',
        '– Ngày dự kiến xong GP được lưu làm Ngày chốt GP của yêu cầu.',
        '– SĐT PM tự lấy theo PM đã chọn.',
    ], ['Tiếp nhận']),
    ('BR-09', 'Yêu cầu bổ sung thông tin', [
        '– Chỉ thực hiện được khi dự án TKT đã có phiếu thu thập thông tin.',
        '– Câu hỏi bổ sung được thêm vào mục “Thông tin bổ sung” của phiếu; câu đã gửi không xóa được.',
        '– Yêu cầu chuyển sang Yêu cầu bổ sung; dự án TKT đang Chờ tiếp nhận làm giải pháp quay về '
        'Thu thập thông tin dự án; người tạo yêu cầu nhận thông báo.',
    ], ['Yêu cầu bổ sung']),
    ('BR-10', 'Từ chối yêu cầu', [
        '– Bắt buộc lý do, tối đa 1.000 ký tự; chỉ thực hiện ở màn Chi tiết.',
        '– Dự án TKT quay về Thu thập thông tin dự án; người tạo yêu cầu nhận thông báo kèm lý do.',
    ], ['Từ chối']),
    ('BR-11', 'Xuất Excel theo bộ lọc', [
        '– Xuất toàn bộ yêu cầu khớp bộ lọc và thứ tự sắp xếp hiện tại, không giới hạn theo trang.',
        '– Chỉ xuất các trường được chọn, theo thứ tự đã kéo.',
    ], ['Xuất Excel']),
])

d.save()
