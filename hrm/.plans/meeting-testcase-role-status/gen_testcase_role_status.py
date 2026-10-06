"""Testcase: hành động của Người tạo / Người chủ trì theo từng trạng thái meeting.

Đích: Google Sheet "Testcase _Quản lý dự án", tab "11.Meeting" (gid 1614285068), nối tiếp cuối tab.
Khuôn khối UPDATE của tab: dòng tiêu đề nền xanh (A:E ghép + G:H ghép), cột B = nhóm (ghép dọc),
D = TC ID, E chức năng, F priority, G tiền điều kiện, H bước, I test data, J expected, L check lần 1,
O ghi chú, P..T cột bên TPE (nền vàng nhạt).
Sinh ra meeting-role-status.html để dán vào Sheets (giữ ô ghép, màu, xuống dòng).
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TITLE_A = "UPDATE TESTCASE (24/09/2026)"
TITLE_G = "Phân quyền thao tác của Người tạo / Người chủ trì theo trạng thái meeting"

SETUP = ("Bộ tài khoản dùng chung:\n"
         "- A: người tạo meeting (không phải chủ trì)\n"
         "- B: người chủ trì (không phải người tạo)\n"
         "- D: thành viên nội bộ (Phía Công ty)\n"
         "- E: có quyền 'Xem danh sách meeting theo công ty', không tham gia meeting")

# (nhóm, chức năng, priority, tiền điều kiện, bước, test data, expected, ghi chú)
G1, G2, G3, G4, G5, G6, G7, G8, G9 = (
    "Trạng thái Lưu nháp", "Trạng thái Lên lịch hẹn", "Trạng thái Đã chốt lịch",
    "Trạng thái Đã hoàn thành", "Trạng thái Huỷ", "Nút thao tác ở màn danh sách",
    "Người tạo đồng thời là chủ trì / Đổi chủ trì", "Chặn thao tác vượt quyền", "Các lối vào khác")

TCS = [
    # ---------------- Lưu nháp ----------------
    (G1, "Người tạo xem chi tiết meeting Lưu nháp", "P0",
     SETUP + "\nMeeting MT-01 do A tạo, chủ trì là B, có D trong thành phần tham gia, trạng thái Lưu nháp.",
     "1. Đăng nhập A.\n2. Vào danh sách Meeting, bấm Xem MT-01.\n3. Quan sát các nút cuối màn hình.",
     "Tài khoản: A\nTrạng thái: Lưu nháp",
     "- Ô Trạng thái meeting hiển thị 'Lưu nháp'.\n- Có đủ nút: Sửa, Xóa, In, Tạo phiếu công tác khác, Quay lại.", ""),
    (G1, "Người chủ trì xem chi tiết meeting Lưu nháp", "P0",
     "Như trên, MT-01 trạng thái Lưu nháp.",
     "1. Đăng nhập B.\n2. Mở chi tiết MT-01.\n3. Quan sát các nút cuối màn hình.",
     "Tài khoản: B",
     "- Có nút: Sửa, In, Tạo phiếu công tác khác, Quay lại.\n- KHÔNG có nút Xóa (chỉ người tạo mới được xoá).", ""),
    (G1, "Thành viên / người chỉ có quyền xem không thấy meeting Lưu nháp", "P0",
     "Như trên, MT-01 trạng thái Lưu nháp.",
     "1. Đăng nhập D, vào danh sách Meeting, tìm MT-01.\n2. Đăng nhập E, làm tương tự.",
     "Tài khoản: D, E",
     "- D và E đều KHÔNG thấy MT-01 trong danh sách.\n- Meeting Lưu nháp chỉ người tạo và người chủ trì nhìn thấy.",
     "Hiện tại mở thẳng đường dẫn chi tiết thì thành viên vẫn xem được bản nháp - cần chốt có chặn hay không."),
    (G1, "Người tạo mở màn Sửa meeting Lưu nháp", "P1",
     "MT-01 trạng thái Lưu nháp.",
     "1. Đăng nhập A.\n2. Mở Sửa MT-01.\n3. Quan sát các nút cuối màn hình.",
     "Tài khoản: A",
     "- Có nút: Lưu nháp, Lưu và Lên lịch, Lưu và Chốt lịch, Quay lại.", ""),
    (G1, "Người chủ trì sửa và đưa meeting Lưu nháp sang Lên lịch", "P0",
     "MT-01 trạng thái Lưu nháp, giờ bắt đầu ở tương lai.",
     "1. Đăng nhập B, mở Sửa MT-01.\n2. Sửa Nội dung cuộc họp.\n3. Bấm Lưu và Lên lịch.",
     "Tài khoản: B\nNội dung: 'Chủ trì cập nhật'",
     "- Có nút: Lưu nháp, Lưu và Lên lịch, Lưu và Chốt lịch, Quay lại (giống người tạo).\n"
     "- Lưu thành công, quay về danh sách.\n- MT-01 chuyển trạng thái 'Lên lịch hẹn', nội dung đã cập nhật.", ""),
    (G1, "Người tạo xoá meeting Lưu nháp", "P0",
     "Meeting MT-02 do A tạo, trạng thái Lưu nháp.",
     "1. Đăng nhập A, mở chi tiết MT-02.\n2. Bấm Xóa, xác nhận.",
     "Tài khoản: A",
     "- Hiện hộp xác nhận xoá.\n- Sau khi xác nhận: thông báo 'Xóa thành công', MT-02 biến mất khỏi danh sách.", ""),

    # ---------------- Lên lịch hẹn ----------------
    (G2, "Người tạo xem chi tiết meeting Lên lịch hẹn (chưa tới giờ họp)", "P0",
     "MT-01 trạng thái Lên lịch hẹn, giờ bắt đầu là ngày mai 09:00.",
     "1. Đăng nhập A, mở chi tiết MT-01.\n2. Quan sát các nút.",
     "Tài khoản: A",
     "- Có nút: Sửa, Hủy, In, Tạo phiếu công tác khác, Quay lại.\n- KHÔNG có nút Xóa (chỉ xoá được khi Lưu nháp).", ""),
    (G2, "Người chủ trì xem chi tiết meeting Lên lịch hẹn", "P0",
     "Như trên.",
     "1. Đăng nhập B, mở chi tiết MT-01.\n2. Quan sát các nút.",
     "Tài khoản: B",
     "- Có nút: Sửa, In, Tạo phiếu công tác khác, Quay lại.\n- KHÔNG có nút Hủy và Xóa.", ""),
    (G2, "Thành viên nội bộ xem meeting Lên lịch hẹn", "P0",
     "Như trên, D chưa xác nhận tham dự.",
     "1. Đăng nhập D, mở chi tiết MT-01.\n2. Quan sát các nút.",
     "Tài khoản: D",
     "- Có nút: In, Tạo phiếu công tác khác, Quay lại.\n- Có cụm xác nhận tham dự: 'Có mặt', 'Vắng có lý do'.\n"
     "- KHÔNG có Sửa, Hủy, Xóa.", ""),
    (G2, "Người chỉ có quyền xem mở meeting Lên lịch hẹn", "P1",
     "Như trên.",
     "1. Đăng nhập E, mở chi tiết MT-01.\n2. Quan sát các nút.",
     "Tài khoản: E",
     "- Chỉ có: In, Tạo phiếu công tác khác, Quay lại.\n- KHÔNG có cụm 'Có mặt' / 'Vắng có lý do' (E không phải thành viên).", ""),
    (G2, "Người tạo mở màn Sửa meeting Lên lịch hẹn", "P1",
     "Như trên.",
     "1. Đăng nhập A, mở Sửa MT-01.\n2. Quan sát các nút.",
     "Tài khoản: A",
     "- Có nút: Lưu, Lưu và Lên lịch, Lưu và Chốt lịch, Hủy, Quay lại.", ""),
    (G2, "Người chủ trì chốt lịch meeting", "P0",
     "Như trên.",
     "1. Đăng nhập B, mở Sửa MT-01.\n2. Quan sát các nút.\n3. Bấm Lưu và Chốt lịch.",
     "Tài khoản: B",
     "- Có nút: Lưu, Lưu và Lên lịch, Lưu và Chốt lịch, Quay lại - KHÔNG có Hủy.\n"
     "- Lưu thành công, MT-01 chuyển trạng thái 'Đã chốt lịch'.", ""),
    (G2, "Người tạo huỷ meeting trước giờ họp", "P0",
     "Meeting MT-03 do A tạo, chủ trì B, trạng thái Lên lịch hẹn, giờ bắt đầu ngày mai.",
     "1. Đăng nhập A, mở chi tiết MT-03.\n2. Bấm Hủy.\n3. Chọn Lý do hủy cuộc họp, nhập Ghi chú.\n4. Bấm Xác nhận hủy.",
     "Lý do: một lý do đang hoạt động\nGhi chú: 'Khách dời lịch'",
     "- Hiện popup 'Xác nhận hủy cuộc họp'.\n- Sau khi xác nhận: thông báo 'Cập nhật thành công'.\n"
     "- MT-03 chuyển trạng thái 'Huỷ'.", ""),
    (G2, "Người tạo không huỷ được khi đã tới giờ họp", "P1",
     "Meeting MT-04 do A tạo, trạng thái Lên lịch hẹn, giờ bắt đầu đã qua 30 phút.",
     "1. Đăng nhập A, mở chi tiết MT-04.\n2. Quan sát nút Hủy, rê chuột lên nút.",
     "Tài khoản: A",
     "- Không huỷ được meeting.\n- Lý do hiển thị: 'Cuộc họp đã đến giờ bắt đầu, không hủy được nữa'.",
     "Hiện nút Hủy vẫn hiện nhưng bị làm mờ. Theo quy ước chung, nút không dùng được phải ẩn hẳn - cần chốt."),

    # ---------------- Đã chốt lịch ----------------
    (G3, "Người tạo xem chi tiết meeting Đã chốt lịch", "P0",
     "MT-01 trạng thái Đã chốt lịch, giờ bắt đầu ngày mai.",
     "1. Đăng nhập A, mở chi tiết MT-01.\n2. Quan sát các nút.",
     "Tài khoản: A",
     "- Có nút: Sửa, Hủy, In, Tạo phiếu công tác khác, Quay lại.", ""),
    (G3, "Người tạo mở Sửa khi chưa tới giờ họp", "P1",
     "Như trên.",
     "1. Đăng nhập A, mở Sửa MT-01.\n2. Quan sát nút Hoàn thành, rê chuột lên nút.",
     "Tài khoản: A",
     "- Có nút: Lưu, Hoàn thành, Hủy, Quay lại.\n"
     "- Chưa bấm được Hoàn thành, lý do: 'Chỉ được xác nhận hoàn thành khi cuộc họp đã bắt đầu'.", ""),
    (G3, "Người tạo hoàn thành meeting sau giờ họp", "P0",
     "MT-01 trạng thái Đã chốt lịch, giờ bắt đầu đã qua; đã điểm danh đủ thành viên.",
     "1. Đăng nhập A, mở Sửa MT-01.\n2. Vào tab Biên bản, nhập biên bản và Kết luận.\n3. Bấm Hoàn thành.",
     "Tài khoản: A",
     "- Nút Hủy không dùng được nữa (đã tới giờ họp).\n- Hoàn thành thành công, MT-01 chuyển 'Đã hoàn thành'.", ""),
    (G3, "Người chủ trì hoàn thành meeting sau giờ họp", "P0",
     "Meeting MT-05 do A tạo, chủ trì B, trạng thái Đã chốt lịch, giờ bắt đầu đã qua.",
     "1. Đăng nhập B, mở Sửa MT-05.\n2. Quan sát các nút.\n3. Điểm danh đủ thành viên, nhập biên bản + Kết luận.\n4. Bấm Hoàn thành.",
     "Tài khoản: B",
     "- Có nút: Lưu, Hoàn thành, Quay lại - KHÔNG có Hủy.\n- Hoàn thành thành công, MT-05 chuyển 'Đã hoàn thành'.",
     "Cần chốt nghiệp vụ: hiện hệ thống cho chủ trì bấm Hoàn thành; ghi chú trong thiết kế lại nói chỉ người tạo được Hoàn thành."),
    (G3, "Chủ trì đổi giờ họp của meeting đã chốt lịch", "P2",
     "MT-01 trạng thái Đã chốt lịch, giờ bắt đầu ngày mai.",
     "1. Đăng nhập B, mở Sửa MT-01.\n2. Đổi Thời gian bắt đầu sang 1 giờ sau.\n3. Bấm Lưu.",
     "Thời gian: lùi 1 giờ",
     "- Hiện popup 'Xác nhận thay đổi thời gian' với nút 'Xác nhận gửi lịch'.\n- Xác nhận xong, giờ mới được lưu.", ""),
    (G3, "Thành viên không còn xác nhận tham dự sau giờ họp", "P1",
     "MT-05 trạng thái Đã chốt lịch, giờ bắt đầu đã qua.",
     "1. Đăng nhập D, mở chi tiết MT-05.\n2. Quan sát.",
     "Tài khoản: D",
     "- Không còn nút 'Có mặt' / 'Vắng có lý do' (điểm danh lúc này thuộc về người chủ trì).\n"
     "- Chỉ có: In, Tạo phiếu công tác khác, Quay lại.", ""),
    (G3, "Chặn Hoàn thành khi chưa điểm danh đủ", "P1",
     "MT-05 giờ bắt đầu đã qua, còn 1 thành viên chưa điểm danh, đã có biên bản.",
     "1. Đăng nhập B (hoặc A), mở Sửa MT-05.\n2. Bấm Hoàn thành.",
     "1 thành viên chưa điểm danh",
     "- Báo 'Vui lòng hoàn thành điểm danh cho tất cả thành viên trước khi chốt biên bản và hoàn thành cuộc họp.'\n"
     "- Meeting giữ nguyên 'Đã chốt lịch'.", ""),
    (G3, "Chặn Hoàn thành khi chưa có biên bản", "P1",
     "MT-05 giờ bắt đầu đã qua, đã điểm danh đủ, tab Biên bản trống.",
     "1. Mở Sửa MT-05.\n2. Bấm Hoàn thành.",
     "Biên bản: trống",
     "- Báo 'Vui lòng thêm biên bản cuộc họp trước khi hoàn thành!'\n- Meeting giữ nguyên trạng thái.", ""),

    # ---------------- Đã hoàn thành ----------------
    (G4, "Mọi vai trò xem meeting Đã hoàn thành", "P0",
     "MT-01 trạng thái Đã hoàn thành.",
     "1. Lần lượt đăng nhập A, B, D, E.\n2. Mở chi tiết MT-01, quan sát các nút.",
     "Tài khoản: A, B, D, E",
     "- Cả 4 tài khoản chỉ có: In, Quay lại.\n- KHÔNG ai có Sửa, Hủy, Xóa, Tạo phiếu công tác khác.", ""),
    (G4, "Người tạo mở thẳng đường dẫn Sửa meeting Đã hoàn thành", "P1",
     "MT-01 trạng thái Đã hoàn thành.",
     "1. Đăng nhập A.\n2. Dán đường dẫn màn Sửa của MT-01 lên trình duyệt.",
     "Tài khoản: A",
     "- Màn Sửa chỉ còn nút Quay lại, không lưu hay đổi trạng thái được.", ""),

    # ---------------- Huỷ ----------------
    (G5, "Mọi vai trò xem meeting đã bị huỷ tay", "P0",
     "MT-03 đã bị A huỷ với lý do + ghi chú.",
     "1. Lần lượt đăng nhập A, B, D.\n2. Mở chi tiết MT-03.",
     "Tài khoản: A, B, D",
     "- Trạng thái 'Huỷ'; có khung Lý do hủy hiển thị đúng lý do và ghi chú.\n"
     "- Chỉ có: In, Quay lại. Không ai sửa hay huỷ lại được.", ""),
    (G5, "Meeting bị hệ thống tự huỷ do quá hạn biên bản", "P1",
     "MT-06 (A tạo, B chủ trì) trạng thái Đã chốt lịch, đã qua hạn nhập biên bản mà chưa Hoàn thành; hệ thống đã tự huỷ.",
     "1. Đăng nhập A, mở chi tiết MT-06.\n2. Đăng nhập B, mở chi tiết MT-06.",
     "Tài khoản: A, B",
     "- Trạng thái 'Huỷ', lý do 'Tự động hủy: quá hạn nhập biên bản cuộc họp.'\n"
     "- A và B đều chỉ có: In, Quay lại; không nhập được biên bản nữa.", ""),

    # ---------------- Danh sách ----------------
    (G6, "Nút trên dòng meeting Lưu nháp - người tạo", "P0",
     "MT-02 do A tạo, trạng thái Lưu nháp.",
     "1. Đăng nhập A, vào danh sách Meeting.\n2. Quan sát cột thao tác của dòng MT-02.",
     "Tài khoản: A",
     "- Có: Xem, Sửa, In biên bản, Tạo phiếu công tác khác, Lịch sử, Xoá.", ""),
    (G6, "Nút trên dòng meeting Lưu nháp - người chủ trì", "P0",
     "MT-02 do A tạo, chủ trì B, trạng thái Lưu nháp.",
     "1. Đăng nhập B, vào danh sách Meeting.\n2. Quan sát dòng MT-02.",
     "Tài khoản: B",
     "- Có: Xem, Sửa, In biên bản, Tạo phiếu công tác khác, Lịch sử.\n- KHÔNG có Xoá.", ""),
    (G6, "Nút trên dòng meeting Lên lịch hẹn - thành viên / người chỉ có quyền xem", "P0",
     "MT-01 trạng thái Lên lịch hẹn.",
     "1. Đăng nhập D, quan sát dòng MT-01.\n2. Đăng nhập E, quan sát dòng MT-01.",
     "Tài khoản: D, E",
     "- Có: Xem, In biên bản, Tạo phiếu công tác khác, Lịch sử.\n- KHÔNG có Sửa, Xoá.", ""),
    (G6, "Nút ở danh sách khớp với nút ở màn chi tiết", "P1",
     "Có meeting ở đủ 5 trạng thái.",
     "1. Với từng tài khoản A, B, D: so bộ nút trên dòng ở danh sách với bộ nút ở màn chi tiết của cùng meeting.",
     "5 trạng thái x 3 tài khoản",
     "- Nút nào bị ẩn ở danh sách thì cũng ẩn ở màn chi tiết và ngược lại (Sửa, Xóa).\n"
     "- Không có trường hợp danh sách ẩn Sửa mà màn chi tiết vẫn hiện Sửa.", ""),

    # ---------------- Người tạo kiêm chủ trì / đổi chủ trì ----------------
    (G7, "Người tạo tự làm chủ trì có đủ quyền của người tạo", "P0",
     "Tài khoản C tạo meeting MT-07 và chọn chính mình là Người chủ trì.",
     "1. Đăng nhập C.\n2. Đưa MT-07 lần lượt qua Lưu nháp, Lên lịch hẹn, Đã chốt lịch; mỗi trạng thái mở chi tiết + Sửa, quan sát nút.",
     "Tài khoản: C",
     "- Lưu nháp: có Xóa.\n- Lên lịch hẹn / Đã chốt lịch (trước giờ họp): có Hủy.\n"
     "- Đã chốt lịch (sau giờ họp): có Hoàn thành.\n- Bộ nút giống hệt người tạo ở các case trên.", ""),
    (G7, "Đổi người chủ trì thì quyền sửa chuyển theo", "P1",
     "MT-01 trạng thái Lên lịch hẹn, chủ trì B. Tài khoản B2 là nhân viên khác.",
     "1. Đăng nhập A, mở Sửa MT-01, đổi Người chủ trì từ B sang B2, bấm Lưu.\n"
     "2. Đăng nhập B, mở chi tiết MT-01.\n3. Đăng nhập B2, mở chi tiết MT-01.",
     "Chủ trì mới: B2",
     "- B2 được tự thêm vào Thành phần Phía Công ty.\n- B2 có nút Sửa.\n"
     "- B không còn nút Sửa (chỉ còn quyền như thành viên nếu vẫn có tên trong thành phần tham gia).", ""),
    (G7, "Bắt buộc chọn Người chủ trì", "P1",
     "Đang ở màn Tạo mới meeting.",
     "1. Nhập đủ thông tin nhưng để trống Người chủ trì.\n2. Bấm Lưu và Lên lịch.",
     "Người chủ trì: trống",
     "- Báo lỗi đỏ dưới ô Người chủ trì: 'Vui lòng chọn Người chủ trì.'\n- Không lưu.", ""),

    # ---------------- Chặn vượt quyền ----------------
    (G8, "Thành viên mở thẳng đường dẫn Sửa", "P0",
     "MT-01 trạng thái Lên lịch hẹn, D là thành viên (không phải người tạo / chủ trì).",
     "1. Đăng nhập D.\n2. Dán đường dẫn màn Sửa của MT-01 lên trình duyệt.",
     "Tài khoản: D",
     "- Hệ thống tự chuyển sang màn Chi tiết, không sửa được.", ""),
    (G8, "Chủ trì gọi thẳng chức năng Hủy (bỏ qua giao diện)", "P1",
     "MT-01 trạng thái Lên lịch hẹn, chưa tới giờ họp.",
     "1. Đăng nhập B.\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Hủy meeting MT-01.",
     "Tài khoản: B",
     "- Hệ thống từ chối: 'Bạn không có quyền thực hiện chức năng này'\n- MT-01 giữ nguyên trạng thái.",
     "Dành cho tester kỹ thuật."),
    (G8, "Chủ trì gọi thẳng chức năng Xoá (bỏ qua giao diện)", "P1",
     "MT-02 trạng thái Lưu nháp, chủ trì B.",
     "1. Đăng nhập B.\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xoá MT-02.",
     "Tài khoản: B",
     "- Hệ thống từ chối: 'Bạn không có quyền thực hiện chức năng này'\n- MT-02 vẫn còn.",
     "Dành cho tester kỹ thuật."),
    (G8, "Thành viên gọi thẳng chức năng Sửa (bỏ qua giao diện)", "P1",
     "MT-01 trạng thái Lên lịch hẹn.",
     "1. Đăng nhập D.\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa MT-01.",
     "Tài khoản: D",
     "- Hệ thống từ chối: 'Bạn không có quyền thực hiện chức năng này'\n- Dữ liệu MT-01 không đổi.",
     "Dành cho tester kỹ thuật."),
    (G8, "Chủ trì gọi thẳng chức năng Sửa để đổi sang Huỷ", "P1",
     "MT-01 trạng thái Lên lịch hẹn, chủ trì B.",
     "1. Đăng nhập B.\n2. Dùng công cụ kiểm thử API gọi chức năng Sửa, gửi trạng thái Huỷ.",
     "Tài khoản: B",
     "- Hệ thống từ chối, MT-01 giữ nguyên 'Lên lịch hẹn' (chủ trì không có quyền huỷ).",
     "Dành cho tester kỹ thuật. Rà code thấy chức năng Sửa chưa chặn đổi trạng thái sang Huỷ - dễ Failed."),

    # ---------------- Phạm vi xem ----------------
    ("Phạm vi xem theo quyền", "Quyền xem theo công ty", "P0",
     "Tài khoản chỉ có quyền 'Xem danh sách meeting theo công ty', đang chọn công ty Tân Phát.\nMT-14 do nhân viên Tân Phát tạo; MT-15 do nhân viên công ty khác tạo.",
     "1. Mở Meetings > Lịch Meeting.\n2. Quan sát danh sách và bộ lọc nâng cao.",
     "Quyền: theo công ty",
     "- Thấy MT-14, không thấy MT-15 (trừ khi mình tạo/chủ trì/tham gia MT-15).\n- Bộ lọc nâng cao không có ô Công ty; có ô Phòng ban, Bộ phận.\n- MT-14 chỉ xem, không có Sửa nếu mình không phải người tạo/chủ trì.", ""),
    ("Phạm vi xem theo quyền", "Quyền xem theo bộ phận", "P1",
     "Tài khoản chỉ có quyền 'Xem danh sách meeting theo bộ phận', quản lý bộ phận X.\nMT-16 do nhân viên bộ phận X tạo; MT-17 do nhân viên bộ phận Y tạo.",
     "1. Mở Meetings > Lịch Meeting.\n2. Quan sát danh sách.",
     "Quyền: theo bộ phận",
     "- Thấy MT-16, không thấy MT-17 (trừ meeting mình tạo/chủ trì/tham gia).\n- Bộ lọc chỉ còn ô Bộ phận.", ""),
    ("Phạm vi xem theo quyền", "Có nhiều quyền xem thì lấy phạm vi rộng nhất", "P1",
     "Tài khoản có cả quyền theo bộ phận và theo công ty.",
     "1. Mở Meetings > Lịch Meeting.\n2. So danh sách với tài khoản chỉ có quyền theo công ty.",
     "Quyền: bộ phận + công ty",
     "- Danh sách giống hệt tài khoản chỉ có quyền theo công ty (lấy phạm vi rộng nhất).", ""),
    ("Phạm vi xem theo quyền", "Phạm vi tính theo phòng ban của người tạo lúc tạo meeting", "P2",
     "MT-12 do nhân viên N tạo khi N thuộc phòng Kinh doanh 1; sau đó N chuyển sang phòng Kinh doanh 2.\nTài khoản Q có quyền xem theo phòng ban, quản lý phòng Kinh doanh 1.",
     "1. Đăng nhập Q, mở danh sách Meeting.",
     "—",
     "- Q vẫn thấy MT-12 (meeting giữ phòng ban tại lúc tạo, không đổi theo người tạo).", ""),
    ("Phạm vi xem theo quyền", "Xuất Excel theo đúng phạm vi", "P1",
     "Tài khoản E không có quyền xem nào, liên quan 3 meeting.",
     "1. Mở danh sách Meeting.\n2. Bấm Xuất Excel.",
     "Tài khoản: E",
     "- Nút Xuất Excel có sẵn (không cần quyền riêng).\n- File chỉ có đúng 3 meeting như trên màn hình.", ""),

    # ---------------- Điểm danh ----------------
    ("Điểm danh", "Người tạo và chủ trì điểm danh khi Đã chốt lịch", "P0",
     "MT-05 trạng thái Đã chốt lịch, có 3 thành viên nội bộ.",
     "1. Lần lượt đăng nhập A (người tạo) và B (chủ trì).\n2. Mở Sửa MT-05 > tab Điểm danh.\n3. Chọn trạng thái cho từng người, bấm Lưu.",
     "Có mặt / Vắng có lý do / Vắng không lý do",
     "- Mỗi người có 3 lựa chọn Có mặt / Vắng có lý do / Vắng không lý do và ô Ghi chú / Lý do.\n- Có nút 'Điểm danh nhanh: Tất cả có mặt'.\n- Lưu thành công, mở lại vẫn đúng kết quả.", ""),
    ("Điểm danh", "Chưa điểm danh được khi meeting còn Lưu nháp / Lên lịch hẹn", "P1",
     "MT-01 trạng thái Lên lịch hẹn.",
     "1. Đăng nhập B, mở Sửa MT-01 > tab Điểm danh.",
     "Trạng thái: Lên lịch hẹn",
     "- Tab chỉ hiển thị kết quả (nhãn Chưa điểm danh / Có mặt...), không chọn được.\n- Muốn điểm danh phải Chốt lịch trước.", ""),
    ("Điểm danh", "Thành viên và người chỉ có quyền xem không điểm danh cho người khác", "P0",
     "MT-05 trạng thái Đã chốt lịch.",
     "1. Đăng nhập D (thành viên), mở chi tiết MT-05 > tab Điểm danh.\n2. Đăng nhập E (quyền xem theo công ty), làm tương tự.",
     "Tài khoản: D, E",
     "- Cả D và E chỉ xem kết quả điểm danh, không chọn/sửa được của ai.", ""),
    ("Điểm danh", "Thành viên tự xác nhận tham dự trước giờ họp", "P0",
     "MT-05 Đã chốt lịch, chưa tới giờ họp; D chưa xác nhận.",
     "1. Đăng nhập D, mở chi tiết MT-05.\n2. Bấm 'Vắng có lý do', nhập lý do, Xác nhận.\n3. B mở Sửa MT-05 > tab Điểm danh.",
     "Lý do: 'Đi công tác'",
     "- Báo 'Xác nhận tham dự thành công'.\n- Tab Điểm danh hiện D: Vắng có lý do kèm lý do.\n- B vẫn sửa đè được kết quả của D.", ""),
    ("Điểm danh", "Thành viên không tự xác nhận được sau giờ họp", "P1",
     "MT-05 Đã chốt lịch, đã qua giờ bắt đầu.",
     "1. Đăng nhập D, mở chi tiết MT-05.\n2. Quan sát cụm xác nhận tham dự.",
     "Tài khoản: D",
     "- Không bấm được Có mặt / Vắng có lý do.\n- Hiện lý do: 'Cuộc họp đã đến giờ bắt đầu, việc chốt điểm danh thuộc về người chủ trì.'", ""),
    ("Điểm danh", "Chủ trì lưu điểm danh không làm mất xác nhận thành viên vừa gửi", "P2",
     "B mở sẵn Sửa MT-05 (Đã chốt lịch, chưa tới giờ họp). Sau đó D bấm 'Có mặt' ở máy khác.",
     "1. B không tải lại trang, sửa Ghi chú của thành viên khác, bấm Lưu.\n2. Mở lại tab Điểm danh.",
     "—",
     "- Kết quả 'Có mặt' D vừa tự xác nhận vẫn còn, không bị ghi đè về 'Chưa điểm danh'.",
     "Rà code thấy lưu màn Sửa ghi đè toàn bộ danh sách thành phần - dễ Failed."),

    # ---------------- Lối vào khác ----------------
    (G9, "Tab Meeting ở Việc của tôi / Giải pháp / Hạng mục ẩn nút theo vai trò", "P1",
     "MT-01 trạng thái Lên lịch hẹn; MT-01 gắn với 1 giải pháp mà D xem được.",
     "1. Đăng nhập D.\n2. Mở tab Meeting ở màn Việc của tôi, màn Quản lý giải pháp, màn Hạng mục giải pháp.\n3. Quan sát nút trên dòng MT-01.",
     "Tài khoản: D",
     "- Không có Sửa / Chỉnh sửa / Xóa với meeting D không tạo và không chủ trì (khớp với màn danh sách Meeting).",
     "Rà code thấy các tab này chưa kiểm vai trò, chỉ xét trạng thái - dễ Failed."),
    (G9, "Lịch meeting: nút Sửa trên khung chi tiết", "P2",
     "MT-01 đã Hoàn thành, A là người tạo.",
     "1. Đăng nhập A, mở Lịch meeting.\n2. Bấm vào MT-01 để mở khung chi tiết.",
     "Tài khoản: A",
     "- Không hiện nút Sửa với meeting Đã hoàn thành / Huỷ.",
     "Rà code thấy khung này hiện Sửa không xét trạng thái - dễ Failed."),
]

# ---------------------------------------------------------------- kiểm tra
BANNED = [r"\bAPI /", r"/api/v1", r"\b(400|403|404|422|423)\b", r"can_edit", r"status", r"created_by", r"host"]
txt = "\n".join("\n".join(t) for t in TCS)
bad = {p: len(re.findall(p, txt)) for p in BANNED if re.findall(p, txt)}
print("!!! thuat ngu:", bad) if bad else print("OK - sach")
emo = re.findall(r"[☀-➿\U0001F300-\U0001FAFF]", txt)
print("!!! emoji", emo) if emo else print("OK - khong emoji")
p0 = sum(t[2] == "P0" for t in TCS)
print(f"{len(TCS)} TC, P0 {p0} ({p0 * 100 // len(TCS)}%)")

# ---------------------------------------------------------------- HTML
BASE = "font-family:'Times New Roman';font-size:11pt;border:1px solid #bfbfbf;vertical-align:middle;white-space:pre-wrap;"
GREEN, YEL = "#93c47d", "#fff2cc"


def td(v, extra="", attrs=""):
    return f'<td {attrs} style="{BASE}{extra}">' + html.escape(v).replace("\n", "<br>") + "</td>"


rows = ["<tr>" + td(TITLE_A, f"background:{GREEN};font-weight:bold;", 'colspan="5"')
        + td("", f"background:{GREEN};") + td(TITLE_G, f"background:{GREEN};font-weight:bold;", 'colspan="2"')
        + "".join(td("", f"background:{GREEN};") for _ in range(7))
        + "".join(td("", f"background:{YEL};") for _ in range(5)) + "</tr>"]
span = {}
for t in TCS: span[t[0]] = span.get(t[0], 0) + 1
seen = set()
for i, (grp, name, pri, pre, steps, data, exp, note) in enumerate(TCS, 1):
    r = "<tr>" + td("")
    if grp not in seen:
        seen.add(grp)
        r += td(grp, "text-align:center;", f'rowspan="{span[grp]}"')
    r += td("") + td(f"TC_11.{i:03d}", "text-align:center;background:#ffffff;") + td(name) \
        + td(pri, "text-align:center;background:#ffffff;") + td(pre) + td(steps) + td(data) + td(exp) + td("") \
        + td("Not Executed", "text-align:center;") + td("") + td("") + td(note) \
        + "".join(td("", f"background:{YEL};") for _ in range(5)) + "</tr>"
    rows.append(r)
doc = '<html><head><meta charset="utf-8"></head><body><table style="border-collapse:collapse">' + "".join(rows) + "</table></body></html>"
open(os.path.join(HERE, "meeting-role-status.html"), "w", encoding="utf-8").write(doc)
print("rows:", len(rows))
