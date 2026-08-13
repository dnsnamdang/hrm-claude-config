# -*- coding: utf-8 -*-
"""Sinh SRS theo FORM CHUAN cho 2 man danh muc bao duong (phan he CSKH):
  1. Cap dich vu bao duong                 -> /customer-care/levels
  2. Danh muc ghi chu kiem tra bao duong   -> /customer-care/note-maintenances

Hai man cung khung chuc nang (list + modal CRUD + xoa co chan rang buoc + xuat Excel)
nen dung chung mot ham dung tai lieu, chi khac phan noi dung khai bao o duoi.

Nguon doi chieu (doc truc tiep tu code):
  BE  Modules/CustomerCare/{Routes/api.php,
        Entities/Level/Level.php, Entities/NoteMaintenance/NoteMaintenance.php,
        Http/Requests/Level/LevelRequest.php,
        Http/Requests/NoteMaintenance/NoteMaintenanceRequest.php}
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (1119-1122)
  FE  hrm-client/pages/customer-care/{levels,note-maintenances}/index.vue
      hrm-client/components/modal/customer-care/{level-modal,note-maintenance-modal}.vue
      hrm-client/components/subsystem-menu/customer-care.js
"""
import os
import sys

# Console Windows mac dinh cp1252 -> print() chuoi tieng Viet se nem UnicodeEncodeError.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 2 module dung chung (srs_docx_lib, srs_uml_render) nam trong assets cua skill srs-documenter
# -> di theo repo, ai clone ve cung chay duoc.
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "srs-documenter", "assets"))
from srs_docx_lib import SrsDoc, ACTOR_P1, ACTOR_BOTH  # noqa: E402

PLANS = (r"d:\CompanyProject\hrm\hrm-claude-config\hrm\.plans\gop-db"
         r"\customer-care-maintenance-catalogs")


def build(cfg):
    d = SrsDoc(out=os.path.join(PLANS, 'SRS - %s.docx' % cfg['screen']),
               menu='Phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → %s' % cfg['screen'],
               route=cfg['route'],
               full_url='https://<host-hrm>%s' % cfg['route'],
               img_prefix=cfg['img'])

    obj = cfg['obj']            # danh tu chi doi tuong, vd "cấp dịch vụ bảo dưỡng"
    n_fn = 8

    # ============================================================ TRANG BIA
    d.h1('SOFTWARE REQUIREMENTS SPECIFICATION (SRS)')
    d.h2('Màn hình: %s' % cfg['screen'])
    d.h2('Phân hệ: Chăm sóc khách hàng (CSKH) – nhóm Danh mục - Dịch vụ')

    d.info_table([
        ('Mã màn hình', cfg['code']),
        ('Đường dẫn', cfg['route']),
        ('Phiên bản', '1.0'),
        ('Ngày lập', '12/08/2026'),
        ('Người lập', '@junfoke'),
        ('Trạng thái tài liệu', 'Draft'),
        ('Nguồn đối chiếu', cfg['source']),
    ])

    # ============================================================ 1. GIOI THIEU
    d.h1('1. Giới thiệu')

    d.h2('1.1 Mục đích')
    d.p('Tài liệu này đặc tả yêu cầu phần mềm (SRS) cho màn hình quản lý %s, nhằm:' % obj)
    d.bullets([
        'Thống nhất yêu cầu giữa BA/PO/Dev/Test',
        'Là căn cứ nghiệm thu chức năng và phân quyền',
        'Làm rõ ràng buộc chặn xoá khi %s đã được dùng ở nghiệp vụ khác — điểm khác biệt '
        'có chủ đích so với màn ERP cũ' % obj,
    ])

    d.h2('1.2 Phạm vi')
    d.p('Màn hình %s cung cấp chức năng:' % cfg['screen'])
    d.bullets(cfg['scope_in'])
    d.p('Ngoài phạm vi:')
    d.bullets(cfg['scope_out'])

    d.h2('1.3 Thuật ngữ và viết tắt')
    d.table(['Thuật ngữ', 'Mô tả'], cfg['glossary'] + [
        ('Đang được sử dụng', 'Bản ghi đã được nghiệp vụ khác tham chiếu nên không được phép xoá'),
        ('P1', 'Quyền “%s”' % cfg['perm_manage']),
        ('P2', 'Quyền “%s”' % cfg['perm_view']),
        ('Quick Search', 'Tìm kiếm nhanh'),
        ('Advanced Filter', 'Bộ lọc nâng cao'),
        ('SRS', 'Software Requirements Specification'),
    ], widths=[1.8, 4.2])

    # ============================================================ 2. TONG QUAN
    d.h1('2. Tổng quan')

    d.h2('2.1 Bối cảnh nghiệp vụ')
    d.p('%s là dữ liệu nền của nghiệp vụ dịch vụ bảo dưỡng, dùng để:' % cfg['screen'])
    d.bullets(cfg['context_use'])
    d.p('Do đó cần:')
    d.bullets(cfg['context_need'])

    d.h2('2.2 Nhóm người dùng')
    d.bullets([
        'Người dùng có quyền P1: được quản lý danh mục (thêm/sửa/xoá) và xuất Excel',
        'Người dùng có quyền P2: chỉ được xem/tra cứu và xuất Excel',
        'Người dùng không có P1/P2: bị chặn truy cập',
    ])

    # ============================================================ 3. PHAN QUYEN
    d.h1('3. Phân quyền và kiểm soát truy cập')

    d.h2('3.1 Danh sách quyền')
    d.table(['Ký hiệu', 'Tên quyền', 'Mã quyền', 'Nhóm quyền'], [
        ('P1', cfg['perm_manage'], cfg['perm_manage_id'], 'Danh mục dịch vụ bảo dưỡng'),
        ('P2', cfg['perm_view'], cfg['perm_view_id'], 'Danh mục dịch vụ bảo dưỡng'),
    ], widths=[0.8, 2.8, 0.9, 1.5])
    d.p('Ghi chú: màn hình tương ứng bên ERP không gate quyền nào, hai quyền trên là quyền mới của HRM.')

    d.h2('3.2 Quy tắc truy cập bắt buộc')
    d.bullets([
        'Chỉ user có P1 hoặc P2 mới được truy cập màn hình.',
        'User không có P1/P2: không hiển thị menu điều hướng tới màn hình.',
        'User không có P1/P2: truy cập trực tiếp URL bị chặn, gọi API trả về lỗi 403.',
        'User chỉ có P2: mọi thao tác ghi (thêm/sửa/xoá) bị chặn ở cả giao diện lẫn API (403), '
        'không phụ thuộc vào việc giao diện có ẩn nút hay không.',
        'Danh sách rút gọn phục vụ ô chọn ở các màn nghiệp vụ khác không gate quyền.',
    ])

    d.h2('3.3 Ma trận phân quyền')
    d.table(['Chức năng', 'P1', 'P2', 'Không có quyền'], [
        ('Truy cập màn', '✅', '✅', '❌'),
        ('Xem danh sách', '✅', '✅', '❌'),
        ('Tìm kiếm nhanh / Lọc nâng cao / Sắp xếp / Phân trang', '✅', '✅', '❌'),
        ('Xem chi tiết', '✅', '✅', '❌'),
        ('Thêm mới', '✅', '❌', '❌'),
        ('Chỉnh sửa', '✅', '❌', '❌'),
        ('Xoá', '✅', '❌', '❌'),
        ('Xuất Excel', '✅', '✅', '❌'),
    ], widths=[3.0, 0.8, 0.8, 1.4])

    # ============================================================ 4. FUNCTION LIST
    d.h1('4. Danh mục chức năng (Function list)')
    d.table(['ID', 'Chức năng', 'Mô tả đặc tả thu nhỏ (Mini-Spec)', 'Quyền'], [
        ('FR-01', 'Truy cập màn hình',
         'Kiểm tra quyền P1/P2. Không có quyền sẽ bị chặn (ẩn menu, chặn URL, API trả 403).',
         'P1, P2'),
        ('FR-02', 'Xem danh sách', cfg['fr02'], 'P1, P2'),
        ('FR-03', 'Tìm kiếm & Lọc', cfg['fr03'], 'P1, P2'),
        ('FR-04', 'Thêm mới', cfg['fr04'], 'P1'),
        ('FR-05', 'Chỉnh sửa',
         'Mở modal nạp sẵn dữ liệu, cho phép sửa toàn bộ trường. Ràng buộc không trùng vẫn được '
         'kiểm tra và bỏ qua chính bản ghi đang sửa.', 'P1'),
        ('FR-06', 'Xem chi tiết',
         'Mở modal ở chế độ chỉ đọc, mọi trường bị vô hiệu hoá và ẩn nút Lưu.', 'P1, P2'),
        ('FR-07', 'Xoá',
         'Xoá bản ghi sau khi xác nhận. Chặn khi %s đã được dùng ở nghiệp vụ khác.' % obj, 'P1'),
        ('FR-08', 'Xuất Excel',
         'Xuất danh sách theo đúng bộ lọc đang áp dụng ra file Excel.', 'P1, P2'),
    ], widths=[0.7, 1.4, 3.4, 0.8])

    # ============================================================ 5. DAC TA
    d.h1('5. Đặc tả chi tiết theo từng chức năng (FUNCTIONAL PACKAGING)')

    d.h2('5.1 Sơ đồ UML tổng quan')
    d.p('Sơ đồ Use Case tổng quan của màn hình, thể hiện quan hệ giữa hai nhóm người dùng và '
        'tám chức năng:')
    d.overview_figure(
        'HỆ THỐNG HRM — %s' % cfg['screen'],
        [(ACTOR_P1, list(range(n_fn))),
         ('Người xem danh mục (P2)', [0, 1, 2, 5, 7])],
        [('FR-01', 'Truy cập màn hình', 'view', None),
         ('FR-02', 'Xem danh sách', 'view', None),
         ('FR-03', 'Tìm kiếm & Lọc', 'view', None),
         ('FR-04', 'Thêm mới', 'crud', None),
         ('FR-05', 'Chỉnh sửa', 'crud', None),
         ('FR-06', 'Xem chi tiết', 'view', None),
         ('FR-07', 'Xoá', 'action', '«include» Kiểm tra dữ liệu đang sử dụng'),
         ('FR-08', 'Xuất Excel', 'io', None)],
        'Sơ đồ Use Case tổng quan màn hình %s' % cfg['screen'])

    d.h2('5.2 Đặc tả chi tiết từng chức năng')

    # ---------------------------------------------------- 5.2.1 TRUY CAP
    d.h2('5.2.1 Truy cập màn hình %s' % cfg['screen_lower'])

    d.h3('5.2.1.1 Biểu đồ Usecase')
    d.uc_figure('FR-01', 'Truy cập màn hình %s' % cfg['screen_lower'], 'view',
                [('include', 'Kiểm tra quyền truy cập')], actor=ACTOR_BOTH)

    d.h3('5.2.1.2 Giới thiệu')
    d.intro_table(
        'Truy cập màn hình %s' % cfg['screen_lower'],
        'Cho phép người dùng truy cập vào màn hình quản lý %s để tra cứu và quản lý dữ liệu.' % obj,
        'Admin; User được phân quyền (P1 hoặc P2)',
        'Người dùng đã đăng nhập thành công vào hệ thống.',
        '1. Người dùng chọn menu Chăm sóc khách hàng → Danh mục - Dịch vụ → %s.\n' % cfg['screen'] +
        '2. Hệ thống xác thực quyền truy cập (P1 hoặc P2).\n'
        '3. Hệ thống điều hướng tới màn hình danh sách và tải dữ liệu trang đầu tiên.\n'
        '4. Hệ thống khôi phục bộ lọc đã lưu của lần truy cập trước (nếu còn hiệu lực).',
        '• Người dùng không có quyền → Hệ thống ẩn menu; truy cập trực tiếp URL bị chặn.\n'
        '• Gọi trực tiếp API khi không có quyền → Hệ thống trả về lỗi 403.',
        '')

    d.h3('5.2.1.3 Layout màn hình')
    d.layout('Ghi chú: tài liệu này không đính kèm ảnh chụp màn hình, người đọc truy cập trực tiếp '
             'đường dẫn trên để đối chiếu giao diện.')

    d.h3('5.2.1.4 Tiêu chí nghiệm thu')
    d.p('Người dùng có quyền truy cập:')
    d.bullets([
        'Nhìn thấy menu %s.' % cfg['screen'],
        'Truy cập được màn hình danh sách.',
        'Hiển thị mặc định: danh sách phải hiển thị đúng cấu trúc bảng gồm %s.' % cfg['columns_text'],
    ])
    d.p('Người dùng không có quyền:')
    d.bullets([
        'Không nhìn thấy menu.',
        'Truy cập trực tiếp URL bị chặn, gọi API trả về 403.',
    ])

    d.h3('5.2.1.5 Danh sách event và xử lý event')
    d.event_table([
        ('Click menu %s' % cfg['screen'], 'Click',
         'Kiểm tra quyền (P1 hoặc P2) và điều hướng tới màn hình danh sách.'),
        ('Truy cập URL trực tiếp', 'System',
         'Kiểm tra quyền; nếu không hợp lệ → chặn truy cập (giao diện) và trả về lỗi 403 (API).'),
        ('Load màn hình', 'System', 'Khôi phục bộ lọc đã lưu và tải danh sách trang 1.'),
    ])

    # ---------------------------------------------------- 5.2.2 XEM DS
    d.h2('5.2.2 Xem danh sách %s' % obj)

    d.h3('5.2.2.1 Giới thiệu')
    d.intro_table(
        'Xem danh sách %s' % obj,
        cfg['list_desc'],
        'Admin; User được phân quyền (P1 hoặc P2)',
        'Người dùng truy cập thành công màn hình %s.' % cfg['screen_lower'],
        '1. Hệ thống lấy danh sách theo bộ lọc hiện tại.\n'
        '2. Hệ thống hiển thị danh sách theo phân trang.\n'
        '3. Hệ thống xác định với mỗi bản ghi có được phép xoá hay không để bật hoặc vô hiệu hoá '
        'nút Xoá tương ứng.',
        '• Không có dữ liệu → Hiển thị danh sách trống kèm thông báo không có dữ liệu.\n'
        '• Bản ghi chưa từng được cập nhật → Cột Cập nhật để trống.',
        cfg['list_special'])

    d.h3('5.2.2.2 Layout màn hình')
    d.layout()

    d.h3('5.2.2.3 Mô tả chi tiết giao diện')
    d.ui_table(cfg['list_ui'] + [
        ('Xem', 'Icon Button', 'Enable', '–', '–', '–', 'Mở modal xem chi tiết ở chế độ chỉ đọc'),
        ('Sửa', 'Icon Button', 'Enable / Ẩn', '–', '–', '–', 'Mở modal chỉnh sửa. Ẩn khi không có P1'),
        ('Xoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
         'Ẩn khi không có P1; vô hiệu hoá khi bản ghi đang được sử dụng, chú giải nêu nơi đang dùng'),
        ('Tạo mới', 'Button', 'Enable / Ẩn', '–', '–', '–', 'Mở modal thêm mới. Ẩn khi không có P1'),
        ('Xuất Excel', 'Button', 'Enable', '–', '–', '–', 'Tải file Excel theo bộ lọc hiện tại'),
        ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1', 'Điều hướng giữa các trang danh sách'),
        ('Chọn số dòng/trang', 'Dropdown', 'Enable', 'Danh sách', 'Không', '10',
         'Thay đổi số bản ghi hiển thị mỗi trang'),
        ('Trạng thái rỗng', 'Label', 'Enable', '–', '–', 'Ẩn', 'Hiển thị khi danh sách trống'),
        ('Loading', 'Loading', 'Hiển thị', '–', '–', 'Ẩn', 'Hiển thị trong lúc chờ tải danh sách'),
    ])

    d.h3('5.2.2.4 Tiêu chí nghiệm thu')
    d.bullets(cfg['list_accept'] + [
        'Bản ghi đang được nghiệp vụ khác sử dụng thì nút Xoá bị vô hiệu hoá, chú giải nêu nơi đang dùng.',
        'Vào màn hình chỉ phát sinh đúng một yêu cầu tải danh sách, không tải lặp.',
        'Phân trang hoạt động đúng, không trùng hoặc thiếu dữ liệu.',
    ])

    d.h3('5.2.2.5 Danh sách event và xử lý event')
    d.event_table([
        ('Load danh sách', 'System',
         'Tải danh sách theo bộ lọc và phân trang hiện tại; hiển thị hiệu ứng chờ trong lúc tải.'),
        ('Đổi trang', 'Click', 'Tải lại danh sách theo trang mới, giữ nguyên bộ lọc.'),
        ('Đổi số dòng/trang', 'Change', 'Tải lại danh sách với số dòng mới, quay về trang 1.'),
        ('Rê chuột lên nút Xoá bị vô hiệu hoá', 'Hover',
         'Hiển thị chú giải nêu các nghiệp vụ đang sử dụng bản ghi.'),
    ])

    # ---------------------------------------------------- 5.2.3 TIM KIEM
    d.h2('5.2.3 Tìm kiếm và lọc danh sách %s' % obj)

    d.h3('5.2.3.1 Giới thiệu')
    d.intro_table(
        'Tìm kiếm và lọc danh sách %s' % obj,
        'Cho phép người dùng thu hẹp danh sách theo từ khoá hoặc theo từng tiêu chí, và sắp xếp '
        'danh sách theo cột mong muốn.',
        'Admin; User được phân quyền (P1 hoặc P2)',
        'Người dùng đang ở màn hình danh sách %s.' % obj,
        cfg['search_flow'],
        '• Bấm Làm mới → Hệ thống xoá toàn bộ điều kiện lọc và tải lại danh sách đầy đủ.\n'
        '• Không có kết quả → Hiển thị danh sách trống kèm thông báo.\n'
        '• Thay đổi tiêu chí ở bộ lọc nâng cao → Hệ thống tự tìm lại ngay, không cần bấm Tìm kiếm.',
        '• Ô tìm kiếm nhanh chỉ áp dụng khi người dùng bấm Tìm kiếm, để tránh gọi lại danh sách '
        'sau mỗi ký tự gõ vào.\n'
        '• Điều kiện lọc được ghi nhớ và dùng lại khi quay về màn hình.')

    d.h3('5.2.3.2 Layout màn hình')
    d.layout()

    d.h3('5.2.3.3 Mô tả chi tiết giao diện')
    d.ui_table(cfg['search_ui'] + [
        ('Tìm kiếm', 'Button', 'Enable', '–', '–', '–', 'Áp dụng bộ lọc và quay về trang 1'),
        ('Làm mới', 'Button', 'Enable', '–', '–', '–', 'Xoá toàn bộ điều kiện lọc và tải lại danh sách'),
        ('Tiêu đề cột sắp xếp', 'Button', 'Enable', cfg['sortable'], '–', 'Không sắp xếp',
         'Bấm để đổi chiều sắp xếp; sắp xếp thực hiện phía máy chủ'),
    ])

    d.h3('5.2.3.4 Tiêu chí nghiệm thu')
    d.bullets(cfg['search_accept'] + [
        'Từ khoá chứa ký tự đặc biệt của phép tìm gần đúng vẫn được tìm như ký tự thông thường, '
        'không trả về toàn bộ danh sách.',
        'Bấm Tìm kiếm luôn quay về trang 1.',
        'Bấm Làm mới thì danh sách được tải lại đầy đủ, không giữ điều kiện cũ.',
    ])

    d.h3('5.2.3.5 Danh sách event và xử lý event')
    d.event_table([
        ('Nhập ô tìm kiếm nhanh', 'Keypress', 'Ghi nhận từ khoá, chưa gọi tìm kiếm.'),
        ('Bấm Tìm kiếm', 'Click', 'Quay về trang 1 và tải lại danh sách theo toàn bộ điều kiện lọc.'),
        ('Đổi tiêu chí lọc nâng cao', 'Change',
         'Quay về trang 1 và tải lại danh sách ngay theo điều kiện mới.'),
        ('Bấm Làm mới', 'Click', 'Xoá toàn bộ điều kiện lọc, quay về trang 1 và tải lại danh sách.'),
        ('Bấm tiêu đề cột', 'Click',
         'Đổi cột và chiều sắp xếp, tải lại danh sách. Cột không nằm trong danh sách được phép '
         'sắp xếp thì bỏ qua điều kiện sắp xếp.'),
    ])

    # ---------------------------------------------------- 5.2.4 THEM MOI
    d.h2('5.2.4 Thêm mới %s' % obj)

    d.h3('5.2.4.1 Biểu đồ Usecase')
    d.uc_figure('FR-04', 'Thêm mới %s' % obj, 'crud', cfg['uc_add_rel'])

    d.h3('5.2.4.2 Giới thiệu')
    d.intro_table(
        'Thêm mới %s' % obj,
        'Cho phép người quản lý danh mục khai báo một %s mới.' % obj,
        'Admin; User được phân quyền P1',
        'Người dùng đang ở màn hình danh sách và có quyền quản lý %s.' % obj,
        cfg['add_flow'],
        '• Người dùng bấm Lưu & Tiếp tục → Hệ thống lưu bản ghi rồi giữ modal mở với các trường '
        'trống để nhập tiếp.\n'
        '• Người dùng bấm Đóng → Hệ thống đóng modal, không lưu gì.\n'
        '• Dữ liệu không hợp lệ → Hệ thống hiển thị lỗi ngay dưới từng trường và không lưu.',
        cfg['add_special'])

    d.h3('5.2.4.3 Layout màn hình')
    d.layout(modal=cfg['modal_add'])

    d.h3('5.2.4.4 Mô tả chi tiết giao diện')
    d.ui_table([('Modal %s' % cfg['modal_add'], 'Modal', 'Enable', '–', '–', 'Ẩn',
                 'Mở khi bấm Tạo mới; tiêu đề “%s”' % cfg['modal_add'])]
               + cfg['form_ui'] + [
        ('Lưu', 'Button', 'Enable', '–', '–', '–',
         'Kiểm tra hợp lệ và ghi bản ghi; vô hiệu hoá trong lúc đang gửi'),
        ('Lưu & Tiếp tục', 'Button', 'Enable', '–', '–', '–',
         'Ghi bản ghi và giữ modal mở để nhập tiếp; chỉ hiển thị ở chế độ thêm mới'),
        ('Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng modal, không lưu'),
        ('Thông báo lỗi theo trường', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         'Hiển thị ngay dưới trường tương ứng kèm viền đỏ'),
    ])

    d.h3('5.2.4.5 Tiêu chí nghiệm thu')
    d.bullets(cfg['add_accept'] + [
        'Nhập quá 255 ký tự ở bất kỳ trường nào thì hiển thị lỗi “Tối đa 255 ký tự”.',
        'Bấm Lưu & Tiếp tục thì modal vẫn mở với các trường trống và danh sách phía sau đã có '
        'bản ghi mới.',
        'Người dùng chỉ có P2 gọi trực tiếp API tạo mới thì bị từ chối với lỗi 403.',
    ])

    d.h3('5.2.4.6 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm Tạo mới', 'Click',
         'Before:\n– Kiểm tra quyền P1; không có quyền thì nút không hiển thị.\n'
         'After:\n– Xoá dữ liệu cũ trong modal và mở modal %s.' % cfg['modal_add']),
        ('Bấm Lưu', 'Click',
         'Before:\n– Kiểm tra quyền P1.\n'
         '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
         'During:\n' + cfg['add_validate'] +
         '– Nếu có lỗi validate → không thực hiện bước After.\n'
         'After:\n– Ghi bản ghi mới vào danh mục.\n'
         '– Hiển thị thông báo thành công, đóng modal và tải lại danh sách.'),
        ('Bấm Lưu & Tiếp tục', 'Click',
         'Xử lý như bấm Lưu; sau khi ghi thành công thì giữ modal mở và xoá trắng các trường.'),
        ('Bấm Đóng', 'Click', 'Đóng modal và xoá dữ liệu đang nhập dở, không lưu bất kỳ thay đổi nào.'),
    ])

    # ---------------------------------------------------- 5.2.5 CHINH SUA
    d.h2('5.2.5 Chỉnh sửa %s' % obj)

    d.h3('5.2.5.1 Biểu đồ Usecase')
    d.uc_figure('FR-05', 'Chỉnh sửa %s' % obj, 'crud', cfg['uc_add_rel'])

    d.h3('5.2.5.2 Giới thiệu')
    d.intro_table(
        'Chỉnh sửa %s' % obj,
        'Cho phép người quản lý danh mục cập nhật thông tin của một %s đã khai báo.' % obj,
        'Admin; User được phân quyền P1',
        'Bản ghi đang tồn tại; người dùng có quyền quản lý %s.' % obj,
        '1. Người dùng bấm biểu tượng Sửa ở dòng cần chỉnh sửa.\n'
        '2. Hệ thống mở modal chỉnh sửa và nạp sẵn dữ liệu hiện tại.\n'
        '3. Người dùng chỉnh sửa các trường cần thay đổi.\n'
        '4. Người dùng bấm Lưu.\n'
        '5. Hệ thống kiểm tra hợp lệ rồi cập nhật bản ghi.\n'
        '6. Hệ thống hiển thị thông báo thành công, đóng modal và tải lại danh sách.',
        '• Bản ghi đã bị xoá bởi người dùng khác → Hệ thống báo dữ liệu đã thay đổi và yêu cầu tải lại.\n'
        '• Giá trị mới trùng với bản ghi khác → Hệ thống báo lỗi và không lưu.',
        'Phép kiểm tra trùng bỏ qua chính bản ghi đang sửa, nên giữ nguyên giá trị cũ vẫn lưu được.')

    d.h3('5.2.5.3 Layout màn hình')
    d.layout(modal=cfg['modal_edit'])

    d.h3('5.2.5.4 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Modal %s' % cfg['modal_edit'], 'Modal', 'Enable', '–', '–', 'Ẩn',
         'Mở khi bấm biểu tượng Sửa; tiêu đề “%s”' % cfg['modal_edit']),
        ('Thông tin cập nhật gần nhất', 'Label', 'Read-only', '–', '–', 'Lấy từ hệ thống',
         'Hiển thị trên tiêu đề modal khi bản ghi đã có lịch sử cập nhật'),
    ] + [(r[0], r[1], r[2], r[3], r[4], 'Lấy từ hệ thống', r[6]) for r in cfg['form_ui']] + [
        ('Lưu', 'Button', 'Enable', '–', '–', '–', 'Kiểm tra hợp lệ và cập nhật bản ghi'),
        ('Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng modal, huỷ thay đổi chưa lưu'),
    ])

    d.h3('5.2.5.5 Tiêu chí nghiệm thu')
    d.bullets([
        'Modal nạp đúng dữ liệu của dòng được chọn.',
        'Đổi giá trị trùng với bản ghi khác thì báo lỗi và không lưu.',
        'Giữ nguyên giá trị của chính bản ghi đang sửa thì lưu được bình thường.',
        'Sau khi lưu, danh sách hiển thị đúng giá trị mới.',
        'Người dùng chỉ có P2 gọi trực tiếp API cập nhật thì bị từ chối với lỗi 403.',
    ])

    d.h3('5.2.5.6 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm biểu tượng Sửa', 'Click',
         'Before:\n– Kiểm tra quyền P1; không có quyền thì biểu tượng không hiển thị.\n'
         'After:\n– Nạp dữ liệu bản ghi và mở modal %s.' % cfg['modal_edit']),
        ('Bấm Lưu', 'Click',
         'Before:\n– Kiểm tra quyền P1.\n'
         '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
         'During:\n' + cfg['add_validate'] +
         '– Nếu có lỗi validate → không thực hiện bước After.\n'
         'After:\n– Cập nhật bản ghi.\n'
         '– Hiển thị thông báo thành công, đóng modal và tải lại danh sách.'),
        ('Bản ghi không còn tồn tại', 'System',
         'Hiển thị thông báo dữ liệu đã thay đổi và yêu cầu tải lại danh sách.'),
    ])

    # ---------------------------------------------------- 5.2.6 XEM CHI TIET
    d.h2('5.2.6 Xem chi tiết %s' % obj)

    d.h3('5.2.6.1 Giới thiệu')
    d.intro_table(
        'Xem chi tiết %s' % obj,
        'Cho phép người dùng xem đầy đủ thông tin của một bản ghi mà không thay đổi dữ liệu.',
        'Admin; User được phân quyền (P1 hoặc P2)',
        'Bản ghi đang tồn tại; người dùng đang ở màn hình danh sách.',
        '1. Người dùng bấm biểu tượng Xem ở dòng cần xem.\n'
        '2. Hệ thống mở modal ở chế độ chỉ đọc và nạp dữ liệu bản ghi.\n'
        '3. Người dùng xem xong thì bấm Đóng.',
        '• Không có quyền → Hệ thống trả về lỗi 403 và không mở modal.\n'
        '• Bản ghi không còn tồn tại → Hệ thống báo dữ liệu đã thay đổi và yêu cầu tải lại.',
        'Ở chế độ chỉ đọc, toàn bộ trường nhập bị vô hiệu hoá và các nút Lưu không hiển thị.')

    d.h3('5.2.6.2 Layout màn hình')
    d.layout(modal=cfg['modal_view'])

    d.h3('5.2.6.3 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Modal %s' % cfg['modal_view'], 'Modal', 'Read-only', '–', '–', 'Ẩn',
         'Tiêu đề “%s”' % cfg['modal_view']),
    ] + [(r[0], r[1], 'Disable', '–', '–', 'Lấy từ hệ thống', 'Chỉ đọc') for r in cfg['form_ui']] + [
        ('Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng modal'),
    ])

    d.h3('5.2.6.4 Tiêu chí nghiệm thu')
    d.bullets([
        'Modal mở ở chế độ chỉ đọc, không sửa được bất kỳ trường nào.',
        'Nút Lưu và Lưu & Tiếp tục không hiển thị.',
        'Người dùng chỉ có P2 vẫn xem được chi tiết.',
    ])

    d.h3('5.2.6.5 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm biểu tượng Xem', 'Click', 'Nạp dữ liệu bản ghi và mở modal ở chế độ chỉ đọc.'),
        ('Bấm Đóng', 'Click', 'Đóng modal và xoá dữ liệu đang hiển thị.'),
    ])

    # ---------------------------------------------------- 5.2.7 XOA
    d.h2('5.2.7 Xoá %s' % obj)

    d.h3('5.2.7.1 Biểu đồ Usecase')
    d.uc_figure('FR-07', 'Xoá %s' % obj, 'action',
                [('include', 'Kiểm tra dữ liệu đang sử dụng')])

    d.h3('5.2.7.2 Giới thiệu')
    d.intro_table(
        'Xoá %s' % obj,
        'Cho phép người quản lý danh mục xoá một bản ghi khai báo nhầm hoặc không còn dùng, '
        'với điều kiện bản ghi đó chưa được nghiệp vụ nào sử dụng.',
        'Admin; User được phân quyền P1',
        'Bản ghi đang tồn tại; người dùng có quyền quản lý %s.' % obj,
        '1. Người dùng bấm biểu tượng Xoá ở dòng cần xoá.\n'
        '2. Hệ thống hiển thị hộp thoại xác nhận nêu rõ tên bản ghi.\n'
        '3. Người dùng xác nhận.\n'
        '4. Hệ thống kiểm tra lại ràng buộc sử dụng rồi xoá bản ghi.\n'
        '5. Hệ thống hiển thị thông báo thành công và tải lại danh sách.',
        '• Bản ghi đang được sử dụng → Nút Xoá bị vô hiệu hoá, chú giải nêu tối đa 3 nơi đang dùng.\n'
        '• Người dùng bấm Huỷ → Hệ thống đóng hộp thoại, không xoá gì.\n'
        '• Dữ liệu phát sinh ngay giữa lúc thao tác → Hệ thống chặn ở lần kiểm tra tại máy chủ.',
        cfg['delete_special'])

    d.h3('5.2.7.3 Layout màn hình')
    d.layout()

    d.h3('5.2.7.4 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Biểu tượng Xoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
         'Ẩn khi không có P1; vô hiệu hoá khi bản ghi đang được sử dụng'),
        ('Chú giải nút Xoá', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
         'Hiện khi rê chuột: “Xóa” hoặc thông báo nêu nơi đang sử dụng'),
        ('Hộp thoại xác nhận xoá', 'Modal', 'Enable', '–', '–', 'Ẩn',
         'Tiêu đề “Xác nhận xóa”, nội dung nêu rõ tên bản ghi'),
        ('Xoá', 'Button', 'Enable', '–', '–', '–', 'Xác nhận xoá bản ghi'),
        ('Huỷ', 'Button', 'Enable', '–', '–', '–', 'Đóng hộp thoại, không xoá'),
        ('Thông báo chặn xoá', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         'Nêu tên các nghiệp vụ đang sử dụng bản ghi (tối đa 3 nơi)'),
    ])

    d.h3('5.2.7.5 Tiêu chí nghiệm thu')
    d.bullets(cfg['delete_accept'] + [
        'Thông báo chặn xoá nêu tối đa 3 nơi đang sử dụng.',
        'Bấm Huỷ ở hộp thoại thì bản ghi vẫn còn nguyên.',
        'Người dùng chỉ có P2 gọi trực tiếp API xoá thì bị từ chối với lỗi 403.',
    ])

    d.h3('5.2.7.6 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm biểu tượng Xoá', 'Click',
         'Before:\n– Kiểm tra quyền P1; không có quyền thì biểu tượng không hiển thị.\n'
         'During:\n– Bản ghi đang được sử dụng → nút bị vô hiệu hoá, chú giải nêu nơi đang dùng.\n'
         'After:\n– Chưa được sử dụng → mở hộp thoại “Xác nhận xóa”.'),
        ('Xác nhận xoá', 'Click',
         'Before:\n– Kiểm tra quyền P1.\n'
         '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
         'During:\n– Kiểm tra lại ràng buộc tại máy chủ; nếu đang được sử dụng → hiển thị thông báo '
         'nêu nơi đang dùng.\n'
         '– Nếu bị chặn → không thực hiện bước After.\n'
         'After:\n– Xoá bản ghi khỏi danh mục.\n'
         '– Hiển thị thông báo thành công và tải lại danh sách.'),
        ('Bấm Huỷ', 'Click', 'Đóng hộp thoại, không xoá bản ghi.'),
    ])

    # ---------------------------------------------------- 5.2.8 XUAT EXCEL
    d.h2('5.2.8 Xuất Excel danh sách %s' % obj)

    d.h3('5.2.8.1 Giới thiệu')
    d.intro_table(
        'Xuất Excel danh sách %s' % obj,
        'Cho phép người dùng tải danh sách ra file Excel để đối chiếu hoặc gửi ra ngoài.',
        'Admin; User được phân quyền (P1 hoặc P2)',
        'Người dùng đang ở màn hình danh sách %s.' % obj,
        '1. Người dùng áp dụng bộ lọc mong muốn (không bắt buộc).\n'
        '2. Người dùng bấm nút Xuất Excel.\n'
        '3. Hệ thống dựng file theo đúng bộ lọc đang áp dụng và trả về cho trình duyệt tải xuống.',
        '• Không có dữ liệu khớp bộ lọc → Hệ thống vẫn trả file chỉ gồm dòng tiêu đề.\n'
        '• Xảy ra lỗi trong lúc dựng file → Hệ thống hiển thị thông báo lỗi, không tải file.',
        'File xuất ra lấy toàn bộ dữ liệu khớp bộ lọc, không giới hạn theo trang đang xem.')

    d.h3('5.2.8.2 Layout màn hình')
    d.layout()

    d.h3('5.2.8.3 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Xuất Excel', 'Button', 'Enable', '–', '–', '–', 'Nằm ở thanh thao tác dưới bảng danh sách'),
        ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         'Hiển thị khi không dựng được file'),
    ])

    d.h3('5.2.8.4 Tiêu chí nghiệm thu')
    d.bullets([
        'Dữ liệu trong file khớp đúng bộ lọc đang áp dụng trên màn hình.',
        'File chứa toàn bộ bản ghi khớp bộ lọc, không chỉ các dòng của trang đang xem.',
        'Người dùng chỉ có P2 vẫn xuất được Excel.',
        'Người dùng không có quyền gọi trực tiếp đường dẫn xuất Excel thì bị từ chối với lỗi 403.',
    ])

    d.h3('5.2.8.5 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm Xuất Excel', 'Click',
         'Before:\n– Kiểm tra quyền P1 hoặc P2; không có quyền → trả về lỗi 403.\n'
         'After:\n– Dựng file Excel theo bộ lọc hiện tại và tải xuống.'),
    ])

    # ============================================================ 6. BR
    d.h1('6. Quy tắc nghiệp vụ (Business Rules)')
    for title, items in cfg['rules']:
        d.p(title)
        d.bullets(items)
    d.p('Chức năng liên quan: FR-01 … FR-08.')

    d.save()


# ================================================================================
# 1. CAP DICH VU BAO DUONG
# ================================================================================
LEVEL = dict(
    screen='Cấp dịch vụ bảo dưỡng',
    screen_lower='cấp dịch vụ bảo dưỡng',
    obj='cấp dịch vụ bảo dưỡng',
    code='CSKH-DM-LEVEL',
    route='/customer-care/levels',
    img='lv_',
    source='Màn ERP quản lý cấp dịch vụ bảo dưỡng (bảng levels trên DB gộp)',
    perm_manage='Quản lý cấp dịch vụ bảo dưỡng', perm_manage_id='1119',
    perm_view='Xem cấp dịch vụ bảo dưỡng', perm_view_id='1120',
    columns_text='STT, Tên cấp, Cập nhật, Hành động',
    sortable='Tên cấp / Cập nhật',
    modal_add='Thêm cấp dịch vụ', modal_edit='Sửa cấp dịch vụ', modal_view='Xem cấp dịch vụ',
    scope_in=[
        'Xem danh sách cấp dịch vụ bảo dưỡng và tìm kiếm nhanh theo tên cấp',
        'Sắp xếp phía máy chủ theo Tên cấp và thời điểm cập nhật, có phân trang',
        'Thêm mới, chỉnh sửa, xem chi tiết cấp dịch vụ qua modal ngay trên màn danh sách',
        'Xoá cấp dịch vụ, có kiểm tra ràng buộc dữ liệu ở 6 bảng nghiệp vụ',
        'Xuất danh sách ra file Excel theo đúng bộ lọc đang áp dụng',
    ],
    scope_out=[
        'Nhập dữ liệu từ file Excel (Import), In danh sách, Lịch sử chỉnh sửa — màn hình không có '
        'các chức năng này',
        'Trạng thái Khoá / Mở khoá — dữ liệu gốc không có cột trạng thái',
        'Thay đổi cấu trúc bảng dữ liệu: giữ nguyên dữ liệu dùng chung với hệ thống ERP',
    ],
    glossary=[
        ('Cấp dịch vụ bảo dưỡng', 'Mức độ dịch vụ bảo dưỡng được khai báo để gắn vào gói bảo dưỡng, '
                                  'báo giá và hợp đồng dịch vụ'),
        ('Gói bảo dưỡng', 'Gói dịch vụ bảo dưỡng bán cho khách hàng, gồm nhiều cấp dịch vụ'),
    ],
    context_use=[
        'Cung cấp danh sách cấp dịch vụ cho gói bảo dưỡng và cấp bảo dưỡng của gói dịch vụ',
        'Cung cấp cấp dịch vụ cho báo giá dịch vụ, hợp đồng dịch vụ, phiếu phân công công việc '
        'và phiếu nhập kết quả',
    ],
    context_need=[
        'Phân quyền rõ ràng giữa người quản lý và người chỉ tra cứu',
        'Ràng buộc nghiêm: không cho xoá cấp dịch vụ đã được dùng ở bất kỳ nghiệp vụ nào trong '
        '6 bảng tham chiếu — màn ERP cũ chỉ kiểm tra 1 trong 6 bảng nên xoá được cấp đang dùng '
        'trong hợp đồng và báo giá dịch vụ',
        'Bảo đảm tên cấp không trùng nhau để tránh nhầm lẫn khi chọn',
    ],
    fr02='Hiển thị bảng dữ liệu 4 cột, phân trang, sắp xếp phía máy chủ. Cờ “đang được sử dụng” '
         'được nạp sẵn cho cả trang để vô hiệu hoá nút Xoá.',
    fr03='Tìm kiếm nhanh theo tên cấp, hỗ trợ sắp xếp trên cột Tên cấp và Cập nhật.',
    fr04='Mở modal, nhập Tên cấp (*). Tên cấp không được trùng. Có nút Lưu & Tiếp tục để nhập liên tiếp.',
    list_desc='Hiển thị danh sách các cấp dịch vụ bảo dưỡng đã khai báo kèm thời điểm cập nhật gần nhất.',
    list_special='Cờ “đang được sử dụng” được nạp cho toàn bộ dòng trên trang trong một lượt truy vấn '
                 'chung, thay vì hỏi riêng từng dòng, để danh sách không bị chậm.',
    list_ui=[
        ('Bảng danh sách cấp dịch vụ', 'Table/Grid', 'Enable', '–', '–', '–',
         'Hiển thị danh sách theo phân trang'),
        ('STT', 'Label', 'Enable', '–', '–', '–', 'Số thứ tự bản ghi, tính theo trang hiện tại'),
        ('Tên cấp', 'Text', 'Enable', '0–255 ký tự', '–', 'Lấy từ hệ thống',
         'Tên cấp dịch vụ, tự xuống dòng khi dài. Cho phép sắp xếp'),
        ('Cập nhật', 'Text', 'Enable', 'dd/mm/yyyy', '–', 'Lấy từ hệ thống',
         'Thời điểm cập nhật gần nhất. Cho phép sắp xếp'),
    ],
    list_accept=[
        'Danh sách hiển thị đúng tên cấp và thời điểm cập nhật của từng bản ghi.',
        'Sắp xếp trên cột Tên cấp và Cập nhật đổi đúng thứ tự dữ liệu, không chỉ đổi mũi tên '
        'trên tiêu đề.',
    ],
    search_flow='1. Người dùng nhập từ khoá vào ô tìm kiếm nhanh.\n'
                '2. Người dùng bấm Tìm kiếm.\n'
                '3. Hệ thống lấy danh sách khớp điều kiện, quay về trang 1 và hiển thị kết quả.\n'
                '4. Người dùng có thể bấm tiêu đề cột Tên cấp hoặc Cập nhật để đổi thứ tự sắp xếp.',
    search_ui=[
        ('Khung bộ lọc', 'Modal', 'Enable', '–', '–', 'Thu gọn',
         'Khung “Bộ lọc cấp dịch vụ bảo dưỡng”, có thể mở rộng / thu gọn'),
        ('Tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Tìm theo tên cấp dịch vụ bảo dưỡng'),
    ],
    search_accept=[
        'Tìm kiếm nhanh trả về đúng các cấp có tên chứa từ khoá.',
    ],
    uc_add_rel=[('include', 'Kiểm tra trùng tên cấp')],
    add_flow='1. Người dùng bấm nút Tạo mới → Hệ thống mở modal Thêm cấp dịch vụ với trường trống.\n'
             '2. Người dùng nhập Tên cấp.\n'
             '3. Người dùng bấm Lưu.\n'
             '4. Hệ thống bỏ khoảng trắng thừa ở hai đầu tên cấp.\n'
             '5. Hệ thống kiểm tra hợp lệ rồi ghi bản ghi mới.\n'
             '6. Hệ thống hiển thị thông báo thành công, đóng modal và tải lại danh sách.',
    add_special='Tên cấp phải là duy nhất trong toàn danh mục.',
    form_ui=[
        ('Tên cấp', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
         'Tên cấp dịch vụ bảo dưỡng, không được trùng'),
    ],
    add_accept=[
        'Bỏ trống Tên cấp thì không lưu được và hiển thị lỗi “Bắt buộc phải nhập”.',
        'Nhập tên cấp đã tồn tại thì hiển thị lỗi “Tên cấp đã tồn tại”.',
        'Nhập tên có khoảng trắng thừa ở hai đầu thì bản ghi lưu xuống đã được cắt bỏ khoảng trắng.',
    ],
    add_validate='– Tên cấp trống → hiển thị “Bắt buộc phải nhập”\n'
                 '– Tên cấp trùng → hiển thị “Tên cấp đã tồn tại”\n'
                 '– Tên cấp vượt 255 ký tự → hiển thị “Tối đa 255 ký tự”\n',
    delete_special='• Ràng buộc chặn xoá kiểm tra đủ 6 bảng nghiệp vụ đang tham chiếu cấp dịch vụ: '
                   'gói bảo dưỡng, cấp bảo dưỡng của gói dịch vụ, báo giá dịch vụ, hợp đồng dịch vụ, '
                   'phiếu phân công công việc và phiếu nhập kết quả.\n'
                   '• Màn ERP cũ chỉ kiểm tra 1 trong 6 bảng nên xoá được cấp đang dùng — bản HRM '
                   'kiểm tra đủ, đây là khác biệt có chủ đích.',
    delete_accept=[
        'Cấp dịch vụ chưa được nghiệp vụ nào sử dụng thì xoá được và biến mất khỏi danh sách.',
        'Cấp dịch vụ đang dùng ở gói bảo dưỡng, báo giá dịch vụ, hợp đồng dịch vụ, phiếu phân công '
        'công việc hoặc phiếu nhập kết quả thì đều không xoá được.',
        'Gọi trực tiếp API xoá đối với cấp dịch vụ đang được sử dụng vẫn bị chặn.',
    ],
    rules=[
        ('BR-01 — Tên cấp dịch vụ là duy nhất', [
            'Tên cấp không được trùng với bất kỳ bản ghi nào khác trong danh mục.',
            'Khi chỉnh sửa, phép kiểm tra trùng bỏ qua chính bản ghi đang sửa.',
            'Tên cấp được bỏ khoảng trắng thừa ở hai đầu trước khi kiểm tra và lưu.',
            'Tên cấp là trường bắt buộc, tối đa 255 ký tự.',
        ]),
        ('BR-02 — Chặn xoá cấp dịch vụ đã phát sinh dữ liệu', [
            'Không được xoá cấp dịch vụ đã được sử dụng ở bất kỳ nghiệp vụ nào trong 6 bảng '
            'tham chiếu.',
            'Thông báo chặn xoá nêu tối đa 3 nơi đang sử dụng.',
            'Ràng buộc được kiểm tra ở cả giao diện lẫn máy chủ; kiểm tra tại máy chủ là chốt '
            'chặn cuối cùng.',
            'Đây là khác biệt có chủ đích so với màn ERP cũ vốn chỉ kiểm tra 1 trong 6 bảng.',
        ]),
        ('BR-03 — Hiệu năng kiểm tra “đang được sử dụng”', [
            'Tình trạng sử dụng của toàn bộ dòng trên trang được nạp trong một lượt truy vấn chung '
            'thay vì hỏi riêng từng dòng.',
            'Bảng hoặc cột chưa tồn tại trên môi trường triển khai thì được bỏ qua, không gây lỗi.',
        ]),
        ('BR-04 — Dữ liệu dùng chung với hệ thống ERP', [
            'Danh mục dùng chung một nguồn dữ liệu với hệ thống ERP đang chạy song song.',
            'Màn hình HRM không thêm cột nào vào dữ liệu gốc, nên không có trạng thái và không có '
            'lịch sử chỉnh sửa.',
        ]),
    ],
)

# ================================================================================
# 2. DANH MUC GHI CHU KIEM TRA BAO DUONG
# ================================================================================
NOTE = dict(
    screen='Danh mục ghi chú kiểm tra bảo dưỡng',
    screen_lower='danh mục ghi chú kiểm tra bảo dưỡng',
    obj='ghi chú kiểm tra bảo dưỡng',
    code='CSKH-DM-NOTEMAINTENANCE',
    route='/customer-care/note-maintenances',
    img='nm_',
    source='Màn ERP quản lý ghi chú kiểm tra bảo dưỡng (bảng note_maintenances trên DB gộp)',
    perm_manage='Quản lý ghi chú kiểm tra bảo dưỡng', perm_manage_id='1121',
    perm_view='Xem ghi chú kiểm tra bảo dưỡng', perm_view_id='1122',
    columns_text='STT, Hạng mục, Ký hiệu, Mô tả, Cập nhật, Hành động',
    sortable='Hạng mục / Ký hiệu / Cập nhật',
    modal_add='Thêm ghi chú kiểm tra', modal_edit='Sửa ghi chú kiểm tra',
    modal_view='Xem ghi chú kiểm tra',
    scope_in=[
        'Xem danh sách ghi chú kiểm tra bảo dưỡng, tìm kiếm nhanh và lọc theo Hạng mục, Ký hiệu',
        'Sắp xếp phía máy chủ theo Hạng mục, Ký hiệu và thời điểm cập nhật, có phân trang',
        'Thêm mới, chỉnh sửa, xem chi tiết ghi chú qua modal ngay trên màn danh sách — '
        'khác ERP vốn dùng trang riêng',
        'Xoá ghi chú, có kiểm tra ràng buộc dữ liệu ở nghiệp vụ cấp bảo dưỡng của gói dịch vụ',
        'Xuất danh sách ra file Excel theo đúng bộ lọc đang áp dụng',
    ],
    scope_out=[
        'Nhập dữ liệu từ file Excel (Import), In danh sách, Lịch sử chỉnh sửa — màn hình không có '
        'các chức năng này',
        'Trạng thái Khoá / Mở khoá — dữ liệu gốc không có cột trạng thái',
        'Hiển thị thông tin người tạo / người cập nhật — hệ thống vẫn ghi nhận nhưng không hiển thị, '
        'giống màn ERP',
        'Thay đổi cấu trúc bảng dữ liệu: giữ nguyên dữ liệu dùng chung với hệ thống ERP',
    ],
    glossary=[
        ('Ghi chú kiểm tra bảo dưỡng', 'Hạng mục cần kiểm tra khi thực hiện bảo dưỡng, dùng trong '
                                       'cấp bảo dưỡng của gói dịch vụ'),
        ('Hạng mục', 'Tên hạng mục kiểm tra'),
        ('Ký hiệu', 'Mã viết tắt của hạng mục, luôn viết hoa'),
    ],
    context_use=[
        'Cung cấp danh sách hạng mục kiểm tra cho cấp bảo dưỡng của gói dịch vụ',
        'Chuẩn hoá cách gọi tên và ký hiệu hạng mục kiểm tra trên toàn hệ thống',
    ],
    context_need=[
        'Phân quyền rõ ràng giữa người quản lý và người chỉ tra cứu',
        'Ràng buộc nghiêm: không cho xoá ghi chú đã được dùng ở cấp bảo dưỡng của gói dịch vụ — '
        'màn ERP cũ xoá thẳng không kiểm tra gì, dù phần lớn bản ghi đang được sử dụng',
        'Bảo đảm Hạng mục và Ký hiệu đều không trùng nhau',
    ],
    fr02='Hiển thị bảng dữ liệu 6 cột, phân trang, sắp xếp phía máy chủ.',
    fr03='Kết hợp Quick Search và Advanced Filter theo Hạng mục và Ký hiệu; hỗ trợ sắp xếp trên '
         '3 cột.',
    fr04='Mở modal, nhập Hạng mục (*), Ký hiệu (*), Mô tả. Ký hiệu tự viết hoa; Hạng mục và '
         'Ký hiệu đều không được trùng. Có nút Lưu & Tiếp tục.',
    list_desc='Hiển thị danh sách các hạng mục kiểm tra bảo dưỡng đã khai báo kèm ký hiệu, mô tả '
              'và thời điểm cập nhật gần nhất.',
    list_special='Hệ thống vẫn ghi nhận người tạo và người cập nhật nhưng không hiển thị trên màn hình, '
                 'giữ đúng cách làm của màn ERP.',
    list_ui=[
        ('Bảng danh sách ghi chú', 'Table/Grid', 'Enable', '–', '–', '–',
         'Hiển thị danh sách theo phân trang'),
        ('STT', 'Label', 'Enable', '–', '–', '–', 'Số thứ tự bản ghi, tính theo trang hiện tại'),
        ('Hạng mục', 'Text', 'Enable', '0–255 ký tự', '–', 'Lấy từ hệ thống',
         'Tên hạng mục kiểm tra, tự xuống dòng khi dài. Cho phép sắp xếp'),
        ('Ký hiệu', 'Text', 'Enable', '0–255 ký tự', '–', 'Lấy từ hệ thống',
         'Mã viết tắt, luôn hiển thị chữ in hoa. Cho phép sắp xếp'),
        ('Mô tả', 'Text', 'Enable', '0–255 ký tự', '–', 'Lấy từ hệ thống',
         'Mô tả thêm cho hạng mục, có thể để trống'),
        ('Cập nhật', 'Text', 'Enable', 'dd/mm/yyyy', '–', 'Lấy từ hệ thống',
         'Thời điểm cập nhật gần nhất. Cho phép sắp xếp'),
    ],
    list_accept=[
        'Danh sách hiển thị đúng hạng mục, ký hiệu và mô tả của từng bản ghi.',
        'Ký hiệu luôn hiển thị ở dạng chữ in hoa.',
        'Sắp xếp trên cả 3 cột đều đổi đúng thứ tự dữ liệu.',
    ],
    search_flow='1. Người dùng nhập từ khoá vào ô tìm kiếm nhanh hoặc mở bộ lọc nâng cao.\n'
                '2. Người dùng nhập các tiêu chí: Hạng mục, Ký hiệu.\n'
                '3. Người dùng bấm Tìm kiếm.\n'
                '4. Hệ thống lấy danh sách khớp điều kiện, quay về trang 1 và hiển thị kết quả.\n'
                '5. Người dùng có thể bấm tiêu đề cột để đổi thứ tự sắp xếp.',
    search_ui=[
        ('Khung bộ lọc', 'Modal', 'Enable', '–', '–', 'Thu gọn',
         'Khung “Bộ lọc ghi chú kiểm tra bảo dưỡng”, có thể mở rộng / thu gọn'),
        ('Tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Tìm theo hạng mục hoặc ký hiệu'),
        ('Hạng mục', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Lọc theo một phần của tên hạng mục'),
        ('Ký hiệu', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Lọc theo một phần của ký hiệu'),
    ],
    search_accept=[
        'Tìm kiếm nhanh tìm được theo cả hạng mục và ký hiệu.',
        'Kết hợp hai tiêu chí Hạng mục và Ký hiệu cho ra kết quả thoả mãn đồng thời cả hai.',
    ],
    uc_add_rel=[('include', 'Kiểm tra trùng hạng mục và ký hiệu'),
                ('include', 'Chuẩn hoá ký hiệu về chữ hoa')],
    add_flow='1. Người dùng bấm nút Tạo mới → Hệ thống mở modal Thêm ghi chú kiểm tra với các '
             'trường trống.\n'
             '2. Người dùng nhập Hạng mục, Ký hiệu và Mô tả (tuỳ chọn).\n'
             '3. Người dùng bấm Lưu.\n'
             '4. Hệ thống chuẩn hoá dữ liệu: ký hiệu viết hoa, bỏ khoảng trắng thừa.\n'
             '5. Hệ thống kiểm tra hợp lệ rồi ghi bản ghi mới kèm người tạo.\n'
             '6. Hệ thống hiển thị thông báo thành công, đóng modal và tải lại danh sách.',
    add_special='• Hạng mục và Ký hiệu đều phải là duy nhất trong toàn danh mục.\n'
                '• Ký hiệu luôn được lưu ở dạng chữ in hoa để đồng bộ với dữ liệu sẵn có của '
                'hệ thống ERP.',
    form_ui=[
        ('Hạng mục', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
         'Tên hạng mục kiểm tra, không được trùng'),
        ('Ký hiệu', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
         'Mã viết tắt, tự viết hoa khi lưu, không được trùng'),
        ('Mô tả', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Mô tả thêm, có thể bỏ trống'),
    ],
    add_accept=[
        'Bỏ trống Hạng mục hoặc Ký hiệu thì không lưu được và hiển thị lỗi “Bắt buộc phải nhập”.',
        'Nhập hạng mục đã tồn tại thì hiển thị lỗi “Hạng mục đã tồn tại”.',
        'Nhập ký hiệu đã tồn tại thì hiển thị lỗi “Ký hiệu đã tồn tại”.',
        'Nhập ký hiệu bằng chữ thường thì bản ghi lưu xuống phải ở dạng chữ in hoa.',
    ],
    add_validate='– Hạng mục trống → hiển thị “Bắt buộc phải nhập”\n'
                 '– Ký hiệu trống → hiển thị “Bắt buộc phải nhập”\n'
                 '– Hạng mục trùng → hiển thị “Hạng mục đã tồn tại”\n'
                 '– Ký hiệu trùng → hiển thị “Ký hiệu đã tồn tại”\n'
                 '– Trường vượt 255 ký tự → hiển thị “Tối đa 255 ký tự”\n',
    delete_special='• Ràng buộc chặn xoá kiểm tra nghiệp vụ cấp bảo dưỡng của gói dịch vụ.\n'
                   '• Màn ERP cũ xoá thẳng không kiểm tra gì, dù phần lớn bản ghi đang được sử dụng — '
                   'bản HRM chặn lại, đây là khác biệt có chủ đích.',
    delete_accept=[
        'Ghi chú chưa được nghiệp vụ nào sử dụng thì xoá được và biến mất khỏi danh sách.',
        'Ghi chú đang dùng ở cấp bảo dưỡng của gói dịch vụ thì không xoá được.',
        'Gọi trực tiếp API xoá đối với ghi chú đang được sử dụng vẫn bị chặn.',
    ],
    rules=[
        ('BR-01 — Hạng mục và Ký hiệu đều là duy nhất', [
            'Hạng mục không được trùng với bất kỳ bản ghi nào khác.',
            'Ký hiệu cũng không được trùng.',
            'Khi chỉnh sửa, phép kiểm tra trùng bỏ qua chính bản ghi đang sửa.',
            'Cả hai đều là trường bắt buộc, tối đa 255 ký tự.',
        ]),
        ('BR-02 — Chuẩn hoá dữ liệu trước khi lưu', [
            'Ký hiệu luôn được lưu ở dạng chữ in hoa, để đồng bộ với dữ liệu sẵn có của hệ thống ERP.',
            'Hạng mục, Ký hiệu và Mô tả đều được bỏ khoảng trắng thừa ở hai đầu.',
            'Mô tả có thể để trống, tối đa 255 ký tự.',
        ]),
        ('BR-03 — Chặn xoá ghi chú đã phát sinh dữ liệu', [
            'Không được xoá ghi chú đã được dùng ở cấp bảo dưỡng của gói dịch vụ.',
            'Thông báo chặn xoá nêu rõ nghiệp vụ đang sử dụng.',
            'Ràng buộc được kiểm tra ở cả giao diện lẫn máy chủ.',
            'Đây là khác biệt có chủ đích so với màn ERP cũ vốn xoá thẳng không kiểm tra gì.',
        ]),
        ('BR-04 — Ghi nhận người tạo và người cập nhật', [
            'Hệ thống ghi nhận người tạo và người cập nhật cho mỗi bản ghi.',
            'Thông tin này không hiển thị trên giao diện, giữ đúng cách làm của màn ERP, nhưng vẫn '
            'lưu để hai cổng đọc được như nhau.',
        ]),
        ('BR-05 — Dữ liệu dùng chung với hệ thống ERP', [
            'Danh mục dùng chung một nguồn dữ liệu với hệ thống ERP đang chạy song song.',
            'Màn hình HRM đưa form về dạng modal thay vì trang riêng như ERP, nhưng không đổi '
            'cấu trúc dữ liệu.',
        ]),
    ],
)

build(LEVEL)
build(NOTE)
