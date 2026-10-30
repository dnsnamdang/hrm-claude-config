# -*- coding: utf-8 -*-
"""Section VIII-XII: duyet & bang gia hieu luc, xuat excel, xoa, co lap & dong thoi, luong dau - cuoi."""
from tc_data_role import MENU, MENU_MAU, MAU, NCC

CHO = ("THGVC-1 Chờ duyệt do NV-VC1 (TPE) lập từ MB-1, có NCC A, NCC B; DGV-1 (TPE) có quyền Duyệt giá "
       "vận chuyển; TPE chưa có bảng giá hiệu lực nào giao với 01/11/2026 - 31/12/2026")

SEC_VIII = [
    ("001", "Duyệt với giá mặc định", "P0",
     CHO,
     "1. DGV-1 mở Chi tiết THGVC-1\n"
     "2. Nhập Ghi chú duyệt \"Chọn giá thấp nhất\", bấm Duyệt",
     "Ghi chú duyệt: Chọn giá thấp nhất",
     "- Báo \"Thao tác thành công!\", về màn cần duyệt, THGVC-1 không còn ở đó\n"
     "- Danh sách chính: THGVC-1 Đã duyệt, Người duyệt DGV-1, Ngày duyệt hôm nay\n"
     "- NV-VC1 nhận thông báo \"DGV-1 vừa duyệt tổng hợp giá vận chuyển đề xuất: THGVC-...\""),

    ("002", "Duyệt tạo Bảng giá hiệu lực mới", "P0",
     CHO,
     "1. DGV-1 Duyệt THGVC-1 với giá mặc định\n"
     "2. Mở menu \"Bảng giá hiệu lực vận chuyển\"",
     "—",
     "- Có bảng giá mới của TPE, hiệu lực 01/11/2026 - 31/12/2026\n"
     "- Xe tải 1,5 tấn / 5 tấn: vượt trội 10,000 / 18,000; Hải Phòng 2,000,000 / 3,200,000; Bắc Ninh 900,000 "
     "/ 1,800,000\n"
     "- Bảng giá có danh sách NCC A, NCC B kèm file báo giá của từng NCC"),

    ("003", "Duyệt với giá đã sửa", "P0",
     CHO,
     "1. DGV-1 sửa ô Duyệt Hải Phòng 5 tấn = 3,000,000\n"
     "2. Nhập Ghi chú duyệt, bấm Duyệt\n"
     "3. Mở Chi tiết THGVC-1 và bảng giá hiệu lực mới",
     "Giá duyệt: 3,000,000",
     "- Chi tiết: cột Duyệt Hải Phòng 5 tấn = 3,000,000\n"
     "- Bảng giá hiệu lực: Hải Phòng 5 tấn = 3,000,000"),

    ("004", "Duyệt khi bỏ trống ô giá duyệt", "P1",
     CHO,
     "1. DGV-1 xóa trắng ô Duyệt Bắc Ninh 1,5 tấn, nhập Ghi chú duyệt, bấm Duyệt",
     "—",
     "- Mong đợi: báo phải nhập giá duyệt\n"
     "- Lưu ý: theo code hiện tại ô trống được coi là 0, duyệt thành công và bảng giá hiệu lực ghi giá 0 - "
     "ghi Failed"),

    ("005", "Bắt buộc Ghi chú duyệt", "P0",
     CHO,
     "1. DGV-1 để trống Ghi chú duyệt, bấm Duyệt",
     "—",
     "- Báo \"Thao tác thất bại!\", dưới ô Ghi chú duyệt báo lỗi bắt buộc\n"
     "- Phiếu vẫn Chờ duyệt"),

    ("006", "Giá duyệt không phải số", "P1",
     CHO,
     "1. Gõ ô Duyệt vượt trội 1,5 tấn = \"abc\", nhập ghi chú, bấm Duyệt",
     "—",
     "- Mong đợi: báo giá duyệt không hợp lệ, không duyệt\n"
     "- Lưu ý: theo code hiện tại chữ được coi là 0, duyệt thành công với giá 0 - ghi Failed"),

    ("007", "Không duyệt", "P0",
     CHO,
     "1. DGV-1 nhập Ghi chú duyệt \"Giá Hải Phòng cao, đàm phán lại\", bấm Không duyệt",
     "—",
     "- Báo thành công; phiếu về Đang tạo\n"
     "- NV-VC1 nhận thông báo \"DGV-1 không duyệt tổng hợp giá vận chuyển đề xuất: THGVC-...\"\n"
     "- Không tạo bảng giá hiệu lực; NV-VC1 thấy lại Sửa, Xóa, Nhập báo giá của NCC"),

    ("008", "Không duyệt cũng bắt buộc ghi chú", "P1",
     CHO,
     "1. Để trống Ghi chú duyệt, bấm Không duyệt",
     "—",
     "- Báo lỗi bắt buộc dưới ô Ghi chú duyệt, phiếu vẫn Chờ duyệt"),

    ("009", "Trùng khoảng ngày với bảng giá hiệu lực có sẵn", "P0",
     CHO + "\nTPE đã có bảng giá hiệu lực BGHL-1 hiệu lực 01/12/2026 - 28/02/2027",
     "1. DGV-1 nhập ghi chú, bấm Duyệt THGVC-1",
     "—",
     "- Báo \"Đã có bảng giá hiệu lực trong khoảng thời gian này (BGHL-1)\"\n"
     "- Phiếu vẫn Chờ duyệt, không tạo bảng giá mới"),

    ("010", "Thông báo sai khi duyệt bị chặn vì trùng bảng giá", "P1",
     "Như TC trên; NV-VC1 đang mở ERP",
     "1. DGV-1 bấm Duyệt, bị chặn vì trùng BGHL-1\n"
     "2. Quan sát màn của NV-VC1",
     "—",
     "- Mong đợi: NV-VC1 không nhận thông báo gì\n"
     "- Lưu ý: theo code hiện tại NV-VC1 vẫn bật thông báo \"vừa duyệt\" dù phiếu vẫn Chờ duyệt - ghi Failed"),

    ("011", "Mẫu đã gắn bảng giá hiệu lực thì cập nhật bảng đó", "P0",
     "Mẫu MB-4 gắn bảng giá hiệu lực BGHL-1; BGHL-1 có Xe tải 1,5 tấn tuyến K1 đi Hải Phòng = 2,500,000, "
     "tuyến K1 đi Hưng Yên = 1,200,000. THGVC-10 lập từ MB-4 (tuyến Hải Phòng, Bắc Ninh), Chờ duyệt",
     "1. DGV-1 Duyệt THGVC-10 với Hải Phòng 1,5 tấn = 2,100,000, Bắc Ninh 1,5 tấn = 950,000\n"
     "2. Mở BGHL-1",
     "—",
     "- Không tạo bảng giá mới\n"
     "- BGHL-1: Hải Phòng 1,5 tấn = 2,100,000 (thay giá cũ), thêm tuyến Bắc Ninh = 950,000\n"
     "- Tuyến Hưng Yên giữ 1,200,000"),

    ("012", "Cập nhật bảng giá có trọng tải mới", "P1",
     "BGHL-1 chỉ có Xe tải 1,5 tấn; THGVC-10 có thêm 5 tấn",
     "1. Duyệt THGVC-10, mở BGHL-1",
     "—",
     "- BGHL-1 có thêm trọng tải 5 tấn với giá duyệt các tuyến của phiếu\n"
     "- Các tuyến cũ của bảng giá chưa có trong phiếu ở trọng tải 5 tấn có giá 0"),

    ("013", "Giá duyệt áp chung cho mọi NCC", "P1",
     CHO,
     "1. Duyệt THGVC-1\n"
     "2. NV-VC1 bấm Lập hợp đồng ở tab NCC A và tab NCC B",
     "—",
     "- Giá hai NCC dùng cho hợp đồng đều là giá ở cột Duyệt"),

    ("014", "Lập hợp đồng từ phiếu đã duyệt", "P1",
     "THGVC-4 Đã duyệt, có NCC A",
     "1. NV-VC1 mở Chi tiết THGVC-4, tab NCC A, bấm \"Lập hợp đồng\"\n"
     "2. Lập xong hợp đồng, quay lại danh sách tổng hợp",
     "—",
     "- Mong đợi: form hợp đồng điền sẵn NCC A và giá duyệt; sau khi lập phiếu sang Đã lập hợp đồng (hoặc Đang "
     "lập hợp đồng nếu còn NCC chưa lập), nút Lập hợp đồng của NCC A ẩn\n"
     "- Lưu ý: theo code hiện tại form hợp đồng trống, phiếu vẫn Đã duyệt và nút vẫn còn - ghi Failed"),

    ("015", "Người duyệt không thấy nút Lập hợp đồng", "P2",
     "THGVC-4 Đã duyệt",
     "1. DGV-1 mở Chi tiết THGVC-4, tab NCC A",
     "—",
     "- Không có nút Lập hợp đồng (chỉ người lập thấy)"),
]

SEC_IX = [
    ("001", "Xuất excel phiếu chờ duyệt", "P0",
     "THGVC-1 Chờ duyệt, có NCC A, NCC B, ghi chú \"Tuyến miền Bắc quý 4\"",
     "1. Ở danh sách mở Hành động THGVC-1, bấm Xuất excel",
     "—",
     "- Tải file \"Tổng hợp giá vận chuyển đề xuất số THGVC-....xlsx\"\n"
     "- Đầu file: tiêu đề công ty, \"Tổng hợp giá vận chuyển đề xuất THGVC-...\", Ghi chú\n"
     "- Bảng giống tab Tổng hợp: cột NCC A, NCC B, Duyệt theo từng trọng tải; cột Duyệt là \"-\""),

    ("002", "Xuất excel phiếu đã duyệt", "P0",
     "THGVC-4 Đã duyệt",
     "1. Xuất excel THGVC-4",
     "—",
     "- Cột Duyệt có đúng giá đã duyệt ở giá cước vượt trội và từng tuyến"),

    ("003", "Xuất excel phiếu chưa có NCC", "P2",
     "THGVC-8 Đang tạo, chưa nhập NCC",
     "1. Xuất excel THGVC-8",
     "—",
     "- Tải được file; bảng chỉ có cột Duyệt (\"-\") theo trọng tải và các tuyến của mẫu"),

    ("004", "Người duyệt không có quyền Quản lý bấm Xuất excel", "P2",
     "DGV-1 chỉ có quyền Duyệt giá vận chuyển",
     "1. Ở màn cần duyệt, mở Hành động THGVC-1, bấm Xuất excel",
     "—",
     "- Ra trang không tìm thấy\n"
     "- Lưu ý: nếu nghiệp vụ muốn người duyệt tải được file so sánh thì ghi Failed"),
]

SEC_X = [
    ("001", "Xóa phiếu Đang tạo", "P0",
     "THGVC-8 Đang tạo của NV-VC1, đã nhập NCC A",
     "1. Mở Hành động THGVC-8, bấm Xóa, xác nhận",
     "—",
     "- Báo \"Xóa thành công!\"\n"
     "- THGVC-8 không còn ở danh sách; lọc Nhà cung cấp = NCC A không ra THGVC-8"),

    ("002", "Hủy xác nhận xóa", "P2",
     "THGVC-8 Đang tạo",
     "1. Bấm Xóa, ở hộp xác nhận bấm Hủy",
     "—",
     "- Phiếu còn nguyên"),

    ("003", "Xóa phiếu đã gửi qua đường dẫn", "P1",
     "THGVC-2 Chờ duyệt của NV-VC1",
     "1. NV-VC1 dán đường dẫn Xóa THGVC-2",
     "—",
     "- Báo \"Không thể xóa!\", phiếu còn nguyên"),

    ("004", "Xóa phiếu không mở lại mẫu báo giá", "P2",
     "MB-5 do NV-VC1 lập, chỉ có 1 phiếu THGVC-11 Đang tạo",
     "1. Xóa THGVC-11\n"
     "2. " + MENU_MAU + ", mở Hành động MB-5",
     "—",
     "- MB-5 vẫn không có Sửa, Xóa\n"
     "- Lưu ý: nếu nghiệp vụ muốn mẫu được mở lại để sửa khi phiếu tổng hợp bị xóa thì ghi Failed"),
]

SEC_XI = [
    ("001", "Người khác mở Chi tiết phiếu Đang tạo", "P0",
     "THGVC-3 Đang tạo của NV-VC2; GD-1 xem theo công ty",
     "1. GD-1 dán đường dẫn Chi tiết THGVC-3",
     "—",
     "- Ra trang không tìm thấy"),

    ("002", "Người lập mở Sửa phiếu của người khác", "P0",
     "THGVC-3 Đang tạo của NV-VC2",
     "1. NV-VC1 dán đường dẫn Sửa THGVC-3",
     "—",
     "- Ra trang không tìm thấy"),

    ("003", "Người duyệt cũ vẫn xem được phiếu bị Không duyệt", "P2",
     "THGVC-5 bị DGV-1 Không duyệt, đang Đang tạo",
     "1. DGV-1 mở thông báo \"không duyệt\" của THGVC-5",
     "—",
     "- Mở được Chi tiết, chỉ xem, không có nút Duyệt"),

    ("004", "Hai người duyệt cùng bấm Duyệt", "P1",
     CHO + "\nDGV-3 cũng có quyền duyệt ở TPE",
     "1. DGV-1 và DGV-3 cùng mở Chi tiết THGVC-1\n"
     "2. Cả hai nhập ghi chú, bấm Duyệt gần như cùng lúc",
     "—",
     "- Mong đợi: 1 người thành công, người kia báo \"Không có quyền!\" hoặc trùng bảng giá; chỉ 1 bảng giá "
     "hiệu lực mới\n"
     "- Lưu ý: nếu có 2 bảng giá hiệu lực trùng ngày thì ghi Failed"),

    ("005", "Duyệt phiếu vừa bị người khác Không duyệt", "P1",
     "DGV-1, DGV-3 cùng mở Chi tiết THGVC-1",
     "1. DGV-3 bấm Không duyệt\n"
     "2. DGV-1 (chưa tải lại) bấm Duyệt",
     "—",
     "- DGV-1 bị báo \"Không có quyền!\", phiếu vẫn Đang tạo"),

    ("006", "Bấm Duyệt 2 lần liên tiếp", "P1",
     CHO,
     "1. DGV-1 bấm Duyệt 2 lần thật nhanh",
     "—",
     "- Nút mờ sau lần bấm đầu; chỉ tạo 1 bảng giá hiệu lực"),

    ("007", "Sửa giá trong lúc phiếu vừa được gửi ở tab khác", "P2",
     "NV-VC1 mở màn Sửa THGVC-1 ở 2 tab",
     "1. Tab 1 bấm Gửi\n"
     "2. Tab 2 bấm bút chì, sửa giá, bấm Lưu lại",
     "—",
     "- Tab 2 báo \"Không có quyền\", giá không đổi"),

    ("008", "Bảng giá hiệu lực ghi công ty của người duyệt", "P2",
     "THGVC-12 Chờ duyệt do NV-TPC (TPC) lập; TGD thuộc TPE có quyền Duyệt giá vận chuyển và quyền xem theo "
     "tổng công ty",
     "1. TGD mở Chi tiết THGVC-12 từ danh sách, Duyệt, mở danh sách bảng giá hiệu lực",
     "—",
     "- Bảng giá mới thuộc TPE (công ty người duyệt), kiểm tra trùng ngày theo bảng giá của TPE\n"
     "- Lưu ý: nếu nghiệp vụ muốn bảng giá thuộc công ty người lập thì ghi Failed"),
]

SEC_XII = [
    ("001", "Luồng đầy đủ: tạo, nhập 2 NCC, gửi, duyệt", "P0",
     MAU + "\n" + NCC,
     "1. NV-VC1 " + MENU_MAU + ", bấm Tổng hợp giá đề xuất ở MB-1, Lưu\n"
     "2. " + MENU + ", Nhập báo giá của NCC cho NCC A rồi NCC B\n"
     "3. Mở Sửa, bấm Gửi\n"
     "4. DGV-1 mở thông báo, nhập ghi chú, bấm Duyệt\n"
     "5. Mở Bảng giá hiệu lực vận chuyển",
     "—",
     "- Bước 1: phiếu Đang tạo\n"
     "- Bước 3: phiếu Chờ duyệt, DGV-1 nhận thông báo\n"
     "- Bước 4: phiếu Đã duyệt, NV-VC1 nhận thông báo\n"
     "- Bước 5: bảng giá mới với giá thấp nhất khác 0 như mục 6 phần mô tả"),

    ("002", "Luồng bị trả về rồi duyệt lại", "P0",
     CHO,
     "1. DGV-1 Không duyệt với ghi chú \"Đàm phán lại Hải Phòng\"\n"
     "2. NV-VC1 nhập lại file NCC B với Hải Phòng 1,5 tấn = 1.950.000, mở Sửa, Gửi\n"
     "3. DGV-1 mở Chi tiết, Duyệt",
     "—",
     "- Bước 3: ô Duyệt Hải Phòng 1,5 tấn mặc định 1,950,000 (NCC B thấp nhất, tô xanh)\n"
     "- Duyệt xong, bảng giá hiệu lực có Hải Phòng 1,5 tấn = 1,950,000"),

    ("003", "Luồng có bỏ bớt NCC trước khi gửi", "P1",
     "THGVC-1 Đang tạo có NCC A, NCC B",
     "1. Mở Sửa, bỏ NCC A, bấm Gửi\n"
     "2. DGV-1 Duyệt, mở bảng giá hiệu lực",
     "—",
     "- Tab Tổng hợp chỉ còn cột NCC B, Duyệt\n"
     "- Bảng giá hiệu lực dùng giá NCC B; danh sách NCC của bảng giá chỉ có NCC B"),

    ("004", "Đối chiếu Xuất excel với màn Chi tiết sau duyệt", "P1",
     "THGVC-1 vừa Đã duyệt",
     "1. Mở Chi tiết tab Tổng hợp\n"
     "2. Xuất excel, so từng ô",
     "—",
     "- Mọi ô giá NCC và cột Duyệt trong file khớp tab Tổng hợp"),
]
