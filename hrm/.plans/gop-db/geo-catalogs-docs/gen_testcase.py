# -*- coding: utf-8 -*-
"""Sinh 6 file testcase cho nhom danh muc dia ly.

Chay:  python .plans/gop-db/geo-catalogs-docs/gen_testcase.py
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
from srs_geo_config import SCREENS  # noqa: E402


def desc_block(cfg):
    ten, dt, co_khoa = cfg['ten'], cfg['doi_tuong'], cfg['co_khoa']
    truong_bb = [t[0] for t in cfg['truong'] if t[3].startswith('Có')]

    if co_khoa:
        m2 = ("- Toàn bộ %s trong danh mục, gồm CẢ bản ghi Hoạt động lẫn bản ghi đã Khóa.\n"
              "- Bộ lọc trạng thái để trống thì hiện cả hai nhóm; đây là mặc định khi vào màn.\n"
              "- Bản ghi đã Khóa vẫn xem được chi tiết và lịch sử." % dt)
        m3 = ("- Không ẩn bản ghi nào theo mặc định.\n"
              "- Bản ghi đã Khóa KHÔNG còn xuất hiện ở ô chọn %s của các màn nghiệp vụ khác — "
              "nhưng vẫn nằm trong danh mục này." % dt)
    else:
        m2 = ("- Chỉ %s còn hiệu lực. Màn hình này KHÔNG có cột Trạng thái.\n"
              "- Phép lọc bản ghi còn hiệu lực nằm ở phía máy chủ, người dùng không đổi được."
              % dt)
        m3 = ("- Bản ghi đã bị Xóa không còn xuất hiện. Trên màn này, xóa được xử lý thành "
              "ngừng sử dụng: bản ghi biến mất khỏi danh sách nhưng dữ liệu không mất hẳn.\n"
              "- Không có bản ghi nào bị ẩn vì lý do phân quyền, do màn hình chưa gắn quyền.")

    m5 = ('- Quốc gia là gốc của cây địa chỉ: Quốc gia → Khu vực → Tỉnh/TP → Quận/Huyện → '
          'Phường/Xã → Đường/Phố.\n'
          '- Màn này quản lý cấp %s.' % dt)
    if cfg['cap_tren']:
        m5 += '\n- Mỗi %s bắt buộc trực thuộc %s.' % (dt, cfg['cap_tren'])
    else:
        m5 += '\n- Quốc gia không trực thuộc cấp nào.'
    if cfg['key'] == 'hamlets':
        m5 += ('\n- ⚠️ Riêng màn này: chọn Quốc gia là Việt Nam thì ô Quận/Huyện/Thị xã BỊ ẨN; '
               'quốc gia khác thì hiện và bắt buộc nhập.')

    m9 = ['Các bẫy dễ sai nhất của màn này, QA đọc trước khi test:',
          '- ⚠️ Màn hình KHÔNG gắn quyền. Mọi tài khoản đăng nhập đều thêm, sửa, xóa được. '
          'Không có trường hợp test "thiếu quyền thì nút bị ẩn" như các màn danh mục khác.',
          '- ⚠️ Trùng tên xét %s, không phải toàn hệ thống — test đúng phạm vi này.'
          % cfg['pham_vi_trung'],
          '- ⚠️ Cửa sổ thêm mới có 3 nút: Lưu, Lưu và tiếp tục, Đóng. Nút "Lưu và tiếp tục" GIỮ '
          'cửa sổ mở và xóa trắng các ô để nhập tiếp bản ghi kế theo.']
    if co_khoa:
        m9 += ['- ⚠️ Sau khi Khóa, hai nút Sửa và Xóa của dòng đó BIẾN MẤT, chỉ còn Mở khóa và '
               'Lịch sử. Đây là thiết kế, không phải lỗi.',
               '- ⚠️ Khóa KHÔNG phải Xóa: bản ghi vẫn nằm trong danh sách với nhãn Khóa.',
               '- ⚠️ Nút Khóa/Mở khóa và Lịch sử nằm trong nút ba chấm "Hành động khác", không '
               'hiện thẳng như Sửa và Xóa.']
    else:
        m9 += ['- ⚠️ Màn này KHÔNG có cột Trạng thái và KHÔNG có thao tác Khóa/Mở khóa. '
               'Đừng báo lỗi thiếu chức năng.',
               '- ⚠️ Nút Lịch sử hiện thẳng trên cột Hành động cùng Sửa và Xóa.']
    if cfg['key'] == 'provinces':
        m9.append('- ⚠️ Thông báo trùng tên của màn này ghi "Tên khu vực này đã tồn tại" — '
                  'chữ "khu vực" bị lấy nhầm từ màn Danh mục khu vực. Ghi nhận là lỗi hiển thị, '
                  'không phải test sai.')
    if cfg['key'] in ('districts', 'hamlets'):
        m9.append('- ⚠️ Cửa sổ Lịch sử của màn này đang hiện SỐ ĐỊNH DANH thay vì tên ở các '
                  'trường tham chiếu. Ghi nhận là lỗi hiển thị đã biết.')
    if cfg['key'] == 'areas':
        m9.append('- ⚠️ Cửa sổ Lịch sử của màn này hiện tên trường thô "nation_name" thay vì '
                  'nhãn "Quốc gia". Ghi nhận là lỗi hiển thị đã biết.')

    return [
        ('1. Mục đích tính năng',
         'Quản lý danh mục %s dùng chung cho toàn hệ thống. Màn hình cho phép tra cứu, tìm kiếm, '
         'thêm mới, chỉnh sửa, xóa%s và xem lịch sử thay đổi. Dữ liệu của màn này là nguồn cho ô '
         'địa chỉ ở mọi màn nghiệp vụ khác.'
         % (dt, ', khóa/mở khóa' if co_khoa else '')),
        ('2. Đối tượng được tính / hiển thị', m2),
        ('3. Đối tượng bị ẩn / không tính', m3),
        ('4. Bộ lọc thời gian áp dụng cho',
         'Màn hình KHÔNG có bộ lọc khoảng thời gian. Yếu tố thời gian chỉ xuất hiện ở cột Ngày '
         'tạo (sắp xếp được), cột Ngày cập nhật (mặc định ẩn) và cửa sổ Lịch sử thay đổi. '
         'Cần lọc theo thời gian thì ghi nhận là yêu cầu mở rộng, không báo lỗi.'),
        ('5. Cấu trúc dữ liệu / cây phân cấp', m5),
        ('6. Quy tắc cộng dồn / deduplicate',
         '- Mỗi %s chỉ hiện MỘT dòng.\n'
         '- Tên %s là duy nhất %s — trùng sẽ bị chặn khi lưu.\n'
         '- Khi sửa, bản ghi đang sửa được loại khỏi phép kiểm tra trùng: giữ nguyên tên của '
         'chính nó thì lưu bình thường.'
         % (dt, dt, cfg['pham_vi_trung'])),
        ('7. Phân quyền cấp',
         'Màn hình này KHÔNG khai báo quyền nào. Mọi người dùng đã đăng nhập đều mở được màn '
         'hình và thực hiện được đầy đủ Thêm mới, Chỉnh sửa, Xóa%s.\n'
         'Phía máy chủ cũng không kiểm tra quyền, nên gọi thẳng chức năng mà bỏ qua giao diện '
         'vẫn ghi được dữ liệu. Đây là hiện trạng của mã nguồn, đã được ghi nhận để bộ phận '
         'quản trị cân nhắc bổ sung quyền.'
         % (', Khóa và Mở khóa' if co_khoa else '')),
        ('8. Cách tính các ô thống kê',
         '- Ô hiển thị tổng số bản ghi ở cuối lưới: là TỔNG số %s khớp bộ lọc đang áp dụng, '
         'không phải tổng toàn danh mục. Đổi bộ lọc thì số này đổi theo.\n'
         '- Số thứ tự chạy liên tục qua các trang: dòng đầu trang 2 tiếp nối dòng cuối trang 1.'
         % dt),
        ('9. Ghi chú đọc bảng', '\n'.join(m9)),
    ]


def sections(cfg):
    ten, dt, co_khoa = cfg['ten'], cfg['doi_tuong'], cfg['co_khoa']
    truong = cfg['truong']
    bb = [t for t in truong if t[3].startswith('Có')]
    kbb = [t for t in truong if not t[3].startswith('Có')]
    ten_truong = truong[0][0]

    # ---------------------------------------------------- I. HIỂN THỊ
    sec1 = [
        (1, 'Mở màn hình từ menu', 'P0',
         'Tài khoản bất kỳ đã đăng nhập. Danh mục có sẵn dữ liệu.',
         '1. Đăng nhập\n2. Vào menu Danh mục chung → Địa lý → %s' % ten, '—',
         '- Tiêu đề trang hiện "%s"\n'
         '- Lưới nạp xong và hiện dữ liệu\n'
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
        (4, 'Mọi tài khoản đều vào được màn hình', 'P0',
         'Hai tài khoản: một quản trị, một nhân viên thường không được gán quyền danh mục nào.',
         '1. Đăng nhập bằng tài khoản nhân viên thường\n2. Mở màn hình\n'
         '3. Quan sát thanh công cụ và cột Hành động', 'Tài khoản: nhân viên thường',
         '- ⚠️ VẪN mở được màn hình, thấy đủ dữ liệu\n'
         '- ⚠️ Nút Tạo mới và các nút thao tác VẪN hiện đầy đủ\n'
         '- Đây là hiện trạng đã ghi nhận, không phải lỗi test'),
        (5, 'Số thứ tự liên tục qua các trang', 'P0',
         'Danh mục có nhiều hơn một trang dữ liệu.',
         '1. Ghi lại số thứ tự dòng cuối trang 1\n2. Sang trang 2, đọc số thứ tự dòng đầu', '—',
         '- Số thứ tự nối tiếp liền mạch, không quay về 1'),
        (6, 'Đổi số dòng mỗi trang', 'P1',
         'Đang hiển thị số dòng mặc định.',
         '1. Đổi ô số dòng mỗi trang sang giá trị lớn hơn\n2. Đếm số dòng trên lưới', '—',
         '- Lưới hiện đúng số dòng đã chọn\n- ⚠️ Sau khi đổi phải quay về trang 1'),
        (7, 'Sắp xếp theo cột Tên', 'P0',
         'Danh mục có ít nhất 5 bản ghi.',
         '1. Bấm tiêu đề cột %s\n2. Đọc 5 dòng đầu\n3. Bấm lần thứ hai' % ten_truong, '—',
         '- Lần 1: xếp tăng dần đúng thứ tự tiếng Việt có dấu\n'
         '- Lần 2: thứ tự đảo ngược hoàn toàn'),
        (8, 'Sắp xếp theo Ngày tạo', 'P1',
         'Danh mục có bản ghi tạo ở nhiều thời điểm khác nhau.',
         '1. Bấm tiêu đề cột Ngày tạo hai lần để lấy giảm dần\n2. Đọc 5 dòng đầu', '—',
         '- Bản ghi tạo gần đây nhất đứng đầu'),
        (9, 'Sắp xếp giữ nguyên khi chuyển trang', 'P1',
         'Đang sắp xếp giảm dần theo cột %s.' % ten_truong,
         '1. Bấm sang trang 2\n2. So dòng đầu trang 2 với dòng cuối trang 1', '—',
         '- Thứ tự nối tiếp liền mạch, không đảo lộn hay lặp bản ghi'),
    ]
    if co_khoa:
        sec1.append(
            (10, 'Cột Trạng thái phân biệt Hoạt động và Khóa', 'P0',
             'Có ít nhất 1 bản ghi Hoạt động và 1 bản ghi đã Khóa.',
             '1. Mở màn hình\n2. Đọc cột Trạng thái của cả hai bản ghi', '—',
             '- Bản ghi bình thường hiện nhãn Hoạt động\n'
             '- Bản ghi đã khóa hiện nhãn Khóa, màu khác biệt rõ ràng\n'
             '- ⚠️ Cả hai đều nằm trong danh sách'))
        sec1.append(
            (11, 'Mặc định KHÔNG lọc trạng thái', 'P0',
             'Danh mục có 3 bản ghi đã Khóa.',
             '1. Vào màn hình lần đầu, không đụng vào bộ lọc\n2. Tìm 3 bản ghi đã Khóa', '—',
             '- ⚠️ Cả 3 bản ghi đã Khóa ĐỀU hiện trong danh sách\n'
             '- Ô lọc Trạng thái để trống'))
    else:
        sec1.append(
            (10, 'Màn hình không có cột Trạng thái', 'P1',
             'Đang ở màn %s.' % ten,
             '1. Đọc toàn bộ tiêu đề cột\n2. Mở bộ lọc', '—',
             '- ⚠️ KHÔNG có cột Trạng thái trên lưới\n'
             '- ⚠️ KHÔNG có ô lọc Trạng thái — đây là thiết kế của màn này'))

    # ---------------------------------------------------- II. TÌM KIẾM
    sec2 = [
        (1, 'Tìm nhanh theo tên', 'P0',
         'Có bản ghi tên chứa đoạn cần tìm.',
         '1. Gõ một phần tên vào ô tìm kiếm\n2. Chờ lưới nạp lại', 'Từ khóa: (một phần tên)',
         '- Chỉ còn các bản ghi có tên chứa từ khóa\n- Tổng số bản ghi đổi theo kết quả'),
        (2, 'Tìm nhanh không phân biệt chữ hoa chữ thường', 'P1',
         'Có bản ghi tên viết hoa chữ đầu.',
         '1. Gõ từ khóa toàn chữ thường\n2. Ghi nhận kết quả\n'
         '3. Xóa, gõ lại toàn chữ hoa\n4. So sánh', '—',
         '- Hai lần tìm cho ra CÙNG một tập kết quả'),
        (3, 'Xóa từ khóa thì danh sách quay về đầy đủ', 'P0',
         'Đang tìm với từ khóa cho ra ít kết quả.',
         '1. Xóa hết nội dung ô tìm kiếm\n2. Chờ lưới nạp lại', '—',
         '- Tổng số bản ghi quay lại như ban đầu\n- Lưới về trang 1'),
        (4, 'Nút Làm mới xóa hết tiêu chí và nạp lại', 'P0',
         'Đang áp dụng đủ các tiêu chí lọc của màn.',
         '1. Bấm nút Làm mới\n2. Quan sát các ô lọc và lưới', '—',
         '- Tất cả ô lọc trở về rỗng\n'
         '- ⚠️ Lưới PHẢI nạp lại ngay, không được giữ nguyên kết quả cũ'),
        (5, 'Áp dụng bộ lọc khi đang ở trang giữa', 'P0',
         'Đang ở trang 3. Bộ lọc mới chỉ cho ra vài kết quả.',
         '1. Áp dụng bộ lọc\n2. Quan sát lưới', '—',
         '- ⚠️ Lưới quay về trang 1 — không được hiện trang trống'),
        (6, 'Lọc ra kết quả rỗng', 'P1',
         'Chọn tổ hợp tiêu chí chắc chắn không có bản ghi nào thỏa.',
         '1. Chọn tổ hợp đó\n2. Bấm Tìm kiếm', '—',
         '- Lưới hiện thông báo không có dữ liệu\n- Tổng số bản ghi = 0'),
    ]
    n = 7
    for f in cfg['loc'][1:]:
        sec2.append(
            (n, 'Lọc theo %s' % f[0], 'P0' if n == 7 else 'P1',
             'Có bản ghi thỏa giá trị lọc sẽ chọn.',
             '1. Chọn %s\n2. Bấm Tìm kiếm' % f[0], '%s: (một giá trị có dữ liệu)' % f[0],
             '- Mọi dòng trả về đều khớp giá trị đã chọn\n- Tổng số bản ghi đổi đúng'))
        n += 1
    if cfg['key'] in ('districts', 'wards'):
        sec2.append(
            (n, 'Đổi Quốc gia thì ô Tỉnh/TP bị xóa trắng', 'P0',
             'Đang chọn Quốc gia = Việt Nam và một Tỉnh/TP cụ thể.',
             '1. Đổi ô Quốc gia sang quốc gia khác\n2. Quan sát ô Tỉnh/TP', '—',
             '- ⚠️ Ô Tỉnh/TP bị xóa trắng và nạp lại danh sách theo quốc gia mới'))
    if cfg['key'] == 'hamlets':
        sec2.append(
            (n, 'Đổi Tỉnh/TP thì ô Phường/xã bị xóa trắng', 'P0',
             'Đang chọn một Tỉnh/TP và một Phường/xã cụ thể.',
             '1. Đổi ô Tỉnh/TP sang tỉnh khác\n2. Quan sát ô Phường/xã', '—',
             '- ⚠️ Ô Phường/xã bị xóa trắng và nạp lại theo Tỉnh/TP mới'))

    # ---------------------------------------------------- III. THÊM MỚI
    sec3 = [
        (1, 'Mở cửa sổ thêm mới', 'P0',
         'Đang ở màn %s.' % ten,
         '1. Bấm nút Tạo mới\n2. Quan sát cửa sổ', '—',
         '- Cửa sổ mở với tiêu đề "Tạo %s"\n'
         '- Mọi ô đều để trống\n'
         '- Có đủ 3 nút: Lưu, Lưu và tiếp tục, Đóng' % dt),
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
        (n, 'Trùng tên bị chặn', 'P0',
         'Danh mục đã có bản ghi tên "X" %s.' % cfg['pham_vi_trung'],
         '1. Thêm mới với tên "X" và cùng %s\n2. Bấm Lưu'
         % (cfg['cap_tren'] or 'phạm vi'), 'Tên: X',
         '- Báo lỗi "%s"\n- Không tạo ra bản ghi mới' % cfg['loi_trung_ten']))
    n += 1
    sec3.append(
        (n, 'Trùng tên nhưng khác phạm vi thì lưu được', 'P0',
         'Đã có bản ghi tên "X" %s.' % cfg['pham_vi_trung'],
         '1. Thêm mới tên "X" nhưng đổi sang %s khác\n2. Bấm Lưu'
         % (cfg['cap_tren'] or 'phạm vi khác'), 'Tên: X',
         '- ⚠️ LƯU ĐƯỢC — trùng tên chỉ bị chặn %s' % cfg['pham_vi_trung']
         if cfg['cap_tren'] else
         '- Ghi nhận: tên duy nhất toàn hệ thống nên trường hợp này KHÔNG áp dụng'))
    n += 1
    for t in kbb:
        sec3.append(
            (n, 'Để trống %s vẫn lưu được' % t[0], 'P1',
             'Đang ở cửa sổ thêm mới.',
             '1. Nhập đủ các ô bắt buộc, để trống %s\n2. Bấm Lưu' % t[0],
             '%s: (để trống)' % t[0],
             '- Lưu thành công, không báo lỗi ô %s' % t[0]))
        n += 1
    sec3.append(
        (n, 'Nút Lưu và tiếp tục giữ cửa sổ mở', 'P0',
         'Đang ở cửa sổ thêm mới, đã nhập đủ trường bắt buộc.',
         '1. Bấm "Lưu và tiếp tục"\n2. Quan sát cửa sổ và danh sách phía sau', '—',
         '- Bản ghi được ghi, hiện thông báo thành công\n'
         '- ⚠️ Cửa sổ VẪN MỞ, các ô đã xóa trắng để nhập tiếp\n'
         '- Nhập bản ghi thứ hai rồi bấm Lưu thì cả hai đều có trong danh sách'))
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
         '- ⚠️ Chỉ tạo ra ĐÚNG MỘT bản ghi, không tạo hai bản trùng'))
    n += 1
    if cfg['key'] == 'hamlets':
        sec3.append(
            (n, 'Chọn Quốc gia Việt Nam thì ô Quận/Huyện bị ẩn', 'P0',
             'Đang ở cửa sổ thêm mới đường/phố.',
             '1. Chọn Quốc gia = Việt Nam\n2. Đếm số ô trên cửa sổ', 'Quốc gia: Việt Nam',
             '- ⚠️ Cửa sổ chỉ có 4 ô: Tên đường/phố, Quốc gia, Tỉnh/TP, Phường/xã\n'
             '- KHÔNG có ô Quận/Huyện/Thị xã'))
        n += 1
        sec3.append(
            (n, 'Chọn quốc gia khác thì ô Quận/Huyện hiện ra và bắt buộc', 'P0',
             'Đang ở cửa sổ thêm mới đường/phố, Quốc gia đang là Việt Nam.',
             '1. Đổi Quốc gia sang một quốc gia khác\n2. Quan sát cửa sổ\n'
             '3. Để trống Quận/Huyện, bấm Lưu', 'Quốc gia: (khác Việt Nam)',
             '- ⚠️ Ô Quận/Huyện/Thị xã HIỆN RA kèm dấu bắt buộc\n'
             '- Bỏ trống thì báo "Bắt buộc phải nhập"'))
        n += 1
    if cfg['key'] in ('nations', 'provinces', 'wards'):
        so_field = [t for t in truong if 'chữ số' in t[2]]
        for t in so_field:
            sec3.append(
                (n, 'Ô %s chỉ nhận chữ số' % t[0], 'P1',
                 'Đang ở cửa sổ thêm mới.',
                 '1. Nhập chữ cái vào ô %s\n2. Bấm Lưu\n3. Đổi sang chữ số, bấm Lưu' % t[0],
                 'abc / 123',
                 '- Bước 2: báo lỗi "Phải là số"\n- Bước 3: hợp lệ, lưu được'))
            n += 1

    # ---------------------------------------------------- IV. SỬA
    sec4 = [
        (1, 'Mở cửa sổ sửa', 'P0',
         'Có bản ghi %s.' % ('đang Hoạt động' if co_khoa else 'trong danh sách'),
         '1. Bấm biểu tượng bút chì ở dòng đó\n2. Quan sát cửa sổ', '—',
         '- Cửa sổ mở với mọi ô đã điền sẵn dữ liệu hiện tại'),
        (2, 'Sửa và lưu thành công', 'P0',
         'Bản ghi A đang có tên "Tên cũ".',
         '1. Mở cửa sổ sửa bản ghi A\n2. Đổi tên thành "Tên mới"\n3. Bấm Lưu\n4. Xem lưới',
         'Tên mới: Tên mới',
         '- Lưu thành công, thông báo cập nhật thành công\n'
         '- Cột tên trên lưới đổi thành "Tên mới"'),
        (3, 'Giữ nguyên tên của chính mình khi sửa', 'P0',
         'Bản ghi A có tên "X".',
         '1. Mở cửa sổ sửa A\n2. KHÔNG đổi tên, chỉ đổi ô khác\n3. Bấm Lưu', 'Tên: giữ nguyên X',
         '- ⚠️ LƯU ĐƯỢC, không báo lỗi trùng với chính mình'),
        (4, 'Sửa trùng tên với bản ghi khác', 'P0',
         'Bản ghi A tên "X", bản ghi B tên "Y", cùng %s.'
         % (cfg['cap_tren'] or 'danh mục'),
         '1. Mở cửa sổ sửa B\n2. Đổi tên thành "X"\n3. Bấm Lưu', 'Tên: X',
         '- Báo lỗi "%s", không lưu' % cfg['loi_trung_ten']),
        (5, 'Để trống tên khi sửa', 'P0',
         'Đang mở cửa sổ sửa một bản ghi.',
         '1. Xóa trắng ô %s\n2. Bấm Lưu' % ten_truong, '(để trống)',
         '- Báo lỗi "Bắt buộc phải nhập", không lưu'),
        (6, 'Sửa xong ghi vào lịch sử', 'P0',
         'Vừa đổi tên một bản ghi từ "Tên cũ" thành "Tên mới".',
         '1. Mở Lịch sử của bản ghi đó\n2. Đọc dòng trên cùng', '—',
         '- Có dòng ghi nhận lần sửa, nêu giá trị cũ "Tên cũ" và giá trị mới "Tên mới"\n'
         '- Kèm người thực hiện và thời điểm'),
        (7, 'Bấm Đóng khi đang sửa thì không ghi gì', 'P0',
         'Đang mở cửa sổ sửa và đã đổi tên.',
         '1. Bấm Đóng\n2. Xem lại lưới', '—',
         '- Tên trên lưới KHÔNG đổi'),
    ]
    if co_khoa:
        sec4.append(
            (8, 'Bản ghi đã Khóa không sửa được', 'P0',
             'Bản ghi B đang ở trạng thái Khóa.',
             '1. Tìm bản ghi B\n2. Quan sát cột Hành động', '—',
             '- ⚠️ Biểu tượng bút chì KHÔNG hiển thị\n'
             '- Chỉ còn Mở khóa và Lịch sử'))

    # ---------------------------------------------------- V. XÓA
    sec5 = [
        (1, 'Hộp xác nhận nêu đúng tên bản ghi', 'P0',
         'Có bản ghi tên "X" trong danh sách.',
         '1. Bấm biểu tượng thùng rác ở dòng đó\n2. Đọc nội dung hộp xác nhận', '—',
         '- Hộp hiện câu "Bạn có chắc muốn xóa %s \\"X\\"?"\n'
         '- Có hai nút Xóa và Hủy' % dt),
        (2, 'Bấm Hủy thì không xóa', 'P0',
         'Đang mở hộp xác nhận xóa.',
         '1. Bấm Hủy\n2. Xem lại lưới', '—',
         '- Hộp đóng, bản ghi vẫn còn nguyên\n- Không có thông báo thành công nào'),
        (3, 'Xóa thành công', 'P0',
         'Bản ghi X chưa được dùng ở đâu.',
         '1. Bấm thùng rác ở dòng X\n2. Bấm Xóa xác nhận\n3. Xem lưới', '—',
         '- Thông báo xóa thành công\n- Bản ghi X biến mất khỏi danh sách'),
        (4, 'Xóa bản ghi đang được dùng', 'P0',
         'Bản ghi X đang được cấp địa chỉ bên dưới hoặc dữ liệu nghiệp vụ khác tham chiếu.',
         '1. Bấm thùng rác ở dòng X\n2. Bấm Xóa xác nhận', '—',
         '- Hệ thống từ chối và nêu lý do\n- Bản ghi X vẫn còn trong danh sách'),
    ]
    if co_khoa:
        sec5.append(
            (5, 'Bản ghi đã Khóa không xóa được', 'P0',
             'Bản ghi B đang ở trạng thái Khóa.',
             '1. Tìm bản ghi B\n2. Quan sát cột Hành động', '—',
             '- ⚠️ Biểu tượng thùng rác KHÔNG hiển thị'))
    else:
        sec5.append(
            (5, 'Xóa là ngừng sử dụng, không mất dữ liệu', 'P1',
             'Bản ghi X vừa bị xóa khỏi danh sách.',
             '1. Kiểm tra các bản ghi cấp dưới hoặc chứng từ từng dùng X\n'
             '2. Ghi nhận X còn hiển thị đúng tên ở những nơi đó không', '—',
             '- ⚠️ Dữ liệu cũ tham chiếu tới X KHÔNG bị mất tên\n'
             '- X chỉ không còn chọn được ở lần nhập mới'))

    out = [
        ('I', 'HIỂN THỊ TRANG & TRUY CẬP', sec1),
        ('II', 'TÌM KIẾM & LỌC DANH SÁCH', sec2),
        ('III', 'THÊM MỚI', sec3),
        ('IV', 'CHỈNH SỬA', sec4),
        ('V', 'XÓA', sec5),
    ]

    # ---------------------------------------------------- VI. KHÓA
    if co_khoa:
        out.append(('VI', 'KHÓA / MỞ KHÓA', [
            (1, 'Nút Khóa nằm trong menu ba chấm', 'P0',
             'Có bản ghi đang Hoạt động.',
             '1. Bấm nút ba chấm "Hành động khác" ở dòng đó\n2. Đọc các mục trong menu', '—',
             '- Menu có hai mục: Khóa và Lịch sử\n'
             '- ⚠️ Sửa và Xóa nằm THẲNG trên cột Hành động, không nằm trong menu này'),
            (2, 'Khóa một bản ghi đang Hoạt động', 'P0',
             'Bản ghi X đang Hoạt động.',
             '1. Mở menu ba chấm ở dòng X, chọn Khóa\n2. Đọc hộp xác nhận\n3. Bấm Khóa', '—',
             '- Hộp xác nhận nêu rõ tên X\n'
             '- Thông báo thành công, cột Trạng thái đổi thành Khóa\n'
             '- ⚠️ X VẪN nằm trong danh sách'),
            (3, 'Hủy ở hộp xác nhận khóa', 'P0',
             'Bản ghi X đang Hoạt động.',
             '1. Chọn Khóa ở dòng X\n2. Bấm Hủy\n3. Xem cột Trạng thái', '—',
             '- Trạng thái vẫn là Hoạt động, không có thông báo thành công'),
            (4, 'Sau khi Khóa thì mất nút Sửa và Xóa', 'P0',
             'Vừa khóa bản ghi X.',
             '1. Quan sát cột Hành động của dòng X', '—',
             '- ⚠️ Chỉ còn hai nút: Mở khóa và Lịch sử\n'
             '- Sửa và Xóa đã biến mất'),
            (5, 'Mở khóa bản ghi', 'P0',
             'Bản ghi X đang ở trạng thái Khóa.',
             '1. Bấm Mở khóa ở dòng X\n2. Xác nhận\n3. Xem cột Trạng thái và cột Hành động', '—',
             '- Trạng thái đổi thành Hoạt động\n'
             '- Nút Sửa và Xóa hiện trở lại'),
            (6, 'Bản ghi đã Khóa không chọn được ở màn khác', 'P0',
             'Bản ghi X vừa bị Khóa.',
             '1. Mở một màn có ô chọn %s\n2. Tìm X trong danh sách chọn' % dt, '—',
             '- X KHÔNG xuất hiện trong danh sách chọn\n'
             '- ⚠️ Đây là mục đích chính của thao tác Khóa'),
            (7, 'Lọc theo trạng thái Khóa', 'P1',
             'Danh mục có đúng 3 bản ghi đang Khóa.',
             '1. Chọn bộ lọc Trạng thái = Khóa\n2. Bấm Tìm kiếm', 'Trạng thái: Khóa',
             '- Ra đúng 3 bản ghi, mọi dòng đều có nhãn Khóa'),
            (8, 'Khóa ghi vào lịch sử', 'P1',
             'Vừa khóa bản ghi X.',
             '1. Mở Lịch sử của X\n2. Đọc dòng trên cùng', '—',
             '- Có dòng ghi nhận đổi trạng thái, kèm người thực hiện và thời điểm'),
            (9, 'Khóa bản ghi đã bị người khác khóa', 'P1',
             'Hai người cùng mở danh sách. Người A vừa khóa X, người B chưa tải lại trang.',
             '1. Người B chọn Khóa ở dòng X\n2. Xác nhận', '—',
             '- Hệ thống báo dữ liệu đã thay đổi\n- Không treo trang, không báo lỗi khó hiểu'),
        ]))
        roman_ls = 'VII'
    else:
        roman_ls = 'VI'

    # ---------------------------------------------------- LỊCH SỬ
    sec_ls = [
        (1, 'Mở cửa sổ Lịch sử', 'P0',
         'Bản ghi X đã được sửa ít nhất 1 lần.',
         '1. Mở Lịch sử của X từ cột Hành động\n2. Quan sát cửa sổ', '—',
         '- Cửa sổ "Lịch sử thay đổi" mở ra\n'
         '- Dòng phụ ghi rõ loại đối tượng và tên X\n'
         '- Có bộ lọc riêng trong cửa sổ'),
        (2, 'Thứ tự mới nhất ở trên cùng', 'P0',
         'Bản ghi X đã được sửa 3 lần vào 3 thời điểm khác nhau.',
         '1. Mở Lịch sử của X\n2. Đọc thời điểm của 3 dòng từ trên xuống', '—',
         '- ⚠️ Dòng trên cùng là lần sửa MỚI NHẤT'),
        (3, 'Mỗi dòng nêu đủ thông tin', 'P0',
         'Vừa đổi tên bản ghi X từ "A" thành "B".',
         '1. Mở Lịch sử của X\n2. Đọc dòng trên cùng', '—',
         '- Nêu rõ trường đã đổi, giá trị cũ "A", giá trị mới "B"\n'
         '- Kèm tên người thực hiện và thời điểm tới phút'),
        (4, 'Bản ghi chưa từng sửa', 'P1',
         'Bản ghi Y vừa được tạo, chưa sửa lần nào.',
         '1. Mở Lịch sử của Y', '—',
         '- Cửa sổ hiện "Chưa có lịch sử thao tác nào."\n'
         '- Không báo lỗi, không hiện cửa sổ trắng trơn'),
        (5, 'Đóng cửa sổ Lịch sử', 'P2',
         'Đang mở cửa sổ Lịch sử, danh sách phía sau đang lọc và ở trang 2.',
         '1. Bấm Đóng', '—',
         '- Cửa sổ đóng, danh sách giữ nguyên bộ lọc và trang 2'),
    ]
    if cfg['key'] == 'areas':
        sec_ls.append(
            (6, 'Nhãn trường trong lịch sử', 'P1',
             'Vừa đổi Quốc gia của một khu vực.',
             '1. Mở Lịch sử của khu vực đó\n2. Đọc nhãn bên trái của dòng thay đổi', '—',
             '- ⚠️ Hiện tại đang hiện tên trường thô "nation_name" thay vì nhãn "Quốc gia" — '
             'đây là lỗi hiển thị đã ghi nhận\n'
             '- Sau khi sửa, nhãn phải là "Quốc gia"'))
    if cfg['key'] in ('districts', 'hamlets'):
        ref = 'Tỉnh/TP' if cfg['key'] == 'districts' else 'Phường/xã'
        sec_ls.append(
            (6, 'Giá trị trường tham chiếu trong lịch sử', 'P1',
             'Vừa đổi %s của một bản ghi.' % ref,
             '1. Mở Lịch sử của bản ghi đó\n2. Đọc giá trị cũ và giá trị mới', '—',
             '- ⚠️ Hiện tại đang hiện SỐ ĐỊNH DANH thay vì tên %s — đây là lỗi hiển thị đã '
             'ghi nhận\n- Sau khi sửa, phải hiện TÊN của %s' % (ref, ref)))
    out.append((roman_ls, 'LỊCH SỬ THAY ĐỔI', sec_ls))

    return out


if __name__ == '__main__':
    tong = 0
    for cfg in SCREENS:
        ten_file = cfg['ten'].replace('/', '-')
        out = os.path.join(HERE, 'testcase - %s.xlsx' % ten_file)
        n = build(output_file=out, sheet_name='Trang tính1',
                  feature_name='%s - Cập nhật ngày 17/08/2026' % cfg['ten'],
                  module_name=cfg['ten'],
                  description_block=desc_block(cfg),
                  role_tcs=[], sections=sections(cfg))
        tong += n
    print('TONG TC 6 MAN:', tong)
