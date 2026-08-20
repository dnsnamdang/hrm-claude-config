# -*- coding: utf-8 -*-
"""Bo sinh TESTCASE dung chung cho cac man DANH MUC.

Dung chung dict cau hinh voi catalog_srs.py: tu `funcs` sinh ra cac section La Ma tuong ung,
tu `truong` sinh ca kiem tra bat buoc / trung / gioi han cua tung o nhap.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
         'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI']


class CatalogTc(object):
    def __init__(self, cfg, out_dir):
        self.c = cfg
        self.out_dir = out_dir
        self.ten = cfg['ten']
        self.dt = cfg['doi_tuong']
        self.qql = cfg['quyen_quan_ly']
        self.qxem = cfg.get('quyen_xem')
        self.funcs = [f if isinstance(f, tuple) else (f, {}) for f in cfg['funcs']]
        self.names = [f[0] for f in self.funcs]
        self.bat_buoc = [t for t in cfg['truong'] if t[4] == 'Có']

    def has(self, n):
        return n in self.names

    # ================================================================ khoi mo ta 9 muc
    def desc_block(self):
        c = self.c
        if c.get('co_trangthai'):
            m2 = ('- Toàn bộ %s trong danh mục, gồm CẢ bản ghi Hoạt động lẫn bản ghi đã Khóa.\n'
                  '- Bộ lọc Trạng thái để trống thì hiện cả hai nhóm.' % self.dt)
            m3 = ('- Không ẩn bản ghi nào theo mặc định.\n'
                  '- Bản ghi Khóa KHÔNG còn chọn được ở nghiệp vụ mới, nhưng vẫn nằm trong '
                  'danh mục này và các chứng từ cũ vẫn hiện đúng tên.')
        else:
            m2 = '- Toàn bộ %s còn trong danh mục. Màn hình KHÔNG có cột Trạng thái.' % self.dt
            m3 = ('- Bản ghi đã bị Xóa không còn xuất hiện. Màn này không có trạng thái Khóa '
                  'nên không có nhóm nào bị ẩn tạm.')

        quyen_txt = ('Màn hình dùng HAI quyền tách rời:\n'
                     '- "%s": làm được mọi thao tác ghi.\n'
                     '- "%s": chỉ tra cứu, xuất Excel và xem lịch sử.\n'
                     'Người chỉ có quyền xem vẫn VÀO ĐƯỢC màn hình nhưng không thấy các nút ghi.'
                     % (self.qql, self.qxem)) if self.qxem else (
            'Màn hình dùng đúng MỘT quyền: "%s".\n'
            'Không có quyền này thì không vào được màn hình, chứ không phải vào được mà nút '
            'bị mờ.' % self.qql)

        return [
            ('1. Mục đích tính năng', c['tc_mucdich']),
            ('2. Đối tượng được tính / hiển thị', m2),
            ('3. Đối tượng bị ẩn / không tính', m3),
            ('4. Bộ lọc thời gian áp dụng cho', c.get('tc_thoigian',
             'Màn hình KHÔNG có bộ lọc khoảng thời gian. Yếu tố thời gian chỉ xuất hiện ở cột '
             'Ngày tạo, cột Ngày cập nhật và cửa sổ Lịch sử thay đổi.')),
            ('5. Cấu trúc dữ liệu / cây phân cấp', c['tc_caudata']),
            ('6. Quy tắc cộng dồn / deduplicate', c['tc_dedupe']),
            ('7. Phân quyền cấp', quyen_txt),
            ('8. Nguồn dữ liệu', c['tc_nguon']),
            ('9. Lưu ý khi kiểm thử', '\n'.join(c['tc_luuy'])),
        ]

    # ================================================================ phan quyen
    def role_tcs(self):
        r = []
        n = 1

        def add(func, prio, pre, steps, td, exp):
            nonlocal n
            r.append(('%02d' % n, func, prio, pre, steps, td, exp))
            n += 1

        add('Có quyền quản lý thì vào được và thấy đủ nút ghi', 'P0',
            'Đăng nhập bằng tài khoản CÓ quyền "%s"' % self.qql,
            '1. Mở menu của phân hệ\n2. Bấm vào mục %s' % self.ten,
            'Tài khoản có quyền quản lý',
            'Mục menu hiển thị. Vào được màn hình. Thấy nút Tạo mới trên thanh công cụ và '
            'thấy nút Sửa ở cột Hành động.')
        if self.qxem:
            add('Chỉ có quyền xem thì vào được nhưng KHÔNG thấy nút ghi', 'P0',
                'Đăng nhập bằng tài khoản CHỈ có quyền "%s"' % self.qxem,
                '1. Mở màn hình %s\n2. Quan sát thanh công cụ và cột Hành động' % self.ten,
                'Tài khoản chỉ có quyền xem',
                'Vào được màn hình và tra cứu bình thường. KHÔNG thấy nút Tạo mới, Sửa, Xóa'
                + (', Khóa' if self.has('lock') else '')
                + (', Import' if self.has('import') else '')
                + '. Vẫn thấy nút Xuất Excel và nút Lịch sử.')
            add('Chỉ có quyền xem thì vẫn xem được lịch sử', 'P1',
                'Đăng nhập bằng tài khoản CHỈ có quyền "%s"' % self.qxem,
                '1. Mở màn hình\n2. Bấm nút Lịch sử trên một dòng bất kỳ',
                'Tài khoản chỉ có quyền xem',
                'Cửa sổ Lịch sử mở bình thường, hiển thị đầy đủ các mốc thay đổi.')
        add('Không có quyền nào thì không thấy mục menu', 'P0',
            'Đăng nhập bằng tài khoản KHÔNG có quyền nào của màn này',
            '1. Mở menu của phân hệ\n2. Tìm mục %s' % self.ten,
            'Tài khoản không có quyền',
            'Mục menu KHÔNG hiển thị trong danh sách chức năng.')
        add('Không có quyền mà vào thẳng đường dẫn thì bị chặn', 'P0',
            'Đăng nhập bằng tài khoản KHÔNG có quyền nào của màn này',
            '1. Dán đường dẫn %s vào thanh địa chỉ\n2. Nhấn Enter' % (
                self.c['host'] + self.c['route']),
            'Đường dẫn đầy đủ của màn hình',
            'Hệ thống chặn truy cập và chuyển sang trang báo không có quyền. KHÔNG hiển thị '
            'dữ liệu danh mục.')
        if self.has('create'):
            add('Mất quyền giữa chừng thì thao tác ghi vẫn bị chặn', 'P1',
                'Đang mở form Tạo mới; quản trị viên thu hồi quyền quản lý của tài khoản',
                '1. Mở form Tạo mới\n2. Nhờ quản trị viên thu hồi quyền\n'
                '3. Nhập dữ liệu hợp lệ rồi bấm Lưu',
                'Dữ liệu hợp lệ',
                'Hệ thống từ chối lưu và báo không có quyền thực hiện chức năng này. '
                'Bản ghi KHÔNG được tạo.')
        return r

    # ================================================================ tung section
    def sections(self):
        """Tra ve danh sach section da danh so La Ma.

        Engine dung chung (`tc_engine.ROMAN`) chi ho tro TOI DA 10 muc. Man nao co nhieu chuc
        nang hon (vd Danh muc tai khoan) thi GOP nhom cuoi — ket xuat, in an, tuy chinh hien
        thi va trai nghiem — vao chung mot muc, thay vi sua engine dung chung.
        """
        raw = []

        def sec(title, tcs):
            raw.append((title, tcs))

        sec('Xem danh sách', self._sec_list())
        if self.has('filter'):
            sec('Tìm kiếm và lọc', self._sec_filter())
        if self.has('view'):
            sec('Xem chi tiết', self._sec_view())
        if self.has('create'):
            sec('Thêm mới', self._sec_create())
        if self.has('edit'):
            sec('Chỉnh sửa', self._sec_edit())
        if self.has('delete'):
            sec('Xóa', self._sec_delete())
        if self.has('lock'):
            sec('Khóa / Mở khóa', self._sec_lock())
        if self.has('save'):
            sec('Lưu cấu hình', self._sec_save())
        if self.has('history'):
            sec('Lịch sử thay đổi', self._sec_history())
        if self.has('import'):
            sec('Nhập dữ liệu từ Excel', self._sec_import())
        if self.has('export'):
            sec('Xuất Excel', self._sec_export())
        if self.has('print'):
            sec('In danh sách', self._sec_print())
        if self.has('columns') or self.has('fcfg'):
            sec('Tùy chỉnh hiển thị', self._sec_display())
        sec('Giao diện và trải nghiệm', self._sec_ux())

        # Gop nhom cuoi neu vuot qua 10 muc (gioi han cua engine dung chung).
        if len(raw) > len(ROMAN[:10]):
            giu = 9
            gop = raw[giu:]
            tcs = []
            for _, ds in gop:
                tcs.extend(t[1:] for t in ds)
            raw = raw[:giu] + [('Kết xuất, in ấn và tùy chỉnh hiển thị', self._mk(tcs))]

        return [(ROMAN[i], t, tcs) for i, (t, tcs) in enumerate(raw)]

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _mk(tcs):
        return [(i + 1,) + t for i, t in enumerate(tcs)]

    def _sec_list(self):
        t = [
            ('Mở màn hình lần đầu hiển thị đúng dữ liệu', 'P0',
             'Đã đăng nhập và có quyền vào màn hình',
             '1. Mở màn %s\n2. Quan sát bảng dữ liệu' % self.ten,
             'Không nhập gì',
             'Bảng hiển thị trang đầu tiên. Góc trái dưới bảng ghi rõ đang hiển thị bao nhiêu '
             'dòng trên tổng số bao nhiêu bản ghi.'),
            ('Hiển thị đủ các cột mặc định', 'P0',
             'Đang ở màn danh sách, chưa từng đổi cấu hình cột',
             '1. Quan sát tiêu đề bảng',
             'Không nhập gì',
             'Bảng hiện đúng bộ cột mặc định của màn hình, trong đó luôn có STT, cột tên và '
             'cột Hành động.'),
            ('Sắp xếp tăng dần theo cột cho phép', 'P1',
             'Danh sách có ít nhất 3 bản ghi',
             '1. Bấm vào tiêu đề một cột có biểu tượng sắp xếp',
             'Không nhập gì',
             'Danh sách sắp lại theo chiều tăng dần và quay về trang 1.'),
            ('Sắp xếp giảm dần khi bấm lần thứ hai', 'P1',
             'Vừa sắp xếp tăng dần ở bước trước',
             '1. Bấm lại vào chính tiêu đề cột đó',
             'Không nhập gì',
             'Danh sách đảo sang chiều giảm dần. Biểu tượng trên tiêu đề đổi chiều theo.'),
            ('Chuyển trang giữ nguyên số thứ tự liên tục', 'P0',
             'Danh sách có nhiều hơn một trang',
             '1. Ghi lại số thứ tự cuối cùng của trang 1\n2. Bấm sang trang 2',
             'Không nhập gì',
             'Số thứ tự của trang 2 chạy tiếp theo trang 1, KHÔNG quay về 1.'),
            ('Chuyển trang giữ nguyên bộ lọc đang áp dụng', 'P0',
             'Đã lọc ra kết quả có nhiều hơn một trang',
             '1. Áp một tiêu chí lọc\n2. Bấm sang trang 2\n3. Quan sát dữ liệu',
             'Một tiêu chí lọc bất kỳ',
             'Trang 2 vẫn chỉ chứa bản ghi khớp tiêu chí lọc. Tiêu chí trên khu vực lọc vẫn còn.'),
            ('Đổi số dòng mỗi trang', 'P1',
             'Danh sách có nhiều hơn 20 bản ghi',
             '1. Chọn 20 ở ô số dòng mỗi trang',
             '20 dòng mỗi trang',
             'Bảng hiển thị tối đa 20 dòng và quay về trang 1.'),
            ('Danh sách rỗng hiển thị đúng thông báo', 'P1',
             'Đang ở màn danh sách',
             '1. Nhập một từ khóa chắc chắn không khớp bản ghi nào\n2. Bấm Tìm kiếm',
             'Từ khóa: zzzkhongtontai',
             'Bảng hiện thông báo không có dữ liệu phù hợp bộ lọc, KHÔNG để trống trơn và '
             'không báo lỗi.'),
        ]
        if self.c.get('co_trangthai'):
            t.append(('Bản ghi đã Khóa vẫn hiển thị trong danh sách', 'P0',
                      'Danh mục có ít nhất một bản ghi đang Khóa',
                      '1. Để trống bộ lọc Trạng thái\n2. Quan sát danh sách',
                      'Không lọc trạng thái',
                      'Bản ghi đang Khóa VẪN hiện trong danh sách, kèm badge Khóa ở cột '
                      'Trạng thái.'))
        return self._mk(t)

    def _sec_filter(self):
        c = self.c
        t = [
            ('Tìm nhanh khớp một phần từ khóa', 'P0',
             'Danh sách có bản ghi chứa từ khóa cần tìm',
             '1. Nhập một phần tên bản ghi vào ô tìm nhanh\n2. Bấm Tìm kiếm',
             'Một phần tên có thật',
             'Danh sách chỉ còn bản ghi có chứa đoạn từ khóa đã nhập.'),
            ('Tìm nhanh không phân biệt chữ hoa chữ thường', 'P1',
             'Danh sách có bản ghi cần tìm',
             '1. Nhập từ khóa TOÀN CHỮ HOA\n2. Bấm Tìm kiếm\n'
             '3. Nhập lại từ khóa đó toàn chữ thường\n4. Bấm Tìm kiếm',
             'Cùng một từ khóa, hai kiểu chữ',
             'Hai lần tìm cho ra cùng một kết quả.'),
            ('Nhấn Enter chạy tìm kiếm như bấm nút', 'P1',
             'Đang ở màn danh sách',
             '1. Gõ từ khóa vào ô tìm nhanh\n2. Nhấn phím Enter',
             'Từ khóa có thật',
             'Danh sách lọc lại y như khi bấm nút Tìm kiếm.'),
            ('Nút Làm mới xóa tiêu chí VÀ nạp lại danh sách ngay', 'P0',
             'Đang có kết quả đã lọc',
             '1. Bấm nút Làm mới\n2. Quan sát khu vực lọc và bảng dữ liệu',
             'Không nhập gì',
             'Mọi ô lọc trắng trơn VÀ bảng nạp lại toàn bộ danh sách ngay lập tức, không phải '
             'bấm thêm Tìm kiếm.'),
            ('Tìm từ khóa không khớp bản ghi nào', 'P1',
             'Đang ở màn danh sách',
             '1. Nhập từ khóa vô nghĩa\n2. Bấm Tìm kiếm',
             'Từ khóa: qqqxxxzzz',
             'Bảng rỗng kèm thông báo không có dữ liệu phù hợp bộ lọc.'),
            ('Từ khóa có khoảng trắng thừa vẫn tìm đúng', 'P2',
             'Danh sách có bản ghi cần tìm',
             '1. Nhập từ khóa kèm khoảng trắng ở đầu và cuối\n2. Bấm Tìm kiếm',
             'Từ khóa có khoảng trắng thừa hai đầu',
             'Kết quả giống như khi nhập từ khóa không có khoảng trắng thừa.'),
        ]
        for f in c['loc'][1:]:
            t.append(('Lọc theo %s' % f[0], 'P1',
                      'Danh sách có bản ghi thuộc giá trị cần lọc',
                      '1. Chọn một giá trị ở ô %s\n2. Bấm Tìm kiếm' % f[0],
                      'Một giá trị có thật của %s' % f[0],
                      'Danh sách chỉ còn bản ghi khớp giá trị đã chọn ở ô %s.' % f[0]))
        if len(c['loc']) > 1:
            t.append(('Kết hợp nhiều tiêu chí cùng lúc', 'P0',
                      'Danh sách có bản ghi thỏa đồng thời hai tiêu chí',
                      '1. Nhập từ khóa vào ô tìm nhanh\n2. Chọn thêm một tiêu chí lọc\n'
                      '3. Bấm Tìm kiếm',
                      'Một từ khóa và một tiêu chí lọc',
                      'Danh sách chỉ còn bản ghi thỏa ĐỒNG THỜI cả hai tiêu chí, không phải '
                      'thỏa một trong hai.'))
        else:
            t.append(('Màn hình không có bộ lọc nâng cao', 'P2',
                      'Đang ở màn danh sách',
                      '1. Quan sát khu vực lọc phía trên bảng',
                      'Không nhập gì',
                      'Chỉ có ô tìm nhanh, nút Tìm kiếm và nút Làm mới. KHÔNG có nút mở bộ lọc '
                      'nâng cao — đây là thiết kế đúng của màn này.'))
        return self._mk(t)

    def _sec_view(self):
        opts = dict(self.funcs[self.names.index('view')][1])
        modal = opts.get('modal', True)
        cot = opts.get('cot_bam', 'tên')
        t = [
            ('Mở xem chi tiết từ danh sách', 'P0',
             'Danh sách có ít nhất một bản ghi',
             '1. Bấm vào %s ở dòng đầu tiên' % cot,
             'Không nhập gì',
             '%s mở ra và hiển thị đúng dữ liệu của dòng vừa bấm.'
             % ('Cửa sổ xem' if modal else 'Màn hình chi tiết')),
            ('Mọi ô ở chế độ chỉ đọc', 'P0',
             'Đang mở màn xem chi tiết',
             '1. Bấm vào từng ô dữ liệu và thử gõ',
             'Gõ thử ký tự bất kỳ',
             'Không ô nào cho nhập. Không có nút Lưu trên màn xem.'),
            ('Dữ liệu hiển thị khớp với dòng trên danh sách', 'P0',
             'Đã ghi lại giá trị các cột của một dòng',
             '1. Bấm mở xem chi tiết dòng đó\n2. Đối chiếu từng trường',
             'Không nhập gì',
             'Mọi trường trùng khớp với giá trị hiển thị ở danh sách.'),
            ('Đóng màn xem không làm thay đổi dữ liệu', 'P1',
             'Đang mở màn xem chi tiết',
             '1. Bấm %s\n2. Quan sát danh sách'
             % ('nút Đóng' if modal else 'nút Quay lại'),
             'Không nhập gì',
             'Trở về danh sách, dữ liệu giữ nguyên như trước khi mở.'),
        ]
        return self._mk(t)

    def _sec_create(self):
        c = self.c
        opts = dict(self.funcs[self.names.index('create')][1])
        modal = opts.get('modal', True)
        noi = 'Cửa sổ' if modal else 'Màn hình'
        t = [
            ('Thêm mới với dữ liệu hợp lệ', 'P0',
             'Có quyền quản lý và đang ở màn danh sách',
             '1. Bấm nút Tạo mới\n2. Nhập đủ các ô bắt buộc bằng giá trị hợp lệ\n3. Bấm Lưu',
             'Dữ liệu hợp lệ, chưa từng tồn tại',
             'Bản ghi được thêm. %s đóng lại, danh sách nạp lại và có bản ghi vừa thêm. '
             'Hiện thông báo thành công.' % noi),
            ('Form mở ra ở trạng thái trắng', 'P1',
             'Có quyền quản lý',
             '1. Bấm nút Tạo mới\n2. Quan sát các ô nhập',
             'Không nhập gì',
             'Mọi ô nhập đều trống%s. Không mang dữ liệu của bản ghi nào.'
             % (', riêng ô Trạng thái đặt sẵn là Hoạt động' if c.get('co_trangthai') else '')),
        ]
        for f in self.bat_buoc:
            t.append(('Bỏ trống ô bắt buộc %s' % f[0], 'P0',
                      'Đang mở form Tạo mới',
                      '1. Để trống ô %s\n2. Nhập các ô bắt buộc còn lại\n3. Bấm Lưu' % f[0],
                      'Ô %s để trống' % f[0],
                      'Hệ thống báo "Bắt buộc phải nhập" bằng chữ đỏ ngay dưới ô %s. '
                      '%s KHÔNG đóng và bản ghi KHÔNG được tạo.' % (f[0], noi)))
        if c.get('loi_trung'):
            t.append(('Trùng %s với bản ghi đã có' % c['truong_trung'], 'P0',
                      'Danh mục đã có một bản ghi để lấy giá trị đem đi trùng',
                      '1. Bấm Tạo mới\n2. Nhập %s giống hệt bản ghi đã có\n'
                      '3. Nhập các ô còn lại hợp lệ\n4. Bấm Lưu' % c['truong_trung'],
                      '%s đã tồn tại' % c['truong_trung'],
                      'Hệ thống báo "%s" ngay dưới ô tương ứng. Bản ghi KHÔNG được tạo.'
                      % c['loi_trung']))
            t.append(('Trùng %s nhưng khác kiểu chữ hoa thường' % c['truong_trung'], 'P1',
                      'Danh mục đã có một bản ghi để đối chiếu',
                      '1. Bấm Tạo mới\n2. Nhập %s giống bản ghi cũ nhưng đổi kiểu chữ\n'
                      '3. Bấm Lưu' % c['truong_trung'],
                      'Giá trị cũ viết khác kiểu chữ',
                      'Vẫn bị chặn với thông báo "%s" — hệ thống coi hai cách viết là trùng nhau.'
                      % c['loi_trung']))
            t.append(('Trùng %s nhưng có khoảng trắng thừa' % c['truong_trung'], 'P1',
                      'Danh mục đã có một bản ghi để đối chiếu',
                      '1. Bấm Tạo mới\n2. Nhập %s giống bản ghi cũ, thêm khoảng trắng ở đầu '
                      'và cuối\n3. Bấm Lưu' % c['truong_trung'],
                      'Giá trị cũ kèm khoảng trắng thừa',
                      'Vẫn bị chặn với thông báo "%s" — khoảng trắng thừa được cắt bỏ trước '
                      'khi so trùng.' % c['loi_trung']))
        for extra in c.get('tc_create_them', []):
            t.append(extra)
        t += [
            ('Nút Lưu và tiếp tục giữ form mở', 'P1',
             'Đang mở form Tạo mới',
             '1. Nhập đủ dữ liệu hợp lệ\n2. Bấm Lưu và tiếp tục',
             'Dữ liệu hợp lệ',
             'Bản ghi được thêm, form VẪN mở và các ô được làm trắng để nhập bản ghi tiếp theo.'),
            ('Đóng form không lưu thì không tạo bản ghi', 'P0',
             'Đang mở form Tạo mới và đã nhập dữ liệu',
             '1. Nhập dữ liệu hợp lệ\n2. Bấm %s' % ('Đóng' if modal else 'Quay lại'),
             'Dữ liệu hợp lệ',
             'Không có bản ghi nào được thêm vào danh sách.'),
            ('Bản ghi mới hiển thị đúng người tạo và ngày tạo', 'P1',
             'Vừa thêm mới thành công một bản ghi',
             '1. Tìm bản ghi vừa thêm trên danh sách\n2. Xem cột Người tạo và Ngày tạo',
             'Không nhập gì',
             'Cột Người tạo hiện đúng họ tên người đang đăng nhập, Ngày tạo là thời điểm vừa lưu.'),
        ]
        return self._mk(t)

    def _sec_edit(self):
        c = self.c
        t = [
            ('Sửa với dữ liệu hợp lệ', 'P0',
             'Có quyền quản lý và danh sách có bản ghi sửa được',
             '1. Bấm nút Sửa trên một dòng\n2. Đổi giá trị một ô\n3. Bấm Lưu',
             'Giá trị mới hợp lệ',
             'Bản ghi được cập nhật. Danh sách nạp lại và hiện giá trị mới. Có thông báo '
             'thành công.'),
            ('Form sửa điền sẵn dữ liệu hiện tại', 'P0',
             'Danh sách có bản ghi sửa được',
             '1. Ghi lại giá trị các cột của một dòng\n2. Bấm nút Sửa trên dòng đó\n'
             '3. Đối chiếu từng ô',
             'Không nhập gì',
             'Mọi ô đã điền sẵn đúng giá trị hiện tại của bản ghi, không có ô nào trống nhầm.'),
        ]
        if c.get('loi_trung'):
            t.append(('Giữ nguyên %s của chính nó thì lưu bình thường' % c['truong_trung'], 'P0',
                      'Đang mở form Sửa một bản ghi',
                      '1. KHÔNG đổi ô %s\n2. Đổi một ô khác\n3. Bấm Lưu' % c['truong_trung'],
                      'Giữ nguyên giá trị cũ của chính bản ghi',
                      'Lưu thành công, KHÔNG báo trùng — bản ghi đang sửa được loại khỏi phép '
                      'so trùng.'),)
            t.append(('Đổi %s thành giá trị của bản ghi khác' % c['truong_trung'], 'P0',
                      'Danh mục có ít nhất hai bản ghi',
                      '1. Mở form Sửa bản ghi A\n2. Đổi %s thành giá trị của bản ghi B\n'
                      '3. Bấm Lưu' % c['truong_trung'],
                      'Giá trị đang thuộc về bản ghi khác',
                      'Hệ thống báo "%s". Bản ghi KHÔNG được cập nhật.' % c['loi_trung']))
        for f in self.bat_buoc:
            t.append(('Xóa trắng ô bắt buộc %s rồi lưu' % f[0], 'P0',
                      'Đang mở form Sửa',
                      '1. Xóa trắng ô %s\n2. Bấm Lưu' % f[0],
                      'Ô %s để trống' % f[0],
                      'Hệ thống báo "Bắt buộc phải nhập" ngay dưới ô %s. Bản ghi KHÔNG được '
                      'cập nhật.' % f[0]))
        for extra in c.get('tc_edit_them', []):
            t.append(extra)
        if c.get('co_trangthai'):
            t.append(('Bản ghi đang Khóa thì không có nút Sửa', 'P0',
                      'Danh mục có bản ghi đang ở trạng thái Khóa',
                      '1. Tìm dòng có badge Khóa\n2. Quan sát cột Hành động',
                      'Không nhập gì',
                      'Nút Sửa KHÔNG hiển thị trên dòng đó. Muốn sửa phải Mở khóa trước.'))
        t += [
            ('Thoát khi chưa lưu có cảnh báo', 'P1',
             'Đang mở form Sửa và vừa đổi dữ liệu',
             '1. Đổi giá trị một ô\n2. Bấm thoát mà không lưu',
             'Giá trị mới bất kỳ',
             'Hệ thống hỏi xác nhận rời khỏi. Chọn ở lại thì dữ liệu đang nhập vẫn còn nguyên.'),
            ('Bản ghi vừa sửa hiển thị đúng người và ngày cập nhật', 'P1',
             'Vừa sửa thành công một bản ghi',
             '1. Bật cột Người cập nhật và Ngày cập nhật\n2. Xem dòng vừa sửa',
             'Không nhập gì',
             'Cột Người cập nhật hiện đúng họ tên người đang đăng nhập, Ngày cập nhật là thời '
             'điểm vừa lưu.'),
        ]
        return self._mk(t)

    def _sec_delete(self):
        c = self.c
        t = [
            ('Xóa bản ghi chưa dùng ở đâu', 'P0',
             'Danh mục có bản ghi %s' % c['dieu_kien_xoa'],
             '1. Bấm nút Xóa trên dòng đó\n2. Bấm Xóa trong hộp thoại xác nhận',
             'Không nhập gì',
             'Bản ghi biến mất khỏi danh sách. Có thông báo xóa thành công.'),
            ('Hộp thoại xác nhận nêu đúng tên bản ghi', 'P0',
             'Danh mục có bản ghi xóa được',
             '1. Ghi lại tên bản ghi\n2. Bấm nút Xóa\n3. Đọc nội dung hộp thoại',
             'Không nhập gì',
             'Hộp thoại ghi rõ tên bản ghi sắp xóa, đúng với dòng vừa bấm.'),
            ('Bấm Hủy thì không xóa gì', 'P0',
             'Đang mở hộp thoại xác nhận xóa',
             '1. Bấm nút Hủy\n2. Quan sát danh sách',
             'Không nhập gì',
             'Hộp thoại đóng lại. Bản ghi VẪN còn nguyên trong danh sách.'),
            ('Bản ghi đang được sử dụng thì không có nút Xóa', 'P0',
             'Danh mục có bản ghi %s' % c['dieu_kien_an_xoa'],
             '1. Tìm dòng đó trên danh sách\n2. Quan sát cột Hành động',
             'Không nhập gì',
             'Nút Xóa KHÔNG hiển thị. Đây là ẩn hẳn nút, không phải hiện nút xám không bấm được.'),
            ('Bản ghi bị dùng ngay trước khi xác nhận', 'P2',
             'Đang mở hộp thoại xác nhận xóa một bản ghi',
             '1. Nhờ người khác dùng bản ghi đó ở một chứng từ\n2. Bấm Xóa trong hộp thoại',
             'Không nhập gì',
             'Hệ thống từ chối xóa và báo rõ lý do. Bản ghi vẫn còn trong danh sách.'),
        ]
        if c.get('co_trangthai'):
            t.append(('Xóa khác với Khóa', 'P1',
                      'Danh mục có bản ghi Hoạt động xóa được',
                      '1. Khóa một bản ghi\n2. Quan sát danh sách\n'
                      '3. Xóa một bản ghi khác\n4. Quan sát danh sách',
                      'Không nhập gì',
                      'Bản ghi Khóa VẪN nằm trong danh sách kèm badge Khóa. Bản ghi bị Xóa thì '
                      'biến mất hẳn.'))
        return self._mk(t)

    def _sec_lock(self):
        t = [
            ('Khóa một bản ghi đang Hoạt động', 'P0',
             'Có quyền quản lý, danh mục có bản ghi Hoạt động',
             '1. Bấm nút Khóa trên dòng đó\n2. Bấm Khóa trong hộp thoại xác nhận',
             'Không nhập gì',
             'Cột Trạng thái của dòng đổi thành badge Khóa. Có thông báo thành công.'),
            ('Mở khóa một bản ghi đang Khóa', 'P0',
             'Danh mục có bản ghi đang Khóa',
             '1. Bấm nút Mở khóa trên dòng đó\n2. Xác nhận trong hộp thoại',
             'Không nhập gì',
             'Cột Trạng thái đổi về Hoạt động. Nút Sửa xuất hiện trở lại trên dòng đó.'),
            ('Nút đổi tên theo trạng thái hiện tại', 'P1',
             'Danh mục có cả bản ghi Hoạt động lẫn bản ghi Khóa',
             '1. Rê chuột lên nút khóa của một dòng Hoạt động\n'
             '2. Rê chuột lên nút khóa của một dòng đang Khóa',
             'Không nhập gì',
             'Dòng Hoạt động hiện nút Khóa, dòng đang Khóa hiện nút Mở khóa — hai nút khác '
             'nhau cả tên lẫn biểu tượng.'),
            ('Bấm Hủy thì không đổi trạng thái', 'P0',
             'Đang mở hộp thoại xác nhận khóa',
             '1. Bấm nút Hủy\n2. Quan sát dòng vừa thao tác',
             'Không nhập gì',
             'Trạng thái giữ nguyên như trước khi bấm.'),
            ('Bản ghi Khóa không sửa được kể cả khi vào thẳng đường dẫn', 'P0',
             'Có một bản ghi đang ở trạng thái Khóa',
             '1. Ghi lại đường dẫn sửa của bản ghi đó khi còn Hoạt động\n2. Khóa bản ghi\n'
             '3. Dán đường dẫn sửa vào thanh địa chỉ và nhấn Enter',
             'Đường dẫn màn sửa của bản ghi đang Khóa',
             'Hệ thống không cho sửa: chuyển về màn xem hoặc từ chối lưu và báo bản ghi đang '
             'bị khóa.'),
            ('Khóa được ghi vào lịch sử', 'P1',
             'Vừa khóa một bản ghi',
             '1. Bấm nút Lịch sử trên dòng đó\n2. Đọc mốc mới nhất',
             'Không nhập gì',
             'Lịch sử có một mốc mới thuộc nhóm thay đổi trạng thái, ghi rõ chuyển từ Hoạt động '
             'sang Khóa kèm người thực hiện.'),
        ]
        return self._mk(t)

    def _sec_save(self):
        c = self.c
        t = [
            ('Lưu cấu hình với dữ liệu hợp lệ', 'P0',
             'Có quyền và đã sao lưu dữ liệu giá trước khi thử',
             '1. Nhập hệ số hợp lệ\n2. Bấm Lưu\n3. Bấm Xác nhận trong hộp thoại',
             'Hệ số hợp lệ trong khoảng cho phép',
             'Cấu hình được ghi. Có thông báo thành công kèm số gói đã cập nhật.'),
            ('Hộp thoại xác nhận nêu rõ phạm vi ảnh hưởng', 'P0',
             'Đang ở màn cấu hình',
             '1. Đổi hệ số\n2. Bấm Lưu\n3. Đọc nội dung hộp thoại',
             'Hệ số mới bất kỳ',
             'Hộp thoại ghi rõ số gói bảo dưỡng sẽ bị ghi đè và số cấp dịch vụ sẽ được tính lại.'),
            ('Bấm Hủy thì không ghi gì', 'P0',
             'Đang mở hộp thoại xác nhận',
             '1. Bấm Hủy\n2. Mở lại màn hình',
             'Không nhập gì',
             'Cấu hình giữ nguyên giá trị cũ. Không gói nào bị đổi giá.'),
            ('Gói đã chỉnh riêng cũng bị ghi đè', 'P0',
             'Đã chỉnh riêng hệ số cho một gói bảo dưỡng và ghi lại giá trị đó',
             '1. Về màn cấu hình, đổi hệ số\n2. Lưu và xác nhận\n'
             '3. Mở lại gói đã chỉnh riêng',
             'Hệ số mới khác hệ số riêng của gói',
             'Gói đó cũng bị áp hệ số mới — đây là hành vi đúng theo thiết kế, không phải lỗi.'),
            ('Định mức đàm phán được ghi đè kể cả khi không đổi', 'P1',
             'Đã chỉnh riêng định mức cho một gói',
             '1. Giữ nguyên định mức trên màn cấu hình\n2. Bấm Lưu và xác nhận\n'
             '3. Mở lại gói đã chỉnh riêng',
             'Giữ nguyên định mức cũ',
             'Định mức của gói vẫn bị áp lại theo giá trị chung.'),
            ('Giá gốc chỉ tính lại khi hệ số thay đổi', 'P1',
             'Đã ghi lại giá gốc của một cấp dịch vụ',
             '1. Giữ nguyên hệ số, chỉ đổi định mức\n2. Lưu và xác nhận\n'
             '3. Kiểm tra lại giá gốc của cấp dịch vụ đó',
             'Chỉ đổi định mức',
             'Giá gốc của cấp dịch vụ KHÔNG bị tính lại.'),
            ('Màn hình hiển thị lần cập nhật gần nhất', 'P2',
             'Đã có ít nhất một lần lưu',
             '1. Mở lại màn hình\n2. Đọc dòng ghi chú phía dưới hai ô nhập',
             'Không nhập gì',
             'Có dòng ghi rõ ngày giờ và tên người thực hiện lần lưu gần nhất.'),
        ]
        for f in c['truong'][:2]:
            if f[4] == 'Có':
                t.append(('Bỏ trống ô bắt buộc %s' % f[0], 'P0',
                          'Đang ở màn cấu hình',
                          '1. Xóa trắng ô %s\n2. Bấm Lưu' % f[0],
                          'Ô %s để trống' % f[0],
                          'Hệ thống báo "Bắt buộc phải nhập" ngay dưới ô %s và KHÔNG ghi gì.'
                          % f[0]))
        for extra in c.get('tc_save_them', []):
            t.append(extra)
        return self._mk(t)

    def _sec_history(self):
        t = [
            ('Mở lịch sử của một bản ghi', 'P0',
             'Danh sách có bản ghi đã từng bị sửa',
             '1. Bấm nút Lịch sử trên dòng đó',
             'Không nhập gì',
             'Cửa sổ lịch sử mở ra, ghi rõ đang xem lịch sử của bản ghi nào.'),
            ('Lịch sử sắp mới nhất lên trước', 'P0',
             'Bản ghi đã bị sửa ít nhất hai lần',
             '1. Mở lịch sử của bản ghi đó\n2. Đọc mốc thời gian từ trên xuống',
             'Không nhập gì',
             'Mốc trên cùng là lần thay đổi gần nhất, các mốc cũ hơn nằm phía dưới.'),
            ('Lịch sử ghi đủ giá trị cũ và giá trị mới', 'P0',
             'Vừa sửa một trường của bản ghi và ghi lại giá trị trước khi sửa',
             '1. Mở lịch sử của bản ghi đó\n2. Đọc mốc mới nhất',
             'Không nhập gì',
             'Mốc mới nhất ghi đúng tên trường đã đổi kèm cả giá trị trước và giá trị sau.'),
            ('Tên trường trong lịch sử là tiếng Việt dễ hiểu', 'P1',
             'Bản ghi đã từng bị sửa',
             '1. Mở lịch sử\n2. Đọc tên các trường được liệt kê',
             'Không nhập gì',
             'Tên trường hiển thị đúng như nhãn trên form, không hiện tên kỹ thuật hay số '
             'định danh.'),
            ('Bản ghi chưa từng sửa hiện trạng thái rỗng', 'P1',
             'Có bản ghi vừa được thêm và chưa sửa lần nào',
             '1. Bấm nút Lịch sử trên dòng đó',
             'Không nhập gì',
             'Cửa sổ hiện thông báo chưa có lịch sử thao tác nào, KHÔNG báo lỗi.'),
            ('Người thực hiện hiển thị đúng', 'P1',
             'Vừa sửa một bản ghi',
             '1. Mở lịch sử của bản ghi đó\n2. Đọc dòng người thực hiện',
             'Không nhập gì',
             'Ghi đúng họ tên người vừa thực hiện thao tác.'),
        ]
        return self._mk(t)

    def _sec_import(self):
        t = [
            ('Tải tệp mẫu', 'P1',
             'Có quyền quản lý, đang mở cửa sổ nhập từ Excel',
             '1. Bấm nút Tải file mẫu',
             'Không nhập gì',
             'Tệp mẫu được tải về, mở ra thấy đủ dòng tiêu đề cột đúng thứ tự.'),
            ('Nạp tệp hợp lệ lên bảng xem trước', 'P0',
             'Đã có tệp điền đúng mẫu',
             '1. Bấm Chọn file Excel và chọn tệp\n2. Bấm Load lên bảng',
             'Tệp có vài dòng dữ liệu hợp lệ',
             'Bảng xem trước hiện đủ số dòng của tệp. Bộ đếm Tổng khớp số dòng.'),
            ('Chưa kiểm tra thì chưa ghi được', 'P0',
             'Vừa nạp tệp lên bảng, chưa bấm kiểm tra',
             '1. Quan sát nút ghi dữ liệu',
             'Không nhập gì',
             'Nút ghi chưa dùng được. Phải chạy kiểm tra trước.'),
            ('Kiểm tra tệp toàn dòng hợp lệ', 'P0',
             'Đã nạp tệp toàn dòng hợp lệ lên bảng',
             '1. Bấm Validate\n2. Quan sát bảng',
             'Tệp toàn dòng hợp lệ',
             'Không dòng nào bị đánh dấu lỗi. Nút ghi dữ liệu bật lên.'),
            ('Kiểm tra tệp có dòng thiếu trường bắt buộc', 'P0',
             'Đã chuẩn bị tệp có một dòng bỏ trống ô bắt buộc',
             '1. Nạp tệp lên bảng\n2. Bấm Validate',
             'Tệp có một dòng thiếu dữ liệu bắt buộc',
             'Dòng đó bị đánh dấu lỗi kèm mô tả lỗi rõ ràng, các dòng còn lại vẫn hợp lệ.'),
            ('Kiểm tra tệp có dòng trùng dữ liệu đã có', 'P0',
             'Đã chuẩn bị tệp có một dòng trùng bản ghi đang có trong danh mục',
             '1. Nạp tệp lên bảng\n2. Bấm Validate',
             'Tệp có một dòng trùng dữ liệu',
             'Dòng đó bị đánh dấu lỗi trùng, không được ghi vào danh mục.'),
            ('Ghi dữ liệu bỏ qua dòng lỗi', 'P0',
             'Đã kiểm tra tệp vừa có dòng hợp lệ vừa có dòng lỗi',
             '1. Bấm nút ghi dữ liệu\n2. Đọc thông báo\n3. Đóng cửa sổ và xem danh sách',
             'Tệp trộn dòng hợp lệ và dòng lỗi',
             'Chỉ dòng hợp lệ được thêm vào danh mục. Thông báo nêu rõ số dòng thành công và '
             'số dòng bị bỏ qua.'),
            ('Lọc chỉ hiện dòng lỗi', 'P1',
             'Đã kiểm tra tệp có cả dòng lỗi lẫn dòng hợp lệ',
             '1. Tích ô Chỉ dòng lỗi',
             'Không nhập gì',
             'Bảng chỉ còn các dòng đang bị lỗi, tiện cho việc sửa lại.'),
            ('Làm mới xóa trắng bảng', 'P1',
             'Bảng xem trước đang có dữ liệu',
             '1. Bấm nút Làm mới',
             'Không nhập gì',
             'Bảng trắng trơn, bộ đếm Tổng về 0, sẵn sàng nạp tệp mới.'),
            ('Chọn tệp sai định dạng cột', 'P1',
             'Có tệp Excel nhưng tiêu đề cột không đúng mẫu',
             '1. Chọn tệp đó\n2. Bấm Load lên bảng',
             'Tệp sai cấu trúc cột',
             'Hệ thống báo lỗi định dạng và KHÔNG đổ dữ liệu lên bảng.'),
        ]
        return self._mk(t)

    def _sec_export(self):
        t = [
            ('Xuất Excel với toàn bộ trường', 'P0',
             'Đang ở màn danh sách có dữ liệu',
             '1. Bấm nút Xuất Excel\n2. Giữ nguyên lựa chọn mặc định\n3. Bấm Xuất file',
             'Không bỏ chọn trường nào',
             'Tệp được tải về, mở ra có đủ các cột đã chọn và đủ số dòng của danh sách.'),
            ('Cửa sổ chọn trường mặc định chọn hết', 'P1',
             'Đang ở màn danh sách',
             '1. Bấm nút Xuất Excel\n2. Quan sát bộ đếm số trường',
             'Không nhập gì',
             'Bộ đếm hiện đang chọn tất cả các trường có sẵn.'),
            ('Bỏ bớt trường thì tệp chỉ có cột đã chọn', 'P0',
             'Đang mở cửa sổ chọn trường xuất',
             '1. Bỏ chọn hai trường bất kỳ\n2. Bấm Xuất file\n3. Mở tệp',
             'Bỏ chọn hai trường',
             'Tệp chỉ có các cột còn được chọn, không có hai cột đã bỏ.'),
            ('Thứ tự cột theo đúng trình tự chọn', 'P1',
             'Đang mở cửa sổ chọn trường xuất',
             '1. Bỏ chọn hết\n2. Chọn lại các trường theo thứ tự mong muốn\n'
             '3. Đọc dòng thứ tự cột\n4. Bấm Xuất file',
             'Chọn trường theo thứ tự tùy ý',
             'Dòng thứ tự cột và thứ tự cột trong tệp khớp đúng trình tự vừa chọn.'),
            ('Không chọn trường nào thì không xuất được', 'P0',
             'Đang mở cửa sổ chọn trường xuất',
             '1. Bấm Bỏ chọn hết\n2. Quan sát nút Xuất file',
             'Không chọn trường nào',
             'Nút Xuất file không dùng được. Không có tệp nào được tạo.'),
            ('Tệp xuất áp đúng bộ lọc đang dùng', 'P0',
             'Đã lọc danh sách còn ít dòng và ghi lại số lượng',
             '1. Bấm Xuất Excel\n2. Bấm Xuất file\n3. Đếm số dòng trong tệp',
             'Một tiêu chí lọc bất kỳ',
             'Số dòng trong tệp khớp số dòng đang hiện sau khi lọc, KHÔNG xuất toàn bộ danh mục.'),
            ('Xuất khi danh sách rỗng', 'P2',
             'Đã lọc ra kết quả rỗng',
             '1. Bấm Xuất Excel\n2. Bấm Xuất file\n3. Mở tệp',
             'Bộ lọc cho kết quả rỗng',
             'Tệp chỉ có dòng tiêu đề, không báo lỗi.'),
        ]
        return self._mk(t)

    def _sec_print(self):
        t = [
            ('Mở bản in danh sách', 'P0',
             'Đang ở màn danh sách có dữ liệu',
             '1. Bấm nút In danh sách',
             'Không nhập gì',
             'Thẻ trình duyệt mới mở ra hiển thị bản in đã dàn trang sẵn.'),
            ('Bản in lấy đúng bộ lọc đang áp dụng', 'P0',
             'Đã lọc danh sách còn ít dòng và ghi lại số lượng',
             '1. Bấm In danh sách\n2. Đếm số dòng trên bản in',
             'Một tiêu chí lọc bất kỳ',
             'Bản in chỉ chứa các dòng khớp bộ lọc, không in toàn bộ danh mục.'),
            ('Bản in lấy đúng bộ cột đang hiển thị', 'P1',
             'Đã tắt bớt vài cột ở cửa sổ tùy chỉnh cột',
             '1. Bấm In danh sách\n2. Đối chiếu cột trên bản in',
             'Không nhập gì',
             'Bản in có đúng bộ cột đang hiện trên màn danh sách.'),
            ('Bản in giữ được dấu tiếng Việt và định dạng số', 'P1',
             'Danh sách có bản ghi tên tiếng Việt có dấu',
             '1. Bấm In danh sách\n2. Đọc kỹ nội dung bản in',
             'Không nhập gì',
             'Chữ tiếng Việt hiện đủ dấu, số hiển thị đúng định dạng, không bị vỡ hay mất chữ.'),
        ]
        return self._mk(t)

    def _sec_display(self):
        t = []
        if self.has('columns'):
            t += [
                ('Tắt một cột thì cột đó biến mất khỏi bảng', 'P0',
                 'Đang ở màn danh sách',
                 '1. Bấm biểu tượng tùy chỉnh cột\n2. Bỏ tích một cột đang hiện\n3. Bấm Lưu',
                 'Bỏ tích một cột',
                 'Bảng vẽ lại, không còn cột vừa bỏ tích.'),
                ('Bật một cột đang ẩn', 'P0',
                 'Màn hình có cột mặc định ẩn',
                 '1. Mở cửa sổ tùy chỉnh cột\n2. Tích chọn một cột đang ẩn\n3. Bấm Lưu',
                 'Tích thêm một cột',
                 'Bảng hiện thêm cột vừa chọn kèm dữ liệu đúng.'),
                ('Cấu hình cột được nhớ ở lần vào sau', 'P0',
                 'Vừa lưu một cấu hình cột khác mặc định',
                 '1. Chuyển sang màn khác\n2. Quay lại màn danh sách',
                 'Không nhập gì',
                 'Bảng dựng lại đúng bộ cột đã lưu, không quay về mặc định.'),
                ('Cột bắt buộc không bỏ tích được', 'P1',
                 'Đang mở cửa sổ tùy chỉnh cột',
                 '1. Thử bỏ tích cột STT và cột Hành động',
                 'Không nhập gì',
                 'Hai cột này luôn được tích và không bỏ tích được.'),
                ('Bấm Đóng thì giữ nguyên cấu hình cũ', 'P1',
                 'Đang mở cửa sổ tùy chỉnh cột',
                 '1. Đổi vài ô tích\n2. Bấm Đóng thay vì Lưu',
                 'Đổi vài lựa chọn',
                 'Bảng giữ nguyên bộ cột cũ, thay đổi vừa rồi không được áp dụng.'),
            ]
        if self.has('fcfg'):
            t += [
                ('Tắt một ô lọc thì ô đó biến mất', 'P0',
                 'Đang ở màn danh sách',
                 '1. Bấm nút Cài đặt bộ lọc\n2. Bỏ tích một ô lọc\n3. Bấm Lưu',
                 'Bỏ tích một ô lọc',
                 'Khu vực lọc vẽ lại, không còn ô vừa bỏ tích.'),
                ('Kéo thả đổi thứ tự ô lọc', 'P1',
                 'Đang mở cửa sổ cài đặt bộ lọc',
                 '1. Kéo một ô lọc lên vị trí đầu\n2. Bấm Lưu',
                 'Đổi thứ tự một ô',
                 'Khu vực lọc hiện các ô theo đúng thứ tự vừa sắp.'),
                ('Khôi phục mặc định đưa bộ lọc về gốc', 'P1',
                 'Đã lưu một cấu hình lọc khác mặc định',
                 '1. Mở cửa sổ cài đặt bộ lọc\n2. Bấm Khôi phục mặc định',
                 'Không nhập gì',
                 'Bộ ô lọc trở về đúng cấu hình gốc của màn hình.'),
                ('Cấu hình bộ lọc được nhớ ở lần vào sau', 'P1',
                 'Vừa lưu một cấu hình lọc khác mặc định',
                 '1. Chuyển sang màn khác\n2. Quay lại màn danh sách',
                 'Không nhập gì',
                 'Khu vực lọc dựng lại đúng cấu hình đã lưu.'),
            ]
        return self._mk(t)

    def _sec_ux(self):
        t = [
            ('Thông báo lỗi hiển thị bằng chữ đỏ ngay dưới ô sai', 'P1',
             'Đang mở form có ô bắt buộc' if self.has('create') else 'Đang ở màn hình',
             '1. Để trống một ô bắt buộc\n2. Bấm Lưu',
             'Ô bắt buộc để trống',
             'Chữ lỗi màu đỏ nằm ngay dưới đúng ô bị sai, không phải thông báo chung chung ở '
             'đầu màn hình.'),
            ('Chữ mô tả và ghi chú không dùng màu đỏ', 'P2',
             'Đang ở màn hình',
             '1. Quan sát các dòng chữ hướng dẫn và ghi chú',
             'Không nhập gì',
             'Chữ hướng dẫn dùng màu xám. Màu đỏ chỉ dành cho lỗi nhập liệu, để người dùng '
             'không tưởng nhầm là đang có lỗi.'),
            ('Nút không dùng được thì ẩn hẳn', 'P0',
             'Danh sách có bản ghi không thao tác được',
             '1. Quan sát cột Hành động của dòng đó',
             'Không nhập gì',
             'Nút không dùng được bị ẩn hẳn, KHÔNG hiện dạng nút xám bấm không ăn.'),
            ('Vòng quay chờ hiện khi đang nạp dữ liệu', 'P2',
             'Đang ở màn danh sách',
             '1. Bấm Tìm kiếm và quan sát ngay',
             'Không nhập gì',
             'Có vòng quay chờ trong lúc nạp, biến mất khi dữ liệu hiện ra.'),
            ('Ngày giờ hiển thị theo định dạng ngày tháng năm', 'P2',
             'Danh sách có dữ liệu',
             '1. Quan sát cột Ngày tạo',
             'Không nhập gì',
             'Ngày hiện dạng ngày/tháng/năm kèm giờ phút, không hiện giây.'),
            ('Màn hình hiển thị tốt trên độ phân giải nhỏ', 'P2',
             'Đang ở màn danh sách',
             '1. Thu nhỏ cửa sổ trình duyệt còn khoảng một nửa màn hình',
             'Không nhập gì',
             'Bảng có thanh cuộn ngang riêng, các nút không bị vỡ khung hay chồng lên nhau.'),
        ]
        return self._mk(t)

    # ================================================================ chay
    def run(self):
        out = os.path.join(self.out_dir, 'testcase - %s.xlsx'
                           % self.ten.replace('/', '-'))
        secs = self.sections()
        total = build(out, self.c['tc_sheet'], self.ten, self.c['tc_module'],
                      self.desc_block(), self.role_tcs(), secs)
        return out, total
