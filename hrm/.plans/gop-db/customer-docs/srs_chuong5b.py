# -*- coding: utf-8 -*-
"""Chuong 5 phan 2 (FR-05 -> FR-12) + chuong 6 cua SRS man Danh muc khach hang."""

ACTOR_QL = 'Nhân viên quản lý khách hàng'
ACTOR_XEM = 'Người dùng đã đăng nhập'


def build(d, shot):
    # ---------------------------------------------------------- FR-05
    d.h3('5.2.5 FR-05 — Tạo mới khách hàng')

    d.p('5.2.5.1 Biểu đồ Usecase')
    d.uc_figure('FR-05', 'Tạo mới khách hàng', 'crud',
                [('include', 'Kiểm tra quyền Thêm khách hàng'),
                 ('include', 'Kiểm tra trùng mã số thuế / email / số CMND-CCCD'),
                 ('extend', 'Mã số thuế không bắt buộc khi đã chọn Công ty mẹ')],
                actor=ACTOR_QL)

    d.p('5.2.5.2 Giới thiệu')
    d.intro_table(
        'Tạo mới khách hàng',
        'Thêm một khách hàng mới vào danh mục. Form gồm nhiều khối, các khối hiện ra tuỳ theo '
        'Loại hình tổ chức được chọn. Mã khách hàng do hệ thống sinh tự động.',
        ACTOR_QL,
        'Người dùng có quyền Thêm khách hàng.',
        '1. Người dùng bấm nút Tạo mới.\n'
        '2. Hệ thống mở màn thêm mới, ban đầu chỉ hiện khối Thông tin khách hàng.\n'
        '3. Người dùng chọn Loại hình tổ chức; hệ thống hiện thêm các khối tương ứng.\n'
        '4. Người dùng nhập thông tin và bấm Lưu.\n'
        '5. Hệ thống kiểm tra dữ liệu, sinh mã khách hàng và ghi bản ghi mới.\n'
        '6. Hệ thống hiển thị thông báo thành công và quay về danh sách.',
        '• Thiếu trường bắt buộc → báo lỗi đỏ ngay dưới ô tương ứng, không đóng màn, giữ nguyên '
        'dữ liệu đã nhập.\n'
        '• Trùng mã số thuế / email / số CMND-CCCD → báo lỗi tương ứng, không tạo bản ghi.\n'
        '• Chọn lĩnh vực không thuộc loại hình đã chọn → báo lỗi và yêu cầu chọn lại.\n'
        '• Thoát màn khi đã sửa mà chưa lưu → hệ thống hỏi xác nhận rời trang.',
        'Khối “Địa chỉ giao hàng” KHÔNG hiện ở màn tạo mới; chỉ hiện ở màn chỉnh sửa.')

    d.p('5.2.5.3 Layout màn hình')
    d.layout(route='/assign/customers/add',
             shot=shot('kh_09_taomoi_tochuc.png'),
             shot_caption='Form Tạo mới khách hàng khi chọn loại hình tổ chức')
    d.figure(shot('kh_08_taomoi_canhan.png'),
             'Form Tạo mới khách hàng khi chọn Loại hình tổ chức là Cá nhân', width_in=6.2)

    d.p('5.2.5.4 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Tên khách hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
         'Thiếu thì báo “Bắt buộc phải nhập”.'),
        ('Loại hình tổ chức', 'Dropdown', 'Enable', '5 giá trị', 'Có', 'Trống',
         'Cá nhân / Doanh nghiệp tư nhân / Doanh nghiệp nước ngoài / Tổ chức phi chính phủ / '
         'Cơ quan nhà nước. Quyết định các khối hiển thị bên dưới.'),
        ('Tên viết tắt', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
        ('Là nhà cung cấp', 'Icon Button', 'Enable', 'Có / Không', 'Không', 'Không tích',
         'Đánh dấu đối tác đồng thời là nhà cung cấp; vẫn chỉ một bản ghi duy nhất.'),
        ('Là khách hãng', 'Icon Button', 'Enable', 'Có / Không', 'Không', 'Không tích',
         'Tích thì bắt buộc phải chọn Hãng xe.'),
        ('Hãng xe', 'Dropdown', 'Enable', 'Danh sách', 'Có khi tích “Là khách hãng”', 'Trống',
         'Thiếu thì báo “Bắt buộc khi là khách hãng”.'),
        ('Nhóm khách hàng', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Chọn nhiều.'),
        ('Loại hình hoạt động – Lĩnh vực kinh doanh', 'Dropdown', 'Enable', 'Danh sách cặp',
         'Không', 'Trống',
         'Khai theo cặp; lĩnh vực phải thuộc loại hình đã chọn, sai thì báo “Lĩnh vực không thuộc '
         'loại hình đã chọn, vui lòng chọn lại”. Thêm được nhiều cặp.'),
        ('Email', 'Textbox', 'Enable', '0–255 ký tự, đúng định dạng email', 'Không', 'Trống',
         'Duy nhất toàn hệ thống; trùng thì báo “Email đã tồn tại”.'),
        ('Website / Ghi chú', 'Textbox / Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
        ('Quốc gia', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống',
         'Thiếu thì báo “Bắt buộc chọn quốc gia”.'),
        ('Tỉnh/Thành phố', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống',
         'Phụ thuộc Quốc gia; thiếu thì báo “Bắt buộc chọn tỉnh/thành phố”.'),
        ('Quận/Huyện', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Phụ thuộc Tỉnh/TP.'),
        ('Phường/Xã', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống',
         'Thiếu thì báo “Bắt buộc chọn phường/xã”.'),
        ('Thôn/Xóm, Số nhà – đường', 'Dropdown / Textbox', 'Enable', '0–255 ký tự', 'Không',
         'Trống', '–'),
        ('Số điện thoại (khối Thông tin cá nhân)', 'Textbox', 'Enable',
         'Bắt đầu bằng 0, dài 10–12 chữ số', 'Có với khách hàng Cá nhân', 'Trống',
         'Thêm được nhiều số. Sai định dạng thì báo “Số điện thoại không đúng định dạng”.'),
        ('Số CMND/CCCD', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Duy nhất; trùng thì báo “Số CMND/CCCD đã tồn tại”.'),
        ('Ngày sinh / Ngày cấp', 'Datepicker', 'Enable', 'dd/mm/yyyy, ≤ ngày hiện tại', 'Không',
         'Trống', 'Chọn ngày tương lai thì báo “Không được lớn hơn ngày hiện tại”.'),
        ('Nơi cấp / Tên đơn vị', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
        ('Mã số thuế (khối Thông tin tổ chức)', 'Textbox', 'Enable',
         '1–14 ký tự, chỉ chữ số và dấu gạch ngang', 'Có khi KHÔNG chọn Công ty mẹ', 'Trống',
         'Duy nhất. Sai định dạng thì báo “Mã số thuế không đúng định dạng”; trùng thì báo '
         '“Mã số thuế đã tồn tại”.'),
        ('Công ty mẹ', 'Dropdown', 'Enable', 'Danh sách khách hàng', 'Không', 'Trống',
         'Chọn công ty mẹ thì Mã số thuế trở thành không bắt buộc.'),
        ('Người đại diện + Chức vụ người đại diện', 'Textbox', 'Enable', '0–255 ký tự',
         'Có với khách hàng tổ chức', 'Trống',
         'Ít nhất một người, phải đủ cả tên và chức vụ.'),
        ('Địa chỉ xuất hoá đơn', 'Textarea', 'Enable', '–', 'Có với khách hàng tổ chức', 'Trống',
         'Thiếu thì báo “Bắt buộc nhập”.'),
        ('Fax / Số điện thoại bàn', 'Textbox', 'Enable', '0–20 ký tự', 'Không', 'Trống', '–'),
        ('Người liên hệ: Họ tên, Chức vụ, SĐT', 'Textbox', 'Enable', '0–255 ký tự',
         'Có với khách hàng tổ chức', 'Trống',
         'Ít nhất một người liên hệ, mỗi người phải có tên, chức vụ và ít nhất một số điện thoại.'),
        ('Tài khoản ngân hàng: Số TK, Chủ TK, Ngân hàng, Tỉnh/TP ngân hàng, Chi nhánh',
         'Textbox / Dropdown', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Chi nhánh phụ thuộc Ngân hàng và Tỉnh/TP ngân hàng.'),
        ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Bị khóa trong lúc đang xử lý để tránh tạo trùng bản ghi.'),
        ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
        ('Thông báo lỗi inline', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         'Chữ đỏ ngay dưới ô bị lỗi.'),
    ])

    d.p('5.2.5.5 Tiêu chí nghiệm thu')
    d.bullets([
        'Người dùng không có quyền Thêm khách hàng không thấy nút Tạo mới; gọi thẳng chức năng '
        'vẫn bị từ chối và không tạo ra bản ghi nào.',
        'Chọn Cá nhân chỉ hiện khối Thông tin cá nhân; chọn loại tổ chức hiện khối Thông tin tổ '
        'chức và khối Người liên hệ.',
        'Khối Địa chỉ giao hàng không hiện ở màn tạo mới.',
        'Mã số thuế bắt buộc khi không chọn Công ty mẹ, và không bắt buộc khi đã chọn.',
        'Bấm Lưu hai lần liên tiếp chỉ tạo ra đúng một khách hàng.',
        'Mọi thông báo lỗi khớp đúng nguyên văn quy định ở bảng mô tả giao diện.',
    ])

    d.p('5.2.5.6 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm nút Tạo mới', 'Click',
         'Before:\n– Kiểm tra quyền Thêm khách hàng.\n'
         '– Nếu không có quyền → không hiển thị nút; gọi thẳng chức năng thì từ chối với thông '
         'báo “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
         'After:\n– Mở màn thêm mới với các ô để trống.'),
        ('Đổi Loại hình tổ chức', 'Change',
         'After:\n– Hiện / ẩn các khối nhập liệu tương ứng; dữ liệu ở khối bị ẩn không được mang '
         'sang khối mới.'),
        ('Đổi Quốc gia / Tỉnh/Thành phố / Quận/Huyện', 'Change',
         'After:\n– Xóa trắng và nạp lại các cấp địa chỉ bên dưới.'),
        ('Tích “Là khách hãng”', 'Change',
         'After:\n– Ô Hãng xe chuyển thành bắt buộc.'),
        ('Bấm Lưu', 'Click',
         'Before:\n– Kiểm tra quyền Thêm khách hàng.\n'
         '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng '
         'xử lý.\n'
         'During:\n'
         '– Tên khách hàng trống → hiển thị “Bắt buộc phải nhập”.\n'
         '– Loại hình tổ chức trống → hiển thị “Bắt buộc nhập”.\n'
         '– Khách hàng cá nhân không có số điện thoại → hiển thị “Bắt buộc phải nhập số điện thoại”.\n'
         '– Số điện thoại sai định dạng → hiển thị “Số điện thoại không đúng định dạng”.\n'
         '– Khách hàng tổ chức thiếu người đại diện → hiển thị “Phải có ít nhất 1 người đại diện”.\n'
         '– Khách hàng tổ chức thiếu người liên hệ → hiển thị “Phải có ít nhất 1 liên hệ”.\n'
         '– Thiếu địa chỉ xuất hoá đơn → hiển thị “Bắt buộc nhập”.\n'
         '– Không chọn công ty mẹ mà thiếu mã số thuế → hiển thị “Bắt buộc nhập”.\n'
         '– Mã số thuế sai định dạng → hiển thị “Mã số thuế không đúng định dạng”.\n'
         '– Mã số thuế / email / số CMND-CCCD đã tồn tại → hiển thị thông báo “… đã tồn tại” '
         'tương ứng.\n'
         '– Thiếu quốc gia / tỉnh–thành phố / phường–xã → hiển thị thông báo bắt buộc chọn '
         'tương ứng.\n'
         '– Lĩnh vực không thuộc loại hình đã chọn → hiển thị “Lĩnh vực không thuộc loại hình đã '
         'chọn, vui lòng chọn lại”.\n'
         '– Nếu có lỗi validate → không thực hiện bước After.\n'
         'After:\n'
         '– Sinh mã khách hàng và ghi bản ghi mới với trạng thái Hoạt động.\n'
         '– Ghi một dòng lịch sử “Thêm mới”.\n'
         '– Hiển thị thông báo “Thêm mới khách hàng thành công” và quay về danh sách.'),
        ('Bấm Quay lại khi đã sửa mà chưa lưu', 'Click',
         'During:\n– Hiển thị hộp hỏi xác nhận rời khỏi trang.\n'
         'After:\n– Chọn ở lại thì giữ nguyên dữ liệu; chọn rời đi thì bỏ mọi thay đổi.'),
    ])

    # ---------------------------------------------------------- FR-06
    d.h3('5.2.6 FR-06 — Chỉnh sửa khách hàng')

    d.p('5.2.6.1 Biểu đồ Usecase')
    d.uc_figure('FR-06', 'Chỉnh sửa khách hàng', 'crud',
                [('include', 'Kiểm tra quyền Sửa khách hàng'),
                 ('include', 'Ghi lịch sử thay đổi'),
                 ('extend', 'Hiện thêm khối Địa chỉ giao hàng')],
                actor=ACTOR_QL)

    d.p('5.2.6.2 Giới thiệu')
    d.intro_table(
        'Chỉnh sửa khách hàng',
        'Sửa thông tin của một khách hàng đã có. Dùng chung form với chức năng Tạo mới, khác ở '
        'chỗ có thêm khối Địa chỉ giao hàng và mã khách hàng không thay đổi.',
        ACTOR_QL,
        'Người dùng có quyền Sửa khách hàng; khách hàng cần sửa nằm trong phạm vi dữ liệu của '
        'người dùng.',
        '1. Người dùng bấm biểu tượng bút chì ở dòng khách hàng cần sửa.\n'
        '2. Hệ thống mở màn chỉnh sửa với đầy đủ dữ liệu hiện tại.\n'
        '3. Người dùng sửa thông tin và bấm Lưu.\n'
        '4. Hệ thống kiểm tra dữ liệu và ghi nhận thay đổi.\n'
        '5. Hệ thống ghi lịch sử thay đổi, hiển thị thông báo thành công và quay về danh sách.',
        '• Không có quyền Sửa → biểu tượng bút chì bị làm mờ.\n'
        '• Giữ nguyên mã số thuế của chính khách hàng đó → KHÔNG báo trùng.\n'
        '• Đổi sang mã số thuế của khách hàng khác → báo “Mã số thuế đã tồn tại”.\n'
        '• Khách hàng vừa bị người khác khóa → hệ thống báo dữ liệu đã thay đổi, không treo trang.',
        'Mã khách hàng là bất biến, không đổi qua thao tác sửa.')

    d.p('5.2.6.3 Layout màn hình')
    d.layout(route='/assign/customers/{id}/edit',
             shot=shot('kh_16_sua.png'),
             shot_caption='Màn Chỉnh sửa khách hàng — có thêm khối Địa chỉ giao hàng')

    d.p('5.2.6.4 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Toàn bộ các ô của form Tạo mới', 'Textbox / Dropdown / Datepicker', 'Enable',
         'Như FR-05', 'Như FR-05', 'Điền sẵn dữ liệu hiện tại',
         'Quy tắc bắt buộc và thông báo lỗi giống hệt FR-05.'),
        ('Mã khách hàng', 'Label', 'Read-only', '–', '–', 'Mã hiện tại',
         'Không sửa được, không đổi sau khi lưu.'),
        ('Khối Địa chỉ giao hàng', 'Textbox / Dropdown', 'Enable', '0–255 ký tự', 'Không',
         'Điền sẵn nếu đã có',
         'CHỈ hiện ở màn chỉnh sửa, không hiện ở màn tạo mới.'),
        ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi nhận thay đổi.'),
        ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Hỏi xác nhận nếu có thay đổi chưa lưu; không hỏi nếu chưa sửa gì.'),
    ])

    d.p('5.2.6.5 Tiêu chí nghiệm thu')
    d.bullets([
        'Người dùng không có quyền Sửa thấy biểu tượng bút chì bị làm mờ, không bị ẩn.',
        'Gọi thẳng chức năng Sửa khi không có quyền thì bị từ chối và dữ liệu không đổi.',
        'Khối Địa chỉ giao hàng hiện ở màn sửa.',
        'Giữ nguyên mã số thuế của chính mình thì lưu được bình thường.',
        'Mã khách hàng không đổi sau khi sửa.',
        'Lịch sử thay đổi ghi đúng trường đã sửa, giá trị cũ và giá trị mới.',
    ])

    d.p('5.2.6.6 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm biểu tượng bút chì', 'Click',
         'Before:\n– Kiểm tra quyền Sửa khách hàng.\n'
         '– Nếu không có quyền → nút bị làm mờ, không mở màn; gọi thẳng chức năng thì từ chối với '
         'thông báo “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
         'After:\n– Mở màn chỉnh sửa với dữ liệu hiện tại của khách hàng.'),
        ('Bấm Lưu', 'Click',
         'Before:\n– Kiểm tra quyền Sửa khách hàng.\n'
         '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng '
         'xử lý.\n'
         'During:\n'
         '– Áp toàn bộ quy tắc kiểm tra như FR-05.\n'
         '– Bỏ qua kiểm tra trùng đối với chính bản ghi đang sửa.\n'
         '– Nếu có lỗi validate → không thực hiện bước After.\n'
         'After:\n'
         '– Ghi nhận thay đổi, giữ nguyên mã khách hàng.\n'
         '– Ghi một dòng lịch sử với giá trị cũ và giá trị mới của từng trường đã đổi.\n'
         '– Hiển thị thông báo “Cập nhật khách hàng thành công” và quay về danh sách.'),
        ('Bấm Quay lại khi chưa sửa gì', 'Click',
         'After:\n– Quay thẳng về danh sách, không hỏi xác nhận.'),
    ])

    # ---------------------------------------------------------- FR-07
    d.h3('5.2.7 FR-07 — Xem chi tiết khách hàng')

    d.p('5.2.7.1 Giới thiệu')
    d.intro_table(
        'Xem chi tiết khách hàng',
        'Hiển thị toàn bộ thông tin của một khách hàng ở chế độ chỉ đọc.',
        '%s; %s' % (ACTOR_QL, ACTOR_XEM),
        'Khách hàng nằm trong phạm vi dữ liệu của người dùng.',
        '1. Người dùng bấm vào mã khách hàng trên bảng danh sách.\n'
        '2. Hệ thống mở màn chi tiết.\n'
        '3. Mọi thông tin hiển thị ở chế độ chỉ đọc.',
        '• Khách hàng ngoài phạm vi dữ liệu → không mở được, hệ thống báo không tìm thấy.\n'
        '• Khách hàng đã Khóa → vẫn xem được, có nhãn Khóa.',
        '')

    d.p('5.2.7.2 Layout màn hình')
    d.layout(route='/assign/customers/{id}',
             shot=shot('kh_13_chitiet.png'),
             shot_caption='Màn Chi tiết khách hàng ở chế độ chỉ đọc')

    d.p('5.2.7.3 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Toàn bộ trường thông tin', 'Text', 'Read-only', '–', '–', 'Dữ liệu hiện tại',
         'Không gõ được, không có nút Lưu.'),
        ('Nhãn trạng thái', 'Badge', 'Read-only', 'Hoạt động / Khóa', '–', 'Theo dữ liệu', '–'),
        ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn danh sách.'),
    ])

    d.p('5.2.7.4 Tiêu chí nghiệm thu')
    d.bullets([
        'Mọi ô ở chế độ chỉ đọc, không có nút Lưu.',
        'Khách hàng ngoài phạm vi dữ liệu không mở được.',
        'Quay lại danh sách giữ nguyên bộ lọc và trang đang xem.',
    ])

    d.p('5.2.7.5 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm mã khách hàng', 'Click',
         'Before:\n– Kiểm tra khách hàng có nằm trong phạm vi dữ liệu của người dùng.\n'
         'After:\n– Mở màn chi tiết ở chế độ chỉ đọc.'),
        ('Bấm Quay lại', 'Click',
         'After:\n– Về màn danh sách, giữ nguyên bộ lọc và trang trước đó.'),
    ])

    # ---------------------------------------------------------- FR-08
    d.h3('5.2.8 FR-08 — Khóa / Mở khóa khách hàng')

    d.p('5.2.8.1 Biểu đồ Usecase')
    d.uc_figure('FR-08', 'Khóa / Mở khóa khách hàng', 'action',
                [('include', 'Kiểm tra quyền Xóa khách hàng'),
                 ('include', 'Xác nhận trước khi thực hiện'),
                 ('extend', 'Khóa KHÔNG xóa dữ liệu, chỉ đổi trạng thái')],
                actor=ACTOR_QL)

    d.p('5.2.8.2 Giới thiệu')
    d.intro_table(
        'Khóa / Mở khóa khách hàng',
        'Đổi trạng thái khách hàng qua lại giữa Hoạt động và Khóa. Khách hàng đã Khóa vẫn nằm '
        'trong danh mục nhưng không chọn được ở các màn nghiệp vụ khác.',
        ACTOR_QL,
        'Người dùng có quyền Xóa khách hàng.',
        '1. Người dùng bấm biểu tượng ổ khóa ở dòng khách hàng.\n'
        '2. Hệ thống hiện hộp xác nhận nêu rõ mã và tên khách hàng.\n'
        '3. Người dùng bấm Khóa (hoặc Mở khóa) để xác nhận.\n'
        '4. Hệ thống đổi trạng thái và ghi lịch sử.\n'
        '5. Bảng cập nhật nhãn trạng thái, hiển thị thông báo thành công.',
        '• Bấm Hủy → đóng hộp, trạng thái không đổi, không có thông báo thành công.\n'
        '• Khách hàng đã bị người khác khóa trước đó → hệ thống báo dữ liệu đã thay đổi, không '
        'treo trang.\n'
        '• Không có quyền Xóa khách hàng → biểu tượng ổ khóa bị làm mờ.',
        'Hệ thống KHÔNG có chức năng xóa vĩnh viễn khách hàng. Khóa và Mở khóa dùng chung quyền '
        '“Xóa khách hàng”.')

    d.p('5.2.8.3 Layout màn hình')
    d.layout(modal='Xác nhận khóa', shot=shot('kh_17_xacnhan_khoa.png'),
             shot_caption='Hộp xác nhận Khóa khách hàng, nêu rõ mã và tên')

    d.p('5.2.8.4 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Biểu tượng ổ khóa', 'Icon Button', 'Enable / Disable', '–', '–', 'Hiển thị',
         'Nằm thẳng trên cột Hành động. Làm mờ khi thiếu quyền Xóa khách hàng.'),
        ('Tiêu đề hộp xác nhận', 'Label', 'Hiển thị', '–', '–', 'Xác nhận khóa',
         'Đổi thành “Xác nhận mở khóa” khi khách hàng đang ở trạng thái Khóa.'),
        ('Nội dung hộp xác nhận', 'Label', 'Hiển thị', '–', '–',
         'Bạn có chắc muốn khóa khách hàng ‘<mã> - <tên>’?',
         'Phải nêu rõ mã và tên khách hàng để tránh thao tác nhầm dòng.'),
        ('Nút Khóa / Mở khóa', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xác nhận thực hiện.'),
        ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng hộp, không làm gì.'),
    ])

    d.p('5.2.8.5 Tiêu chí nghiệm thu')
    d.bullets([
        'Hộp xác nhận nêu đúng mã và tên khách hàng của dòng đã bấm.',
        'Sau khi khóa, khách hàng VẪN nằm trong danh sách với nhãn Khóa và vẫn xuất ra file.',
        'Khách hàng đã khóa không chọn được ở màn nghiệp vụ khác; mở khóa thì chọn lại được.',
        'Khóa không làm mất báo giá, hợp đồng hay dữ liệu liên quan.',
        'Người không có quyền Xóa khách hàng thấy biểu tượng ổ khóa bị làm mờ; gọi thẳng chức '
        'năng vẫn bị từ chối và trạng thái không đổi.',
    ])

    d.p('5.2.8.6 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm biểu tượng ổ khóa', 'Click',
         'Before:\n– Kiểm tra quyền Xóa khách hàng.\n'
         '– Nếu không có quyền → nút bị làm mờ, không mở hộp xác nhận.\n'
         'After:\n– Hiện hộp xác nhận kèm mã và tên khách hàng.'),
        ('Bấm Khóa / Mở khóa trong hộp xác nhận', 'Click',
         'Before:\n– Kiểm tra quyền Xóa khách hàng.\n'
         '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng '
         'xử lý.\n'
         'During:\n'
         '– Khách hàng không còn tồn tại hoặc đã ở trạng thái đích → hiển thị thông báo dữ liệu '
         'đã thay đổi, đề nghị tải lại danh sách.\n'
         '– Nếu có lỗi → không thực hiện bước After.\n'
         'After:\n'
         '– Đổi trạng thái khách hàng; KHÔNG xóa bất kỳ dữ liệu nào.\n'
         '– Ghi một dòng lịch sử đổi trạng thái kèm người thực hiện và thời điểm.\n'
         '– Cập nhật nhãn trạng thái trên bảng; hiển thị thông báo “Khóa khách hàng thành công” '
         '(hoặc “Mở khóa khách hàng thành công”).'),
        ('Bấm Hủy', 'Click',
         'After:\n– Đóng hộp xác nhận, không thay đổi gì.'),
    ])

    # ---------------------------------------------------------- FR-09
    d.h3('5.2.9 FR-09 — Lịch sử thay đổi')

    d.p('5.2.9.1 Giới thiệu')
    d.intro_table(
        'Xem lịch sử thay đổi của khách hàng',
        'Liệt kê các lần Thêm mới, Sửa và đổi trạng thái của một khách hàng, kèm giá trị cũ, giá '
        'trị mới, người thực hiện và thời điểm.',
        '%s; %s' % (ACTOR_QL, ACTOR_XEM),
        'Khách hàng nằm trong phạm vi dữ liệu của người dùng.',
        '1. Người dùng mở menu ba chấm ở dòng khách hàng.\n'
        '2. Người dùng chọn Lịch sử.\n'
        '3. Hệ thống hiển thị danh sách các lần thay đổi, MỚI NHẤT ở trên cùng.',
        '• Khách hàng chưa từng sửa → chỉ có dòng Thêm mới, không báo lỗi.\n'
        '• Thay đổi ở người liên hệ cũng được ghi nhận thành dòng riêng.',
        'Thứ tự luôn là mới nhất trước, thống nhất với các màn lịch sử khác của hệ thống.')

    d.p('5.2.9.2 Layout màn hình')
    d.layout(modal='Lịch sử khách hàng', shot=shot('kh_06_lichsu.png'),
             shot_caption='Cửa sổ Lịch sử khách hàng — mới nhất ở trên cùng')

    d.p('5.2.9.3 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Menu ba chấm → Lịch sử', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ lịch sử.'),
        ('Danh sách thay đổi', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
         'Sắp xếp mới nhất ở trên cùng.'),
        ('Loại thay đổi', 'Badge', 'Read-only', 'Thêm mới / Sửa / Đổi trạng thái', '–',
         'Theo dữ liệu', '–'),
        ('Giá trị cũ → Giá trị mới', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
         'Hiển thị rõ hai vế cho từng trường đã đổi.'),
        ('Người thực hiện, thời điểm', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', '–',
         'Theo dữ liệu', '–'),
        ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Đóng cửa sổ, giữ nguyên bộ lọc và trang của danh sách.'),
    ])

    d.p('5.2.9.4 Tiêu chí nghiệm thu')
    d.bullets([
        'Dòng mới nhất luôn ở trên cùng.',
        'Mỗi dòng nêu rõ trường đã đổi, giá trị cũ, giá trị mới, người thực hiện và thời điểm.',
        'Thao tác Khóa / Mở khóa cũng sinh dòng lịch sử.',
        'Khách hàng chưa từng sửa vẫn mở được lịch sử, chỉ có dòng Thêm mới.',
    ])

    d.p('5.2.9.5 Danh sách event và xử lý event')
    d.event_table([
        ('Chọn Lịch sử trong menu ba chấm', 'Click',
         'After:\n– Mở cửa sổ, nạp danh sách thay đổi theo thứ tự mới nhất trước.'),
        ('Bấm Đóng', 'Click',
         'After:\n– Đóng cửa sổ; danh sách phía sau giữ nguyên bộ lọc và trang.'),
    ])

    # ---------------------------------------------------------- FR-10
    d.h3('5.2.10 FR-10 — Nhập khách hàng từ file Excel')

    d.p('5.2.10.1 Biểu đồ Usecase')
    d.uc_figure('FR-10', 'Nhập khách hàng từ file Excel', 'io',
                [('include', 'Kiểm tra quyền Thêm khách hàng'),
                 ('include', 'Validate trước khi ghi dữ liệu'),
                 ('extend', 'Dòng bỏ trống Tên khách hàng là người liên hệ của dòng trên')],
                actor=ACTOR_QL)

    d.p('5.2.10.2 Giới thiệu')
    d.intro_table(
        'Nhập khách hàng từ file Excel',
        'Thêm nhiều khách hàng cùng lúc từ file Excel theo mẫu. Có bước kiểm tra dữ liệu trước '
        'khi ghi để người dùng sửa lỗi mà không tạo ra bản ghi rác.',
        ACTOR_QL,
        'Người dùng có quyền Thêm khách hàng và đã chuẩn bị file theo mẫu.',
        '1. Người dùng bấm Import Excel.\n'
        '2. Người dùng bấm Tải file mẫu và điền dữ liệu (dữ liệu bắt đầu từ dòng 3).\n'
        '3. Người dùng chọn file rồi bấm Load lên bảng.\n'
        '4. Người dùng bấm Validate; hệ thống kiểm tra từng dòng và báo lỗi theo số dòng.\n'
        '5. Người dùng sửa lỗi rồi bấm Import.\n'
        '6. Hệ thống ghi các dòng hợp lệ và báo tổng số dòng, số dòng thành công, số dòng lỗi.',
        '• File vượt quá 1.000 dòng → hệ thống từ chối xử lý, nêu rõ giới hạn.\n'
        '• Toàn bộ dòng lỗi → không ghi bản ghi nào.\n'
        '• Một phần dòng lỗi → các dòng hợp lệ vẫn được ghi, dòng lỗi thì không.\n'
        '• Thiếu cột bắt buộc trong file → báo lỗi thiếu cột, dừng xử lý.\n'
        '• Trùng mã số thuế ngay trong file → báo lỗi ở dòng thứ hai.',
        'File mẫu gồm 3 trang: trang nhập liệu và các trang danh mục tra cứu sinh từ dữ liệu thật '
        'của hệ thống. Tiêu đề ở dòng 1, DỮ LIỆU BẮT ĐẦU TỪ DÒNG 3.')

    d.p('5.2.10.3 Layout màn hình')
    d.layout(modal='Import khách hàng', shot=shot('kh_11_import_excel.png'),
             shot_caption='Cửa sổ Import khách hàng với các bước Load lên bảng – Validate – Import')

    d.p('5.2.10.4 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi thiếu quyền',
         'Chỉ hiện khi có quyền Thêm khách hàng.'),
        ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Tải file mẫu 3 trang, 26 cột, các cột bắt buộc có dấu sao đỏ.'),
        ('Ô Chọn file Excel', 'Button', 'Enable', 'Định dạng bảng tính', 'Có', 'Trống', '–'),
        ('Nút Load lên bảng', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Đọc file và hiển thị dữ liệu lên bảng xem trước.'),
        ('Nút Validate', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Kiểm tra từng dòng; dòng hợp lệ sẽ bị khóa lại không cho sửa tiếp.'),
        ('Nút Import', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi các dòng hợp lệ.'),
        ('Ô Chỉ dòng lỗi', 'Icon Button', 'Enable', 'Có / Không', 'Không', 'Không tích',
         'Lọc bảng xem trước để chỉ hiện các dòng đang lỗi.'),
        ('Bảng xem trước', 'Table/Grid', 'Enable', '≤ 1.000 dòng', '–', 'Trống',
         'Sửa trực tiếp được trước khi Validate.'),
        ('Ô Tổng', 'Label', 'Read-only', '≥ 0', '–', '0',
         'Tổng số dòng đọc được từ file.'),
        ('Thông báo lỗi theo dòng', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         'Nêu rõ số dòng và lý do lỗi.'),
        ('Nút Làm mới / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Xóa trạng thái hiện tại / đóng cửa sổ.'),
    ])

    d.p('5.2.10.5 Tiêu chí nghiệm thu')
    d.bullets([
        'Bước Validate không ghi bất kỳ bản ghi nào vào hệ thống.',
        'Ba con số tổng dòng, dòng thành công và dòng lỗi luôn cộng khớp.',
        'File quá 1.000 dòng bị từ chối với thông báo nêu rõ giới hạn.',
        'Dòng bỏ trống Tên khách hàng được hiểu là người liên hệ của khách hàng ở dòng ngay trên; '
        'dòng như vậy đứng đầu file thì báo lỗi.',
        'Người không có quyền Thêm khách hàng gọi thẳng chức năng vẫn bị từ chối, không dòng nào '
        'được ghi.',
        'Khách hàng nhập từ file ghi nhận đúng người tạo là người thực hiện nhập.',
    ])

    d.p('5.2.10.6 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm Import Excel', 'Click',
         'Before:\n– Kiểm tra quyền Thêm khách hàng.\n'
         '– Nếu không có quyền → không hiển thị nút; gọi thẳng chức năng thì từ chối với thông '
         'báo “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
         'After:\n– Mở cửa sổ Import ở trạng thái sạch.'),
        ('Bấm Tải file mẫu', 'Click',
         'After:\n– Sinh file mẫu 3 trang kèm danh mục thật của hệ thống và tải về.'),
        ('Bấm Load lên bảng', 'Click',
         'During:\n'
         '– File không đọc được hoặc sai định dạng → hiển thị thông báo file không hợp lệ.\n'
         '– File không có dòng dữ liệu → hiển thị thông báo file không có dữ liệu.\n'
         '– Số dòng vượt quá 1.000 → hiển thị thông báo vượt quá giới hạn mỗi lần nhập.\n'
         '– Thiếu cột bắt buộc → hiển thị thông báo thiếu cột, nêu rõ tên cột.\n'
         'After:\n– Hiển thị dữ liệu lên bảng xem trước và cập nhật ô Tổng.'),
        ('Bấm Validate', 'Click',
         'During:\n'
         '– Kiểm tra từng dòng theo đúng quy tắc của chức năng Tạo mới.\n'
         '– Kiểm tra trùng mã số thuế / email / số CMND-CCCD với dữ liệu đã có VÀ với các dòng '
         'khác trong cùng file.\n'
         '– Kiểm tra mã danh mục có tồn tại; cặp loại hình – lĩnh vực có khớp nhau.\n'
         'After:\n'
         '– Đánh dấu dòng lỗi kèm lý do theo số dòng; khóa các dòng hợp lệ.\n'
         '– KHÔNG ghi bất kỳ bản ghi nào ở bước này.'),
        ('Bấm Import', 'Click',
         'Before:\n– Kiểm tra quyền Thêm khách hàng.\n'
         '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng '
         'xử lý.\n'
         'During:\n– Bỏ qua các dòng đang lỗi.\n'
         'After:\n'
         '– Ghi các dòng hợp lệ thành khách hàng mới, người tạo là người đang thực hiện.\n'
         '– Hiển thị kết quả: tổng số dòng, số dòng thành công, số dòng lỗi.\n'
         '– Vào hết → “Import thành công”; vào một phần → “Import một phần thành công”; trượt hết '
         '→ thông báo thất bại kèm danh sách lỗi.'),
    ])

    # ---------------------------------------------------------- FR-11
    d.h3('5.2.11 FR-11 — Xuất danh sách ra CSV / Excel / PDF')

    d.p('5.2.11.1 Biểu đồ Usecase')
    d.uc_figure('FR-11', 'Xuất danh sách ra CSV / Excel / PDF', 'io',
                [('include', 'Kiểm tra quyền Xuất dữ liệu khách hàng'),
                 ('include', 'Áp đúng bộ lọc và phạm vi dữ liệu'),
                 ('extend', 'Thứ tự cột theo thứ tự người dùng chọn')],
                actor=ACTOR_QL)

    d.p('5.2.11.2 Giới thiệu')
    d.intro_table(
        'Xuất danh sách khách hàng',
        'Xuất kết quả đang lọc ra file CSV, Excel hoặc PDF, cho phép chọn trường và thứ tự cột.',
        ACTOR_QL,
        'Người dùng có quyền Xuất dữ liệu khách hàng.',
        '1. Người dùng bấm Xuất CSV / Xuất Excel / Xuất PDF.\n'
        '2. Hệ thống mở cửa sổ Chọn trường xuất.\n'
        '3. Người dùng chọn các trường và thứ tự mong muốn.\n'
        '4. Người dùng bấm Xuất.\n'
        '5. Hệ thống sinh file theo đúng bộ lọc, phạm vi dữ liệu và thứ tự trường đã chọn.',
        '• Không chọn trường nào → hệ thống chặn, yêu cầu chọn ít nhất một trường.\n'
        '• Bộ lọc không có kết quả → hệ thống báo không có dữ liệu hoặc sinh file chỉ có dòng '
        'tiêu đề.\n'
        '• Không có quyền → ba nút bị vô hiệu hóa; gọi thẳng chức năng vẫn bị từ chối.',
        'File xuất chứa TOÀN BỘ kết quả lọc, không giới hạn ở trang đang xem.')

    d.p('5.2.11.3 Layout màn hình')
    d.layout(modal='Chọn trường xuất Excel', shot=shot('kh_12_chon_truong_xuat.png'),
             shot_caption='Cửa sổ Chọn trường xuất Excel — thứ tự cột theo thứ tự chọn')

    d.p('5.2.11.4 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Nút Xuất CSV / Xuất Excel / Xuất PDF', 'Button', 'Enable / Disable', '–', '–',
         'Vô hiệu khi thiếu quyền', 'Chỉ dùng được khi có quyền Xuất dữ liệu khách hàng.'),
        ('Ô Trường xuất', 'Dropdown', 'Enable', '20 trường', 'Có', 'Chọn sẵn toàn bộ',
         'Mã KH, Tên KH, MST/SĐT, Đối tượng, Nhóm khách, Địa chỉ, Tỉnh/TP, Tên đơn vị, Tên viết '
         'tắt, Địa chỉ xuất hóa đơn, Hãng xe, Công ty mẹ, Cấp đại lý, Người đại diện, Tên liên hệ, '
         'SĐT liên hệ, Chức vụ liên hệ, Người tạo, Người sửa (gần nhất), Trạng thái.'),
        ('Dòng hướng dẫn thứ tự cột', 'Label', 'Hiển thị', '–', '–',
         'Thứ tự cột chạy theo thứ tự bạn chọn',
         'Muốn đổi vị trí thì bỏ chọn rồi chọn lại theo trình tự mong muốn.'),
        ('Nút Xuất', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Sinh file và tải về.'),
        ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
    ])

    d.p('5.2.11.5 Tiêu chí nghiệm thu')
    d.bullets([
        'Số dòng trong file khớp đúng tổng số bản ghi của bộ lọc, không phải số dòng của trang '
        'đang xem.',
        'Thứ tự cột trong file đúng thứ tự người dùng đã chọn.',
        'Tiếng Việt hiển thị đúng dấu ở cả ba định dạng.',
        'Số điện thoại giữ nguyên chữ số 0 ở đầu; mã số thuế giữ nguyên phần sau dấu gạch ngang.',
        'Khách hàng nằm ngoài phạm vi dữ liệu KHÔNG xuất hiện trong file.',
        'Khách hàng đã Khóa vẫn có trong file, cột Trạng thái ghi bằng chữ tiếng Việt.',
    ])

    d.p('5.2.11.6 Danh sách event và xử lý event')
    d.event_table([
        ('Bấm nút xuất file', 'Click',
         'Before:\n– Kiểm tra quyền Xuất dữ liệu khách hàng.\n'
         '– Nếu không có quyền → nút bị vô hiệu hóa; gọi thẳng chức năng thì từ chối với thông báo '
         '“Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
         'After:\n– Mở cửa sổ Chọn trường xuất với toàn bộ trường được chọn sẵn.'),
        ('Chọn / bỏ chọn trường', 'Change',
         'During:\n– Ghi nhận thứ tự chọn để quyết định thứ tự cột trong file.'),
        ('Bấm Xuất', 'Click',
         'During:\n– Không chọn trường nào → hiển thị thông báo yêu cầu chọn ít nhất một trường '
         'và dừng xử lý.\n'
         'After:\n'
         '– Sinh file theo đúng bộ lọc đang áp dụng, đúng phạm vi dữ liệu và đúng thứ tự trường '
         'đã chọn.\n'
         '– Tải file về máy người dùng.'),
    ])

    # ---------------------------------------------------------- FR-12
    d.h3('5.2.12 FR-12 — Màn Quản lý khách hàng')

    d.p('5.2.12.1 Biểu đồ Usecase')
    d.uc_figure('FR-12', 'Màn Quản lý khách hàng', 'view',
                [('include', 'Kiểm tra quyền Xem khách hàng'),
                 ('extend', 'Sửa trang thiết bị cần quyền Sửa khách hàng')],
                actor=ACTOR_QL)

    d.p('5.2.12.2 Giới thiệu')
    d.intro_table(
        'Màn Quản lý khách hàng',
        'Màn tổng hợp mọi thông tin nghiệp vụ của một khách hàng, gồm 6 thẻ: Thông tin chung, '
        'Thông tin liên hệ, Báo giá, Hợp đồng, Danh sách trang thiết bị, Thông tin khác.',
        ACTOR_QL,
        'Người dùng có quyền Xem khách hàng; khách hàng nằm trong phạm vi dữ liệu của người dùng.',
        '1. Người dùng mở menu ba chấm ở dòng khách hàng và chọn Quản lý.\n'
        '2. Hệ thống mở màn Quản lý khách hàng, chọn sẵn thẻ Thông tin chung.\n'
        '3. Người dùng chuyển sang các thẻ khác để xem báo giá, hợp đồng, trang thiết bị.\n'
        '4. Ở thẻ Danh sách trang thiết bị, người dùng có quyền Sửa khách hàng có thể thêm / sửa / '
        'xóa thiết bị khai ngoài hệ thống và bổ sung số máy.',
        '• Không có quyền Xem khách hàng → các thẻ nghiệp vụ bị từ chối, báo không có quyền, '
        'không treo trang.\n'
        '• Không có quyền Sửa khách hàng → các nút thao tác thiết bị bị vô hiệu hóa nhưng vẫn xem '
        'được danh sách.\n'
        '• Thêm số máy đã tồn tại → cảnh báo và cho biết số máy đang thuộc thiết bị nào.',
        'Số lượng thiết bị là tổng cộng dồn theo từng mã thiết bị, không đếm theo số dòng chứng từ.')

    d.p('5.2.12.3 Layout màn hình')
    d.layout(route='/assign/customers/{id}/manager',
             shot=shot('kh_14_quanly_kh.png'),
             shot_caption='Màn Quản lý khách hàng với 6 thẻ nghiệp vụ')
    d.figure(shot('kh_15_tab_thietbi.png'),
             'Thẻ Danh sách trang thiết bị của màn Quản lý khách hàng', width_in=6.2)

    d.p('5.2.12.4 Mô tả chi tiết giao diện')
    d.ui_table([
        ('Thẻ Thông tin chung', 'Table/Grid', 'Read-only', '–', '–', 'Được chọn sẵn',
         'Hiển thị thông tin cơ bản, người đại diện, địa chỉ.'),
        ('Thẻ Thông tin liên hệ', 'Table/Grid', 'Read-only', '–', '–', 'Ẩn nội dung',
         'Danh sách người liên hệ của khách hàng.'),
        ('Thẻ Báo giá', 'Table/Grid', 'Read-only', '–', '–', 'Ẩn nội dung',
         'Chỉ hiện báo giá của đúng khách hàng đang xem. Cần quyền Xem khách hàng.'),
        ('Thẻ Hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Ẩn nội dung',
         'Cần quyền Xem khách hàng.'),
        ('Thẻ Danh sách trang thiết bị', 'Table/Grid', 'Enable', '–', '–', 'Ẩn nội dung',
         'Gồm thiết bị đã bán qua hệ thống và thiết bị khai thêm từ ngoài, phân biệt rõ hai nhóm.'),
        ('Thẻ Thông tin khác', 'Table/Grid', 'Enable', '–', '–', 'Ẩn nội dung',
         'Ảnh, tài liệu, video đính kèm.'),
        ('Nút thêm / sửa / xóa thiết bị', 'Button', 'Enable / Disable', '–', '–',
         'Vô hiệu khi thiếu quyền', 'Cần quyền Sửa khách hàng.'),
        ('Chức năng tăng số lượng thiết bị', 'Button', 'Enable / Disable', '≥ 1', 'Có', '–',
         'Số nhập vào được CỘNG DỒN vào số lượng hiện có, không thay thế.'),
        ('Chức năng thêm số máy', 'Button', 'Enable / Disable', '0–255 ký tự', 'Có', 'Trống',
         'Số máy phải chưa tồn tại trong hệ thống.'),
        ('Nút xuất file / In trên thẻ Báo giá – Hợp đồng', 'Button', 'Enable', '–', '–',
         'Hiển thị', 'Bản in có tiêu đề đầu trang của công ty.'),
        ('Nút tải ảnh / tài liệu (thẻ Thông tin khác)', 'Button', 'Enable / Disable', '–', 'Không',
         'Vô hiệu khi thiếu quyền', 'Cần quyền Sửa khách hàng.'),
    ])

    d.p('5.2.12.5 Tiêu chí nghiệm thu')
    d.bullets([
        'Đủ 6 thẻ, thẻ Thông tin chung được chọn sẵn khi mở màn.',
        'Các thẻ Báo giá, Hợp đồng, Danh sách trang thiết bị chỉ hiện dữ liệu của đúng khách hàng '
        'đang xem.',
        'Người không có quyền Xem khách hàng bị chặn ở các thẻ nghiệp vụ, trang không trắng và '
        'không treo.',
        'Người không có quyền Sửa khách hàng vẫn xem được danh sách thiết bị nhưng không thao tác '
        'được.',
        'Tăng số lượng thiết bị là cộng dồn, không thay thế giá trị cũ.',
        'Thêm số máy đã tồn tại bị cảnh báo kèm thông tin thiết bị đang giữ số máy đó.',
    ])

    d.p('5.2.12.6 Danh sách event và xử lý event')
    d.event_table([
        ('Chọn Quản lý trong menu ba chấm', 'Click',
         'Before:\n– Kiểm tra khách hàng nằm trong phạm vi dữ liệu.\n'
         'After:\n– Mở màn Quản lý khách hàng, chọn sẵn thẻ Thông tin chung.'),
        ('Bấm sang thẻ Báo giá / Hợp đồng / Danh sách trang thiết bị', 'Click',
         'Before:\n– Kiểm tra quyền Xem khách hàng.\n'
         '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng '
         'xử lý, không hiện dữ liệu.\n'
         'After:\n– Nạp và hiển thị dữ liệu của đúng khách hàng đang xem.'),
        ('Thêm / sửa / xóa thiết bị khai ngoài', 'Click',
         'Before:\n– Kiểm tra quyền Sửa khách hàng.\n'
         '– Nếu không có quyền → nút bị vô hiệu hóa; gọi thẳng chức năng thì từ chối và dừng xử lý.\n'
         'During:\n– Thiếu tên thiết bị hoặc số lượng không hợp lệ → hiển thị lỗi tương ứng.\n'
         '– Nếu có lỗi validate → không thực hiện bước After.\n'
         'After:\n– Ghi nhận thay đổi và cập nhật lại danh sách thiết bị.'),
        ('Thêm số máy', 'Click',
         'During:\n– Số máy đã tồn tại → hiển thị cảnh báo kèm thiết bị đang giữ số máy đó và '
         'dừng xử lý.\n'
         'After:\n– Gắn số máy vào thiết bị và cập nhật chi tiết.'),
        ('Tăng số lượng thiết bị', 'Click',
         'During:\n– Số nhập vào phải lớn hơn 0.\n'
         'After:\n– CỘNG DỒN vào số lượng hiện có và cập nhật danh sách.'),
    ])

    # ============================================================ 6. QUY TẮC NGHIỆP VỤ
    d.h1('6. Quy tắc nghiệp vụ (Business Rules)')

    d.p('BR-01 — Phạm vi dữ liệu bốn cấp')
    d.bullets([
        'Hệ thống xét bốn cấp quyền xem theo thứ tự ưu tiên: tất cả → công ty → phòng ban → bộ '
        'phận. Người dùng có nhiều cấp thì áp cấp RỘNG NHẤT, không lấy giao của các cấp.',
        'Khách hàng “thuộc” một cấp khi đã phát sinh báo giá gắn với công ty / phòng ban / bộ '
        'phận tương ứng.',
        'Người dùng không có cấp nào chỉ thấy khách hàng do chính mình tạo.',
        'Bất kể cấp nào, người dùng LUÔN thấy thêm khách hàng do chính mình tạo và khách hàng '
        'mình đang đăng ký còn hạn hoặc đã từng tương tác. Đây là phần bổ sung có chủ đích so với '
        'phần mềm cũ — chỉ thêm chứ không bớt.',
        'Chức năng xuất file dùng đúng phạm vi này; không được xuất ra khách hàng mà người dùng '
        'không nhìn thấy trên bảng.',
    ])
    d.p('Chức năng liên quan: FR-01, FR-02, FR-11.')

    d.p('BR-02 — Lớp bảo vệ khách hàng cá nhân')
    d.bullets([
        'Khách hàng CÁ NHÂN chỉ hiển thị khi thỏa ít nhất một trong các điều kiện: do chính mình '
        'tạo; mình đang đăng ký còn hạn; đang có người khác đăng ký còn hạn; đã phát sinh báo giá, '
        'cuộc họp hoặc dự án tiềm năng của bất kỳ ai.',
        'Khách hàng cá nhân “tự do” — không thỏa điều kiện nào ở trên — KHÔNG hiển thị trong danh '
        'sách. Người dùng chỉ tìm được khi gõ ĐÚNG TRỌN VẸN số điện thoại; gõ thiếu một chữ số thì '
        'không ra kết quả.',
        'Khách hàng TỔ CHỨC không chịu lớp bảo vệ này.',
        'Mục đích: tránh tình trạng tranh giành khách hàng cá nhân giữa các nhân viên kinh doanh.',
    ])
    d.p('Chức năng liên quan: FR-01, FR-02.')

    d.p('BR-03 — Trường bắt buộc rẽ nhánh theo Loại hình tổ chức')
    d.bullets([
        'Chung cho mọi loại: Tên khách hàng, Loại hình tổ chức, Quốc gia, Tỉnh/Thành phố, '
        'Phường/Xã. Quận/Huyện và Thôn/Xóm KHÔNG bắt buộc.',
        'Khách hàng Cá nhân: bắt buộc ít nhất một số điện thoại, bắt đầu bằng chữ số 0 và dài từ '
        '10 đến 12 chữ số.',
        'Khách hàng tổ chức: bắt buộc ít nhất một Người đại diện (đủ tên và chức vụ), Địa chỉ xuất '
        'hoá đơn, và ít nhất một Người liên hệ (đủ tên, chức vụ và ít nhất một số điện thoại).',
        'Đổi Loại hình tổ chức làm đổi hẳn các khối nhập liệu; dữ liệu ở khối bị ẩn không được '
        'mang sang khối mới.',
    ])
    d.p('Chức năng liên quan: FR-05, FR-06, FR-10.')

    d.p('BR-04 — Mã số thuế phụ thuộc Công ty mẹ')
    d.bullets([
        'Khách hàng tổ chức KHÔNG chọn Công ty mẹ: Mã số thuế BẮT BUỘC.',
        'Khách hàng tổ chức ĐÃ chọn Công ty mẹ: Mã số thuế KHÔNG bắt buộc, vì chi nhánh dùng chung '
        'mã số thuế của công ty mẹ.',
        'Dù bắt buộc hay không, khi đã nhập thì mã số thuế phải đúng định dạng (chỉ chữ số và dấu '
        'gạch ngang, tối đa 14 ký tự) và phải duy nhất toàn hệ thống.',
    ])
    d.p('Chức năng liên quan: FR-05, FR-06, FR-10.')

    d.p('BR-05 — Các trường duy nhất toàn hệ thống')
    d.bullets([
        'Email, Mã số thuế và Số CMND/CCCD là duy nhất trên toàn hệ thống.',
        'Khi sửa, bản ghi đang sửa được loại khỏi phép kiểm tra trùng — giữ nguyên giá trị của '
        'chính mình thì lưu được bình thường.',
        'Khi nhập từ file Excel, phải kiểm tra trùng cả với dữ liệu đã có VÀ giữa các dòng trong '
        'cùng một file.',
    ])
    d.p('Chức năng liên quan: FR-05, FR-06, FR-10.')

    d.p('BR-06 — Cặp Loại hình hoạt động – Lĩnh vực kinh doanh')
    d.bullets([
        'Ngành nghề khai theo CẶP, không chọn rời từng vế.',
        'Lĩnh vực kinh doanh phải thuộc đúng Loại hình hoạt động đã chọn ở vế trái; sai thì hệ '
        'thống chặn với thông báo “Lĩnh vực không thuộc loại hình đã chọn, vui lòng chọn lại”.',
        'Một khách hàng khai được nhiều cặp.',
    ])
    d.p('Chức năng liên quan: FR-02, FR-05, FR-06, FR-10.')

    d.p('BR-07 — Khóa không phải Xóa')
    d.bullets([
        'Hệ thống KHÔNG có chức năng xóa vĩnh viễn khách hàng.',
        'Khách hàng đã Khóa VẪN nằm trong danh mục với nhãn Khóa, vẫn xuất ra file, vẫn xem được '
        'chi tiết và lịch sử.',
        'Tác dụng duy nhất của Khóa là chặn khách hàng đó khỏi các ô chọn khách hàng ở màn nghiệp '
        'vụ khác.',
        'Khóa và Mở khóa dùng chung quyền “Xóa khách hàng”; không có quyền riêng mang tên Khóa.',
    ])
    d.p('Chức năng liên quan: FR-08, FR-11.')

    d.p('BR-08 — Cây địa chỉ phụ thuộc')
    d.bullets([
        'Thứ tự phụ thuộc: Quốc gia → Tỉnh/Thành phố → Quận/Huyện → Phường/Xã → Thôn/Xóm.',
        'Đổi một cấp thì mọi cấp bên dưới bị xóa trắng và nạp lại theo giá trị mới.',
        'Quy tắc này áp cho cả panel bộ lọc và form nhập liệu.',
    ])
    d.p('Chức năng liên quan: FR-02, FR-05, FR-06.')

    d.p('BR-09 — Cấu trúc file nhập liệu')
    d.bullets([
        'File mẫu gồm 3 trang: một trang nhập liệu và các trang danh mục tra cứu sinh từ dữ liệu '
        'thật của hệ thống.',
        'Dòng 1 là tiêu đề cột; DỮ LIỆU BẮT ĐẦU TỪ DÒNG 3. Dòng 2 không được đọc.',
        'Dòng bỏ trống ô Tên khách hàng được hiểu là thêm người liên hệ cho khách hàng ở dòng ngay '
        'trên. Dòng như vậy đứng đầu file là lỗi.',
        'Mỗi lần nhập tối đa 1.000 dòng dữ liệu.',
        'Tiêu đề cột chấp nhận một số cách viết thay thế; đổi thành tên hoàn toàn khác thì hệ '
        'thống báo thiếu cột.',
    ])
    d.p('Chức năng liên quan: FR-10.')

    d.p('BR-10 — Một đối tác chỉ có một bản ghi')
    d.bullets([
        'Sau khi gộp dữ liệu hai phần mềm cũ, mỗi đối tác chỉ tồn tại một bản ghi duy nhất.',
        'Đối tác vừa là khách hàng vừa là nhà cung cấp được đánh dấu bằng ô “Là nhà cung cấp”, '
        'xuất hiện ở cả hai màn nhưng vẫn là MỘT bản ghi — sửa ở màn này thì màn kia đổi theo.',
        'Người tạo và ngày tạo giữ đúng dữ liệu gốc từ phần mềm nguồn.',
    ])
    d.p('Chức năng liên quan: FR-01, FR-05, FR-06.')

    d.p('BR-11 — Cấu hình hiển thị lưu theo người dùng')
    d.bullets([
        'Cấu hình cột và cấu hình bộ lọc lưu riêng cho từng người dùng và từng màn hình, không '
        'ảnh hưởng người dùng khác.',
        'Cột STT và Mã KH bị khóa luôn hiển thị.',
        'Bốn cột Công ty mẹ, Hãng xe, Người tạo, Người sửa (gần nhất) mặc định ẩn vì làm truy vấn '
        'đếm chậm hơn; chỉ gửi yêu cầu lấy dữ liệu bổ sung khi người dùng thực sự bật ít nhất một '
        'trong bốn cột này.',
        'Ẩn một ô lọc chỉ ẩn trên giao diện; giá trị lọc đã áp dụng vẫn còn tác dụng cho tới khi '
        'bấm Làm mới.',
    ])
    d.p('Chức năng liên quan: FR-03, FR-04.')

    d.p('BR-12 — Lịch sử thay đổi sắp xếp mới nhất trước')
    d.bullets([
        'Mọi thao tác Thêm mới, Sửa và đổi trạng thái đều sinh dòng lịch sử.',
        'Danh sách lịch sử luôn sắp xếp MỚI NHẤT Ở TRÊN CÙNG, thống nhất với các màn lịch sử khác '
        'của hệ thống.',
        'Mỗi dòng nêu rõ trường đã đổi, giá trị cũ, giá trị mới, người thực hiện và thời điểm.',
    ])
    d.p('Chức năng liên quan: FR-05, FR-06, FR-08, FR-09.')
