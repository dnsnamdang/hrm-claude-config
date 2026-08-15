# -*- coding: utf-8 -*-
"""Section V (Tao moi / Sua / Xem chi tiet) cua testcase man Danh muc khach hang."""

SEC_V = [
    (1, "Mở màn Tạo mới khách hàng", "P0",
     "Tài khoản có quyền 'Thêm khách hàng'.",
     "1. Mở Danh mục khách hàng\n2. Bấm nút Tạo mới",
     "—",
     "- Mở màn thêm mới, tiêu đề ghi rõ đang thêm khách hàng\n"
     "- Ban đầu chỉ hiện khối Thông tin khách hàng\n"
     "- ⚠️ Khối Địa chỉ giao hàng KHÔNG hiện khi tạo mới"),

    (2, "Chọn Loại hình tổ chức = Cá nhân hiện khối Thông tin cá nhân", "P0",
     "Đang ở màn Tạo mới.",
     "1. Chọn ô Loại hình tổ chức = Cá nhân\n2. Quan sát các khối trên màn hình",
     "Loại hình tổ chức: Cá nhân",
     "- Hiện thêm khối Thông tin cá nhân với các ô Số CMND/CCCD, Ngày sinh, Ngày cấp, Nơi cấp, Tên đơn vị\n"
     "- ⚠️ KHÔNG hiện khối Thông tin tổ chức và khối Người liên hệ"),

    (3, "Chọn Đối tượng là loại tổ chức hiện đủ 2 khối", "P0",
     "Đang ở màn Tạo mới.",
     "1. Chọn ô Loại hình tổ chức = Doanh nghiệp tư nhân\n2. Quan sát các khối",
     "Loại hình tổ chức: Doanh nghiệp tư nhân",
     "- Hiện khối Thông tin tổ chức (Mã số thuế, Người đại diện, Chức vụ người đại diện, "
     "Địa chỉ xuất hoá đơn, Công ty mẹ, Fax)\n"
     "- Hiện khối Người liên hệ\n"
     "- KHÔNG hiện khối Thông tin cá nhân"),

    (4, "Đổi Đối tượng từ Cá nhân sang tổ chức", "P0",
     "Đang chọn Cá nhân và đã nhập Số CMND/CCCD.",
     "1. Đổi ô Loại hình tổ chức sang Tổ chức phi chính phủ\n2. Quan sát màn hình\n3. Đổi ngược lại về Cá nhân",
     "Cá nhân → Tổ chức phi chính phủ → Cá nhân",
     "- Khối Thông tin cá nhân biến mất, khối Thông tin tổ chức và Người liên hệ hiện ra\n"
     "- ⚠️ Dữ liệu đã gõ ở khối cũ không được mang sang khối mới — cần ghi nhận rõ hành vi khi quay lại"),

    (5, "Tạo mới khách hàng cá nhân đủ trường bắt buộc", "P0",
     "Tài khoản có quyền Thêm khách hàng. Danh mục địa chỉ có Việt Nam – Hà Nội – Ba Đình – Phúc Xá.",
     "1. Bấm Tạo mới\n2. Chọn Loại hình tổ chức = Cá nhân\n3. Nhập Tên khách hàng\n"
     "4. Nhập 1 số điện thoại\n5. Chọn Quốc gia, Tỉnh/Thành phố, Phường/Xã\n6. Bấm Lưu",
     "Tên: Nguyễn Văn Test · SĐT: 0912000111 · Việt Nam – Hà Nội – Phúc Xá",
     "- Lưu thành công, hiện thông báo thành công\n"
     "- Quay về danh sách, khách hàng mới có mặt với mã tự sinh\n"
     "- Cột Trạng thái là Hoạt động"),

    (6, "Tạo mới khách hàng tổ chức đủ trường bắt buộc", "P0",
     "Tài khoản có quyền Thêm khách hàng.",
     "1. Bấm Tạo mới, chọn Loại hình tổ chức = Doanh nghiệp tư nhân\n2. Nhập Tên khách hàng\n"
     "3. Nhập Mã số thuế chưa tồn tại\n4. Nhập 1 Người đại diện kèm chức vụ\n"
     "5. Nhập Địa chỉ xuất hoá đơn\n6. Nhập 1 Người liên hệ kèm chức vụ và 1 số điện thoại\n"
     "7. Chọn Quốc gia, Tỉnh/Thành phố, Phường/Xã\n8. Bấm Lưu",
     "Tên: Doanh nghiệp Kiểm Thử · MST: 0100999888 · Người đại diện: Trần A – Giám đốc · "
     "Người liên hệ: Lê B – Kế toán – 0913000222",
     "- Lưu thành công, quay về danh sách, khách hàng mới có mặt"),

    (7, "Thiếu Tên khách hàng thì bị chặn", "P0",
     "Đang ở màn Tạo mới, đã chọn Loại hình tổ chức = Cá nhân.",
     "1. Để trống ô Tên khách hàng\n2. Nhập các trường còn lại hợp lệ\n3. Bấm Lưu",
     "Tên khách hàng: (để trống)",
     "- Hệ thống báo lỗi đỏ ngay dưới ô Tên khách hàng: 'Bắt buộc phải nhập'\n"
     "- Màn hình không đóng, dữ liệu đã nhập vẫn còn"),

    (8, "Thiếu Loại hình tổ chức thì bị chặn", "P0",
     "Đang ở màn Tạo mới.",
     "1. Không chọn ô Loại hình tổ chức\n2. Nhập Tên khách hàng\n3. Bấm Lưu",
     "Loại hình tổ chức: (không chọn)",
     "- Báo lỗi đỏ tại ô Loại hình tổ chức: 'Bắt buộc nhập'"),

    (9, "Khách hàng cá nhân bắt buộc ít nhất 1 số điện thoại", "P0",
     "Đang tạo mới khách hàng Cá nhân, đã nhập tên và địa chỉ.",
     "1. Không nhập số điện thoại nào\n2. Bấm Lưu",
     "Số điện thoại: (để trống)",
     "- Báo lỗi 'Bắt buộc phải nhập số điện thoại'\n"
     "- ⚠️ Quy tắc này chỉ áp cho khách hàng Cá nhân"),

    (10, "Số điện thoại sai định dạng", "P0",
     "Đang tạo mới khách hàng Cá nhân.",
     "1. Nhập số điện thoại 12345\n2. Bấm Lưu\n3. Đổi thành 84912345678, bấm Lưu\n"
     "4. Đổi thành 0912345678, bấm Lưu",
     "12345 / 84912345678 / 0912345678",
     "- Bước 2 và 3: báo lỗi 'Số điện thoại không đúng định dạng'\n"
     "- Bước 4: hợp lệ, lưu được\n"
     "- ⚠️ Số phải bắt đầu bằng chữ số 0 và dài từ 10 đến 12 chữ số"),

    (11, "Khách hàng tổ chức bắt buộc Người đại diện", "P0",
     "Đang tạo mới khách hàng Doanh nghiệp tư nhân, đã nhập tên và mã số thuế.",
     "1. Không nhập Người đại diện\n2. Bấm Lưu",
     "Người đại diện: (để trống)",
     "- Báo lỗi 'Bắt buộc phải nhập' hoặc 'Phải có ít nhất 1 người đại diện'"),

    (12, "Người đại diện thiếu Chức vụ", "P1",
     "Đang tạo mới khách hàng tổ chức.",
     "1. Nhập tên Người đại diện, để trống Chức vụ người đại diện\n2. Bấm Lưu",
     "Người đại diện: Trần A · Chức vụ: (để trống)",
     "- Báo lỗi tại ô Chức vụ người đại diện\n"
     "- ⚠️ Cả tên và chức vụ đều bắt buộc"),

    (13, "Khách hàng tổ chức bắt buộc Địa chỉ xuất hoá đơn", "P0",
     "Đang tạo mới khách hàng tổ chức, đã nhập các trường khác.",
     "1. Để trống Địa chỉ xuất hoá đơn\n2. Bấm Lưu",
     "Địa chỉ xuất hoá đơn: (để trống)",
     "- Báo lỗi 'Bắt buộc nhập' tại ô Địa chỉ xuất hoá đơn"),

    (14, "Khách hàng tổ chức bắt buộc ít nhất 1 Người liên hệ", "P0",
     "Đang tạo mới khách hàng tổ chức.",
     "1. Xóa hết dòng Người liên hệ\n2. Bấm Lưu",
     "Người liên hệ: (không có dòng nào)",
     "- Báo lỗi 'Phải có ít nhất 1 liên hệ'"),

    (15, "Người liên hệ bắt buộc số điện thoại và chức vụ", "P0",
     "Đang tạo mới khách hàng tổ chức, đã thêm 1 dòng Người liên hệ chỉ có tên.",
     "1. Để trống SĐT người liên hệ và Chức vụ người liên hệ\n2. Bấm Lưu",
     "Người liên hệ: Lê B, không SĐT, không chức vụ",
     "- Báo lỗi 'Bắt buộc nhập số điện thoại liên hệ' và lỗi tại ô Chức vụ người liên hệ"),

    (16, "Mã số thuế bắt buộc khi KHÔNG chọn Công ty mẹ", "P0",
     "Đang tạo mới khách hàng Doanh nghiệp tư nhân, ô Công ty mẹ để trống.",
     "1. Để trống Mã số thuế\n2. Bấm Lưu",
     "Công ty mẹ: (trống) · Mã số thuế: (trống)",
     "- Báo lỗi 'Bắt buộc nhập' tại ô Mã số thuế"),

    (17, "Mã số thuế KHÔNG bắt buộc khi đã chọn Công ty mẹ", "P0",
     "Đang tạo mới khách hàng Doanh nghiệp tư nhân. Có sẵn khách hàng KH-MEDE dùng làm công ty mẹ.",
     "1. Chọn Công ty mẹ = KH-MEDE\n2. Để trống Mã số thuế\n"
     "3. Nhập đủ các trường bắt buộc khác\n4. Bấm Lưu",
     "Công ty mẹ: KH-MEDE · Mã số thuế: (trống)",
     "- ⚠️ LƯU THÀNH CÔNG, không báo lỗi mã số thuế\n"
     "- Bật cột Công ty mẹ trên lưới thấy đúng tên KH-MEDE"),

    (18, "Mã số thuế sai định dạng", "P1",
     "Đang tạo mới khách hàng tổ chức, không chọn công ty mẹ.",
     "1. Nhập Mã số thuế = ABC123XYZ\n2. Bấm Lưu\n3. Đổi thành 0100999888-001, bấm Lưu",
     "ABC123XYZ / 0100999888-001",
     "- Bước 2: báo lỗi 'Mã số thuế không đúng định dạng'\n"
     "- Bước 3: hợp lệ (chỉ chấp nhận chữ số và dấu gạch ngang, tối đa 14 ký tự)"),

    (19, "Mã số thuế trùng với khách hàng đã có", "P0",
     "Khách hàng KH-M đang dùng mã số thuế 0101234567.",
     "1. Tạo mới khách hàng tổ chức, nhập Mã số thuế = 0101234567\n2. Bấm Lưu",
     "Mã số thuế: 0101234567",
     "- Báo lỗi 'Mã số thuế đã tồn tại'\n"
     "- Không tạo ra khách hàng mới"),

    (20, "Email trùng với khách hàng đã có", "P0",
     "Khách hàng KH-N đang dùng email test@abc.com.",
     "1. Tạo mới khách hàng, nhập Email = test@abc.com\n2. Bấm Lưu",
     "Email: test@abc.com",
     "- Báo lỗi 'Email đã tồn tại'"),

    (21, "Email sai định dạng", "P1",
     "Đang tạo mới khách hàng.",
     "1. Nhập Email = abc@@xyz\n2. Bấm Lưu",
     "Email: abc@@xyz",
     "- Báo lỗi định dạng email tại ô Email"),

    (22, "Số CMND/CCCD trùng với khách hàng đã có", "P0",
     "Khách hàng cá nhân KH-O đang dùng số CCCD 001199012345.",
     "1. Tạo mới khách hàng cá nhân, nhập Số CMND/CCCD = 001199012345\n2. Bấm Lưu",
     "Số CMND/CCCD: 001199012345",
     "- Báo lỗi 'Số CMND/CCCD đã tồn tại'"),

    (23, "Ngày sinh không được lớn hơn ngày hiện tại", "P0",
     "Đang tạo mới khách hàng cá nhân.",
     "1. Nhập Ngày sinh là ngày mai\n2. Bấm Lưu",
     "Ngày sinh: (ngày mai)",
     "- Báo lỗi 'Không được lớn hơn ngày hiện tại'"),

    (24, "Ngày cấp không được lớn hơn ngày hiện tại", "P1",
     "Đang tạo mới khách hàng cá nhân.",
     "1. Nhập Ngày cấp là ngày mai\n2. Bấm Lưu",
     "Ngày cấp: (ngày mai)",
     "- Báo lỗi 'Không được lớn hơn ngày hiện tại'"),

    (25, "Ngày sinh người liên hệ không được ở tương lai", "P1",
     "Đang tạo mới khách hàng tổ chức, có 1 dòng người liên hệ.",
     "1. Nhập Ngày sinh của người liên hệ là ngày mai\n2. Bấm Lưu",
     "Ngày sinh người liên hệ: (ngày mai)",
     "- Báo lỗi 'Không được lớn hơn ngày hiện tại' ngay tại dòng người liên hệ đó"),

    (26, "Bắt buộc chọn Quốc gia, Tỉnh/Thành phố, Phường/Xã", "P0",
     "Đang tạo mới khách hàng, đã nhập tên.",
     "1. Để trống cả ba ô địa chỉ bắt buộc\n2. Bấm Lưu",
     "—",
     "- Báo đủ ba lỗi: 'Bắt buộc chọn quốc gia', 'Bắt buộc chọn tỉnh/thành phố', 'Bắt buộc chọn phường/xã'\n"
     "- ⚠️ Quận/Huyện và Thôn/Xóm KHÔNG bắt buộc"),

    (27, "Cây địa chỉ nạp phụ thuộc lẫn nhau", "P0",
     "Đang tạo mới khách hàng.",
     "1. Chọn Quốc gia = Việt Nam\n2. Chọn Tỉnh/Thành phố = Hà Nội\n3. Mở ô Quận/Huyện\n"
     "4. Chọn Quận/Huyện = Ba Đình, mở ô Phường/Xã\n5. Đổi Tỉnh/Thành phố sang Hải Phòng",
     "Việt Nam – Hà Nội – Ba Đình → đổi sang Hải Phòng",
     "- Bước 3: chỉ hiện quận/huyện của Hà Nội\n"
     "- Bước 4: chỉ hiện phường/xã của Ba Đình\n"
     "- Bước 5: ⚠️ Quận/Huyện và Phường/Xã bị xóa trắng, nạp lại theo Hải Phòng"),

    (28, "Tích 'Là khách hãng' bắt buộc chọn Hãng xe", "P0",
     "Đang tạo mới khách hàng tổ chức.",
     "1. Tích ô 'Là khách hãng'\n2. Không chọn Hãng xe nào\n3. Bấm Lưu",
     "Là khách hãng: có tích · Hãng xe: (trống)",
     "- Báo lỗi 'Bắt buộc khi là khách hãng' tại ô Hãng xe"),

    (29, "Không tích 'Là khách hãng' thì Hãng xe không bắt buộc", "P1",
     "Đang tạo mới khách hàng tổ chức.",
     "1. Không tích 'Là khách hãng'\n2. Không chọn Hãng xe\n3. Nhập đủ các trường bắt buộc, bấm Lưu",
     "Là khách hãng: không tích",
     "- Lưu thành công, không báo lỗi Hãng xe"),

    (30, "Chọn cặp Loại hình hoạt động – Lĩnh vực kinh doanh hợp lệ", "P0",
     "Loại hình 'Sản xuất' có chứa lĩnh vực 'Cơ khí'.",
     "1. Ở khối Lĩnh vực kinh doanh, chọn Loại hình hoạt động = Sản xuất\n"
     "2. Mở ô Lĩnh vực kinh doanh, chọn Cơ khí\n3. Bấm Lưu",
     "Cặp: Sản xuất – Cơ khí",
     "- Lưu thành công\n"
     "- Mở lại chi tiết thấy đúng cặp đã chọn"),

    (31, "Chọn lĩnh vực không thuộc loại hình đã chọn", "P0",
     "Lĩnh vực 'Bán lẻ' KHÔNG thuộc loại hình 'Sản xuất'.",
     "1. Chọn Loại hình hoạt động = Sản xuất\n2. Ép chọn Lĩnh vực = Bán lẻ\n3. Bấm Lưu",
     "Cặp lệch: Sản xuất – Bán lẻ",
     "- Báo lỗi 'Lĩnh vực không thuộc loại hình đã chọn, vui lòng chọn lại'\n"
     "- Không lưu được"),

    (32, "Thêm nhiều cặp lĩnh vực kinh doanh", "P1",
     "Đang tạo mới khách hàng tổ chức.",
     "1. Thêm cặp thứ nhất Sản xuất – Cơ khí\n2. Bấm thêm dòng, thêm cặp thứ hai Thương mại – Bán lẻ\n"
     "3. Bấm Lưu\n4. Mở lại chi tiết",
     "2 cặp như trên",
     "- Lưu được cả hai cặp, mở lại thấy đủ 2 dòng"),

    (33, "Thêm nhiều số điện thoại cho khách hàng cá nhân", "P1",
     "Đang tạo mới khách hàng cá nhân.",
     "1. Nhập số thứ nhất 0912000111\n2. Bấm thêm dòng, nhập số thứ hai 0912000222\n"
     "3. Bấm Lưu\n4. Xem cột SĐT trên lưới",
     "2 số điện thoại",
     "- Lưu được cả hai số\n"
     "- Cột SĐT hiện cả hai, ngăn nhau bằng dấu phẩy"),

    (34, "Xóa dòng số điện thoại cuối cùng của khách hàng cá nhân", "P1",
     "Khách hàng cá nhân đang có đúng 1 số điện thoại.",
     "1. Bấm xóa dòng số điện thoại duy nhất\n2. Bấm Lưu",
     "—",
     "- Bị chặn, báo phải có ít nhất 1 số điện thoại"),

    (35, "Thêm nhiều Người liên hệ cho khách hàng tổ chức", "P1",
     "Đang tạo mới khách hàng tổ chức.",
     "1. Nhập người liên hệ thứ nhất đủ tên, chức vụ, số điện thoại\n"
     "2. Bấm thêm người liên hệ, nhập người thứ hai đủ trường\n3. Bấm Lưu\n4. Mở lại chi tiết",
     "2 người liên hệ",
     "- Lưu được cả hai, mở lại thấy đủ 2 khối người liên hệ"),

    (36, "Thêm tài khoản ngân hàng cho khách hàng", "P1",
     "Đang tạo mới khách hàng. Danh mục ngân hàng có sẵn dữ liệu.",
     "1. Nhập Số tài khoản, Chủ tài khoản\n2. Chọn Ngân hàng, Tỉnh/TP ngân hàng, Chi nhánh\n3. Bấm Lưu",
     "STK: 19001234567 · Chủ TK: Nguyễn Văn Test · Ngân hàng: Techcombank",
     "- Lưu thành công, mở lại chi tiết thấy đủ thông tin tài khoản"),

    (37, "Ô Chi nhánh phụ thuộc ô Ngân hàng và Tỉnh/TP ngân hàng", "P1",
     "Đang nhập tài khoản ngân hàng.",
     "1. Chọn Ngân hàng = Techcombank, Tỉnh/TP ngân hàng = Hà Nội\n2. Mở ô Chi nhánh\n"
     "3. Đổi Ngân hàng sang Vietcombank\n4. Mở lại ô Chi nhánh",
     "—",
     "- Bước 2: chỉ hiện chi nhánh Techcombank tại Hà Nội\n"
     "- Bước 4: ô Chi nhánh bị xóa trắng, nạp lại theo ngân hàng mới"),

    (38, "Mở màn Sửa khách hàng", "P0",
     "Khách hàng KH-P là doanh nghiệp tư nhân, đã có đủ dữ liệu.",
     "1. Ở dòng KH-P bấm biểu tượng bút chì\n2. Quan sát các khối trên màn",
     "—",
     "- Mở màn sửa, mọi ô đã điền sẵn dữ liệu hiện tại\n"
     "- ⚠️ Khối Địa chỉ giao hàng HIỆN RA ở màn sửa (khác với màn tạo mới)"),

    (39, "Sửa và lưu thành công", "P0",
     "Khách hàng KH-P đang có Tên viết tắt là 'KHP'.",
     "1. Mở màn sửa KH-P\n2. Đổi Tên viết tắt thành 'KHP-2026'\n3. Bấm Lưu\n4. Xem lại lưới",
     "Tên viết tắt: KHP-2026",
     "- Lưu thành công, thông báo thành công\n"
     "- Cột Tên viết tắt trên lưới đổi thành KHP-2026"),

    (40, "Sửa không đổi mã khách hàng", "P0",
     "Khách hàng KH-P có mã KH.00300.",
     "1. Mở màn sửa, đổi tên và lưu\n2. Xem cột Mã KH",
     "—",
     "- ⚠️ Mã khách hàng KHÔNG đổi, vẫn là KH.00300"),

    (41, "Sửa trùng mã số thuế với khách hàng khác", "P0",
     "Khách hàng KH-Q có mã số thuế 0101234567. Đang sửa khách hàng KH-P.",
     "1. Mở màn sửa KH-P\n2. Đổi Mã số thuế thành 0101234567\n3. Bấm Lưu",
     "Mã số thuế: 0101234567",
     "- Báo lỗi 'Mã số thuế đã tồn tại', không lưu"),

    (42, "Giữ nguyên mã số thuế của chính mình khi sửa", "P0",
     "Khách hàng KH-P có mã số thuế riêng 0100888777.",
     "1. Mở màn sửa KH-P\n2. Không đổi Mã số thuế, chỉ đổi Tên viết tắt\n3. Bấm Lưu",
     "Mã số thuế: giữ nguyên 0100888777",
     "- ⚠️ LƯU ĐƯỢC, không báo lỗi trùng với chính mình"),

    (43, "Nhập Địa chỉ giao hàng ở màn sửa", "P1",
     "Đang mở màn sửa khách hàng KH-P.",
     "1. Ở khối Địa chỉ giao hàng, nhập một địa chỉ đầy đủ\n2. Bấm Lưu\n3. Mở lại màn sửa",
     "Địa chỉ giao hàng: Số 1 Trần Duy Hưng, Cầu Giấy, Hà Nội",
     "- Lưu thành công, mở lại thấy đúng địa chỉ giao hàng đã nhập"),

    (44, "Cảnh báo khi thoát màn sửa mà chưa lưu", "P0",
     "Đang mở màn sửa và vừa đổi Tên viết tắt.",
     "1. Bấm nút Quay lại mà không bấm Lưu\n2. Quan sát",
     "—",
     "- Hệ thống hỏi xác nhận rời khỏi trang vì có thay đổi chưa lưu\n"
     "- Chọn ở lại thì quay về màn sửa, dữ liệu còn nguyên\n"
     "- Chọn rời đi thì về danh sách, thay đổi không được lưu"),

    (45, "Không cảnh báo khi thoát mà chưa sửa gì", "P1",
     "Vừa mở màn sửa, chưa đổi gì.",
     "1. Bấm nút Quay lại",
     "—",
     "- Về thẳng danh sách, KHÔNG hiện hỏi xác nhận"),

    (46, "Xem chi tiết khách hàng ở chế độ chỉ đọc", "P0",
     "Tài khoản chỉ có quyền 'Xem tất cả khách hàng', không có quyền Sửa.",
     "1. Mở chi tiết khách hàng KH-P\n2. Thử gõ vào ô Tên khách hàng",
     "—",
     "- Mọi ô ở chế độ chỉ đọc, không gõ được\n"
     "- Không hiện nút Lưu"),

    (47, "Sửa khách hàng đang ở trạng thái Khóa", "P1",
     "Khách hàng KH-R đang ở trạng thái Khóa. Tài khoản có quyền Sửa khách hàng.",
     "1. Tìm KH-R\n2. Bấm biểu tượng Sửa\n3. Ghi nhận hành vi",
     "—",
     "- Ghi nhận rõ: cho sửa hay chặn sửa khách hàng đã Khóa\n"
     "- ⚠️ Hành vi phải nhất quán với quy định nghiệp vụ, không được lúc cho lúc chặn"),

    (48, "Lưu nhiều lần liên tiếp không tạo bản ghi trùng", "P0",
     "Đang ở màn tạo mới, đã nhập đủ trường bắt buộc.",
     "1. Bấm Lưu\n2. Bấm Lưu lần thứ hai thật nhanh trước khi trang chuyển\n3. Xem danh sách",
     "—",
     "- ⚠️ Chỉ tạo ra ĐÚNG MỘT khách hàng, không tạo hai bản ghi trùng\n"
     "- Nút Lưu bị khóa trong lúc đang xử lý"),

    (49, "Tích 'Là nhà cung cấp' khi tạo khách hàng", "P1",
     "Đang tạo mới khách hàng tổ chức.",
     "1. Tích ô 'Là nhà cung cấp'\n2. Nhập đủ trường bắt buộc, bấm Lưu\n"
     "3. Mở màn Danh mục nhà cung cấp tìm khách hàng vừa tạo",
     "Là nhà cung cấp: có tích",
     "- Lưu thành công\n"
     "- ⚠️ Đối tác này xuất hiện ở CẢ hai màn khách hàng và nhà cung cấp, nhưng chỉ là MỘT bản ghi"),

    (50, "Chọn Công ty mẹ là chính khách hàng đang sửa", "P1",
     "Đang sửa khách hàng KH-P.",
     "1. Mở ô Công ty mẹ\n2. Tìm chính KH-P trong danh sách",
     "—",
     "- ⚠️ KH-P KHÔNG được xuất hiện trong danh sách chọn công ty mẹ của chính nó\n"
     "- Nếu chọn được thì phải bị chặn khi lưu"),
]
