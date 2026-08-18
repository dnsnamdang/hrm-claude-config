# -*- coding: utf-8 -*-
"""Bo sinh HDSD dung chung cho cac man DANH MUC.

Dung chung dict cau hinh voi catalog_srs.py / catalog_tc.py. Tai lieu viet click-by-click:
moi nut deu mo ta form mo ra, tung o nhap (bat buoc + gia tri mac dinh), cach luu va ket qua.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "hdsd-documenter", "assets"))

from hdsd_engine import HdsdBuilder  # noqa: E402

NGAY = '18/08/2026'
NGUOI = 'Tri Lee'


class CatalogHdsd(object):
    def __init__(self, cfg, shots_dir, out_dir):
        self.c = cfg
        self.shots_dir = shots_dir
        self.out_dir = out_dir
        self.ten = cfg['ten']
        self.dt = cfg['doi_tuong']
        self.qql = cfg['quyen_quan_ly']
        self.qxem = cfg.get('quyen_xem')
        self.funcs = [f if isinstance(f, tuple) else (f, {}) for f in cfg['funcs']]
        self.names = [f[0] for f in self.funcs]

    def has(self, n):
        return n in self.names

    def shot(self, key):
        return self.c['shots'][key]

    # ================================================================ dung file
    def build(self):
        c = self.c
        b = HdsdBuilder(
            output=os.path.join(self.out_dir, 'HDSD_%s.docx' % self.ten.replace('/', '-')),
            shots_dir=self.shots_dir,
            cover_title='(Màn hình: %s)' % self.ten,
            doc_title='HDSD - %s' % self.ten)
        self.b = b

        b.h1('TỔNG QUAN')

        b.h2('1. Thuật ngữ sử dụng trong tài liệu')
        b.table([['Thuật ngữ', 'Giải thích']] + [[t[0], t[1]] for t in c['thuat_ngu']])

        b.h2('2. Cập nhật tài liệu')
        b.table([
            ['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung'],
            ['1.0', NGAY, NGUOI, 'Lập mới theo mẫu tài liệu hiện hành cho màn %s.' % self.ten],
        ])

        b.h2('3. Giới thiệu chung')
        for p in c['hdsd_gioithieu']:
            b.para(p)
        b.para('Đường dẫn truy cập:')
        b.bullet('Menu: %s' % c['menu'])
        b.bullet('Hoặc gõ thẳng đường dẫn %s vào thanh địa chỉ trình duyệt'
                 % (c['host'] + c['route']))

        b.h2('4. Quyền sử dụng')
        rows = [['Tên quyền', 'Cho phép làm gì', 'Ghi chú']]
        rows.append([self.qql, c['tacdung_ql'],
                     'Đây là quyền dành cho người phụ trách danh mục.'])
        if self.qxem:
            rows.append([self.qxem, c['tacdung_xem'],
                         'Cấp cho người chỉ cần tra cứu, không được sửa dữ liệu.'])
        b.table(rows)
        b.para('Nếu bạn không thấy mục menu này, hãy liên hệ quản trị viên để được cấp quyền. '
               'Gõ thẳng đường dẫn khi chưa có quyền cũng sẽ bị hệ thống chặn.')

        b.h1('HƯỚNG DẪN SỬ DỤNG')
        stt = [0]

        def h2(t):
            stt[0] += 1
            b.h2('%d. %s' % (stt[0], t))
            return stt[0]

        self._mo_man(h2)
        if self.has('filter'):
            self._tim_kiem(h2)
        if self.has('view'):
            self._xem(h2)
        if self.has('create'):
            self._them(h2)
        if self.has('edit'):
            self._sua(h2)
        if self.has('delete'):
            self._xoa(h2)
        if self.has('lock'):
            self._khoa(h2)
        if self.has('save'):
            self._luu(h2)
        if self.has('history'):
            self._lichsu(h2)
        if self.has('import'):
            self._import(h2)
        if self.has('export'):
            self._xuat(h2)
        if self.has('print'):
            self._in(h2)
        if self.has('columns') or self.has('fcfg'):
            self._hienthi(h2)
        self._faq(h2)

        b.finish()
        return b

    # ---------------------------------------------------------------- 1
    def _mo_man(self, h2):
        b, c = self.b, self.c
        h2('Mở màn hình và đọc danh sách')
        b.para('Vào menu theo đường dẫn ở phần Tổng quan. Màn hình mở ra gồm hai khu vực: '
               'khu vực tìm kiếm ở trên và bảng danh sách ở dưới.')
        if 'danhsach' in c['shots']:
            b.image(self.shot('danhsach'), 'Màn hình %s khi mới mở' % self.ten)
        b.para('Ý nghĩa từng cột trong bảng:')
        b.table([['Cột', 'Ý nghĩa']] + [[x[0], x[1]] for x in c['cot']])
        b.para('Một số điểm cần biết khi đọc bảng:')
        b.bullet('Số thứ tự chạy liên tục qua các trang, không quay về 1 khi sang trang mới.')
        b.bullet('Cột nào có biểu tượng mũi tên hai chiều cạnh tiêu đề là cột sắp xếp được. '
                 'Bấm lần đầu sắp tăng dần, bấm lần nữa đảo sang giảm dần.')
        b.bullet('Góc trái dưới bảng ghi rõ đang xem bao nhiêu dòng trên tổng số bao nhiêu '
                 'bản ghi. Góc phải là ô chọn số dòng mỗi trang và các nút chuyển trang.')
        if c.get('co_trangthai'):
            b.bullet('Bản ghi đã Khóa vẫn nằm trong danh sách, nhận biết bằng nhãn Khóa ở cột '
                     'Trạng thái. Bản ghi bị Xóa mới biến mất hẳn.')
        b.bullet('Nút nào bạn không thấy ở cột Hành động nghĩa là thao tác đó hiện không dùng '
                 'được — do bạn chưa có quyền, hoặc do bản ghi không đủ điều kiện.')

    # ---------------------------------------------------------------- 2
    def _tim_kiem(self, h2):
        b, c = self.b, self.c
        h2('Tìm kiếm và lọc danh sách')
        b.para('Dùng khi danh mục đã nhiều bản ghi và bạn cần tìm nhanh một mục cụ thể.')
        if 'boloc' in c['shots']:
            b.image(self.shot('boloc'), 'Khu vực tìm kiếm và lọc')
        b.para('Các ô lọc có sẵn:')
        b.table([['Ô lọc', 'Cách dùng']] + [[f[0], f[4]] for f in c['loc']])
        b.para('Các bước thực hiện:')
        b.bullet('Bước 1: Nhập từ khóa vào ô tìm nhanh, hoặc chọn giá trị ở các ô lọc.')
        b.bullet('Bước 2: Bấm nút Tìm kiếm, hoặc nhấn phím Enter ngay tại ô tìm nhanh.')
        b.bullet('Bước 3: Bảng hiển thị lại từ trang 1 với các bản ghi khớp tiêu chí.')
        b.para('Lưu ý khi lọc:')
        b.bullet('Nhập nhiều tiêu chí cùng lúc thì hệ thống lọc theo kiểu “và” — bản ghi phải '
                 'thỏa TẤT CẢ tiêu chí mới hiện ra.')
        b.bullet('Ô tìm nhanh không phân biệt chữ hoa chữ thường, và khớp cả khi bạn chỉ nhập '
                 'một phần tên.')
        b.bullet('Nút Làm mới xóa hết tiêu chí VÀ nạp lại danh sách đầy đủ ngay, bạn không cần '
                 'bấm thêm Tìm kiếm.')
        b.bullet('Nếu bảng báo không có dữ liệu phù hợp, hãy kiểm tra lại xem còn tiêu chí nào '
                 'chưa xóa không.')

    # ---------------------------------------------------------------- 3
    def _xem(self, h2):
        b, c = self.b, self.c
        opts = dict(self.funcs[self.names.index('view')][1])
        modal = opts.get('modal', True)
        cot = opts.get('cot_bam', 'tên')
        h2('Xem chi tiết một %s' % self.dt)
        b.para('Bấm vào %s ở dòng cần xem. Hệ thống mở %s ở chế độ chỉ đọc — bạn xem được đầy '
               'đủ thông tin nhưng không sửa được gì.'
               % (cot, 'cửa sổ xem' if modal else 'màn hình chi tiết'))
        if 'xem' in c['shots']:
            b.image(self.shot('xem'), 'Màn xem chi tiết %s' % self.dt)
        b.para('Muốn sửa thì đóng màn xem rồi bấm nút Sửa ở cột Hành động.')

    # ---------------------------------------------------------------- 4
    def _them(self, h2):
        b, c = self.b, self.c
        opts = dict(self.funcs[self.names.index('create')][1])
        modal = opts.get('modal', True)
        h2('Thêm mới một %s' % self.dt)
        b.para('Bấm nút Tạo mới ở góc phải phía trên bảng. Hệ thống mở %s trống.'
               % ('cửa sổ nhập liệu' if modal else 'màn hình nhập liệu riêng'))
        if 'taomoi' in c['shots']:
            b.image(self.shot('taomoi'), 'Form Tạo %s' % self.dt)
        b.para('Ý nghĩa từng ô nhập:')
        b.table([['Ô nhập', 'Bắt buộc', 'Giá trị ban đầu', 'Cách nhập']]
                + [[t[0], t[4], t[5], t[6]] for t in c['truong']])
        b.para('Các bước thực hiện:')
        b.bullet('Bước 1: Nhập đủ các ô có dấu sao đỏ bên cạnh nhãn — đó là ô bắt buộc.')
        b.bullet('Bước 2: Bấm Lưu để ghi và đóng form, hoặc bấm Lưu và tiếp tục nếu bạn còn '
                 'muốn thêm nhiều bản ghi liên tiếp.')
        b.bullet('Bước 3: Hệ thống báo thành công và danh sách nạp lại, có bản ghi vừa thêm.')
        if 'validate' in c['shots']:
            b.para('Nếu nhập thiếu hoặc sai, hệ thống báo lỗi bằng chữ đỏ ngay dưới ô bị sai. '
                   'Form KHÔNG đóng và dữ liệu bạn đã nhập vẫn còn nguyên.')
            b.image(self.shot('validate'), 'Hệ thống báo lỗi ngay dưới ô còn thiếu')
        b.para('Những lỗi thường gặp:')
        b.table([['Thông báo', 'Nguyên nhân và cách xử lý']]
                + c['hdsd_loi'])
        b.para('Bấm %s để hủy bỏ; hệ thống không ghi gì.'
               % ('Đóng' if modal else 'Quay lại'))

    # ---------------------------------------------------------------- 5
    def _sua(self, h2):
        b, c = self.b, self.c
        h2('Chỉnh sửa một %s' % self.dt)
        b.para('Bấm nút Sửa (biểu tượng cây bút) ở cột Hành động của dòng cần sửa. Form mở ra '
               'đã điền sẵn dữ liệu hiện tại.')
        if 'sua' in c['shots']:
            b.image(self.shot('sua'), 'Form Sửa %s' % self.dt)
        b.para('Các bước thực hiện:')
        b.bullet('Bước 1: Sửa lại các ô cần đổi. Quy tắc nhập giống hệt phần Thêm mới.')
        b.bullet('Bước 2: Bấm Lưu.')
        b.bullet('Bước 3: Hệ thống báo thành công và danh sách hiện giá trị mới.')
        b.para('Lưu ý khi sửa:')
        if c.get('loi_trung'):
            b.bullet('Giữ nguyên %s cũ của chính bản ghi thì KHÔNG bị báo trùng. Chỉ khi bạn '
                     'đổi sang giá trị đang thuộc về bản ghi khác mới bị chặn.'
                     % c['truong_trung'])
        if c.get('co_trangthai'):
            b.bullet('Bản ghi đang ở trạng thái Khóa thì KHÔNG có nút Sửa. Bạn phải bấm Mở '
                     'khóa trước, sửa xong rồi Khóa lại nếu cần.')
        b.bullet('Nếu bạn đã đổi dữ liệu rồi thoát mà chưa lưu, hệ thống sẽ hỏi xác nhận để '
                 'bạn không mất công nhập lại.')
        for extra in c.get('hdsd_sua_them', []):
            b.bullet(extra)

    # ---------------------------------------------------------------- 6
    def _xoa(self, h2):
        b, c = self.b, self.c
        h2('Xóa một %s' % self.dt)
        b.para('Bấm nút Xóa (biểu tượng thùng rác màu đỏ) ở cột Hành động. Hệ thống hỏi xác '
               'nhận và ghi rõ tên bản ghi sắp xóa.')
        if 'xoa' in c['shots']:
            b.image(self.shot('xoa'), 'Hộp thoại xác nhận xóa')
        b.para('Bấm Xóa để xác nhận, hoặc Hủy để giữ nguyên.')
        b.para('Vì sao có dòng không thấy nút Xóa?')
        b.bullet('Nút Xóa chỉ hiện khi %s.' % c['dieu_kien_xoa'])
        b.bullet('Dòng nào %s thì nút Xóa bị ẩn hẳn. Đây là cách hệ thống bảo vệ dữ liệu: xóa '
                 'một mục đang được dùng sẽ làm hỏng các chứng từ liên quan.'
                 % c['dieu_kien_an_xoa'])
        if c.get('co_trangthai'):
            b.bullet('Nếu bạn chỉ muốn ngừng dùng chứ không muốn mất dữ liệu, hãy dùng thao '
                     'tác Khóa thay vì Xóa.')
        b.bullet('Xóa xong là không khôi phục được, hãy cân nhắc kỹ trước khi xác nhận.')

    # ---------------------------------------------------------------- 7
    def _khoa(self, h2):
        b, c = self.b, self.c
        h2('Khóa và Mở khóa một %s' % self.dt)
        b.para('Khóa dùng khi bạn muốn ngừng cho chọn %s ở nghiệp vụ mới, nhưng vẫn giữ nguyên '
               'dữ liệu và các chứng từ cũ.' % self.dt)
        if 'khoa' in c['shots']:
            b.image(self.shot('khoa'), 'Hộp thoại xác nhận khóa')
        b.para('Các bước thực hiện:')
        b.bullet('Bước 1: Bấm nút hình ổ khóa ở cột Hành động. Dòng đang Hoạt động hiện nút '
                 'Khóa, dòng đang Khóa hiện nút Mở khóa.')
        b.bullet('Bước 2: Đọc kỹ câu hỏi xác nhận rồi bấm nút xác nhận.')
        b.bullet('Bước 3: Nhãn ở cột Trạng thái đổi theo ngay.')
        b.para('Phân biệt Khóa và Xóa:')
        b.table([
            ['Tiêu chí', 'Khóa', 'Xóa'],
            ['Bản ghi còn trong danh sách', 'Còn, kèm nhãn Khóa', 'Mất hẳn'],
            ['Chọn được ở nghiệp vụ mới', 'Không', 'Không'],
            ['Chứng từ cũ', 'Giữ nguyên', 'Giữ nguyên'],
            ['Khôi phục lại được', 'Được, bấm Mở khóa', 'Không'],
            ['Điều kiện thực hiện', 'Luôn làm được khi có quyền',
             'Chỉ khi %s' % c['dieu_kien_xoa']],
        ])
        b.para('Khi bản ghi đang Khóa, nút Sửa và nút Xóa không dùng được. Muốn sửa thì Mở '
               'khóa trước.')

    # ---------------------------------------------------------------- 8
    def _luu(self, h2):
        b, c = self.b, self.c
        h2('Cập nhật hệ số và định mức')
        b.para('CẢNH BÁO QUAN TRỌNG: một lần lưu ở màn này sẽ áp giá trị mới cho TOÀN BỘ gói '
               'bảo dưỡng đang có, kể cả gói bạn đã chỉnh riêng trước đó. Thao tác này KHÔNG '
               'hoàn tác được. Hãy sao lưu dữ liệu giá TRƯỚC khi lưu lần đầu.')
        b.para('Ý nghĩa từng ô nhập:')
        b.table([['Ô nhập', 'Bắt buộc', 'Giá trị ban đầu', 'Cách nhập']]
                + [[t[0], t[4], t[5], t[6]] for t in c['truong']])
        b.para('Các bước thực hiện:')
        b.bullet('Bước 1: Sửa Hệ số giá bán dịch vụ và Định mức đàm phán giá theo giá trị mong '
                 'muốn.')
        b.bullet('Bước 2: Bấm nút Lưu ở góc phải phía dưới màn hình.')
        b.bullet('Bước 3: Đọc kỹ hộp thoại xác nhận — hộp thoại ghi rõ có bao nhiêu gói bảo '
                 'dưỡng sẽ bị ghi đè và bao nhiêu cấp dịch vụ sẽ được tính lại giá gốc.')
        if 'xacnhan' in c['shots']:
            b.image(self.shot('xacnhan'), 'Hộp thoại xác nhận cập nhật giá dịch vụ')
        b.bullet('Bước 4: Bấm Xác nhận để thực hiện, hoặc Hủy để giữ nguyên.')
        b.para('Sau khi lưu, hệ thống báo số gói đã cập nhật thành công và số gói bị bỏ qua. '
               'Gói bị bỏ qua là gói không xác định được đơn giá công của công ty — những gói '
               'này giữ nguyên giá cũ, bạn cần xử lý riêng.')
        b.para('Dòng ghi chú phía dưới hai ô nhập cho biết lần cập nhật gần nhất do ai thực '
               'hiện và vào lúc nào.')

    # ---------------------------------------------------------------- 9
    def _lichsu(self, h2):
        b, c = self.b, self.c
        h2('Xem lịch sử thay đổi')
        b.para('Dùng khi bạn cần biết một bản ghi đã bị ai sửa, sửa lúc nào và đổi từ giá trị '
               'nào sang giá trị nào.')
        b.para('Bấm nút Lịch sử (biểu tượng đồng hồ quay ngược) ở cột Hành động của dòng cần xem.')
        if 'lichsu' in c['shots']:
            b.image(self.shot('lichsu'), 'Cửa sổ Lịch sử thay đổi')
        b.para('Cách đọc cửa sổ lịch sử:')
        b.bullet('Các mốc sắp xếp mới nhất lên trên cùng.')
        b.bullet('Mỗi mốc ghi ngày giờ, nhóm hành động và người thực hiện.')
        b.bullet('Bên dưới mỗi mốc là danh sách các trường đã đổi, kèm giá trị cũ và giá trị mới.')
        b.bullet('Bản ghi chưa từng bị sửa thì cửa sổ hiện thông báo chưa có lịch sử thao tác '
                 'nào — đây là bình thường, không phải lỗi.')
        b.para('Lịch sử chỉ để tra cứu, bạn không sửa hay xóa được nội dung trong đó.')

    # ---------------------------------------------------------------- 10
    def _import(self, h2):
        b, c = self.b, self.c
        h2('Nhập nhiều %s cùng lúc từ Excel' % self.dt)
        b.para('Dùng khi bạn cần thêm nhiều bản ghi một lần thay vì nhập tay từng cái.')
        b.para('Bấm nút Import Excel ở thanh công cụ phía trên bảng.')
        if 'import' in c['shots']:
            b.image(self.shot('import'), 'Cửa sổ nhập dữ liệu từ Excel')
        b.para('Quy trình gồm bốn bước, phải làm theo đúng thứ tự:')
        b.bullet('Bước 1: Bấm Tải file mẫu để lấy tệp Excel có sẵn dòng tiêu đề đúng định dạng. '
                 'Điền dữ liệu vào tệp này, đừng tự tạo tệp mới với tiêu đề khác.')
        b.bullet('Bước 2: Bấm Chọn file Excel và chọn tệp vừa điền, rồi bấm Load lên bảng. '
                 'Nội dung tệp hiện lên bảng xem trước để bạn đối chiếu.')
        b.bullet('Bước 3: Bấm Validate. Hệ thống kiểm tra từng dòng, đánh dấu dòng sai kèm mô '
                 'tả lỗi và khóa lại các dòng hợp lệ. Tích ô Chỉ dòng lỗi để xem nhanh những '
                 'dòng cần sửa.')
        b.bullet('Bước 4: Bấm Import để ghi các dòng hợp lệ vào danh mục. Hệ thống báo lại số '
                 'dòng thành công và số dòng bị bỏ qua.')
        b.para('Lưu ý khi nhập từ Excel:')
        b.bullet('Chưa bấm Validate thì nút Import chưa dùng được — đây là ràng buộc cố ý để '
                 'bạn không ghi nhầm dữ liệu sai.')
        b.bullet('Hệ thống chỉ ghi các dòng hợp lệ. Dòng lỗi vẫn nằm trên bảng để bạn sửa lại '
                 'rồi kiểm tra và nhập tiếp.')
        b.bullet('Bấm Làm mới để xóa trắng bảng và bắt đầu lại từ đầu.')
        b.bullet('Chọn nhầm tệp sai cấu trúc cột thì hệ thống báo lỗi định dạng và không đổ dữ '
                 'liệu lên bảng.')

    # ---------------------------------------------------------------- 11
    def _xuat(self, h2):
        b, c = self.b, self.c
        h2('Xuất danh sách ra Excel')
        b.para('Bấm nút Xuất Excel ở thanh công cụ phía trên bảng.')
        if 'xuat' in c['shots']:
            b.image(self.shot('xuat'), 'Cửa sổ chọn trường xuất file')
        b.para('Các bước thực hiện:')
        b.bullet('Bước 1: Cửa sổ mở ra với tất cả các trường được chọn sẵn. Bỏ chọn những '
                 'trường bạn không cần.')
        b.bullet('Bước 2: Kiểm tra dòng “Thứ tự cột trong file” — đây chính là thứ tự cột sẽ có '
                 'trong tệp. Muốn đổi vị trí thì bỏ chọn hết rồi chọn lại theo trình tự mong muốn.')
        b.bullet('Bước 3: Bấm Xuất file. Tệp được tải về máy bạn.')
        b.para('Lưu ý khi xuất:')
        b.bullet('Tệp xuất ra lấy đúng bộ lọc bạn đang áp dụng trên danh sách. Muốn xuất toàn '
                 'bộ danh mục thì bấm Làm mới để xóa hết tiêu chí lọc trước khi xuất.')
        b.bullet('Không chọn trường nào thì nút Xuất file không bấm được.')
        for extra in c.get('hdsd_xuat_them', []):
            b.bullet(extra)

    # ---------------------------------------------------------------- 12
    def _in(self, h2):
        b, c = self.b, self.c
        h2('In danh sách')
        b.para('Bấm nút In danh sách ở thanh công cụ. Hệ thống mở một thẻ trình duyệt mới chứa '
               'bản in đã dàn trang sẵn.')
        if 'in' in c['shots']:
            b.image(self.shot('in'), 'Bản in danh sách')
        b.para('Tại thẻ mới, dùng chức năng in của trình duyệt để gửi máy in hoặc lưu thành tệp PDF.')
        b.para('Lưu ý khi in:')
        b.bullet('Bản in lấy đúng bộ lọc và bộ cột đang hiển thị trên màn danh sách. Muốn in '
                 'thêm cột nào thì bật cột đó lên trước khi bấm In.')
        b.bullet('Nếu bản in quá rộng, hãy tắt bớt cột hoặc chọn khổ giấy ngang trong hộp thoại '
                 'in của trình duyệt.')

    # ---------------------------------------------------------------- 13
    def _hienthi(self, h2):
        b, c = self.b, self.c
        h2('Tùy chỉnh cách hiển thị')
        if self.has('columns'):
            b.para('Chọn cột muốn thấy trên bảng:')
            if 'cot' in c['shots']:
                b.image(self.shot('cot'), 'Cửa sổ Tuỳ chỉnh cột hiển thị')
            b.bullet('Bấm biểu tượng tùy chỉnh cột ở cuối thanh công cụ.')
            b.bullet('Tích chọn cột muốn hiện, bỏ tích cột muốn ẩn, rồi bấm Lưu.')
            b.bullet('Một số cột bắt buộc như STT và Hành động luôn hiển thị, không bỏ tích được.')
            b.bullet('Cấu hình được lưu riêng cho tài khoản của bạn, lần vào sau vẫn giữ nguyên.')
        if self.has('fcfg'):
            b.para('Chọn ô lọc muốn thấy:')
            if 'caidat_boloc' in c['shots']:
                b.image(self.shot('caidat_boloc'), 'Cửa sổ Cài đặt bộ lọc')
            b.bullet('Bấm nút Cài đặt bộ lọc ở góc phải khu vực tìm kiếm.')
            b.bullet('Tích chọn ô lọc muốn dùng; kéo tay nắm để đổi thứ tự các ô, rồi bấm Lưu.')
            b.bullet('Bấm Khôi phục mặc định nếu muốn đưa bộ lọc về như ban đầu.')

    # ---------------------------------------------------------------- 14
    def _faq(self, h2):
        b, c = self.b, self.c
        h2('Câu hỏi thường gặp')
        b.table([['Tình huống', 'Giải thích và cách xử lý']] + c['hdsd_faq'])
