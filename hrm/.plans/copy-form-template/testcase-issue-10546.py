"""Sinh CSV testcase issue #10546 — In mẫu phiếu thu thập thông tin (theo code hiện tại).

Output: .plans/copy-form-template/testcase-issue-10546.csv
Chèn vào tab 'Testcase _ Mẫu phiếu thu thập thông tin' (gid=302734452).
Layout tab này có 22 cột, cột C BỎ TRỐNG:
A Module | B Nhóm chức năng | C (trống) | D TC ID | E Chức năng | F Priority
| G Tiền điều kiện | H Bước thực hiện | I Test Data | J Expected Result (chi tiết)
"""
import csv

OUT = ".plans/copy-form-template/testcase-issue-10546.csv"
NCOL = 22
MODULE = "Mẫu phiếu thu thập thông tin"

BLOCK_TITLE = "UPDATE BỔ SUNG 31/07/2026"
BLOCK_NOTE = "Task http://quanly.dnsmedia.vn/issues/10546 — In mẫu phiếu thu thập thông tin"

# (group, tc_id, chức năng, priority, tiền điều kiện, bước, test data, expected)
TCS = [
    # ------- Nhóm 1: nút In ở màn danh sách -------
    ("In mẫu phiếu - Danh sách", "TC-ROLE-131", "Hiển thị nút In mẫu phiếu trên từng dòng danh sách", "P0",
     "Có ít nhất 3 mẫu phiếu ở 3 trạng thái: Nháp, Hoạt động, Khoá",
     "1. Mở Danh mục → Phiếu thu thập thông tin.\n2. Quan sát cột thao tác của từng dòng.",
     "3 mẫu phiếu 3 trạng thái",
     "- Mỗi dòng có icon máy in với tooltip \"In mẫu phiếu\".\n- Nút hiển thị ở cả 3 trạng thái Nháp / Hoạt động / Khoá (không bị ẩn theo trạng thái)."),

    ("In mẫu phiếu - Danh sách", "TC-ROLE-132", "Mở xem trước bản in từ danh sách", "P0",
     "Có mẫu phiếu \"Khảo sát hạ tầng\" đã thiết lập đủ Section/Group/Câu hỏi",
     "1. Tại dòng mẫu phiếu, bấm icon \"In mẫu phiếu\".\n2. Quan sát màn hình.",
     "Mẫu phiếu: Khảo sát hạ tầng",
     "- Hiện thanh loading rồi mở popup tiêu đề \"Xem trước mẫu phiếu in\".\n- Popup có 2 nút \"In\" và \"Đóng\" + nút X ở góc phải.\n- Phản hồi ngay khi click, không phải chuyển sang trang khác."),

    ("In mẫu phiếu - Danh sách", "TC-ROLE-133", "Thông tin đầu phiếu lấy đúng từ dòng được chọn", "P0",
     "Mẫu phiếu có Tên \"Khảo sát hạ tầng\", Mã \"MP-001\", Ứng dụng \"Quản lý kho\"; user đăng nhập là Nguyễn Văn A",
     "1. Bấm In mẫu phiếu ở dòng tương ứng.\n2. Đọc khối thông tin đầu bản xem trước.",
     "MP-001 / Khảo sát hạ tầng / Quản lý kho / Nguyễn Văn A",
     "Hiển thị đúng: Tên mẫu phiếu = Khảo sát hạ tầng; Mã mẫu phiếu = MP-001; Ứng dụng = Quản lý kho; Ngày in mẫu = ngày hiện tại (dd/mm/yyyy); Người in mẫu = Nguyễn Văn A."),

    ("In mẫu phiếu - Danh sách", "TC-ROLE-134", "Lỗi khi tải dữ liệu mẫu phiếu để in", "P1",
     "Mẫu phiếu vừa bị xoá bởi user khác / mất kết nối API",
     "1. Bấm icon \"In mẫu phiếu\".\n2. Quan sát thông báo.",
     "-",
     "- Hiển thị thông báo lỗi \"Không thể tải mẫu phiếu để in\".\n- Không mở popup xem trước; danh sách giữ nguyên, không trắng màn."),

    # ------- Nhóm 2: nút In ở màn chi tiết -------
    ("In mẫu phiếu - Xem chi tiết", "TC-ROLE-135", "Hiển thị nút In mẫu phiếu ở màn xem chi tiết", "P0",
     "Đang mở màn Xem chi tiết một mẫu phiếu bất kỳ",
     "1. Quan sát thanh nút phía dưới màn hình.",
     "-",
     "Có nút \"In mẫu phiếu\" (icon máy in) đứng cạnh nút \"Sao chép\" và nút Quay lại."),

    ("In mẫu phiếu - Xem chi tiết", "TC-ROLE-136", "Mở xem trước bản in từ màn chi tiết", "P0",
     "Đang xem chi tiết mẫu phiếu đã tải xong dữ liệu",
     "1. Bấm nút \"In mẫu phiếu\".\n2. Quan sát popup.",
     "-",
     "Popup \"Xem trước mẫu phiếu in\" mở ngay lập tức với đầy đủ nội dung mẫu phiếu đang xem (không cần tải lại dữ liệu)."),

    ("In mẫu phiếu - Xem chi tiết", "TC-ROLE-137", "Đóng popup xem trước", "P1",
     "Popup xem trước đang mở",
     "1. Bấm nút \"Đóng\" (hoặc dấu X).\n2. Quan sát màn hình.",
     "-",
     "Popup đóng lại, quay về màn hình trước đó, không thực hiện lệnh in, dữ liệu không thay đổi."),

    # ------- Nhóm 3: nội dung bản xem trước -------
    ("Nội dung bản in", "TC-ROLE-138", "Bố cục chung của bản xem trước", "P0",
     "Mẫu phiếu có đủ Section/Group/Câu hỏi",
     "1. Mở xem trước bản in.\n2. Quan sát từ trên xuống.",
     "-",
     "Theo thứ tự: ảnh header công ty → tiêu đề \"PHIẾU THU THẬP THÔNG TIN DỰ ÁN\" (in hoa, căn giữa) → khối thông tin mẫu phiếu → tiêu đề \"NỘI DUNG KHẢO SÁT\" → bảng nội dung."),

    ("Nội dung bản in", "TC-ROLE-139", "Tiêu đề 4 cột của bảng nội dung khảo sát", "P0",
     "Popup xem trước đang mở",
     "1. Quan sát dòng tiêu đề bảng.",
     "-",
     "Bảng có đúng 4 cột: STT | NỘI DUNG | LOẠI CÂU HỎI | GIÁ TRỊ LỰA CHỌN ĐI KÈM (in hoa, nền xám, có viền)."),

    ("Nội dung bản in", "TC-ROLE-140", "In đầy đủ Section và Group đã thiết lập", "P0",
     "Mẫu phiếu có 2 Section; Section 1 có 2 Group",
     "1. Mở xem trước.\n2. Đối chiếu danh sách Section/Group với cấu hình mẫu phiếu.",
     "Section 1 (Group 1.1, 1.2), Section 2",
     "- Dòng Section đánh số 1, 2 và in đậm, nền xám.\n- Dòng Group đánh số 1.1, 1.2 (theo Section cha), in đậm.\n- Không thiếu Section/Group nào."),

    ("Nội dung bản in", "TC-ROLE-141", "Đánh số câu hỏi chạy liên tục toàn phiếu", "P0",
     "Mẫu phiếu có 3 câu hỏi ở Section 1 và 2 câu hỏi ở Section 2",
     "1. Mở xem trước.\n2. Đọc cột STT của các dòng câu hỏi.",
     "5 câu hỏi / 2 section",
     "Câu hỏi được đánh số 1→5 chạy liên tục toàn phiếu, KHÔNG đánh lại từ 1 ở mỗi Section."),

    ("Nội dung bản in", "TC-ROLE-142", "Câu hỏi con hiển thị đúng số thứ tự và nhãn", "P0",
     "Câu hỏi số 3 có 2 câu hỏi con",
     "1. Mở xem trước.\n2. Quan sát các dòng ngay dưới câu hỏi số 3.",
     "Câu 3 có 2 con",
     "- 2 dòng con có STT là 3.1 và 3.2, nằm ngay dưới câu cha.\n- Cột NỘI DUNG có ghi chú \" - câu hỏi con\" phía sau nội dung."),

    ("Nội dung bản in", "TC-ROLE-143", "Đánh dấu câu hỏi bắt buộc", "P0",
     "Có câu hỏi bật cờ Bắt buộc và câu hỏi không bắt buộc",
     "1. Mở xem trước.\n2. So sánh 2 dòng câu hỏi.",
     "1 câu bắt buộc, 1 câu không",
     "Câu bắt buộc có ký hiệu (*) màu đỏ sau nội dung; câu không bắt buộc không có."),

    ("Nội dung bản in", "TC-ROLE-144", "Câu hỏi có mô tả sinh thêm dòng Ghi chú", "P0",
     "Câu hỏi số 2 có nhập phần mô tả \"Nhập theo đơn vị m2\"",
     "1. Mở xem trước.\n2. Quan sát dòng ngay dưới câu hỏi số 2.",
     "Mô tả: Nhập theo đơn vị m2",
     "- Có thêm 1 dòng in nghiêng chứa nội dung mô tả.\n- Cột STT của dòng này để trống, cột LOẠI CÂU HỎI ghi \"Ghi chú\"."),

    ("Nội dung bản in", "TC-ROLE-145", "Nhãn loại câu hỏi hiển thị bằng tiếng Việt", "P0",
     "Mẫu phiếu có đủ các loại: Text ngắn, Text dài, Số, Dropdown, Radio, Checkbox, Ngày, File, Có/Không, Nhóm câu hỏi",
     "1. Mở xem trước.\n2. Đọc cột LOẠI CÂU HỎI của từng dòng.",
     "10 loại câu hỏi",
     "Hiển thị đúng nhãn: Text ngắn, Text dài, Số, Dropdown, Radio 1 lựa chọn, Checkbox nhiều lựa chọn, Ngày, File, Có / Không, Nhóm câu hỏi (không hiện mã kỹ thuật text/select/radio…)."),

    ("Nội dung bản in", "TC-ROLE-146", "Cột Giá trị lựa chọn đi kèm", "P0",
     "Câu hỏi Dropdown có 3 lựa chọn: Cao, Trung bình, Thấp; và 1 câu hỏi Text ngắn",
     "1. Mở xem trước.\n2. Đọc cột GIÁ TRỊ LỰA CHỌN ĐI KÈM của 2 dòng.",
     "Cao / Trung bình / Thấp",
     "- Câu Dropdown/Radio/Checkbox liệt kê các lựa chọn, ngăn cách bằng dấu \";\" (Cao; Trung bình; Thấp).\n- Câu Text ngắn (và các loại không có lựa chọn) để trống cột này."),

    ("Nội dung bản in", "TC-ROLE-147", "Câu hỏi chưa đặt nội dung", "P2",
     "Mẫu phiếu (Nháp) có 1 câu hỏi chưa nhập nội dung",
     "1. Mở xem trước.\n2. Quan sát dòng câu hỏi đó.",
     "Câu hỏi để trống nội dung",
     "Hiển thị chữ \"Chưa đặt nội dung câu hỏi\" thay vì để trống, vẫn được đánh số bình thường."),

    ("Nội dung bản in", "TC-ROLE-148", "Mẫu phiếu chưa có câu hỏi nào", "P1",
     "Mẫu phiếu mới tạo, chưa thiết lập Section/câu hỏi",
     "1. Bấm In mẫu phiếu.\n2. Quan sát bản xem trước.",
     "Mẫu phiếu rỗng",
     "- Vẫn mở được bản xem trước với header, thông tin mẫu phiếu và bảng chỉ có dòng tiêu đề.\n- Không báo lỗi, không trắng màn."),

    # ------- Nhóm 4: thao tác in -------
    ("Thao tác in", "TC-ROLE-149", "Bấm In mở hộp thoại in của trình duyệt", "P0",
     "Popup xem trước đang mở; trình duyệt cho phép popup",
     "1. Bấm nút \"In\".\n2. Quan sát.",
     "-",
     "- Mở cửa sổ in mới có tiêu đề \"Mẫu phiếu thu thập thông tin\".\n- Hộp thoại in của trình duyệt tự bật lên, không phải bấm Ctrl+P."),

    ("Thao tác in", "TC-ROLE-150", "AC3 - In ra giấy hoặc lưu file PDF", "P0",
     "Đang ở hộp thoại in của trình duyệt",
     "1. Chọn máy in để in giấy.\n2. Lặp lại và chọn đích \"Lưu dưới dạng PDF\" → Lưu.",
     "-",
     "In ra giấy được; lưu PDF được và file PDF mở lên đúng nội dung mẫu phiếu."),

    ("Thao tác in", "TC-ROLE-151", "Định dạng trang in", "P0",
     "Đang xem bản preview trong hộp thoại in",
     "1. Quan sát khổ giấy, lề, phông chữ và đường viền bảng.",
     "Khổ A4",
     "- Khổ A4, lề trên/dưới 20mm, lề trái 25mm, lề phải 15mm.\n- Phông Times New Roman; bảng có viền đầy đủ, không tràn ra ngoài lề."),

    ("Thao tác in", "TC-ROLE-152", "Mẫu phiếu dài in sang nhiều trang", "P1",
     "Mẫu phiếu có trên 40 câu hỏi",
     "1. Bấm In.\n2. Xem preview các trang 2, 3…",
     "40+ câu hỏi",
     "- Nội dung tự ngắt sang trang tiếp theo, không bị cắt mất dòng.\n- Các trang sau giữ đúng lề và viền bảng, không mất cột."),

    ("Thao tác in", "TC-ROLE-153", "Trình duyệt chặn popup khi bấm In", "P1",
     "Trình duyệt đang bật chặn cửa sổ bật lên cho domain hệ thống",
     "1. Bấm nút \"In\".\n2. Quan sát thông báo.",
     "Popup blocked",
     "Hiển thị thông báo lỗi \"Không thể mở cửa sổ in. Vui lòng cho phép popup.\"; không treo màn hình."),

    ("Thao tác in", "TC-ROLE-154", "Nội dung bản in khớp với bản xem trước", "P0",
     "Mẫu phiếu có Section, Group, câu hỏi con, câu hỏi bắt buộc và dòng Ghi chú",
     "1. Chụp/ghi lại nội dung bản xem trước.\n2. Bấm In và đối chiếu với preview của hộp thoại in.",
     "-",
     "Số dòng, số thứ tự, nhãn loại câu hỏi, dấu (*), dòng Ghi chú và danh sách lựa chọn ở bản in trùng khớp 100% với bản xem trước."),

    ("Thao tác in", "TC-ROLE-155", "In lại nhiều lần liên tiếp", "P2",
     "Vừa in xong 1 lần và đã đóng cửa sổ in",
     "1. Bấm \"In\" lần 2.\n2. Đóng popup, mở In mẫu phiếu của mẫu khác rồi bấm In.",
     "2 mẫu phiếu khác nhau",
     "- Lần in thứ 2 hoạt động bình thường.\n- Bản in của mẫu phiếu thứ hai hiển thị đúng dữ liệu của mẫu đó, không lẫn dữ liệu mẫu trước."),
]


def pad(vals):
    return list(vals) + [""] * (NCOL - len(vals))


with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(pad([BLOCK_TITLE, "", "", "", BLOCK_NOTE]))
    last_group = None
    for group, tc_id, func, prio, pre, steps, data, exp in TCS:
        if group != last_group:
            w.writerow(pad(["", "", "", group]))
            last_group = group
            first_of_group = True
        w.writerow(pad([
            MODULE if first_of_group else "",
            group if first_of_group else "",
            "",
            tc_id, func, prio, pre, steps, data, exp,
        ]))
        first_of_group = False

print(f"OK: {OUT} — {len(TCS)} testcase")
