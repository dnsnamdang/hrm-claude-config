# -*- coding: utf-8 -*-
"""Bo sinh SRS dung chung cho cac man DANH MUC (form moi 4 phan, chot 2026-08-17).

Dung cho 7 man duoc lam lai tai lieu ngay 18/08/2026:
  Cap dich vu bao duong · Ghi chu kiem tra bao duong · Serial thiet bi lam dich vu ·
  Cap nhat nhanh gia dich vu · Danh muc tai khoan · Danh muc loai tai khoan · Danh muc tien te

Moi man khai 1 dict cau hinh + danh sach `funcs` (thu tu chuc nang). Thu vien tu dung
du 4 phan, ma tran phan quyen, so do UML va tung muc 2.x theo dung form.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "..", "..", ".claude", "skills", "srs-documenter", "assets")
sys.path.insert(0, ASSETS)

from srs_docx_lib import SrsDoc  # noqa: E402

# ---------------------------------------------------------------- dinh nghia chuc nang
# ma FR -> (nhan mac dinh, nhom mau UML, co usecase rieng khong)
FUNC_META = {
    'list':    ('Xem danh sách',            'view',   False),
    'filter':  ('Tìm kiếm và lọc',          'view',   False),
    'columns': ('Tùy chỉnh cột hiển thị',   'view',   True),
    'fcfg':    ('Cài đặt bộ lọc',           'view',   True),
    'view':    ('Xem chi tiết',             'view',   False),
    'create':  ('Thêm mới',                 'crud',   True),
    'edit':    ('Chỉnh sửa',                'crud',   True),
    'delete':  ('Xóa',                      'action', True),
    'lock':    ('Khóa / Mở khóa',           'action', True),
    'history': ('Xem lịch sử thay đổi',     'view',   False),
    'import':  ('Nhập dữ liệu từ Excel',    'io',     True),
    'export':  ('Xuất Excel',               'io',     True),
    'print':   ('In danh sách',             'io',     True),
    'save':    ('Lưu cấu hình',             'crud',   True),
}


def _shot(shots_dir, name):
    p = os.path.join(shots_dir, name)
    if not os.path.exists(p):
        raise IOError('Thieu anh: %s' % p)
    return p


class CatalogSrs(object):
    def __init__(self, cfg, shots_dir, out_dir):
        self.c = cfg
        self.shots_dir = shots_dir
        self.out_dir = out_dir
        self.ten = cfg['ten']
        self.dt = cfg['doi_tuong']
        self.qql = cfg['quyen_quan_ly']
        self.qxem = cfg.get('quyen_xem')
        self.funcs = [f if isinstance(f, tuple) else (f, {}) for f in cfg['funcs']]
        self.url = cfg['host'] + cfg['route']
        # Tac nhan
        self.P1 = 'Người quản lý danh mục (có quyền “%s”)' % self.qql
        self.P2 = ('Người tra cứu (chỉ có quyền “%s”)' % self.qxem) if self.qxem else None

    # -------------------------------------------------------------- tien ich
    def shot(self, key):
        return _shot(self.shots_dir, self.c['shots'][key])

    def has(self, name):
        return any(f[0] == name for f in self.funcs)

    def fr_code(self, name):
        for i, f in enumerate(self.funcs):
            if f[0] == name:
                return 'FR-%02d' % (i + 1)
        return None

    def label(self, name, opts):
        if 'nhan' in opts:
            return opts['nhan']
        base = FUNC_META[name][0]
        if name in ('list', 'view', 'create', 'edit', 'delete'):
            return '%s %s' % (base, self.dt)
        return base

    # -------------------------------------------------------------- dung file
    def build(self):
        c = self.c
        out = os.path.join(self.out_dir, 'SRS - %s.docx' % self.ten.replace('/', '-'))
        d = SrsDoc(out=out, menu=c['menu'], route=c['route'], full_url=self.url,
                   img_prefix=c['key'] + '_')
        self.d = d

        d.title_block(self.ten)
        d.h2('Mục lục')
        d.toc()

        self._phan1()
        self._phan2()
        self._phan3()
        self._phan4()

        d.save()
        return out

    # ================================================================ PHAN 1
    def _phan1(self):
        d, c = self.d, self.c
        d.h1('Phần 1. Giới thiệu')
        d.h2('1 Mục đích')
        d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s, nhằm:' % self.ten)
        d.bullets(c['muc_dich'])

        d.h2('2 Thuật ngữ và viết tắt')
        d.table(['Thuật ngữ', 'Mô tả'],
                c['thuat_ngu'] + [('SRS', 'Software Requirements Specification — tài liệu '
                                          'đặc tả yêu cầu phần mềm.')],
                widths=[1.8, 4.2])

    # ================================================================ PHAN 2
    def _phan2(self):
        d, c = self.d, self.c
        d.h1('Phần 2. Phân quyền')
        d.h2('1 Danh sách quyền')

        rows = [('P1', self.qql, c['tacdung_ql'])]
        if self.qxem:
            rows.append(('P2', self.qxem, c['tacdung_xem']))
        d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], rows, widths=[0.8, 2.2, 3.0])
        d.p(c['ghichu_quyen'])

        d.h2('2 Ma trận phân quyền')
        cols = ['Chức năng', 'P1'] + (['P2'] if self.qxem else []) + ['Không có quyền nào']
        body = []
        for name, opts in self.funcs:
            ok_xem = opts.get('chi_doc', FUNC_META[name][1] in ('view',)) or name == 'export'
            r = ['%s %s' % (self.fr_code(name), self.label(name, opts)), '✅']
            if self.qxem:
                r.append('✅' if ok_xem else '❌')
            r.append('❌')
            body.append(tuple(r))
        w = [3.0, 1.0, 1.0, 1.0] if self.qxem else [3.4, 1.3, 1.3]
        d.table(cols, body, widths=w)

    # ================================================================ PHAN 3
    def _phan3(self):
        d, c = self.d, self.c
        d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

        d.h2('1 Sơ đồ UML tổng quan')
        ucs, idx_p1, idx_p2 = [], [], []
        for i, (name, opts) in enumerate(self.funcs):
            ucs.append((self.fr_code(name), self.label(name, opts),
                        FUNC_META[name][1], opts.get('uml_note')))
            idx_p1.append(i)
            if self.qxem and (opts.get('chi_doc', FUNC_META[name][1] == 'view')
                              or name == 'export'):
                idx_p2.append(i)
        actors = [(self.P1, idx_p1)]
        if self.qxem:
            actors.append((self.P2, idx_p2))
        d.overview_figure('HỆ THỐNG HRM — %s' % self.ten.upper(), actors, ucs,
                          'Sơ đồ Use Case tổng quan màn %s' % self.ten)

        d.h2('2 Đặc tả chi tiết từng chức năng')
        for i, (name, opts) in enumerate(self.funcs):
            getattr(self, '_fn_' + name)(i + 1, opts)

    # ---------------------------------------------------------------- helper muc 2.x
    def _head(self, no, name, opts):
        """Tra ve (prefix danh so, co usecase khong)."""
        self.d.h3('2.%d %s' % (no, self.label(name, opts)))
        return '2.%d' % no, FUNC_META[name][2]

    def _uc(self, pre, name, opts, rel):
        self.d.p('%s.1 Biểu đồ Usecase' % pre)
        self.d.uc_figure(self.fr_code(name), self.label(name, opts),
                         FUNC_META[name][1], rel, actor=self.P1)
        return 2

    # ---------------------------------------------------------------- 1. Xem danh sach
    def _fn_list(self, no, opts):
        d, c = self.d, self.c
        pre, _ = self._head(no, 'list', opts)
        d.p('%s.1 Giới thiệu' % pre)
        d.intro_table(
            self.label('list', opts),
            'Hiển thị toàn bộ %s trong danh mục, có phân trang, sắp xếp và tùy chỉnh cột.'
            % self.dt,
            self._tacnhan(True),
            'Người dùng có quyền “%s”%s.'
            % (self.qql, ' hoặc “%s”' % self.qxem if self.qxem else ''),
            '1. Người dùng vào %s.\n'
            '2. Hệ thống kiểm tra quyền rồi nạp trang đầu tiên của danh sách.\n'
            '3. Bảng hiển thị dữ liệu kèm tổng số bản ghi.' % c['menu'],
            '• Không có quyền → mục menu không hiển thị; truy cập thẳng đường dẫn thì hệ thống '
            'từ chối và báo không có quyền.\n'
            '• Danh mục chưa có bản ghi nào → bảng hiện thông báo không có dữ liệu.')

        d.p('%s.2 Layout màn hình' % pre)
        d.layout(shot=self.shot('danhsach'), shot_caption='Màn %s lúc mới truy cập' % self.ten)

        d.p('%s.3 Mô tả chi tiết giao diện' % pre)
        rows = [(x[0], 'Table/Grid', 'Read-only', '–', '–', x[1]) for x in c['cot']]
        rows += c.get('nut_thanh_cong_cu', [])
        rows += [
            ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
             'Nút về đầu / lùi / số trang / tiến / về cuối và ô chọn số dòng mỗi trang '
             '(5, 10, 20, 50, 100).'),
            ('Tổng số bản ghi', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
             'Dòng “Hiển thị x–y / tổng” ở góc trái dưới bảng.'),
            ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
             'Hiện “Không có dữ liệu phù hợp bộ lọc.” khi danh sách trống.'),
            ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Ẩn', 'Hiện trong lúc nạp dữ liệu.'),
        ]
        d.ui_table(rows, required=False)

        d.p('%s.4 Danh sách event và xử lý event' % pre)
        d.event_table([
            ('Mở màn hình', 'System',
             'Before:\n– Kiểm tra quyền “%s”.\n'
             '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
             'và dừng xử lý.\n'
             'After:\n– Nạp trang đầu tiên của danh sách và hiển thị tổng số bản ghi.'
             % self._ten_quyen_xem()),
            ('Bấm tiêu đề cột sắp xếp được', 'Click',
             'After:\n– Đổi chiều sắp xếp (tăng ↔ giảm) và nạp lại danh sách từ trang 1.'),
            ('Chuyển trang', 'Click',
             'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
             'After:\n– Nạp dữ liệu trang mới, số thứ tự chạy tiếp tục không quay về 1.'),
            ('Đổi số dòng mỗi trang', 'Change',
             'After:\n– Quay về trang 1 và nạp lại theo số dòng mới.'),
        ])

    # ---------------------------------------------------------------- 2. Tim kiem & loc
    def _fn_filter(self, no, opts):
        d, c = self.d, self.c
        pre, _ = self._head(no, 'filter', opts)
        nhieu = len(c['loc']) > 1
        d.p('%s.1 Giới thiệu' % pre)
        d.intro_table(
            'Tìm kiếm và lọc danh sách',
            'Thu hẹp danh sách bằng ô tìm kiếm nhanh%s.'
            % (' và các tiêu chí lọc nâng cao' if nhieu else
               '. Màn hình này KHÔNG có bộ lọc nâng cao'),
            self._tacnhan(True),
            'Đang ở màn %s.' % self.ten,
            '1. Người dùng nhập từ khóa hoặc chọn tiêu chí lọc.\n'
            '2. Người dùng bấm Tìm kiếm.\n'
            '3. Hệ thống áp đồng thời mọi tiêu chí và nạp lại danh sách từ trang 1.',
            '• Không có kết quả → bảng hiện thông báo không có dữ liệu.\n'
            '• Bấm Làm mới → xóa hết tiêu chí VÀ nạp lại danh sách đầy đủ ngay lập tức.')

        d.p('%s.2 Layout màn hình' % pre)
        d.layout(shot=self.shot(c['shots'].get('boloc') and 'boloc' or 'danhsach'),
                 shot_caption='Khu vực tìm kiếm và lọc của màn %s' % self.ten)

        d.p('%s.3 Mô tả chi tiết giao diện' % pre)
        rows = [(f[0], f[1], 'Enable', f[2], 'Không', f[3], f[4]) for f in c['loc']]
        rows += [
            ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
             'Áp dụng đồng thời mọi tiêu chí đang nhập.'),
            ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
             'Xóa hết tiêu chí VÀ nạp lại danh sách đầy đủ ngay.'),
        ]
        d.ui_table(rows)

        d.p('%s.4 Danh sách event và xử lý event' % pre)
        d.event_table([
            ('Bấm Tìm kiếm', 'Click',
             'Before:\n– Thu thập giá trị của mọi tiêu chí đang có.\n'
             'During:\n– Áp đồng thời các tiêu chí theo kiểu “và”.\n'
             'After:\n– Nạp lại bảng từ trang 1 và cập nhật tổng số bản ghi.'),
            ('Bấm Làm mới', 'Click',
             'After:\n– Xóa trắng mọi tiêu chí VÀ nạp lại danh sách đầy đủ ngay lập tức.'),
            ('Gõ vào ô tìm nhanh rồi nhấn Enter', 'Keypress',
             'After:\n– Chạy tìm kiếm y như bấm nút Tìm kiếm.'),
        ])

    # ---------------------------------------------------------------- Tuy chinh cot
    def _fn_columns(self, no, opts):
        d = self.d
        pre, _ = self._head(no, 'columns', opts)
        n = self._uc(pre, 'columns', opts,
                     [('include', 'Lưu cấu hình theo từng người dùng')])
        d.p('%s.%d Giới thiệu' % (pre, n))
        d.intro_table(
            'Tùy chỉnh cột hiển thị',
            'Chọn những cột muốn thấy trên bảng danh sách. Cấu hình lưu riêng cho từng người '
            'dùng và giữ nguyên ở các lần vào sau.',
            self._tacnhan(True),
            'Đang ở màn %s.' % self.ten,
            '1. Người dùng bấm biểu tượng tùy chỉnh cột ở góc phải thanh công cụ.\n'
            '2. Hệ thống mở cửa sổ liệt kê toàn bộ cột kèm ô tích.\n'
            '3. Người dùng tích / bỏ tích rồi bấm Lưu.\n'
            '4. Bảng vẽ lại theo bộ cột mới.',
            '• Bấm Đóng → giữ nguyên cấu hình cũ.\n'
            '• Cột bắt buộc (STT, cột tên và Hành động) luôn được chọn, không bỏ tích được.')
        d.p('%s.%d Layout màn hình' % (pre, n + 1))
        d.layout(modal='Tuỳ chỉnh cột', shot=self.shot('cot'),
                 shot_caption='Cửa sổ Tuỳ chỉnh cột hiển thị')
        d.p('%s.%d Mô tả chi tiết giao diện' % (pre, n + 2))
        d.ui_table([
            ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách', 'Không',
             'Theo cấu hình đã lưu', 'Mỗi dòng là một cột kèm ô tích bật/tắt.'),
            ('Ô tích của cột bắt buộc', 'Icon Button', 'Disable', '–', '–', 'Đã tích',
             'STT, cột tên và Hành động luôn hiển thị nên không bỏ tích được.'),
            ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị',
             'Ghi cấu hình và vẽ lại bảng.'),
            ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Giữ nguyên cấu hình cũ.'),
        ])
        d.p('%s.%d Danh sách event và xử lý event' % (pre, n + 3))
        d.event_table([
            ('Tích / bỏ tích một cột', 'Change',
             'After:\n– Cập nhật lựa chọn tạm thời, bảng chưa đổi cho tới khi bấm Lưu.'),
            ('Bấm Lưu', 'Click',
             'After:\n– Ghi cấu hình cột cho riêng người dùng hiện tại.\n'
             '– Đóng cửa sổ và vẽ lại bảng theo bộ cột mới.'),
        ])

    # ---------------------------------------------------------------- Cai dat bo loc
    def _fn_fcfg(self, no, opts):
        d = self.d
        pre, _ = self._head(no, 'fcfg', opts)
        n = self._uc(pre, 'fcfg', opts, [('include', 'Lưu cấu hình theo từng người dùng')])
        d.p('%s.%d Giới thiệu' % (pre, n))
        d.intro_table(
            'Cài đặt bộ lọc',
            'Chọn những ô lọc muốn hiển thị và sắp xếp thứ tự của chúng trên khu vực tìm kiếm '
            'nâng cao. Cấu hình lưu riêng theo từng người dùng và từng màn hình.',
            self._tacnhan(True),
            'Đang ở màn %s.' % self.ten,
            '1. Người dùng bấm nút Cài đặt bộ lọc.\n'
            '2. Hệ thống mở cửa sổ liệt kê toàn bộ ô lọc kèm ô tích.\n'
            '3. Người dùng tích chọn, kéo thả để đổi thứ tự rồi bấm Lưu.\n'
            '4. Khu vực lọc vẽ lại theo cấu hình mới.',
            '• Bấm Khôi phục mặc định → đưa về bộ ô lọc gốc của màn hình.\n'
            '• Bấm Đóng → giữ nguyên cấu hình cũ.')
        d.p('%s.%d Layout màn hình' % (pre, n + 1))
        d.layout(modal='Cài đặt bộ lọc', shot=self.shot('caidat_boloc'),
                 shot_caption='Cửa sổ Cài đặt bộ lọc')
        d.p('%s.%d Mô tả chi tiết giao diện' % (pre, n + 2))
        d.ui_table([
            ('Danh sách ô lọc', 'Table/Grid', 'Enable', 'Danh sách', 'Không',
             'Theo cấu hình đã lưu', 'Mỗi dòng là một ô lọc kèm ô tích và tay nắm kéo thả.'),
            ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
             'Kéo để đổi thứ tự ô lọc.'),
            ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình.'),
            ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
             'Đưa về bộ ô lọc gốc.'),
            ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Giữ nguyên cấu hình cũ.'),
        ])
        d.p('%s.%d Danh sách event và xử lý event' % (pre, n + 3))
        d.event_table([
            ('Kéo thả đổi thứ tự', 'Change',
             'After:\n– Cập nhật thứ tự tạm thời, chưa áp dụng cho tới khi bấm Lưu.'),
            ('Bấm Lưu', 'Click',
             'After:\n– Ghi cấu hình cho riêng người dùng và màn hình hiện tại.\n'
             '– Vẽ lại khu vực lọc theo cấu hình mới.'),
            ('Bấm Khôi phục mặc định', 'Click',
             'After:\n– Xóa cấu hình riêng và đưa khu vực lọc về bộ ô gốc.'),
        ])

    # ---------------------------------------------------------------- Xem chi tiet
    def _fn_view(self, no, opts):
        d, c = self.d, self.c
        pre, _ = self._head(no, 'view', opts)
        modal = opts.get('modal', True)
        d.p('%s.1 Giới thiệu' % pre)
        d.intro_table(
            self.label('view', opts),
            'Xem đầy đủ thông tin của một %s ở chế độ chỉ đọc, không sửa được.' % self.dt,
            self._tacnhan(True),
            'Người dùng có quyền “%s”%s.'
            % (self.qql, ' hoặc “%s”' % self.qxem if self.qxem else ''),
            '1. Người dùng bấm vào %s ở cột đầu của dòng cần xem.\n'
            '2. Hệ thống %s và đổ dữ liệu ở chế độ chỉ đọc.'
            % (opts.get('cot_bam', 'tên'),
               'mở cửa sổ xem' if modal else 'mở màn hình chi tiết'),
            '• Bản ghi đã bị người khác xóa → hệ thống báo không tìm thấy dữ liệu.')
        d.p('%s.2 Layout màn hình' % pre)
        if modal:
            d.layout(modal='Xem %s' % self.dt, shot=self.shot('xem'),
                     shot_caption='Cửa sổ Xem %s' % self.dt)
        else:
            d.layout(route=opts.get('route'), shot=self.shot('xem'),
                     shot_caption='Màn hình Chi tiết %s' % self.dt)
        d.p('%s.3 Mô tả chi tiết giao diện' % pre)
        rows = [(t[0], t[1], 'Read-only', t[3], t[5], t[6]) for t in c['truong']]
        rows += opts.get('them_dong', [])
        rows.append(('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị',
                     'Đóng cửa sổ, không ghi gì.') if modal else
                    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị',
                     'Trở về màn danh sách.'))
        d.ui_table(rows, required=False)
        d.p('%s.4 Danh sách event và xử lý event' % pre)
        d.event_table([
            ('Bấm %s trên dòng' % opts.get('cot_bam', 'tên'), 'Click',
             'Before:\n– Kiểm tra quyền “%s”.\n'
             'After:\n– Nạp dữ liệu bản ghi và hiển thị ở chế độ chỉ đọc.'
             % self._ten_quyen_xem()),
            ('Bấm %s' % ('Đóng' if modal else 'Quay lại'), 'Click',
             'After:\n– %s, không ghi gì.'
             % ('Đóng cửa sổ' if modal else 'Trở về màn danh sách')),
        ])

    # ---------------------------------------------------------------- Them moi
    def _fn_create(self, no, opts):
        d, c = self.d, self.c
        pre, _ = self._head(no, 'create', opts)
        modal = opts.get('modal', True)
        rel = [('include', 'Kiểm tra quyền “%s”' % self.qql)]
        if c.get('loi_trung'):
            rel.append(('include', 'Kiểm tra trùng %s' % c['truong_trung']))
        rel += opts.get('rel_them', [])
        n = self._uc(pre, 'create', opts, rel)

        d.p('%s.%d Giới thiệu' % (pre, n))
        d.intro_table(
            self.label('create', opts),
            'Thêm một %s mới vào danh mục thông qua %s.'
            % (self.dt, 'cửa sổ nhập liệu' if modal else 'màn hình nhập liệu riêng'),
            self.P1,
            'Người dùng có quyền “%s”.' % self.qql,
            '1. Người dùng bấm nút Tạo mới.\n'
            '2. Hệ thống %s.\n'
            '3. Người dùng nhập thông tin và bấm Lưu.\n'
            '4. Hệ thống kiểm tra dữ liệu và ghi bản ghi mới.\n'
            '5. %s, danh sách nạp lại và hiển thị thông báo thành công.'
            % ('mở cửa sổ nhập liệu' if modal else 'mở màn hình nhập liệu',
               'Cửa sổ đóng' if modal else 'Hệ thống quay về màn danh sách'),
            '• Thiếu trường bắt buộc hoặc trùng %s → báo lỗi đỏ ngay dưới ô tương ứng, '
            '%s KHÔNG đóng, dữ liệu đã nhập vẫn còn.\n'
            '• Bấm Lưu và tiếp tục → ghi xong vẫn giữ form mở, làm trắng các ô để nhập tiếp.\n'
            '• Bấm %s → hủy bỏ, không ghi gì.'
            % (c.get('truong_trung', 'tên'), 'cửa sổ' if modal else 'màn hình',
               'Đóng' if modal else 'Quay lại'),
            opts.get('dacbiet'))

        d.p('%s.%d Layout màn hình' % (pre, n + 1))
        if modal:
            d.layout(modal='Tạo %s' % self.dt, shot=self.shot('taomoi'),
                     shot_caption='Cửa sổ Tạo %s' % self.dt)
        else:
            d.layout(route=opts.get('route'), shot=self.shot('taomoi'),
                     shot_caption='Màn hình Thêm %s' % self.dt)
        if 'validate' in c['shots']:
            d.figure(self.shot('validate'),
                     'Hệ thống báo lỗi đỏ ngay dưới ô còn thiếu', width_in=6.2)

        d.p('%s.%d Mô tả chi tiết giao diện' % (pre, n + 2))
        rows = list(c['truong'])
        rows += [
            ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị',
             'Ghi bản ghi rồi %s.' % ('đóng cửa sổ' if modal else 'quay về danh sách')),
            ('Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', 'Hiển thị',
             'Ghi bản ghi, giữ form mở và làm trắng các ô để nhập tiếp.'),
            ('Nút %s' % ('Đóng' if modal else 'Quay lại'), 'Button', 'Enable', '–', '–',
             'Hiển thị', 'Hủy bỏ, không ghi gì.'),
            ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
             'Chữ đỏ ngay dưới ô bị lỗi.'),
        ]
        d.ui_table(rows)

        d.p('%s.%d Danh sách event và xử lý event' % (pre, n + 3))
        during = ['– %s để trống → hiển thị “Bắt buộc phải nhập”.' % t[0]
                  for t in c['truong'] if t[4] == 'Có']
        during += c.get('loi_khac', [])
        if c.get('loi_trung'):
            during.append('– %s đã tồn tại → hiển thị “%s”.'
                          % (c['truong_trung'], c['loi_trung']))
        during.append('– Nếu có lỗi kiểm tra → không thực hiện bước After.')
        d.event_table([
            ('Bấm nút Tạo mới', 'Click',
             'Before:\n– Kiểm tra quyền “%s”.\n'
             '– Nếu không có quyền → nút không hiển thị.\n'
             'After:\n– Mở form nhập liệu trắng%s.'
             % (self.qql,
                ', ô Trạng thái đặt sẵn là Hoạt động' if c.get('co_trangthai') else '')),
            ('Bấm Lưu', 'Click',
             'Before:\n– Kiểm tra quyền “%s”.\n'
             '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” '
             'và dừng xử lý.\n'
             'During:\n%s\n'
             'After:\n– Ghi bản ghi mới vào danh mục.\n'
             '– Ghi một dòng lịch sử ghi nhận việc thêm mới.\n'
             '– %s và nạp lại danh sách.\n'
             '– Hiển thị thông báo “%s”.'
             % (self.qql, '\n'.join(during),
                'Đóng cửa sổ' if modal else 'Quay về màn danh sách',
                c.get('tb_them', 'Thêm mới thành công'))),
            ('Bấm Lưu và tiếp tục', 'Click',
             'During:\n– Kiểm tra y hệt nút Lưu.\n'
             'After:\n– Ghi bản ghi mới, giữ form mở và làm trắng các ô để nhập bản ghi tiếp '
             'theo.'),
            ('Bấm %s' % ('Đóng' if modal else 'Quay lại'), 'Click',
             'After:\n– Hủy bỏ toàn bộ dữ liệu đang nhập, không ghi gì.'),
        ])

    # ---------------------------------------------------------------- Chinh sua
    def _fn_edit(self, no, opts):
        d, c = self.d, self.c
        pre, _ = self._head(no, 'edit', opts)
        modal = opts.get('modal', True)
        rel = [('include', 'Kiểm tra quyền “%s”' % self.qql)]
        if c.get('loi_trung'):
            rel.append(('include', 'Kiểm tra trùng %s (bỏ qua chính nó)' % c['truong_trung']))
        if c.get('co_trangthai'):
            rel.append(('extend', 'Chặn sửa khi bản ghi đang Khóa'))
        rel += opts.get('rel_them', [])
        n = self._uc(pre, 'edit', opts, rel)

        khoa = (' Bản ghi đang ở trạng thái Khóa thì nút Sửa bị ẩn, phải Mở khóa trước.'
                if c.get('co_trangthai') else '')
        d.p('%s.%d Giới thiệu' % (pre, n))
        d.intro_table(
            self.label('edit', opts),
            'Sửa thông tin của một %s đã có.%s' % (self.dt, khoa),
            self.P1,
            'Người dùng có quyền “%s”%s.'
            % (self.qql, ' và bản ghi đang ở trạng thái Hoạt động'
               if c.get('co_trangthai') else ''),
            '1. Người dùng bấm nút Sửa trên dòng cần sửa.\n'
            '2. Hệ thống mở form đã điền sẵn dữ liệu hiện tại.\n'
            '3. Người dùng chỉnh sửa và bấm Lưu.\n'
            '4. Hệ thống kiểm tra dữ liệu và cập nhật bản ghi.\n'
            '5. Danh sách nạp lại và hiển thị thông báo thành công.',
            '• Thiếu trường bắt buộc hoặc trùng %s → báo lỗi đỏ ngay dưới ô tương ứng.\n'
            '• Bản ghi bị người khác khóa trong lúc đang mở form → hệ thống từ chối lưu và báo '
            'bản ghi đang bị khóa.\n'
            '• Thoát khi chưa lưu → hệ thống hỏi xác nhận rời khỏi.'
            % c.get('truong_trung', 'tên'),
            opts.get('dacbiet'))

        d.p('%s.%d Layout màn hình' % (pre, n + 1))
        if modal:
            d.layout(modal='Sửa %s' % self.dt, shot=self.shot('sua'),
                     shot_caption='Cửa sổ Sửa %s' % self.dt)
        else:
            d.layout(route=opts.get('route'), shot=self.shot('sua'),
                     shot_caption='Màn hình Sửa %s' % self.dt)

        d.p('%s.%d Mô tả chi tiết giao diện' % (pre, n + 2))
        rows = [(t[0], t[1], t[2], t[3], t[4], 'Theo dữ liệu', t[6]) for t in c['truong']]
        rows += opts.get('them_dong', [])
        rows += [
            ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Cập nhật bản ghi.'),
            ('Nút %s' % ('Đóng' if modal else 'Quay lại'), 'Button', 'Enable', '–', '–',
             'Hiển thị', 'Hủy bỏ thay đổi, không ghi gì.'),
        ]
        d.ui_table(rows)

        d.p('%s.%d Danh sách event và xử lý event' % (pre, n + 3))
        during = ['– %s để trống → hiển thị “Bắt buộc phải nhập”.' % t[0]
                  for t in c['truong'] if t[4] == 'Có']
        during += c.get('loi_khac', [])
        if c.get('loi_trung'):
            during.append('– %s trùng với bản ghi khác → hiển thị “%s”. Giữ nguyên giá trị cũ '
                          'của chính nó thì KHÔNG báo trùng.'
                          % (c['truong_trung'], c['loi_trung']))
        during.append('– Nếu có lỗi kiểm tra → không thực hiện bước After.')
        d.event_table([
            ('Bấm nút Sửa', 'Click',
             'Before:\n– Kiểm tra quyền “%s”.\n'
             '– Nếu không có quyền%s → nút không hiển thị.\n'
             'After:\n– Mở form đã điền sẵn dữ liệu hiện tại của bản ghi.'
             % (self.qql, ' hoặc bản ghi đang Khóa' if c.get('co_trangthai') else '')),
            ('Bấm Lưu', 'Click',
             'Before:\n– Kiểm tra quyền “%s”.\n'
             '– Kiểm tra bản ghi có đang bị khóa không; nếu có → từ chối và báo bản ghi đang '
             'bị khóa.\n'
             'During:\n%s\n'
             'After:\n– Cập nhật bản ghi.\n'
             '– Ghi một dòng lịch sử cho từng trường đã đổi, kèm giá trị cũ và giá trị mới.\n'
             '– Nạp lại danh sách và hiển thị thông báo “%s”.'
             % (self.qql, '\n'.join(during), c.get('tb_sua', 'Cập nhật thành công'))),
            ('Thoát khi chưa lưu', 'Click',
             'After:\n– Hệ thống hỏi xác nhận rời khỏi; chọn ở lại thì giữ nguyên dữ liệu '
             'đang nhập.'),
        ])

    # ---------------------------------------------------------------- Xoa
    def _fn_delete(self, no, opts):
        d, c = self.d, self.c
        pre, _ = self._head(no, 'delete', opts)
        rel = [('include', 'Kiểm tra quyền “%s”' % self.qql),
               ('extend', 'Ẩn nút Xóa khi %s' % c['dieu_kien_an_xoa'])]
        n = self._uc(pre, 'delete', opts, rel)

        d.p('%s.%d Giới thiệu' % (pre, n))
        d.intro_table(
            self.label('delete', opts),
            'Xóa hẳn một %s khỏi danh mục. Chỉ %s mới hiện nút Xóa.'
            % (self.dt, c['dieu_kien_xoa']),
            self.P1,
            'Người dùng có quyền “%s” và %s.' % (self.qql, c['dieu_kien_xoa']),
            '1. Người dùng bấm nút Xóa trên dòng cần xóa.\n'
            '2. Hệ thống mở hộp thoại xác nhận, nêu rõ tên bản ghi sắp xóa.\n'
            '3. Người dùng bấm Xóa để xác nhận.\n'
            '4. Hệ thống xóa bản ghi, nạp lại danh sách và báo thành công.',
            '• Bản ghi đã được dùng ở nghiệp vụ khác → nút Xóa KHÔNG hiển thị.\n'
            '• Bấm Hủy → đóng hộp thoại, không xóa gì.\n'
            '• Bản ghi vừa bị người khác dùng ngay trước khi xác nhận → hệ thống từ chối xóa '
            'và báo lý do.')

        d.p('%s.%d Layout màn hình' % (pre, n + 1))
        d.layout(modal='Xác nhận xóa', shot=self.shot('xoa'),
                 shot_caption='Hộp thoại Xác nhận xóa')

        d.p('%s.%d Mô tả chi tiết giao diện' % (pre, n + 2))
        d.ui_table([
            ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', 'Nội dung cố định.'),
            ('Câu hỏi xác nhận', 'Label', 'Hiển thị', 'Theo dữ liệu',
             'Ghi rõ tên %s sắp xóa: “%s”.' % (self.dt, c['cauhoi_xoa'])),
            ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa (nút màu đỏ).'),
            ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa gì.'),
        ], required=False, scope=False)

        d.p('%s.%d Danh sách event và xử lý event' % (pre, n + 3))
        d.event_table([
            ('Bấm nút Xóa trên dòng', 'Click',
             'Before:\n– Kiểm tra quyền “%s” và điều kiện %s.\n'
             '– Không thỏa → nút KHÔNG hiển thị (không hiện nút xám).\n'
             'After:\n– Mở hộp thoại xác nhận kèm tên bản ghi.' % (self.qql, c['dieu_kien_xoa'])),
            ('Bấm Xóa trong hộp thoại', 'Click',
             'Before:\n– Kiểm tra lại quyền và điều kiện xóa ở phía máy chủ.\n'
             'During:\n– Bản ghi đã phát sinh dữ liệu liên quan → từ chối và báo lý do cụ thể.\n'
             '– Nếu bị từ chối → không thực hiện bước After.\n'
             'After:\n– Xóa bản ghi khỏi danh mục.\n'
             '– Nạp lại danh sách và hiển thị thông báo “%s”.'
             % c.get('tb_xoa', 'Xóa thành công')),
            ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp thoại, không xóa gì.'),
        ])

    # ---------------------------------------------------------------- Khoa / Mo khoa
    def _fn_lock(self, no, opts):
        d, c = self.d, self.c
        pre, _ = self._head(no, 'lock', opts)
        rel = [('include', 'Kiểm tra quyền “%s”' % self.qql),
               ('extend', 'Bản ghi đang Khóa thì nút đổi thành Mở khóa')]
        n = self._uc(pre, 'lock', opts, rel)

        d.p('%s.%d Giới thiệu' % (pre, n))
        d.intro_table(
            'Khóa / Mở khóa %s' % self.dt,
            'Chuyển %s sang trạng thái Khóa để ngừng cho chọn ở nghiệp vụ mới, hoặc mở lại. '
            'Khác với Xóa, dữ liệu vẫn còn nguyên và các chứng từ cũ không bị ảnh hưởng.'
            % self.dt,
            self.P1,
            'Người dùng có quyền “%s”.' % self.qql,
            '1. Người dùng bấm nút Khóa (hoặc Mở khóa) trên dòng tương ứng.\n'
            '2. Hệ thống mở hộp thoại xác nhận.\n'
            '3. Người dùng xác nhận.\n'
            '4. Hệ thống đổi trạng thái, nạp lại danh sách và báo thành công.',
            '• Bản ghi đang Khóa → nút Sửa bị ẩn, chỉ còn Mở khóa và các thao tác chỉ đọc.\n'
            '• Bấm Hủy → đóng hộp thoại, không đổi gì.')

        d.p('%s.%d Layout màn hình' % (pre, n + 1))
        d.layout(modal='Xác nhận khóa / mở khóa', shot=self.shot('khoa'),
                 shot_caption='Hộp thoại Xác nhận khóa')

        d.p('%s.%d Mô tả chi tiết giao diện' % (pre, n + 2))
        d.ui_table([
            ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Theo dữ liệu',
             '“Xác nhận khóa” hoặc “Xác nhận mở khóa” tùy trạng thái hiện tại.'),
            ('Câu hỏi xác nhận', 'Label', 'Hiển thị', 'Theo dữ liệu',
             'Ghi rõ tên %s: “%s”.' % (self.dt, c['cauhoi_khoa'])),
            ('Nút Khóa / Mở khóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện đổi trạng thái.'),
            ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không đổi gì.'),
        ], required=False, scope=False)

        d.p('%s.%d Danh sách event và xử lý event' % (pre, n + 3))
        d.event_table([
            ('Bấm nút Khóa / Mở khóa', 'Click',
             'Before:\n– Kiểm tra quyền “%s”.\n'
             '– Nếu không có quyền → nút không hiển thị.\n'
             'After:\n– Mở hộp thoại xác nhận đúng với trạng thái hiện tại.' % self.qql),
            ('Xác nhận trong hộp thoại', 'Click',
             'Before:\n– Kiểm tra lại quyền ở phía máy chủ.\n'
             'After:\n– Đổi trạng thái bản ghi giữa Hoạt động và Khóa.\n'
             '– Ghi một dòng lịch sử thuộc nhóm thay đổi trạng thái.\n'
             '– Nạp lại danh sách; dòng vừa đổi hiển thị badge trạng thái mới.'),
            ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp thoại, không đổi gì.'),
        ])

    # ---------------------------------------------------------------- Lich su
    def _fn_history(self, no, opts):
        d, c = self.d, self.c
        pre, _ = self._head(no, 'history', opts)
        d.p('%s.1 Giới thiệu' % pre)
        d.intro_table(
            'Xem lịch sử thay đổi',
            'Xem lại các lần bản ghi bị thay đổi: ai làm, lúc nào, trường nào đổi và giá trị '
            'trước / sau.',
            self._tacnhan(True),
            'Đang ở màn %s.' % self.ten,
            '1. Người dùng bấm nút Lịch sử trên dòng cần xem.\n'
            '2. Hệ thống mở cửa sổ lịch sử của đúng bản ghi đó.\n'
            '3. Các mốc thay đổi hiển thị theo thứ tự mới nhất lên trước.',
            '• Bản ghi chưa từng bị sửa → cửa sổ hiện “Chưa có lịch sử thao tác nào.”')
        d.p('%s.2 Layout màn hình' % pre)
        d.layout(modal='Lịch sử thay đổi', shot=self.shot('lichsu'),
                 shot_caption='Cửa sổ Lịch sử thay đổi')
        d.p('%s.3 Mô tả chi tiết giao diện' % pre)
        d.ui_table([
            ('Tiêu đề', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
             'Ghi rõ đang xem lịch sử của bản ghi nào.'),
            ('Mốc thời gian', 'Label', 'Hiển thị', 'dd/mm/yyyy', 'Theo dữ liệu',
             'Ngày giờ của lần thay đổi.'),
            ('Nhóm hành động', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
             'Ví dụ “Thay đổi thông tin”, “Thay đổi trạng thái”.'),
            ('Người thực hiện', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
             'Mã nhân viên, họ tên và bộ phận.'),
            ('Dòng thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
             'Mỗi dòng là một trường: tên trường, giá trị cũ (gạch đỏ) và giá trị mới.'),
            ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', 'Nạp lại lịch sử.'),
            ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
             'Hiện “Chưa có lịch sử thao tác nào.” khi chưa có bản ghi lịch sử.'),
            ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
        ], required=False)
        d.p('%s.4 Danh sách event và xử lý event' % pre)
        d.event_table([
            ('Bấm nút Lịch sử', 'Click',
             'After:\n– Mở cửa sổ và nạp lịch sử của đúng bản ghi, sắp mới nhất lên trước.'),
            ('Bấm Làm mới', 'Click', 'After:\n– Nạp lại danh sách lịch sử.'),
            ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ, không ảnh hưởng dữ liệu.'),
        ])

    # ---------------------------------------------------------------- Xuat Excel
    def _fn_export(self, no, opts):
        d, c = self.d, self.c
        pre, _ = self._head(no, 'export', opts)
        n = self._uc(pre, 'export', opts,
                     [('include', 'Chọn trường và thứ tự cột'),
                      ('extend', 'Áp đúng bộ lọc đang dùng trên danh sách')])
        d.p('%s.%d Giới thiệu' % (pre, n))
        d.intro_table(
            'Xuất Excel',
            'Kết xuất danh sách đang xem ra tệp Excel. Người dùng tự chọn những cột cần xuất '
            'và thứ tự cột trong tệp.',
            self._tacnhan(True),
            'Đang ở màn %s.' % self.ten,
            '1. Người dùng bấm nút Xuất Excel.\n'
            '2. Hệ thống mở cửa sổ chọn trường xuất, mặc định chọn hết.\n'
            '3. Người dùng chọn / bỏ chọn trường rồi bấm Xuất file.\n'
            '4. Hệ thống tạo tệp theo đúng bộ lọc đang áp dụng và tải về.',
            '• Không chọn trường nào → nút Xuất file không dùng được.\n'
            '• Danh sách rỗng → tệp chỉ có dòng tiêu đề.\n'
            '• Bấm Đóng → hủy, không tạo tệp.')
        d.p('%s.%d Layout màn hình' % (pre, n + 1))
        d.layout(modal='Chọn trường xuất file', shot=self.shot('xuat'),
                 shot_caption='Cửa sổ Chọn trường xuất file')
        d.p('%s.%d Mô tả chi tiết giao diện' % (pre, n + 2))
        d.ui_table([
            ('Câu hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
             'Nhắc thứ tự cột chạy theo đúng trình tự người dùng chọn.'),
            ('Ô chọn Trường xuất', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Chọn tất cả',
             'Chọn nhiều trường; mỗi trường hiện thành một thẻ có nút bỏ chọn.'),
            ('Dòng thứ tự cột', 'Label', 'Hiển thị', '–', '–', 'Theo lựa chọn',
             'Liệt kê thứ tự cột sẽ xuất ra tệp.'),
            ('Bộ đếm', 'Label', 'Hiển thị', '–', '–', 'Theo lựa chọn',
             'Ví dụ “Đang chọn 5/5 trường”.'),
            ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Chọn hết trường.'),
            ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ chọn hết.'),
            ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Enable',
             'Không dùng được khi chưa chọn trường nào.'),
            ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Hủy, không tạo tệp.'),
        ])
        d.p('%s.%d Danh sách event và xử lý event' % (pre, n + 3))
        d.event_table([
            ('Bấm nút Xuất Excel', 'Click',
             'After:\n– Mở cửa sổ chọn trường xuất với toàn bộ trường được chọn sẵn.'),
            ('Chọn / bỏ chọn trường', 'Change',
             'After:\n– Cập nhật dòng thứ tự cột và bộ đếm số trường đang chọn.'),
            ('Bấm Xuất file', 'Click',
             'Before:\n– Kiểm tra đã chọn ít nhất một trường.\n'
             'During:\n– Chưa chọn trường nào → nút không dùng được.\n'
             'After:\n– Tạo tệp Excel theo đúng bộ lọc đang áp dụng trên danh sách.\n'
             '– Tải tệp về máy người dùng.'),
        ])

    # ---------------------------------------------------------------- Import
    def _fn_import(self, no, opts):
        d, c = self.d, self.c
        pre, _ = self._head(no, 'import', opts)
        n = self._uc(pre, 'import', opts,
                     [('include', 'Kiểm tra quyền “%s”' % self.qql),
                      ('include', 'Kiểm tra dữ liệu từng dòng'),
                      ('extend', 'Khóa dòng hợp lệ sau khi kiểm tra')])
        d.p('%s.%d Giới thiệu' % (pre, n))
        d.intro_table(
            'Nhập dữ liệu từ Excel',
            'Thêm nhiều %s cùng lúc từ tệp Excel. Quy trình ba bước: nạp lên bảng xem trước, '
            'kiểm tra dữ liệu, rồi mới ghi vào danh mục.' % self.dt,
            self.P1,
            'Người dùng có quyền “%s”.' % self.qql,
            '1. Người dùng bấm Import Excel.\n'
            '2. Người dùng tải tệp mẫu, điền dữ liệu rồi chọn tệp.\n'
            '3. Bấm Load lên bảng để xem trước nội dung.\n'
            '4. Bấm Validate; hệ thống đánh dấu dòng lỗi và khóa dòng hợp lệ.\n'
            '5. Bấm Import để ghi các dòng hợp lệ vào danh mục.',
            '• Có dòng lỗi → hệ thống chỉ ghi các dòng hợp lệ, dòng lỗi giữ nguyên để sửa lại.\n'
            '• Bật “Chỉ dòng lỗi” → bảng chỉ hiện các dòng còn lỗi.\n'
            '• Bấm Làm mới → xóa trắng bảng để nhập lại từ đầu.',
            'Phải bấm Validate trước thì nút Import mới dùng được.')
        d.p('%s.%d Layout màn hình' % (pre, n + 1))
        d.layout(modal='Import %s' % self.dt, shot=self.shot('import'),
                 shot_caption='Cửa sổ Import từ Excel')
        d.p('%s.%d Mô tả chi tiết giao diện' % (pre, n + 2))
        d.ui_table([
            ('Nút Chọn file Excel', 'Button', 'Enable', '.xlsx', 'Có', 'Chưa chọn tệp',
             'Mở hộp thoại chọn tệp trên máy.'),
            ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị',
             'Tải tệp mẫu có sẵn tiêu đề cột đúng định dạng.'),
            ('Nút Load lên bảng', 'Button', 'Enable / Disable', '–', '–', 'Disable',
             'Đọc tệp và đổ nội dung lên bảng xem trước.'),
            ('Nút Validate', 'Button', 'Enable / Disable', '–', '–', 'Disable',
             'Kiểm tra từng dòng, đánh dấu lỗi và khóa dòng hợp lệ.'),
            ('Nút Import', 'Button', 'Enable / Disable', '–', '–', 'Disable',
             'Chỉ dùng được sau khi đã Validate.'),
            ('Ô tích Chỉ dòng lỗi', 'Icon Button', 'Enable', '–', 'Không', 'Không tích',
             'Lọc bảng chỉ hiện dòng còn lỗi.'),
            ('Bảng xem trước', 'Table/Grid', 'Enable', '–', '–', 'Trống',
             'Mỗi dòng là một bản ghi sắp thêm; dòng lỗi được tô khác màu kèm mô tả lỗi.'),
            ('Bộ đếm Tổng', 'Label', 'Hiển thị', '–', '–', '0', 'Tổng số dòng đang có trên bảng.'),
            ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa trắng bảng.'),
            ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ.'),
        ])
        d.p('%s.%d Danh sách event và xử lý event' % (pre, n + 3))
        d.event_table([
            ('Bấm Tải file mẫu', 'Click', 'After:\n– Tải về tệp mẫu đúng định dạng cột.'),
            ('Bấm Load lên bảng', 'Click',
             'During:\n– Tệp sai định dạng cột → báo lỗi và không đổ dữ liệu.\n'
             'After:\n– Đổ toàn bộ dòng của tệp lên bảng xem trước.'),
            ('Bấm Validate', 'Click',
             'Before:\n– Kiểm tra quyền “%s”.\n'
             'During:\n%s\n'
             'After:\n– Đánh dấu dòng lỗi kèm mô tả, khóa các dòng hợp lệ.\n'
             '– Bật nút Import.' % (self.qql, '\n'.join(c.get('loi_import', [
                 '– Dòng thiếu trường bắt buộc → đánh dấu lỗi.',
                 '– Dòng trùng dữ liệu đã có → đánh dấu lỗi.'])))),
            ('Bấm Import', 'Click',
             'Before:\n– Kiểm tra quyền “%s” và bắt buộc đã Validate.\n'
             'After:\n– Ghi các dòng hợp lệ vào danh mục.\n'
             '– Báo số dòng thêm thành công và số dòng bị bỏ qua.\n'
             '– Nạp lại danh sách phía sau.' % self.qql),
        ])

    # ---------------------------------------------------------------- In danh sach
    def _fn_print(self, no, opts):
        d = self.d
        pre, _ = self._head(no, 'print', opts)
        n = self._uc(pre, 'print', opts,
                     [('extend', 'Áp đúng bộ lọc và bộ cột đang hiển thị')])
        d.p('%s.%d Giới thiệu' % (pre, n))
        d.intro_table(
            'In danh sách',
            'Mở bản in của danh sách đang xem trên một thẻ trình duyệt mới, đã dàn trang sẵn '
            'để gửi máy in hoặc lưu thành PDF.',
            self._tacnhan(True),
            'Đang ở màn %s.' % self.ten,
            '1. Người dùng bấm nút In danh sách.\n'
            '2. Hệ thống mở thẻ mới chứa bản in.\n'
            '3. Người dùng dùng chức năng in của trình duyệt.',
            '• Bản in lấy đúng bộ lọc và bộ cột đang hiển thị trên danh sách.\n'
            '• Danh sách rỗng → bản in chỉ có tiêu đề và bảng trống.')
        d.p('%s.%d Layout màn hình' % (pre, n + 1))
        d.layout(route=opts.get('route'), shot=self.shot('in'),
                 shot_caption='Bản in danh sách')
        d.p('%s.%d Mô tả chi tiết giao diện' % (pre, n + 2))
        d.ui_table([
            ('Tiêu đề bản in', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
             'Tên danh mục kèm ngày in.'),
            ('Bảng dữ liệu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
             'Đúng bộ cột đang hiển thị trên màn danh sách.'),
            ('Khối ký', 'Label', 'Hiển thị', '–', 'Theo mẫu',
             'Phần chữ ký cuối trang theo mẫu in của công ty.'),
        ], required=False)
        d.p('%s.%d Danh sách event và xử lý event' % (pre, n + 3))
        d.event_table([
            ('Bấm In danh sách', 'Click',
             'Before:\n– Thu thập bộ lọc và bộ cột đang áp dụng.\n'
             'After:\n– Mở thẻ trình duyệt mới hiển thị bản in đã dàn trang.'),
        ])

    # ---------------------------------------------------------------- Luu cau hinh
    def _fn_save(self, no, opts):
        d, c = self.d, self.c
        pre, _ = self._head(no, 'save', opts)
        n = self._uc(pre, 'save', opts,
                     [('include', 'Kiểm tra quyền “%s”' % self.qql),
                      ('include', 'Xác nhận trước khi ghi đè hàng loạt')])
        d.p('%s.%d Giới thiệu' % (pre, n))
        d.intro_table(
            'Lưu cấu hình giá dịch vụ',
            'Ghi lại hệ số giá bán và định mức đàm phán, đồng thời áp giá trị mới cho TOÀN BỘ '
            'gói bảo dưỡng đang có, ghi đè cả những gói đã được chỉnh riêng.',
            self.P1,
            'Người dùng có quyền “%s”.' % self.qql,
            '1. Người dùng sửa Hệ số giá bán dịch vụ và / hoặc Định mức đàm phán giá.\n'
            '2. Người dùng bấm Lưu.\n'
            '3. Hệ thống mở hộp thoại xác nhận, nêu rõ số gói bảo dưỡng và số cấp dịch vụ bị '
            'ảnh hưởng.\n'
            '4. Người dùng bấm Xác nhận.\n'
            '5. Hệ thống ghi cấu hình, áp lại cho toàn bộ gói và báo kết quả.',
            '• Bấm Hủy ở hộp thoại → không ghi gì, giá trị đang nhập vẫn giữ nguyên.\n'
            '• Gói không xác định được đơn giá công của công ty → hệ thống bỏ qua gói đó và '
            'báo lại số gói bị bỏ qua.\n'
            '• Giá gốc của cấp dịch vụ chỉ được tính lại khi hệ số thực sự thay đổi.',
            'Đây là thao tác ghi đè hàng loạt, không có chức năng hoàn tác.')
        d.p('%s.%d Layout màn hình' % (pre, n + 1))
        d.layout(modal='Xác nhận cập nhật giá dịch vụ', shot=self.shot('xacnhan'),
                 shot_caption='Hộp thoại Xác nhận cập nhật giá dịch vụ')
        d.p('%s.%d Mô tả chi tiết giao diện' % (pre, n + 2))
        d.ui_table([
            ('Câu cảnh báo phạm vi', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu',
             'Nêu rõ số gói bảo dưỡng sẽ bị ghi đè.'),
            ('Câu cảnh báo tính lại', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu',
             'Nêu số cấp dịch vụ sẽ được tính lại giá gốc nếu hệ số đổi.'),
            ('Nút Xác nhận', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thực hiện ghi đè.'),
            ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không ghi gì.'),
        ])
        d.p('%s.%d Danh sách event và xử lý event' % (pre, n + 3))
        during = ['– %s để trống → hiển thị “Bắt buộc phải nhập”.' % t[0]
                  for t in c['truong'] if t[4] == 'Có']
        during += c.get('loi_khac', [])
        during.append('– Nếu có lỗi kiểm tra → không thực hiện bước After.')
        d.event_table([
            ('Bấm Lưu', 'Click',
             'Before:\n– Kiểm tra quyền “%s”.\n'
             'During:\n%s\n'
             'After:\n– Mở hộp thoại xác nhận kèm số gói và số cấp dịch vụ bị ảnh hưởng.'
             % (self.qql, '\n'.join(during))),
            ('Bấm Xác nhận', 'Click',
             'Before:\n– Kiểm tra lại quyền ở phía máy chủ.\n'
             'After:\n– Ghi hệ số và định mức vào cấu hình chung.\n'
             '– Áp hệ số và định mức mới cho toàn bộ gói bảo dưỡng.\n'
             '– Tính lại giá gốc của các cấp dịch vụ nếu hệ số thay đổi.\n'
             '– Hiển thị thông báo thành công kèm số gói đã cập nhật và số gói bị bỏ qua.'),
            ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp thoại, không ghi gì.'),
        ])

    # ================================================================ PHAN 4
    def _phan4(self):
        d, c = self.d, self.c
        d.h1('Phần 4. Quy tắc nghiệp vụ')
        for i, (ten, dong) in enumerate(c['quy_tac']):
            d.p('BR-%02d — %s' % (i + 1, ten))
            d.bullets(dong)

    # ---------------------------------------------------------------- phu tro
    def _tacnhan(self, gom_xem):
        if self.qxem and gom_xem:
            return '%s; %s; Người dùng đã đăng nhập' % (self.P1, self.P2)
        return '%s; Người dùng đã đăng nhập' % self.P1

    def _ten_quyen_xem(self):
        if self.qxem:
            return '%s” hoặc “%s' % (self.qql, self.qxem)
        return self.qql
