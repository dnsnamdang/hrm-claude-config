# -*- coding: utf-8 -*-
"""Section V-VII: nhap bao gia NCC, sua / luu / gui, man chi tiet & tab Tong hop."""
from tc_data_role import MAU, NCC

PHIEU = "THGVC-1 Đang tạo của NV-VC1, lập từ mẫu MB-1.\n" + MAU

SEC_V = [
    ("001", "Mở cửa sổ Nhập báo giá của NCC", "P0",
     PHIEU,
     "1. Ở danh sách mở Hành động THGVC-1, bấm \"Nhập báo giá của NCC\"",
     "—",
     "- Cửa sổ tiêu đề \"Nhập báo giá của NCC cho tổng hợp báo giá số: THGVC-...\"\n"
     "- Ô Chọn nhà cung cấp, ô File báo giá, đường dẫn \"Mẫu báo giá\", nút Đóng, Lưu lại"),

    ("002", "Tải file mẫu báo giá", "P0",
     PHIEU,
     "1. Trong cửa sổ nhập bấm \"Mẫu báo giá\"",
     "—",
     "- Tải file Mau_bao_gia_van_chuyen.xlsx\n"
     "- File có dòng tên loại xe \"Xe tải\", dòng trọng tải \"1,5 tấn\", \"5 tấn\", dòng Giá cước vượt trội và 2 "
     "dòng tuyến K1 đi Hải Phòng, K1 đi Bắc Ninh"),

    ("003", "Nhập báo giá NCC A thành công", "P0",
     PHIEU + "\n" + NCC,
     "1. Mở cửa sổ nhập, chọn NCC A, chọn file NCC A\n"
     "2. Bấm Lưu lại\n"
     "3. Mở Sửa THGVC-1",
     "File: bao-gia-ncc-a.xlsx",
     "- Báo \"Nhập báo giá thành công\", cửa sổ đóng\n"
     "- Màn Sửa có tab NCC A, link File báo giá bao-gia-ncc-a.xlsx\n"
     "- Giá cước vượt trội 12,000 / 18,000; Hải Phòng 2,000,000 / 3,500,000; Bắc Ninh 1,000,000 / 1,800,000"),

    ("004", "Nhập thêm NCC thứ hai", "P0",
     "THGVC-1 đã có NCC A.\n" + NCC,
     "1. Nhập file cho NCC B\n"
     "2. Mở Sửa THGVC-1",
     "—",
     "- Có 2 tab NCC A, NCC B; giá NCC A không đổi"),

    ("005", "Nhập lại cho NCC đã có báo giá", "P0",
     "THGVC-1 đã có NCC A; file mới NCC A sửa Hải Phòng 1,5 tấn = 1.900.000",
     "1. Mở cửa sổ nhập, chọn NCC A, chọn file mới, bấm Lưu lại\n"
     "2. Ở hộp hỏi bấm Xác nhận",
     "—",
     "- Hiện hộp \"Đã nhập báo giá\" - \"Bạn đã nhập báo giá cho nhà cung cấp này. Bạn có muốn tiếp tục và thay "
     "thế báo giá đã nhập\"\n"
     "- Sau Xác nhận: báo thành công, tab NCC A Hải Phòng 1,5 tấn = 1,900,000, file báo giá là file mới"),

    ("006", "Hủy khi được hỏi thay thế báo giá", "P1",
     "THGVC-1 đã có NCC A",
     "1. Nhập lại file cho NCC A, ở hộp hỏi bấm Hủy",
     "—",
     "- Không thay đổi giá NCC A"),

    ("007", "Chưa chọn nhà cung cấp", "P0",
     PHIEU,
     "1. Mở cửa sổ nhập, chỉ chọn file, bấm Lưu lại",
     "—",
     "- Dưới ô nhà cung cấp báo \"Vui lòng chọn một nhà cung cấp\""),

    ("008", "Chưa chọn file", "P0",
     PHIEU,
     "1. Chọn NCC A, không chọn file, bấm Lưu lại",
     "—",
     "- Báo \"Vui lòng chọn file báo giá bạn muốn tải lên\""),

    ("009", "File không phải Excel", "P1",
     PHIEU,
     "1. Chọn NCC A, chọn file bao-gia.pdf (đổi bộ lọc chọn file sang Tất cả), bấm Lưu lại",
     "File: bao-gia.pdf",
     "- Báo lỗi định dạng file, không nhập"),

    ("010", "Sai thứ tự loại xe", "P1",
     "Mẫu MB-3 có 2 loại xe theo thứ tự Xe tải, Xe container; file NCC để Xe container trước",
     "1. Nhập file này cho phiếu lập từ MB-3",
     "—",
     "- Báo \"Thứ tự các phương tiện không đúng.\"\n"
     "- Cửa sổ Lỗi: dòng 8, \"Thứ tự sai, thứ tự đúng là: Xe tải, Xe container\""),

    ("011", "Sai thứ tự trọng tải", "P1",
     PHIEU,
     "1. Đổi chỗ 2 ô \"1,5 tấn\" và \"5 tấn\" ở dòng 9 file mẫu, nhập file",
     "—",
     "- Báo \"Thứ tự trọng tải của các phương tiện không đúng.\""),

    ("012", "Thiếu một tuyến", "P0",
     PHIEU,
     "1. Xóa dòng K1 đi Bắc Ninh khỏi file, nhập file",
     "—",
     "- Báo \"Định dạng dữ liệu không đúng, vui lòng kiểm tra lại.\"\n"
     "- Cửa sổ Lỗi: \"Tuyến đường không khớp với báo giá cơ bản\", dữ liệu \"K1 đi Bắc Ninh\""),

    ("013", "Tên tuyến không có trong mẫu", "P0",
     PHIEU,
     "1. Đổi tên dòng K1 đi Bắc Ninh thành \"K1 đi Bắc Giang\", nhập file",
     "—",
     "- Báo lỗi; cửa sổ Lỗi có dòng 12 \"Tuyến đường không đúng.\""),

    ("014", "Giá hoặc số km không phải số", "P0",
     PHIEU,
     "1. Điền ô Hải Phòng 5 tấn = \"ba triệu\", ô số km Bắc Ninh = \"40km\", nhập file",
     "—",
     "- Cửa sổ Lỗi có \"Số tiền không đúng định dạng.\" (dòng 11) và \"Số km không đúng định dạng số.\" (dòng 12)\n"
     "- Không nhập dữ liệu nào"),

    ("015", "Ô giá để trống", "P1",
     PHIEU,
     "1. Để trống ô Bắc Ninh 5 tấn, nhập file",
     "—",
     "- Báo \"Số tiền không đúng định dạng.\" ở dòng 12; muốn giá 0 phải gõ 0"),

    ("016", "Giá có số lẻ", "P2",
     PHIEU,
     "1. Điền Hải Phòng 1,5 tấn = 2000000,5, nhập file",
     "—",
     "- Báo \"Số tiền không đúng định dạng.\""),

    ("017", "Tuyến khác thứ tự so với mẫu", "P0",
     PHIEU + "\nFile NCC B để dòng K1 đi Bắc Ninh trước K1 đi Hải Phòng, giá như dữ liệu mẫu",
     "1. Nhập file NCC A (đúng thứ tự) và file NCC B\n"
     "2. Mở Chi tiết, tab Tổng hợp, dòng K1 đi Hải Phòng, trọng tải 1,5 tấn",
     "—",
     "- Mong đợi: cột NCC B = 2,200,000\n"
     "- Lưu ý: theo code hiện tại tab Tổng hợp xếp giá theo vị trí dòng nên cột NCC B hiện 900,000 (giá Bắc "
     "Ninh); giá duyệt mặc định cũng lệch - ghi Failed"),

    ("018", "Lặp một tuyến và thiếu một tuyến", "P1",
     "Mẫu có 3 tuyến Hải Phòng, Bắc Ninh, Hà Nam; file NCC có 3 dòng: Hải Phòng, Bắc Ninh, Bắc Ninh",
     "1. Nhập file",
     "—",
     "- Mong đợi: báo thiếu tuyến Hà Nam và trùng tuyến Bắc Ninh\n"
     "- Lưu ý: theo code hiện tại chỉ so số dòng nên nhập thành công, NCC thiếu giá Hà Nam - ghi Failed"),

    ("019", "Giá cước vượt trội là chữ", "P2",
     PHIEU,
     "1. Điền ô giá cước vượt trội 1,5 tấn = \"mười nghìn\", nhập file",
     "—",
     "- Mong đợi: báo \"Số tiền không đúng định dạng.\" như ô giá tuyến\n"
     "- Lưu ý: theo code hiện tại ô này không được kiểm tra, báo \"File báo giá tải lên không đúng...\" kèm "
     "đoạn lỗi kỹ thuật khó hiểu - ghi Failed"),

    ("020", "Phiếu đã gửi không còn nhập báo giá", "P1",
     "THGVC-2 Chờ duyệt của NV-VC1; NV-VC1 đã mở sẵn cửa sổ nhập trước khi phiếu được gửi ở tab khác",
     "1. Chọn NCC, file, bấm Lưu lại",
     "—",
     "- Báo \"Không có quyền\", không nhập"),
]

SEC_VI = [
    ("001", "Mở màn Sửa", "P0",
     "THGVC-1 Đang tạo đã có NCC A, NCC B",
     "1. NV-VC1 bấm Sửa ở Hành động THGVC-1",
     "—",
     "- Tiêu đề \"Sửa tổng hợp giá vận chuyển đề xuất THGVC-...\"\n"
     "- Khối Chi tiết có tab NCC A, NCC B, mỗi tab có dấu x\n"
     "- Bảng mỗi tab: Tuyến đường, Số km, cột theo Loại xe > Trọng tải, dòng Giá cước vượt trội, nút bút chì "
     "cuối dòng\n"
     "- Nút Lưu, Gửi, Hủy"),

    ("002", "Sửa giá cước vượt trội", "P0",
     "THGVC-1 có NCC A, vượt trội 1,5 tấn = 12,000",
     "1. Ở tab NCC A bấm bút chì dòng Giá cước vượt trội\n"
     "2. Sửa 1,5 tấn = 11000, bấm Lưu lại",
     "Giá: 11000",
     "- Cửa sổ tiêu đề \"Cập nhật giá cước vượt trội, NCC: NCC A\"\n"
     "- Báo \"Cập nhật thành công\", ô hiện 11,000"),

    ("003", "Sửa giá một tuyến", "P0",
     "THGVC-1 có NCC B, Bắc Ninh 5 tấn = 0",
     "1. Ở tab NCC B bấm bút chì dòng K1 đi Bắc Ninh\n"
     "2. Sửa 5 tấn = 1700000, bấm Lưu lại",
     "Giá: 1700000",
     "- Cửa sổ tiêu đề \"K1 đi Bắc Ninh\", hiện ô giá cho từng trọng tải\n"
     "- Báo thành công, ô Bắc Ninh 5 tấn hiện 1,700,000"),

    ("004", "Giá sửa lưu ngay, Hủy không hoàn tác", "P1",
     "THGVC-1 NCC A Hải Phòng 1,5 tấn = 2,000,000",
     "1. Sửa ô này thành 2100000 ở cửa sổ con, bấm Lưu lại\n"
     "2. Bấm Hủy ở cuối màn Sửa, mở lại Chi tiết",
     "—",
     "- Giá vẫn là 2,100,000 (đã lưu khi bấm Lưu lại ở cửa sổ con)"),

    ("005", "Gõ giá có dấu phẩy ngăn cách", "P1",
     "THGVC-1 NCC A Hải Phòng 5 tấn = 3,500,000",
     "1. Bấm bút chì dòng Hải Phòng, gõ 5 tấn = \"3,600,000\", bấm Lưu lại",
     "Giá: 3,600,000",
     "- Mong đợi: lưu 3,600,000 hoặc báo sai định dạng\n"
     "- Lưu ý: theo code hiện tại chỉ lấy phần trước dấu phẩy, lưu giá 3 - ghi Failed"),

    ("006", "Gõ giá âm hoặc số lẻ", "P2",
     "THGVC-1 NCC A",
     "1. Sửa vượt trội 1,5 tấn = -5000, Lưu lại\n"
     "2. Sửa lại = 12000,75, Lưu lại",
     "—",
     "- Mong đợi: chặn giá âm\n"
     "- Lưu ý: theo code hiện tại lưu được -5,000; số lẻ bị cắt còn 12,000 - ghi Failed phần giá âm"),

    ("007", "Để trống giá khi sửa", "P1",
     "THGVC-1 NCC A",
     "1. Xóa trắng ô 1,5 tấn ở cửa sổ sửa tuyến, bấm Lưu lại",
     "—",
     "- Báo \"Bắt buộc phải nhập\", không lưu"),

    ("008", "Bỏ một NCC khỏi phiếu", "P0",
     "THGVC-1 có NCC A, NCC B",
     "1. Bấm x ở tab NCC B, bấm Xác nhận\n"
     "2. Bấm Lưu, mở Chi tiết",
     "—",
     "- Hộp hỏi \"Bạn có chắc chắn muốn xóa báo giá của nhà cung cấp: NCC B\"\n"
     "- Sau Lưu: Chi tiết chỉ còn tab Tổng hợp và NCC A"),

    ("009", "Bỏ NCC nhưng không Lưu", "P1",
     "THGVC-1 có NCC A, NCC B",
     "1. Bấm x tab NCC B, Xác nhận\n"
     "2. Bấm Hủy",
     "—",
     "- NCC B vẫn còn trong phiếu"),

    ("010", "Lưu không gửi", "P0",
     "THGVC-1 có NCC A",
     "1. Sửa Ghi chú thành \"Đợt 2\", bấm Lưu",
     "—",
     "- Báo \"Lưu thành công. Bạn cần gửi để đề xuất được duyệt!\"\n"
     "- Về danh sách, phiếu vẫn Đang tạo, Ghi chú = Đợt 2"),

    ("011", "Gửi duyệt", "P0",
     "THGVC-1 có NCC A, NCC B; DGV-1, DGV-3 có quyền Duyệt giá vận chuyển ở TPE",
     "1. Mở Sửa THGVC-1, bấm Gửi",
     "—",
     "- Báo \"Gửi thành công!\"\n"
     "- Phiếu Chờ duyệt, Ngày gửi = hôm nay\n"
     "- DGV-1, DGV-3 nhận thông báo \"NV-VC1 vừa tạo tổng hợp giá vận chuyển đề xuất: THGVC-...\", bấm vào mở "
     "Chi tiết phiếu"),

    ("012", "Gửi khi chưa có NCC nào", "P0",
     "THGVC-8 Đang tạo, chưa nhập báo giá NCC",
     "1. Mở Sửa THGVC-8, bấm Gửi",
     "—",
     "- Không gửi được, phiếu vẫn Đang tạo\n"
     "- Mong đợi: hiện rõ \"Bắt buộc phải chọn báo giá vận chuyển NCC\"\n"
     "- Lưu ý: theo code hiện tại chỉ báo \"Sửa thất bại!\", câu lý do không hiện ra - ghi Failed phần thông báo"),

    ("013", "Thêm và xóa file đính kèm", "P1",
     "THGVC-1 có file bao-gia-tong.pdf",
     "1. Bấm x ở file bao-gia-tong.pdf, Xác nhận\n"
     "2. Thêm file bien-ban.pdf, bấm Lưu",
     "—",
     "- Hỏi \"Bạn chắc chắn muốn xóa file này?\", báo \"Xóa thành công\", file mất ngay\n"
     "- Sau Lưu: Chi tiết chỉ còn bien-ban.pdf"),

    ("014", "Sửa phiếu không còn Đang tạo qua đường dẫn", "P0",
     "THGVC-2 Chờ duyệt của NV-VC1",
     "1. NV-VC1 dán đường dẫn Sửa THGVC-2",
     "—",
     "- Ra trang không tìm thấy"),

    ("015", "Sửa lại sau khi bị Không duyệt", "P0",
     "THGVC-5 bị Không duyệt, quay về Đang tạo",
     "1. NV-VC1 mở Sửa THGVC-5, sửa giá NCC A, bấm Gửi",
     "—",
     "- Sửa được; phiếu Chờ duyệt lại, Ngày gửi = ngày gửi lại\n"
     "- Người duyệt nhận lại thông báo"),
]

SEC_VII = [
    ("001", "Tab Tổng hợp so sánh giá các NCC", "P0",
     "THGVC-1 Chờ duyệt có NCC A, NCC B.\n" + NCC,
     "1. NV-VC1 mở Chi tiết THGVC-1, tab Tổng hợp",
     "—",
     "- Hàng tiêu đề: Xe tải > 1,5 tấn, 5 tấn; dưới mỗi trọng tải có cột NCC A, NCC B, Duyệt\n"
     "- Giá cước vượt trội 1,5 tấn: 12,000 | 10,000 | -\n"
     "- K1 đi Hải Phòng 1,5 tấn: 2,000,000 | 2,200,000 | -\n"
     "- Cột Duyệt hiện \"-\" khi chưa duyệt"),

    ("002", "Ô giá thấp nhất tô xanh", "P0",
     "Như trên",
     "1. Quan sát màu chữ tab Tổng hợp",
     "—",
     "- Xanh: vượt trội 1,5 tấn NCC B (10,000), 5 tấn NCC A (18,000)\n"
     "- Xanh: Hải Phòng 1,5 tấn NCC A, 5 tấn NCC B; Bắc Ninh 1,5 tấn NCC B, 5 tấn NCC A\n"
     "- Ô Bắc Ninh 5 tấn NCC B = 0 không tô xanh"),

    ("003", "Giá duyệt mặc định là giá thấp nhất khác 0", "P0",
     "THGVC-1 Chờ duyệt như trên; DGV-1 có quyền duyệt",
     "1. DGV-1 mở Chi tiết THGVC-1, xem cột Duyệt",
     "—",
     "- Vượt trội: 10,000 / 18,000\n"
     "- Hải Phòng: 2,000,000 / 3,200,000\n"
     "- Bắc Ninh: 900,000 / 1,800,000\n"
     "- Các ô Duyệt là ô nhập sửa được"),

    ("004", "Mọi NCC đều giá 0", "P2",
     "Ô Bắc Ninh 5 tấn: NCC A = 0, NCC B = 0",
     "1. DGV-1 mở Chi tiết",
     "—",
     "- Ô Duyệt tương ứng = 0, không ô nào tô xanh"),

    ("005", "Tab từng NCC", "P1",
     "THGVC-1 có NCC A đã tải file bao-gia-ncc-a.xlsx",
     "1. Bấm tab NCC A",
     "—",
     "- Link File báo giá bao-gia-ncc-a.xlsx tải được\n"
     "- Bảng giá riêng của NCC A, không có ô sửa"),

    ("006", "Người không có quyền duyệt chỉ xem", "P1",
     "THGVC-1 Chờ duyệt; TP-VC xem theo phòng ban",
     "1. TP-VC mở Chi tiết THGVC-1",
     "—",
     "- Cột Duyệt hiện \"-\", không có ô Ghi chú duyệt, không có nút Duyệt\n"
     "- Chỉ có nút Quay lại"),

    ("007", "Xem phiếu đã duyệt", "P0",
     "THGVC-4 Đã duyệt với ghi chú duyệt \"Chọn giá thấp nhất\"",
     "1. NV-VC1 mở Chi tiết THGVC-4",
     "—",
     "- Cột Duyệt hiện giá đã duyệt\n"
     "- Khối Ghi chú duyệt (khóa) \"Chọn giá thấp nhất\"\n"
     "- Mỗi tab NCC có nút \"Lập hợp đồng\""),
]
