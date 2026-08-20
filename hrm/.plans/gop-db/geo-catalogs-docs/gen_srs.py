# -*- coding: utf-8 -*-
"""Sinh 6 file SRS cho nhom danh muc dia ly, theo FORM MOI (user chot 2026-08-17):
4 phan — Gioi thieu / Phan quyen / Dac ta chi tiet / Quy tac nghiep vu.

Chay:  python .plans/gop-db/geo-catalogs-docs/gen_srs.py
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
from srs_geo_config import SCREENS, HOST, QUYEN_CHUNG, CANH_BAO_QUYEN  # noqa: E402

SHOTS = os.path.join(HERE, "geo_shots")
ACTOR = 'Người dùng đã đăng nhập'


def shot(name):
    p = os.path.join(SHOTS, name)
    if not os.path.exists(p):
        raise IOError('Thieu anh: %s' % p)
    return p


def build(cfg):
    ten = cfg['ten']
    dt = cfg['doi_tuong']
    co_khoa = cfg['co_khoa']
    S = cfg['shots']
    url = HOST + cfg['route']

    # Ten man co dau '/' (Tinh/TP, Quan/Huyen...) — phai thay truoc khi ghep duong dan,
    # neu khong '/' bi hieu la phan cach thu muc va file de sai cho.
    ten_file = ten.replace('/', '-')
    out = os.path.join(HERE, 'SRS - %s.docx' % ten_file)
    d = SrsDoc(out=out, menu='Phân hệ Danh mục chung → Địa lý → %s' % ten,
               route=cfg['route'], full_url=url, img_prefix=cfg['key'] + '_')

    # -------------------------------------------------- trang đầu + mục lục
    d.title_block(ten)
    d.h2('Mục lục')
    d.toc()

    # ================================================== PHẦN 1
    d.h1('Phần 1. Giới thiệu')

    d.h2('1 Mục đích')
    d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s, nhằm:' % ten)
    d.bullets(cfg['muc_dich'])

    d.h2('2 Thuật ngữ và viết tắt')
    d.table(['Thuật ngữ', 'Mô tả'], cfg['thuat_ngu'], widths=[1.8, 4.2])

    # ================================================== PHẦN 2
    d.h1('Phần 2. Phân quyền')

    d.h2('1 Danh sách quyền')
    d.p(QUYEN_CHUNG)
    d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
        ('—', '(chưa khai báo quyền nào)',
         'Toàn bộ chức năng của màn hình đều mở cho mọi người dùng đã đăng nhập.'),
    ], widths=[0.8, 2.2, 3.0])
    d.p(CANH_BAO_QUYEN)

    d.h2('2 Ma trận phân quyền')
    fr = [
        ('FR-01 Xem danh sách %s' % dt, '✅'),
        ('FR-02 Tìm kiếm và lọc', '✅'),
        ('FR-03 Thêm mới %s' % dt, '✅'),
        ('FR-04 Chỉnh sửa %s' % dt, '✅'),
        ('FR-05 Xóa %s' % dt, '✅'),
    ]
    if co_khoa:
        fr.append(('FR-06 Khóa / Mở khóa %s' % dt, '✅'))
        fr.append(('FR-07 Xem lịch sử thay đổi', '✅'))
    else:
        fr.append(('FR-06 Xem lịch sử thay đổi', '✅'))
    d.table(['Chức năng', 'Người dùng đã đăng nhập'], fr, widths=[3.6, 2.4])
    d.p('Ma trận chỉ có một cột vì màn hình chưa phân biệt vai trò. Khi bổ sung quyền, ma trận '
        'này phải được lập lại theo từng quyền.')

    # ================================================== PHẦN 3
    d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

    d.h2('1 Sơ đồ UML tổng quan')
    ucs = [
        ('FR-01', 'Xem danh sách', 'view', None),
        ('FR-02', 'Tìm kiếm và lọc', 'view', None),
        ('FR-03', 'Thêm mới', 'crud', None),
        ('FR-04', 'Chỉnh sửa', 'crud', None),
    ]
    if co_khoa:
        ucs += [('FR-05', 'Xóa', 'action', '«extend» Ẩn khi bản ghi đã Khóa'),
                ('FR-06', 'Khóa / Mở khóa', 'action', None),
                ('FR-07', 'Lịch sử thay đổi', 'view', None)]
        idx = [0, 1, 2, 3, 4, 5, 6]
    else:
        ucs += [('FR-05', 'Xóa', 'action', '«extend» Xóa là ngừng sử dụng, không mất dữ liệu'),
                ('FR-06', 'Lịch sử thay đổi', 'view', None)]
        idx = [0, 1, 2, 3, 4, 5]
    d.overview_figure('HỆ THỐNG HRM — %s' % ten.upper(),
                      [(ACTOR, idx)], ucs,
                      'Sơ đồ Use Case tổng quan màn %s' % ten)

    d.h2('2 Đặc tả chi tiết từng chức năng')

    # ---------------------------------------------------------- 2.1 Xem DS
    d.h3('2.1 Xem danh sách %s' % dt)

    d.p('2.1.1 Giới thiệu')
    d.intro_table(
        'Xem danh sách %s' % dt,
        'Hiển thị toàn bộ %s trong danh mục, có phân trang và sắp xếp.' % dt,
        ACTOR,
        'Người dùng đã đăng nhập vào hệ thống.',
        '1. Người dùng vào menu Danh mục chung → Địa lý → %s.\n'
        '2. Hệ thống nạp trang đầu tiên của danh sách.\n'
        '3. Bảng hiển thị dữ liệu kèm tổng số bản ghi.' % ten,
        '• Danh mục chưa có bản ghi nào → bảng hiện thông báo không có dữ liệu.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.')

    d.p('2.1.2 Layout màn hình')
    d.layout(shot=shot(S['danhsach']), shot_caption='Màn %s lúc mới truy cập' % ten)

    d.p('2.1.3 Mô tả chi tiết giao diện')
    rows = [(c[0], 'Table/Grid', 'Read-only', '–', '–', c[1]) for c in cfg['cot']]
    rows += [
        ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
         'Mở cửa sổ thêm mới %s.' % dt),
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
         'After:\n– Nạp trang đầu tiên của danh sách và hiển thị tổng số bản ghi.'),
        ('Bấm tiêu đề cột sắp xếp được', 'Click',
         'After:\n– Đổi chiều sắp xếp và nạp lại danh sách từ trang 1.'),
        ('Chuyển trang', 'Click',
         'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
         'After:\n– Nạp dữ liệu trang mới, số thứ tự tiếp tục liên tục.'),
        ('Đổi số dòng mỗi trang', 'Change',
         'After:\n– Quay về trang 1 và nạp lại theo số dòng mới.'),
    ])

    # ---------------------------------------------------------- 2.2 Tìm kiếm
    d.h3('2.2 Tìm kiếm và lọc')

    d.p('2.2.1 Giới thiệu')
    d.intro_table(
        'Tìm kiếm và lọc danh sách',
        'Thu hẹp danh sách bằng ô tìm kiếm nhanh và các tiêu chí lọc của màn hình.',
        ACTOR,
        'Đang ở màn %s.' % ten,
        '1. Người dùng nhập từ khóa hoặc chọn tiêu chí lọc.\n'
        '2. Người dùng bấm Tìm kiếm.\n'
        '3. Hệ thống áp đồng thời mọi tiêu chí và nạp lại danh sách từ trang 1.',
        '• Không có kết quả → bảng hiện thông báo không có dữ liệu.\n'
        '• Bấm Làm mới → xóa hết tiêu chí VÀ nạp lại danh sách đầy đủ ngay.')

    d.p('2.2.2 Layout màn hình')
    d.layout(shot=shot(S['danhsach']),
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
    ev = [
        ('Bấm Tìm kiếm', 'Click',
         'Before:\n– Thu thập giá trị của mọi tiêu chí đang có.\n'
         'During:\n– Áp đồng thời các tiêu chí theo kiểu “và”.\n'
         'After:\n– Nạp lại bảng từ trang 1 và cập nhật tổng số bản ghi.'),
        ('Bấm Làm mới', 'Click',
         'After:\n– Xóa trắng mọi tiêu chí VÀ nạp lại danh sách đầy đủ ngay lập tức.'),
    ]
    if cfg['key'] in ('districts', 'wards'):
        ev.append(('Đổi Quốc gia ở bộ lọc', 'Change',
                   'After:\n– Xóa trắng ô Tỉnh/TP và nạp lại danh sách theo quốc gia mới.'))
    if cfg['key'] == 'hamlets':
        ev.append(('Đổi Tỉnh/TP ở bộ lọc', 'Change',
                   'After:\n– Xóa trắng ô Phường/xã và nạp lại danh sách theo Tỉnh/TP mới.'))
    d.event_table(ev)

    # ---------------------------------------------------------- 2.3 Thêm mới
    d.h3('2.3 Thêm mới %s' % dt)

    d.p('2.3.1 Biểu đồ Usecase')
    rel = [('include', 'Kiểm tra trùng tên %s' % cfg['pham_vi_trung'])]
    if cfg['cap_tren']:
        rel.append(('include', 'Chọn %s' % cfg['cap_tren']))
    if cfg['key'] == 'hamlets':
        rel.append(('extend', 'Ẩn ô Quận/Huyện khi Quốc gia là Việt Nam'))
    d.uc_figure('FR-03', 'Thêm mới %s' % dt, 'crud', rel, actor=ACTOR)

    d.p('2.3.2 Giới thiệu')
    d.intro_table(
        'Thêm mới %s' % dt,
        'Thêm một %s mới vào danh mục thông qua cửa sổ nhập liệu.' % dt,
        ACTOR,
        'Đang ở màn %s.' % ten,
        '1. Người dùng bấm nút Tạo mới.\n'
        '2. Hệ thống mở cửa sổ nhập liệu với các ô để trống.\n'
        '3. Người dùng nhập thông tin và bấm Lưu.\n'
        '4. Hệ thống kiểm tra dữ liệu và ghi bản ghi mới.\n'
        '5. Cửa sổ đóng lại, danh sách nạp lại và hiển thị thông báo thành công.',
        '• Thiếu trường bắt buộc hoặc trùng tên → báo lỗi đỏ ngay dưới ô tương ứng, cửa sổ '
        'KHÔNG đóng, dữ liệu đã nhập vẫn còn.\n'
        '• Bấm “Lưu và tiếp tục” → ghi bản ghi rồi giữ cửa sổ mở với các ô đã xóa trắng, '
        'để nhập tiếp bản ghi kế theo.\n'
        '• Bấm Đóng → hủy bỏ, không ghi gì.',
        'Cửa sổ có ba nút: Lưu, Lưu và tiếp tục, Đóng.')

    d.p('2.3.3 Layout màn hình')
    d.layout(modal='Tạo %s' % dt, shot=shot(S['taomoi']),
             shot_caption='Cửa sổ Tạo %s' % dt)
    if cfg['key'] == 'hamlets':
        d.figure(shot(S['khac_vn']),
                 'Cùng cửa sổ khi chọn Quốc gia khác Việt Nam — hiện thêm ô Quận/Huyện/Thị xã',
                 width_in=6.2)
    if 'validate' in S:
        d.figure(shot(S['validate']),
                 'Cửa sổ báo lỗi đỏ ngay dưới ô còn thiếu', width_in=6.2)

    d.p('2.3.4 Mô tả chi tiết giao diện')
    rows = [(t[0], t[1], 'Enable', t[2], t[3], t[4], t[5]) for t in cfg['truong']]
    rows += [
        ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Ghi bản ghi rồi đóng cửa sổ.'),
        ('Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Ghi bản ghi rồi giữ cửa sổ mở để nhập tiếp.'),
        ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Hủy bỏ, không ghi gì.'),
        ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         'Chữ đỏ ngay dưới ô bị lỗi.'),
    ]
    d.ui_table(rows)

    d.p('2.3.5 Danh sách event và xử lý event')
    during = ['– %s để trống → hiển thị “Bắt buộc phải nhập”.' % t[0]
              for t in cfg['truong'] if t[3].startswith('Có')]
    during.append('– Tên đã tồn tại %s → hiển thị “%s”.'
                  % (cfg['pham_vi_trung'], cfg['loi_trung_ten']))
    during.append('– Nếu có lỗi kiểm tra → không thực hiện bước After.')
    ev = [
        ('Bấm nút Tạo mới', 'Click',
         'After:\n– Mở cửa sổ nhập liệu với các ô để trống.'),
        ('Bấm Lưu', 'Click',
         'During:\n' + '\n'.join(during) + '\n'
         'After:\n– Ghi bản ghi mới.\n'
         '– Đóng cửa sổ, nạp lại danh sách, hiển thị thông báo thêm mới thành công.'),
        ('Bấm Lưu và tiếp tục', 'Click',
         'During:\n– Áp dụng đúng các quy tắc kiểm tra như nút Lưu.\n'
         'After:\n– Ghi bản ghi mới, xóa trắng các ô và GIỮ cửa sổ mở để nhập tiếp.'),
        ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ, không ghi dữ liệu.'),
    ]
    if cfg['key'] == 'hamlets':
        ev.insert(1, ('Đổi ô Quốc gia', 'Change',
                      'After:\n– Quốc gia là Việt Nam → ẨN ô Quận/Huyện/Thị xã và bỏ yêu cầu '
                      'nhập ô này.\n– Quốc gia khác → HIỆN ô Quận/Huyện/Thị xã và bắt buộc nhập.\n'
                      '– Xóa trắng và nạp lại các cấp địa chỉ bên dưới.'))
    d.event_table(ev)

    # ---------------------------------------------------------- 2.4 Chỉnh sửa
    d.h3('2.4 Chỉnh sửa %s' % dt)

    d.p('2.4.1 Biểu đồ Usecase')
    rel4 = [('include', 'Kiểm tra trùng tên %s' % cfg['pham_vi_trung'])]
    if co_khoa:
        rel4.append(('extend', 'Ẩn nút Sửa khi bản ghi đã Khóa'))
    d.uc_figure('FR-04', 'Chỉnh sửa %s' % dt, 'crud', rel4, actor=ACTOR)

    d.p('2.4.2 Giới thiệu')
    dk = 'Bản ghi cần sửa đang ở trạng thái Hoạt động.' if co_khoa \
        else 'Bản ghi cần sửa đang có trong danh sách.'
    phu = ('• Trùng tên với bản ghi khác → báo lỗi, cửa sổ không đóng.\n'
           '• Giữ nguyên tên của chính bản ghi đang sửa → lưu bình thường, không báo trùng.')
    if co_khoa:
        phu += '\n• Bản ghi đã Khóa → nút Sửa KHÔNG hiển thị, phải Mở khóa trước.'
    d.intro_table(
        'Chỉnh sửa %s' % dt,
        'Sửa thông tin của một %s đã có. Dùng chung cửa sổ với chức năng Thêm mới.' % dt,
        ACTOR, dk,
        '1. Người dùng bấm biểu tượng bút chì ở dòng cần sửa.\n'
        '2. Hệ thống mở cửa sổ với dữ liệu hiện tại đã điền sẵn.\n'
        '3. Người dùng sửa thông tin và bấm Lưu.\n'
        '4. Hệ thống kiểm tra dữ liệu, ghi nhận thay đổi và ghi một dòng lịch sử.\n'
        '5. Cửa sổ đóng lại, danh sách nạp lại và hiển thị thông báo thành công.',
        phu)

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
         ('Before:\n– Bản ghi đã Khóa thì nút này không hiển thị.\n' if co_khoa else '') +
         'After:\n– Mở cửa sổ với dữ liệu hiện tại đã điền sẵn.'),
        ('Bấm Lưu', 'Click',
         'During:\n' + '\n'.join(during[:-1]) + '\n'
         '– Bỏ qua kiểm tra trùng đối với chính bản ghi đang sửa.\n'
         '– Nếu có lỗi kiểm tra → không thực hiện bước After.\n'
         'After:\n– Ghi nhận thay đổi và ghi một dòng lịch sử nêu giá trị cũ và giá trị mới.\n'
         '– Đóng cửa sổ, nạp lại danh sách, hiển thị thông báo cập nhật thành công.'),
    ])

    # ---------------------------------------------------------- 2.5 Xóa
    d.h3('2.5 Xóa %s' % dt)

    d.p('2.5.1 Biểu đồ Usecase')
    rel5 = [('include', 'Xác nhận trước khi thực hiện')]
    if co_khoa:
        rel5.append(('extend', 'Ẩn nút Xóa khi bản ghi đã Khóa'))
    else:
        rel5.append(('extend', 'Xóa là ngừng sử dụng, dữ liệu không mất hẳn'))
    d.uc_figure('FR-05', 'Xóa %s' % dt, 'action', rel5, actor=ACTOR)

    d.p('2.5.2 Giới thiệu')
    mota5 = 'Loại một %s khỏi danh mục.' % dt
    if not co_khoa:
        mota5 += (' Trên màn này, xóa được xử lý thành ngừng sử dụng ở phía máy chủ: bản ghi '
                  'biến mất khỏi danh sách nhưng dữ liệu không bị mất hẳn.')
    d.intro_table(
        'Xóa %s' % dt, mota5, ACTOR,
        'Bản ghi cần xóa đang có trong danh sách.',
        '1. Người dùng bấm biểu tượng thùng rác ở dòng cần xóa.\n'
        '2. Hệ thống hiện hộp xác nhận nêu rõ tên bản ghi.\n'
        '3. Người dùng bấm Xóa để xác nhận.\n'
        '4. Hệ thống loại bản ghi khỏi danh sách và hiển thị thông báo thành công.',
        '• Bấm Hủy → đóng hộp, không thay đổi gì.\n'
        '• Bản ghi đang được dùng ở cấp địa chỉ bên dưới hoặc ở dữ liệu nghiệp vụ khác → '
        'hệ thống từ chối và nêu lý do.' +
        ('\n• Bản ghi đã Khóa → nút Xóa KHÔNG hiển thị.' if co_khoa else ''))

    d.p('2.5.3 Layout màn hình')
    d.layout(modal='Xóa %s' % dt, shot=shot(S.get('xoa', S['danhsach'])),
             shot_caption='Hộp xác nhận xóa %s' % dt)

    d.p('2.5.4 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Biểu tượng thùng rác', 'Icon Button', 'Enable', 'Hiển thị',
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
         ('Before:\n– Bản ghi đã Khóa thì nút này không hiển thị.\n' if co_khoa else '') +
         'After:\n– Hiện hộp xác nhận kèm tên bản ghi.'),
        ('Bấm Xóa trong hộp xác nhận', 'Click',
         'During:\n– Bản ghi đang được dùng ở nơi khác → hiển thị thông báo từ chối và dừng '
         'xử lý.\n'
         'After:\n– Loại bản ghi khỏi danh sách%s.\n'
         '– Nạp lại danh sách và hiển thị thông báo xóa thành công.'
         % ('' if co_khoa else ' (chuyển sang trạng thái ngừng sử dụng)')),
        ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp xác nhận, không thay đổi gì.'),
    ])

    n = 6
    # ---------------------------------------------------------- 2.6 Khóa
    if co_khoa:
        d.h3('2.6 Khóa / Mở khóa %s' % dt)

        d.p('2.6.1 Biểu đồ Usecase')
        d.uc_figure('FR-06', 'Khóa / Mở khóa %s' % dt, 'action',
                    [('include', 'Xác nhận trước khi thực hiện'),
                     ('extend', 'Khóa KHÔNG xóa dữ liệu, chỉ đổi trạng thái')],
                    actor=ACTOR)

        d.p('2.6.2 Giới thiệu')
        d.intro_table(
            'Khóa / Mở khóa %s' % dt,
            'Đổi trạng thái %s qua lại giữa Hoạt động và Khóa. Bản ghi đã Khóa vẫn nằm trong '
            'danh mục nhưng không chọn được ở các màn nghiệp vụ khác.' % dt,
            ACTOR,
            'Bản ghi cần đổi trạng thái đang có trong danh sách.',
            '1. Người dùng mở nút ba chấm ở dòng cần thao tác.\n'
            '2. Người dùng chọn Khóa (hoặc Mở khóa).\n'
            '3. Hệ thống hiện hộp xác nhận nêu rõ tên bản ghi.\n'
            '4. Người dùng xác nhận.\n'
            '5. Hệ thống đổi trạng thái, ghi lịch sử và cập nhật cột Trạng thái.',
            '• Bấm Hủy → đóng hộp, trạng thái không đổi.\n'
            '• Sau khi Khóa, hai nút Sửa và Xóa của dòng đó BIẾN MẤT, chỉ còn Mở khóa và '
            'Lịch sử.\n'
            '• Bản ghi đã bị người khác đổi trạng thái trước đó → hệ thống báo dữ liệu đã '
            'thay đổi.')

        d.p('2.6.3 Layout màn hình')
        d.layout(modal='Khóa %s' % dt, shot=shot(S['khoa']),
                 shot_caption='Hộp xác nhận khóa %s' % dt)
        if 'menu' in S:
            d.figure(shot(S['menu']),
                     'Nút ba chấm chứa hai thao tác Khóa và Lịch sử', width_in=6.2)

        d.p('2.6.4 Mô tả chi tiết giao diện')
        d.ui_table([
            ('Nút ba chấm “Hành động khác”', 'Icon Button', 'Enable', 'Hiển thị',
             'Chứa hai mục Khóa / Mở khóa và Lịch sử.'),
            ('Mục Khóa / Mở khóa', 'Button', 'Enable', 'Theo trạng thái dòng',
             'Nhãn đổi theo trạng thái hiện tại của bản ghi.'),
            ('Tiêu đề hộp xác nhận', 'Label', 'Hiển thị', 'Khóa %s' % dt,
             'Đổi thành “Mở khóa %s” khi bản ghi đang bị khóa.' % dt),
            ('Nội dung hộp xác nhận', 'Label', 'Hiển thị',
             'Bạn có chắc muốn khóa %s “<tên>”?' % dt, 'Nêu rõ tên bản ghi.'),
            ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Xác nhận thực hiện.'),
            ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không làm gì.'),
            ('Cột Trạng thái', 'Badge', 'Read-only', 'Theo dữ liệu',
             'Hoạt động hoặc Khóa, hai màu khác nhau.'),
        ], required=False, scope=False)

        d.p('2.6.5 Danh sách event và xử lý event')
        d.event_table([
            ('Bấm nút ba chấm', 'Click',
             'After:\n– Mở menu gồm hai mục Khóa / Mở khóa và Lịch sử.'),
            ('Chọn Khóa hoặc Mở khóa', 'Click',
             'After:\n– Hiện hộp xác nhận kèm tên bản ghi.'),
            ('Xác nhận trong hộp', 'Click',
             'During:\n– Bản ghi không còn tồn tại hoặc đã ở trạng thái đích → hiển thị thông '
             'báo dữ liệu đã thay đổi và dừng xử lý.\n'
             'After:\n– Đổi trạng thái bản ghi, KHÔNG xóa dữ liệu.\n'
             '– Ghi một dòng lịch sử đổi trạng thái.\n'
             '– Cập nhật cột Trạng thái và các nút thao tác của dòng.'),
            ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp xác nhận, không thay đổi gì.'),
        ])
        n = 7

    # ---------------------------------------------------------- Lịch sử
    d.h3('2.%d Xem lịch sử thay đổi' % n)

    d.p('2.%d.1 Giới thiệu' % n)
    d.intro_table(
        'Xem lịch sử thay đổi',
        'Liệt kê các lần thay đổi của một %s, kèm giá trị cũ, giá trị mới, người thực hiện '
        'và thời điểm.' % dt,
        ACTOR,
        'Bản ghi cần xem đang có trong danh sách.',
        '1. Người dùng mở lịch sử của bản ghi từ cột Hành động.\n'
        '2. Hệ thống mở cửa sổ Lịch sử thay đổi.\n'
        '3. Danh sách các lần thay đổi hiển thị theo thứ tự mới nhất ở trên cùng.',
        '• Bản ghi chưa từng sửa → cửa sổ hiện “Chưa có lịch sử thao tác nào.”\n'
        '• Cửa sổ có bộ lọc riêng để thu hẹp theo loại thay đổi.')

    d.p('2.%d.2 Layout màn hình' % n)
    d.layout(modal='Lịch sử thay đổi', shot=shot(S['lichsu']),
             shot_caption='Cửa sổ Lịch sử thay đổi của %s' % dt)

    d.p('2.%d.3 Mô tả chi tiết giao diện' % n)
    d.ui_table([
        ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Lịch sử thay đổi',
         'Kèm dòng phụ ghi loại đối tượng và tên bản ghi.'),
        ('Bộ lọc', 'Dropdown', 'Enable', 'Trống', 'Thu hẹp theo loại thay đổi.'),
        ('Danh sách thay đổi', 'Table/Grid', 'Read-only', 'Theo dữ liệu',
         'Sắp xếp mới nhất ở trên cùng.'),
        ('Thời điểm', 'Text', 'Read-only', 'Theo dữ liệu', 'Định dạng dd/mm/yyyy hh:mm.'),
        ('Loại thay đổi', 'Badge', 'Read-only', 'Theo dữ liệu',
         'Ví dụ: Thay đổi thông tin, Khóa, Mở khóa.'),
        ('Người thực hiện', 'Text', 'Read-only', 'Theo dữ liệu',
         'Kèm mã nhân viên và phòng ban.'),
        ('Giá trị cũ và giá trị mới', 'Text', 'Read-only', 'Theo dữ liệu',
         'Hiển thị hai vế cho từng trường đã đổi.'),
        ('Trạng thái rỗng', 'Label', 'Hiển thị', 'Ẩn',
         'Hiện “Chưa có lịch sử thao tác nào.” khi bản ghi chưa từng sửa.'),
        ('Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ.'),
    ], required=False, scope=False)

    d.p('2.%d.4 Danh sách event và xử lý event' % n)
    d.event_table([
        ('Mở lịch sử của một bản ghi', 'Click',
         'After:\n– Mở cửa sổ và nạp danh sách thay đổi theo thứ tự mới nhất trước.'),
        ('Đổi bộ lọc trong cửa sổ', 'Change',
         'After:\n– Nạp lại danh sách theo tiêu chí đã chọn.'),
        ('Bấm Đóng', 'Click',
         'After:\n– Đóng cửa sổ; danh sách phía sau giữ nguyên bộ lọc và trang.'),
    ])

    # ================================================== PHẦN 4
    d.h1('Phần 4. Quy tắc nghiệp vụ')

    d.p('BR-01 — Màn hình chưa được gắn quyền')
    d.bullets([
        'Không chức năng nào của màn hình kiểm tra quyền, kể cả Thêm mới, Chỉnh sửa, Xóa'
        + (' và Khóa / Mở khóa.' if co_khoa else '.'),
        'Mọi người dùng đã đăng nhập đều thao tác được đầy đủ.',
        'Giao diện cố ý KHÔNG tạo cờ quyền giả để ẩn nút, vì quy ước của dự án cấm gán cứng '
        'giá trị cho cờ quyền.',
        'Đây là hiện trạng cần được xem xét bổ sung quyền, do danh mục địa lý được dùng chung '
        'cho toàn hệ thống.',
    ])

    d.p('BR-02 — Ràng buộc trùng tên')
    d.bullets([
        'Tên %s không được trùng %s.' % (dt, cfg['pham_vi_trung']),
        'Khi sửa, bản ghi đang sửa được loại khỏi phép kiểm tra trùng — giữ nguyên tên của '
        'chính nó thì lưu bình thường.',
        'Thông báo khi trùng: “%s”.' % cfg['loi_trung_ten'],
    ])
    if cfg.get('ghi_chu_loi_trung'):
        d.p(cfg['ghi_chu_loi_trung'])

    d.p('BR-03 — Quan hệ với các cấp địa chỉ khác')
    if cfg['cap_tren']:
        d.bullets([
            'Mỗi %s bắt buộc trực thuộc %s.' % (dt, cfg['cap_tren']),
            'Đổi cấp trên thì các ô cấp dưới bị xóa trắng và nạp lại theo giá trị mới.',
            'Danh mục này là nguồn dữ liệu cho ô địa chỉ ở các màn nghiệp vụ khác, nên sửa hoặc '
            'khóa một bản ghi sẽ ảnh hưởng tới mọi màn đang dùng nó.',
        ])
    else:
        d.bullets([
            'Quốc gia là gốc của cây địa chỉ, không trực thuộc cấp nào.',
            'Mọi Khu vực và Tỉnh/TP đều phải trỏ về một quốc gia, nên xóa hoặc khóa một quốc gia '
            'sẽ ảnh hưởng tới toàn bộ nhánh địa chỉ bên dưới.',
        ])

    if co_khoa:
        d.p('BR-04 — Khóa không phải Xóa')
        d.bullets([
            'Bản ghi đã Khóa VẪN nằm trong danh mục với nhãn Khóa, vẫn xem được lịch sử.',
            'Tác dụng của Khóa là chặn bản ghi khỏi các ô chọn ở màn nghiệp vụ khác.',
            'Sau khi Khóa, hai nút Sửa và Xóa của dòng đó BIẾN MẤT — muốn sửa phải Mở khóa trước.',
        ])
        d.p('BR-05 — Bộ lọc mặc định không lọc trạng thái')
        d.bullets([
            'Vào màn hình, danh sách hiện CẢ bản ghi Hoạt động lẫn bản ghi đã Khóa.',
            'Trước đây bộ lọc mặc định là Hoạt động nên giấu mất bản ghi đã khóa; hành vi hiện '
            'tại là chủ đích sửa lại.',
        ])
    else:
        d.p('BR-04 — Xóa là ngừng sử dụng')
        d.bullets([
            'Màn hình này không có cột Trạng thái và không có thao tác Khóa / Mở khóa.',
            'Danh sách chỉ hiển thị bản ghi còn hiệu lực; phép lọc này nằm ở phía máy chủ nên '
            'người dùng không đổi được.',
            'Thao tác Xóa chuyển bản ghi sang trạng thái ngừng sử dụng — bản ghi biến mất khỏi '
            'danh sách nhưng dữ liệu không mất hẳn.',
        ])

    if cfg['key'] == 'hamlets':
        d.p('BR-05 — Quy tắc riêng với Việt Nam')
        d.bullets([
            'Khi Quốc gia là Việt Nam, ô Quận/Huyện/Thị xã bị ẨN HẲN và không phải nhập; địa chỉ '
            'đi thẳng từ Tỉnh/TP xuống Phường/Xã.',
            'Với mọi quốc gia khác, ô Quận/Huyện/Thị xã hiện ra và BẮT BUỘC nhập.',
            'Quy tắc này chỉ áp cho màn Đường/Phố.',
        ])

    d.p('BR-%02d — Lịch sử thay đổi sắp xếp mới nhất trước' % (6 if co_khoa else 5))
    d.bullets([
        'Mọi thao tác sửa%s đều sinh dòng lịch sử.'
        % (' và đổi trạng thái' if co_khoa else ''),
        'Danh sách lịch sử luôn sắp xếp MỚI NHẤT Ở TRÊN CÙNG.',
        'Mỗi dòng nêu trường đã đổi, giá trị cũ, giá trị mới, người thực hiện và thời điểm.',
    ])

    d.save()
    return out


if __name__ == '__main__':
    for cfg in SCREENS:
        build(cfg)
