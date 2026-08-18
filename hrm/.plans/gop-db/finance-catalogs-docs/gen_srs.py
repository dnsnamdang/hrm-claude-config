# -*- coding: utf-8 -*-
"""Sinh 3 file SRS cho nhom danh muc Tai chinh, theo FORM MOI (4 phan).

Chay:  python .plans/gop-db/finance-catalogs-docs/gen_srs.py
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
from fin_config import SCREENS, HOST  # noqa: E402

SHOTS = os.path.join(HERE, "fin_shots")


def shot(name):
    p = os.path.join(SHOTS, name)
    if not os.path.exists(p):
        raise IOError('Thieu anh: %s' % p)
    return p


def build(cfg):
    ten, dt = cfg['ten'], cfg['doi_tuong']
    quyen = cfg['quyen']
    S = cfg['shots']
    url = HOST + cfg['route']
    P1 = 'Người quản lý danh mục (có quyền “%s”)' % quyen
    P0 = 'Người dùng không có quyền “%s”' % quyen

    out = os.path.join(HERE, 'SRS - %s.docx' % ten.replace('/', '-'))
    d = SrsDoc(out=out, menu='Phân hệ Tài chính → Danh mục → %s' % ten,
               route=cfg['route'], full_url=url, img_prefix=cfg['key'] + '_')

    d.title_block(ten)
    d.h2('Mục lục')
    d.toc()

    # ================================================== PHẦN 1
    d.h1('Phần 1. Giới thiệu')
    d.h2('1 Mục đích')
    d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s, nhằm:' % ten)
    d.bullets(cfg['muc_dich'])

    d.h2('2 Thuật ngữ và viết tắt')
    d.table(['Thuật ngữ', 'Mô tả'],
            cfg['thuat_ngu'] + [('SRS', 'Software Requirements Specification')],
            widths=[1.8, 4.2])

    # ================================================== PHẦN 2
    d.h1('Phần 2. Phân quyền')
    d.h2('1 Danh sách quyền')
    d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
        ('P1', quyen,
         'Mở màn hình và thực hiện đầy đủ Thêm mới, Chỉnh sửa, Xóa. Thiếu quyền này thì mục '
         'menu không hiển thị và truy cập thẳng đường dẫn bị chặn.'),
    ], widths=[0.8, 2.2, 3.0])
    d.p('Màn hình chỉ có MỘT quyền duy nhất, không tách riêng quyền xem và quyền sửa. Người '
        'không có quyền này không vào được màn hình.')

    d.h2('2 Ma trận phân quyền')
    fr = [
        ('FR-01 Xem danh sách %s' % dt, '✅', '❌'),
        ('FR-02 Tìm kiếm và lọc', '✅', '❌'),
        ('FR-03 Thêm mới %s' % dt, '✅', '❌'),
        ('FR-04 Chỉnh sửa %s' % dt, '✅', '❌'),
        ('FR-05 Xóa %s' % dt, '✅', '❌'),
        ('FR-06 Xem lịch sử thay đổi', '✅', '❌'),
    ]
    d.table(['Chức năng', 'P1', 'Không có quyền'], fr, widths=[3.4, 1.3, 1.3])

    # ================================================== PHẦN 3
    d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

    d.h2('1 Sơ đồ UML tổng quan')
    ghi_chu_xoa = ('«extend» Ẩn nút Xóa khi đã phát sinh chứng từ' if cfg['dieu_kien_xoa']
                   else '«extend» Xóa là ngừng sử dụng, không mất dữ liệu')
    d.overview_figure(
        'HỆ THỐNG HRM — %s' % ten.upper(),
        [(P1, [0, 1, 2, 3, 4, 5])],
        [('FR-01', 'Xem danh sách', 'view', None),
         ('FR-02', 'Tìm kiếm và lọc', 'view', None),
         ('FR-03', 'Thêm mới', 'crud', None),
         ('FR-04', 'Chỉnh sửa', 'crud', None),
         ('FR-05', 'Xóa', 'action', ghi_chu_xoa),
         ('FR-06', 'Lịch sử thay đổi', 'view', None)],
        'Sơ đồ Use Case tổng quan màn %s' % ten)

    d.h2('2 Đặc tả chi tiết từng chức năng')

    # ---------------------------------------------------------- 2.1
    d.h3('2.1 Xem danh sách %s' % dt)
    d.p('2.1.1 Giới thiệu')
    d.intro_table(
        'Xem danh sách %s' % dt,
        'Hiển thị toàn bộ %s trong danh mục, có phân trang và sắp xếp.' % dt,
        P1,
        'Người dùng có quyền “%s”.' % quyen,
        '1. Người dùng vào menu Tài chính → Danh mục → %s.\n'
        '2. Hệ thống kiểm tra quyền rồi nạp trang đầu tiên của danh sách.\n'
        '3. Bảng hiển thị dữ liệu kèm tổng số bản ghi.' % ten,
        '• Không có quyền → mục menu không hiển thị; truy cập thẳng đường dẫn thì hệ thống từ '
        'chối và báo không có quyền.\n'
        '• Danh mục chưa có bản ghi nào → bảng hiện thông báo không có dữ liệu.')

    d.p('2.1.2 Layout màn hình')
    d.layout(shot=shot(S['danhsach']), shot_caption='Màn %s lúc mới truy cập' % ten)

    d.p('2.1.3 Mô tả chi tiết giao diện')
    rows = [(c[0], 'Table/Grid', 'Read-only', '–', '–', c[1]) for c in cfg['cot']]
    rows += [
        ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
         'Chỉ hiện với người có quyền “%s”.' % quyen),
        ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
         'Nút về đầu / lùi / số trang / tiến / về cuối và ô chọn số dòng mỗi trang.'),
        ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
         'Hiện thông báo không có dữ liệu khi danh sách trống.'),
        ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Ẩn', 'Hiện trong lúc nạp dữ liệu.'),
    ]
    d.ui_table(rows, required=False)

    d.p('2.1.4 Danh sách event và xử lý event')
    d.event_table([
        ('Mở màn hình', 'System',
         'Before:\n– Kiểm tra quyền “%s”.\n'
         '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng '
         'xử lý.\n'
         'After:\n– Nạp trang đầu tiên của danh sách và hiển thị tổng số bản ghi.' % quyen),
        ('Bấm tiêu đề cột sắp xếp được', 'Click',
         'After:\n– Đổi chiều sắp xếp và nạp lại danh sách từ trang 1.'),
        ('Chuyển trang', 'Click',
         'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
         'After:\n– Nạp dữ liệu trang mới, số thứ tự tiếp tục liên tục.'),
        ('Đổi số dòng mỗi trang', 'Change',
         'After:\n– Quay về trang 1 và nạp lại theo số dòng mới.'),
    ])

    # ---------------------------------------------------------- 2.2
    d.h3('2.2 Tìm kiếm và lọc')
    d.p('2.2.1 Giới thiệu')
    d.intro_table(
        'Tìm kiếm và lọc danh sách',
        'Thu hẹp danh sách bằng ô tìm kiếm nhanh%s.'
        % (' và các tiêu chí lọc nâng cao' if len(cfg['loc']) > 1 else
           '. Màn hình này KHÔNG có bộ lọc nâng cao'),
        P1,
        'Đang ở màn %s.' % ten,
        '1. Người dùng nhập từ khóa hoặc chọn tiêu chí lọc.\n'
        '2. Người dùng bấm Tìm kiếm.\n'
        '3. Hệ thống áp đồng thời mọi tiêu chí và nạp lại danh sách từ trang 1.',
        '• Không có kết quả → bảng hiện thông báo không có dữ liệu.\n'
        '• Bấm Làm mới → xóa hết tiêu chí VÀ nạp lại danh sách đầy đủ ngay.')

    d.p('2.2.2 Layout màn hình')
    d.layout(shot=shot(S.get('boloc', S['danhsach'])),
             shot_caption='Khu vực tìm kiếm và lọc của màn %s' % ten)

    d.p('2.2.3 Mô tả chi tiết giao diện')
    rows = [(f[0], f[1], 'Enable', f[2], 'Không', f[3], f[4]) for f in cfg['loc']]
    rows += [
        ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng các tiêu chí.'),
        ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Xóa hết tiêu chí VÀ nạp lại danh sách ngay.'),
    ]
    d.ui_table(rows)

    d.p('2.2.4 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm Tìm kiếm', 'Click',
         'Before:\n– Thu thập giá trị của mọi tiêu chí đang có.\n'
         'During:\n– Áp đồng thời các tiêu chí theo kiểu “và”.\n'
         'After:\n– Nạp lại bảng từ trang 1 và cập nhật tổng số bản ghi.'),
        ('Bấm Làm mới', 'Click',
         'After:\n– Xóa trắng mọi tiêu chí VÀ nạp lại danh sách đầy đủ ngay lập tức.'),
    ])

    # ---------------------------------------------------------- 2.3
    d.h3('2.3 Thêm mới %s' % dt)
    d.p('2.3.1 Biểu đồ Usecase')
    rel = [('include', 'Kiểm tra quyền “%s”' % quyen),
           ('include', 'Kiểm tra trùng %s' % ('mã' if cfg['co_ma'] else 'tên'))]
    d.uc_figure('FR-03', 'Thêm mới %s' % dt, 'crud', rel, actor=P1)

    d.p('2.3.2 Giới thiệu')
    d.intro_table(
        'Thêm mới %s' % dt,
        'Thêm một %s mới vào danh mục thông qua cửa sổ nhập liệu.' % dt,
        P1,
        'Người dùng có quyền “%s”.' % quyen,
        '1. Người dùng bấm nút Tạo mới.\n'
        '2. Hệ thống mở cửa sổ nhập liệu.\n'
        '3. Người dùng nhập thông tin và bấm Lưu.\n'
        '4. Hệ thống kiểm tra dữ liệu và ghi bản ghi mới.\n'
        '5. Cửa sổ đóng, danh sách nạp lại và hiển thị thông báo thành công.',
        '• Thiếu trường bắt buộc hoặc trùng %s → báo lỗi đỏ ngay dưới ô tương ứng, cửa sổ KHÔNG '
        'đóng, dữ liệu đã nhập vẫn còn.\n'
        '• Bấm Đóng → hủy bỏ, không ghi gì.'
        % ('mã' if cfg['co_ma'] else 'tên'),
        'Cửa sổ chỉ có hai nút: Lưu và Đóng.')

    d.p('2.3.3 Layout màn hình')
    d.layout(modal='Tạo %s' % dt, shot=shot(S['taomoi']),
             shot_caption='Cửa sổ Tạo %s' % dt)
    if 'validate' in S:
        d.figure(shot(S['validate']),
                 'Cửa sổ báo lỗi đỏ ngay dưới ô còn thiếu', width_in=6.2)

    d.p('2.3.4 Mô tả chi tiết giao diện')
    rows = [(t[0], t[1], 'Enable', t[2], t[3], t[4], t[5]) for t in cfg['truong']]
    rows += [
        ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi bản ghi rồi đóng cửa sổ.'),
        ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Hủy bỏ, không ghi gì.'),
        ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         'Chữ đỏ ngay dưới ô bị lỗi.'),
    ]
    d.ui_table(rows)

    d.p('2.3.5 Danh sách event và xử lý event')
    during = ['– %s để trống → hiển thị “Bắt buộc phải nhập”.' % t[0]
              for t in cfg['truong'] if t[3] == 'Có']
    during.append('– %s đã tồn tại → hiển thị “%s”.'
                  % ('Mã' if cfg['co_ma'] else 'Tên', cfg['loi_trung']))
    during.append('– Nếu có lỗi kiểm tra → không thực hiện bước After.')
    d.event_table([
        ('Bấm nút Tạo mới', 'Click',
         'Before:\n– Kiểm tra quyền “%s”.\n'
         '– Nếu không có quyền → nút không hiển thị.\n'
         'After:\n– Mở cửa sổ nhập liệu%s.'
         % (quyen,
            ' với ô Trạng thái đặt sẵn là Hoạt động' if cfg['co_trangthai'] else '')),
        ('Bấm Lưu', 'Click',
         'Before:\n– Kiểm tra quyền “%s”.\n'
         '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng '
         'xử lý.\n'
         'During:\n%s\n'
         'After:\n– Ghi bản ghi mới.\n'
         '– Đóng cửa sổ, nạp lại danh sách, hiển thị thông báo thêm mới thành công.'
         % (quyen, '\n'.join(during))),
        ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ, không ghi dữ liệu.'),
    ])

    # ---------------------------------------------------------- 2.4
    d.h3('2.4 Chỉnh sửa %s' % dt)
    d.p('2.4.1 Biểu đồ Usecase')
    d.uc_figure('FR-04', 'Chỉnh sửa %s' % dt, 'crud',
                [('include', 'Kiểm tra quyền “%s”' % quyen),
                 ('include', 'Ghi lịch sử thay đổi')], actor=P1)

    d.p('2.4.2 Giới thiệu')
    d.intro_table(
        'Chỉnh sửa %s' % dt,
        'Sửa thông tin của một %s đã có. Dùng chung cửa sổ với chức năng Thêm mới.' % dt,
        P1,
        'Người dùng có quyền “%s”; bản ghi cần sửa đang có trong danh sách.' % quyen,
        '1. Người dùng bấm biểu tượng bút chì ở dòng cần sửa.\n'
        '2. Hệ thống mở cửa sổ với dữ liệu hiện tại đã điền sẵn.\n'
        '3. Người dùng sửa thông tin và bấm Lưu.\n'
        '4. Hệ thống kiểm tra dữ liệu, ghi nhận thay đổi và ghi một dòng lịch sử.\n'
        '5. Cửa sổ đóng, danh sách nạp lại và hiển thị thông báo thành công.',
        '• Trùng %s với bản ghi khác → báo lỗi, cửa sổ không đóng.\n'
        '• Giữ nguyên %s của chính bản ghi đang sửa → lưu bình thường, không báo trùng.'
        % (('mã', 'mã') if cfg['co_ma'] else ('tên', 'tên')))

    d.p('2.4.3 Layout màn hình')
    d.layout(modal='Sửa %s' % dt, shot=shot(S['taomoi']),
             shot_caption='Cửa sổ nhập liệu dùng chung cho Thêm mới và Chỉnh sửa %s' % dt)

    d.p('2.4.4 Mô tả chi tiết giao diện')
    rows = [(t[0], t[1], 'Enable', t[2], t[3], 'Dữ liệu hiện tại', t[5])
            for t in cfg['truong']]
    rows += [
        ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi thay đổi rồi đóng cửa sổ.'),
        ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Hủy bỏ, không ghi gì.'),
    ]
    d.ui_table(rows)

    d.p('2.4.5 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm biểu tượng bút chì', 'Click',
         'Before:\n– Kiểm tra quyền “%s”; thiếu quyền thì nút không hiển thị.\n'
         'After:\n– Mở cửa sổ với dữ liệu hiện tại đã điền sẵn.' % quyen),
        ('Bấm Lưu', 'Click',
         'During:\n%s\n'
         '– Bỏ qua kiểm tra trùng đối với chính bản ghi đang sửa.\n'
         '– Nếu có lỗi kiểm tra → không thực hiện bước After.\n'
         'After:\n– Ghi nhận thay đổi và ghi một dòng lịch sử nêu giá trị cũ và giá trị mới.\n'
         '– Đóng cửa sổ, nạp lại danh sách, hiển thị thông báo cập nhật thành công.'
         % '\n'.join(during[:-1])),
    ])

    # ---------------------------------------------------------- 2.5
    d.h3('2.5 Xóa %s' % dt)
    d.p('2.5.1 Biểu đồ Usecase')
    rel5 = [('include', 'Kiểm tra quyền “%s”' % quyen),
            ('include', 'Xác nhận trước khi thực hiện')]
    if cfg['dieu_kien_xoa']:
        rel5.append(('extend', 'Ẩn nút Xóa khi đã phát sinh chứng từ'))
    else:
        rel5.append(('extend', 'Xóa là ngừng sử dụng, dữ liệu không mất hẳn'))
    d.uc_figure('FR-05', 'Xóa %s' % dt, 'action', rel5, actor=P1)

    d.p('2.5.2 Giới thiệu')
    mota5 = 'Loại một %s khỏi danh mục.' % dt
    if cfg['xoa_mem']:
        mota5 += (' Trên màn này, xóa được xử lý thành ngừng sử dụng ở phía máy chủ: bản ghi '
                  'biến mất khỏi danh sách nhưng dữ liệu không bị mất hẳn.')
    phu5 = ('• Bấm Hủy → đóng hộp, không thay đổi gì.')
    if cfg['dieu_kien_xoa']:
        phu5 += ('\n• ⚠️ Nút Xóa CHỈ hiển thị với bản ghi %s. Bản ghi đã dùng ở bút toán thì '
                 'không có nút Xóa — muốn ngừng dùng thì chuyển Trạng thái sang Khóa.'
                 % cfg['dieu_kien_xoa'])
    d.intro_table(
        'Xóa %s' % dt, mota5, P1,
        'Người dùng có quyền “%s”; bản ghi cần xóa đang có trong danh sách.' % quyen,
        '1. Người dùng bấm biểu tượng thùng rác ở dòng cần xóa.\n'
        '2. Hệ thống hiện hộp xác nhận nêu rõ tên bản ghi.\n'
        '3. Người dùng bấm Xóa để xác nhận.\n'
        '4. Hệ thống loại bản ghi khỏi danh sách và hiển thị thông báo thành công.',
        phu5)

    d.p('2.5.3 Layout màn hình')
    d.layout(modal='Xóa %s' % dt, shot=shot(S['xoa']),
             shot_caption='Hộp xác nhận xóa %s' % dt)

    d.p('2.5.4 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Biểu tượng thùng rác', 'Icon Button', 'Enable / Ẩn',
         'Ẩn khi không xóa được' if cfg['dieu_kien_xoa'] else 'Hiển thị',
         'Nằm trên cột Hành động của từng dòng.'),
        ('Tiêu đề hộp xác nhận', 'Label', 'Hiển thị', 'Xóa %s' % dt,
         'Nêu rõ loại đối tượng đang xóa.'),
        ('Nội dung hộp xác nhận', 'Label', 'Hiển thị',
         'Bạn có chắc muốn xóa %s “<tên>”?' % dt,
         'Nêu rõ tên bản ghi để tránh thao tác nhầm dòng.'),
        ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Xác nhận thực hiện.'),
        ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không làm gì.'),
    ], required=False, scope=False)

    d.p('2.5.5 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm biểu tượng thùng rác', 'Click',
         ('Before:\n– Bản ghi đã phát sinh ở bút toán kế toán thì nút này KHÔNG hiển thị.\n'
          if cfg['dieu_kien_xoa'] else '') +
         'After:\n– Hiện hộp xác nhận kèm tên bản ghi.'),
        ('Bấm Xóa trong hộp xác nhận', 'Click',
         'Before:\n– Kiểm tra quyền “%s”; thiếu quyền thì từ chối và dừng xử lý.\n'
         'After:\n– Loại bản ghi khỏi danh sách%s.\n'
         '– Nạp lại danh sách và hiển thị thông báo xóa thành công.'
         % (quyen, ' (chuyển sang trạng thái ngừng sử dụng)' if cfg['xoa_mem'] else '')),
        ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp xác nhận, không thay đổi gì.'),
    ])

    # ---------------------------------------------------------- 2.6
    d.h3('2.6 Xem lịch sử thay đổi')
    d.p('2.6.1 Giới thiệu')
    d.intro_table(
        'Xem lịch sử thay đổi',
        'Liệt kê các lần thay đổi của một %s, kèm giá trị cũ, giá trị mới, người thực hiện và '
        'thời điểm.' % dt,
        P1,
        'Bản ghi cần xem đang có trong danh sách.',
        '1. Người dùng bấm biểu tượng lịch sử ở dòng cần xem.\n'
        '2. Hệ thống mở cửa sổ Lịch sử thay đổi.\n'
        '3. Danh sách các lần thay đổi hiển thị theo thứ tự mới nhất ở trên cùng.',
        '• Bản ghi chưa từng sửa → cửa sổ hiện “Chưa có lịch sử thao tác nào.”\n'
        '• Cửa sổ có bộ lọc riêng để thu hẹp theo loại thay đổi.')

    d.p('2.6.2 Layout màn hình')
    d.layout(modal='Lịch sử thay đổi', shot=shot(S['lichsu']),
             shot_caption='Cửa sổ Lịch sử thay đổi của %s' % dt)

    d.p('2.6.3 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Lịch sử thay đổi',
         'Kèm dòng phụ ghi loại đối tượng và tên bản ghi.'),
        ('Bộ lọc', 'Dropdown', 'Enable', 'Trống', 'Thu hẹp theo loại thay đổi.'),
        ('Danh sách thay đổi', 'Table/Grid', 'Read-only', 'Theo dữ liệu',
         'Sắp xếp mới nhất ở trên cùng.'),
        ('Thời điểm', 'Text', 'Read-only', 'Theo dữ liệu', 'Định dạng dd/mm/yyyy hh:mm.'),
        ('Loại thay đổi', 'Badge', 'Read-only', 'Theo dữ liệu',
         'Ví dụ: Thay đổi thông tin.'),
        ('Người thực hiện', 'Text', 'Read-only', 'Theo dữ liệu',
         'Kèm mã nhân viên và phòng ban.'),
        ('Giá trị cũ và giá trị mới', 'Text', 'Read-only', 'Theo dữ liệu',
         'Hiển thị hai vế cho từng trường đã đổi.'),
        ('Trạng thái rỗng', 'Label', 'Hiển thị', 'Ẩn',
         'Hiện “Chưa có lịch sử thao tác nào.” khi bản ghi chưa từng sửa.'),
        ('Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.'),
    ], required=False, scope=False)

    d.p('2.6.4 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm biểu tượng lịch sử', 'Click',
         'After:\n– Mở cửa sổ và nạp danh sách thay đổi theo thứ tự mới nhất trước.'),
        ('Đổi bộ lọc trong cửa sổ', 'Change',
         'After:\n– Nạp lại danh sách theo tiêu chí đã chọn.'),
        ('Bấm Đóng', 'Click',
         'After:\n– Đóng cửa sổ; danh sách phía sau giữ nguyên bộ lọc và trang.'),
    ])

    # ================================================== PHẦN 4
    d.h1('Phần 4. Quy tắc nghiệp vụ')

    d.p('BR-01 — Một quyền duy nhất cho cả xem và sửa')
    d.bullets([
        'Màn hình chỉ dùng một quyền “%s”, không tách quyền xem riêng.' % quyen,
        'Người không có quyền này không thấy mục menu và không truy cập được bằng đường dẫn.',
        'Mọi thao tác ghi đều kiểm tra lại quyền ở tầng máy chủ; gọi thẳng chức năng mà bỏ qua '
        'giao diện vẫn bị từ chối.',
    ])

    d.p('BR-02 — Ràng buộc trùng')
    if cfg['co_ma']:
        d.bullets([
            'Mã %s là duy nhất trên toàn hệ thống; trùng sẽ bị chặn với thông báo “%s”.'
            % (dt, cfg['loi_trung']),
            'Tên %s KHÔNG bị ràng buộc duy nhất — hai bản ghi khác mã được phép trùng tên.' % dt,
            'Khi sửa, bản ghi đang sửa được loại khỏi phép kiểm tra trùng.',
        ])
    else:
        d.bullets([
            'Tên %s là duy nhất trên toàn hệ thống; trùng sẽ bị chặn với thông báo “%s”.'
            % (dt, cfg['loi_trung']),
            'Khi sửa, bản ghi đang sửa được loại khỏi phép kiểm tra trùng — giữ nguyên tên của '
            'chính nó thì lưu bình thường.',
        ])

    if cfg['dieu_kien_xoa']:
        d.p('BR-03 — Chỉ xóa được khi chưa phát sinh chứng từ')
        d.bullets([
            'Nút Xóa CHỈ hiển thị với %s %s.' % (dt, cfg['dieu_kien_xoa']),
            'Bản ghi đã được dùng trong bút toán kế toán sẽ KHÔNG có nút Xóa — đây là thiết kế, '
            'nhằm giữ toàn vẹn số liệu kế toán đã ghi.',
            'Muốn ngừng sử dụng bản ghi loại này, người dùng chuyển Trạng thái sang Khóa thay vì '
            'xóa.',
            'Quy ước chung của dự án: nút không dùng được thì ẩn hẳn, không hiện rồi làm mờ.',
        ])
        d.p('BR-04 — Trạng thái Hoạt động và Khóa')
        d.bullets([
            'Bản ghi mới luôn được đặt Trạng thái Hoạt động.',
            'Chuyển sang Khóa thì bản ghi không còn chọn được khi lập bút toán mới, nhưng vẫn '
            'nằm trong danh mục và các bút toán cũ giữ nguyên.',
            'Trạng thái đổi bằng cách mở cửa sổ Sửa rồi chọn lại ô Trạng thái — màn này KHÔNG có '
            'nút Khóa riêng trên cột Hành động.',
        ])
        n_br = 5
    else:
        d.p('BR-03 — Xóa là ngừng sử dụng')
        d.bullets([
            'Màn hình không có cột Trạng thái trên lưới và không có thao tác Khóa riêng.',
            'Thao tác Xóa chuyển bản ghi sang trạng thái ngừng sử dụng ở phía máy chủ: bản ghi '
            'biến mất khỏi danh sách nhưng dữ liệu không mất hẳn.',
            'Nhờ vậy, chứng từ cũ đang tham chiếu tới bản ghi vẫn hiển thị đúng tên.',
        ])
        n_br = 4

    d.p('BR-%02d — Lịch sử thay đổi sắp xếp mới nhất trước' % n_br)
    d.bullets([
        'Mọi thao tác sửa đều sinh dòng lịch sử.',
        'Danh sách lịch sử luôn sắp xếp MỚI NHẤT Ở TRÊN CÙNG.',
        'Mỗi dòng nêu trường đã đổi, giá trị cũ, giá trị mới, người thực hiện và thời điểm.',
    ])

    d.save()
    return out


if __name__ == '__main__':
    for cfg in SCREENS:
        build(cfg)
