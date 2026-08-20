# -*- coding: utf-8 -*-
"""Sinh testcase man 'Danh muc cong viec, loi thiet bi'.

Chay:  python .plans/gop-db/device-error-catalog-docs/gen_testcase.py
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
import de_config as C  # noqa: E402

TEN, DT, QUYEN = C.TEN, C.DOI_TUONG, C.QUYEN

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Quản lý danh mục các hạng mục công việc sửa chữa và tình trạng lỗi thiết bị. Đây là danh '
     'mục nền của nghiệp vụ sửa chữa: dữ liệu ở đây được chọn khi lập báo giá dịch vụ và phiếu '
     'sửa chữa. Màn hình cho phép tra cứu, lọc theo 8 tiêu chí, tuỳ chỉnh cột, thêm mới, chỉnh '
     'sửa, xóa, khóa / mở khóa, in danh sách, in chi tiết, xuất tệp bảng tính và xem lịch sử '
     'thay đổi.'),

    ('2. Đối tượng được tính / hiển thị',
     '- Toàn bộ hạng mục trong danh mục, gồm CẢ bản ghi Hoạt động lẫn bản ghi đã Khóa.\n'
     '- Sáu loại hạng mục: %s.\n'
     '- Bộ lọc Trạng thái để trống thì hiện cả hai nhóm; đây là mặc định khi vào màn.\n'
     '- Bản ghi đã Khóa vẫn xem được chi tiết, in và xem lịch sử.' % ', '.join(C.LOAI)),

    ('3. Đối tượng bị ẩn / không tính',
     '- Không ẩn bản ghi nào theo mặc định.\n'
     '- Bản ghi đã Khóa KHÔNG còn chọn được khi lập báo giá dịch vụ hoặc phiếu sửa chữa mới, '
     'nhưng vẫn nằm trong danh mục này.\n'
     '- Bản ghi đã bị Xóa không còn xuất hiện; chỉ hạng mục chưa phát sinh chứng từ mới xóa được.'),

    ('4. Bộ lọc thời gian áp dụng cho',
     'Màn hình KHÔNG có bộ lọc khoảng thời gian. Yếu tố thời gian chỉ xuất hiện ở cột Ngày tạo '
     '(sắp xếp được), cột Ngày cập nhật (mặc định ẩn, sắp xếp được) và cửa sổ Lịch sử thay đổi. '
     'Cần lọc theo thời gian thì ghi nhận là yêu cầu mở rộng, không báo lỗi.'),

    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- Danh mục phẳng, không phân cấp cha con. Mỗi hạng mục là một bản ghi độc lập, thuộc đúng '
     'MỘT loại trong sáu loại.\n'
     '- Mỗi hạng mục có ba bảng con: Áp dụng cho thiết bị (bắt buộc ít nhất một dòng), Vật tư '
     'thay thế (không bắt buộc) và Dịch vụ sửa chữa kèm theo (không bắt buộc).\n'
     '- Hạng mục được tham chiếu từ báo giá dịch vụ và phiếu sửa chữa; đây là căn cứ quyết định '
     'có xóa được hay không.'),

    ('6. Quy tắc cộng dồn / deduplicate',
     '- Mỗi hạng mục chỉ hiện MỘT dòng dù áp dụng cho nhiều thiết bị.\n'
     '- Cột Áp dụng cho thiết bị gộp nhiều thiết bị vào một ô.\n'
     '- ⚠️ Tên hạng mục là duy nhất TRONG CÙNG MỘT LOẠI, KHÔNG phải toàn danh mục. Hai loại khác '
     'nhau được phép có hạng mục trùng tên.\n'
     '- Khi sửa, bản ghi đang sửa được loại khỏi phép kiểm tra trùng.'),

    ('7. Phân quyền cấp',
     'Màn hình dùng đúng MỘT quyền: "%s".\n'
     '- Có quyền: mở được màn hình và thực hiện đầy đủ Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, '
     'In, Xuất tệp bảng tính.\n'
     '- Không có quyền: mục menu không hiển thị; truy cập thẳng đường dẫn thì hệ thống từ chối '
     'và báo không có quyền.\n'
     '- Riêng chức năng Xem lịch sử thay đổi không gắn quyền.\n'
     'Màn hình KHÔNG tách quyền xem riêng, cũng không phân quyền theo cấp công ty / phòng ban / '
     'bộ phận.' % QUYEN),

    ('8. Cách tính các ô thống kê',
     '- Ô hiển thị tổng số bản ghi ở cuối lưới: là TỔNG số hạng mục khớp bộ lọc đang áp dụng, '
     'không phải tổng toàn danh mục.\n'
     '- Cột Công kỹ thuật được tính tự động từ Định mức công khi người dùng để trống ô đó.\n'
     '- Cột Đơn giá bán được tính tự động theo công thức của hệ thống khi để trống.\n'
     '- Ô Hệ số giá bán dịch vụ và Đơn giá công kỹ thuật để trống thì lấy theo cấu hình của công '
     'ty người dùng đang đăng nhập — hai người ở hai công ty khác nhau có thể ra kết quả khác nhau.'),

    ('9. Ghi chú đọc bảng',
     'Các bẫy dễ sai nhất của màn này, QA đọc trước khi test:\n'
     '- ⚠️ TRÙNG TÊN XÉT THEO TỪNG LOẠI, không phải toàn danh mục. Tạo hạng mục cùng tên ở loại '
     'khác PHẢI lưu được — đừng báo lỗi nhầm.\n'
     '- ⚠️ Nút Xóa CHỈ hiện khi bản ghi đang Hoạt động VÀ chưa phát sinh chứng từ. Thiếu một '
     'trong hai điều kiện thì nút biến mất hẳn, không phải bị làm mờ.\n'
     '- ⚠️ Bản ghi đã Khóa chỉ còn ba thao tác: Mở khóa, In, Lịch sử. Nút Sửa và Xóa biến mất.\n'
     '- ⚠️ Cột Hành động chỉ hiện thẳng HAI nút đầu tiên, phần còn lại tự động dồn vào nút ba '
     'chấm. Vì vậy dòng không xóa được sẽ thấy Sửa và Khóa nằm ngoài, khác với dòng xóa được là '
     'Sửa và Xóa — đây là thiết kế, không phải lỗi.\n'
     '- ⚠️ Bảy cột mặc định ẩn: Loại, Áp dụng cho thiết bị, Định mức công, Công kỹ thuật, Đơn giá '
     'bán, Người cập nhật, Ngày cập nhật. Muốn kiểm tra các cột này phải bật ở cửa sổ Tuỳ chỉnh cột.\n'
     '- ⚠️ Chức năng thêm mới mở TRANG RIÊNG chứ không phải cửa sổ, vì form có ba bảng con.\n'
     '- ⚠️ Bảng Dịch vụ sửa chữa kèm theo không bắt buộc, NHƯNG đã thêm dòng thì phải nhập đủ cả '
     'Giá vốn và Giá dịch vụ. Bỏ trống sẽ báo lỗi ngay tại ô trong bảng.\n'
     '- ⚠️ Để trống Công kỹ thuật và Đơn giá bán là hợp lệ — hệ thống tự tính. Đừng báo lỗi '
     'thiếu dữ liệu.\n'
     '- ⚠️ Lọc theo Tên hoặc mã hàng hóa trả về hạng mục CÓ ÁP DỤNG cho hàng hóa đó, không phải '
     'hạng mục trùng tên với hàng hóa.'),
]

ROLE_TCS = [
    ('00', 'Có quyền thì mở được màn hình', 'P0',
     'Tài khoản T1 được gán quyền "%s".' % QUYEN,
     '1. Đăng nhập bằng T1\n2. Vào menu Chăm sóc khách hàng → Danh mục → Công việc, lỗi thiết bị',
     'Tài khoản: T1',
     '- Mục menu hiển thị\n'
     '- Mở được màn hình, thấy danh sách và các nút Tạo mới, Xuất Excel, In danh sách'),
    ('01', 'Không có quyền thì không thấy menu', 'P0',
     'Tài khoản T2 KHÔNG được gán quyền "%s".' % QUYEN,
     '1. Đăng nhập bằng T2\n2. Mở phân hệ Chăm sóc khách hàng, tìm mục menu Công việc, lỗi thiết bị',
     'Tài khoản: T2',
     '- ⚠️ Mục menu KHÔNG hiển thị với T2'),
    ('02', 'Không có quyền, truy cập thẳng đường dẫn', 'P0',
     'Tài khoản T2 KHÔNG có quyền "%s".' % QUYEN,
     '1. Đăng nhập bằng T2\n2. Gõ thẳng đường dẫn %s vào thanh địa chỉ' % C.ROUTE,
     'Tài khoản: T2',
     '- Hệ thống từ chối, báo không có quyền\n- Không hiện dữ liệu của danh mục'),
    ('03', 'Chặn thêm mới khi bỏ qua giao diện', 'P0',
     'Tài khoản T2 KHÔNG có quyền "%s".' % QUYEN,
     '1. Đăng nhập bằng T2, lấy phiên đăng nhập\n'
     '2. Dùng công cụ kiểm thử gọi thẳng chức năng Thêm mới, bỏ qua giao diện\n'
     '3. Kiểm tra lại danh mục bằng tài khoản có quyền',
     'Tài khoản: T2',
     '- Hệ thống từ chối, báo không có quyền\n- ⚠️ Không có hạng mục mới nào được tạo'),
    ('04', 'Chặn chỉnh sửa khi bỏ qua giao diện', 'P0',
     'Tài khoản T2 KHÔNG có quyền "%s". Hạng mục A đang có tên "Tên gốc".' % QUYEN,
     '1. Đăng nhập bằng T2\n'
     '2. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa cho A, đổi tên\n'
     '3. Mở lại A bằng tài khoản có quyền',
     'Tài khoản: T2',
     '- Hệ thống từ chối, báo không có quyền\n- Tên A vẫn là "Tên gốc"'),
    ('05', 'Chặn xóa khi bỏ qua giao diện', 'P0',
     'Tài khoản T2 KHÔNG có quyền "%s". Hạng mục B đang có trong danh mục.' % QUYEN,
     '1. Đăng nhập bằng T2\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa cho B\n'
     '3. Kiểm tra lại danh mục',
     'Tài khoản: T2',
     '- Hệ thống từ chối, báo không có quyền\n- B vẫn còn trong danh mục'),
    ('06', 'Chặn khóa / mở khóa khi bỏ qua giao diện', 'P0',
     'Tài khoản T2 KHÔNG có quyền "%s". Hạng mục C đang Hoạt động.' % QUYEN,
     '1. Đăng nhập bằng T2\n2. Dùng công cụ kiểm thử gọi thẳng thao tác Khóa cho C\n'
     '3. Kiểm tra trạng thái C',
     'Tài khoản: T2',
     '- Hệ thống từ chối, báo không có quyền\n- C vẫn ở trạng thái Hoạt động'),
    ('07', 'Chặn xuất tệp bảng tính khi bỏ qua giao diện', 'P1',
     'Tài khoản T2 KHÔNG có quyền "%s".' % QUYEN,
     '1. Đăng nhập bằng T2\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Xuất Excel',
     'Tài khoản: T2',
     '- Hệ thống từ chối, báo không có quyền\n- Không có tệp nào được sinh ra'),
    ('08', 'Xem lịch sử không cần quyền của màn', 'P1',
     'Tài khoản T3 mở được màn hình nhưng theo quy ước, chức năng Lịch sử không gắn quyền riêng.',
     '1. Đăng nhập bằng T3\n2. Mở danh sách\n3. Chọn Lịch sử ở nút ba chấm của một dòng',
     'Tài khoản: T3',
     '- Cửa sổ Lịch sử mở bình thường\n'
     '- ⚠️ Đây là quy ước chung của mọi màn danh sách, không phải lỗ hổng'),
]

SEC_I = [
    (1, 'Mở màn hình từ menu', 'P0',
     'Tài khoản có quyền "%s". Danh mục có sẵn dữ liệu.' % QUYEN,
     '1. Đăng nhập\n2. Vào menu Chăm sóc khách hàng → Danh mục → Công việc, lỗi thiết bị', '—',
     '- Tiêu đề trang hiện "%s"\n- Lưới nạp xong và hiện dữ liệu\n'
     '- Thanh công cụ có nút Tạo mới, Xuất Excel, In danh sách và biểu tượng cấu hình cột' % TEN),
    (2, 'Kiểm tra cột mặc định hiện và cột mặc định ẩn', 'P0',
     'Người dùng chưa từng chỉnh cấu hình cột trên màn này.',
     '1. Mở màn hình\n2. Đọc tên từng tiêu đề cột', '—',
     '- Hiện các cột: STT, Tên công việc / Tình trạng lỗi, Người tạo, Ngày tạo, Trạng thái, '
     'Hành động\n'
     '- ⚠️ Bảy cột MẶC ĐỊNH ẨN: Loại, Áp dụng cho thiết bị, Định mức công, Công kỹ thuật, '
     'Đơn giá bán, Người cập nhật, Ngày cập nhật'),
    (3, 'Hiển thị khi không có dữ liệu khớp', 'P1',
     'Danh mục có dữ liệu bình thường.',
     '1. Gõ vào ô tìm kiếm một chuỗi chắc chắn không tồn tại\n2. Chờ lưới nạp lại',
     'Từ khóa: zzzkhongtontai999',
     '- Lưới hiện thông báo không có dữ liệu\n- Không báo lỗi kỹ thuật'),
    (4, 'Cột Trạng thái phân biệt Hoạt động và Khóa', 'P0',
     'Có ít nhất 1 hạng mục Hoạt động và 1 hạng mục đã Khóa.',
     '1. Mở màn hình\n2. Đọc cột Trạng thái của cả hai bản ghi', '—',
     '- Hai trạng thái hiện đúng chữ và khác màu rõ ràng\n'
     '- ⚠️ Cả hai đều nằm trong danh sách'),
    (5, 'Số thứ tự liên tục qua các trang', 'P0',
     'Danh mục có nhiều hơn một trang dữ liệu.',
     '1. Ghi lại số thứ tự dòng cuối trang 1\n2. Sang trang 2, đọc số thứ tự dòng đầu', '—',
     '- Số thứ tự nối tiếp liền mạch, không quay về 1'),
    (6, 'Sắp xếp theo Tên công việc / Tình trạng lỗi', 'P0',
     'Danh mục có ít nhất 5 bản ghi.',
     '1. Bấm tiêu đề cột Tên công việc / Tình trạng lỗi\n2. Đọc 5 dòng đầu\n3. Bấm lần thứ hai',
     '—',
     '- Lần 1: xếp tăng dần đúng thứ tự tiếng Việt có dấu\n- Lần 2: thứ tự đảo ngược'),
    (7, 'Sắp xếp theo Đơn giá bán', 'P1',
     'Đã bật cột Đơn giá bán ở cửa sổ Tuỳ chỉnh cột.',
     '1. Bấm tiêu đề cột Đơn giá bán hai lần để lấy giảm dần\n2. Đọc 5 dòng đầu', '—',
     '- Hạng mục có đơn giá cao nhất đứng đầu\n- Số hiển thị đúng định dạng tiền tệ'),
    (8, 'Sắp xếp theo Ngày tạo', 'P1',
     'Danh mục có bản ghi tạo ở nhiều thời điểm.',
     '1. Bấm tiêu đề cột Ngày tạo hai lần\n2. Đọc 5 dòng đầu', '—',
     '- Hạng mục tạo gần đây nhất đứng đầu'),
    (9, 'Đổi số dòng mỗi trang', 'P1',
     'Đang hiển thị số dòng mặc định.',
     '1. Đổi ô số dòng mỗi trang sang giá trị lớn hơn\n2. Đếm số dòng', '—',
     '- Lưới hiện đúng số dòng đã chọn\n- ⚠️ Sau khi đổi phải quay về trang 1'),
    (10, 'Cột Áp dụng cho thiết bị gộp nhiều thiết bị', 'P1',
     'Hạng mục X áp dụng cho 3 thiết bị. Đã bật cột Áp dụng cho thiết bị.',
     '1. Tìm hạng mục X\n2. Đọc ô Áp dụng cho thiết bị', '—',
     '- Cả 3 thiết bị hiện trong cùng một ô, không bị cắt mất thiết bị nào'),
]

SEC_II = [
    (1, 'Tìm nhanh theo tên', 'P0',
     'Có hạng mục tên chứa đoạn cần tìm.',
     '1. Gõ một phần tên vào ô tìm kiếm\n2. Chờ lưới nạp lại', 'Từ khóa: (một phần tên)',
     '- Chỉ còn các hạng mục có tên chứa từ khóa\n- Tổng số bản ghi đổi theo kết quả'),
    (2, 'Mở panel Tìm kiếm nâng cao', 'P0',
     'Đang ở màn danh sách.',
     '1. Bấm nút Tìm kiếm nâng cao\n2. Đếm số ô lọc', '—',
     '- Panel mở ra với 8 tiêu chí: Loại, Trạng thái, Nhóm hàng hóa, Tên hoặc mã hàng hóa, '
     'Người tạo, Người sửa, Đơn giá bán từ – đến, Định mức công'),
    (3, 'Lọc theo Loại', 'P0',
     'Danh mục có hạng mục ở nhiều loại khác nhau.',
     '1. Chọn Loại = Lỗi đã xác định\n2. Bấm Tìm kiếm\n3. Bật cột Loại để đối chiếu',
     'Loại: Lỗi đã xác định',
     '- Mọi dòng trả về đều thuộc loại Lỗi đã xác định'),
    (4, 'Lọc theo Trạng thái = Khóa', 'P0',
     'Danh mục có ít nhất 2 hạng mục đã Khóa.',
     '1. Chọn Trạng thái = Khóa\n2. Bấm Tìm kiếm', 'Trạng thái: Khóa',
     '- Mọi dòng đều có nhãn Khóa\n- Mọi dòng chỉ còn ba thao tác Mở khóa, In, Lịch sử'),
    (5, 'Lọc theo Nhóm hàng hóa', 'P1',
     'Có hạng mục áp dụng cho thiết bị thuộc một nhóm hàng hóa cụ thể.',
     '1. Chọn Nhóm hàng hóa\n2. Bấm Tìm kiếm', 'Nhóm hàng hóa: (một nhóm có dữ liệu)',
     '- Chỉ còn hạng mục có áp dụng cho thiết bị thuộc nhóm đã chọn'),
    (6, 'Lọc theo Tên hoặc mã hàng hóa', 'P0',
     'Hạng mục X áp dụng cho thiết bị có mã TB001.',
     '1. Nhập Tên hoặc mã hàng hóa = TB001\n2. Bấm Tìm kiếm', 'Mã hàng hóa: TB001',
     '- Hạng mục X có trong kết quả\n'
     '- ⚠️ Bộ lọc này tìm theo THIẾT BỊ ĐƯỢC ÁP DỤNG, không phải tên hạng mục'),
    (7, 'Lọc theo Người tạo', 'P1',
     'Nhân viên NV-A đã tạo 5 hạng mục.',
     '1. Chọn Người tạo = NV-A\n2. Bấm Tìm kiếm', 'Người tạo: NV-A',
     '- Ra 5 hạng mục, cột Người tạo đều là NV-A'),
    (8, 'Lọc theo Người sửa', 'P1',
     'Nhân viên NV-B là người sửa gần nhất của 3 hạng mục.',
     '1. Chọn Người sửa = NV-B\n2. Bấm Tìm kiếm\n3. Bật cột Người cập nhật', 'Người sửa: NV-B',
     '- Ra 3 hạng mục, cột Người cập nhật đều là NV-B'),
    (9, 'Lọc theo khoảng Đơn giá bán', 'P0',
     'Danh mục có hạng mục với nhiều mức đơn giá khác nhau.',
     '1. Nhập Đơn giá bán từ 100.000 đến 500.000\n2. Bấm Tìm kiếm\n3. Bật cột Đơn giá bán',
     'Từ: 100.000 · Đến: 500.000',
     '- Mọi dòng có đơn giá nằm trong khoảng đã nhập, tính cả hai đầu'),
    (10, 'Lọc chỉ nhập một đầu của khoảng đơn giá', 'P1',
     'Danh mục có hạng mục với nhiều mức đơn giá.',
     '1. Chỉ nhập Đơn giá bán từ 500.000, để trống ô đến\n2. Bấm Tìm kiếm', 'Từ: 500.000',
     '- Ra mọi hạng mục có đơn giá từ 500.000 trở lên, không bị chặn vì thiếu đầu kia'),
    (11, 'Lọc theo Định mức công', 'P1',
     'Có hạng mục với định mức công bằng 2.',
     '1. Nhập Định mức công = 2\n2. Bấm Tìm kiếm\n3. Bật cột Định mức công', 'Định mức công: 2',
     '- Mọi dòng trả về có định mức công đúng bằng giá trị đã nhập'),
    (12, 'Kết hợp nhiều tiêu chí lọc', 'P0',
     'Có hạng mục vừa thuộc loại Lỗi đã xác định, vừa đang Hoạt động.',
     '1. Chọn Loại = Lỗi đã xác định và Trạng thái = Hoạt động\n2. Bấm Tìm kiếm',
     '2 tiêu chí như trên',
     '- Chỉ hạng mục thỏa ĐỒNG THỜI cả hai điều kiện\n'
     '- ⚠️ Các tiêu chí kết hợp theo kiểu "và", không phải "hoặc"'),
    (13, 'Nút Làm mới xóa hết tiêu chí và nạp lại', 'P0',
     'Đang áp dụng 3 tiêu chí lọc.',
     '1. Bấm nút Làm mới\n2. Quan sát các ô lọc và lưới', '—',
     '- Tất cả ô lọc trở về rỗng\n- ⚠️ Lưới PHẢI nạp lại ngay, không giữ kết quả cũ'),
    (14, 'Áp dụng bộ lọc khi đang ở trang giữa', 'P0',
     'Đang ở trang 3. Bộ lọc mới chỉ cho ra vài kết quả.',
     '1. Áp dụng bộ lọc\n2. Quan sát lưới', '—',
     '- ⚠️ Lưới quay về trang 1, không hiện trang trống'),
    (15, 'Lọc ra kết quả rỗng', 'P1',
     'Chọn tổ hợp tiêu chí chắc chắn không có hạng mục nào thỏa.',
     '1. Chọn tổ hợp đó\n2. Bấm Tìm kiếm', '—',
     '- Lưới hiện thông báo không có dữ liệu\n- Tổng số bản ghi = 0'),
]

SEC_III = [
    (1, 'Mở cửa sổ Tuỳ chỉnh cột', 'P0',
     'Đang ở màn danh sách.',
     '1. Bấm biểu tượng Cấu hình cột hiển thị ở góc phải thanh công cụ', '—',
     '- Cửa sổ "Tuỳ chỉnh cột" mở ra, liệt kê đủ 13 cột kèm ô tích'),
    (2, 'Bật một cột đang ẩn', 'P0',
     'Cột Đơn giá bán đang ẩn.',
     '1. Mở Tuỳ chỉnh cột\n2. Tích cột Đơn giá bán\n3. Bấm Lưu\n4. Quan sát lưới',
     'Bật: Đơn giá bán',
     '- Cột Đơn giá bán hiện trên lưới kèm dữ liệu đúng'),
    (3, 'Bật cùng lúc cả 7 cột mặc định ẩn', 'P1',
     'Người dùng chưa chỉnh cấu hình cột.',
     '1. Mở Tuỳ chỉnh cột, tích cả 7 cột đang ẩn, bấm Lưu\n2. Kéo ngang lưới', 'Bật 7 cột',
     '- Cả 7 cột hiện đủ dữ liệu, lưới cuộn ngang được, không vỡ bố cục'),
    (4, 'Tắt một cột đang hiện', 'P0',
     'Cột Người tạo đang hiện.',
     '1. Mở Tuỳ chỉnh cột, bỏ tích Người tạo, bấm Lưu', 'Tắt: Người tạo',
     '- Cột Người tạo biến mất, các cột khác dồn lại không để khoảng trống'),
    (5, 'Không bỏ tích được cột bị khóa', 'P0',
     'Đang mở cửa sổ Tuỳ chỉnh cột.',
     '1. Bấm ô tích của cột STT\n2. Bấm ô tích của cột Tên công việc / Tình trạng lỗi', '—',
     '- Cả hai không bỏ tích được, luôn giữ trạng thái đã chọn'),
    (6, 'Cấu hình cột ghi nhớ theo tài khoản', 'P0',
     'Tài khoản A vừa bật cột Đơn giá bán và tắt cột Người tạo.',
     '1. Đăng xuất A, đăng nhập tài khoản B, mở màn hình\n'
     '2. Đăng xuất, đăng nhập lại A', '—',
     '- Tài khoản B thấy cấu hình MẶC ĐỊNH, không bị ảnh hưởng bởi A\n'
     '- Tài khoản A quay lại vẫn thấy cấu hình riêng của mình'),
    (7, 'Đóng cửa sổ mà không bấm Lưu', 'P1',
     'Đang mở Tuỳ chỉnh cột và vừa tích thêm 2 cột.',
     '1. Bấm Đóng\n2. Quan sát lưới', '—',
     '- Lưới KHÔNG đổi, cấu hình cũ giữ nguyên'),
]

SEC_IV = [
    (1, 'Mở trang thêm mới', 'P0',
     'Tài khoản có quyền "%s".' % QUYEN,
     '1. Bấm nút Tạo mới\n2. Quan sát màn hình', '—',
     '- ⚠️ Hệ thống mở TRANG RIÊNG, không phải cửa sổ\n'
     '- Tiêu đề trang là "Thêm công việc / lỗi thiết bị"\n'
     '- Có 11 ô nhập và 3 bảng con, mọi ô để trống'),
    (2, 'Thêm mới đủ trường bắt buộc', 'P0',
     'Đã chuẩn bị tên chưa tồn tại trong loại sẽ chọn. Có sẵn thiết bị để chọn.',
     '1. Bấm Tạo mới\n2. Chọn Loại công việc / lỗi\n3. Nhập Tên công việc / tình trạng lỗi\n'
     '4. Nhập Định mức công, Định mức giảm giá, VAT, Hệ số công nghệ\n'
     '5. Thêm ít nhất 1 thiết bị vào bảng Áp dụng cho thiết bị\n6. Bấm Lưu',
     'Loại: Lỗi đã xác định · Tên: Kiểm tra thử · Định mức công: 2 · Giảm giá: 10 · VAT: 10 · '
     'Hệ số công nghệ: 1',
     '- Lưu thành công, hiện thông báo thành công\n'
     '- Quay về danh sách, hạng mục mới có mặt với trạng thái Hoạt động'),
    (3, 'Thiếu Loại công việc / lỗi thì bị chặn', 'P0',
     'Đang ở trang thêm mới, các ô khác đã nhập hợp lệ.',
     '1. Không chọn Loại công việc / lỗi\n2. Bấm Lưu', 'Loại: (không chọn)',
     '- Báo lỗi đỏ tại ô Loại công việc / lỗi\n- Trang KHÔNG chuyển, dữ liệu đã nhập vẫn còn'),
    (4, 'Thiếu Tên công việc / tình trạng lỗi thì bị chặn', 'P0',
     'Đang ở trang thêm mới, các ô khác đã nhập hợp lệ.',
     '1. Để trống ô Tên công việc / tình trạng lỗi\n2. Bấm Lưu', 'Tên: (để trống)',
     '- Báo lỗi đỏ ngay dưới ô Tên: "Bắt buộc phải nhập"'),
    (5, 'Thiếu Định mức công thì bị chặn', 'P0',
     'Đang ở trang thêm mới.',
     '1. Để trống ô Định mức công\n2. Bấm Lưu', 'Định mức công: (để trống)',
     '- Báo lỗi đỏ tại ô Định mức công'),
    (6, 'Thiếu Định mức giảm giá thì bị chặn', 'P0',
     'Đang ở trang thêm mới.',
     '1. Để trống ô Định mức giảm giá\n2. Bấm Lưu', 'Định mức giảm giá: (để trống)',
     '- Báo lỗi đỏ tại ô Định mức giảm giá'),
    (7, 'Thiếu VAT thì bị chặn', 'P0',
     'Đang ở trang thêm mới.',
     '1. Để trống ô VAT\n2. Bấm Lưu', 'VAT: (để trống)',
     '- Báo lỗi đỏ tại ô VAT'),
    (8, 'VAT vượt quá 100', 'P0',
     'Đang ở trang thêm mới.',
     '1. Nhập VAT = 150\n2. Bấm Lưu\n3. Đổi thành 10, bấm Lưu', 'VAT: 150 / 10',
     '- Bước 2: báo lỗi "Tối đa 100"\n- Bước 3: hợp lệ, lưu được'),
    (9, 'VAT nhập chữ', 'P1',
     'Đang ở trang thêm mới.',
     '1. Nhập VAT = abc\n2. Bấm Lưu', 'VAT: abc',
     '- Báo lỗi "Phải là số"'),
    (10, 'Hệ số công nghệ bằng 0', 'P0',
     'Đang ở trang thêm mới.',
     '1. Nhập Hệ số công nghệ = 0\n2. Bấm Lưu\n3. Đổi thành 1, bấm Lưu',
     'Hệ số công nghệ: 0 / 1',
     '- Bước 2: báo lỗi "Nhập hệ số lớn hơn 0"\n- Bước 3: hợp lệ, lưu được'),
    (11, 'Đơn giá bán nhập số âm', 'P1',
     'Đang ở trang thêm mới.',
     '1. Nhập Đơn giá bán = -1000\n2. Bấm Lưu', 'Đơn giá bán: -1000',
     '- Báo lỗi "Không được nhỏ hơn 0"'),
    (12, 'Chưa thêm thiết bị nào thì bị chặn', 'P0',
     'Đang ở trang thêm mới, đã nhập đủ mọi ô bắt buộc.',
     '1. Để trống bảng Áp dụng cho thiết bị\n2. Bấm Lưu', 'Bảng thiết bị: (không có dòng nào)',
     '- Bị chặn, hệ thống báo phải chọn ít nhất một thiết bị\n- Không tạo ra hạng mục mới'),
    (13, 'Trùng tên TRONG CÙNG loại thì bị chặn', 'P0',
     'Danh mục đã có hạng mục tên "Kiểm tra cầu nâng" thuộc loại Lỗi đã xác định.',
     '1. Thêm mới với Loại = Lỗi đã xác định và Tên = Kiểm tra cầu nâng\n2. Bấm Lưu',
     'Loại: Lỗi đã xác định · Tên: Kiểm tra cầu nâng',
     '- Bị chặn, hệ thống báo tên đã tồn tại\n- Không tạo ra hạng mục mới'),
    (14, 'Trùng tên nhưng KHÁC loại thì lưu được', 'P0',
     'Danh mục đã có hạng mục tên "Kiểm tra cầu nâng" thuộc loại Lỗi đã xác định.',
     '1. Thêm mới với Loại = Tư vấn, khảo sát và Tên = Kiểm tra cầu nâng\n'
     '2. Nhập đủ các ô bắt buộc và 1 thiết bị\n3. Bấm Lưu',
     'Loại: Tư vấn, khảo sát · Tên: Kiểm tra cầu nâng',
     '- ⚠️ LƯU THÀNH CÔNG — trùng tên chỉ bị chặn trong CÙNG MỘT loại\n'
     '- Danh sách có hai hạng mục cùng tên, khác loại'),
    (15, 'Để trống Công kỹ thuật thì hệ thống tự tính', 'P0',
     'Đang ở trang thêm mới, đã nhập Định mức công = 2.',
     '1. Để trống ô Công kỹ thuật\n2. Nhập đủ các ô còn lại, bấm Lưu\n'
     '3. Mở lại hạng mục vừa tạo, đọc ô Công kỹ thuật', 'Công kỹ thuật: (để trống)',
     '- ⚠️ Lưu được, KHÔNG báo lỗi thiếu dữ liệu\n'
     '- Ô Công kỹ thuật có giá trị được tính tự động từ Định mức công'),
    (16, 'Để trống Đơn giá bán thì hệ thống tự tính', 'P0',
     'Đang ở trang thêm mới.',
     '1. Để trống ô Đơn giá bán\n2. Nhập đủ các ô còn lại, bấm Lưu\n'
     '3. Bật cột Đơn giá bán trên lưới', 'Đơn giá bán: (để trống)',
     '- Lưu được, cột Đơn giá bán có giá trị được tính tự động'),
    (17, 'Để trống Hệ số giá bán dịch vụ thì lấy theo cấu hình công ty', 'P1',
     'Công ty của người dùng đã có cấu hình hệ số giá bán dịch vụ.',
     '1. Để trống ô Hệ số giá bán dịch vụ\n2. Nhập đủ các ô còn lại, bấm Lưu\n'
     '3. Mở lại hạng mục vừa tạo', 'Hệ số giá bán dịch vụ: (để trống)',
     '- Lưu được, hệ thống dùng hệ số theo cấu hình công ty\n'
     '- ⚠️ Người dùng ở công ty khác có thể ra kết quả tính khác'),
    (18, 'Thêm nhiều thiết bị vào bảng Áp dụng cho thiết bị', 'P1',
     'Đang ở trang thêm mới.',
     '1. Bấm thêm thiết bị, chọn thiết bị thứ nhất\n2. Lặp lại, chọn thiết bị thứ hai và ba\n'
     '3. Bấm Lưu\n4. Bật cột Áp dụng cho thiết bị', '3 thiết bị',
     '- Cả 3 thiết bị được lưu và hiện đủ trong ô Áp dụng cho thiết bị'),
    (19, 'Thêm vật tư thay thế', 'P1',
     'Đang ở trang thêm mới.',
     '1. Thêm 2 dòng vào bảng Vật tư thay thế\n2. Nhập đủ các ô bắt buộc, bấm Lưu\n'
     '3. Mở lại hạng mục', '2 vật tư',
     '- Lưu thành công, mở lại thấy đủ 2 vật tư thay thế'),
    (20, 'Bỏ trống bảng Vật tư thay thế vẫn lưu được', 'P1',
     'Đang ở trang thêm mới.',
     '1. Không thêm dòng nào vào bảng Vật tư thay thế\n2. Nhập đủ các ô bắt buộc, bấm Lưu',
     'Bảng vật tư: (trống)',
     '- Lưu thành công — bảng này KHÔNG bắt buộc'),
    (21, 'Dòng dịch vụ thiếu Giá vốn thì bị chặn', 'P0',
     'Đang ở trang thêm mới, đã thêm 1 dòng vào bảng Dịch vụ sửa chữa kèm theo.',
     '1. Để trống ô Giá vốn của dòng dịch vụ đó\n2. Nhập đủ các ô còn lại, bấm Lưu',
     'Giá vốn: (để trống)',
     '- ⚠️ Báo lỗi "Bắt buộc phải nhập" NGAY TẠI Ô GIÁ VỐN trong bảng, không phải thông báo chung\n'
     '- Không lưu được'),
    (22, 'Dòng dịch vụ thiếu Giá dịch vụ thì bị chặn', 'P0',
     'Đang ở trang thêm mới, đã thêm 1 dòng vào bảng Dịch vụ sửa chữa kèm theo.',
     '1. Để trống ô Giá dịch vụ của dòng đó\n2. Bấm Lưu', 'Giá dịch vụ: (để trống)',
     '- Báo lỗi "Bắt buộc phải nhập" ngay tại ô Giá dịch vụ trong bảng'),
    (23, 'Giá vốn nhập số âm', 'P1',
     'Đang ở trang thêm mới, đã thêm 1 dòng dịch vụ.',
     '1. Nhập Giá vốn = -500\n2. Bấm Lưu', 'Giá vốn: -500',
     '- Báo lỗi "Không được nhỏ hơn 0" tại ô Giá vốn'),
    (24, 'Bỏ trống bảng Dịch vụ sửa chữa vẫn lưu được', 'P0',
     'Đang ở trang thêm mới.',
     '1. Không thêm dòng nào vào bảng Dịch vụ sửa chữa kèm theo\n'
     '2. Nhập đủ các ô bắt buộc, bấm Lưu', 'Bảng dịch vụ: (trống)',
     '- Lưu thành công — bảng này KHÔNG bắt buộc, chỉ ràng buộc khi ĐÃ thêm dòng'),
    (25, 'Cảnh báo khi thoát trang mà chưa lưu', 'P0',
     'Đang ở trang thêm mới và đã nhập một phần dữ liệu.',
     '1. Bấm Quay lại\n2. Quan sát', '—',
     '- Hệ thống hỏi xác nhận rời khỏi trang\n'
     '- Chọn ở lại thì dữ liệu còn nguyên; chọn rời đi thì mất hết'),
    (26, 'Bấm Lưu hai lần liên tiếp', 'P0',
     'Đang ở trang thêm mới, đã nhập đủ trường bắt buộc.',
     '1. Bấm Lưu\n2. Bấm Lưu lần hai thật nhanh\n3. Xem danh sách', '—',
     '- ⚠️ Chỉ tạo ra ĐÚNG MỘT hạng mục'),
]

SEC_V = [
    (1, 'Mở trang chỉnh sửa', 'P0',
     'Hạng mục A đang ở trạng thái Hoạt động.',
     '1. Bấm biểu tượng bút chì ở dòng A\n2. Quan sát trang', '—',
     '- Mở trang chỉnh sửa, mọi ô và cả ba bảng con đã điền sẵn dữ liệu hiện tại'),
    (2, 'Sửa và lưu thành công', 'P0',
     'Hạng mục A đang có tên "Tên cũ".',
     '1. Mở trang sửa A\n2. Đổi tên thành "Tên mới"\n3. Bấm Lưu\n4. Xem lưới',
     'Tên mới: Tên mới',
     '- Lưu thành công, cột tên trên lưới đổi theo'),
    (3, 'Giữ nguyên tên của chính mình khi sửa', 'P0',
     'Hạng mục A có tên "X" thuộc loại Lỗi đã xác định.',
     '1. Mở trang sửa A\n2. KHÔNG đổi tên, chỉ đổi Định mức công\n3. Bấm Lưu',
     'Tên: giữ nguyên X',
     '- ⚠️ LƯU ĐƯỢC, không báo lỗi trùng với chính mình'),
    (4, 'Sửa trùng tên với hạng mục khác cùng loại', 'P0',
     'Hạng mục A tên "X" và hạng mục B tên "Y", cùng thuộc loại Lỗi đã xác định.',
     '1. Mở trang sửa B\n2. Đổi tên thành "X"\n3. Bấm Lưu', 'Tên: X',
     '- Bị chặn, báo tên đã tồn tại'),
    (5, 'Đổi Loại sang loại đang có hạng mục trùng tên', 'P0',
     'Hạng mục A tên "X" thuộc loại Tư vấn, khảo sát. Loại Lỗi đã xác định cũng đã có hạng mục '
     'tên "X".',
     '1. Mở trang sửa A\n2. Đổi Loại sang Lỗi đã xác định\n3. Bấm Lưu',
     'Loại mới: Lỗi đã xác định',
     '- ⚠️ Bị chặn vì sau khi đổi loại sẽ trùng tên trong loại mới\n'
     '- Đây là điểm dễ bỏ sót khi kiểm thử'),
    (6, 'Sửa các bảng con', 'P1',
     'Hạng mục A đang có 2 thiết bị áp dụng.',
     '1. Mở trang sửa A\n2. Xóa 1 thiết bị, thêm 1 thiết bị khác\n3. Bấm Lưu\n'
     '4. Mở lại trang sửa', '—',
     '- Bảng Áp dụng cho thiết bị phản ánh đúng thay đổi'),
    (7, 'Xóa hết thiết bị khi sửa thì bị chặn', 'P0',
     'Hạng mục A đang có 1 thiết bị áp dụng.',
     '1. Mở trang sửa A\n2. Xóa thiết bị duy nhất\n3. Bấm Lưu', '—',
     '- Bị chặn, báo phải có ít nhất một thiết bị'),
    (8, 'Sửa xong ghi vào lịch sử', 'P0',
     'Vừa đổi tên hạng mục A từ "Tên cũ" thành "Tên mới".',
     '1. Mở Lịch sử của A\n2. Đọc dòng trên cùng', '—',
     '- Có dòng ghi nhận lần sửa, nêu giá trị cũ và giá trị mới, kèm người thực hiện và thời điểm'),
    (9, 'Hạng mục đã Khóa không sửa được', 'P0',
     'Hạng mục B đang ở trạng thái Khóa.',
     '1. Tìm dòng B\n2. Quan sát cột Hành động', '—',
     '- ⚠️ Biểu tượng bút chì KHÔNG hiển thị\n'
     '- Chỉ còn ba thao tác: Mở khóa, In, Lịch sử'),
]

SEC_VI = [
    (1, 'Nút Xóa hiện khi hạng mục chưa phát sinh chứng từ', 'P0',
     'Hạng mục Z đang Hoạt động, chưa dùng ở báo giá hay phiếu sửa chữa nào.',
     '1. Tìm dòng Z\n2. Quan sát cột Hành động', '—',
     '- Có biểu tượng thùng rác, hiện thẳng cạnh nút Sửa'),
    (2, 'Nút Xóa bị ẩn khi hạng mục đã phát sinh chứng từ', 'P0',
     'Hạng mục Y đang Hoạt động nhưng đã được dùng trong ít nhất một báo giá hoặc phiếu sửa chữa.',
     '1. Tìm dòng Y\n2. Quan sát cột Hành động', '—',
     '- ⚠️ KHÔNG có biểu tượng thùng rác\n'
     '- ⚠️ Vì cột chỉ hiện thẳng hai nút đầu, dòng này sẽ thấy Sửa và Khóa nằm ngoài — khác dòng '
     'xóa được là Sửa và Xóa. Đây là thiết kế, không phải lỗi'),
    (3, 'Nút Xóa bị ẩn khi hạng mục đã Khóa', 'P0',
     'Hạng mục B đang ở trạng thái Khóa và chưa phát sinh chứng từ.',
     '1. Tìm dòng B\n2. Quan sát cột Hành động', '—',
     '- ⚠️ Vẫn KHÔNG có nút Xóa — cần thỏa CẢ HAI điều kiện: đang Hoạt động và chưa phát sinh '
     'chứng từ'),
    (4, 'Hộp xác nhận nêu đúng tên hạng mục', 'P0',
     'Hạng mục Z đang xóa được.',
     '1. Bấm biểu tượng thùng rác ở dòng Z\n2. Đọc nội dung hộp xác nhận', '—',
     '- Hộp nêu rõ tên hạng mục Z\n- Có hai nút Xóa và Hủy'),
    (5, 'Bấm Hủy thì không xóa', 'P0',
     'Đang mở hộp xác nhận xóa.',
     '1. Bấm Hủy\n2. Xem lại lưới', '—',
     '- Hộp đóng, hạng mục vẫn còn nguyên'),
    (6, 'Xóa thành công', 'P0',
     'Hạng mục Z đang xóa được.',
     '1. Bấm thùng rác ở dòng Z\n2. Bấm Xóa xác nhận\n3. Xem lưới', '—',
     '- Thông báo xóa thành công\n- Hạng mục Z biến mất khỏi danh sách'),
    (7, 'Chặn xóa hạng mục đã phát sinh khi bỏ qua giao diện', 'P0',
     'Hạng mục Y đã được dùng trong báo giá.',
     '1. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa cho Y\n2. Kiểm tra danh mục', '—',
     '- Hệ thống từ chối và nêu lý do\n- Y vẫn còn trong danh mục'),
]

SEC_VII = [
    (1, 'Nút Khóa nằm trong nút ba chấm', 'P0',
     'Hạng mục Z đang Hoạt động và xóa được.',
     '1. Bấm nút ba chấm ở dòng Z\n2. Đọc các mục trong menu', '—',
     '- Menu có ba mục: Khóa, In, Lịch sử\n'
     '- ⚠️ Sửa và Xóa nằm THẲNG trên cột, không nằm trong menu này'),
    (2, 'Khóa một hạng mục đang Hoạt động', 'P0',
     'Hạng mục Z đang Hoạt động.',
     '1. Mở nút ba chấm ở dòng Z, chọn Khóa\n2. Đọc hộp xác nhận\n3. Bấm Khóa', '—',
     '- Hộp xác nhận nêu rõ tên Z\n'
     '- Thông báo thành công, cột Trạng thái đổi thành Khóa\n'
     '- ⚠️ Z VẪN nằm trong danh sách'),
    (3, 'Hủy ở hộp xác nhận khóa', 'P0',
     'Hạng mục Z đang Hoạt động.',
     '1. Chọn Khóa ở dòng Z\n2. Bấm Hủy\n3. Xem cột Trạng thái', '—',
     '- Trạng thái vẫn là Hoạt động, không có thông báo thành công'),
    (4, 'Sau khi Khóa thì mất nút Sửa và Xóa', 'P0',
     'Vừa khóa hạng mục Z.',
     '1. Quan sát cột Hành động của dòng Z', '—',
     '- ⚠️ Chỉ còn ba nút: Mở khóa, In, Lịch sử'),
    (5, 'Mở khóa hạng mục', 'P0',
     'Hạng mục Z đang ở trạng thái Khóa.',
     '1. Chọn Mở khóa ở dòng Z\n2. Xác nhận\n3. Xem cột Trạng thái và cột Hành động', '—',
     '- Trạng thái đổi thành Hoạt động\n- Nút Sửa hiện trở lại'),
    (6, 'Hạng mục đã Khóa không chọn được ở nghiệp vụ', 'P0',
     'Hạng mục Z vừa bị Khóa.',
     '1. Mở màn lập báo giá dịch vụ hoặc phiếu sửa chữa\n2. Tìm Z ở ô chọn công việc / lỗi', '—',
     '- Z KHÔNG xuất hiện trong danh sách chọn\n'
     '- ⚠️ Đây là mục đích chính của thao tác Khóa'),
    (7, 'Khóa không làm mất dữ liệu', 'P0',
     'Hạng mục Y đã được dùng trong 2 báo giá.',
     '1. Khóa Y\n2. Mở lại 2 báo giá đó', '—',
     '- Hai báo giá vẫn hiển thị đầy đủ thông tin hạng mục Y\n'
     '- ⚠️ Khóa chỉ đổi trạng thái, KHÔNG xóa dữ liệu'),
    (8, 'Khóa ghi vào lịch sử', 'P1',
     'Vừa khóa hạng mục Z.',
     '1. Mở Lịch sử của Z\n2. Đọc dòng trên cùng', '—',
     '- Có dòng ghi nhận đổi trạng thái, kèm người thực hiện và thời điểm'),
    (9, 'Khóa hạng mục đã bị người khác khóa', 'P1',
     'Hai người cùng mở danh sách. Người A vừa khóa Z, người B chưa tải lại trang.',
     '1. Người B chọn Khóa ở dòng Z\n2. Xác nhận', '—',
     '- Hệ thống báo dữ liệu đã thay đổi\n- Không treo trang, không báo lỗi khó hiểu'),
]

SEC_VIII = [
    (1, 'Xuất tệp bảng tính theo bộ lọc', 'P0',
     'Bộ lọc đang cho ra 25 hạng mục.',
     '1. Bấm Xuất Excel\n2. Mở tệp, đếm số dòng dữ liệu', '—',
     '- Tệp có đúng 25 dòng dữ liệu, không kể dòng tiêu đề\n'
     '- ⚠️ Xuất theo bộ lọc chứ không xuất toàn danh mục'),
    (2, 'Xuất tệp khi đang ở trang giữa', 'P0',
     'Bộ lọc cho ra 60 hạng mục, đang xem trang 2.',
     '1. Bấm Xuất Excel\n2. Đếm số dòng trong tệp', '—',
     '- ⚠️ Tệp có đủ 60 dòng của TOÀN BỘ kết quả lọc, không phải chỉ trang đang xem'),
    (3, 'Cột thuế suất trong tệp xuất', 'P0',
     'Có hạng mục với VAT = 8 và hạng mục với VAT = 10.',
     '1. Xuất Excel\n2. Tìm cột thuế suất, đối chiếu hai hạng mục trên', '—',
     '- Cột thuế suất có mặt trong tệp và đúng giá trị của từng hạng mục'),
    (4, 'Số liệu trong tệp đúng định dạng', 'P1',
     'Có hạng mục với đơn giá bán 1.500.000.',
     '1. Xuất Excel\n2. Đọc ô đơn giá bán của hạng mục đó', '—',
     '- Giá trị là kiểu số, tính toán được\n'
     '- ⚠️ Không bị cảnh báo lưu số dưới dạng chữ'),
    (5, 'Tiếng Việt trong tệp xuất', 'P0',
     'Có hạng mục tên chứa dấu tiếng Việt.',
     '1. Xuất Excel\n2. Mở tệp bằng phần mềm bảng tính', '—',
     '- ⚠️ Tiếng Việt hiển thị đúng dấu, không lỗi phông chữ'),
    (6, 'Xuất khi bộ lọc không có kết quả', 'P1',
     'Bộ lọc cho ra 0 hạng mục.',
     '1. Bấm Xuất Excel\n2. Mở tệp', '—',
     '- Hoặc hệ thống báo không có dữ liệu, hoặc tệp chỉ có dòng tiêu đề\n'
     '- Không báo lỗi kỹ thuật'),
    (7, 'In danh sách theo bộ lọc', 'P0',
     'Bộ lọc đang cho ra 25 hạng mục.',
     '1. Bấm In danh sách\n2. Xem bản in', '—',
     '- Bản in có đủ 25 hạng mục\n'
     '- Có tiêu đề đầu trang của công ty\n- Nội dung không bị cắt lề'),
    (8, 'In chi tiết một hạng mục', 'P0',
     'Hạng mục A có 3 thiết bị áp dụng và 2 dịch vụ kèm theo.',
     '1. Mở nút ba chấm ở dòng A, chọn In\n2. Xem bản in', '—',
     '- Bản in chi tiết hiện đủ thông tin hạng mục, 3 thiết bị và 2 dịch vụ'),
    (9, 'In được cả hạng mục đã Khóa', 'P1',
     'Hạng mục B đang ở trạng thái Khóa.',
     '1. Mở nút ba chấm ở dòng B\n2. Chọn In', '—',
     '- ⚠️ Thao tác In VẪN dùng được với hạng mục đã Khóa'),
    (10, 'Bản in nhiều trang', 'P1',
     'Bộ lọc cho ra hơn 50 hạng mục.',
     '1. Bấm In danh sách\n2. Cuộn qua các trang của bản in', '—',
     '- Bảng không bị mất viền khi sang trang\n- Không có dòng nào bị cắt ngang'),
]

SEC_IX = [
    (1, 'Mở cửa sổ Lịch sử', 'P0',
     'Hạng mục A đã được sửa ít nhất 1 lần.',
     '1. Mở nút ba chấm ở dòng A, chọn Lịch sử\n2. Quan sát cửa sổ', '—',
     '- Cửa sổ "Lịch sử thay đổi" mở ra\n'
     '- Dòng phụ ghi rõ "Công việc / lỗi thiết bị" và tên hạng mục'),
    (2, 'Thứ tự mới nhất ở trên cùng', 'P0',
     'Hạng mục A đã được sửa 3 lần vào 3 thời điểm khác nhau.',
     '1. Mở Lịch sử của A\n2. Đọc thời điểm 3 dòng từ trên xuống', '—',
     '- ⚠️ Dòng trên cùng là lần sửa MỚI NHẤT'),
    (3, 'Mỗi dòng nêu đủ thông tin', 'P0',
     'Vừa đổi Định mức công của hạng mục A từ 2 thành 3.',
     '1. Mở Lịch sử của A\n2. Đọc dòng trên cùng', '—',
     '- Nêu rõ trường Định mức công, giá trị cũ 2, giá trị mới 3\n'
     '- Kèm tên người thực hiện và thời điểm tới phút'),
    (4, 'Hạng mục chưa từng sửa', 'P1',
     'Hạng mục Y vừa được tạo, chưa sửa lần nào.',
     '1. Mở Lịch sử của Y', '—',
     '- Cửa sổ hiện "Chưa có lịch sử thao tác nào."\n- Không báo lỗi'),
    (5, 'Đóng cửa sổ Lịch sử', 'P2',
     'Đang mở cửa sổ Lịch sử, danh sách phía sau đang lọc và ở trang 2.',
     '1. Bấm Đóng', '—',
     '- Cửa sổ đóng, danh sách giữ nguyên bộ lọc và trang 2'),
]

SEC_X = [
    (1, 'Hai người cùng sửa một hạng mục', 'P0',
     'Người A và người B cùng mở trang sửa hạng mục X.',
     '1. Người A đổi tên thành "A1", bấm Lưu\n'
     '2. Người B (chưa tải lại) đổi tên thành "B1", bấm Lưu\n3. Mở lại X', 'A1 / B1',
     '- Ghi nhận rõ kết quả cuối cùng và cách hệ thống xử lý\n'
     '- ⚠️ Không được mất dữ liệu ngầm mà không báo gì\n- Lịch sử ghi nhận cả hai lần sửa'),
    (2, 'Sửa hạng mục vừa bị người khác khóa', 'P1',
     'Người A vừa khóa X. Người B đang mở trang sửa X từ trước.',
     '1. Người B bấm Lưu\n2. Quan sát', '—',
     '- Hệ thống báo dữ liệu đã thay đổi, không treo trang'),
    (3, 'Luồng tổng hợp — tạo, sửa, khóa, mở khóa, xem lịch sử', 'P0',
     'Tài khoản có quyền "%s".' % QUYEN,
     '1. Tạo mới một hạng mục đủ trường bắt buộc và 1 thiết bị\n'
     '2. Tìm hạng mục đó trên lưới\n3. Sửa Định mức công, lưu\n'
     '4. Khóa hạng mục, xác nhận\n5. Mở khóa lại\n6. Mở Lịch sử', '—',
     '- Mỗi bước đều thành công, thông báo rõ ràng\n'
     '- Lịch sử có đủ các mốc: sửa và đổi trạng thái hai lần\n'
     '- Thứ tự lịch sử mới nhất ở trên cùng'),
    (4, 'Luồng tổng hợp — tạo rồi dùng ngay ở báo giá', 'P0',
     'Tài khoản có quyền quản lý danh mục và quyền lập báo giá dịch vụ.',
     '1. Tạo mới một hạng mục\n2. Mở màn lập báo giá dịch vụ\n'
     '3. Tìm hạng mục vừa tạo ở ô chọn công việc / lỗi', '—',
     '- Hạng mục mới xuất hiện ngay trong danh sách chọn, không cần đăng nhập lại'),
    (5, 'Luồng tổng hợp — lọc, tuỳ chỉnh cột rồi xuất tệp', 'P1',
     'Tài khoản có quyền "%s".' % QUYEN,
     '1. Lọc theo Loại và Trạng thái\n2. Bật thêm cột Đơn giá bán và Định mức công\n'
     '3. Bấm Xuất Excel\n4. Mở tệp đối chiếu với lưới', '—',
     '- Số dòng trong tệp khớp tổng số bản ghi của bộ lọc\n'
     '- Dữ liệu từng dòng khớp với lưới'),
    (6, 'Hạng mục trùng tên khác loại hoạt động độc lập', 'P0',
     'Có hai hạng mục cùng tên "Kiểm tra cầu nâng" ở hai loại khác nhau.',
     '1. Sửa hạng mục thuộc loại thứ nhất, đổi Định mức công\n'
     '2. Mở hạng mục thuộc loại thứ hai, đọc Định mức công', '—',
     '- ⚠️ Hạng mục thứ hai KHÔNG bị ảnh hưởng — hai bản ghi hoàn toàn độc lập'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', SEC_I),
    ('II', 'TÌM KIẾM & LỌC DANH SÁCH', SEC_II),
    ('III', 'TUỲ CHỈNH CỘT HIỂN THỊ', SEC_III),
    ('IV', 'THÊM MỚI', SEC_IV),
    ('V', 'CHỈNH SỬA', SEC_V),
    ('VI', 'XÓA', SEC_VI),
    ('VII', 'KHÓA / MỞ KHÓA', SEC_VII),
    ('VIII', 'IN VÀ XUẤT TỆP BẢNG TÍNH', SEC_VIII),
    ('IX', 'LỊCH SỬ THAY ĐỔI', SEC_IX),
    ('X', 'THAO TÁC ĐỒNG THỜI & LUỒNG TỔNG HỢP', SEC_X),
]

if __name__ == '__main__':
    build(output_file=os.path.join(HERE, 'testcase - %s.xlsx' % TEN.replace('/', '-')),
          sheet_name='Trang tính1',
          feature_name='%s - Cập nhật ngày 18/08/2026' % TEN,
          module_name='DM công việc, lỗi thiết bị',
          description_block=DESCRIPTION_BLOCK,
          role_tcs=ROLE_TCS, sections=SECTIONS)
