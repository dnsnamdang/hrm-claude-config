# -*- coding: utf-8 -*-
"""Section V (duyet & khong duyet), VI (xoa), VII (in & xuat excel)."""

SEC_V = [
    ("001", "Kế toán mở phiếu từ màn Chờ duyệt", "P0",
     "KT-1 có quyền Kế toán thanh toán; công ty có phiếu mã kết thúc .00015 ở Chờ tạo phiếu kế toán",
     "1. Mở màn Phiếu yêu cầu điều chỉnh công nợ chờ duyệt\n"
     "2. Bấm Mã phiếu .00015\n"
     "3. Quan sát hàng nút dưới cùng",
     "—",
     "- Mở được chi tiết\n"
     "- Hàng nút có: Tạo phiếu kế toán, Không duyệt, Quay lại\n"
     "- Không có nút Sửa, Xóa, In, Xuất Excel"),

    ("002", "Nút Tạo phiếu kế toán chuyển sang màn Phiếu kế toán", "P0",
     "KT-1; phiếu .00015 đang ở Chờ tạo phiếu kế toán",
     "1. Mở chi tiết phiếu .00015\n"
     "2. Bấm nút Tạo phiếu kế toán\n"
     "3. Quan sát màn mở ra\n"
     "4. Quay lại kiểm trạng thái phiếu .00015",
     "—",
     "- Chuyển sang màn tạo Phiếu kế toán điều chỉnh công nợ, phiếu yêu cầu đã gắn sẵn\n"
     "- Các dòng điều chỉnh từ và điều chỉnh đến được nạp sẵn\n"
     "- Trạng thái phiếu yêu cầu CHƯA đổi ở bước này"),

    ("003", "Thao tác Tạo phiếu kế toán ngay từ danh sách", "P1",
     "KT-1 ở màn Chờ duyệt, có phiếu đủ điều kiện",
     "1. Mở menu hành động của dòng phiếu\n"
     "2. Bấm mục Tạo phiếu kế toán",
     "—",
     "- Menu có mục Tạo phiếu kế toán\n"
     "- Bấm vào chuyển đúng sang màn tạo Phiếu kế toán kèm sẵn phiếu yêu cầu của dòng đó"),

    ("004", "Cửa sổ Không duyệt bắt buộc nhập lý do", "P0",
     "KT-1 đang ở màn chi tiết phiếu Chờ tạo phiếu kế toán",
     "1. Bấm nút Không duyệt\n"
     "2. Quan sát hộp thoại\n"
     "3. Bấm Xác nhận khi ô lý do còn TRỐNG\n"
     "4. Nhập vài dấu cách rồi bấm Xác nhận",
     "Lý do: để trống, rồi vài dấu cách",
     "- Hộp thoại tiêu đề \"Bạn chắc chắn không duyệt phiếu?\", bên trong có ô nhập nhiều dòng với gợi "
     "ý \"Nhập lý do không duyệt (bắt buộc)\"\n"
     "- Để trống: hiện dòng chữ đỏ \"Vui lòng nhập lý do không duyệt\" NGAY TRONG hộp thoại, hộp thoại "
     "KHÔNG đóng\n"
     "- Chỉ nhập dấu cách cũng bị chặn y như để trống"),

    ("005", "Không duyệt thành công", "P0",
     "Vẫn phiếu ở TC_05.004",
     "1. Nhập lý do \"Sai hợp đồng điều chỉnh đến\"\n"
     "2. Bấm Xác nhận\n"
     "3. Đọc thông báo và quan sát trang chuyển tới\n"
     "4. Mở lại chi tiết phiếu",
     "Lý do: Sai hợp đồng điều chỉnh đến",
     "- Hộp thoại đóng, hiện thông báo xanh thành công\n"
     "- Hệ thống chuyển về màn Chờ duyệt, phiếu KHÔNG còn trong danh sách đó\n"
     "- Mở lại chi tiết: trạng thái Từ chối, nội dung lý do không duyệt được lưu và hiển thị"),

    ("006", "Hủy hộp thoại Không duyệt", "P0",
     "KT-1 đang mở hộp thoại Không duyệt, đã gõ lý do",
     "1. Bấm nút Hủy\n"
     "2. Kiểm trạng thái phiếu\n"
     "3. Mở lại hộp thoại Không duyệt",
     "—",
     "- Hộp thoại đóng, trạng thái phiếu KHÔNG đổi\n"
     "- Mở lại thì ô lý do TRỐNG, không giữ nội dung lần trước"),

    ("007", "Không duyệt không gửi thông báo cho người lập", "P0",
     "KT-1 vừa Không duyệt một phiếu do NV-A lập",
     "1. Đăng nhập NV-A, mở chuông thông báo, đếm số thông báo mới\n"
     "2. Mở màn danh sách, tìm phiếu vừa bị từ chối",
     "—",
     "- ⚠️ Hiện trạng: NV-A KHÔNG nhận được thông báo nào. Người lập phải tự vào xem mới biết. Ghi "
     "nhận Failed\n"
     "- Kỳ vọng đúng: gửi thông báo cho người lập kèm lý do từ chối\n"
     "- Phiếu vẫn hiện đúng trạng thái Từ chối trong danh sách của NV-A"),

    ("008", "Người lập sửa lại phiếu bị từ chối", "P0",
     "Phiếu trạng thái Từ chối do NV-A lập",
     "1. Đăng nhập NV-A, mở chi tiết phiếu, đọc lý do từ chối\n"
     "2. Mở menu hành động, bấm Sửa\n"
     "3. Chỉnh lại nội dung, bấm Lưu và gửi duyệt\n"
     "4. Đăng nhập KT-1, mở màn Chờ duyệt",
     "—",
     "- NV-A sửa được\n"
     "- Phiếu quay lại Chờ tạo phiếu kế toán và xuất hiện lại ở màn Chờ duyệt của KT-1\n"
     "- ⚠️ Kiểm xem lý do từ chối cũ có bị xóa hay còn lưu lại trên phiếu — ghi nhận thực tế"),

    ("009", "Người không phải kế toán không thấy nút xử lý", "P0",
     "NV-B không có quyền Kế toán thanh toán nhưng nhìn thấy được phiếu Chờ tạo phiếu kế toán trong "
     "phạm vi quyền xem",
     "1. Mở chi tiết phiếu đó bằng NV-B\n"
     "2. Quan sát hàng nút\n"
     "3. Mở menu hành động của dòng đó ngoài danh sách",
     "—",
     "- Màn chi tiết chỉ có nút Quay lại\n"
     "- Menu hành động chỉ có In và Xuất Excel\n"
     "- Không có Tạo phiếu kế toán và Không duyệt"),

    ("010", "Phiếu ở trạng thái cuối không còn thao tác xử lý", "P1",
     "Phiếu ở Đã tạo phiếu kế toán, phiếu ở Đã duyệt phiếu kế toán và phiếu ở Hủy",
     "1. Mở chi tiết từng phiếu bằng tài khoản KT-1\n"
     "2. Quan sát hàng nút và menu hành động ngoài danh sách",
     "3 trạng thái",
     "- Màn chi tiết chỉ có nút Quay lại\n"
     "- Menu hành động chỉ có In và Xuất Excel\n"
     "- Không có Tạo phiếu kế toán và Không duyệt"),

    ("011", "Không duyệt không làm mất dòng chi tiết", "P1",
     "Phiếu có 2 dòng Điều chỉnh từ và tổng 4 dòng Điều chỉnh đến, đang ở Chờ tạo phiếu kế toán",
     "1. Kế toán nhập lý do và bấm Không duyệt\n"
     "2. Mở lại chi tiết, đếm dòng và đọc số tiền từng dòng",
     "—",
     "- Vẫn đủ 2 dòng từ và 4 dòng đến, số tiền không đổi\n"
     "- Cột Số tiền ngoài danh sách không đổi"),

    ("012", "Màn Chờ duyệt cập nhật khi có phiếu mới gửi lên", "P1",
     "KT-1 đang mở màn Chờ duyệt thấy 3 phiếu; NV-A cùng công ty vừa gửi duyệt 1 phiếu",
     "1. Bấm nút tìm kiếm hoặc tải lại trang\n"
     "2. Đọc lại số tổng",
     "—",
     "- Số phiếu tăng thành 4\n"
     "- Phiếu mới nằm đầu danh sách"),
]

SEC_VI = [
    ("001", "Xóa phiếu nháp từ danh sách", "P0",
     "Phiếu T trạng thái Đang tạo do chính người đăng nhập lập",
     "1. Mở menu hành động dòng phiếu T, bấm Xóa\n"
     "2. Đọc hộp thoại\n"
     "3. Bấm Xác nhận\n"
     "4. Quan sát danh sách",
     "—",
     "- Hộp thoại tiêu đề \"Xác nhận xóa!\", nội dung \"Bạn chắc chắn muốn xóa bản ghi này?\"\n"
     "- Bấm Xác nhận: thông báo xanh \"Xóa phiếu yêu cầu điều chỉnh thành công!\"\n"
     "- Phiếu T biến mất khỏi danh sách, tổng giảm 1"),

    ("002", "Hủy hộp thoại xác nhận xóa", "P0",
     "Phiếu T trạng thái Đang tạo",
     "1. Bấm Xóa ở dòng phiếu T\n"
     "2. Bấm nút Hủy\n"
     "3. Quan sát danh sách",
     "—",
     "- Hộp thoại đóng\n"
     "- Phiếu T còn nguyên, tổng không đổi"),

    ("003", "Xóa phiếu ở trạng thái Từ chối", "P0",
     "Phiếu U trạng thái Từ chối do chính người đăng nhập lập",
     "1. Mở menu hành động, bấm Xóa, xác nhận\n"
     "2. Tìm lại phiếu U bằng ô Mã phiếu",
     "—",
     "- Xóa thành công, thông báo xanh\n"
     "- Tìm lại không ra dòng nào"),

    ("004", "Menu không có nút Xóa với phiếu đã gửi duyệt hoặc đã xử lý", "P0",
     "3 phiếu do chính người đăng nhập lập, lần lượt ở Chờ tạo phiếu kế toán, Đã tạo phiếu kế toán, "
     "Đã duyệt phiếu kế toán",
     "1. Mở menu hành động của từng phiếu",
     "3 trạng thái",
     "- Cả 3 phiếu đều KHÔNG có mục Xóa và không có mục Sửa\n"
     "- Chỉ còn In và Xuất Excel"),

    ("005", "Nút Xóa hiện sai với phiếu Đang tạo của người khác", "P0",
     "Người đăng nhập nhìn thấy được một phiếu Đang tạo do NV-B lập (xem cách dựng ở TC_03.009)",
     "1. Mở menu hành động của dòng đó\n"
     "2. So với một phiếu Từ chối của NV-B",
     "—",
     "- ⚠️ Hiện trạng: phiếu Đang tạo của NGƯỜI KHÁC vẫn hiện nút Xóa; phiếu Từ chối của người khác thì "
     "không. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: cả hai trạng thái đều phải xét đúng người lập"),

    ("006", "Xóa được phiếu bất kỳ bằng đường dẫn trực tiếp", "P0",
     "Phiếu trạng thái Đã duyệt phiếu kế toán do người khác lập; đã sao lưu dữ liệu trước khi test",
     "1. Lấy đường dẫn xóa (thay số phiếu vào đường dẫn xóa của một phiếu nháp của mình)\n"
     "2. Dán vào thanh địa chỉ\n"
     "3. Kiểm tra phiếu còn hay mất",
     "—",
     "- ⚠️ Hiện trạng: phiếu BỊ XÓA, hệ thống báo xóa thành công dù không đúng người lập và không đúng "
     "trạng thái. LỖ HỔNG, ghi nhận Failed\n"
     "- Kỳ vọng đúng: từ chối và giữ nguyên phiếu\n"
     "- Khôi phục dữ liệu ngay sau khi test"),

    ("007", "Xóa phiếu không xóa theo dòng chi tiết", "P0",
     "Phiếu V trạng thái Đang tạo, có 2 dòng Điều chỉnh từ và 3 dòng Điều chỉnh đến",
     "1. Ghi lại mã phiếu và các hợp đồng của phiếu V\n"
     "2. Xóa phiếu V\n"
     "3. Nhờ đội kỹ thuật đối chiếu xem các dòng chi tiết của phiếu V còn tồn tại hay không\n"
     "4. Tạo phiếu mới, chọn lại đúng các hợp đồng đó",
     "—",
     "- Xóa phiếu thành công, phiếu không còn trên danh sách\n"
     "- ⚠️ Hiện trạng: các dòng chi tiết của phiếu đã xóa VẪN nằm lại trong hệ thống. Ghi nhận Failed — "
     "dữ liệu rác này làm sai các phép cộng theo dòng chi tiết và làm sai bộ lọc theo hợp đồng\n"
     "- Kiểm ngay: lọc theo Hợp đồng điều chỉnh từ bằng mã hợp đồng của phiếu đã xóa, xem có ra phiếu "
     "ma nào không"),

    ("008", "Xóa phiếu xong quay lại đúng chỗ", "P2",
     "Đang ở trang 2 của danh sách, lọc Trạng thái = Đang tạo",
     "1. Xóa 1 phiếu ở trang 2\n"
     "2. Quan sát trang hiện ra sau khi xóa",
     "—",
     "- Quay lại màn danh sách kèm thông báo xanh\n"
     "- Ghi nhận thực tế trang và bộ lọc có được giữ hay không"),
]

SEC_VII = [
    ("001", "In phiếu từ menu hành động", "P0",
     "Danh sách đang có phiếu loại khách hàng",
     "1. Mở menu hành động của một dòng, bấm In\n"
     "2. Quan sát trang mở ra",
     "—",
     "- Mở bản in của đúng phiếu đó, khổ giấy NGANG\n"
     "- Bản in dùng một mẫu duy nhất cho cả hai loại phiếu"),

    ("002", "Nội dung khối đầu bản in", "P0",
     "Phiếu tạo từ Phiếu báo có, đã có Diễn giải",
     "1. Mở bản in\n"
     "2. Đọc từ trên xuống",
     "—",
     "- Trên cùng là phần đầu trang của công ty người lập\n"
     "- Có Mã phiếu, Mã phiếu báo có, Người tạo, Phòng ban, Diễn giải và Ngày / Tháng / Năm lập\n"
     "- Mọi thông tin khớp với màn chi tiết\n"
     "- Phiếu lập tay thì ô Mã phiếu báo có để trống"),

    ("003", "Bảng chi tiết trên bản in", "P0",
     "Phiếu khách hàng có 2 dòng Điều chỉnh từ, mỗi dòng 2 dòng Điều chỉnh đến",
     "1. Mở bản in\n"
     "2. Đối chiếu số dòng và số tiền với màn chi tiết",
     "—",
     "- Bản in hiện đủ cả 2 dòng Điều chỉnh từ và 4 dòng Điều chỉnh đến, đúng cấu trúc lồng nhau\n"
     "- Số tiền có dấu chấm ngăn nghìn\n"
     "- Không dòng nào bị mất hay bị gộp nhầm"),

    ("004", "Bản in của phiếu NCC", "P1",
     "Phiếu loại Điều chỉnh công nợ NCC, loại tiền VND",
     "1. Mở bản in\n"
     "2. Đọc tiêu đề cột và nội dung",
     "—",
     "- Bản in dùng cùng mẫu với phiếu khách hàng\n"
     "- ⚠️ Kiểm kỹ tiêu đề cột có đổi thành Nhà cung cấp / Hợp đồng mua hay vẫn để nhãn của phiếu "
     "khách hàng; ghi nhận thực tế và báo lại nghiệp vụ nếu nhãn không khớp"),

    ("005", "Bản in của phiếu NCC dùng ngoại tệ", "P1",
     "Phiếu NCC loại tiền USD, tỷ giá 25.000, số tiền 1.000 USD",
     "1. Mở bản in\n"
     "2. Tìm các số tiền và thông tin loại tiền, tỷ giá",
     "—",
     "- Ghi nhận thực tế: bản in hiện số nguyên tệ, số quy đổi hay cả hai\n"
     "- ⚠️ Nếu bản in không thể hiện được loại tiền và tỷ giá thì ghi nhận và báo lại nghiệp vụ"),

    ("006", "In phiếu ở mọi trạng thái", "P1",
     "5 phiếu ở 5 trạng thái khác nhau, gồm cả Đang tạo và Từ chối",
     "1. Với mỗi phiếu, bấm In từ menu hành động",
     "—",
     "- Cả 5 phiếu đều in được, không trạng thái nào bị chặn\n"
     "- Bản in của phiếu Từ chối hiển thị được nội dung lý do không duyệt (nếu mẫu có ô này)"),

    ("007", "Xuất Excel một phiếu", "P0",
     "Danh sách đang có phiếu",
     "1. Mở menu hành động của một dòng, bấm Xuất Excel\n"
     "2. Chờ tệp tải về, mở tệp",
     "—",
     "- Tệp tải về tên chi_tiet_yeu_cau_dieu_chinh_cong_no.xlsx\n"
     "- Mở được bằng Excel, không báo hỏng tệp\n"
     "- Nội dung khớp với bản in: thông tin chung và bảng chi tiết"),

    ("008", "Tệp Excel của mọi phiếu trùng tên", "P1",
     "Danh sách đang có ít nhất 3 phiếu",
     "1. Xuất Excel lần lượt 3 phiếu khác nhau\n"
     "2. Mở thư mục tải về, đọc tên 3 tệp",
     "—",
     "- ⚠️ Hiện trạng: cả 3 tệp mang CÙNG một tên, trình duyệt phải tự đánh số thêm để phân biệt. Ghi "
     "nhận Failed\n"
     "- Kỳ vọng đúng: tên tệp kèm mã phiếu như màn Đề nghị thanh toán\n"
     "- Mở 3 tệp kiểm nội dung có đúng 3 phiếu khác nhau không, tránh trường hợp ghi đè"),

    ("009", "Xuất Excel phiếu ở mọi trạng thái", "P2",
     "5 phiếu ở 5 trạng thái khác nhau",
     "1. Với mỗi phiếu, bấm Xuất Excel",
     "—",
     "- Cả 5 phiếu đều xuất được, không trạng thái nào bị chặn"),

    ("010", "In phiếu có dòng thiếu hợp đồng", "P2",
     "Phiếu cũ có dòng chi tiết trỏ tới hợp đồng đã bị xóa",
     "1. Mở bản in của phiếu đó",
     "—",
     "- Bản in VẪN hiện ra, không trắng trang và không báo lỗi\n"
     "- Dòng đó để trống mã hợp đồng, số dư hiện 0"),
]
