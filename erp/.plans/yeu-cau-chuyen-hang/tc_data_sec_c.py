# -*- coding: utf-8 -*-
"""Section V (tiep nhan & khong duyet), VI (xoa), VII (in & xuat excel)."""

SEC_V = [
    ("001", "Kế toán kho mở phiếu từ màn Chờ duyệt", "P0",
     "KT-1 có quyền Kế toán kho; công ty có phiếu PYCCH-00042 ở Chờ duyệt",
     "1. Mở màn Phiếu yêu cầu chuyển hàng chờ duyệt\n"
     "2. Bấm Mã yêu cầu PYCCH-00042\n"
     "3. Quan sát khối Ghi chú duyệt và hàng nút",
     "—",
     "- Mở được chi tiết\n"
     "- Khối Ghi chú duyệt hiện và gõ được\n"
     "- Hàng nút có: Không duyệt, Tổng hợp, Quay lại"),

    ("002", "Nút Tổng hợp chuyển sang màn Phiếu yêu cầu xuất hàng", "P0",
     "KT-1; phiếu PYCCH-00042 ở Chờ duyệt",
     "1. Mở chi tiết phiếu, bấm nút Tổng hợp\n"
     "2. Quan sát màn mở ra\n"
     "3. Quay lại danh sách, đọc Trạng thái phiếu PYCCH-00042",
     "—",
     "- Chuyển sang màn tạo Phiếu yêu cầu xuất hàng, loại Xuất điều chuyển kho chi nhánh\n"
     "- Phiếu PYCCH-00042 đã được gắn sẵn, hàng hóa và khách hàng nạp sẵn\n"
     "- ⚠️ Trạng thái phiếu yêu cầu VẪN là Chờ duyệt — chưa đổi ở bước này"),

    ("003", "Trạng thái chỉ đổi sau khi lưu xong Phiếu yêu cầu xuất hàng", "P0",
     "Tiếp nối TC_05.002, đang ở màn tạo Phiếu yêu cầu xuất hàng",
     "1. Thoát khỏi màn mà KHÔNG lưu, quay lại kiểm trạng thái phiếu yêu cầu\n"
     "2. Bấm Tổng hợp lại, lần này điền đủ và LƯU phiếu yêu cầu xuất hàng\n"
     "3. Quay lại kiểm trạng thái, cột Người tiếp nhận và Ngày tiếp nhận\n"
     "4. Đăng nhập người lập phiếu, mở chuông thông báo",
     "—",
     "- Bước 1: phiếu VẪN ở Chờ duyệt, vẫn nằm trong màn Chờ duyệt\n"
     "- Bước 3: trạng thái đổi thành \"Đã tiếp nhận\" (nhãn xanh), cột Người tiếp nhận hiện tên KT-1, "
     "cột Ngày tiếp nhận hiện ngày hôm nay\n"
     "- Bước 4: người lập nhận thông báo \"<tên KT-1> vừa tiếp nhận yêu cầu chuyển hàng: <mã>\"\n"
     "- Phiếu rời khỏi màn Chờ duyệt"),

    ("004", "Thao tác Tổng hợp ngay từ danh sách", "P1",
     "KT-1 ở màn Chờ duyệt, có phiếu đủ điều kiện",
     "1. Mở menu hành động của dòng phiếu\n"
     "2. Bấm mục Tổng hợp",
     "—",
     "- Menu có mục Tổng hợp\n"
     "- Bấm vào chuyển đúng sang màn tạo Phiếu yêu cầu xuất hàng kèm sẵn phiếu của dòng đó"),

    ("005", "Không gộp được yêu cầu của nhiều người khác nhau", "P0",
     "Hai phiếu Chờ duyệt: phiếu A do NV-A lập, phiếu B do NV-B lập, cùng công ty",
     "1. KT-1 bấm Tổng hợp từ phiếu A\n"
     "2. Ở màn Phiếu yêu cầu xuất hàng, thêm tiếp phiếu B vào cùng phiếu xuất\n"
     "3. Bấm Lưu",
     "2 phiếu của 2 người khác nhau",
     "- Hệ thống CHẶN, hiện thông báo \"Phiếu yêu cầu chuyển hàng không cùng 1 người yêu cầu. Vui lòng "
     "kiểm tra lại!\"\n"
     "- Không phiếu nào đổi trạng thái\n"
     "- Gộp 2 phiếu của CÙNG một người thì lưu được bình thường"),

    ("006", "Xóa phiếu yêu cầu xuất hàng trả trạng thái về Chờ duyệt", "P0",
     "Phiếu PYCCH-00042 đang ở Đã tiếp nhận, đã gắn với một Phiếu yêu cầu xuất hàng",
     "1. Xóa hẳn Phiếu yêu cầu xuất hàng đó ở màn của nó\n"
     "2. Quay lại màn Phiếu yêu cầu chuyển hàng, đọc Trạng thái, Người tiếp nhận, Ngày tiếp nhận\n"
     "3. Mở màn Chờ duyệt của KT-1",
     "—",
     "- Phiếu PYCCH-00042 quay về trạng thái Chờ duyệt\n"
     "- Cột Người tiếp nhận và Ngày tiếp nhận được XÓA TRẮNG\n"
     "- Phiếu xuất hiện trở lại trong màn Chờ duyệt"),

    ("007", "Không duyệt bắt buộc nhập Ghi chú duyệt", "P0",
     "KT-1 đang ở màn chi tiết phiếu Chờ duyệt, khối Ghi chú duyệt để TRỐNG",
     "1. Bấm nút Không duyệt\n"
     "2. Quan sát",
     "Ghi chú duyệt: để trống",
     "- Hệ thống chặn, hiện lỗi đỏ ngay dưới khối Ghi chú duyệt\n"
     "- Trạng thái phiếu KHÔNG đổi, vẫn ở Chờ duyệt\n"
     "- ⚠️ Không có hộp thoại xác nhận trước khi gửi — bấm là gửi thẳng"),

    ("008", "Không duyệt thành công đẩy phiếu về Đang tạo", "P0",
     "KT-1 đang ở màn chi tiết phiếu PYCCH-00042 (Chờ duyệt)",
     "1. Nhập Ghi chú duyệt \"Thiếu chứng từ kèm theo\"\n"
     "2. Bấm nút Không duyệt\n"
     "3. Đọc thông báo và quan sát trang chuyển tới\n"
     "4. Mở màn Chờ duyệt và màn Kế toán kho theo dõi, tìm phiếu PYCCH-00042",
     "Ghi chú duyệt: Thiếu chứng từ kèm theo",
     "- Hiện thông báo thành công\n"
     "- Hệ thống chuyển sang màn \"Kế toán kho theo dõi\"\n"
     "- ⚠️ Phiếu về trạng thái ĐANG TẠO (không phải một trạng thái từ chối riêng), nên BIẾN MẤT khỏi "
     "cả màn Chờ duyệt lẫn màn Kế toán kho theo dõi — kế toán kho không còn thấy phiếu nữa\n"
     "- Ghi nhận đúng hiện trạng và báo lại nghiệp vụ nếu thấy bất tiện"),

    ("009", "Người lập nhận thông báo khi bị Không duyệt", "P0",
     "KT-1 vừa Không duyệt một phiếu do NV-A lập",
     "1. Đăng nhập NV-A, mở chuông thông báo\n"
     "2. Bấm vào thông báo\n"
     "3. Đọc khối Ghi chú duyệt trên màn chi tiết",
     "—",
     "- NV-A nhận thông báo \"<tên KT-1> vừa từ chối yêu cầu chuyển hàng: <mã>\"\n"
     "- Bấm vào mở đúng màn chi tiết phiếu\n"
     "- Khối Ghi chú duyệt hiện đúng lý do KT-1 đã nhập\n"
     "- ⚠️ Đây là điểm màn này làm ĐÚNG — có gửi thông báo, khác ba màn phiếu tài chính"),

    ("010", "Người lập sửa lại phiếu bị Không duyệt", "P0",
     "Phiếu Q trạng thái Đang tạo (vừa bị Không duyệt), do NV-A lập",
     "1. NV-A mở menu hành động, kiểm mục Sửa yêu cầu và Xóa yêu cầu\n"
     "2. Bấm Sửa, chỉnh nội dung theo lý do bị từ chối\n"
     "3. Bấm Lưu & Gửi\n"
     "4. KT-1 mở màn Chờ duyệt",
     "—",
     "- Hai mục Sửa yêu cầu và Xóa yêu cầu HIỆN LẠI\n"
     "- Sau khi Lưu & Gửi, phiếu quay lại Chờ duyệt\n"
     "- Phiếu xuất hiện lại ở màn Chờ duyệt của KT-1\n"
     "- ⚠️ Kiểm xem Ghi chú duyệt cũ có bị xóa hay còn lưu — ghi nhận thực tế"),

    ("011", "Người không phải kế toán kho không thấy nút xử lý", "P0",
     "NV-B không có quyền Kế toán kho; NV-B là người lập phiếu đang ở Chờ duyệt",
     "1. NV-B mở chi tiết phiếu của mình\n"
     "2. Quan sát khối Ghi chú duyệt và hàng nút",
     "—",
     "- Khối Ghi chú duyệt KHÔNG hiện (phiếu chưa có ghi chú duyệt nào)\n"
     "- Hàng nút chỉ có Quay lại\n"
     "- Không có Không duyệt và Tổng hợp"),

    ("012", "Kế toán kho khác công ty không xử lý được", "P0",
     "KT-9 có quyền Kế toán kho nhưng thuộc công ty 1; phiếu ở Chờ duyệt do người công ty 3 lập",
     "1. KT-9 mở màn Chờ duyệt, tìm phiếu đó\n"
     "2. Dán thẳng đường dẫn chi tiết phiếu",
     "—",
     "- Phiếu KHÔNG có trong màn Chờ duyệt của KT-9\n"
     "- Mở thẳng chi tiết: ra trang báo không tìm thấy nội dung"),

    ("013", "Phiếu ở trạng thái sau không còn thao tác xử lý", "P1",
     "Phiếu ở Đã tiếp nhận, phiếu ở Đã xuất kho và phiếu ở Đã hủy",
     "1. KT-1 mở chi tiết từng phiếu\n"
     "2. Quan sát hàng nút và menu hành động ngoài danh sách",
     "3 trạng thái",
     "- Màn chi tiết chỉ có nút Quay lại\n"
     "- Menu hành động chỉ có In yêu cầu\n"
     "- Không có Tổng hợp và Không duyệt"),

    ("014", "Không duyệt không làm mất dòng chi tiết", "P1",
     "Phiếu có 2 hàng hóa và 4 dòng khách hàng, đang ở Chờ duyệt",
     "1. KT-1 nhập ghi chú và bấm Không duyệt\n"
     "2. NV-A mở lại chi tiết, đếm hàng hóa và dòng khách hàng, đọc số lượng từng dòng",
     "—",
     "- Vẫn đủ 2 hàng hóa và 4 dòng khách hàng\n"
     "- Số lượng, ngày cần, ghi chú từng dòng không đổi\n"
     "- Tệp đính kèm vẫn còn"),

    ("015", "Màn Chờ duyệt cập nhật khi có phiếu mới gửi lên", "P1",
     "KT-1 đang mở màn Chờ duyệt thấy 4 phiếu; NV-A cùng công ty vừa bấm Lưu & Gửi 1 phiếu",
     "1. Bấm nút tìm kiếm hoặc tải lại trang\n"
     "2. Đọc lại số tổng",
     "—",
     "- Số phiếu tăng thành 5\n"
     "- Phiếu mới nằm đầu danh sách"),
]

SEC_VI = [
    ("001", "Xóa phiếu nháp từ danh sách", "P0",
     "Phiếu T trạng thái Đang tạo do chính người đăng nhập lập, có 2 hàng hóa",
     "1. Mở menu hành động dòng phiếu T, bấm Xóa yêu cầu\n"
     "2. Đọc hộp thoại\n"
     "3. Bấm Xác nhận\n"
     "4. Quan sát danh sách",
     "—",
     "- Hộp thoại tiêu đề \"Xác nhận xóa!\", nội dung \"Bạn chắc chắn muốn xóa bản ghi này?\"\n"
     "- Bấm Xác nhận: thông báo xanh \"Xóa thành công!\"\n"
     "- Phiếu T biến mất khỏi danh sách, tổng giảm 1"),

    ("002", "Hủy hộp thoại xác nhận xóa", "P0",
     "Phiếu T trạng thái Đang tạo",
     "1. Bấm Xóa yêu cầu ở dòng phiếu T\n"
     "2. Bấm nút Hủy\n"
     "3. Quan sát danh sách",
     "—",
     "- Hộp thoại đóng\n"
     "- Phiếu T còn nguyên, tổng không đổi"),

    ("003", "Xóa phiếu xóa theo toàn bộ hàng hóa và dòng khách hàng", "P0",
     "Phiếu V trạng thái Đang tạo, có 3 hàng hóa và 6 dòng khách hàng",
     "1. Ghi lại mã phiếu và các hàng hóa của phiếu V\n"
     "2. Xóa phiếu V\n"
     "3. Nhờ đội kỹ thuật đối chiếu xem hàng hóa và dòng khách hàng của phiếu V còn tồn tại không\n"
     "4. Lọc theo tên, mã hàng hóa bằng mã hàng của phiếu đã xóa",
     "—",
     "- Xóa phiếu thành công\n"
     "- Toàn bộ dòng hàng hóa và dòng khách hàng của phiếu bị XÓA THEO, không để lại dòng mồ côi\n"
     "- Lọc theo mã hàng đó không ra phiếu ma nào\n"
     "- ⚠️ Đây là điểm màn này làm ĐÚNG, khác ba màn phiếu tài chính (những màn đó để lại dòng rác)"),

    ("004", "Menu không có mục Xóa với phiếu đã gửi", "P0",
     "3 phiếu do chính người đăng nhập lập, lần lượt ở Chờ duyệt, Đã tiếp nhận, Đã xuất kho",
     "1. Mở menu hành động của từng phiếu\n"
     "2. Mở màn chi tiết từng phiếu, quan sát hàng nút",
     "3 trạng thái",
     "- Cả 3 phiếu đều KHÔNG có mục Xóa yêu cầu và Sửa yêu cầu\n"
     "- Chỉ còn In yêu cầu"),

    ("005", "Không xóa được phiếu nháp của người khác qua giao diện", "P0",
     "Phiếu nháp do NV-B lập; đăng nhập bằng KT-1 có quyền Kế toán kho cùng công ty",
     "1. Tìm phiếu nháp của NV-B trong mọi chế độ danh sách\n"
     "2. Nếu không thấy, dùng tài khoản quản trị lấy số phiếu rồi dán đường dẫn xóa",
     "—",
     "- Phiếu nháp của NV-B KHÔNG hiện ở bất kỳ chế độ nào của KT-1\n"
     "- Dán thẳng đường dẫn xóa: hệ thống từ chối, hiện thông báo màu vàng \"Không thể xóa!\"\n"
     "- Phiếu VẪN còn nguyên"),

    ("006", "Không xóa được phiếu đã gửi bằng đường dẫn trực tiếp", "P0",
     "Phiếu R trạng thái Đã tiếp nhận, do chính người đăng nhập lập",
     "1. Lấy đường dẫn xóa của phiếu R (thay số phiếu vào đường dẫn xóa của một phiếu nháp)\n"
     "2. Dán vào thanh địa chỉ\n"
     "3. Kiểm tra phiếu còn hay mất",
     "—",
     "- Hệ thống TỪ CHỐI, hiện thông báo màu vàng \"Không thể xóa!\"\n"
     "- Phiếu R VẪN còn nguyên, trạng thái không đổi\n"
     "- ⚠️ Điểm làm đúng của màn này"),

    ("007", "Xóa phiếu vừa bị Không duyệt", "P1",
     "Phiếu Q vừa bị Không duyệt nên đã về Đang tạo, do chính người đăng nhập lập",
     "1. Mở menu hành động, bấm Xóa yêu cầu, xác nhận\n"
     "2. Tìm lại phiếu Q",
     "—",
     "- Xóa được (phiếu đang ở Đang tạo và đúng người lập)\n"
     "- Tìm lại không ra dòng nào"),

    ("008", "Xóa phiếu xong quay lại đúng chỗ", "P2",
     "Đang ở trang 2 của danh sách, lọc Trạng thái = Đang tạo",
     "1. Xóa 1 phiếu ở trang 2\n"
     "2. Quan sát trang hiện ra sau khi xóa",
     "—",
     "- Quay lại màn danh sách kèm thông báo xanh\n"
     "- Ghi nhận thực tế trang và bộ lọc có được giữ hay không"),
]

SEC_VII = [
    ("001", "In yêu cầu từ menu hành động", "P0",
     "Danh sách đang có phiếu do chính người đăng nhập lập",
     "1. Mở menu hành động của một dòng, bấm In yêu cầu\n"
     "2. Quan sát trang mở ra",
     "—",
     "- Mở bản in của đúng phiếu đó\n"
     "- Bản in dùng một mẫu duy nhất cho mọi trạng thái"),

    ("002", "Nội dung bản in", "P0",
     "Phiếu có 2 hàng hóa, mỗi hàng hóa 2 dòng khách hàng, đã điền Ghi chú",
     "1. Mở bản in\n"
     "2. Đọc từ trên xuống, đối chiếu với màn chi tiết",
     "—",
     "- Trên cùng có biểu trưng của công ty người lập\n"
     "- Có Mã yêu cầu, Ngày lập, Người lập, Ghi chú\n"
     "- Bảng hiện đủ 2 hàng hóa và 4 dòng khách hàng, đúng cấu trúc lồng nhau\n"
     "- Mỗi dòng khách hàng có Khách hàng, Số lượng, Ngày cần, Ghi chú"),

    ("003", "In phiếu của người khác bị chặn", "P0",
     "Tài khoản C chỉ có quyền xem theo công ty, không có quyền Kế toán kho; phiếu X của người khác "
     "cùng công ty",
     "1. Tìm phiếu X trong danh sách\n"
     "2. Mở menu hành động, bấm In yêu cầu",
     "—",
     "- ⚠️ Hiện trạng: mục In yêu cầu VẪN hiện trong menu nhưng bấm vào ra trang báo không tìm thấy "
     "nội dung. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: hoặc cho in được, hoặc ẩn hẳn mục In khỏi menu\n"
     "- Cùng phiếu đó, tài khoản KT-1 (kế toán kho cùng công ty) in được bình thường"),

    ("004", "In phiếu ở mọi trạng thái", "P1",
     "5 phiếu do chính người đăng nhập lập, ở 5 trạng thái khác nhau gồm cả Đang tạo và Đã hủy",
     "1. Với mỗi phiếu, bấm In yêu cầu",
     "—",
     "- Cả 5 phiếu đều in được, không trạng thái nào bị chặn\n"
     "- Bản in hiện đúng nội dung từng phiếu"),

    ("005", "In phiếu không tồn tại", "P2",
     "Người đăng nhập bất kỳ",
     "1. Gõ đường dẫn in với một số phiếu chắc chắn không tồn tại",
     "Số phiếu: 99999999",
     "- Hệ thống hiện trang báo không tìm thấy\n"
     "- Không treo trang trắng"),

    ("006", "Xuất Excel danh sách", "P0",
     "Danh sách đang có 12 phiếu, không đặt bộ lọc",
     "1. Bấm nút Xuất excel\n"
     "2. Chờ tệp tải về, mở tệp\n"
     "3. Đếm số dòng và đối chiếu nội dung với màn hình",
     "—",
     "- Mở TAB MỚI để tải, tệp tên danh_sach_yeu_cau_chuyen_hang.xlsx\n"
     "- Tệp có đúng 12 dòng dữ liệu\n"
     "- 7 cột: STT, Mã yêu cầu, Người tạo, Ngày tạo, Người tiếp nhận, Ngày tiếp nhận, Trạng thái\n"
     "- Cột Trạng thái ghi đúng tên trạng thái bằng chữ, không phải con số"),

    ("007", "Xuất Excel áp đúng bộ lọc đang dùng", "P0",
     "Đang lọc Trạng thái = Chờ duyệt và Người tạo = NV-B, kết quả 3 phiếu",
     "1. Bấm Xuất excel, mở tệp\n"
     "2. Đếm số dòng, soát cột Trạng thái và Người tạo",
     "—",
     "- Tệp có đúng 3 dòng\n"
     "- Mọi dòng đều là Chờ duyệt và do NV-B lập\n"
     "- ⚠️ Nếu tệp ra đủ toàn bộ danh sách thay vì 3 dòng thì ghi Failed"),

    ("008", "Xuất Excel ở màn Chờ duyệt", "P1",
     "Tài khoản KT-1 đang ở màn Chờ duyệt với 4 phiếu",
     "1. Tìm nút Xuất excel trên màn\n"
     "2. Nếu có, bấm và mở tệp",
     "—",
     "- Ghi nhận thực tế: màn Chờ duyệt (vào từ menu) CÓ nút Xuất excel, còn màn Kế toán kho theo dõi "
     "thì KHÔNG\n"
     "- Nếu xuất được thì tệp phải đúng 4 phiếu đang hiện"),

    ("009", "Xuất Excel khi bảng rỗng", "P2",
     "Đang lọc bằng điều kiện không khớp phiếu nào",
     "1. Bấm nút Xuất excel\n"
     "2. Mở tệp",
     "—",
     "- Tệp vẫn tải về được, không báo lỗi\n"
     "- Bảng trong tệp chỉ có dòng tiêu đề, không có dòng dữ liệu"),

    ("010", "Bản in của phiếu có nhiều hàng hóa và nhiều khách hàng", "P1",
     "Phiếu có 3 hàng hóa với tổng 6 dòng khách hàng",
     "1. Mở bản in\n"
     "2. Đếm số khối hàng hóa và số dòng khách hàng\n"
     "3. Kiểm bố cục khi in ra giấy",
     "—",
     "- Bản in hiện đủ 3 khối hàng hóa và 6 dòng khách hàng\n"
     "- Không dòng nào bị mất hay bị gộp nhầm sang hàng hóa khác\n"
     "- Bảng không tràn khỏi mép giấy"),
]
