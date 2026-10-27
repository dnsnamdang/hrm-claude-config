# -*- coding: utf-8 -*-
"""Section IV, V, VI - lay du lieu, tinh chi phi, luu / gui duyet / sua."""
from tc_data_role import KK

SEC_IV = [
    ("001", "Lấy dữ liệu đúng các dòng chênh lệch", "P0",
     KK,
     "1. Tạo mới, chọn Từ ngày 01/10, Đến ngày 10/10, Kho vật lý K1\n"
     "2. Bấm Lấy dữ liệu\n"
     "3. Đọc dòng H1 ở tab Hàng thừa",
     "Từ ngày: 01/10\n"
     "Đến ngày: 10/10\n"
     "Kho vật lý: K1",
     "- Khung Phiếu kiểm kê: KK-10, KK-11 đều được chọn\n"
     "- H1: Mã kho KT01, SL 3, Đơn giá bán 150.000, Thành tiền bán 450.000, Đơn giá vốn 100.000, Thành "
     "tiền vốn 300.000, Phiếu xử lý NDC-1\n"
     "- Nút Lưu, Lưu và gửi duyệt sáng lên"),

    ("002", "Hàng thiếu vào tab Hàng thiếu với số lượng dương", "P0",
     KK,
     "1. Lấy dữ liệu như IV.001\n"
     "2. Mở tab Hàng thiếu",
     "—",
     "- H2: SL 2 (không có dấu trừ), Thành tiền bán 600.000, Thành tiền vốn 500.000, Phiếu xử lý XDC-1\n"
     "- H3: SL 1, Thành tiền vốn 50.000, Phiếu xử lý XDC-2\n"
     "- H1 không có ở tab này"),

    ("003", "Chỉ lấy phiếu kiểm kê đã Hoàn thành", "P0",
     KK + "\nKho K1 có thêm KK-13 Chờ xử lý và KK-14 Đang xử lý ngày kiểm 06/10, cùng có chênh lệch",
     "1. Lấy dữ liệu 01/10 đến 10/10, kho K1",
     "—",
     "- Khung Phiếu kiểm kê chỉ có KK-10, KK-11\n"
     "- Không có dòng nào của KK-13, KK-14"),

    ("004", "Lọc theo Ngày kiểm kê tính trọn hai đầu", "P0",
     KK,
     "1. Lấy dữ liệu từ 05/10 đến 05/10, kho K1\n"
     "2. Đổi thành 06/10 đến 07/10, bấm lại",
     "—",
     "- Bước 1: chỉ có KK-10\n"
     "- Bước 2: chỉ có KK-11"),

    ("005", "Chỉ lấy phiếu kiểm kê có kho đã chọn", "P0",
     KK + "\nKho K2 có KK-20 Hoàn thành ngày 06/10, hàng H5 thiếu 4",
     "1. Lấy dữ liệu 01/10 đến 10/10, kho K2\n"
     "2. Đổi sang kho K1, bấm lại",
     "—",
     "- Bước 1: chỉ có KK-20 với H5\n"
     "- Bước 2: chỉ có KK-10, KK-11"),

    ("006", "Phiếu kiểm kê nhiều kho chỉ nên lấy hàng của kho đã chọn", "P1",
     "KK-21 Hoàn thành kiểm 2 kho K1 và K2: H1 ở K1 thừa 2 (đã nhập điều chỉnh ở K1), H6 ở K2 thiếu 1 (đã "
     "xuất điều chỉnh ở K2)",
     "1. Lấy dữ liệu theo ngày của KK-21, kho K1",
     "—",
     "- Mong đợi: chỉ có H1\n"
     "- Lưu ý: nếu H6 cũng hiện và cột Phiếu xử lý, Đơn giá vốn của H6 trống thì ghi Failed"),

    ("007", "Hàng chỉ lệch vị trí không vào biên bản", "P0",
     "KK-12 Hoàn thành ngày 06/10 kho K1: hàng H4 vị trí P1 thiếu 2, vị trí P2 thừa 2 (đã xử lý bằng phiếu "
     "điều chuyển vị trí)",
     "1. Lấy dữ liệu 06/10 đến 06/10, kho K1",
     "—",
     "- Không có dòng H4 ở cả 2 tab\n"
     "- KK-12 không hiện ở khung Phiếu kiểm kê"),

    ("008", "Cộng chênh lệch nhiều vị trí của cùng một hàng", "P1",
     "KK-15 Hoàn thành kho K1: hàng H7 vị trí P1 thừa 5, vị trí P2 thiếu 2 (đã nhập điều chỉnh 3)",
     "1. Lấy dữ liệu theo ngày của KK-15, kho K1",
     "—",
     "- Tab Hàng thừa có 1 dòng H7, SL 3\n"
     "- Lưu ý: nếu SL hoặc Thành tiền gấp đôi thực tế thì ghi Failed"),

    ("009", "Không có phiếu phù hợp", "P1",
     "Kho K3 không có phiếu kiểm kê Hoàn thành nào trong tháng 10",
     "1. Lấy dữ liệu 01/10 đến 31/10, kho K3",
     "—",
     "- Khung Phiếu kiểm kê trống\n"
     "- 2 tab ghi \"Không có dữ liệu\"\n"
     "- Nút Lưu, Lưu và gửi duyệt vẫn mờ"),

    ("010", "Bỏ chọn phiếu kiểm kê ẩn dòng của phiếu đó", "P0",
     KK,
     "1. Lấy dữ liệu như IV.001\n"
     "2. Bỏ chọn KK-11 ở khung Phiếu kiểm kê\n"
     "3. Bấm Lưu, mở lại biên bản",
     "—",
     "- Bước 2: H3 biến mất khỏi tab Hàng thiếu, H1 và H2 còn\n"
     "- Bước 3: biên bản chỉ có H1, H2; khung Phiếu kiểm kê có KK-11 nhưng không được chọn"),

    ("011", "Bấm Lấy dữ liệu lần nữa thay toàn bộ dòng", "P2",
     "Đã lấy dữ liệu, nhập Lý do cho H1",
     "1. Bấm Lấy dữ liệu lần nữa",
     "—",
     "- Danh sách được nạp lại, Lý do vừa nhập bị xóa\n"
     "- % chi phí trở về mặc định"),

    ("012", "Hàng nhập điều chỉnh vào 2 kho kế toán", "P1",
     "KK-16 Hoàn thành kho K1: hàng H8 thừa 4, phiếu nhập điều chỉnh chia vào kho kế toán KT01 và KT02",
     "1. Lấy dữ liệu theo ngày của KK-16, kho K1",
     "—",
     "- Mong đợi: H8 hiện cột Mã kho \"KT01\" và \"KT02\"\n"
     "- Lưu ý: theo code hiện tại bảng không được nạp dữ liệu - ghi Failed"),

    ("013", "Phiếu kiểm kê lên Hoàn thành nhờ phiếu nhập điều chỉnh còn nháp", "P1",
     "KK-17 lên Hoàn thành trong khi phiếu nhập điều chỉnh NDC-5 của hàng H9 vẫn chưa hoàn thành",
     "1. Lấy dữ liệu theo ngày của KK-17\n"
     "2. Nhập đủ Lý do, NV chịu, bấm Lưu",
     "—",
     "- Bước 1: dòng H9 có cột Phiếu xử lý và Đơn giá vốn trống, Thành tiền vốn 0\n"
     "- Bước 2: báo \"Tạo thất bại!\", không có dòng báo lỗi nào trên màn\n"
     "- Lưu ý: ghi Failed, hệ thống cần báo rõ hoặc không cho phiếu kiểm kê lên Hoàn thành"),

    ("014", "Bấm mã ở cột Phiếu xử lý", "P2",
     KK,
     "1. Lấy dữ liệu, bấm NDC-1 ở tab Hàng thừa\n"
     "2. Quay lại, bấm XDC-1 ở tab Hàng thiếu",
     "—",
     "- Bước 1: mở trang chi tiết phiếu nhập NDC-1 ngay ở tab hiện tại\n"
     "- Mong đợi bước 2: mở trang chi tiết phiếu xuất XDC-1 ở tab mới\n"
     "- Lưu ý: theo code hiện tại bước 2 mở trang phiếu NHẬP có cùng số thứ tự - ghi Failed"),

    ("015", "Thêm, bỏ file đính kèm trước khi lưu", "P1",
     "Đã lấy dữ liệu",
     "1. Bấm dấu + ở File đính kèm, chọn file \"bienban.pdf\"\n"
     "2. Bấm thêm ô thứ 2 rồi bấm dấu x ở ô đó",
     "File: bienban.pdf",
     "- Bước 1: ô hiện biểu tượng PDF và tên \"bienban.pdf\"\n"
     "- Bước 2: ô thứ 2 bị bỏ, còn 1 file"),
]


SEC_V = [
    ("001", "Giá trị mặc định của dòng", "P0",
     KK,
     "1. Lấy dữ liệu, đọc dòng H1 ở tab Hàng thừa",
     "—",
     "- Giá xử lý: Giá vốn\n"
     "- % Chi phí nhân viên 100, % Chi phí công ty 0\n"
     "- Chi phí nhân viên 300.000, Chi phí công ty 0\n"
     "- NV chịu trống, Lý do trống"),

    ("002", "Đổi % nhân viên thì % công ty tự đổi", "P0",
     KK,
     "1. Ở dòng H1, nhập % Chi phí nhân viên 40",
     "% Chi phí nhân viên: 40",
     "- % Chi phí công ty tự thành 60\n"
     "- Chi phí nhân viên 120.000, Chi phí công ty 180.000"),

    ("003", "Đổi % công ty thì % nhân viên tự đổi", "P1",
     KK,
     "1. Ở dòng H1, nhập % Chi phí công ty 25",
     "% Chi phí công ty: 25",
     "- % Chi phí nhân viên tự thành 75\n"
     "- Chi phí nhân viên 225.000, Chi phí công ty 75.000"),

    ("004", "Giá xử lý Giá bán tính theo Thành tiền bán", "P0",
     KK,
     "1. Ở dòng H1, chọn Giá xử lý \"Giá bán\", nhập % Chi phí nhân viên 40",
     "Giá xử lý: Giá bán",
     "- Chi phí nhân viên 180.000 (40% của 450.000)\n"
     "- Chi phí công ty 270.000"),

    ("005", "Hàng thiếu tính chi phí tương tự", "P0",
     KK,
     "1. Mở tab Hàng thiếu, đọc dòng H2 để mặc định\n"
     "2. Đổi Giá xử lý H2 sang Giá bán",
     "—",
     "- Bước 1: Chi phí nhân viên 500.000, Chi phí công ty 0\n"
     "- Bước 2: Chi phí nhân viên 600.000"),

    ("006", "Nhập % lớn hơn 100", "P1",
     KK,
     "1. Ở dòng H1, nhập % Chi phí nhân viên 150",
     "% Chi phí nhân viên: 150",
     "- Ô tự về 100, % Chi phí công ty 0"),

    ("007", "Nhập % âm", "P2",
     KK,
     "1. Ở dòng H1, nhập % Chi phí nhân viên -10",
     "% Chi phí nhân viên: -10",
     "- Mong đợi: không cho nhập số âm\n"
     "- Lưu ý: theo code hiện tại % công ty thành 110, Chi phí công ty 330.000 - ghi Failed"),

    ("008", "Xóa trống % nhân viên", "P2",
     KK,
     "1. Ở dòng H1, xóa trống ô % Chi phí nhân viên",
     "—",
     "- % Chi phí công ty thành 100, Chi phí nhân viên 0, Chi phí công ty 300.000"),

    ("009", "Chọn NV chịu", "P1",
     "Có nhân viên NV-C mã NV0123",
     "1. Ở dòng H1, gõ \"NV0123\" vào ô NV chịu, chọn NV-C\n"
     "2. Lưu, mở lại biên bản",
     "NV chịu: NV-C",
     "- Bước 1: ô hiện NV-C\n"
     "- Bước 2: ô NV chịu hiện dạng \"NV0123-<họ tên NV-C>\""),

    ("010", "Mỗi dòng phải có NV chịu riêng", "P1",
     KK,
     "1. Chọn NV chịu NV-C cho H1, để H2 trống, nhập đủ Lý do\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\"\n"
     "- Dưới ô NV chịu của H2 có dòng báo lỗi bằng tiếng Anh, biên bản chưa được tạo"),

    ("011", "Thiếu NV chịu ở tab Hàng thừa không chỉ ra dòng lỗi", "P1",
     KK,
     "1. Nhập đủ Lý do và NV chịu cho H2, H3; để trống NV chịu H1\n"
     "2. Bấm Lưu, mở tab Hàng thừa",
     "—",
     "- Báo \"Tạo thất bại!\"\n"
     "- Mong đợi: dưới ô NV chịu H1 có dòng báo lỗi\n"
     "- Lưu ý: theo code hiện tại không có dòng báo lỗi nào ở tab Hàng thừa - ghi Failed"),

    ("012", "Chi phí công ty sau khi lưu", "P0",
     KK,
     "1. Ở H1 nhập % Chi phí nhân viên 40, chọn NV chịu, nhập Lý do; nhập đủ H2, H3; bấm Lưu\n"
     "2. Mở Chi tiết biên bản, đọc Chi phí công ty H1\n"
     "3. Bấm In, đọc Chi phí công ty H1",
     "% Chi phí nhân viên: 40",
     "- Bước 2: 180.000\n"
     "- Mong đợi bước 3: 180.000\n"
     "- Lưu ý: theo code hiện tại bản In ghi 120.000 (bằng Chi phí nhân viên) - ghi Failed"),
]


SEC_VI = [
    ("001", "Lưu nháp", "P0",
     KK,
     "1. Lấy dữ liệu, nhập Lý do, NV chịu cho mọi dòng, Ghi chú \"Kiểm kê tháng 10\"\n"
     "2. Bấm Lưu",
     "Ghi chú: Kiểm kê tháng 10",
     "- Báo \"Thao tác thành công!\", về danh sách\n"
     "- Dòng mới: Trạng thái Đang tạo, Kho K1, Hàng thừa 3, Hàng thiếu 3, Người lập là mình\n"
     "- Người có quyền duyệt không nhận thông báo"),

    ("002", "Lưu và gửi duyệt", "P0",
     KK,
     "1. Lấy dữ liệu, nhập đủ Lý do, NV chịu\n"
     "2. Bấm Lưu và gửi duyệt",
     "—",
     "- Báo \"Thao tác thành công!\", về danh sách\n"
     "- Biên bản ở Chờ duyệt\n"
     "- Người có quyền duyệt nhận thông báo cần duyệt"),

    ("003", "Mở Sửa hiện đúng dữ liệu đã lưu", "P0",
     "BB-1 Đang tạo đã lưu như VI.001, H1 có % nhân viên 40, NV chịu NV-C, có 1 file đính kèm",
     "1. Bấm bánh răng ở BB-1, chọn Sửa",
     "—",
     "- Tiêu đề kèm số biên bản\n"
     "- Từ ngày, Đến ngày, Kho, Ghi chú, khung Phiếu kiểm kê đúng như lúc lưu\n"
     "- H1: % nhân viên 40, % công ty 60, NV chịu NV-C, Chi phí công ty 180.000\n"
     "- File đã đính kèm hiện, bấm vào mở được"),

    ("004", "Sửa rồi Lưu vẫn giữ Đang tạo", "P0",
     "BB-1 Đang tạo",
     "1. Mở Sửa BB-1, đổi Lý do H2 thành \"Thủ kho làm mất\"\n"
     "2. Bấm Lưu, mở lại Chi tiết",
     "Lý do: Thủ kho làm mất",
     "- Báo \"Thao tác thành công!\"\n"
     "- BB-1 vẫn Đang tạo, Lý do H2 là \"Thủ kho làm mất\""),

    ("005", "Sửa rồi Lưu và gửi duyệt", "P0",
     "BB-1 Đang tạo",
     "1. Mở Sửa BB-1, bấm Lưu và gửi duyệt",
     "—",
     "- BB-1 chuyển Chờ duyệt, menu bánh răng không còn Sửa\n"
     "- Người có quyền duyệt nhận thông báo"),

    ("006", "Sửa: lấy lại dữ liệu theo kho khác", "P1",
     "BB-1 Đang tạo của kho K1; kho K2 có KK-20 Hoàn thành",
     "1. Mở Sửa BB-1, đổi Kho vật lý sang K2, bấm Lấy dữ liệu\n"
     "2. Nhập đủ Lý do, NV chịu, bấm Lưu",
     "Kho vật lý: K2",
     "- BB-1 chuyển sang kho K2, chỉ còn các dòng của KK-20\n"
     "- Cột Hàng thừa, Hàng thiếu trên lưới tính lại theo dòng mới"),

    ("007", "Thêm file khi sửa giữ file cũ", "P1",
     "BB-1 Đang tạo đã có file a.pdf",
     "1. Mở Sửa BB-1, thêm file b.pdf, bấm Lưu\n"
     "2. Mở Chi tiết BB-1",
     "File: b.pdf",
     "- Có cả a.pdf và b.pdf"),

    ("008", "Lưu không kèm file", "P1",
     KK,
     "1. Lấy dữ liệu, nhập đủ Lý do, NV chịu, không thêm file\n"
     "2. Bấm Lưu",
     "—",
     "- Lưu thành công, File đính kèm để trống là hợp lệ"),

    ("009", "Nút Lưu mờ khi chưa có dòng nào", "P1",
     "—",
     "1. Tạo mới, chưa lấy dữ liệu\n"
     "2. Lấy dữ liệu rồi bỏ chọn mọi phiếu ở khung Phiếu kiểm kê",
     "—",
     "- Cả 2 bước: Lưu, Lưu và gửi duyệt bị mờ, không bấm được"),
]
