# -*- coding: utf-8 -*-
"""Section VI -> X cua testcase man Danh muc khach hang."""

SEC_VI = [
    (1, "Cột Hành động và menu ba chấm trên một dòng", "P0",
     "Tài khoản có đủ quyền Sửa và Xóa khách hàng.",
     "1. Mở Danh mục khách hàng\n2. Bấm biểu tượng ba chấm ở cột Hành động của một dòng",
     "—",
     "- Menu ba chấm mở ra với hai mục Quản lý và Lịch sử\n"
     "- ⚠️ Sửa (biểu tượng bút chì) và Khóa / Mở khóa (biểu tượng ổ khóa) nằm THẲNG trên cột "
     "Hành động, KHÔNG nằm trong menu ba chấm"),

    (2, "Khóa một khách hàng đang Hoạt động", "P0",
     "Khách hàng KH-B đang ở trạng thái Hoạt động. Tài khoản có quyền Xóa khách hàng.",
     "1. Bấm biểu tượng ổ khóa ở dòng KH-B\n2. Bấm Đồng ý ở hộp xác nhận\n3. Xem lại lưới",
     "—",
     "- Hộp xác nhận hiện rõ tên khách hàng sắp khóa\n"
     "- Sau khi đồng ý: thông báo thành công, cột Trạng thái đổi thành Khóa\n"
     "- ⚠️ KH-B VẪN nằm trong danh sách, không bị biến mất"),

    (3, "Hủy bỏ ở hộp xác nhận Khóa", "P0",
     "Khách hàng KH-B đang Hoạt động.",
     "1. Bấm biểu tượng ổ khóa ở dòng KH-B\n2. Bấm Hủy ở hộp xác nhận\n3. Xem cột Trạng thái",
     "—",
     "- Hộp đóng lại, KH-B vẫn ở trạng thái Hoạt động\n"
     "- Không có thông báo thành công nào"),

    (4, "Mở khóa một khách hàng đang Khóa", "P0",
     "Khách hàng KH-C đang ở trạng thái Khóa.",
     "1. Bấm biểu tượng ổ khóa ở dòng KH-C\n2. Bấm Đồng ý\n3. Xem cột Trạng thái",
     "—",
     "- Thông báo thành công, cột Trạng thái đổi thành Hoạt động"),

    (5, "Khóa không làm mất dữ liệu liên quan", "P0",
     "Khách hàng KH-S có 3 báo giá và 1 hợp đồng.",
     "1. Khóa KH-S\n2. Mở màn Quản lý khách hàng của KH-S\n3. Xem thẻ Báo giá và Hợp đồng",
     "—",
     "- Vẫn thấy đủ 3 báo giá và 1 hợp đồng\n"
     "- ⚠️ Khóa chỉ đổi trạng thái, KHÔNG xóa dữ liệu nghiệp vụ"),

    (6, "Khách hàng đã Khóa không chọn được ở màn nghiệp vụ khác", "P0",
     "Khách hàng KH-B vừa bị Khóa.",
     "1. Mở màn tạo báo giá mới\n2. Ở ô chọn khách hàng, gõ tên KH-B",
     "—",
     "- KH-B KHÔNG xuất hiện trong danh sách chọn\n"
     "- ⚠️ Đây là mục đích chính của thao tác Khóa"),

    (7, "Khách hàng đã Khóa vẫn xuất ra file", "P1",
     "Bộ lọc đang cho ra 50 khách hàng, trong đó có 3 khách hàng đã Khóa.",
     "1. Bấm Xuất Excel\n2. Mở file, đếm số dòng và đọc cột Trạng thái",
     "—",
     "- File có đủ 50 dòng, 3 dòng ghi trạng thái Khóa"),

    (8, "Khóa khách hàng đã bị người khác khóa trước đó", "P1",
     "Hai người dùng cùng mở danh sách. Người A vừa khóa KH-T, người B chưa tải lại trang.",
     "1. Người B bấm biểu tượng ổ khóa ở dòng KH-T\n2. Bấm Đồng ý",
     "—",
     "- Hệ thống báo dữ liệu đã thay đổi hoặc khách hàng đã ở trạng thái Khóa\n"
     "- ⚠️ Không treo trang, không báo lỗi kỹ thuật khó hiểu"),

    (9, "Trạng thái sau khi Khóa được ghi vào lịch sử", "P1",
     "Vừa khóa khách hàng KH-B.",
     "1. Mở menu thao tác ở dòng KH-B\n2. Chọn Lịch sử",
     "—",
     "- Có một dòng lịch sử ghi nhận lần đổi trạng thái, kèm người thực hiện và thời điểm\n"
     "- Dòng này nằm ở TRÊN CÙNG (mới nhất trước)"),

    (10, "Khóa rồi lọc lại theo trạng thái", "P1",
     "Trước khi thao tác có 35 khách hàng Khóa.",
     "1. Khóa thêm 1 khách hàng\n2. Lọc Trạng thái = Khóa",
     "—",
     "- Kết quả là 36 khách hàng"),

    (11, "Mở khóa rồi chọn lại được ở màn nghiệp vụ", "P0",
     "Khách hàng KH-C vừa được Mở khóa.",
     "1. Mở màn tạo báo giá mới\n2. Ở ô chọn khách hàng, gõ tên KH-C",
     "—",
     "- KH-C xuất hiện trở lại trong danh sách chọn"),

    (12, "Khóa hàng loạt bằng cách bấm liên tiếp nhiều dòng", "P2",
     "Có 3 khách hàng đang Hoạt động cần khóa.",
     "1. Khóa lần lượt cả 3 dòng, mỗi lần đều xác nhận\n2. Lọc Trạng thái = Khóa",
     "—",
     "- Cả 3 khách hàng đều chuyển sang Khóa\n"
     "- Lưới cập nhật đúng sau mỗi lần thao tác, không cần tải lại trang"),
]

SEC_VII = [
    (1, "Mở màn Quản lý khách hàng", "P0",
     "Khách hàng KH-D có đủ dữ liệu ở các thẻ. Tài khoản có quyền Xem khách hàng.",
     "1. Mở menu thao tác ở dòng KH-D\n2. Chọn Quản lý",
     "—",
     "- Mở màn Quản lý khách hàng với 6 thẻ: Thông tin chung, Thông tin liên hệ, Báo giá, "
     "Hợp đồng, Danh sách trang thiết bị, Thông tin khác\n"
     "- Thẻ Thông tin chung được chọn sẵn"),

    (2, "Thẻ Thông tin chung hiển thị đúng dữ liệu", "P0",
     "Khách hàng KH-D là doanh nghiệp tư nhân, có 2 người liên hệ.",
     "1. Mở màn Quản lý khách hàng của KH-D\n2. Đọc thẻ Thông tin chung",
     "—",
     "- Hiện đúng tên, mã, mã số thuế, địa chỉ, người đại diện\n"
     "- Hiện đủ 2 người liên hệ"),

    (3, "Thẻ Báo giá liệt kê đúng báo giá của khách hàng", "P0",
     "Khách hàng KH-D có 2 báo giá.",
     "1. Bấm thẻ Báo giá\n2. Đếm số dòng",
     "—",
     "- Hiện đúng 2 báo giá, mỗi dòng có số báo giá, ngày, giá trị, trạng thái\n"
     "- ⚠️ Không lẫn báo giá của khách hàng khác"),

    (4, "Thẻ Hợp đồng liệt kê đúng hợp đồng của khách hàng", "P0",
     "Khách hàng KH-D có 1 hợp đồng.",
     "1. Bấm thẻ Hợp đồng\n2. Đếm số dòng",
     "—",
     "- Hiện đúng 1 hợp đồng với số, ngày ký và giá trị"),

    (5, "Xuất file danh sách báo giá / hợp đồng của khách hàng", "P1",
     "Đang ở thẻ Báo giá của KH-D với 2 dòng.",
     "1. Bấm nút xuất file trên thẻ Báo giá\n2. Mở file tải về",
     "—",
     "- File chứa đúng 2 dòng báo giá của KH-D"),

    (6, "In danh sách báo giá kèm tiêu đề đầu trang", "P1",
     "Đang ở thẻ Báo giá của KH-D.",
     "1. Bấm nút In\n2. Xem bản xem trước",
     "—",
     "- Bản in có tiêu đề đầu trang của công ty (logo và thông tin)\n"
     "- Nội dung không bị cắt lề"),

    (7, "Thẻ Danh sách trang thiết bị hiển thị thiết bị của khách hàng", "P0",
     "Khách hàng KH-D có 5 thiết bị đã bán và 2 thiết bị ngoài hệ thống.",
     "1. Bấm thẻ Danh sách trang thiết bị\n2. Đọc danh sách",
     "—",
     "- Hiện đủ cả thiết bị đã bán qua hệ thống và thiết bị khai thêm từ ngoài\n"
     "- Phân biệt rõ hai nhóm này"),

    (8, "Thêm thiết bị ngoài hệ thống", "P0",
     "Đang ở thẻ Danh sách trang thiết bị. Tài khoản có quyền Sửa khách hàng.",
     "1. Bấm thêm thiết bị\n2. Nhập tên thiết bị, số lượng, thông tin kèm theo\n3. Bấm Lưu",
     "Tên thiết bị: Máy nén khí XYZ · Số lượng: 2",
     "- Thêm thành công, thiết bị mới có mặt trong danh sách"),

    (9, "Sửa thiết bị ngoài hệ thống", "P1",
     "Đã có thiết bị 'Máy nén khí XYZ' số lượng 2.",
     "1. Bấm sửa thiết bị đó\n2. Đổi số lượng thành 3\n3. Bấm Lưu",
     "Số lượng: 3",
     "- Lưu thành công, danh sách hiện số lượng 3"),

    (10, "Xóa thiết bị ngoài hệ thống", "P1",
     "Đã có thiết bị 'Máy nén khí XYZ'.",
     "1. Bấm xóa thiết bị đó\n2. Xác nhận",
     "—",
     "- Thiết bị biến mất khỏi danh sách"),

    (11, "Tăng số lượng thiết bị", "P1",
     "Thiết bị 'Máy A' đang có số lượng 5.",
     "1. Bấm chức năng tăng số lượng ở dòng Máy A\n2. Nhập thêm 3\n3. Bấm Lưu",
     "Thêm: 3",
     "- Số lượng cộng dồn thành 8\n"
     "- ⚠️ Cộng dồn chứ không thay thế giá trị cũ"),

    (12, "Thêm số máy cho thiết bị", "P1",
     "Thiết bị 'Máy A' chưa có số máy.",
     "1. Bấm thêm số máy\n2. Nhập số máy chưa tồn tại\n3. Bấm Lưu",
     "Số máy: SN-2026-001",
     "- Thêm thành công, số máy hiện trong chi tiết thiết bị"),

    (13, "Thêm số máy đã tồn tại", "P0",
     "Số máy SN-2026-001 đã gắn cho thiết bị khác.",
     "1. Thêm số máy SN-2026-001 cho thiết bị B\n2. Bấm Lưu",
     "Số máy: SN-2026-001",
     "- Hệ thống cảnh báo số máy đã tồn tại, cho biết đang thuộc thiết bị nào"),

    (14, "Không có quyền Sửa khách hàng thì không thao tác được thiết bị", "P0",
     "Tài khoản chỉ có quyền Xem khách hàng.",
     "1. Mở thẻ Danh sách trang thiết bị\n2. Quan sát các nút thêm / sửa / xóa thiết bị",
     "—",
     "- Các nút bị vô hiệu hóa\n"
     "- Vẫn xem được danh sách thiết bị"),

    (15, "Thẻ Thông tin khác — tải ảnh lên", "P1",
     "Đang ở thẻ Thông tin khác. Tài khoản có quyền Sửa khách hàng.",
     "1. Bấm chọn ảnh\n2. Chọn một file ảnh hợp lệ\n3. Bấm Lưu",
     "File: anh_khach_hang.jpg",
     "- Tải lên thành công, ảnh hiện trong danh sách file đính kèm\n"
     "- Bấm vào ảnh xem được ảnh phóng to"),

    (16, "Thẻ Thông tin khác — xóa file đính kèm", "P1",
     "Đã có 1 ảnh đính kèm.",
     "1. Bấm xóa ảnh\n2. Xác nhận",
     "—",
     "- Ảnh biến mất khỏi danh sách đính kèm"),

    (17, "Mở màn Lịch sử thay đổi", "P0",
     "Khách hàng KH-P đã được sửa 3 lần.",
     "1. Mở menu thao tác ở dòng KH-P\n2. Chọn Lịch sử",
     "—",
     "- Mở cửa sổ Lịch sử khách hàng, hiện 3 lần thay đổi\n"
     "- ⚠️ Thứ tự MỚI NHẤT ở trên cùng"),

    (18, "Lịch sử hiển thị giá trị cũ và giá trị mới", "P0",
     "Vừa đổi Tên viết tắt của KH-P từ 'KHP' thành 'KHP-2026'.",
     "1. Mở Lịch sử của KH-P\n2. Đọc dòng mới nhất",
     "—",
     "- Dòng ghi rõ trường Tên viết tắt, giá trị cũ 'KHP', giá trị mới 'KHP-2026'\n"
     "- Kèm tên người sửa và thời điểm chính xác tới phút"),

    (19, "Lịch sử ghi nhận thao tác Thêm mới", "P1",
     "Vừa tạo mới khách hàng KH-NEW.",
     "1. Mở Lịch sử của KH-NEW",
     "—",
     "- Có dòng ghi nhận lần Thêm mới, kèm người tạo và thời điểm"),

    (20, "Lịch sử của khách hàng chưa từng sửa", "P1",
     "Khách hàng KH-U vừa được tạo, chưa sửa lần nào.",
     "1. Mở Lịch sử của KH-U",
     "—",
     "- Chỉ có dòng Thêm mới, không có dòng sửa nào\n"
     "- Không báo lỗi, không hiện cửa sổ trống trơn"),

    (21, "Lịch sử ghi nhận thay đổi ở người liên hệ", "P1",
     "Vừa thêm 1 người liên hệ cho KH-P.",
     "1. Mở Lịch sử của KH-P\n2. Đọc dòng mới nhất",
     "—",
     "- Có dòng ghi nhận việc thêm người liên hệ, nêu rõ tên người liên hệ mới"),

    (22, "Đóng cửa sổ Lịch sử", "P2",
     "Đang mở cửa sổ Lịch sử.",
     "1. Bấm nút đóng hoặc bấm ra ngoài cửa sổ",
     "—",
     "- Cửa sổ đóng, quay về danh sách với bộ lọc và trang cũ giữ nguyên"),
]

SEC_VIII = [
    (1, "Mở cửa sổ Import Excel", "P0",
     "Tài khoản có quyền Thêm khách hàng.",
     "1. Mở Danh mục khách hàng\n2. Bấm nút Import Excel",
     "—",
     "- Cửa sổ mở ra, có nút Tải file mẫu, ô chọn file và bảng hướng dẫn các cột"),

    (2, "Tải file mẫu", "P0",
     "Đang ở cửa sổ Import Excel.",
     "1. Bấm nút Tải file mẫu\n2. Mở file tải về",
     "—",
     "- File có 3 trang: trang nhập liệu và các trang danh mục tra cứu\n"
     "- Dòng 1 là tiêu đề cột, ⚠️ dữ liệu bắt đầu từ DÒNG 3\n"
     "- Các trang danh mục có dữ liệu thật của hệ thống (nhóm khách hàng, lĩnh vực, địa chỉ…)"),

    (3, "File mẫu có đủ 26 cột", "P1",
     "Vừa tải file mẫu.",
     "1. Mở file, đọc dòng tiêu đề",
     "—",
     "- Có đủ 26 cột, các cột bắt buộc có dấu sao đỏ\n"
     "- Cột đầu tiên là Tên khách hàng"),

    (4, "Nhập file hợp lệ toàn bộ", "P0",
     "File có 5 dòng khách hàng, tất cả đều hợp lệ và chưa tồn tại.",
     "1. Chọn file\n2. Bấm Load lên bảng rồi bấm Validate\n3. Bấm Import\n4. Xem danh sách",
     "File: 5 dòng hợp lệ",
     "- Thông báo nhập thành công, số dòng thành công là 5, số dòng lỗi là 0\n"
     "- 5 khách hàng mới có mặt trong danh sách"),

    (5, "Bước Validate trước khi ghi dữ liệu", "P0",
     "File có 5 dòng, trong đó dòng 3 thiếu tên khách hàng.",
     "1. Chọn file\n2. Bấm Load lên bảng rồi bấm Validate\n3. Đọc kết quả Validate",
     "File: 5 dòng, 1 dòng lỗi",
     "- Hệ thống liệt kê lỗi theo từng dòng, nêu rõ số dòng và lý do\n"
     "- ⚠️ Chưa có khách hàng nào được ghi vào hệ thống ở bước này"),

    (6, "Nhập file có một phần dòng lỗi", "P0",
     "File có 10 dòng, 7 dòng hợp lệ và 3 dòng lỗi (thiếu số điện thoại).",
     "1. Chọn file, bấm Validate\n2. Bấm Import\n3. Đọc kết quả\n4. Xem danh sách",
     "File: 10 dòng, 3 lỗi",
     "- Thông báo nhập một phần thành công\n"
     "- Số dòng thành công 7, số dòng lỗi 3, cộng lại đúng bằng 10\n"
     "- ⚠️ 7 khách hàng hợp lệ ĐÃ được thêm, 3 dòng lỗi không được thêm"),

    (7, "Nhập file lỗi toàn bộ", "P0",
     "File có 4 dòng, tất cả đều thiếu tên khách hàng.",
     "1. Chọn file, bấm Validate\n2. Bấm Import\n3. Xem danh sách",
     "File: 4 dòng lỗi hết",
     "- Thông báo nhập thất bại, liệt kê lỗi từng dòng\n"
     "- ⚠️ Không có khách hàng nào được thêm"),

    (8, "Nhập file vượt quá giới hạn số dòng", "P0",
     "File có 1.500 dòng dữ liệu. Giới hạn mỗi lần nhập là 1.000 dòng.",
     "1. Chọn file\n2. Bấm Load lên bảng rồi bấm Validate",
     "File: 1.500 dòng",
     "- Hệ thống báo vượt quá số dòng cho phép mỗi lần nhập, nêu rõ giới hạn\n"
     "- Không xử lý file, không thêm khách hàng nào"),

    (9, "Nhập file rỗng", "P1",
     "File chỉ có dòng tiêu đề, không có dòng dữ liệu.",
     "1. Chọn file\n2. Bấm Load lên bảng rồi bấm Validate",
     "File: 0 dòng dữ liệu",
     "- Hệ thống báo file không có dữ liệu\n"
     "- Không báo lỗi kỹ thuật"),

    (10, "Nhập file sai định dạng", "P1",
     "Có một file văn bản đổi đuôi thành đuôi Excel.",
     "1. Chọn file đó\n2. Bấm Load lên bảng rồi bấm Validate",
     "File: file văn bản giả dạng Excel",
     "- Hệ thống báo file không đọc được hoặc không đúng định dạng\n"
     "- Không treo trang"),

    (11, "Nhập file bắt đầu dữ liệu sai dòng", "P0",
     "File có dữ liệu bắt đầu ngay từ dòng 2 thay vì dòng 3.",
     "1. Chọn file\n2. Bấm Load lên bảng rồi bấm Validate\n3. Đọc kết quả",
     "File: dữ liệu từ dòng 2",
     "- ⚠️ Dòng 2 bị bỏ qua, hệ thống chỉ đọc từ dòng 3\n"
     "- QA cần cảnh báo người dùng giữ đúng cấu trúc file mẫu"),

    (12, "Dòng con bỏ trống Tên khách hàng để thêm người liên hệ", "P0",
     "File có dòng 3 là khách hàng tổ chức, dòng 4 và 5 bỏ trống Tên khách hàng nhưng có tên người liên hệ.",
     "1. Chọn file, bấm Validate, bấm Import\n"
     "2. Mở chi tiết khách hàng vừa tạo\n3. Đếm số người liên hệ",
     "File: 1 khách hàng + 2 dòng con",
     "- Chỉ tạo ra 1 khách hàng\n"
     "- ⚠️ Khách hàng đó có 3 người liên hệ (1 từ dòng chính, 2 từ dòng con)"),

    (13, "Dòng con đứng đầu file khi chưa có khách hàng nào", "P1",
     "File có dòng 3 bỏ trống Tên khách hàng.",
     "1. Chọn file, bấm Load lên bảng rồi bấm Validate",
     "—",
     "- Báo lỗi tại dòng 3: không xác định được khách hàng cha\n"
     "- Không thêm dữ liệu"),

    (14, "Nhập trùng mã số thuế đã có trong hệ thống", "P0",
     "File có 1 dòng với mã số thuế 0101234567 đã tồn tại.",
     "1. Chọn file, bấm Load lên bảng rồi bấm Validate",
     "Mã số thuế: 0101234567",
     "- Báo lỗi tại dòng đó: mã số thuế đã tồn tại\n"
     "- Không thêm khách hàng"),

    (15, "Nhập trùng mã số thuế giữa hai dòng trong cùng file", "P0",
     "File có dòng 3 và dòng 5 dùng cùng mã số thuế 0100777666 (chưa tồn tại trong hệ thống).",
     "1. Chọn file, bấm Load lên bảng rồi bấm Validate",
     "Trùng nội bộ file",
     "- ⚠️ Hệ thống phát hiện trùng ngay trong file, báo lỗi rõ ở dòng thứ hai\n"
     "- Không tạo ra hai khách hàng trùng mã số thuế"),

    (16, "Nhập lĩnh vực kinh doanh theo cặp mã", "P0",
     "File có cột Lĩnh vực kinh doanh khách hàng ghi theo cặp, ví dụ LHHDKH.0001:LVKDKH.0003.",
     "1. Điền đúng một cặp hợp lệ vào file\n2. Nhập dữ liệu\n3. Mở chi tiết khách hàng",
     "Cặp: LHHDKH.0001:LVKDKH.0003",
     "- Khách hàng có đúng cặp loại hình – lĩnh vực tương ứng"),

    (17, "Nhập nhiều cặp lĩnh vực trong một ô", "P1",
     "Ô Lĩnh vực ghi hai cặp ngăn nhau bằng dấu phẩy.",
     "1. Nhập dữ liệu\n2. Mở chi tiết khách hàng",
     "LHHDKH.0001:LVKDKH.0003, LHHDKH.0002:LVKDKH.0007",
     "- Khách hàng có đủ 2 cặp lĩnh vực"),

    (18, "Nhập cặp lĩnh vực không khớp nhau", "P0",
     "Ô Lĩnh vực ghi một cặp mà lĩnh vực không thuộc loại hình đó.",
     "1. Chọn file, bấm Load lên bảng rồi bấm Validate",
     "Cặp lệch",
     "- Báo lỗi tại dòng đó: lĩnh vực không thuộc loại hình đã chọn"),

    (19, "Nhập mã danh mục không tồn tại", "P0",
     "File ghi mã tỉnh/thành phố không có trong danh mục.",
     "1. Chọn file, bấm Load lên bảng rồi bấm Validate",
     "Mã tỉnh sai",
     "- Báo lỗi tại dòng đó, nêu rõ giá trị không tìm thấy trong danh mục"),

    (20, "Số điện thoại sai định dạng trong file", "P0",
     "File có dòng khách hàng cá nhân với số điện thoại 12345.",
     "1. Chọn file, bấm Load lên bảng rồi bấm Validate",
     "SĐT: 12345",
     "- Báo lỗi tại dòng đó: số điện thoại không đúng định dạng"),

    (21, "Tiêu đề cột trong file bị sửa tên", "P1",
     "Người dùng đổi tiêu đề cột 'Tên khách hàng' thành 'Tên KH'.",
     "1. Chọn file, bấm Load lên bảng rồi bấm Validate",
     "Tiêu đề: Tên KH",
     "- ⚠️ Vẫn nhận đúng cột vì hệ thống chấp nhận một số cách viết thay thế\n"
     "- Nếu đổi thành tên hoàn toàn khác thì phải báo lỗi thiếu cột"),

    (22, "Thiếu hẳn một cột bắt buộc trong file", "P0",
     "Người dùng xóa hẳn cột Tên khách hàng khỏi file.",
     "1. Chọn file, bấm Load lên bảng rồi bấm Validate",
     "—",
     "- Hệ thống báo thiếu cột bắt buộc, nêu rõ tên cột\n"
     "- Không xử lý tiếp"),

    (23, "Đóng cửa sổ Import giữa chừng", "P1",
     "Đã chọn file và đang xem kết quả kiểm tra.",
     "1. Đóng cửa sổ mà không bấm Import\n2. Xem danh sách khách hàng",
     "—",
     "- Không có khách hàng nào được thêm\n"
     "- Mở lại cửa sổ Import thì trạng thái sạch, không giữ file cũ"),

    (24, "Nhập dữ liệu với file lớn đúng giới hạn", "P1",
     "File có đúng 1.000 dòng hợp lệ.",
     "1. Chọn file, bấm Validate, bấm Import\n2. Bấm giờ thời gian xử lý",
     "File: 1.000 dòng",
     "- Xử lý xong không bị ngắt giữa chừng\n"
     "- Số dòng thành công là 1.000\n"
     "- Ghi nhận thời gian xử lý để đối chiếu"),

    (25, "Khách hàng nhập từ file được ghi nhận người tạo", "P1",
     "Tài khoản T6 vừa nhập 3 khách hàng từ file.",
     "1. Bật cột Người tạo trên lưới\n2. Tìm 3 khách hàng vừa nhập",
     "—",
     "- Cột Người tạo hiện đúng tên của T6"),
]

SEC_IX = [
    (1, "Xuất CSV theo bộ lọc đang áp dụng", "P0",
     "Bộ lọc Tỉnh/Thành phố = Hà Nội cho ra 320 khách hàng.",
     "1. Áp dụng bộ lọc trên\n2. Bấm Xuất CSV\n3. Mở file, đếm số dòng dữ liệu",
     "—",
     "- File có đúng 320 dòng dữ liệu, không kể dòng tiêu đề\n"
     "- ⚠️ Xuất theo bộ lọc chứ không xuất toàn bộ hệ thống"),

    (2, "Xuất Excel theo bộ lọc đang áp dụng", "P0",
     "Bộ lọc cho ra 320 khách hàng.",
     "1. Bấm Xuất Excel\n2. Mở file",
     "—",
     "- File có đúng 320 dòng, tiêu đề cột rõ ràng\n"
     "- Các cột số hiển thị đúng kiểu số, không bị cảnh báo lưu số dưới dạng chữ"),

    (3, "Xuất PDF theo bộ lọc đang áp dụng", "P0",
     "Bộ lọc cho ra 20 khách hàng.",
     "1. Bấm Xuất PDF\n2. Mở file",
     "—",
     "- File hiện đúng 20 khách hàng\n"
     "- Bảng không bị tràn ra ngoài lề, chữ đọc được"),

    (4, "Xuất khi không áp dụng bộ lọc nào", "P1",
     "Không áp dụng bộ lọc, tổng 3.451 khách hàng.",
     "1. Bấm Xuất Excel\n2. Bấm giờ thời gian tải file\n3. Mở file, đếm số dòng",
     "—",
     "- File có đủ 3.451 dòng\n"
     "- ⚠️ Ghi nhận thời gian xuất, không được treo trình duyệt"),

    (5, "Xuất khi bộ lọc không có kết quả", "P1",
     "Bộ lọc cho ra 0 khách hàng.",
     "1. Bấm Xuất Excel\n2. Mở file",
     "—",
     "- Hoặc hệ thống báo không có dữ liệu để xuất, hoặc file chỉ có dòng tiêu đề\n"
     "- Không báo lỗi kỹ thuật"),

    (6, "Cửa sổ Chọn trường xuất Excel", "P0",
     "Đang ở màn danh sách.",
     "1. Bấm Xuất Excel\n2. Quan sát cửa sổ hiện ra",
     "—",
     "- Cửa sổ tên 'Chọn trường xuất Excel', ô Trường xuất liệt kê 20 trường: Mã KH, Tên KH, "
     "MST/SĐT, Đối tượng, Nhóm khách, Địa chỉ, Tỉnh/TP, Tên đơn vị, Tên viết tắt, "
     "Địa chỉ xuất hóa đơn, Hãng xe, Công ty mẹ, Cấp đại lý, Người đại diện, Tên liên hệ, "
     "SĐT liên hệ, Chức vụ liên hệ, Người tạo, Người sửa (gần nhất), Trạng thái\n"
     "- Có dòng hướng dẫn nói rõ thứ tự cột trong file chạy theo thứ tự người dùng chọn"),

    (7, "Bỏ chọn một trường thì file không có cột đó", "P0",
     "Đang mở cửa sổ Chọn trường xuất Excel, đang chọn đủ 20 trường.",
     "1. Bấm dấu x để bỏ trường Tên đơn vị\n2. Bấm Xuất\n3. Mở file, đọc dòng tiêu đề",
     "Bỏ chọn: Tên đơn vị",
     "- File không có cột Tên đơn vị, các cột còn lại đủ và đúng thứ tự"),

    (8, "Bỏ chọn hết các trường", "P1",
     "Đang mở cửa sổ Chọn trường xuất Excel.",
     "1. Bỏ chọn toàn bộ trường\n2. Bấm Xuất",
     "—",
     "- Hệ thống chặn, yêu cầu chọn ít nhất 1 trường"),

    (17, "Thứ tự cột trong file chạy theo thứ tự chọn", "P0",
     "Đang mở cửa sổ Chọn trường xuất Excel.",
     "1. Bỏ chọn hết\n2. Chọn lần lượt Trạng thái, rồi Tên KH, rồi Mã KH\n"
     "3. Bấm Xuất\n4. Mở file, đọc thứ tự cột",
     "Thứ tự chọn: Trạng thái → Tên KH → Mã KH",
     "- ⚠️ Cột trong file theo đúng thứ tự vừa chọn: Trạng thái, Tên KH, Mã KH\n"
     "- Muốn đổi vị trí phải bỏ chọn rồi chọn lại, không kéo thả được"),

    (9, "Nội dung file khớp với nội dung trên lưới", "P0",
     "Bộ lọc cho ra 20 khách hàng, đang sắp xếp theo Tên khách hàng tăng dần.",
     "1. Ghi lại 5 dòng đầu trên lưới\n2. Xuất Excel\n3. So sánh 5 dòng đầu trong file",
     "—",
     "- 5 dòng đầu trong file trùng khớp với lưới cả về nội dung và thứ tự\n"
     "- ⚠️ Thứ tự sắp xếp phải được giữ trong file"),

    (10, "Ký tự tiếng Việt trong file CSV", "P0",
     "Có khách hàng tên 'Doanh nghiệp Đại Việt'.",
     "1. Xuất CSV\n2. Mở file bằng phần mềm bảng tính",
     "—",
     "- ⚠️ Tiếng Việt hiển thị đúng dấu, không bị lỗi font"),

    (11, "Số điện thoại giữ số 0 đầu trong file", "P0",
     "Khách hàng có số điện thoại 0912345678.",
     "1. Xuất Excel\n2. Mở file, đọc ô số điện thoại",
     "—",
     "- ⚠️ Số vẫn là 0912345678, KHÔNG bị mất số 0 ở đầu"),

    (12, "Mã số thuế giữ nguyên định dạng trong file", "P0",
     "Khách hàng có mã số thuế 0101234567-001.",
     "1. Xuất Excel\n2. Đọc ô mã số thuế",
     "—",
     "- Mã số thuế hiện nguyên vẹn cả phần sau dấu gạch ngang"),

    (13, "Cột nhiều giá trị trong file", "P1",
     "Khách hàng có 3 số điện thoại và 2 nhóm khách hàng.",
     "1. Xuất Excel\n2. Đọc ô SĐT và ô Nhóm KH của khách hàng đó",
     "—",
     "- Các giá trị nằm chung một ô, ngăn nhau bằng dấu phẩy, không bị cắt"),

    (14, "Tên file tải về", "P2",
     "Đang xuất file.",
     "1. Xuất lần lượt CSV, Excel, PDF\n2. Đọc tên file tải về",
     "—",
     "- Tên file có ý nghĩa, nhận ra ngay là danh sách khách hàng\n"
     "- Đuôi file đúng với định dạng đã chọn"),

    (15, "Xuất file khi đang ở trang 5", "P1",
     "Bộ lọc cho ra 320 khách hàng, đang xem trang 5.",
     "1. Bấm Xuất Excel\n2. Đếm số dòng trong file",
     "—",
     "- ⚠️ File có đủ 320 dòng của TOÀN BỘ kết quả lọc, không phải chỉ 20 dòng của trang đang xem"),

    (16, "Khách hàng đã Khóa trong file xuất", "P1",
     "Bộ lọc cho ra 50 khách hàng gồm 3 khách hàng đã Khóa.",
     "1. Xuất Excel\n2. Đọc cột Trạng thái",
     "—",
     "- 3 dòng ghi trạng thái Khóa bằng chữ tiếng Việt, không phải số hay ký hiệu"),
]

SEC_X = [
    (1, "Hai người dùng cùng sửa một khách hàng", "P0",
     "Người A và người B cùng mở màn sửa khách hàng KH-P.",
     "1. Người A đổi Tên viết tắt thành 'A1', bấm Lưu\n"
     "2. Người B (chưa tải lại) đổi Tên viết tắt thành 'B1', bấm Lưu\n3. Mở lại chi tiết KH-P",
     "A1 / B1",
     "- Ghi nhận rõ kết quả cuối cùng và cách hệ thống xử lý\n"
     "- ⚠️ Không được mất dữ liệu ngầm mà không báo gì cho người dùng\n"
     "- Lịch sử phải ghi nhận cả hai lần sửa"),

    (2, "Sửa khách hàng vừa bị người khác khóa", "P1",
     "Người A vừa khóa KH-T. Người B đang mở màn sửa KH-T từ trước.",
     "1. Người B bấm Lưu\n2. Quan sát",
     "—",
     "- Hệ thống báo dữ liệu đã thay đổi, không treo trang\n"
     "- Người B biết được lý do không lưu được"),

    (3, "Xem chi tiết khách hàng vừa bị xóa hoặc đổi trạng thái", "P1",
     "Danh sách đang mở, một khách hàng vừa bị người khác khóa.",
     "1. Bấm xem chi tiết khách hàng đó\n2. Quan sát",
     "—",
     "- Mở được chi tiết với trạng thái mới nhất\n"
     "- Không hiện dữ liệu cũ đã lỗi thời"),

    (4, "Cô lập dữ liệu giữa hai tài khoản khác phạm vi", "P0",
     "Tài khoản T2 (cấp công ty A) và T2B (cấp công ty B). Khách hàng KH-A chỉ thuộc công ty A.",
     "1. Đăng nhập T2, tìm KH-A — ghi nhận có kết quả\n"
     "2. Đăng xuất, đăng nhập T2B, tìm KH-A",
     "—",
     "- T2 thấy KH-A, T2B KHÔNG thấy\n"
     "- ⚠️ Cấu hình cột và cài đặt bộ lọc của hai tài khoản cũng độc lập"),

    (5, "Luồng tổng hợp — tạo, sửa, khóa, mở khóa, xem lịch sử", "P0",
     "Tài khoản có đủ quyền Thêm, Sửa, Xóa, Xem khách hàng.",
     "1. Tạo mới một khách hàng tổ chức đủ trường bắt buộc\n"
     "2. Tìm khách hàng đó trên lưới\n3. Sửa Tên viết tắt, lưu\n"
     "4. Khóa khách hàng, xác nhận\n5. Mở khóa lại\n6. Mở Lịch sử",
     "Tên: Công ty Kiểm Thử Luồng",
     "- Mỗi bước đều thành công, thông báo rõ ràng\n"
     "- Lịch sử có đủ các mốc: Thêm mới, Sửa, đổi trạng thái hai lần\n"
     "- Thứ tự lịch sử mới nhất ở trên cùng"),

    (6, "Luồng tổng hợp — nhập từ file rồi xuất ra file", "P0",
     "Tài khoản có quyền Thêm và Xuất dữ liệu khách hàng. File có 5 dòng hợp lệ.",
     "1. Nhập 5 khách hàng từ file\n2. Lọc để chỉ còn 5 khách hàng vừa nhập\n"
     "3. Xuất Excel\n4. So sánh nội dung file xuất với file nhập",
     "File: 5 dòng",
     "- 5 khách hàng trong file xuất khớp với dữ liệu đã nhập\n"
     "- ⚠️ Không sai lệch dấu tiếng Việt, không mất số 0 đầu số điện thoại"),

    (7, "Luồng tổng hợp — tạo khách hàng rồi dùng ngay ở màn báo giá", "P0",
     "Tài khoản có quyền Thêm khách hàng và quyền tạo báo giá.",
     "1. Tạo mới một khách hàng tổ chức\n2. Mở màn tạo báo giá\n"
     "3. Ở ô chọn khách hàng, tìm khách hàng vừa tạo",
     "—",
     "- Khách hàng mới xuất hiện ngay trong danh sách chọn, không cần đăng nhập lại"),

    (8, "Luồng tổng hợp — cấu hình lưới rồi xuất file", "P1",
     "Tài khoản có quyền Xuất dữ liệu khách hàng.",
     "1. Bật cột Công ty mẹ, tắt cột Email\n2. Kéo Email lên đầu rồi tắt đi\n"
     "3. Lọc ra 20 khách hàng\n4. Xuất Excel, chọn cột theo ý muốn\n5. Mở file",
     "—",
     "- File chứa đúng các cột đã tích trong cửa sổ chọn cột\n"
     "- Số dòng đúng 20"),

    (9, "Kiểm tra không rò rỉ khách hàng cá nhân qua chức năng xuất file", "P0",
     "Tài khoản T2 cấp công ty. Có khách hàng cá nhân tự do KH-TD ngoài phạm vi.",
     "1. Đăng nhập T2, xuất Excel toàn bộ danh sách\n2. Tìm KH-TD trong file",
     "—",
     "- ⚠️ KH-TD KHÔNG có trong file\n"
     "- Phạm vi dữ liệu khi xuất file phải giống hệt phạm vi trên lưới"),

    (10, "Đăng xuất giữa chừng khi đang nhập form", "P2",
     "Đang mở màn tạo mới và đã nhập một phần dữ liệu.",
     "1. Để phiên đăng nhập hết hạn hoặc đăng xuất ở tab khác\n2. Bấm Lưu",
     "—",
     "- Hệ thống đưa về màn đăng nhập, không báo lỗi kỹ thuật khó hiểu\n"
     "- Không tạo ra bản ghi rác"),

    (11, "Chuyển đổi qua lại giữa các màn không mất bộ lọc", "P1",
     "Đang lọc Tỉnh/Thành phố = Hà Nội.",
     "1. Sang màn Quản lý khách hàng của một dòng\n2. Quay lại danh sách\n"
     "3. Mở Lịch sử một dòng, đóng lại\n4. Quan sát bộ lọc",
     "—",
     "- Bộ lọc Hà Nội vẫn còn nguyên sau tất cả các thao tác"),

    (12, "Kiểm tra dữ liệu sau khi gộp hai phần mềm cũ", "P0",
     "Dữ liệu khách hàng đến từ hai nguồn cũ đã được gộp về một chỗ.",
     "1. Tìm một khách hàng vốn có ở phần mềm nguồn thứ nhất\n"
     "2. Tìm một khách hàng vốn có ở phần mềm nguồn thứ hai\n"
     "3. Mở chi tiết cả hai",
     "—",
     "- Cả hai đều tìm được và mở chi tiết bình thường\n"
     "- ⚠️ Không có khách hàng nào bị trùng lặp thành hai dòng sau khi gộp\n"
     "- Người tạo và ngày tạo giữ đúng dữ liệu gốc"),
]
