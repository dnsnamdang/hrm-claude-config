# -*- coding: utf-8 -*-
"""Sinh 3 file testcase cho nhom danh muc Tai chinh.

Chay:  python .plans/gop-db/finance-catalogs-docs/gen_testcase.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
sys.path.insert(0, HERE)
from tc_engine import build  # noqa: E402
from fin_config import SCREENS  # noqa: E402


def desc_block(cfg):
    ten, dt, quyen = cfg['ten'], cfg['doi_tuong'], cfg['quyen']
    ma_hay_ten = 'Mã' if cfg['co_ma'] else 'Tên'

    if cfg['co_trangthai']:
        m2 = ('- Toàn bộ %s trong danh mục, gồm CẢ bản ghi Hoạt động lẫn bản ghi đã Khóa.\n'
              '- Bộ lọc Trạng thái để trống thì hiện cả hai nhóm.' % dt)
        m3 = ('- Không ẩn bản ghi nào theo mặc định.\n'
              '- Bản ghi Khóa KHÔNG còn chọn được khi lập bút toán mới, nhưng vẫn nằm trong '
              'danh mục này.')
    else:
        m2 = '- Toàn bộ %s còn hiệu lực. Màn hình KHÔNG có cột Trạng thái.' % dt
        m3 = ('- Bản ghi đã bị Xóa không còn xuất hiện. Trên màn này, xóa được xử lý thành '
              'ngừng sử dụng: bản ghi biến mất khỏi danh sách nhưng dữ liệu không mất hẳn.')

    m9 = ['Các bẫy dễ sai nhất của màn này, QA đọc trước khi test:',
          '- ⚠️ Màn hình chỉ có MỘT quyền "%s" cho cả xem lẫn sửa. Không có quyền thì không vào '
          'được màn hình, chứ không phải vào được mà nút bị mờ.' % quyen,
          '- ⚠️ Cửa sổ nhập liệu chỉ có 2 nút: Lưu và Đóng. Màn này KHÔNG có nút '
          '"Lưu và tiếp tục" như nhóm danh mục địa lý.']
    if cfg['co_ma']:
        m9 += ['- ⚠️ Ràng buộc duy nhất áp cho %s, KHÔNG áp cho tên. Hai bản ghi khác mã được '
               'phép trùng tên — đừng báo lỗi nhầm.' % ma_hay_ten.lower(),
               '- ⚠️ Nút Xóa CHỈ hiện với bản ghi %s. Bản ghi đã dùng ở bút toán thì KHÔNG có '
               'nút Xóa; muốn ngừng dùng phải mở cửa sổ Sửa rồi chuyển Trạng thái sang Khóa.'
               % cfg['dieu_kien_xoa'],
               '- ⚠️ Màn này KHÔNG có nút Khóa riêng trên cột Hành động. Đổi trạng thái làm '
               'trong cửa sổ Sửa.']
    else:
        m9 += ['- ⚠️ Màn này chỉ có ĐÚNG MỘT ô nhập là Tên nguồn vốn. Không có mã, không có ghi '
               'chú, không có trạng thái.',
               '- ⚠️ Màn này KHÔNG có bộ lọc nâng cao, chỉ có ô tìm kiếm nhanh.',
               '- ⚠️ Xóa ở màn này là ngừng sử dụng, không xóa hẳn. Chứng từ cũ vẫn hiện đúng '
               'tên nguồn vốn.']
    m9.append('- ⚠️ Trạng thái mặc định của bản ghi mới là Hoạt động (nếu màn có trạng thái).')

    return [
        ('1. Mục đích tính năng',
         'Quản lý danh mục %s dùng cho nghiệp vụ kế toán. Màn hình cho phép tra cứu, tìm kiếm, '
         'thêm mới, chỉnh sửa, xóa và xem lịch sử thay đổi. Dữ liệu của màn này được chọn khi '
         'lập bút toán kế toán.' % dt),
        ('2. Đối tượng được tính / hiển thị', m2),
        ('3. Đối tượng bị ẩn / không tính', m3),
        ('4. Bộ lọc thời gian áp dụng cho',
         'Màn hình KHÔNG có bộ lọc khoảng thời gian. Yếu tố thời gian chỉ xuất hiện ở cột Ngày '
         'tạo (sắp xếp được), cột Ngày cập nhật (mặc định ẩn) và cửa sổ Lịch sử thay đổi.'),
        ('5. Cấu trúc dữ liệu / cây phân cấp',
         '- Danh mục phẳng, không phân cấp cha con.\n'
         '- Mỗi %s là một bản ghi độc lập.\n'
         '- Bản ghi được tham chiếu từ các bút toán kế toán; đây là căn cứ quyết định có xóa '
         'được hay không.' % dt),
        ('6. Quy tắc cộng dồn / deduplicate',
         '- Mỗi %s chỉ hiện MỘT dòng.\n'
         '- %s là duy nhất toàn hệ thống — trùng sẽ bị chặn khi lưu với thông báo "%s".\n'
         '- Khi sửa, bản ghi đang sửa được loại khỏi phép kiểm tra trùng: giữ nguyên giá trị của '
         'chính nó thì lưu bình thường.'
         % (dt, ma_hay_ten + ' ' + dt, cfg['loi_trung'])),
        ('7. Phân quyền cấp',
         'Màn hình dùng đúng MỘT quyền: "%s".\n'
         '- Có quyền: mở được màn hình và thực hiện đầy đủ Thêm mới, Chỉnh sửa, Xóa, Xem lịch sử.\n'
         '- Không có quyền: mục menu không hiển thị; truy cập thẳng đường dẫn thì hệ thống từ '
         'chối và báo không có quyền.\n'
         'Màn hình KHÔNG tách quyền xem riêng, cũng không phân quyền theo cấp công ty / phòng '
         'ban / bộ phận.' % quyen),
        ('8. Cách tính các ô thống kê',
         '- Ô hiển thị tổng số bản ghi ở cuối lưới: là TỔNG số %s khớp bộ lọc đang áp dụng, '
         'không phải tổng toàn danh mục.\n'
         '- Số thứ tự chạy liên tục qua các trang.' % dt),
        ('9. Ghi chú đọc bảng', '\n'.join(m9)),
    ]


def sections(cfg):
    ten, dt, quyen = cfg['ten'], cfg['doi_tuong'], cfg['quyen']
    truong = cfg['truong']
    bb = [t for t in truong if t[3] == 'Có']
    ten_truong = truong[0][0]
    ma_field = truong[0][0] if cfg['co_ma'] else None

    # ------------------------------------------------ TC phân quyền
    role = [
        ('00', 'Có quyền thì mở được màn hình', 'P0',
         'Tài khoản T1 được gán quyền "%s".' % quyen,
         '1. Đăng nhập bằng T1\n2. Vào menu Tài chính → Danh mục → %s' % ten,
         'Tài khoản: T1',
         '- Mục menu hiển thị\n- Mở được màn hình, thấy danh sách và nút Tạo mới'),
        ('01', 'Không có quyền thì không thấy menu', 'P0',
         'Tài khoản T2 KHÔNG được gán quyền "%s".' % quyen,
         '1. Đăng nhập bằng T2\n2. Mở phân hệ Tài chính, tìm mục menu %s' % ten,
         'Tài khoản: T2',
         '- ⚠️ Mục menu KHÔNG hiển thị với T2'),
        ('02', 'Không có quyền, truy cập thẳng đường dẫn', 'P0',
         'Tài khoản T2 KHÔNG có quyền "%s".' % quyen,
         '1. Đăng nhập bằng T2\n2. Gõ thẳng đường dẫn %s vào thanh địa chỉ' % cfg['route'],
         'Tài khoản: T2',
         '- Hệ thống từ chối, báo không có quyền\n- Không hiện dữ liệu của danh mục'),
        ('03', 'Chặn thêm mới khi bỏ qua giao diện', 'P0',
         'Tài khoản T2 KHÔNG có quyền "%s".' % quyen,
         '1. Đăng nhập bằng T2, lấy phiên đăng nhập\n'
         '2. Dùng công cụ kiểm thử gọi thẳng chức năng Thêm mới, bỏ qua giao diện\n'
         '3. Kiểm tra lại danh mục bằng tài khoản có quyền',
         'Tài khoản: T2',
         '- Hệ thống từ chối, báo không có quyền\n- ⚠️ Không có bản ghi mới nào được tạo'),
        ('04', 'Chặn chỉnh sửa khi bỏ qua giao diện', 'P0',
         'Tài khoản T2 KHÔNG có quyền "%s". Bản ghi A đang có tên "Tên gốc".' % quyen,
         '1. Đăng nhập bằng T2\n'
         '2. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa cho A, đổi tên\n'
         '3. Mở lại A bằng tài khoản có quyền',
         'Tài khoản: T2',
         '- Hệ thống từ chối, báo không có quyền\n- Tên A vẫn là "Tên gốc"'),
        ('05', 'Chặn xóa khi bỏ qua giao diện', 'P0',
         'Tài khoản T2 KHÔNG có quyền "%s". Bản ghi B đang có trong danh mục.' % quyen,
         '1. Đăng nhập bằng T2\n'
         '2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa cho B\n'
         '3. Kiểm tra lại danh mục',
         'Tài khoản: T2',
         '- Hệ thống từ chối, báo không có quyền\n- B vẫn còn trong danh mục'),
    ]

    # ------------------------------------------------ I. HIỂN THỊ
    sec1 = [
        (1, 'Mở màn hình từ menu', 'P0',
         'Tài khoản có quyền "%s". Danh mục có sẵn dữ liệu.' % quyen,
         '1. Đăng nhập\n2. Vào menu Tài chính → Danh mục → %s' % ten, '—',
         '- Tiêu đề trang hiện "%s"\n- Lưới nạp xong và hiện dữ liệu\n'
         '- Có nút Tạo mới trên thanh công cụ' % ten),
        (2, 'Kiểm tra đủ các cột của lưới', 'P0',
         'Người dùng chưa chỉnh cấu hình cột.',
         '1. Mở màn hình\n2. Đọc tên từng tiêu đề cột', '—',
         '- Có đủ các cột: %s\n- ⚠️ Các cột ghi "mặc định ẩn" KHÔNG xuất hiện'
         % ', '.join(c[0] for c in cfg['cot'])),
        (3, 'Hiển thị khi không có dữ liệu khớp', 'P1',
         'Danh mục có dữ liệu bình thường.',
         '1. Gõ vào ô tìm kiếm một chuỗi chắc chắn không tồn tại\n2. Chờ lưới nạp lại',
         'Từ khóa: zzzkhongtontai999',
         '- Lưới hiện thông báo không có dữ liệu\n- Không báo lỗi kỹ thuật'),
        (4, 'Số thứ tự liên tục qua các trang', 'P0',
         'Danh mục có nhiều hơn một trang dữ liệu.',
         '1. Ghi lại số thứ tự dòng cuối trang 1\n2. Sang trang 2, đọc số thứ tự dòng đầu', '—',
         '- Số thứ tự nối tiếp liền mạch, không quay về 1'),
        (5, 'Sắp xếp theo cột %s' % ten_truong, 'P0',
         'Danh mục có ít nhất 5 bản ghi.',
         '1. Bấm tiêu đề cột %s\n2. Đọc 5 dòng đầu\n3. Bấm lần thứ hai' % ten_truong, '—',
         '- Lần 1: xếp tăng dần\n- Lần 2: thứ tự đảo ngược hoàn toàn'),
        (6, 'Sắp xếp theo Ngày tạo', 'P1',
         'Danh mục có bản ghi tạo ở nhiều thời điểm.',
         '1. Bấm tiêu đề cột Ngày tạo hai lần để lấy giảm dần\n2. Đọc 5 dòng đầu', '—',
         '- Bản ghi tạo gần đây nhất đứng đầu'),
        (7, 'Đổi số dòng mỗi trang', 'P1',
         'Đang hiển thị số dòng mặc định.',
         '1. Đổi ô số dòng mỗi trang sang giá trị lớn hơn\n2. Đếm số dòng', '—',
         '- Lưới hiện đúng số dòng đã chọn\n- ⚠️ Sau khi đổi phải quay về trang 1'),
    ]
    if cfg['co_trangthai']:
        sec1.append(
            (8, 'Cột Trạng thái phân biệt Hoạt động và Khóa', 'P0',
             'Có ít nhất 1 bản ghi Hoạt động và 1 bản ghi đã Khóa.',
             '1. Mở màn hình\n2. Đọc cột Trạng thái của cả hai bản ghi', '—',
             '- Hai trạng thái hiện đúng chữ và khác màu rõ ràng\n'
             '- ⚠️ Cả hai đều nằm trong danh sách'))
    else:
        sec1.append(
            (8, 'Màn hình không có cột Trạng thái', 'P1',
             'Đang ở màn %s.' % ten,
             '1. Đọc toàn bộ tiêu đề cột\n2. Mở cửa sổ Tạo mới', '—',
             '- ⚠️ Lưới KHÔNG có cột Trạng thái\n'
             '- ⚠️ Cửa sổ nhập liệu cũng KHÔNG có ô Trạng thái'))

    # ------------------------------------------------ II. TÌM KIẾM
    sec2 = [
        (1, 'Tìm nhanh theo tên', 'P0',
         'Có bản ghi tên chứa đoạn cần tìm.',
         '1. Gõ một phần tên vào ô tìm kiếm\n2. Chờ lưới nạp lại', 'Từ khóa: (một phần tên)',
         '- Chỉ còn các bản ghi có tên chứa từ khóa'),
        (2, 'Xóa từ khóa thì danh sách quay về đầy đủ', 'P0',
         'Đang tìm với từ khóa cho ra ít kết quả.',
         '1. Xóa hết nội dung ô tìm kiếm\n2. Chờ lưới nạp lại', '—',
         '- Tổng số bản ghi quay lại như ban đầu\n- Lưới về trang 1'),
        (3, 'Nút Làm mới xóa hết tiêu chí và nạp lại', 'P0',
         'Đang áp dụng các tiêu chí lọc của màn.',
         '1. Bấm nút Làm mới\n2. Quan sát các ô lọc và lưới', '—',
         '- Tất cả ô lọc trở về rỗng\n- ⚠️ Lưới PHẢI nạp lại ngay'),
        (4, 'Áp dụng bộ lọc khi đang ở trang giữa', 'P0',
         'Đang ở trang 3. Bộ lọc mới chỉ cho ra vài kết quả.',
         '1. Áp dụng bộ lọc\n2. Quan sát lưới', '—',
         '- ⚠️ Lưới quay về trang 1, không hiện trang trống'),
    ]
    if cfg['co_ma']:
        sec2.insert(1, (
            5, 'Tìm nhanh theo mã', 'P0',
            'Có bản ghi mã "ABC123".',
            '1. Gõ ABC123 vào ô tìm kiếm\n2. Chờ lưới nạp lại', 'Từ khóa: ABC123',
            '- Ra đúng bản ghi có mã ABC123'))
    n = 6
    for f in cfg['loc'][1:]:
        sec2.append(
            (n, 'Lọc theo %s' % f[0], 'P0' if n == 6 else 'P1',
             'Có bản ghi thỏa giá trị lọc sẽ chọn.',
             '1. Mở Tìm kiếm nâng cao\n2. Chọn %s\n3. Bấm Tìm kiếm' % f[0],
             '%s: (một giá trị có dữ liệu)' % f[0],
             '- Mọi dòng trả về đều khớp giá trị đã chọn'))
        n += 1
    if len(cfg['loc']) == 1:
        sec2.append(
            (n, 'Màn hình không có bộ lọc nâng cao', 'P1',
             'Đang ở màn %s.' % ten,
             '1. Quan sát khu vực bộ lọc phía trên lưới', '—',
             '- ⚠️ Chỉ có ô tìm kiếm nhanh, KHÔNG có panel lọc nâng cao\n'
             '- Đây là thiết kế của màn này, không phải thiếu chức năng'))

    # ------------------------------------------------ III. THÊM MỚI
    sec3 = [
        (1, 'Mở cửa sổ thêm mới', 'P0',
         'Đang ở màn %s.' % ten,
         '1. Bấm nút Tạo mới\n2. Quan sát cửa sổ', '—',
         '- Cửa sổ mở với tiêu đề "Tạo %s"\n'
         '- Có đúng %d ô nhập\n'
         '- ⚠️ Chỉ có 2 nút: Lưu và Đóng' % (dt, len(truong))),
        (2, 'Thêm mới đủ trường bắt buộc', 'P0',
         'Đã chuẩn bị giá trị hợp lệ, chưa tồn tại trong danh mục.',
         '1. Bấm Tạo mới\n2. Nhập đủ: %s\n3. Bấm Lưu' % ', '.join(t[0] for t in bb),
         '(giá trị hợp lệ cho từng ô bắt buộc)',
         '- Lưu thành công, hiện thông báo thành công\n'
         '- Cửa sổ đóng, danh sách nạp lại và có bản ghi mới'),
    ]
    n = 3
    for t in bb:
        sec3.append(
            (n, 'Thiếu %s thì bị chặn' % t[0], 'P0',
             'Đang ở cửa sổ thêm mới, các ô khác đã nhập hợp lệ.',
             '1. Để trống ô %s\n2. Bấm Lưu' % t[0], '%s: (để trống)' % t[0],
             '- Báo lỗi đỏ ngay dưới ô %s: "Bắt buộc phải nhập"\n'
             '- Cửa sổ KHÔNG đóng, dữ liệu đã nhập vẫn còn' % t[0]))
        n += 1
    sec3.append(
        (n, 'Trùng %s bị chặn' % ('mã' if cfg['co_ma'] else 'tên'), 'P0',
         'Danh mục đã có bản ghi %s "X".' % ('mã' if cfg['co_ma'] else 'tên'),
         '1. Thêm mới với %s "X"\n2. Bấm Lưu' % ('mã' if cfg['co_ma'] else 'tên'),
         '%s: X' % ('Mã' if cfg['co_ma'] else 'Tên'),
         '- Báo lỗi "%s"\n- Không tạo ra bản ghi mới' % cfg['loi_trung']))
    n += 1
    if cfg['co_ma']:
        sec3.append(
            (n, 'Trùng TÊN nhưng khác mã thì lưu được', 'P0',
             'Danh mục đã có bản ghi tên "Tên chung", mã khác.',
             '1. Thêm mới với tên "Tên chung" và mã chưa tồn tại\n2. Bấm Lưu',
             'Tên: Tên chung',
             '- ⚠️ LƯU ĐƯỢC — ràng buộc duy nhất chỉ áp cho mã, không áp cho tên'))
        n += 1
        sec3.append(
            (n, 'Trạng thái mặc định khi thêm mới', 'P0',
             'Đang ở cửa sổ thêm mới.',
             '1. Quan sát ô Trạng thái trước khi nhập gì', '—',
             '- ⚠️ Ô Trạng thái đặt sẵn là Hoạt động'))
        n += 1
        sec3.append(
            (n, 'Thêm mới với Trạng thái Khóa', 'P1',
             'Đang ở cửa sổ thêm mới.',
             '1. Nhập đủ trường bắt buộc\n2. Đổi Trạng thái sang Khóa\n3. Bấm Lưu\n'
             '4. Xem cột Trạng thái trên lưới', 'Trạng thái: Khóa',
             '- Bản ghi được tạo với trạng thái Khóa\n'
             '- Không chọn được bản ghi này khi lập bút toán mới'))
        n += 1
        sec3.append(
            (n, 'Ghi chú để trống vẫn lưu được', 'P1',
             'Đang ở cửa sổ thêm mới.',
             '1. Nhập đủ trường bắt buộc, để trống Ghi chú\n2. Bấm Lưu', 'Ghi chú: (để trống)',
             '- Lưu thành công, không báo lỗi ô Ghi chú'))
        n += 1
    sec3.append(
        (n, 'Bấm Đóng thì không ghi gì', 'P0',
         'Đang ở cửa sổ thêm mới, đã nhập đủ trường bắt buộc.',
         '1. Bấm Đóng\n2. Xem danh sách', '—',
         '- Cửa sổ đóng, KHÔNG có bản ghi mới nào được tạo'))
    n += 1
    sec3.append(
        (n, 'Bấm Lưu hai lần liên tiếp', 'P0',
         'Đang ở cửa sổ thêm mới, đã nhập đủ trường bắt buộc.',
         '1. Bấm Lưu\n2. Bấm Lưu lần hai thật nhanh\n3. Xem danh sách', '—',
         '- ⚠️ Chỉ tạo ra ĐÚNG MỘT bản ghi'))

    # ------------------------------------------------ IV. SỬA
    sec4 = [
        (1, 'Mở cửa sổ sửa', 'P0',
         'Có bản ghi trong danh sách.',
         '1. Bấm biểu tượng bút chì ở dòng đó\n2. Quan sát cửa sổ', '—',
         '- Cửa sổ mở với mọi ô đã điền sẵn dữ liệu hiện tại'),
        (2, 'Sửa và lưu thành công', 'P0',
         'Bản ghi A đang có tên "Tên cũ".',
         '1. Mở cửa sổ sửa A\n2. Đổi tên thành "Tên mới"\n3. Bấm Lưu\n4. Xem lưới',
         'Tên mới: Tên mới',
         '- Lưu thành công, cột tên trên lưới đổi theo'),
        (3, 'Giữ nguyên %s của chính mình khi sửa'
            % ('mã' if cfg['co_ma'] else 'tên'), 'P0',
         'Bản ghi A có %s "X".' % ('mã' if cfg['co_ma'] else 'tên'),
         '1. Mở cửa sổ sửa A\n2. KHÔNG đổi %s, chỉ đổi ô khác\n3. Bấm Lưu'
         % ('mã' if cfg['co_ma'] else 'tên'),
         '%s: giữ nguyên X' % ('Mã' if cfg['co_ma'] else 'Tên'),
         '- ⚠️ LƯU ĐƯỢC, không báo lỗi trùng với chính mình'),
        (4, 'Sửa trùng %s với bản ghi khác' % ('mã' if cfg['co_ma'] else 'tên'), 'P0',
         'Bản ghi A có %s "X", bản ghi B có %s "Y".'
         % (('mã', 'mã') if cfg['co_ma'] else ('tên', 'tên')),
         '1. Mở cửa sổ sửa B\n2. Đổi %s thành "X"\n3. Bấm Lưu'
         % ('mã' if cfg['co_ma'] else 'tên'),
         '%s: X' % ('Mã' if cfg['co_ma'] else 'Tên'),
         '- Báo lỗi "%s", không lưu' % cfg['loi_trung']),
        (5, 'Để trống trường bắt buộc khi sửa', 'P0',
         'Đang mở cửa sổ sửa một bản ghi.',
         '1. Xóa trắng ô %s\n2. Bấm Lưu' % ten_truong, '(để trống)',
         '- Báo lỗi "Bắt buộc phải nhập", không lưu'),
        (6, 'Sửa xong ghi vào lịch sử', 'P0',
         'Vừa đổi tên một bản ghi từ "A" thành "B".',
         '1. Mở Lịch sử của bản ghi đó\n2. Đọc dòng trên cùng', '—',
         '- Có dòng ghi nhận lần sửa, nêu giá trị cũ "A" và giá trị mới "B"\n'
         '- Kèm người thực hiện và thời điểm'),
        (7, 'Bấm Đóng khi đang sửa thì không ghi gì', 'P0',
         'Đang mở cửa sổ sửa và đã đổi tên.',
         '1. Bấm Đóng\n2. Xem lại lưới', '—', '- Tên trên lưới KHÔNG đổi'),
    ]
    if cfg['co_trangthai']:
        sec4.append(
            (8, 'Đổi trạng thái sang Khóa qua cửa sổ Sửa', 'P0',
             'Bản ghi A đang Hoạt động.',
             '1. Mở cửa sổ sửa A\n2. Đổi Trạng thái sang Khóa\n3. Bấm Lưu\n'
             '4. Xem cột Trạng thái', 'Trạng thái: Khóa',
             '- Cột Trạng thái đổi thành Khóa\n'
             '- ⚠️ Màn này KHÔNG có nút Khóa riêng — đổi trạng thái làm trong cửa sổ Sửa'))
        sec4.append(
            (9, 'Bản ghi Khóa không chọn được khi lập bút toán', 'P0',
             'Bản ghi A vừa chuyển sang Khóa.',
             '1. Mở màn lập bút toán kế toán\n2. Tìm A ở ô chọn %s' % dt, '—',
             '- A KHÔNG xuất hiện trong danh sách chọn'))

    # ------------------------------------------------ V. XÓA
    sec5 = [
        (1, 'Hộp xác nhận nêu đúng tên bản ghi', 'P0',
         'Có bản ghi tên "X" và đang xóa được.',
         '1. Bấm biểu tượng thùng rác ở dòng đó\n2. Đọc nội dung hộp xác nhận', '—',
         '- Hộp hiện câu "Bạn có chắc muốn xóa %s \\"X\\"?"\n- Có hai nút Xóa và Hủy' % dt),
        (2, 'Bấm Hủy thì không xóa', 'P0',
         'Đang mở hộp xác nhận xóa.',
         '1. Bấm Hủy\n2. Xem lại lưới', '—',
         '- Hộp đóng, bản ghi vẫn còn nguyên'),
        (3, 'Xóa thành công', 'P0',
         'Bản ghi X đang xóa được.',
         '1. Bấm thùng rác ở dòng X\n2. Bấm Xóa xác nhận\n3. Xem lưới', '—',
         '- Thông báo xóa thành công\n- Bản ghi X biến mất khỏi danh sách'),
    ]
    if cfg['dieu_kien_xoa']:
        sec5.append(
            (4, 'Bản ghi đã phát sinh bút toán thì KHÔNG có nút Xóa', 'P0',
             'Bản ghi Y đã được dùng trong ít nhất một bút toán kế toán.',
             '1. Tìm dòng Y\n2. Quan sát cột Hành động', '—',
             '- ⚠️ Chỉ có Sửa và Lịch sử, KHÔNG có biểu tượng thùng rác\n'
             '- Đây là thiết kế, không phải lỗi thiếu nút'))
        sec5.append(
            (5, 'Bản ghi chưa phát sinh bút toán thì CÓ nút Xóa', 'P0',
             'Bản ghi Z vừa được tạo, chưa dùng ở bút toán nào.',
             '1. Tìm dòng Z\n2. Quan sát cột Hành động', '—',
             '- Có đủ ba nút: Sửa, Xóa và Lịch sử'))
        sec5.append(
            (6, 'Chặn xóa bản ghi đã phát sinh khi bỏ qua giao diện', 'P0',
             'Bản ghi Y đã được dùng trong bút toán kế toán.',
             '1. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa cho Y\n2. Kiểm tra danh mục', '—',
             '- Hệ thống từ chối và nêu lý do\n- Y vẫn còn trong danh mục'))
    else:
        sec5.append(
            (4, 'Xóa là ngừng sử dụng, không mất dữ liệu', 'P0',
             'Bản ghi X đang được một chứng từ cũ tham chiếu.',
             '1. Xóa X\n2. Mở chứng từ cũ đang dùng X\n3. Đọc tên nguồn vốn trên chứng từ', '—',
             '- X biến mất khỏi danh mục\n'
             '- ⚠️ Chứng từ cũ VẪN hiển thị đúng tên X, không bị trống'))

    # ------------------------------------------------ VI. LỊCH SỬ
    sec6 = [
        (1, 'Mở cửa sổ Lịch sử', 'P0',
         'Bản ghi X đã được sửa ít nhất 1 lần.',
         '1. Bấm biểu tượng lịch sử ở dòng X\n2. Quan sát cửa sổ', '—',
         '- Cửa sổ "Lịch sử thay đổi" mở ra\n'
         '- Dòng phụ ghi rõ loại đối tượng và tên X\n- Có bộ lọc riêng'),
        (2, 'Thứ tự mới nhất ở trên cùng', 'P0',
         'Bản ghi X đã được sửa 3 lần vào 3 thời điểm khác nhau.',
         '1. Mở Lịch sử của X\n2. Đọc thời điểm 3 dòng từ trên xuống', '—',
         '- ⚠️ Dòng trên cùng là lần sửa MỚI NHẤT'),
        (3, 'Mỗi dòng nêu đủ thông tin', 'P0',
         'Vừa đổi tên bản ghi X từ "A" thành "B".',
         '1. Mở Lịch sử của X\n2. Đọc dòng trên cùng', '—',
         '- Nêu rõ trường đã đổi, giá trị cũ "A", giá trị mới "B"\n'
         '- Kèm tên người thực hiện và thời điểm tới phút'),
        (4, 'Bản ghi chưa từng sửa', 'P1',
         'Bản ghi Y vừa được tạo, chưa sửa lần nào.',
         '1. Mở Lịch sử của Y', '—',
         '- Cửa sổ hiện "Chưa có lịch sử thao tác nào."\n- Không báo lỗi'),
        (5, 'Đóng cửa sổ Lịch sử', 'P2',
         'Đang mở cửa sổ Lịch sử, danh sách phía sau đang lọc và ở trang 2.',
         '1. Bấm Đóng', '—',
         '- Cửa sổ đóng, danh sách giữ nguyên bộ lọc và trang 2'),
    ]

    return [
        ('I', 'HIỂN THỊ TRANG & TRUY CẬP', sec1),
        ('II', 'TÌM KIẾM & LỌC DANH SÁCH', sec2),
        ('III', 'THÊM MỚI', sec3),
        ('IV', 'CHỈNH SỬA', sec4),
        ('V', 'XÓA', sec5),
        ('VI', 'LỊCH SỬ THAY ĐỔI', sec6),
    ], role


if __name__ == '__main__':
    tong = 0
    for cfg in SCREENS:
        secs, role = sections(cfg)
        out = os.path.join(HERE, 'testcase - %s.xlsx' % cfg['ten'].replace('/', '-'))
        n = build(output_file=out, sheet_name='Trang tính1',
                  feature_name='%s - Cập nhật ngày 17/08/2026' % cfg['ten'],
                  module_name=cfg['ten'],
                  description_block=desc_block(cfg),
                  role_tcs=role, sections=secs)
        tong += n
    print('TONG TC 3 MAN:', tong)
