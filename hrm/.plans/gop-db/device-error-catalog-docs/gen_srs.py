# -*- coding: utf-8 -*-
"""Sinh SRS man 'Danh muc cong viec, loi thiet bi' theo FORM MOI (4 phan).

Chay:  python .plans/gop-db/device-error-catalog-docs/gen_srs.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "srs-documenter", "assets"))
sys.path.insert(0, HERE)
from srs_docx_lib import SrsDoc  # noqa: E402
import de_config as C  # noqa: E402

SHOTS = os.path.join(HERE, "de_shots")


def shot(name):
    p = os.path.join(SHOTS, name)
    if not os.path.exists(p):
        raise IOError('Thieu anh: %s' % p)
    return p


TEN, DT, QUYEN, S = C.TEN, C.DOI_TUONG, C.QUYEN, C.SHOTS
P1 = 'Người quản lý danh mục (có quyền “%s”)' % QUYEN

d = SrsDoc(out=os.path.join(HERE, 'SRS - %s.docx' % TEN.replace('/', '-')),
           menu='Phân hệ Chăm sóc khách hàng → Danh mục → Công việc, lỗi thiết bị',
           route=C.ROUTE, full_url=C.HOST + C.ROUTE, img_prefix='de_')

d.title_block(TEN)
d.h2('Mục lục')
d.toc()

# ==================================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s, nhằm:' % TEN)
d.bullets([
    'Thống nhất yêu cầu giữa BA / PO / Dev / Test cho màn danh mục nền của nghiệp vụ sửa chữa.',
    'Là căn cứ nghiệm thu chức năng và phân quyền.',
    'Làm rõ quy tắc trùng tên theo TỪNG LOẠI — hai loại khác nhau được phép trùng tên, đây là '
    'điểm dễ hiểu sai nhất của màn hình.',
    'Làm rõ điều kiện hiển thị của từng nút trên cột Hành động: nút Sửa và Xóa biến mất khi bản '
    'ghi đã Khóa hoặc đã phát sinh chứng từ.',
    'Làm rõ các trường để trống thì hệ thống tự tính hoặc lấy theo cấu hình công ty.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'],
        C.THUAT_NGU + [('SRS', 'Software Requirements Specification')],
        widths=[1.8, 4.2])

# ==================================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('P1', QUYEN,
     'Mở màn hình, xem danh sách, thêm mới, chỉnh sửa, xóa, khóa / mở khóa, xuất Excel và in '
     'danh sách. Thiếu quyền này thì mục menu không hiển thị và truy cập thẳng đường dẫn bị chặn.'),
], widths=[0.8, 2.2, 3.0])
d.p('Màn hình chỉ có MỘT quyền duy nhất cho cả xem lẫn thao tác. Riêng chức năng Xem lịch sử '
    'thay đổi không gắn quyền, theo quy ước chung của mọi màn danh sách.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'P1', 'Không có quyền'], [
    ('FR-01 Xem danh sách', '✅', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '❌'),
    ('FR-03 Tuỳ chỉnh cột hiển thị', '✅', '❌'),
    ('FR-04 Thêm mới', '✅', '❌'),
    ('FR-05 Chỉnh sửa', '✅', '❌'),
    ('FR-06 Xóa', '✅', '❌'),
    ('FR-07 Khóa / Mở khóa', '✅', '❌'),
    ('FR-08 In và Xuất Excel', '✅', '❌'),
    ('FR-09 Xem lịch sử thay đổi', '✅', '❌'),
], widths=[3.4, 1.3, 1.3])

# ==================================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure(
    'HỆ THỐNG HRM — %s' % TEN.upper(),
    [(P1, [0, 1, 2, 3, 4, 5, 6, 7, 8])],
    [('FR-01', 'Xem danh sách', 'view', None),
     ('FR-02', 'Tìm kiếm và lọc', 'view', None),
     ('FR-03', 'Tuỳ chỉnh cột', 'view', None),
     ('FR-04', 'Thêm mới', 'crud', None),
     ('FR-05', 'Chỉnh sửa', 'crud', None),
     ('FR-06', 'Xóa', 'action', '«extend» Ẩn nút Xóa khi đã phát sinh chứng từ'),
     ('FR-07', 'Khóa / Mở khóa', 'action', None),
     ('FR-08', 'In và Xuất Excel', 'io', None),
     ('FR-09', 'Lịch sử thay đổi', 'view', None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách')
d.p('2.1.1 Giới thiệu')
d.intro_table(
    'Xem danh sách %s' % DT,
    'Hiển thị toàn bộ hạng mục trong danh mục, có phân trang, sắp xếp và tuỳ chỉnh cột.',
    P1,
    'Người dùng có quyền “%s”.' % QUYEN,
    '1. Người dùng vào menu Chăm sóc khách hàng → Danh mục → Công việc, lỗi thiết bị.\n'
    '2. Hệ thống kiểm tra quyền rồi nạp trang đầu tiên của danh sách.\n'
    '3. Bảng hiển thị dữ liệu theo cấu hình cột của riêng người dùng.',
    '• Không có quyền → mục menu không hiển thị; truy cập thẳng đường dẫn thì hệ thống từ chối.\n'
    '• Danh mục chưa có bản ghi nào → bảng hiện thông báo không có dữ liệu.')

d.p('2.1.2 Layout màn hình')
d.layout(shot=shot(S['danhsach']), shot_caption='Màn %s lúc mới truy cập' % TEN)

d.p('2.1.3 Mô tả chi tiết giao diện')
rows = [(c[0], 'Table/Grid', 'Read-only', '–', '–', c[1]) for c in C.COT]
rows += [
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Mở trang thêm mới. Chỉ hiện với người có quyền.'),
    ('Nút Xuất Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Xuất danh sách đang lọc ra tệp bảng tính.'),
    ('Nút In danh sách', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Mở bản in toàn bộ danh sách đang lọc.'),
    ('Biểu tượng Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ bật / tắt cột.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
     'Nút về đầu / lùi / số trang / tiến / về cuối và ô chọn số dòng mỗi trang.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện thông báo không có dữ liệu khi danh sách trống.'),
]
d.ui_table(rows, required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền “%s”.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng '
     'xử lý.\n'
     'After:\n– Nạp trang đầu tiên theo cấu hình cột đã lưu của người dùng.' % QUYEN),
    ('Bấm tiêu đề cột sắp xếp được', 'Click',
     'After:\n– Đổi chiều sắp xếp và nạp lại danh sách từ trang 1.'),
    ('Chuyển trang', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\n'
     'After:\n– Nạp dữ liệu trang mới, số thứ tự tiếp tục liên tục.'),
])

# ------------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')
d.p('2.2.1 Giới thiệu')
d.intro_table(
    'Tìm kiếm và lọc danh sách',
    'Thu hẹp danh sách bằng ô tìm kiếm nhanh và 8 tiêu chí lọc nâng cao.',
    P1,
    'Đang ở màn %s.' % TEN,
    '1. Người dùng bấm Tìm kiếm nâng cao để mở panel lọc.\n'
    '2. Người dùng nhập hoặc chọn các tiêu chí.\n'
    '3. Người dùng bấm Tìm kiếm.\n'
    '4. Hệ thống áp đồng thời mọi tiêu chí và nạp lại danh sách từ trang 1.',
    '• Không có kết quả → bảng hiện thông báo không có dữ liệu.\n'
    '• Bấm Làm mới → xóa hết tiêu chí VÀ nạp lại danh sách đầy đủ ngay.\n'
    '• Lọc theo tên hoặc mã hàng hóa sẽ trả về hạng mục CÓ ÁP DỤNG cho hàng hóa đó, không phải '
    'hạng mục trùng tên với hàng hóa.')

d.p('2.2.2 Layout màn hình')
d.layout(shot=shot(S['boloc']), shot_caption='Panel Tìm kiếm nâng cao đang mở')

d.p('2.2.3 Mô tả chi tiết giao diện')
rows = [(f[0], f[1], 'Enable', f[2], 'Không', f[3], f[4]) for f in C.LOC]
rows += [
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng các tiêu chí.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Xóa hết tiêu chí VÀ nạp lại danh sách ngay.'),
]
d.ui_table(rows)

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm nâng cao', 'Click', 'After:\n– Mở panel chứa 8 tiêu chí lọc.'),
    ('Bấm Tìm kiếm', 'Click',
     'Before:\n– Thu thập giá trị của mọi tiêu chí đang có.\n'
     'During:\n– Áp đồng thời các tiêu chí theo kiểu “và”.\n'
     'After:\n– Nạp lại bảng từ trang 1 và cập nhật tổng số bản ghi.'),
    ('Bấm Làm mới', 'Click',
     'After:\n– Xóa trắng mọi tiêu chí VÀ nạp lại danh sách đầy đủ ngay lập tức.'),
])

# ------------------------------------------------------------------ 2.3
d.h3('2.3 Tuỳ chỉnh cột hiển thị')
d.p('2.3.1 Giới thiệu')
d.intro_table(
    'Tuỳ chỉnh cột hiển thị',
    'Cho phép bật / tắt các cột của bảng. Cấu hình ghi nhớ riêng cho từng người dùng.',
    P1,
    'Đang ở màn %s.' % TEN,
    '1. Người dùng bấm biểu tượng Cấu hình cột hiển thị.\n'
    '2. Hệ thống mở cửa sổ liệt kê toàn bộ cột kèm ô tích.\n'
    '3. Người dùng tích hoặc bỏ tích rồi bấm Lưu.\n'
    '4. Bảng vẽ lại theo cấu hình mới.',
    '• Cột STT và cột Tên bị khóa, luôn hiển thị.\n'
    '• Đóng cửa sổ mà không bấm Lưu → cấu hình không đổi.',
    'Bảy cột mặc định ẩn: Loại, Áp dụng cho thiết bị, Định mức công, Công kỹ thuật, Đơn giá bán, '
    'Người cập nhật, Ngày cập nhật.')

d.p('2.3.2 Layout màn hình')
d.layout(modal='Tuỳ chỉnh cột', shot=shot(S['cot']),
         shot_caption='Cửa sổ Tuỳ chỉnh cột hiển thị')

d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Biểu tượng Cấu hình cột hiển thị', 'Icon Button', 'Enable', 'Hiển thị',
     'Nằm ở góc phải thanh công cụ.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', 'Theo cấu hình đã lưu',
     'Mỗi dòng là một cột kèm ô tích.'),
    ('Ô tích cột STT và cột Tên', 'Icon Button', 'Disable', 'Đã tích',
     'Bị khóa, không bỏ tích được.'),
    ('Nút Lưu', 'Button', 'Enable', 'Hiển thị', 'Ghi nhận cấu hình.'),
    ('Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng, bỏ qua thay đổi.'),
], required=False, scope=False)

d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Cấu hình cột hiển thị', 'Click',
     'After:\n– Mở cửa sổ, nạp cấu hình cột đã lưu của người dùng.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Ghi nhận cấu hình cho riêng người dùng hiện tại và vẽ lại bảng.'),
])

# ------------------------------------------------------------------ 2.4
d.h3('2.4 Thêm mới %s' % DT)
d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Thêm mới %s' % DT, 'crud',
            [('include', 'Kiểm tra quyền “%s”' % QUYEN),
             ('include', 'Kiểm tra trùng tên trong cùng loại'),
             ('extend', 'Tự tính Công kỹ thuật và Đơn giá bán khi để trống')],
            actor=P1)

d.p('2.4.2 Giới thiệu')
d.intro_table(
    'Thêm mới %s' % DT,
    'Thêm một hạng mục công việc hoặc tình trạng lỗi mới. Khác các màn danh mục khác, chức năng '
    'này mở một TRANG RIÊNG chứ không phải cửa sổ, vì form có nhiều bảng con.',
    P1,
    'Người dùng có quyền “%s”.' % QUYEN,
    '1. Người dùng bấm nút Tạo mới; hệ thống mở trang thêm mới.\n'
    '2. Người dùng chọn Loại công việc / lỗi và nhập các trường thông tin.\n'
    '3. Người dùng thêm ít nhất một thiết bị vào bảng Áp dụng cho thiết bị.\n'
    '4. Người dùng khai thêm Vật tư thay thế và Dịch vụ sửa chữa kèm theo nếu có.\n'
    '5. Người dùng bấm Lưu.\n'
    '6. Hệ thống kiểm tra dữ liệu, ghi bản ghi mới và quay về danh sách.',
    '• Thiếu trường bắt buộc → báo lỗi đỏ ngay dưới ô tương ứng, trang không chuyển.\n'
    '• Trùng tên trong cùng loại → bị chặn; trùng tên ở loại khác thì lưu được.\n'
    '• Chưa thêm thiết bị nào → bị chặn.\n'
    '• Đã thêm dòng dịch vụ nhưng bỏ trống Giá vốn hoặc Giá dịch vụ → bị chặn tại đúng ô đó.',
    'Để trống Công kỹ thuật và Đơn giá bán thì hệ thống tự tính; để trống Hệ số giá bán dịch vụ '
    'và Đơn giá công kỹ thuật thì lấy theo cấu hình của công ty.')

d.p('2.4.3 Layout màn hình')
d.layout(route=C.ROUTE + '/create', shot=shot(S['taomoi']),
         shot_caption='Trang Thêm công việc / lỗi thiết bị')
d.figure(shot(S['validate']), 'Trang thêm mới báo lỗi đỏ ngay dưới ô còn thiếu', width_in=6.2)

d.p('2.4.4 Mô tả chi tiết giao diện')
rows = [(t[0], t[1], 'Enable', t[2], t[3], t[4], t[5]) for t in C.TRUONG]
rows += [
    ('Nút thêm dòng ở các bảng con', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở cửa sổ tìm kiếm hàng hóa hoặc dịch vụ để chọn.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi bản ghi rồi quay về danh sách.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
    ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi, kể cả ô nằm trong bảng con.'),
]
d.ui_table(rows)

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'Before:\n– Kiểm tra quyền “%s”; thiếu quyền thì nút không hiển thị.\n'
     'After:\n– Mở trang thêm mới với các ô để trống.' % QUYEN),
    ('Nhập Định mức công', 'Change / Blur',
     'After:\n– Hệ thống tính lại Công kỹ thuật nếu ô đó đang để trống.'),
    ('Bấm thêm thiết bị / vật tư / dịch vụ', 'Click',
     'After:\n– Mở cửa sổ tìm kiếm; chọn xong thì thêm dòng vào bảng con tương ứng.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền “%s”.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng '
     'xử lý.\n'
     'During:\n'
     '– Loại công việc / lỗi để trống → hiển thị “Bắt buộc phải nhập”.\n'
     '– Tên công việc / tình trạng lỗi để trống → hiển thị “Bắt buộc phải nhập”.\n'
     '– Tên đã tồn tại TRONG CÙNG LOẠI → hiển thị thông báo trùng tên.\n'
     '– Định mức công, Định mức giảm giá, VAT, Hệ số công nghệ để trống → hiển thị '
     '“Bắt buộc phải nhập”.\n'
     '– Hệ số công nghệ bằng 0 → hiển thị “Nhập hệ số lớn hơn 0”.\n'
     '– VAT lớn hơn 100 → hiển thị “Tối đa 100”.\n'
     '– Ô số nhập chữ → hiển thị “Phải là số”; nhập số âm → hiển thị “Không được nhỏ hơn 0”.\n'
     '– Chưa thêm thiết bị nào → hiển thị thông báo bắt buộc chọn thiết bị.\n'
     '– Dòng dịch vụ thiếu Giá vốn hoặc Giá dịch vụ → hiển thị “Bắt buộc phải nhập” tại đúng ô '
     'đó trong bảng.\n'
     '– Nếu có lỗi kiểm tra → không thực hiện bước After.\n'
     'After:\n'
     '– Tự tính Công kỹ thuật và Đơn giá bán cho các ô để trống.\n'
     '– Ghi bản ghi mới với trạng thái Hoạt động.\n'
     '– Quay về danh sách và hiển thị thông báo thêm mới thành công.' % QUYEN),
])

# ------------------------------------------------------------------ 2.5
d.h3('2.5 Chỉnh sửa %s' % DT)
d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa %s' % DT, 'crud',
            [('include', 'Kiểm tra quyền “%s”' % QUYEN),
             ('extend', 'Ẩn nút Sửa khi bản ghi đã Khóa')], actor=P1)

d.p('2.5.2 Giới thiệu')
d.intro_table(
    'Chỉnh sửa %s' % DT,
    'Sửa thông tin của một hạng mục đã có. Dùng chung trang với chức năng Thêm mới.',
    P1,
    'Người dùng có quyền “%s”; bản ghi đang ở trạng thái Hoạt động.' % QUYEN,
    '1. Người dùng bấm biểu tượng bút chì ở dòng cần sửa.\n'
    '2. Hệ thống mở trang chỉnh sửa với dữ liệu hiện tại đã điền sẵn.\n'
    '3. Người dùng sửa thông tin và bấm Lưu.\n'
    '4. Hệ thống kiểm tra dữ liệu, ghi nhận thay đổi và quay về danh sách.',
    '• ⚠️ Bản ghi đã Khóa KHÔNG có nút bút chì — phải Mở khóa trước.\n'
    '• Giữ nguyên tên cũ của chính bản ghi đó → lưu bình thường, không báo trùng.\n'
    '• Đổi Loại sang loại đang có hạng mục trùng tên → bị chặn.')

d.p('2.5.3 Layout màn hình')
d.layout(route=C.ROUTE + '/{id}/edit', shot=shot(S['taomoi']),
         shot_caption='Trang nhập liệu dùng chung cho Thêm mới và Chỉnh sửa')

d.p('2.5.4 Mô tả chi tiết giao diện')
rows = [(t[0], t[1], 'Enable', t[2], t[3], 'Dữ liệu hiện tại', t[5]) for t in C.TRUONG]
rows += [
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi thay đổi rồi quay về danh sách.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
]
d.ui_table(rows)

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng bút chì', 'Click',
     'Before:\n– Kiểm tra quyền “%s”; thiếu quyền thì nút không hiển thị.\n'
     '– Bản ghi đã Khóa thì nút này cũng không hiển thị.\n'
     'After:\n– Mở trang chỉnh sửa với dữ liệu hiện tại.' % QUYEN),
    ('Bấm Lưu', 'Click',
     'During:\n– Áp toàn bộ quy tắc kiểm tra như chức năng Thêm mới.\n'
     '– Bỏ qua kiểm tra trùng đối với chính bản ghi đang sửa.\n'
     '– Nếu có lỗi kiểm tra → không thực hiện bước After.\n'
     'After:\n– Ghi nhận thay đổi và ghi một dòng lịch sử.\n'
     '– Quay về danh sách và hiển thị thông báo cập nhật thành công.'),
])

# ------------------------------------------------------------------ 2.6
d.h3('2.6 Xóa %s' % DT)
d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Xóa %s' % DT, 'action',
            [('include', 'Kiểm tra quyền “%s”' % QUYEN),
             ('include', 'Xác nhận trước khi thực hiện'),
             ('extend', 'Ẩn nút Xóa khi đã phát sinh chứng từ')], actor=P1)

d.p('2.6.2 Giới thiệu')
d.intro_table(
    'Xóa %s' % DT,
    'Loại một hạng mục khỏi danh mục.',
    P1,
    'Người dùng có quyền “%s”; bản ghi đang Hoạt động VÀ chưa phát sinh chứng từ nào.' % QUYEN,
    '1. Người dùng bấm biểu tượng thùng rác ở dòng cần xóa.\n'
    '2. Hệ thống hiện hộp xác nhận nêu rõ tên hạng mục.\n'
    '3. Người dùng bấm Xóa để xác nhận.\n'
    '4. Hệ thống loại bản ghi khỏi danh sách và hiển thị thông báo thành công.',
    '• ⚠️ Nút Xóa CHỈ hiển thị khi bản ghi đang Hoạt động VÀ chưa phát sinh chứng từ. Thiếu một '
    'trong hai điều kiện thì nút biến mất hẳn.\n'
    '• Bấm Hủy → đóng hộp, không thay đổi gì.',
    'Hạng mục đã phát sinh chứng từ thì dùng thao tác Khóa thay cho Xóa.')

d.p('2.6.3 Layout màn hình')
d.layout(modal='Xác nhận xóa', shot=shot(S['menu']),
         shot_caption='Cột Hành động — Sửa và Xóa hiện thẳng, các thao tác còn lại nằm trong '
                      'nút ba chấm')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Biểu tượng thùng rác', 'Icon Button', 'Enable / Ẩn', 'Ẩn khi không xóa được',
     'Chỉ hiện khi bản ghi đang Hoạt động và chưa phát sinh chứng từ.'),
    ('Nội dung hộp xác nhận', 'Label', 'Hiển thị', 'Nêu rõ tên hạng mục',
     'Giúp tránh thao tác nhầm dòng.'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Xác nhận thực hiện.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không làm gì.'),
], required=False, scope=False)

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng thùng rác', 'Click',
     'Before:\n– Bản ghi đã Khóa hoặc đã phát sinh chứng từ thì nút này KHÔNG hiển thị.\n'
     'After:\n– Hiện hộp xác nhận kèm tên hạng mục.'),
    ('Bấm Xóa trong hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra quyền “%s”; thiếu quyền thì từ chối và dừng xử lý.\n'
     'After:\n– Loại bản ghi khỏi danh sách, nạp lại và hiển thị thông báo xóa thành công.'
     % QUYEN),
    ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp xác nhận, không thay đổi gì.'),
])

# ------------------------------------------------------------------ 2.7
d.h3('2.7 Khóa / Mở khóa %s' % DT)
d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Khóa / Mở khóa %s' % DT, 'action',
            [('include', 'Kiểm tra quyền “%s”' % QUYEN),
             ('include', 'Xác nhận trước khi thực hiện'),
             ('extend', 'Khóa KHÔNG xóa dữ liệu, chỉ đổi trạng thái')], actor=P1)

d.p('2.7.2 Giới thiệu')
d.intro_table(
    'Khóa / Mở khóa %s' % DT,
    'Đổi trạng thái hạng mục qua lại giữa Hoạt động và Khóa. Hạng mục đã Khóa vẫn nằm trong '
    'danh mục nhưng không chọn được khi lập báo giá hoặc phiếu sửa chữa mới.',
    P1,
    'Người dùng có quyền “%s”.' % QUYEN,
    '1. Người dùng mở nút ba chấm ở dòng cần thao tác và chọn Khóa (hoặc Mở khóa).\n'
    '2. Hệ thống hiện hộp xác nhận nêu rõ tên hạng mục.\n'
    '3. Người dùng xác nhận.\n'
    '4. Hệ thống đổi trạng thái và cập nhật lại danh sách.',
    '• Sau khi Khóa, hai nút Sửa và Xóa của dòng đó biến mất; chỉ còn Mở khóa, In và Lịch sử.\n'
    '• Bấm Hủy → đóng hộp, trạng thái không đổi.')

d.p('2.7.3 Layout màn hình')
d.layout(modal='Xác nhận khóa', shot=shot(S['khoa']),
         shot_caption='Hộp xác nhận khóa hạng mục')

d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mục Khóa / Mở khóa trong nút ba chấm', 'Button', 'Enable / Ẩn', 'Ẩn khi thiếu quyền',
     'Nhãn đổi theo trạng thái hiện tại của dòng.'),
    ('Tiêu đề hộp xác nhận', 'Label', 'Hiển thị', 'Xác nhận khóa',
     'Đổi thành Xác nhận mở khóa khi bản ghi đang Khóa.'),
    ('Nội dung hộp xác nhận', 'Label', 'Hiển thị', 'Nêu rõ tên hạng mục', '–'),
    ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Xác nhận thực hiện.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không làm gì.'),
], required=False, scope=False)

d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Khóa trong nút ba chấm', 'Click',
     'Before:\n– Kiểm tra quyền “%s”; thiếu quyền thì mục này không hiển thị.\n'
     'After:\n– Hiện hộp xác nhận kèm tên hạng mục.' % QUYEN),
    ('Xác nhận Khóa / Mở khóa', 'Click',
     'During:\n– Bản ghi không còn tồn tại hoặc đã ở trạng thái đích → hiển thị thông báo dữ '
     'liệu đã thay đổi.\n'
     'After:\n– Đổi trạng thái; KHÔNG xóa bất kỳ dữ liệu nào.\n'
     '– Cập nhật lại cột Trạng thái và tập nút trên cột Hành động của dòng đó.'),
])

# ------------------------------------------------------------------ 2.8
d.h3('2.8 In và Xuất Excel')
d.p('2.8.1 Giới thiệu')
d.intro_table(
    'In danh sách và Xuất Excel',
    'Xuất kết quả đang lọc ra tệp bảng tính, hoặc mở bản in danh sách. Ngoài ra mỗi dòng có thao '
    'tác In riêng để in chi tiết một hạng mục.',
    P1,
    'Người dùng có quyền “%s”.' % QUYEN,
    '1. Người dùng lọc danh sách theo nhu cầu.\n'
    '2. Người dùng bấm Xuất Excel hoặc In danh sách.\n'
    '3. Hệ thống sinh tệp hoặc mở bản in theo đúng bộ lọc đang áp dụng.',
    '• In một dòng: chọn In trong nút ba chấm của dòng đó, hệ thống mở bản in chi tiết hạng mục.\n'
    '• Bộ lọc không có kết quả → tệp chỉ có dòng tiêu đề, hoặc hệ thống báo không có dữ liệu.',
    'Tệp xuất chứa TOÀN BỘ kết quả lọc, không giới hạn ở trang đang xem. Cột thuế suất được xuất '
    'kèm để đối chiếu.')

d.p('2.8.2 Layout màn hình')
d.layout(shot=shot(S['danhsach']),
         shot_caption='Thanh công cụ với các nút Tạo mới, Xuất Excel và In danh sách')

d.p('2.8.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel', 'Button', 'Enable / Ẩn', 'Ẩn khi thiếu quyền',
     'Xuất toàn bộ kết quả lọc ra tệp bảng tính.'),
    ('Nút In danh sách', 'Button', 'Enable / Ẩn', 'Ẩn khi thiếu quyền',
     'Mở bản in toàn bộ danh sách đang lọc theo mẫu in của hệ thống.'),
    ('Mục In trong nút ba chấm của dòng', 'Button', 'Enable', 'Hiển thị',
     'Mở bản in chi tiết của riêng hạng mục đó.'),
], required=False, scope=False)

d.p('2.8.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Kiểm tra quyền “%s”; thiếu quyền thì nút không hiển thị.\n'
     'After:\n– Sinh tệp bảng tính theo đúng bộ lọc đang áp dụng và tải về.' % QUYEN),
    ('Bấm In danh sách', 'Click',
     'After:\n– Mở bản in toàn bộ danh sách đang lọc, có tiêu đề đầu trang của công ty.'),
    ('Chọn In ở một dòng', 'Click',
     'After:\n– Mở bản in chi tiết của riêng hạng mục đó.'),
])

# ------------------------------------------------------------------ 2.9
d.h3('2.9 Xem lịch sử thay đổi')
d.p('2.9.1 Giới thiệu')
d.intro_table(
    'Xem lịch sử thay đổi',
    'Liệt kê các lần thay đổi của một hạng mục, kèm giá trị cũ, giá trị mới, người thực hiện và '
    'thời điểm.',
    P1,
    'Bản ghi cần xem đang có trong danh sách.',
    '1. Người dùng chọn Lịch sử trong nút ba chấm của dòng.\n'
    '2. Hệ thống mở cửa sổ Lịch sử thay đổi.\n'
    '3. Danh sách hiển thị theo thứ tự mới nhất ở trên cùng.',
    '• Bản ghi chưa từng sửa → cửa sổ hiện “Chưa có lịch sử thao tác nào.”\n'
    '• Chức năng này không gắn quyền, theo quy ước chung của mọi màn danh sách.')

d.p('2.9.2 Layout màn hình')
d.layout(modal='Lịch sử thay đổi', shot=shot(S['lichsu']),
         shot_caption='Cửa sổ Lịch sử thay đổi của một hạng mục')

d.p('2.9.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Lịch sử thay đổi',
     'Kèm dòng phụ ghi loại đối tượng và tên hạng mục.'),
    ('Danh sách thay đổi', 'Table/Grid', 'Read-only', 'Theo dữ liệu',
     'Sắp xếp mới nhất ở trên cùng.'),
    ('Giá trị cũ và giá trị mới', 'Text', 'Read-only', 'Theo dữ liệu',
     'Hiển thị hai vế cho từng trường đã đổi.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', 'Ẩn',
     'Hiện “Chưa có lịch sử thao tác nào.” khi bản ghi chưa từng sửa.'),
    ('Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False, scope=False)

d.p('2.9.4 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Lịch sử trong nút ba chấm', 'Click',
     'After:\n– Mở cửa sổ và nạp danh sách thay đổi theo thứ tự mới nhất trước.'),
    ('Bấm Đóng', 'Click',
     'After:\n– Đóng cửa sổ; danh sách phía sau giữ nguyên bộ lọc và trang.'),
])

# ==================================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.p('BR-01 — Một quyền duy nhất cho cả xem và thao tác')
d.bullets([
    'Màn hình dùng đúng một quyền “%s”, không tách quyền xem riêng.' % QUYEN,
    'Người không có quyền này không thấy mục menu và không truy cập được bằng đường dẫn.',
    'Riêng chức năng Xem lịch sử thay đổi không gắn quyền, theo quy ước chung của mọi màn '
    'danh sách.',
])

d.p('BR-02 — Trùng tên xét theo TỪNG LOẠI')
d.bullets([
    'Tên hạng mục không được trùng TRONG CÙNG MỘT LOẠI công việc / lỗi.',
    'Hai loại khác nhau ĐƯỢC PHÉP có hạng mục trùng tên — ví dụ “Kiểm tra cầu nâng” tồn tại đồng '
    'thời ở loại Lỗi đã xác định và loại Tư vấn, khảo sát.',
    'Vì vậy khi đổi Loại của một hạng mục, hệ thống kiểm tra lại trùng tên trong loại mới.',
    'Khi sửa, bản ghi đang sửa được loại khỏi phép kiểm tra trùng.',
])

d.p('BR-03 — Điều kiện hiển thị của từng nút trên cột Hành động')
d.bullets([
    'Nút Sửa: chỉ hiện khi có quyền VÀ bản ghi đang Hoạt động.',
    'Nút Xóa: chỉ hiện khi có quyền VÀ bản ghi đang Hoạt động VÀ chưa phát sinh chứng từ.',
    'Nút Khóa / Mở khóa: chỉ hiện khi có quyền; nhãn đổi theo trạng thái hiện tại.',
    'Nút In và Lịch sử: luôn hiện, không phụ thuộc trạng thái hay quyền.',
    'Bản ghi đã Khóa vì thế chỉ còn ba thao tác: Mở khóa, In, Lịch sử.',
    'Quy ước chung của dự án: nút không dùng được thì ẩn hẳn, không hiện rồi làm mờ. Điều kiện '
    'hiện/ẩn ở màn danh sách phải khớp với màn chi tiết.',
])

d.p('BR-04 — Trường để trống thì hệ thống tự tính')
d.bullets([
    'Công kỹ thuật để trống → tính tự động từ Định mức công.',
    'Đơn giá bán để trống → tính tự động theo công thức của hệ thống.',
    'Hệ số giá bán dịch vụ và Đơn giá công kỹ thuật để trống → lấy theo cấu hình của công ty '
    'người dùng đang đăng nhập.',
    'Người dùng nhập tay thì giá trị nhập tay được ưu tiên.',
])

d.p('BR-05 — Ràng buộc của các bảng con')
d.bullets([
    'Bảng “Áp dụng cho thiết bị” BẮT BUỘC có ít nhất một dòng.',
    'Bảng “Vật tư thay thế” không bắt buộc.',
    'Bảng “Dịch vụ sửa chữa kèm theo” không bắt buộc, NHƯNG mỗi dòng đã thêm thì phải nhập đủ cả '
    'Giá vốn và Giá dịch vụ; bỏ trống sẽ bị chặn tại đúng ô đó.',
])

d.p('BR-06 — Khóa không phải Xóa')
d.bullets([
    'Khóa chỉ đổi trạng thái, không xóa dữ liệu; hạng mục vẫn nằm trong danh mục.',
    'Hạng mục đã Khóa không chọn được khi lập báo giá hoặc phiếu sửa chữa mới.',
    'Hạng mục đã phát sinh chứng từ không xóa được — dùng Khóa thay thế.',
])

d.p('BR-07 — Lịch sử thay đổi sắp xếp mới nhất trước')
d.bullets([
    'Mọi thao tác sửa và đổi trạng thái đều sinh dòng lịch sử.',
    'Danh sách lịch sử luôn sắp xếp MỚI NHẤT Ở TRÊN CÙNG.',
    'Mỗi dòng nêu trường đã đổi, giá trị cũ, giá trị mới, người thực hiện và thời điểm.',
])

d.save()
