# -*- coding: utf-8 -*-
"""Sinh "SRS - Danh mục nhóm ngành.docx" theo FORM CHUẨN (bản mẫu 2026-08-28).

Chạy:  python3 .plans/danh-muc-nhom-nganh/gen_srs.py
Thư viện dùng chung: .claude/skills/srs-documenter/assets/{srs_docx_lib,srs_uml_render}.py
Ảnh chụp thật (Playwright, 1440x900, bản nhánh `tpe`): nhom-nganh_shots/ — chỉ để local.

Nguồn đối chiếu code:
  FE  pages/assign/industry-groups/{index.vue, AddScopeModal.vue}
  BE  Modules/Assign/Routes/api.php (nhóm /assign/scopes) · Http/Requests/Scope/ScopeRequest.php
      Http/Controllers/Api/V1/ScopeController.php · Services/ScopeService.php
      Entities/Scope/Scope.php · resources/views/exports/scopes.blade.php
  Quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 983, 998)
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

OUT = os.path.join(HERE, 'SRS - Danh mục nhóm ngành.docx')
SHOTS = os.path.join(HERE, 'nhom-nganh_shots')
MENU = 'Phân hệ Dự án & Giao việc => Danh mục => Nhóm ngành'

A_QL = 'Người quản lý danh mục nhóm ngành (Q1)'
A_XEM = 'Người xem danh mục nhóm ngành (Q2)'

NO_PERM = ('– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
           'và dừng xử lý.')


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route='/assign/industry-groups',
           full_url='https://<host-hrm>/assign/industry-groups', img_prefix='nhomnganh_')


# Icon cho từng chặng của dòng "Menu:" — ảnh cắt từ chính phần tử trên giao diện
# (form 2026-09-24, bám bản QA "SRS - Danh mục quốc gia").
d.set_menu_icons({k: shot('icon_%s.png' % v) for k, v in {
    'Phân hệ Dự án & Giao việc': 'phanhe', 'Danh mục': 'danhmuc', 'Nhóm ngành': 'nhomnganh',
    'Tìm kiếm nâng cao': 'timkiem', 'Tạo mới': 'taomoi', 'Sửa': 'sua', 'Xem chi tiết': 'xem',
    'Xóa': 'xoa', 'Khóa': 'khoa', 'Mở khóa': 'mokhoa', 'Import Excel': 'import',
    'Xuất Excel': 'xuat',
}.items()})

d.title_block('Danh mục nhóm ngành')
d.h2('Mục lục')
d.toc()

# ================================================================ PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục nhóm ngành thuộc phân hệ '
    'Dự án & Giao việc, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ ràng buộc giữa Nhóm ngành với Lĩnh vực Công ty kinh doanh (danh mục cha) và với '
    'Nhóm giải pháp, Ứng dụng (dữ liệu con đang tham chiếu tới nhóm ngành).',
    'Làm rõ điều kiện được Sửa mã, Xóa, Khóa và Mở khóa một nhóm ngành.',
    'Làm rõ quy tắc nhập dữ liệu hàng loạt bằng tệp Excel.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Nhóm ngành', 'Ngành kỹ thuật/công nghệ do TPE cung cấp, được phân chia theo tính chất '
     'công nghệ. Mỗi nhóm ngành thuộc đúng 1 Lĩnh vực Công ty kinh doanh.'),
    ('Lĩnh vực Công ty kinh doanh', 'Danh mục cha của Nhóm ngành, quản lý ở menu Danh mục => '
     'Lĩnh vực Công ty kinh doanh.'),
    ('Nhóm giải pháp', 'Danh mục con gắn với một hoặc nhiều nhóm ngành. Cột “Số nhóm giải pháp” '
     'đếm số nhóm giải pháp đang gắn với nhóm ngành.'),
    ('Ứng dụng', 'Danh mục ứng dụng có khai báo nhóm ngành. Cột “Số ứng dụng” đếm số ứng dụng '
     'đang gắn với nhóm ngành.'),
    ('Mã nhóm ngành', 'Mã định danh dạng NN.XXXX: tiền tố “NN.” cố định + 4 ký tự do người dùng '
     'nhập. Không trùng trong toàn hệ thống.'),
    ('Trạng thái Khóa', 'Nhóm ngành ngừng sử dụng: không được chọn ở các màn nghiệp vụ, không sửa '
     'được. Khóa KHÔNG xóa dữ liệu, có thể Mở khóa lại.'),
    ('Dữ liệu liên kết', 'Nhóm giải pháp hoặc Ứng dụng đang tham chiếu tới nhóm ngành.'),
], widths=[1.8, 4.2])

# ================================================================ PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý danh mục nhóm ngành',
     'Xem danh sách, xem chi tiết; hiện nút Tạo mới, Import Excel; được Sửa, Xóa, Khóa / Mở khóa '
     'và Xuất Excel.'),
    ('Q2', 'Xem danh mục nhóm ngành', 'Chỉ xem danh sách, tìm kiếm và xem chi tiết.'),
], widths=[0.8, 2.0, 3.2])
d.p('Màn hình không phân quyền theo cấp dữ liệu (công ty / phòng ban / bộ phận): người có quyền '
    'xem được toàn bộ nhóm ngành của hệ thống.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách nhóm ngành', '✅', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '❌'),
    ('FR-03 Tạo mới nhóm ngành', '✅', '❌', '❌'),
    ('FR-04 Chỉnh sửa nhóm ngành', '✅', '❌', '❌'),
    ('FR-05 Xem chi tiết nhóm ngành', '✅', '✅', '❌'),
    ('FR-06 Xóa nhóm ngành', '✅', '❌', '❌'),
    ('FR-07 Khóa / Mở khóa nhóm ngành', '✅', '❌', '❌'),
    ('FR-08 Import Excel', '✅', '❌', '❌'),
    ('FR-09 Xuất Excel', '✅', '❌', '❌'),
], widths=[3.0, 0.8, 0.8, 1.4])

# ================================================================ PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_QL, [0, 1, 2, 3, 4, 5, 6]),
     (A_XEM, [0])],
    [('FR-01', 'Xem danh sách nhóm ngành', 'view'),
     ('FR-03', 'Tạo mới nhóm ngành', 'crud'),
     ('FR-04', 'Chỉnh sửa nhóm ngành', 'crud'),
     ('FR-06', 'Xóa nhóm ngành', 'action'),
     ('FR-07', 'Khóa / Mở khóa nhóm ngành', 'action'),
     ('FR-08', 'Import Excel nhóm ngành', 'io'),
     ('FR-09', 'Xuất Excel danh sách nhóm ngành', 'io')],
    # «extend» CHỈ dùng cho chức năng phụ gắn vào màn danh sách (bám bản QA "Danh mục quốc gia")
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-05', 'Xem chi tiết nhóm ngành', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Danh mục nhóm ngành')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1
d.h3('2.1 Xem danh sách nhóm ngành')
d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Danh mục nhóm ngành tại phần mô tả chi tiết.', anchor='list')
d.intro_table(
    ten='Xem danh sách nhóm ngành',
    mota='Hiển thị toàn bộ nhóm ngành kèm Lĩnh vực Công ty kinh doanh, số nhóm giải pháp, số ứng '
         'dụng đang liên kết, thông tin cập nhật và trạng thái; có phân trang.',
    tacnhan='Người quản lý / người xem danh mục nhóm ngành; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng vào menu Phân hệ Dự án & Giao việc → Danh mục → Nhóm ngành.\n'
          '2. Hệ thống nạp trang 1, 10 dòng/trang, sắp xếp bản ghi mới tạo lên đầu.\n'
          '3. Bảng hiển thị dữ liệu, dòng “Hiển thị a–b / N nhóm ngành” và thanh phân trang.',
    phu='• Không có bản ghi phù hợp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm số ở cột Số nhóm giải pháp / Số ứng dụng (khác 0) → mở tab mới tới danh sách Nhóm '
        'giải pháp / Ứng dụng đã lọc sẵn theo nhóm ngành đó.\n'
        '• Bấm tiêu đề cột Cập nhật → đảo chiều sắp xếp theo thời gian cập nhật.\n'
        '• Lỗi tải dữ liệu → thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)
d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách nhóm ngành lúc mới truy cập')
d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng “Danh sách nhóm ngành”', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Tiêu đề cố định phía trên bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1', 'Mở form Tạo mới (FR-03).'),
    ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền Q1',
     'Mở cửa sổ Import (FR-08).'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Tải tệp Excel danh sách (FR-09).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục', 'Đánh số liên tục qua các trang.'),
    ('Cột Mã nhóm ngành - Tên nhóm ngành', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Dòng 1: “Mã - Tên”. Dòng 2: Người tạo, Ngày tạo (dd/mm/yyyy hh:mm:ss). Dưới cùng là 3 nút '
     'thao tác Xem, Sửa, Xóa.'),
    ('Nút Xem (biểu tượng mắt)', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Mở chi tiết (FR-05).'),
    ('Nút Sửa (biểu tượng bút)', 'Icon Button', 'Enable / Disable', '–', 'Theo trạng thái',
     'Không bấm được khi nhóm ngành đang Khóa (FR-04).'),
    ('Nút Xóa (biểu tượng thùng rác)', 'Icon Button', 'Enable / Disable', '–', 'Theo dữ liệu',
     'Không bấm được khi đã có Nhóm giải pháp hoặc Ứng dụng liên kết; rê chuột hiện “Không thể xóa '
     'bản ghi, bản ghi hiện tại đã có dữ liệu liên kết đang tồn tại trên hệ thống” (FR-06).'),
    ('Cột Lĩnh vực Công ty kinh doanh', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tên lĩnh vực đang gán; chưa gán hiển thị “—”.'),
    ('Cột Số nhóm giải pháp', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Căn phải. Khác 0 thì là liên kết mở tab mới tới danh sách Nhóm giải pháp của nhóm ngành.'),
    ('Cột Số ứng dụng', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Căn phải. Khác 0 thì là liên kết mở tab mới tới danh sách Ứng dụng của nhóm ngành.'),
    ('Cột Mô tả', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Trống hiển thị “—”.'),
    ('Cột Cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm:ss', 'Theo dữ liệu',
     'Thời gian cập nhật cuối + “bởi <người cập nhật>”. Sắp xếp được tăng / giảm.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu',
     'Nhãn trạng thái kèm nút ổ khóa để Khóa / Mở khóa (FR-07).'),
    ('Dòng “Hiển thị a–b / N nhóm ngành”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số bản ghi khớp bộ lọc.'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5 / 10 / 20 / 50', '10', 'Đổi thì quay về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Về đầu / lùi / số trang / tiến / về cuối.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '“Không có dữ liệu phù hợp bộ lọc.”'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Ẩn', 'Hiện trong lúc nạp dữ liệu.'),
], required=False)
d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'During:\n– Nạp danh mục Lĩnh vực Công ty kinh doanh đang Hoạt động (cho ô lọc).\n'
     'After:\n– Hiển thị trang 1, 10 dòng, bản ghi mới tạo lên đầu.'),
    ('Bấm tiêu đề cột Cập nhật', 'Click',
     'After:\n– Sắp xếp theo thời gian cập nhật, bấm lại để đảo chiều; quay về trang 1.'),
    ('Bấm số trang / đổi Số dòng/trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu; đổi số dòng/trang thì quay về trang 1.'),
    ('Bấm số ở cột Số nhóm giải pháp / Số ứng dụng', 'Click',
     'After:\n– Mở tab mới tới danh sách Nhóm giải pháp / Ứng dụng đã lọc theo nhóm ngành.'),
    ('Quay lại tab trình duyệt đang mở màn hình', 'System',
     'After:\n– Tự nạp lại danh sách để hiển thị dữ liệu mới nhất.'),
])

# ---------------------------------------------------------------- 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của Danh mục '
           'nhóm ngành tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc nhóm ngành',
    mota='Tìm nhanh theo từ khóa và lọc nâng cao theo mã, tên, trạng thái, lĩnh vực, người tạo, '
         'người cập nhật, khoảng ngày cập nhật.',
    tacnhan='Người quản lý / người xem danh mục nhóm ngành; Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách nhóm ngành.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
          '2. Hoặc bấm “Tìm kiếm nâng cao” để mở khối lọc và chọn / nhập điều kiện.\n'
          '3. Mỗi lần đổi một ô lọc nâng cao, hệ thống tự lọc lại ngay, không cần bấm Tìm kiếm.\n'
          '4. Bảng hiển thị kết quả từ trang 1.',
    phu='• Bấm Làm mới → xóa hết điều kiện lọc, trả về danh sách ban đầu.\n'
        '• Không có kết quả → “Không có dữ liệu phù hợp bộ lọc.”',
    dacbiet=None)
d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02-bo-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao đang mở')
d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Tìm gần đúng theo Mã nhóm ngành hoặc Tên nhóm ngành. Chỉ áp dụng khi bấm Tìm kiếm / Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng điều kiện, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi điều kiện lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Khối lọc đang đóng',
     'Mở / đóng khối lọc nâng cao.'),
    ('Mã nhóm ngành', 'Textbox', 'Enable', '–', 'Không', 'Trống', 'Lọc gần đúng theo mã.'),
    ('Tên nhóm ngành', 'Textbox', 'Enable', '–', 'Không', 'Trống', 'Lọc gần đúng theo tên.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Trống', 'Có nút xóa chọn.'),
    ('Lĩnh vực Công ty kinh doanh', 'Dropdown', 'Enable', 'Danh sách lĩnh vực đang Hoạt động',
     'Không', 'Trống', 'Lọc đúng theo lĩnh vực.'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Lọc đúng theo người tạo.'),
    ('Người cập nhật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc đúng theo người cập nhật cuối.'),
    ('Cập nhật từ', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Ngày cập nhật ≥ ngày chọn (tính cả ngày).'),
    ('Cập nhật đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Ngày cập nhật ≤ ngày chọn (tính cả ngày).'),
])
d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm / Enter ở ô tìm nhanh', 'Click / Keypress',
     'Before:\n– Lấy từ khóa, bỏ khoảng trắng đầu cuối.\n'
     'After:\n– Lọc gần đúng theo mã hoặc tên kết hợp các điều kiện lọc nâng cao; hiển thị trang 1.'),
    ('Đổi giá trị một ô lọc nâng cao', 'Change',
     'After:\n– Tự lọc lại ngay theo toàn bộ điều kiện đang chọn.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xóa mọi điều kiện, sắp xếp mặc định, hiển thị trang 1.'),
])

# ---------------------------------------------------------------- 2.3
FORM_ROWS = [
    ('Mã nhóm ngành', 'Textbox', 'Enable / Disable', 'NN. + 4 ký tự', 'Có', 'Tiền tố “NN.” cố định',
     'Chỉ nhận chữ không dấu, chữ số và dấu gạch dưới; hệ thống đổi sang chữ in hoa. Không trùng.'),
    ('Tên nhóm ngành', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Không trùng; không chứa dấu phẩy (,) và dấu hai chấm (:). Icon ⓘ mô tả khái niệm Nhóm ngành.'),
    ('Lĩnh vực Công ty kinh doanh', 'Dropdown', 'Enable', 'Danh sách lĩnh vực đang Hoạt động', 'Có',
     'Trống', 'Chọn đúng 1 lĩnh vực.'),
    ('Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Có', 'Hoạt động',
     'Không có nút xóa chọn — luôn phải có giá trị.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Trống', 'Nội dung mô tả tự do.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ kèm biểu tượng cảnh báo ngay dưới ô bị lỗi.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu.'),
]

d.h3('2.3 Tạo mới nhóm ngành')
d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Tạo mới nhóm ngành', 'crud',
            actor=A_QL, caption='Biểu đồ Use Case — FR-03 Tạo mới nhóm ngành')
d.p('2.3.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Tạo mới nhóm ngành',
    mota='Thêm một nhóm ngành mới vào danh mục, gắn với 1 Lĩnh vực Công ty kinh doanh.',
    tacnhan='Người quản lý danh mục nhóm ngành',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở cửa sổ “Tạo mới nhóm ngành”, Trạng thái mặc định Hoạt động.\n'
          '3. Người dùng nhập Mã, Tên, chọn Lĩnh vực Công ty kinh doanh, nhập Mô tả (nếu có).\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống kiểm tra dữ liệu và ghi bản ghi mới.\n'
          '6. Thông báo “Thêm mới thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Bấm “Lưu & Tiếp tục” → lưu xong giữ cửa sổ mở, xóa trắng form để nhập bản ghi tiếp.\n'
        '• Dữ liệu không hợp lệ → báo lỗi đỏ dưới từng ô sai, thông báo “Bạn chưa nhập đầy đủ thông '
        'tin”, giữ nguyên dữ liệu đã nhập.\n'
        '• Lỗi khác → thông báo “Thêm mới thất bại” (hoặc nội dung lỗi hệ thống trả về).',
    dacbiet='Nút Lưu và Lưu & Tiếp tục bị khóa trong lúc đang xử lý để tránh tạo trùng.')
d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Tạo mới nhóm ngành', shot=shot('03-tao-moi.png'),
         shot_caption='Cửa sổ Tạo mới nhóm ngành')
d.figure(shot('03b-tao-moi-loi.png'), 'Cửa sổ Tạo mới khi bấm Lưu mà chưa nhập các trường bắt buộc',
         width_in=6.2)
d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([('Tiêu đề “Tạo mới nhóm ngành”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '–')]
           + FORM_ROWS[:-1] + [
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu rồi đóng cửa sổ.'),
    ('Nút Lưu & Tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Lưu rồi xóa trắng form để nhập tiếp. Chỉ có ở Tạo mới.'),
    FORM_ROWS[-1],
])
d.p('2.3.5 Danh sách event và xử lý event')
SAVE_DURING = (
    '– Mã nhóm ngành trống → “Bắt buộc phải nhập”.\n'
    '– Mã không đủ 4 ký tự sau “NN.” → “Vui lòng nhập 4 ký tự”.\n'
    '– Mã có ký tự không hợp lệ → “Chỉ cho phép: Chữ cái không dấu(A-Z, a-z), chữ số (0-9) và dấu '
    'gạch dưới (_).”\n'
    '– Mã đã tồn tại → “Đã tồn tại trên hệ thống”.\n'
    '– Tên nhóm ngành trống → “Bắt buộc phải nhập”; trùng → “Đã tồn tại trên hệ thống”; quá 255 ký '
    'tự → “Vui lòng nhập tối đa 255 ký tự.”; chứa , hoặc : → “không được chứa ký tự dấu phẩy (,) và '
    'dấu hai chấm (:)”.\n'
    '– Chưa chọn Lĩnh vực Công ty kinh doanh → “Bắt buộc phải chọn”; lĩnh vực không còn → “Lĩnh vực '
    'Công ty kinh doanh không tồn tại”; lĩnh vực đã khóa → “Lĩnh vực Công ty kinh doanh \"<tên>\" đã '
    'bị khoá, vui lòng chọn lĩnh vực khác”.\n'
    '– Nếu có lỗi validate → thông báo “Bạn chưa nhập đầy đủ thông tin” và không thực hiện bước After.')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'Before:\n– Nút chỉ hiển thị khi có quyền Q1.\n'
     'After:\n– Mở cửa sổ với form trống, Trạng thái = Hoạt động; nạp danh sách lĩnh vực đang Hoạt động.'),
    ('Bấm Lưu / Lưu & Tiếp tục', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n' + SAVE_DURING + '\n'
     'After:\n– Ghi bản ghi mới, mã chuyển sang chữ in hoa; ghi người tạo, thời điểm tạo.\n'
     '– Thông báo “Thêm mới thành công”, nạp lại danh sách.\n'
     '– Lưu: đóng cửa sổ. Lưu & Tiếp tục: giữ cửa sổ, xóa trắng form.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, không lưu dữ liệu đang nhập.'),
])

# ---------------------------------------------------------------- 2.4
d.h3('2.4 Chỉnh sửa nhóm ngành')
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Chỉnh sửa nhóm ngành', 'crud',
            actor=A_QL, caption='Biểu đồ Use Case — FR-04 Chỉnh sửa nhóm ngành')
d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX (áp dụng tương tự cho màn Sửa).',
           anchor='create')
d.intro_table(
    ten='Chỉnh sửa nhóm ngành',
    mota='Cập nhật thông tin của một nhóm ngành đang Hoạt động.',
    tacnhan='Người quản lý danh mục nhóm ngành',
    dieukien='Người dùng có quyền Q1; nhóm ngành đang ở trạng thái Hoạt động.',
    chinh='1. Người dùng bấm nút Sửa trên dòng nhóm ngành.\n'
          '2. Hệ thống mở cửa sổ “Sửa nhóm ngành” với dữ liệu hiện tại, kèm thời điểm và người cập '
          'nhật cuối.\n'
          '3. Người dùng sửa thông tin và bấm Lưu.\n'
          '4. Hệ thống kiểm tra dữ liệu và cập nhật.\n'
          '5. Thông báo “Cập nhật thành công”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Nhóm ngành đang Khóa → nút Sửa không bấm được.\n'
        '• Lĩnh vực đang gán nay đã bị khóa → vẫn hiển thị đúng tên trong ô (có biểu tượng 🔒) và '
        'vẫn lưu được nếu giữ nguyên; đổi sang lĩnh vực khác thì chỉ chọn được lĩnh vực Hoạt động.\n'
        '• Bản ghi đã bị xóa / khóa bởi người khác trong lúc sửa → “Dữ liệu đã thay đổi, vui lòng '
        'tải lại”.\n'
        '• Dữ liệu không hợp lệ → báo lỗi dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin”.',
    dacbiet='Nhóm ngành đã có Nhóm giải pháp hoặc Ứng dụng liên kết thì không được đổi Mã. Ô Trạng '
            'thái bị khóa khi nhóm ngành còn Nhóm giải pháp đang Hoạt động.')
d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', modal='Sửa nhóm ngành', shot=shot('04-sua.png'),
         shot_caption='Cửa sổ Sửa nhóm ngành')
d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Sửa nhóm ngành”', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     'Kèm chip “Cập nhật: <thời điểm>” và người cập nhật cuối.'),
    ('Mã nhóm ngành', 'Textbox', 'Enable', 'NN. + 4 ký tự', 'Có', 'Theo dữ liệu',
     'Như Tạo mới. Đã có dữ liệu liên kết mà đổi mã → báo lỗi, không lưu.'),
    ('Tên nhóm ngành', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo dữ liệu', 'Như Tạo mới.'),
    ('Lĩnh vực Công ty kinh doanh', 'Dropdown', 'Enable', 'Lĩnh vực đang Hoạt động + lĩnh vực đang gán',
     'Có', 'Theo dữ liệu', 'Lĩnh vực đang gán đã khóa vẫn hiển thị kèm 🔒.'),
    ('Trạng thái', 'Dropdown', 'Enable / Disable', 'Hoạt động / Khóa', 'Có', 'Theo dữ liệu',
     'Bị khóa khi nhóm ngành còn Nhóm giải pháp đang Hoạt động.'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Theo dữ liệu', '–'),
    ('Ngày tạo', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', 'Người tạo và thời điểm tạo.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Không có nút Lưu & Tiếp tục.'),
    FORM_ROWS[-2], FORM_ROWS[-1],
])
d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ bấm được khi nhóm ngành đang Hoạt động.\n'
     'During:\n– Nạp chi tiết bản ghi và danh sách lĩnh vực (kèm lĩnh vực đang gán).\n'
     '– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ Sửa với dữ liệu hiện tại.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     '– Nhóm ngành không còn Hoạt động, hoặc chuyển sang Khóa khi còn Nhóm giải pháp đang Hoạt '
     'động → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'During:\n' + SAVE_DURING.replace(
         '– Nếu có lỗi validate',
         '– Đổi mã khi đã có dữ liệu liên kết → “Không thể sửa mã khi đã có dữ liệu nhóm giải pháp '
         'hoặc ứng dụng liên quan.”\n– Nếu có lỗi validate') + '\n'
     'After:\n– Cập nhật bản ghi; ghi người cập nhật, thời điểm cập nhật.\n'
     '– Thông báo “Cập nhật thành công”, đóng cửa sổ, nạp lại danh sách.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ, bỏ các thay đổi chưa lưu.'),
])

# ---------------------------------------------------------------- 2.5
d.h3('2.5 Xem chi tiết nhóm ngành')
d.p('2.5.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết nhóm ngành',
    mota='Xem toàn bộ thông tin của một nhóm ngành ở chế độ chỉ đọc, kèm số nhóm giải pháp và số '
         'ứng dụng đang liên kết.',
    tacnhan='Người quản lý / người xem danh mục nhóm ngành',
    dieukien='Người dùng có quyền Q1 hoặc Q2.',
    chinh='1. Người dùng bấm nút Xem trên dòng nhóm ngành.\n'
          '2. Hệ thống mở cửa sổ “Xem chi tiết nhóm ngành”, mọi ô ở trạng thái chỉ đọc.\n'
          '3. Người dùng bấm Đóng để quay về danh sách.',
    phu='• Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”, không mở cửa sổ.',
    dacbiet=None)
d.p('2.5.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', modal='Xem chi tiết nhóm ngành', shot=shot('05-xem.png'),
         shot_caption='Cửa sổ Xem chi tiết nhóm ngành')
d.p('2.5.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xem chi tiết nhóm ngành”', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Kèm chip thời điểm và người cập nhật cuối.'),
    ('Mã nhóm ngành', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', 'Không hiện dấu *.'),
    ('Tên nhóm ngành', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Lĩnh vực Công ty kinh doanh', 'Dropdown', 'Read-only', '–', 'Theo dữ liệu',
     'Lĩnh vực đã khóa vẫn hiển thị đúng tên kèm 🔒.'),
    ('Trạng thái', 'Dropdown', 'Read-only', 'Hoạt động / Khóa', 'Theo dữ liệu', '–'),
    ('Mô tả', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Số nhóm giải pháp', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Số nhóm giải pháp đang liên kết.'),
    ('Số ứng dụng', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu', 'Số ứng dụng đang liên kết.'),
    ('Ngày tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Người tạo và thời điểm tạo.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Không có nút Lưu.'),
], required=False)
d.p('2.5.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xem', 'Click',
     'Before:\n– Kiểm tra quyền Q1 hoặc Q2.\n' + NO_PERM + '\n'
     'After:\n– Mở cửa sổ chi tiết ở chế độ chỉ đọc.'),
    ('Bấm Đóng / dấu ×', 'Click', 'After:\n– Đóng cửa sổ.'),
])

# ---------------------------------------------------------------- 2.6
d.h3('2.6 Xóa nhóm ngành')
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Xóa nhóm ngành', 'action',
            actor=A_QL, caption='Biểu đồ Use Case — FR-06 Xóa nhóm ngành')
d.p('2.6.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa.', anchor='delete')
d.intro_table(
    ten='Xóa nhóm ngành',
    mota='Xóa hẳn một nhóm ngành chưa được Nhóm giải pháp hay Ứng dụng nào sử dụng.',
    tacnhan='Người quản lý danh mục nhóm ngành',
    dieukien='Người dùng có quyền Q1; nhóm ngành chưa có Nhóm giải pháp và Ứng dụng liên kết.',
    chinh='1. Người dùng bấm nút Xóa trên dòng nhóm ngành.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận xóa”.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xóa bản ghi, thông báo “Xoá thành công” và nạp lại danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, không xóa.\n'
        '• Nhóm ngành đã có dữ liệu liên kết → nút Xóa không bấm được; nếu phát sinh liên kết trong '
        'lúc đang xác nhận → “Dữ liệu đang được sử dụng, vui lòng tải lại”.\n'
        '• Bản ghi đã bị xóa trước đó → “Dữ liệu đã thay đổi, vui lòng tải lại”.',
    dacbiet='Xóa là xóa hẳn, không khôi phục được. Muốn ngừng dùng nhóm ngành đã có liên kết thì '
            'dùng chức năng Khóa.')
d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', modal='Xác nhận xóa', shot=shot('06-xoa.png'),
         shot_caption='Hộp thoại xác nhận xóa nhóm ngành')
d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề “Xác nhận xóa”', 'Label', 'Hiển thị', 'Hiển thị', '–'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu', '“Bạn có chắc muốn xóa nhóm ngành \'<tên>\'?”'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
], required=False, scope=False)
d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng', 'Click',
     'Before:\n– Nút chỉ bấm được khi nhóm ngành chưa có Nhóm giải pháp và Ứng dụng liên kết.\n'
     'After:\n– Hiện hộp thoại xác nhận.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Còn Nhóm giải pháp hoặc Ứng dụng liên kết → “Dữ liệu đang được sử dụng, vui lòng '
     'tải lại” và dừng xử lý.\n'
     '– Bản ghi không còn → “Dữ liệu đã thay đổi, vui lòng tải lại”.\n'
     'After:\n– Xóa bản ghi, thông báo “Xoá thành công”, nạp lại danh sách.'),
    ('Bấm Hủy / dấu ×', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.7
d.h3('2.7 Khóa / Mở khóa nhóm ngành')
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Khóa / Mở khóa nhóm ngành', 'action',
            actor=A_QL, caption='Biểu đồ Use Case — FR-07 Khóa / Mở khóa nhóm ngành')
d.p('2.7.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử, Khóa / Mở khóa.', anchor='history')
d.intro_table(
    ten='Khóa / Mở khóa nhóm ngành',
    mota='Chuyển trạng thái nhóm ngành giữa Hoạt động và Khóa bằng nút ổ khóa ở cột Trạng thái.',
    tacnhan='Người quản lý danh mục nhóm ngành',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút ổ khóa ở cột Trạng thái.\n'
          '2. Hệ thống hiện hộp thoại “Xác nhận khoá” (hoặc “Xác nhận mở khoá”).\n'
          '3. Người dùng bấm Khoá (hoặc Mở khoá).\n'
          '4. Hệ thống đổi trạng thái, thông báo “Khoá thành công” / “Mở khoá thành công”, nạp lại '
          'danh sách.',
    phu='• Nhóm ngành còn Nhóm giải pháp đang Hoạt động → nút Khóa không bấm được, rê chuột hiện '
        '“Bạn cần khóa hết các danh mục con trước khi thực hiện thay đổi trạng thái tại đây”.\n'
        '• Phát sinh Nhóm giải pháp Hoạt động trong lúc xác nhận → “Dữ liệu đã thay đổi, vui lòng '
        'tải lại”.\n'
        '• Bấm Hủy → không đổi trạng thái.',
    dacbiet='Mở khóa luôn được phép. Nhóm ngành đang Khóa không Sửa được cho tới khi Mở khóa.')
d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Khóa / Mở khóa', modal='Xác nhận khoá / Xác nhận mở khoá',
         shot=shot('07-khoa.png'), shot_caption='Hộp thoại xác nhận khóa nhóm ngành')
d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút ổ khóa ở cột Trạng thái', 'Icon Button', 'Enable / Disable', 'Theo dữ liệu',
     'Đang Hoạt động: biểu tượng khóa đóng (Khóa). Đang Khóa: biểu tượng khóa mở (Mở khóa).'),
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo trạng thái', '“Xác nhận khoá” / “Xác nhận mở khoá”.'),
    ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
     '“Bạn có chắc muốn khoá (mở khoá) nhóm ngành \'<tên>\'?”'),
    ('Nút Khoá / Mở khoá', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại.'),
], required=False, scope=False)
d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút ổ khóa', 'Click',
     'Before:\n– Khóa: chỉ bấm được khi không còn Nhóm giải pháp đang Hoạt động.\n'
     'After:\n– Hiện hộp thoại xác nhận tương ứng.'),
    ('Bấm Khoá', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Còn Nhóm giải pháp đang Hoạt động → “Dữ liệu đã thay đổi, vui lòng tải lại” và '
     'dừng xử lý.\n'
     'After:\n– Đổi trạng thái sang Khóa, ghi người cập nhật, thông báo “Khoá thành công”, nạp lại '
     'danh sách.'),
    ('Bấm Mở khoá', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'After:\n– Đổi trạng thái sang Hoạt động, ghi người cập nhật, thông báo “Mở khoá thành công”, '
     'nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.8
d.h3('2.8 Import Excel')
d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Import Excel nhóm ngành', 'io',
            actor=A_QL, caption='Biểu đồ Use Case — FR-08 Import Excel nhóm ngành')
d.p('2.8.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Import Excel nhóm ngành',
    mota='Thêm mới hàng loạt nhóm ngành từ tệp Excel theo file mẫu. Chỉ thêm mới, không cập nhật '
         'nhóm ngành đã có.',
    tacnhan='Người quản lý danh mục nhóm ngành',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng bấm Import Excel.\n'
          '2. (Tuỳ chọn) Bấm “Tải file mẫu” để lấy tệp Mau_import_NhomNganh.xlsx.\n'
          '3. Bấm “Chọn file Excel”, chọn tệp đã điền dữ liệu.\n'
          '4. Bấm “Load lên bảng” để đọc tệp ra bảng xem trước.\n'
          '5. Bấm “Validate” → hệ thống kiểm tra từng dòng, đánh dấu dòng hợp lệ / lỗi kèm lý do; '
          'dòng hợp lệ bị khóa không sửa được.\n'
          '6. Người dùng sửa trực tiếp các dòng lỗi và Validate lại (nếu cần).\n'
          '7. Bấm “Import” → hệ thống thêm các dòng hợp lệ, thông báo “Import thành công <n> nhóm '
          'ngành”, đóng cửa sổ và nạp lại danh sách.',
    phu='• Có dòng lỗi khi Import → chỉ thêm dòng hợp lệ, thông báo “Import thành công x/y nhóm '
        'ngành. z nhóm ngành thất bại.”\n'
        '• Không dòng nào hợp lệ → “Không có dữ liệu hợp lệ để import”.\n'
        '• Bật “Chỉ dòng lỗi” để lọc bảng xem trước chỉ còn dòng lỗi.\n'
        '• Bấm Làm mới → xóa dữ liệu đã nạp để chọn tệp khác.',
    dacbiet='Mỗi lần import tối đa 1.000 dòng.')
d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Import Excel', modal='Import Nhóm ngành', shot=shot('08-import.png'),
         shot_caption='Cửa sổ Import Nhóm ngành')
d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx / .xls', 'Có', 'Hiển thị', 'Chọn tệp cần import.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải Mau_import_NhomNganh.xlsx.'),
    ('Nút Load lên bảng', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa chọn tệp',
     'Đọc tệp ra bảng xem trước.'),
    ('Nút Validate', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa có dữ liệu',
     'Kiểm tra dữ liệu từng dòng.'),
    ('Nút Import', 'Button', 'Enable / Disable', '–', '–', 'Disable khi chưa Validate',
     'Ghi các dòng hợp lệ.'),
    ('Công tắc Chỉ dòng lỗi', 'Button', 'Enable', '–', '–', 'Tắt', 'Lọc bảng chỉ còn dòng lỗi.'),
    ('Cột Mã nhóm ngành', 'Textbox', 'Enable', 'NN.XXXX', 'Có', 'Theo tệp', 'Không trùng trong tệp và hệ thống.'),
    ('Cột Tên nhóm ngành', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Theo tệp',
     'Không trùng; không chứa , và :.'),
    ('Cột Mã lĩnh vực Công ty kinh doanh', 'Textbox', 'Enable', 'LVCTKD.XXXX', 'Có', 'Theo tệp',
     'Lĩnh vực phải tồn tại và đang Hoạt động.'),
    ('Cột Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Có', 'Theo tệp',
     'Nhận cả active / inactive.'),
    ('Cột Mô tả', 'Textarea', 'Enable', '0–1.000 ký tự', 'Không', 'Theo tệp', '–'),
    ('Dòng Tổng / hợp lệ / lỗi', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', 'Thống kê sau Validate.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không import.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa dữ liệu đã nạp.'),
])
d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Validate', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During (từng dòng):\n'
     '– Thiếu mã / tên / trạng thái / mã lĩnh vực → “Mã nhóm ngành không được để trống”, “Tên nhóm '
     'ngành không được để trống”, “Trạng thái không được để trống”, “Mã lĩnh vực Công ty kinh doanh '
     'không được để trống”.\n'
     '– Mã sai định dạng → “Mã nhóm ngành phải theo định dạng NN.XXXX (4 ký tự)”.\n'
     '– Mã trùng trong tệp → “Mã nhóm ngành bị trùng lặp trong file import (dòng n)”; trùng hệ thống '
     '→ “Mã nhóm ngành đã tồn tại trong hệ thống”.\n'
     '– Tên trùng trong tệp → “Tên nhóm ngành bị trùng lặp trong file import (dòng n)”; trùng hệ '
     'thống → “Tên nhóm ngành đã tồn tại trong hệ thống”; quá dài → “Tên nhóm ngành vượt quá độ dài '
     'cho phép (tối đa 255 ký tự)”; chứa , hoặc : → “không được chứa ký tự dấu phẩy (,) và dấu hai '
     'chấm (:)”.\n'
     '– Lĩnh vực không có → “Lĩnh vực Công ty kinh doanh \"<mã>\" không tồn tại”; đã khóa → “Lĩnh '
     'vực Công ty kinh doanh \"<mã>\" đã bị khoá”.\n'
     '– Trạng thái sai → “Trạng thái không hợp lệ, chỉ nhận giá trị: active hoặc inactive”.\n'
     '– Mô tả quá dài → “Mô tả vượt quá độ dài cho phép (tối đa 1000 ký tự)”.\n'
     'After:\n– Đánh dấu từng dòng hợp lệ / lỗi; thông báo “Validate thành công” hoặc “Validate xong: '
     'x hợp lệ, y không hợp lệ”.'),
    ('Bấm Import', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Kiểm tra lại toàn bộ dữ liệu như bước Validate.\n'
     '– Không có dòng hợp lệ → “Không có dữ liệu hợp lệ để import” và dừng xử lý.\n'
     'After:\n– Thêm mới các dòng hợp lệ, mã chuyển sang chữ in hoa.\n'
     '– Thông báo kết quả, đóng cửa sổ, nạp lại danh sách.'),
    ('Bấm Tải file mẫu', 'Click', 'After:\n– Tải tệp Mau_import_NhomNganh.xlsx.'),
])

# ---------------------------------------------------------------- 2.9
d.h3('2.9 Xuất Excel')
d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Xuất Excel danh sách nhóm ngành', 'io',
            actor=A_QL, caption='Biểu đồ Use Case — FR-09 Xuất Excel')
d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách nhóm ngành',
    mota='Tải về tệp danh_sach_nhom_nganh.xls chứa các nhóm ngành theo bộ lọc đang áp dụng.',
    tacnhan='Người quản lý danh mục nhóm ngành',
    dieukien='Người dùng có quyền Q1.',
    chinh='1. Người dùng (tuỳ chọn) đặt bộ lọc trên màn danh sách.\n'
          '2. Bấm Xuất Excel.\n'
          '3. Hệ thống dựng tệp theo bộ lọc và trình duyệt tải tệp về.',
    phu='• Lỗi khi dựng tệp → thông báo lỗi, không tải tệp.',
    dacbiet='Tệp gồm tiêu đề “Danh sách nhóm ngành” và 12 cột: STT, Mã nhóm ngành, Tên nhóm ngành, '
            'Lĩnh vực Công ty kinh doanh, Mô tả, Trạng thái, Số nhóm giải pháp, Số ứng dụng, Người '
            'tạo, Người cập nhật, Ngày tạo, Ngày cập nhật.')
d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('01-danh-sach.png'),
         shot_caption='Nút Xuất Excel ở góc phải phía trên bảng danh sách')
d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tải tệp Excel theo bộ lọc.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện trong lúc dựng tệp.'),
])
d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Kiểm tra quyền Q1.\n' + NO_PERM + '\n'
     'During:\n– Lấy các điều kiện lọc: Mã, Tên, Trạng thái, Người tạo, Người cập nhật, Cập nhật từ, '
     'Cập nhật đến.\n'
     'After:\n– Tải tệp danh_sach_nhom_nganh.xls.'),
])

# ================================================================ PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Danh mục nhóm ngành; không lặp lại các quy '
           'tắc đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Định dạng và tính duy nhất của Mã', [
        '– Mã = tiền tố “NN.” + đúng 4 ký tự gồm chữ không dấu, chữ số, dấu gạch dưới.',
        '– Hệ thống lưu mã ở dạng chữ in hoa; không trùng trong toàn hệ thống.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-02', 'Tên nhóm ngành', [
        '– Bắt buộc, tối đa 255 ký tự, không trùng.',
        '– Không chứa dấu phẩy (,) và dấu hai chấm (:).',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-03', 'Gắn Lĩnh vực Công ty kinh doanh', [
        '– Mỗi nhóm ngành bắt buộc thuộc đúng 1 lĩnh vực.',
        '– Chỉ chọn được lĩnh vực đang Hoạt động.',
        '– Ngoại lệ: khi Sửa, lĩnh vực đang gán nay đã bị khóa vẫn hiển thị đúng tên (🔒) và được '
        'giữ nguyên khi lưu.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel', 'Tìm kiếm và lọc']),
    ('BR-04', 'Khóa sửa Mã khi đã có liên kết',
     '– Nhóm ngành đã có Nhóm giải pháp hoặc Ứng dụng liên kết thì không được đổi Mã.',
     'Chỉnh sửa'),
    ('BR-05', 'Chỉ sửa nhóm ngành đang Hoạt động',
     '– Nhóm ngành đang Khóa không sửa được; phải Mở khóa trước.', ['Chỉnh sửa', 'Danh sách']),
    ('BR-06', 'Điều kiện Xóa', [
        '– Chỉ xóa được khi chưa có Nhóm giải pháp và Ứng dụng nào liên kết.',
        '– Xóa là xóa hẳn; nhóm ngành đã có liên kết thì dùng Khóa thay cho Xóa.',
    ], 'Xóa'),
    ('BR-07', 'Điều kiện Khóa / Mở khóa', [
        '– Chỉ Khóa được khi không còn Nhóm giải pháp nào đang Hoạt động gắn với nhóm ngành '
        '(áp dụng cả khi đổi Trạng thái trong form Sửa).',
        '– Mở khóa luôn được phép.',
    ], ['Khóa / Mở khóa', 'Chỉnh sửa']),
    ('BR-08', 'Import chỉ thêm mới', [
        '– Mỗi lần tối đa 1.000 dòng.',
        '– Mã / tên đã có trong hệ thống hoặc trùng nhau trong tệp → dòng lỗi, không ghi đè.',
        '– Chỉ các dòng hợp lệ được thêm; dòng lỗi được báo lý do cụ thể.',
    ], 'Import Excel'),
    ('BR-09', 'Số liệu liên kết', [
        '– Số nhóm giải pháp / Số ứng dụng đếm theo số bản ghi khác nhau đang gắn với nhóm ngành.',
        '– Số khác 0 là liên kết mở tab mới tới danh sách tương ứng đã lọc theo nhóm ngành.',
    ], ['Danh sách', 'Xem chi tiết']),
])

d.save()
