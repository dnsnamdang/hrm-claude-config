# -*- coding: utf-8 -*-
"""Section VI - X — xoa, in/xuat, rang buoc, co lap & dong thoi, luong dau-cuoi."""
from tc_data_role import DATA

SEC_VI = [
    ("001", "Xóa phiếu nháp", "P0",
     "PĐ-1 Đang tạo do TK1 lập",
     "1. TK1 bấm bánh răng PĐ-1 > Xóa\n"
     "2. Bấm \"Xác nhận\"",
     "—",
     "- Hộp \"Xác nhận xóa!\", nội dung \"Bạn chắc chắn muốn xóa bản ghi này?\"\n"
     "- \"Xóa thành công!\", PĐ-1 biến mất; tồn không đổi"),

    ("002", "Bấm Hủy ở hộp xác nhận", "P1",
     "PĐ-1 Đang tạo",
     "1. Bấm Xóa rồi \"Hủy\"",
     "—",
     "- PĐ-1 còn nguyên"),

    ("003", "Xóa phiếu nháp lập từ phiếu kiểm kê", "P2",
     "PĐ-9 Đang tạo lập từ KK-2",
     "1. Xóa PĐ-9, mở lại KK-2",
     "—",
     "- KK-2 vẫn Chờ xử lý, vẫn có nút Tạo phiếu điều chuyển vị trí với đủ dòng thiếu"),
]


SEC_VII = [
    ("001", "In dự kiến trước khi điều chuyển", "P0",
     DATA,
     "1. Chọn K1, Ghi chú \"Dồn hàng\", dòng HH-0091 P1 / L02 > P4, SL 5\n"
     "2. Bấm \"In dự kiến\"",
     "—",
     "- Mở cửa sổ mới có logo, tên, địa chỉ công ty, Ngày lập hôm nay, Người lập, Kho \"K1 - <tên>\", Ghi chú\n"
     "- Bảng: STT, Hàng hóa (tên, Model, Mã hàng), ĐVT, Vị trí xuất, Lô xuất, Vị trí nhập, SL, Ghi chú (trống)\n"
     "- Không tạo phiếu, tồn không đổi"),

    ("002", "In dự kiến khi chưa chọn Vị trí nhập và SL", "P1",
     "Dòng đã có Vị trí xuất, Lô xuất; chưa có Vị trí nhập, SL",
     "1. Bấm \"In dự kiến\"",
     "—",
     "- In được, cột Vị trí nhập và SL để trống (dùng làm phiếu đi lấy hàng)"),

    ("003", "In dự kiến khi thiếu thông tin bắt buộc", "P1",
     "Chưa nhập Ghi chú, dòng chưa chọn Vị trí xuất",
     "1. Bấm \"In dự kiến\"",
     "—",
     "- Thông báo \"Tạo thất bại!\", chữ đỏ \"Bắt buộc phải nhập\" dưới Ghi chú, \"Bắt buộc phải chọn\" ở Vị trí xuất / Lô xuất\n"
     "- Không mở cửa sổ in"),

    ("004", "In phiếu đã chuyển", "P0",
     "PĐ-3 Đã chuyển, lập ngày 12/10/2026 bởi TK1",
     "1. Bấm bánh răng PĐ-3 > In phiếu",
     "—",
     "- Có Số phiếu, Ngày lập 12/10/2026, Người lập TK1, Kho, Ghi chú\n"
     "- Bảng: STT, Hàng hóa, ĐVT, Vị trí xuất, Lô xuất, Vị trí nhập, SL — khớp màn Chi tiết"),

    ("005", "Xuất excel danh sách", "P0",
     "Phạm vi có 23 phiếu",
     "1. Bấm \"Xuất excel\", mở file",
     "—",
     "- File danh_sach_phieu_dieu_chuyen_vi_tri.xlsx\n"
     "- Cột: STT, Mã phiếu, Ngày lập, Kho, Phiếu kiểm kê, Trạng thái, Người lập\n"
     "- Đủ 23 dòng, không theo phân trang"),

    ("006", "Xuất excel theo Mã phiếu và Trạng thái", "P1",
     "Lọc Trạng thái = Đã chuyển ra 9 phiếu",
     "1. Bấm \"Xuất excel\"",
     "—",
     "- File có đúng 9 dòng"),

    ("007", "Xuất excel khi lọc thời gian, hàng hóa, kho", "P0",
     "Lọc kho K1 và khoảng 01/10-05/10/2026, lưới ra 3 phiếu; phạm vi có 23",
     "1. Bấm \"Xuất excel\"",
     "—",
     "- Mong đợi: file có 3 dòng, có dòng \"Từ ngày ... đến ngày ...\"\n"
     "- Lưu ý: code hiện tại không gửi 3 ô này nên file ra 23 dòng — nếu vậy ghi Failed"),
]


SEC_VIII = [
    ("001", "Lưu khi chưa chọn kho, chưa nhập ghi chú, chưa có hàng", "P0",
     "Màn Tạo mới trống",
     "1. Bấm \"Lưu\"",
     "—",
     "- \"Tạo thất bại!\"\n"
     "- Chữ đỏ \"Bắt buộc phải chọn\" dưới Chọn kho, \"Bắt buộc phải nhập\" dưới Ghi chú, lỗi dưới bảng Chi tiết"),

    ("002", "Ghi chú quá 255 ký tự", "P1",
     "Đủ dữ liệu khác",
     "1. Nhập Ghi chú 256 ký tự, bấm Lưu\n"
     "2. Rút còn 255 ký tự, bấm Lưu",
     "Ghi chú: 256 / 255 ký tự",
     "- 256: \"Không được vượt quá 255 ký tự\"\n"
     "- 255: lưu được"),

    ("003", "Điều chuyển khi dòng thiếu Vị trí nhập, Lô xuất hoặc SL", "P0",
     "Dòng HH-0091 có Vị trí xuất P1, chưa có Lô xuất, Vị trí nhập, SL; đã đính kèm file",
     "1. Bấm \"Điều chuyển\"",
     "—",
     "- \"Tạo thất bại!\", lỗi \"Bắt buộc phải chọn\" / \"Bắt buộc phải nhập\" ở từng ô thiếu"),

    ("004", "Điều chuyển khi chưa đính kèm file", "P0",
     "Dòng hợp lệ, chưa có file",
     "1. Bấm \"Điều chuyển\"",
     "—",
     "- \"Tạo thất bại!\", lỗi \"Bắt buộc phải chọn\" ở khối File đính kèm"),

    ("005", "File không phải PDF", "P1",
     "Dòng hợp lệ",
     "1. Ép chọn file anh.png (đổi bộ lọc hộp chọn file sang Tất cả tệp), bấm Điều chuyển",
     "File: anh.png",
     "- Lưu ý: hệ thống vẫn chấp nhận png, jpg, jpeg dù nhãn ghi PDF — ghi nhận\n"
     "- File docx: báo \"Không hợp lệ\""),

    ("006", "SL bằng 0", "P0",
     "Dòng hợp lệ, có file",
     "1. Nhập SL = 0, bấm \"Điều chuyển\"",
     "SL: 0",
     "- Mong đợi: hệ thống chặn SL phải lớn hơn 0\n"
     "- Lưu ý: code hiện tại cho tạo phiếu Đã chuyển với SL 0 — nếu vậy ghi Failed"),

    ("007", "SL âm, chữ, số lẻ", "P1",
     "Dòng hợp lệ, có file",
     "1. Lần lượt nhập SL -2, abc, 2.5 rồi bấm Điều chuyển",
     "SL: -2 / abc / 2.5",
     "- -2 và abc: không lưu được, có lỗi ở ô SL\n"
     "- 2.5: ghi lại kết quả (hàng đếm theo cái không nên cho số lẻ)"),

    ("008", "Lưu nháp rồi tồn giảm, tới lúc Điều chuyển vượt tồn", "P1",
     "PĐ-1 Đang tạo: P1 / L02 > P4 SL 10; sau đó P1 bị xuất còn 5",
     "1. Mở Sửa PĐ-1, quan sát dòng\n"
     "2. Bấm Điều chuyển",
     "—",
     "- Dòng hiện SL tồn mới, tô đỏ, nút Điều chuyển khóa\n"
     "- Nếu vẫn bấm được thì hệ thống báo \"Dữ liệu hàng hóa vượt quá tồn\""),
]


SEC_IX = [
    ("001", "Phiếu ghi nhận công ty của người lập", "P0",
     "TK1 công ty 1 lập PĐ-10; C có quyền xem theo công ty, thuộc công ty 3",
     "1. C tìm PĐ-10",
     "—",
     "- C không thấy PĐ-10"),

    ("002", "Hai người cùng điều chuyển một lô", "P0",
     "P1 lô L02 = 15; TK1 và TK5 cùng mở màn Tạo mới",
     "1. TK1 điều chuyển 10 sang P4\n"
     "2. TK5 (chưa tải lại) điều chuyển 10 sang P5",
     "—",
     "- TK1 thành công; TK5 báo \"Dữ liệu hàng hóa vượt quá tồn: HH-0091\"\n"
     "- Tồn P1 = 5, P4 = 10, P5 = 0 (không âm)"),

    ("003", "Hai tab cùng Điều chuyển một phiếu nháp", "P1",
     "PĐ-1 Đang tạo mở Sửa ở 2 tab",
     "1. Tab 1 bấm Điều chuyển\n"
     "2. Tab 2 bấm Điều chuyển",
     "—",
     "- Tab 2 bị từ chối (phiếu không còn Đang tạo); tồn chỉ đổi 1 lần"),

    ("004", "Tạo 2 phiếu điều chuyển từ cùng một dòng thiếu", "P1",
     "KK-2 thiếu 2 cái ở P1 / L02; XL mở nút Tạo phiếu điều chuyển vị trí 2 lần (2 tab)",
     "1. Tab 1 Điều chuyển 2 cái\n"
     "2. Tab 2 Điều chuyển tiếp",
     "—",
     "- Mong đợi: tab 2 bị chặn vì dòng đã xử lý đủ\n"
     "- Nếu chuyển được thêm 2 cái thì ghi Failed"),

    ("005", "Kho ngoài phạm vi thủ kho không chọn được", "P1",
     "TK1 chỉ là thủ kho K1",
     "1. Mở Tạo mới, mở ô Chọn kho",
     "—",
     "- Không có kho nào ngoài K1"),
]


SEC_X = [
    ("001", "Luồng chuẩn: nháp, in dự kiến, điều chuyển, in phiếu", "P0",
     DATA,
     "1. TK1 tạo phiếu K1, dòng P1 / L02 > P4 SL 5, bấm Lưu\n"
     "2. Mở Sửa, bấm In dự kiến\n"
     "3. Đính kèm bienban.pdf, bấm Điều chuyển\n"
     "4. Mở Chi tiết, In phiếu, Xuất excel danh sách",
     "—",
     "- Phiếu: Đang tạo rồi Đã chuyển\n"
     "- Tồn P1 15 về 10, P4 0 lên 5\n"
     "- Bản in và Excel khớp màn Chi tiết"),

    ("002", "Luồng xử lý hàng thiếu từ kiểm kê theo vị trí", "P0",
     "Kế hoạch KH-11 > phiếu kiểm kê KK-2 đã duyệt, thiếu 2 cái ở P1 / L02 (thực tế hàng nằm ở P4)",
     "1. XL nhận thông báo, mở KK-2, bấm Tạo phiếu điều chuyển vị trí\n"
     "2. Chọn Vị trí nhập P4, đính kèm file, Điều chuyển\n"
     "3. Xem KK-2, KH-11, tồn P1",
     "—",
     "- KK-2 và KH-11 Hoàn thành\n"
     "- Tồn P1 giảm 2 (khớp số thực kiểm)"),

    ("003", "Luồng điều chuyển chia nhiều vị trí theo ĐVT lớn", "P1",
     "P1 lô L02 = 30 cái; Thùng hệ số 12",
     "1. Dòng 1: P1 / L02 > P4, Thùng, SL 1; dòng 2: P1 / L02 > P5, Cái, SL 10\n"
     "2. Điều chuyển",
     "—",
     "- P1 còn 8, P4 có 12, P5 có 10"),
]
