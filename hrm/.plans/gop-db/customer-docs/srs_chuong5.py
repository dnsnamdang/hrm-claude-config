# -*- coding: utf-8 -*-
"""Chuong 5 (dac ta chi tiet tung chuc nang) + chuong 6 cua SRS man Danh muc khach hang."""

ACTOR_QL = 'Nhân viên quản lý khách hàng'
ACTOR_XEM = 'Người dùng đã đăng nhập'


def build(d, shot):
    # ============================================================ 5. ĐẶC TẢ CHI TIẾT
    d.h1('5. Đặc tả chi tiết theo từng chức năng')

    d.h2('5.1 Sơ đồ UML tổng quan')
    d.overview_figure(
        'HỆ THỐNG HRM — DANH MỤC KHÁCH HÀNG',
        [('Nhân viên quản lý khách hàng', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
         ('Người dùng chỉ có quyền xem', [0, 1, 2, 3, 6, 8])],
        [('FR-01', 'Truy cập & xem danh sách', 'view', None),
         ('FR-02', 'Tìm kiếm & lọc nâng cao', 'view', None),
         ('FR-03', 'Cài đặt bộ lọc', 'view', None),
         ('FR-04', 'Tuỳ chỉnh cột', 'view', None),
         ('FR-05', 'Tạo mới khách hàng', 'crud', None),
         ('FR-06', 'Chỉnh sửa khách hàng', 'crud', None),
         ('FR-07', 'Xem chi tiết', 'view', None),
         ('FR-08', 'Khóa / Mở khóa', 'action', '«extend» Khóa không xóa dữ liệu'),
         ('FR-09', 'Lịch sử thay đổi', 'view', None),
         ('FR-10', 'Nhập từ file Excel', 'io', None),
         ('FR-11', 'Xuất CSV / Excel / PDF', 'io', None),
         ('FR-12', 'Màn Quản lý khách hàng', 'view', None)],
        'Sơ đồ Use Case tổng quan màn Danh mục khách hàng')

    d.h2('5.2 Đặc tả chi tiết từng chức năng')

    # ---------------------------------------------------------- FR-01
    d.h3('5.2.1 FR-01 — Truy cập và xem danh sách khách hàng')

    d.p('5.2.1.1 Giới thiệu')
    d.intro_table(
        'Truy cập và xem danh sách khách hàng',
        'Hiển thị bảng khách hàng nằm trong phạm vi dữ liệu của người đăng nhập, kèm phân trang '
        'và ô thống kê tổng số bản ghi khớp bộ lọc.',
        '%s; %s' % (ACTOR_QL, ACTOR_XEM),
        'Người dùng đã đăng nhập vào hệ thống. Không cần quyền riêng để mở màn hình này.',
        '1. Người dùng vào menu Giao việc → Danh mục chung → Danh mục khách hàng.\n'
        '2. Hệ thống xác định phạm vi dữ liệu theo cấp quyền xem của người dùng.\n'
        '3. Hệ thống áp thêm lớp bảo vệ khách hàng cá nhân.\n'
        '4. Hệ thống trả về trang đầu tiên của danh sách và tổng số bản ghi.\n'
        '5. Bảng hiển thị dữ liệu, ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
        '• Không có bản ghi nào trong phạm vi → bảng hiện thông báo không có dữ liệu, N = 0.\n'
        '• Người dùng không có cấp quyền xem nào → chỉ thấy khách hàng do chính mình tạo.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
        '')

    d.p('5.2.1.2 Layout màn hình')
    d.layout(shot=shot('kh_01_danhsach.png'),
             shot_caption='Màn Danh mục khách hàng lúc mới truy cập')

    d.p('5.2.1.3 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–', 'Danh sách khách hàng',
         'Tiêu đề cố định phía trên bảng.'),
        ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi thiếu quyền',
         'Chỉ hiện khi có quyền Thêm khách hàng.'),
        ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi thiếu quyền',
         'Chỉ hiện khi có quyền Thêm khách hàng.'),
        ('Nút Xuất CSV / Xuất Excel / Xuất PDF', 'Button', 'Enable / Ẩn', '–', '–',
         'Ẩn khi thiếu quyền', 'Chỉ hiện khi có quyền Xuất dữ liệu khách hàng.'),
        ('Biểu tượng Tuỳ chỉnh cột', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
         'Mở cửa sổ bật / tắt và sắp xếp cột.'),
        ('Cột STT', 'Table/Grid', 'Read-only', '≥ 1', '–', 'Số thứ tự liên tục',
         'Luôn hiển thị, không tắt được. Tiếp tục tăng qua các trang.'),
        ('Cột Mã KH', 'Table/Grid', 'Read-only', '–', '–', 'Mã sinh tự động',
         'Luôn hiển thị, không tắt được. Bấm vào mở màn chi tiết.'),
        ('Cột Tên khách hàng', 'Table/Grid', 'Read-only', '0–255 ký tự', '–', 'Trống', '–'),
        ('Cột Tên viết tắt', 'Table/Grid', 'Read-only', '0–255 ký tự', '–', 'Trống', '–'),
        ('Cột Loại', 'Table/Grid', 'Read-only', 'Danh sách 5 giá trị', '–', 'Trống',
         'Cá nhân / Doanh nghiệp tư nhân / Doanh nghiệp nước ngoài / Tổ chức phi chính phủ / '
         'Cơ quan nhà nước.'),
        ('Cột MST', 'Table/Grid', 'Read-only', '1–14 ký tự số và gạch ngang', '–', 'Trống', '–'),
        ('Cột SĐT', 'Table/Grid', 'Read-only', 'Danh sách', '–', 'Trống',
         'Nhiều số ngăn nhau bằng dấu phẩy.'),
        ('Cột Email', 'Table/Grid', 'Read-only', '0–255 ký tự', '–', 'Trống', '–'),
        ('Cột Nhóm KH', 'Table/Grid', 'Read-only', 'Danh sách', '–', 'Trống',
         'Nhiều nhóm ngăn nhau bằng dấu phẩy.'),
        ('Cột Địa chỉ / Tỉnh–TP / Tên đơn vị / Địa chỉ xuất hóa đơn', 'Table/Grid', 'Read-only',
         '–', '–', 'Trống', '–'),
        ('Cột Công ty mẹ / Hãng xe / Người tạo / Người sửa (gần nhất)', 'Table/Grid', 'Read-only',
         '–', '–', 'Ẩn',
         'Bốn cột này MẶC ĐỊNH ẨN vì làm chậm truy vấn đếm; bật lên ở cửa sổ Tuỳ chỉnh cột.'),
        ('Cột Trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', '–', 'Hoạt động',
         'Hai trạng thái khác màu rõ ràng.'),
        ('Cột Hành động', 'Icon Button', 'Enable / Disable', '–', '–', 'Hiển thị',
         'Gồm biểu tượng bút chì (Sửa), ổ khóa (Khóa / Mở khóa) và menu ba chấm '
         '(Quản lý, Lịch sử). Thiếu quyền thì làm mờ chứ không ẩn.'),
        ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', '–', 'Theo kết quả',
         'N là tổng số khách hàng khớp bộ lọc, không phải tổng toàn hệ thống.'),
        ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1',
         'Có nút về đầu / lùi / số trang / tiến / về cuối và ô chọn số dòng mỗi trang.'),
        ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
         'Hiện thông báo không có dữ liệu kèm hình minh họa khi N = 0.'),
        ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', '–', 'Ẩn',
         'Hiện trong lúc nạp dữ liệu.'),
    ])

    d.p('5.2.1.4 Tiêu chí nghiệm thu')
    d.bullets([
        'Người dùng có quyền Xem tất cả khách hàng thấy đúng tổng số khách hàng của hệ thống.',
        'Người dùng cấp công ty / phòng ban / bộ phận chỉ thấy phần dữ liệu tương ứng; khách hàng '
        'của đơn vị khác không xuất hiện kể cả khi tìm đúng tên.',
        'Người dùng không có cấp quyền xem nào vẫn mở được màn hình và thấy khách hàng của mình.',
        'Khách hàng đã Khóa vẫn nằm trong danh sách với nhãn Khóa.',
        'Bốn cột nặng mặc định ẩn khi người dùng chưa từng chỉnh cấu hình cột.',
    ])

    d.p('5.2.1.5 Danh sách event và xử lý event')
    d.event_table([
        ('Mở màn hình', 'System',
         'Before:\n– Xác định cấp quyền xem của người dùng theo thứ tự ưu tiên.\n'
         'During:\n– Áp phạm vi dữ liệu; áp thêm lớp bảo vệ khách hàng cá nhân.\n'
         'After:\n– Trả về trang 1 và tổng số bản ghi; hiển thị bảng.'),
        ('Bấm số trang / nút tiến lùi', 'Click',
         'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
         'After:\n– Nạp lại dữ liệu trang mới, số thứ tự tiếp tục liên tục.'),
        ('Đổi số dòng mỗi trang', 'Change',
         'After:\n– Quay về trang 1 và nạp lại theo số dòng mới.'),
        ('Bấm mã khách hàng', 'Click',
         'After:\n– Mở màn chi tiết khách hàng ở chế độ chỉ đọc.'),
    ])

    # ---------------------------------------------------------- FR-02
    d.h3('5.2.2 FR-02 — Tìm kiếm và bộ lọc nâng cao')

    d.p('5.2.2.1 Giới thiệu')
    d.intro_table(
        'Tìm kiếm và bộ lọc nâng cao',
        'Thu hẹp danh sách bằng ô tìm nhanh và 19 tiêu chí lọc nâng cao.',
        '%s; %s' % (ACTOR_QL, ACTOR_XEM),
        'Đang ở màn Danh mục khách hàng.',
        '1. Người dùng gõ từ khóa vào ô tìm nhanh hoặc bấm nút Bộ lọc nâng cao.\n'
        '2. Người dùng chọn / nhập các tiêu chí cần lọc.\n'
        '3. Người dùng bấm Tìm kiếm.\n'
        '4. Hệ thống áp đồng thời mọi tiêu chí theo kiểu “và”, trong phạm vi dữ liệu của '
        'người dùng.\n'
        '5. Bảng nạp lại từ trang 1, tổng số bản ghi cập nhật theo kết quả.',
        '• Không có kết quả → bảng hiện thông báo không có dữ liệu, tổng bằng 0.\n'
        '• Bấm Làm mới → xóa toàn bộ tiêu chí VÀ nạp lại danh sách đầy đủ ngay lập tức.\n'
        '• Đóng cửa sổ bộ lọc mà không bấm Tìm kiếm → kết quả trên bảng không đổi.\n'
        '• Gõ đúng trọn vẹn số điện thoại → hiện được cả khách hàng cá nhân tự do ngoài phạm vi.',
        '')

    d.p('5.2.2.2 Layout màn hình')
    d.layout(shot=shot('kh_02_boloc_nangcao.png'),
             shot_caption='Panel Bộ lọc nâng cao đang mở với đầy đủ tiêu chí')

    d.p('5.2.2.3 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Tìm theo tên, mã khách hàng, mã số thuế hoặc số điện thoại.'),
        ('Nút Bộ lọc nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Mở panel bộ lọc; hiện kèm SỐ TIÊU CHÍ đang có giá trị.'),
        ('Công ty – Phòng ban – Bộ phận – Nhân viên', 'Dropdown', 'Enable', 'Danh sách', 'Không',
         'Trống', 'Chọn theo cây đơn vị tới cấp nhân viên.'),
        ('Quốc gia', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
         'Quyết định danh sách của ô Tỉnh/Thành phố.'),
        ('Tỉnh/Thành phố', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
         'Xóa trắng và nạp lại khi đổi Quốc gia.'),
        ('Mã khách hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Khớp một phần.'),
        ('MST/SĐT', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Tìm trên cả mã số thuế và từng số điện thoại.'),
        ('Tên khách hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Khớp một phần.'),
        ('Số CCCD', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
        ('Tên đơn vị', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
        ('Loại hình tổ chức', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống', '–'),
        ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khóa', 'Không', 'Trống',
         'Bỏ trống thì hiện cả hai trạng thái.'),
        ('Loại hình hoạt động – Lĩnh vực kinh doanh', 'Dropdown', 'Enable', 'Danh sách cặp',
         'Không', 'Trống', 'Chọn theo CẶP, không chọn rời từng vế.'),
        ('Người sửa gần nhất', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', '–'),
        ('Khách hàng hãng', 'Dropdown', 'Enable', 'Có / Không', 'Không', 'Trống', '–'),
        ('Hãng xe', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', '–'),
        ('Cấp đại lý', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', '–'),
        ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng bộ lọc.'),
        ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Xóa hết tiêu chí VÀ nạp lại danh sách ngay.'),
    ])

    d.p('5.2.2.4 Tiêu chí nghiệm thu')
    d.bullets([
        'Các tiêu chí kết hợp theo kiểu “và”; chọn ba tiêu chí thì chỉ khách hàng thỏa cả ba mới ra.',
        'Ô tìm nhanh không xóa bộ lọc nâng cao đang áp dụng và ngược lại.',
        'Nút Làm mới nạp lại danh sách ngay, không chỉ xóa ô lọc trên giao diện.',
        'Tìm đúng trọn vẹn số điện thoại hiện được khách hàng cá nhân tự do; thiếu một chữ số thì '
        'không ra.',
        'Áp dụng bộ lọc khi đang ở trang giữa thì bảng quay về trang 1, không hiện trang trống.',
        'Đổi Quốc gia thì ô Tỉnh/Thành phố bị xóa trắng và nạp lại.',
    ])

    d.p('5.2.2.5 Danh sách event và xử lý event')
    d.event_table([
        ('Gõ vào ô tìm nhanh', 'Keypress',
         'During:\n– Chờ người dùng ngừng gõ rồi mới gọi tìm kiếm.\n'
         'After:\n– Nạp lại bảng từ trang 1; giữ nguyên bộ lọc nâng cao đang áp dụng.'),
        ('Bấm Tìm kiếm', 'Click',
         'Before:\n– Thu thập giá trị của mọi tiêu chí đang có.\n'
         'During:\n– Áp đồng thời các tiêu chí theo kiểu “và” trong phạm vi dữ liệu.\n'
         'After:\n– Nạp lại bảng từ trang 1; cập nhật ô “Hiển thị a–b / N”; cập nhật số trên nút '
         'Bộ lọc nâng cao.'),
        ('Bấm Làm mới', 'Click',
         'After:\n– Xóa trắng mọi tiêu chí VÀ nạp lại danh sách đầy đủ ngay lập tức.'),
        ('Đổi Quốc gia', 'Change',
         'After:\n– Xóa trắng ô Tỉnh/Thành phố và nạp lại danh sách theo quốc gia mới.'),
    ])

    # ---------------------------------------------------------- FR-03
    d.h3('5.2.3 FR-03 — Cài đặt bộ lọc')

    d.p('5.2.3.1 Biểu đồ Usecase')
    d.uc_figure('FR-03', 'Cài đặt bộ lọc', 'view',
                [('include', 'Ghi nhớ cấu hình theo người dùng')],
                actor=ACTOR_XEM)

    d.p('5.2.3.2 Giới thiệu')
    d.intro_table(
        'Cài đặt bộ lọc',
        'Cho phép người dùng chọn những ô lọc nào hiển thị trên panel bộ lọc nâng cao và sắp xếp '
        'thứ tự của chúng. Cấu hình được ghi nhớ riêng cho từng người dùng.',
        '%s; %s' % (ACTOR_QL, ACTOR_XEM),
        'Đang mở panel Bộ lọc nâng cao.',
        '1. Người dùng bấm Cài đặt bộ lọc.\n'
        '2. Hệ thống hiển thị danh sách 15 ô lọc có thể cấu hình, kèm ô tích và tay nắm kéo.\n'
        '3. Người dùng tích / bỏ tích, kéo đổi thứ tự.\n'
        '4. Người dùng bấm Lưu.\n'
        '5. Hệ thống ghi nhớ cấu hình và cập nhật lại panel bộ lọc.',
        '• Bỏ tích ô lọc đang có giá trị → ô biến mất khỏi giao diện nhưng GIÁ TRỊ LỌC VẪN CÒN '
        'tác dụng cho tới khi bấm Làm mới.\n'
        '• Đóng cửa sổ không bấm Lưu → cấu hình không đổi.',
        'Cấu hình lưu theo từng người dùng và từng màn hình; người dùng khác không bị ảnh hưởng.')

    d.p('5.2.3.3 Layout màn hình')
    d.layout(modal='Cài đặt bộ lọc', shot=shot('kh_03_caidat_boloc.png'),
             shot_caption='Cửa sổ Cài đặt bộ lọc với danh sách ô lọc cấu hình được')

    d.p('5.2.3.4 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Nằm trong panel Bộ lọc nâng cao.'),
        ('Danh sách ô lọc', 'Table/Grid', 'Enable', '15 mục', '–', 'Theo cấu hình đã lưu',
         'Mỗi dòng có ô tích và tay nắm kéo.'),
        ('Ô tích chọn', 'Icon Button', 'Enable', '–', 'Không', 'Theo cấu hình đã lưu',
         'Bật / tắt hiển thị của ô lọc tương ứng.'),
        ('Tay nắm kéo', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo để đổi thứ tự.'),
        ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi nhận cấu hình.'),
        ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, bỏ qua thay đổi.'),
    ])

    d.p('5.2.3.5 Tiêu chí nghiệm thu')
    d.bullets([
        'Bỏ tích một ô lọc thì ô đó biến mất khỏi panel bộ lọc nâng cao.',
        'Cấu hình còn nguyên sau khi tải lại trang và sau khi đăng nhập lại.',
        'Người dùng khác không bị ảnh hưởng bởi cấu hình của mình.',
        'Ẩn ô lọc KHÔNG làm mất giá trị lọc đang áp dụng — kết quả trên bảng không đổi.',
    ])

    d.p('5.2.3.6 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm Cài đặt bộ lọc', 'Click',
         'After:\n– Mở cửa sổ, nạp danh sách ô lọc theo cấu hình đã lưu của người dùng.'),
        ('Tích / bỏ tích ô lọc', 'Change',
         'During:\n– Cập nhật trạng thái tạm trong cửa sổ, chưa ghi nhận.'),
        ('Kéo đổi thứ tự', 'Change',
         'During:\n– Cập nhật thứ tự tạm trong cửa sổ.'),
        ('Bấm Lưu', 'Click',
         'After:\n– Ghi nhận cấu hình cho người dùng hiện tại; đóng cửa sổ; cập nhật lại panel '
         'bộ lọc.\n– Hiển thị thông báo “Lưu cấu hình thành công”.'),
    ])

    # ---------------------------------------------------------- FR-04
    d.h3('5.2.4 FR-04 — Tuỳ chỉnh cột hiển thị')

    d.p('5.2.4.1 Biểu đồ Usecase')
    d.uc_figure('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view',
                [('include', 'Ghi nhớ cấu hình theo người dùng'),
                 ('extend', 'Khóa cứng cột STT và Mã KH')],
                actor=ACTOR_XEM)

    d.p('5.2.4.2 Giới thiệu')
    d.intro_table(
        'Tuỳ chỉnh cột hiển thị',
        'Cho phép bật / tắt và sắp xếp các cột của bảng danh sách. Cấu hình ghi nhớ theo từng '
        'người dùng.',
        '%s; %s' % (ACTOR_QL, ACTOR_XEM),
        'Đang ở màn Danh mục khách hàng.',
        '1. Người dùng bấm biểu tượng Tuỳ chỉnh cột.\n'
        '2. Hệ thống hiển thị danh sách 20 cột kèm ô tích và tay nắm kéo.\n'
        '3. Người dùng tích / bỏ tích, kéo đổi thứ tự.\n'
        '4. Người dùng bấm Lưu.\n'
        '5. Bảng vẽ lại theo cấu hình mới.',
        '• Cột STT và Mã KH bị khóa, không bỏ tích được.\n'
        '• Bật một trong bốn cột Công ty mẹ / Hãng xe / Người tạo / Người sửa → truy vấn nặng '
        'hơn, thời gian nạp bảng tăng.\n'
        '• Bấm khôi phục mặc định → bảng trở về cấu hình gốc.',
        'Bốn cột nặng mặc định ẩn để không phải trả giá hiệu năng khi người dùng không cần.')

    d.p('5.2.4.3 Layout màn hình')
    d.layout(modal='Tuỳ chỉnh cột', shot=shot('kh_04_cauhinh_cot.png'),
             shot_caption='Cửa sổ Tuỳ chỉnh cột — STT và Mã KH bị khóa luôn hiển thị')

    d.p('5.2.4.4 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Biểu tượng Tuỳ chỉnh cột', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
         'Nằm ở góc phải thanh công cụ.'),
        ('Danh sách cột', 'Table/Grid', 'Enable', '20 mục', '–', 'Theo cấu hình đã lưu', '–'),
        ('Ô tích cột STT', 'Icon Button', 'Disable', '–', '–', 'Đã tích',
         'Bị khóa, không bỏ tích được.'),
        ('Ô tích cột Mã KH', 'Icon Button', 'Disable', '–', '–', 'Đã tích',
         'Bị khóa, không bỏ tích được.'),
        ('Ô tích các cột còn lại', 'Icon Button', 'Enable', '–', 'Không',
         'Theo cấu hình đã lưu', '–'),
        ('Nút khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Trả bảng về cấu hình gốc.'),
        ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi nhận cấu hình.'),
    ])

    d.p('5.2.4.5 Tiêu chí nghiệm thu')
    d.bullets([
        'Bật cột ẩn thì cột hiện trên bảng kèm dữ liệu đúng.',
        'Không bỏ tích được cột STT và Mã KH.',
        'Cấu hình ghi nhớ theo tài khoản, không lây sang tài khoản khác.',
        'Bốn cột nặng mặc định ẩn với người dùng chưa từng chỉnh cấu hình.',
    ])

    d.p('5.2.4.6 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm biểu tượng Tuỳ chỉnh cột', 'Click',
         'After:\n– Mở cửa sổ, nạp cấu hình cột đã lưu.'),
        ('Tích / bỏ tích cột', 'Change',
         'During:\n– Cột STT và Mã KH không cho đổi trạng thái.\n'
         '– Các cột khác cập nhật trạng thái tạm.'),
        ('Bấm Lưu', 'Click',
         'After:\n– Ghi nhận cấu hình; vẽ lại bảng; nếu có bật cột nặng thì gọi lại dữ liệu kèm '
         'các cột đó.'),
        ('Bấm khôi phục mặc định', 'Click',
         'After:\n– Đặt lại cấu hình gốc và vẽ lại bảng.'),
    ])
