# -*- coding: utf-8 -*-
"""Generator testcase cho man 'Lich lam viec cua toi' (/assign/my-todo).

Dung engine chung tc_engine.build(). Xem .claude/skills/testcase-documenter/SKILL.md.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "..", ".claude", "skills",
                                 "testcase-documenter", "assets"))
from tc_engine import build

FEATURE_NAME = "Lịch làm việc của tôi"
MODULE_NAME = "Lịch làm việc của tôi"
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testcase.xlsx")

# ============================================================ 9 MỤC MÔ TẢ
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Gộp 6 nguồn việc của người đang đăng nhập (Task, Issue, Phiếu công tác, Phiếu giao việc, "
     "Meeting, Nhắc việc cá nhân) về MỘT màn xem nhanh duy nhất, gồm 2 tab: \"Công việc của tôi\" "
     "(danh sách chia theo hạn, có thẻ thống kê và danh sách cá nhân) và \"Lịch làm việc\" (lịch "
     "Tháng/Tuần). Người dùng không phải mở lần lượt từng phân hệ (Task, Issue, Meeting, Phiếu…) "
     "để biết hôm nay/tuần này mình còn việc gì."),
    ("2. Đối tượng được tính / hiển thị",
     "6 loại việc, mỗi loại có điều kiện thuộc \"việc của tôi\" riêng: "
     "(1) Task, Issue — được giao (người phụ trách) cho người đang đăng nhập; "
     "(2) Phiếu giao việc, Phiếu công tác — người đang đăng nhập có tên trong danh sách nhân sự "
     "tham gia phiếu; "
     "(3) Meeting — người đang đăng nhập có tên trong mục \"Thành phần — Phía Công ty\" của cuộc "
     "họp (không xét người chủ trì, không xét người tạo nếu không có tên ở thành phần); riêng "
     "Meeting đang ở trạng thái \"Đang tạo\" thì CHỈ người tạo thấy được, người có tên trong thành "
     "phần nhưng không phải người tạo cũng KHÔNG thấy; "
     "(4) Nhắc việc cá nhân — là nhắc việc do chính người đang đăng nhập tạo ra, không chia sẻ "
     "được cho người khác xem. "
     "Ở tab danh sách, việc được xếp vào 1 trong 7 nhóm theo hạn: Quá hạn, Hôm nay, Ngày mai, Tuần "
     "này, Tuần sau, Sau đó, Không hạn. Ở tab lịch, việc hiện thành thẻ trên lưới Tháng/Tuần theo "
     "đúng ngày hạn (nhiều ngày thì trải trên mọi ngày trong khoảng)."),
    ("3. Đối tượng bị ẩn / không tính",
     "— Task, Issue KHÔNG giao cho người đang đăng nhập (giao cho người khác). "
     "— Phiếu giao việc, Phiếu công tác mà người đang đăng nhập KHÔNG có tên trong danh sách nhân "
     "sự tham gia. "
     "— Meeting mà người đang đăng nhập không có tên trong \"Thành phần — Phía Công ty\"; hoặc "
     "Meeting đang ở trạng thái \"Đang tạo\" mà người đang đăng nhập không phải người tạo. "
     "— Nhắc việc cá nhân của người khác. "
     "— Riêng TAB DANH SÁCH còn lọc bỏ thêm theo trạng thái (tab lịch KHÔNG lọc, hiện đủ): Task ở "
     "trạng thái Hoàn thành/Huỷ/Từ chối/Từ chối bắt đầu, Issue ở trạng thái Đã đóng/Từ chối, Phiếu "
     "giao việc/Phiếu công tác ở trạng thái Từ chối/Không duyệt, Meeting ở trạng thái Huỷ, và các "
     "trạng thái CHƯA DUYỆT (Chờ duyệt) của mọi loại có bước duyệt. "
     "— Việc chưa xác định được ngày hạn (không có ngày bắt đầu) KHÔNG lên lịch ở tab Lịch làm "
     "việc (vẫn còn thấy ở tab danh sách, nhóm \"Không hạn\")."),
    ("4. Bộ lọc thời gian áp dụng cho",
     "Tab danh sách: lọc theo NGÀY HẠN (due date) của việc để chia nhóm Quá hạn/Hôm nay/…/Không "
     "hạn và tính 4 thẻ thống kê — dữ liệu tải theo THÁNG đang xem trên lịch mini. "
     "Tab lịch: lọc theo khoảng ngày của LƯỚI đang hiển thị — chế độ Tháng tải đúng 42 ô (6 tuần, "
     "gồm cả ngày của tháng liền kề), chế độ Tuần tải đúng 7 ngày từ Thứ 2 đến Chủ nhật. Việc nhiều "
     "ngày được tính là \"trong khoảng\" nếu khoảng thời gian của việc giao với khoảng đang xem, "
     "không chỉ xét ngày bắt đầu."),
    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Nhắc việc cá nhân có thể có nhiều BƯỚC CON (mỗi bước tích hoàn thành độc lập, nhưng có quy "
     "tắc lan truyền với việc cha — xem mục 6). Danh sách cá nhân là cây 1 cấp: 1 danh sách chứa "
     "nhiều nhắc việc; mỗi nhắc việc thuộc đúng 1 danh sách. Mỗi người dùng có sẵn tối thiểu 1 danh "
     "sách \"Mặc định\" do hệ thống tạo khi tài khoản phát sinh nhắc việc đầu tiên."),
    ("6. Quy tắc cộng dồn / lan truyền / loại trừ trùng",
     "— Nhóm \"Tuần này\" ở tab danh sách là nhóm BAO TRÙM, CỐ Ý: việc hạn Hôm nay hoặc Ngày mai "
     "vẫn được liệt kê thêm 1 lần nữa ở nhóm \"Tuần này\" để khớp đúng con số trên thẻ thống kê "
     "\"Tuần này\" — đây KHÔNG phải lỗi hiển thị trùng. "
     "— Quá hạn chỉ tính khi hạn đã qua VÀ việc còn ở nhóm trạng thái \"Chưa bắt đầu\"/\"Đang "
     "chạy\"; việc đã xong hoặc đã dừng/huỷ KHÔNG BAO GIỜ tính quá hạn dù hạn đã qua rất lâu. "
     "— Tick hoàn thành lan truyền cha ⇄ con: tích việc CHA thì mọi bước CON cùng chuyển theo; tích "
     "đủ hết các bước CON thì việc CHA tự chuyển Hoàn thành, bỏ tích 1 bước CON bất kỳ thì việc CHA "
     "lập tức bỏ Hoàn thành. "
     "— Số đếm trên chip loại (tab lịch) tính theo đúng kỳ THẬT (Tháng/Tuần) đang xem, không cộng "
     "thêm các thẻ của ngày tháng liền kề hiện mờ trên lưới 42 ô — nên số trên chip có thể ÍT HƠN "
     "số thẻ nhìn thấy bằng mắt, đây là hành vi đúng."),
    ("7. Phân quyền cấp",
     "KHÔNG áp dụng phân quyền theo cấp (Q/V) như các màn danh mục khác — nhóm route của màn này "
     "không gắn bất kỳ tên quyền chức năng nào, điều kiện DUY NHẤT để vào màn là ĐÃ ĐĂNG NHẬP hệ "
     "thống. Phạm vi dữ liệu nhìn thấy quyết định bởi tiêu chí SỞ HỮU từng loại việc (xem mục 2). "
     "Riêng 2 nút \"Sửa\" và \"Xem biên bản\" trong panel chi tiết Meeting KẾ THỪA NGUYÊN quy tắc "
     "phân quyền của màn Meeting gốc (không phải quyền riêng của màn này): nút \"Sửa\" chỉ hiện "
     "khi người đang đăng nhập là người tạo HOẶC người chủ trì cuộc họp đó — người chỉ có tên trong "
     "thành phần tham gia thì không sửa được; nút \"Xem biên bản\" chỉ hiện khi cuộc họp đã có ít "
     "nhất 1 bản ghi biên bản."),
    ("8. Cách tính các ô thống kê",
     "— 4 thẻ thống kê (Quá hạn / Hôm nay / Tuần này / Tổng việc) ở tab danh sách: đếm trên tập "
     "việc ĐÃ TẢI của tháng đang xem trên lịch mini, có chịu ảnh hưởng của bộ lọc Loại và Trạng "
     "thái (chọn Loại=Task thì 4 thẻ chỉ đếm Task), nhưng KHÔNG chịu ảnh hưởng của ô tìm nhanh (gõ "
     "tìm nhanh chỉ ẩn/hiện dòng trên màn, không đổi số trên 4 thẻ). "
     "— \"Tuần này\" trên thẻ thống kê = tổng số việc thuộc nhóm bao trùm \"Tuần này\" (đã gồm cả "
     "phần trùng với Hôm nay/Ngày mai, xem mục 6). "
     "— 6 chip loại (tab lịch): mỗi chip đếm đúng số việc của loại đó rơi vào kỳ THẬT (Tháng/Tuần) "
     "đang xem — không đếm thẻ của ngày liền kề tháng trước/sau dù các thẻ đó vẫn được vẽ trên lưới "
     "42 ô."),
    ("9. Ghi chú đọc bảng",
     "⚠️ Nhóm \"Tuần này\" CỐ Ý lặp lại việc đã có ở \"Hôm nay\"/\"Ngày mai\" — đừng báo lỗi trùng "
     "dữ liệu. "
     "⚠️ Ở chế độ xem Tháng, lưới luôn vẽ đủ 6 hàng (42 ô) kể cả ngày của tháng liền kề (các ô đó "
     "làm mờ hơn) — số đếm trên chip loại có thể ÍT HƠN số thẻ nhìn thấy trên lưới, đây là hành vi "
     "đúng, không phải lỗi lệch số. "
     "⚠️ Ô lọc Trạng thái ở tab lịch CHỈ mở khoá khi đang bật ĐÚNG 1 chip loại; bật 0 hoặc từ 2 chip "
     "trở lên thì ô này khoá và hiện chữ \"Chọn 1 loại để lọc trạng thái\" thay vì \"Tất cả\". "
     "⚠️ Việc \"Tạm dừng\" (chỉ có ở Task) được LÀM MỜ như mọi việc dừng/huỷ khác, nhưng KHÔNG gạch "
     "ngang tiêu đề — chỉ 4 trạng thái kết thúc HẲN (Huỷ, Từ chối, Từ chối bắt đầu của Task; Từ "
     "chối của Issue/Phiếu giao việc; Không duyệt của Phiếu công tác; Huỷ của Meeting) mới gạch "
     "ngang. "
     "⚠️ Việc CHƯA CÓ HẠN không bao giờ xuất hiện trên lịch (tab Lịch làm việc), dù vẫn còn ở tab "
     "danh sách nhóm \"Không hạn\" — đừng báo thiếu dữ liệu trên lịch. "
     "⚠️ Tiêu đề popover \"+N khác\" còn giữ chữ \"Meeting\" cứng từ bản thiết kế cũ (vd \"Meeting "
     "ngày 11/09/2026 (5)\") dù bên trong có thể là Task/Issue/loại khác — đây là hạn chế đã biết "
     "của nhãn hiển thị, không phải sai loại việc. "
     "⚠️ Panel chi tiết Meeting/Phiếu công tác/Phiếu giao việc CHỈ CÓ 1 BẢN duy nhất dùng chung cho "
     "cả 2 tab — mở dòng/thẻ khác trong lúc panel đang mở sẽ THAY nội dung panel, không mở thêm "
     "panel thứ hai."),
]

# ============================================================ TC-ROLE — PHẠM VI DỮ LIỆU THEO SỞ HỮU
ROLE_TCS = [
    ("01", "Task/Issue chỉ hiện với người được giao, không hiện với người khác", "P0",
     "Tài khoản A được giao 3 Task và 2 Issue có hạn trong tháng hiện tại. Tài khoản B không được "
     "giao Task/Issue nào trong số đó.",
     "1. Đăng nhập tài khoản A, vào Lịch làm việc của tôi, tab \"Công việc của tôi\".\n"
     "2. Ghi nhận đủ 3 Task + 2 Issue nói trên xuất hiện trong danh sách.\n"
     "3. Đăng xuất, đăng nhập tài khoản B, vào lại đúng màn.",
     "Tài khoản A: 3 Task + 2 Issue | Tài khoản B: 0 Task, 0 Issue của A",
     "- Tài khoản A: thấy đủ 3 Task và 2 Issue được giao cho mình.\n"
     "- Tài khoản B: danh sách KHÔNG có bất kỳ Task/Issue nào của tài khoản A, dù cùng công ty."),
    ("02", "Phiếu giao việc / Phiếu công tác chỉ hiện với nhân sự có tên tham gia", "P0",
     "Phiếu giao việc PGV-001 có danh sách nhân sự tham gia gồm tài khoản A và C. Tài khoản B "
     "không có tên trong danh sách nhân sự tham gia phiếu này.",
     "1. Đăng nhập tài khoản A, vào tab \"Công việc của tôi\", tìm phiếu PGV-001.\n"
     "2. Đăng nhập tài khoản B, vào lại đúng màn, tìm phiếu PGV-001.",
     "Phiếu giao việc PGV-001 — nhân sự tham gia: A, C",
     "- Tài khoản A: thấy phiếu PGV-001 trong danh sách.\n"
     "- Tài khoản B: KHÔNG thấy phiếu PGV-001 (không có tên trong nhân sự tham gia)."),
    ("03", "Meeting chỉ hiện với người có tên trong Thành phần — Phía Công ty", "P0",
     "Meeting \"Họp triển khai Q3\" (đã Lên lịch) có Thành phần — Phía Công ty gồm tài khoản A và "
     "D (D chỉ là người chủ trì, KHÔNG có tên trong Thành phần).",
     "1. Đăng nhập tài khoản A, vào tab \"Công việc của tôi\", tìm meeting \"Họp triển khai Q3\".\n"
     "2. Đăng nhập tài khoản D (người chủ trì nhưng không có tên trong Thành phần), tìm lại đúng "
     "meeting.",
     "Meeting \"Họp triển khai Q3\" — Thành phần: A; Chủ trì: D",
     "- Tài khoản A: thấy meeting trong danh sách (có tên trong Thành phần).\n"
     "- Tài khoản D: KHÔNG thấy meeting này dù là người chủ trì — chỉ xét tên trong Thành phần, "
     "không xét vai trò chủ trì."),
    ("04", "Meeting \"Đang tạo\" chỉ người tạo thấy, người có tên Thành phần cũng không thấy", "P0",
     "Meeting \"Họp nội bộ nháp\" đang ở trạng thái \"Đang tạo\", người tạo là tài khoản A, Thành "
     "phần — Phía Công ty đã điền sẵn gồm A và E.",
     "1. Đăng nhập tài khoản A (người tạo), vào tab \"Công việc của tôi\", tìm meeting \"Họp nội bộ "
     "nháp\".\n"
     "2. Đăng nhập tài khoản E (có tên trong Thành phần nhưng không phải người tạo), tìm lại đúng "
     "meeting.",
     "Meeting \"Họp nội bộ nháp\" — trạng thái Đang tạo; người tạo A; Thành phần: A, E",
     "- Tài khoản A: thấy meeting trong danh sách.\n"
     "- Tài khoản E: KHÔNG thấy meeting này khi còn ở trạng thái \"Đang tạo\", dù có tên trong "
     "Thành phần."),
    ("05", "Nhắc việc cá nhân không chia sẻ được, chỉ chủ sở hữu thấy", "P0",
     "Tài khoản A có nhắc việc cá nhân \"Chuẩn bị báo cáo tuần\" trong danh sách \"Mặc định\".",
     "1. Đăng nhập tài khoản A, xác nhận thấy nhắc việc \"Chuẩn bị báo cáo tuần\".\n"
     "2. Đăng nhập tài khoản B, vào cùng màn, tìm nhắc việc cùng tên.",
     "Nhắc việc \"Chuẩn bị báo cáo tuần\" — chủ sở hữu: tài khoản A",
     "- Tài khoản A: thấy nhắc việc của mình.\n"
     "- Tài khoản B: KHÔNG thấy nhắc việc này ở bất kỳ đâu (danh sách gộp, danh sách cá nhân, tab "
     "lịch) — nhắc việc cá nhân không chia sẻ được."),
    ("06", "Nút \"Sửa\" trong panel Meeting ẩn khi không phải người tạo/chủ trì", "P0",
     "Meeting \"Họp khách hàng X\" do tài khoản A tạo và chủ trì; tài khoản F có tên trong Thành "
     "phần — Phía Công ty nhưng chỉ tham gia, không phải người tạo/chủ trì.",
     "1. Đăng nhập tài khoản A, bấm dòng meeting \"Họp khách hàng X\" mở panel chi tiết.\n"
     "2. Quan sát nút \"Sửa\" ở panel.\n"
     "3. Đăng nhập tài khoản F, mở lại đúng panel meeting này.\n"
     "4. Quan sát nút \"Sửa\".",
     "Meeting \"Họp khách hàng X\" — người tạo/chủ trì: A; người tham gia: F",
     "- Tài khoản A (người tạo/chủ trì): panel hiện nút \"Sửa\".\n"
     "- ⚠️ Tài khoản F (chỉ tham gia): panel KHÔNG hiện nút \"Sửa\" — ẩn hẳn, không hiện xám."),
    ("07", "Nút \"Xem biên bản\" chỉ hiện khi Meeting đã có biên bản", "P1",
     "Meeting \"Họp A\" chưa có bản ghi biên bản nào; Meeting \"Họp B\" đã có 1 biên bản.",
     "1. Mở panel chi tiết \"Họp A\", quan sát khu vực nút thao tác.\n"
     "2. Đóng panel, mở panel chi tiết \"Họp B\", quan sát khu vực nút thao tác.",
     "Họp A: 0 biên bản | Họp B: 1 biên bản",
     "- \"Họp A\": KHÔNG có nút \"Xem biên bản\".\n"
     "- \"Họp B\": có nút \"Xem biên bản\", bấm vào mở đúng biên bản đã lập."),
    ("08", "Dùng công cụ kiểm thử API gọi thẳng chức năng xem chi tiết việc không thuộc sở hữu", "P1",
     "Task \"Thiết kế màn hình Y\" được giao cho tài khoản A, tài khoản B không liên quan.",
     "1. Đăng nhập tài khoản B trên trình duyệt để lấy phiên đăng nhập hợp lệ.\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng xem chi tiết đúng Task \"Thiết kế màn hình "
     "Y\" bằng phiên của tài khoản B, bỏ qua giao diện.",
     "Task \"Thiết kế màn hình Y\" — người phụ trách: A",
     "- Hệ thống từ chối trả dữ liệu chi tiết của Task cho tài khoản B (không phải người phụ "
     "trách) — không lộ nội dung Task cho người ngoài phạm vi sở hữu.\n"
     "- Ghi chú cho tester kỹ thuật: nhóm ca này dành riêng để kiểm bảo mật tầng máy chủ, không "
     "chạy được bằng thao tác giao diện thông thường."),
]

# ============================================================ SECTIONS
SECTIONS = []

# -------------------------------------------------------------------- I
SECTIONS.append(("I", "HIỂN THỊ TRANG & TRUY CẬP", [
    (1, "Vào màn lần đầu, tab \"Công việc của tôi\" được chọn sẵn", "P0",
     "Tài khoản A đăng nhập lần đầu trong ngày, có 2 Task quá hạn, 1 Task hạn hôm nay, 3 việc hạn "
     "tuần này, 8 việc tổng cộng trong tháng.",
     "1. Đăng nhập, vào menu Dự án & giao việc → Lịch làm việc của tôi.",
     "—",
     "- Tab \"✅ Công việc của tôi\" được chọn sẵn.\n"
     "- Đủ 4 thẻ thống kê: Quá hạn = 2, Hôm nay = 1, Tuần này = số đúng theo nhóm bao trùm, Tổng "
     "việc = 8.\n"
     "- Danh sách hiện đủ các nhóm theo hạn, cột phải có lịch mini và danh sách cá nhân."),
    (2, "Đổi tab không tải lại trang, giữ trạng thái tab kia", "P1",
     "Đang ở tab \"Công việc của tôi\", đã gõ chữ \"báo cáo\" vào ô tìm nhanh.",
     "1. Bấm tab \"📅 Lịch làm việc\".\n"
     "2. Quan sát lịch hiển thị.\n"
     "3. Bấm lại tab \"✅ Công việc của tôi\".",
     "Ô tìm nhanh: \"báo cáo\"",
     "- Chuyển tab mượt, KHÔNG tải lại toàn trang (không mất vị trí cuộn, không nháy trắng màn "
     "hình).\n"
     "- Quay lại tab danh sách: ô tìm nhanh vẫn còn giữ chữ \"báo cáo\" đã gõ trước đó."),
    (3, "Chưa đăng nhập thì bị điều hướng về màn đăng nhập", "P0",
     "Chưa đăng nhập vào hệ thống (đã đăng xuất hoặc phiên chưa từng đăng nhập).",
     "1. Truy cập thẳng đường dẫn màn Lịch làm việc của tôi khi chưa đăng nhập.",
     "—",
     "- Hệ thống điều hướng về màn đăng nhập, không hiện bất kỳ dữ liệu nào của màn Lịch làm việc."),
    (4, "Không có việc nào trong phạm vi vẫn hiện đủ tiêu đề nhóm với số đếm 0", "P1",
     "Tài khoản mới tạo, chưa được giao Task/Issue nào, chưa có phiếu/meeting nào, chưa tạo nhắc "
     "việc nào.",
     "1. Đăng nhập tài khoản mới, vào tab \"Công việc của tôi\".",
     "—",
     "- 4 thẻ thống kê đều = 0.\n"
     "- Các nhóm luôn hiện (Quá hạn, Hôm nay, Ngày mai, Tuần này) vẫn hiện tiêu đề kèm số đếm 0, "
     "phần thân để trống, KHÔNG có hình minh hoạ trạng thái rỗng riêng."),
    (5, "Mở tab \"Lịch làm việc\" lần đầu vào đúng chế độ Tháng, kỳ hiện tại", "P0",
     "Đang ở ngày 11/09/2026. Có ít nhất 3 việc thuộc tháng 9/2026.",
     "1. Từ tab \"Công việc của tôi\", bấm tab \"📅 Lịch làm việc\".",
     "—",
     "- Chế độ xem mặc định là \"Tháng\".\n"
     "- Nhãn kỳ hiển thị đúng \"Tháng 9/2026\".\n"
     "- Lưới vẽ đủ 6 hàng (42 ô), có 3 việc nói trên hiện đúng ô ngày tương ứng."),
    (6, "Phiên đăng nhập hết hạn giữa lúc đang thao tác → về màn đăng nhập", "P2",
     "Đang mở màn Lịch làm việc của tôi, phiên đăng nhập vừa hết hạn ở phía máy chủ.",
     "1. Đang ở màn, thực hiện 1 thao tác gọi lại dữ liệu (đổi bộ lọc, đổi tháng…).",
     "—",
     "- Hệ thống điều hướng về màn đăng nhập, không hiện lỗi kỹ thuật khó hiểu trên màn."),
]))

# -------------------------------------------------------------------- II
SECTIONS.append(("II", "BỘ LỌC & TÌM KIẾM", [
    (1, "Ô tìm nhanh lọc theo tiêu đề ngay khi gõ, không đổi 4 thẻ thống kê", "P0",
     "Danh sách đang có 8 việc, trong đó 2 việc có tiêu đề chứa chữ \"báo cáo\".",
     "1. Gõ \"báo cáo\" vào ô tìm nhanh.\n"
     "2. Quan sát danh sách và 4 thẻ thống kê.",
     "Từ khoá: báo cáo",
     "- Danh sách chỉ còn 2 việc có tiêu đề chứa \"báo cáo\" (không phân biệt hoa/thường), lọc "
     "NGAY khi gõ, không cần bấm nút.\n"
     "- 4 thẻ thống kê GIỮ NGUYÊN số như trước khi gõ tìm nhanh."),
    (2, "Chọn Loại = Task, danh sách và thẻ thống kê đổi theo", "P0",
     "Có 3 Task, 2 Issue, 1 Meeting đến hạn trong tháng.",
     "1. Mở dropdown \"Loại\", chọn \"Task\".",
     "Loại: Task",
     "- Hệ thống gọi lại dữ liệu, danh sách chỉ còn 3 Task.\n"
     "- 4 thẻ thống kê tính lại chỉ trên 3 Task đó (không còn tính Issue/Meeting)."),
    (3, "Dropdown Loại đủ 7 lựa chọn", "P1",
     "Đứng ở tab \"Công việc của tôi\".",
     "1. Mở dropdown \"Loại\".",
     "—",
     "- Đủ 7 lựa chọn theo đúng thứ tự: Tất cả, Task, Issue, Phiếu giao việc, Phiếu giao công tác, "
     "Meeting, Cá nhân."),
    (4, "Dropdown Trạng thái dùng chung 3 lựa chọn cho mọi loại, mặc định \"Chưa xong\"", "P1",
     "Vừa vào màn, chưa đổi bộ lọc Trạng thái.",
     "1. Quan sát ô Trạng thái lúc mới vào màn.\n"
     "2. Mở dropdown Trạng thái.",
     "—",
     "- Giá trị mặc định hiện \"Chưa xong\".\n"
     "- Đủ 3 lựa chọn: Chưa xong, Đã xong, Tất cả — dùng chung 1 bộ cho cả 6 loại việc (không đổi "
     "theo từng loại như bên tab Lịch)."),
    (5, "Bấm nút làm mới bộ lọc trả mọi tiêu chí về mặc định", "P0",
     "Đã gõ \"abc\" vào ô tìm nhanh, chọn Loại = Meeting, Trạng thái = Tất cả, đang chọn ngày 15 "
     "trên lịch mini.",
     "1. Bấm nút làm mới bộ lọc (icon vòng xoay cạnh ô tìm nhanh).",
     "—",
     "- Ô tìm nhanh về trống.\n"
     "- Loại về \"Tất cả\", Trạng thái về \"Chưa xong\".\n"
     "- Ngày 15 đang chọn trên lịch mini được bỏ chọn, danh sách quay về chế độ nhóm theo hạn.\n"
     "- Danh sách tải lại theo đúng bộ lọc mặc định."),
    (6, "Không có việc khớp từ khoá tìm nhanh → nhóm hiện rỗng, không có thông báo riêng", "P2",
     "Danh sách đang có việc nhưng không việc nào có tiêu đề chứa \"xyzkhongtontai\".",
     "1. Gõ \"xyzkhongtontai\" vào ô tìm nhanh.",
     "Từ khoá: xyzkhongtontai",
     "- Các nhóm vẫn hiện tiêu đề, phần thân trống.\n"
     "- KHÔNG có thông báo riêng kiểu \"không tìm thấy kết quả\"."),
    (7, "Bấm ngày có chấm trên lịch mini chuyển sang chế độ phẳng đúng ngày", "P0",
     "Ngày 20 trong tháng đang xem có 2 việc đến hạn (có chấm); các ngày khác không có chấm.",
     "1. Bấm vào ô ngày 20 trên lịch mini.",
     "—",
     "- Danh sách chính chuyển sang \"chế độ phẳng\": chỉ còn liệt kê đúng 2 việc có hạn ngày 20, "
     "KHÔNG còn chia theo 7 nhóm hạn.\n"
     "- Ô ngày 20 tô nền xanh đậm, khác màu ô \"Hôm nay\" (nếu 2 ngày khác nhau)."),
    (8, "Bấm lại đúng ngày đang chọn để bỏ chọn, quay về chế độ nhóm", "P1",
     "Đang chọn ngày 20 ở chế độ phẳng (tiếp nối TC trên).",
     "1. Bấm lại đúng ô ngày 20 đang được tô chọn.",
     "—",
     "- Bỏ chọn ngày 20, danh sách quay lại chế độ nhóm theo hạn của toàn bộ tháng."),
    (9, "Ngày thuộc tháng liền kề trên lịch mini không bấm được", "P2",
     "Lịch mini đang hiển thị tháng 9/2026, các ô đầu/cuối lưới thuộc tháng 8 và tháng 10 hiện mờ.",
     "1. Bấm vào 1 ô ngày mờ thuộc tháng liền kề (vd ngày 31/08).",
     "—",
     "- Không có phản ứng gì, danh sách chính không đổi (ô này không bấm được)."),
    (10, "Chọn ngày trên lịch mini không có việc → thông báo đúng chữ", "P2",
     "Ngày 25 trong tháng đang xem không có việc nào đến hạn (không có chấm).",
     "1. Bấm vào ô ngày 25.",
     "—",
     "- Danh sách chính hiện đúng dòng chữ \"Không có việc trong ngày này\"."),
    (11, "Nút lùi/tiến tháng ở lịch mini chỉ đổi hiển thị lịch mini", "P2",
     "Lịch mini đang ở tháng 9/2026, danh sách chính đang hiện việc của tháng 9/2026.",
     "1. Bấm mũi tên tiến 1 tháng ở lịch mini.\n"
     "2. Quan sát danh sách chính.",
     "—",
     "- Lịch mini chuyển sang hiển thị tháng 10/2026.\n"
     "- Danh sách chính KHÔNG đổi, vẫn hiện việc của tháng 9/2026 cho tới khi người dùng bấm chọn "
     "1 ngày cụ thể."),
    (12, "6 chip loại ở tab lịch, mỗi chip kèm số lượng đúng kỳ đang xem", "P0",
     "Tháng 9/2026 có 4 Task, 2 Issue, 1 Phiếu công tác, 3 Meeting, 0 Phiếu giao việc, 2 Nhắc việc "
     "cá nhân có hạn trong tháng (tính đúng theo kỳ thật, không tính thẻ ngày liền kề).",
     "1. Vào tab \"📅 Lịch làm việc\", chế độ Tháng.\n"
     "2. Quan sát số trên từng chip.",
     "—",
     "- Chip Task hiện 4, Issue hiện 2, Phiếu công tác hiện 1, Meeting hiện 3, Phiếu giao việc hiện "
     "0, Nhắc việc cá nhân hiện 2.\n"
     "- ⚠️ Nếu lưới 42 ô có vẽ thêm thẻ của ngày tháng liền kề, số trên chip KHÔNG cộng thêm các "
     "thẻ đó — đúng theo thiết kế, không phải lỗi lệch số."),
    (13, "Bấm 1 chip loại để lọc, ô Trạng thái mở khoá đúng bộ trạng thái của loại đó", "P0",
     "Đang ở tab Lịch làm việc, chưa bật chip nào.",
     "1. Bấm chip \"Task\".\n"
     "2. Quan sát ô Trạng thái.\n"
     "3. Mở dropdown Trạng thái.",
     "Loại: Task",
     "- Chip \"Task\" chuyển trạng thái bật (nổi bật), lưới chỉ còn hiện Task.\n"
     "- Ô Trạng thái mở khoá, đổ đúng 10 trạng thái Task: Nháp, Chờ duyệt, Cần làm, Đang làm, Tạm "
     "dừng, Review, Từ chối, Hoàn thành, Huỷ, Từ chối bắt đầu."),
    (14, "Bật 0 hoặc từ 2 chip trở lên thì ô Trạng thái khoá lại", "P0",
     "Đang bật đúng chip \"Task\" (ô Trạng thái đang mở khoá theo TC trước).",
     "1. Bấm thêm chip \"Issue\" (đang bật 2 chip: Task, Issue).\n"
     "2. Quan sát ô Trạng thái.\n"
     "3. Bấm tắt cả 2 chip đang bật (về 0 chip).\n"
     "4. Quan sát lại ô Trạng thái.",
     "—",
     "- Bật 2 chip: ô Trạng thái khoá lại, hiện chữ \"Chọn 1 loại để lọc trạng thái\" thay cho "
     "\"Tất cả\".\n"
     "- Bật 0 chip: ô Trạng thái vẫn khoá, cùng thông báo trên; lưới hiện đủ 6 loại."),
    (15, "Đổi loại đang lọc trạng thái thì trạng thái cũ tự về rỗng", "P1",
     "Đang bật chip \"Task\", đã chọn Trạng thái = \"Đang làm\".",
     "1. Bấm tắt chip \"Task\", bấm bật chip \"Meeting\".\n"
     "2. Quan sát ô Trạng thái.",
     "—",
     "- Trạng thái \"Đang làm\" (thuộc bộ Task) tự động về rỗng — không giữ lại giá trị vô nghĩa "
     "với Meeting.\n"
     "- Mở lại dropdown Trạng thái: đổ đúng 5 trạng thái Meeting (Đang tạo, Lên lịch, Chốt lịch, "
     "Hoàn thành, Hủy)."),
    (16, "Bấm nút làm mới ở tab lịch tắt hết chip và khoá Trạng thái", "P1",
     "Đang bật chip \"Task\" với Trạng thái = \"Hoàn thành\".",
     "1. Bấm nút làm mới trên thanh lọc của tab Lịch làm việc.",
     "—",
     "- Tắt hết mọi chip loại (không chip nào được bật = xem đủ 6 loại).\n"
     "- Trạng thái về rỗng và khoá lại.\n"
     "- Lưới gọi lại dữ liệu đủ 6 loại việc."),
]))

# -------------------------------------------------------------------- III
SECTIONS.append(("III", "DANH SÁCH, NHÓM THEO HẠN & THẺ THỐNG KÊ", [
    (1, "Việc phân đúng vào 7 nhóm theo hạn", "P0",
     "Tài khoản A có: 1 việc hạn hôm qua (còn Đang làm) = Quá hạn; 1 việc hạn hôm nay; 1 việc hạn "
     "ngày mai; 1 việc hạn trong 5 ngày tới (cùng tuần); 1 việc hạn tuần sau; 1 việc hạn tháng sau; "
     "1 việc không đặt ngày hạn.",
     "1. Vào tab \"Công việc của tôi\", mở hết các nhóm.",
     "—",
     "- Việc hạn hôm qua nằm ở nhóm \"Quá hạn\".\n"
     "- Việc hạn hôm nay nằm ở nhóm \"Hôm nay\".\n"
     "- Việc hạn ngày mai nằm ở nhóm \"Ngày mai\" VÀ CẢ nhóm \"Tuần này\" (xem TC III.2).\n"
     "- Việc hạn tuần sau nằm ở nhóm \"Tuần sau\".\n"
     "- Việc hạn tháng sau nằm ở nhóm \"Sau đó\".\n"
     "- Việc không đặt hạn nằm ở nhóm \"Không hạn\", KHÔNG tính vào 4 thẻ thống kê."),
    (2, "Nhóm \"Tuần này\" là nhóm bao trùm, việc hạn Ngày mai xuất hiện thêm ở đây", "P0",
     "1 việc có hạn đúng ngày mai (thuộc cùng tuần với hôm nay).",
     "1. Mở nhóm \"Ngày mai\", ghi nhận có việc này.\n"
     "2. Mở nhóm \"Tuần này\", tìm cùng việc đó.",
     "—",
     "- ⚠️ Việc này xuất hiện ở CẢ nhóm \"Ngày mai\" LẪN nhóm \"Tuần này\" — đây là hành vi cố ý "
     "(nhóm \"Tuần này\" bao trùm), không phải lỗi hiển thị trùng dòng."),
    (3, "4 thẻ thống kê không đổi theo ô tìm nhanh nhưng đổi theo Loại/Trạng thái", "P0",
     "Đang có 4 thẻ: Quá hạn 2, Hôm nay 3, Tuần này 6, Tổng việc 10.",
     "1. Gõ 1 từ khoá bất kỳ vào ô tìm nhanh khiến danh sách chỉ còn 2 dòng.\n"
     "2. Quan sát 4 thẻ thống kê.\n"
     "3. Xoá ô tìm nhanh, đổi Loại = Task khiến danh sách chỉ còn Task.\n"
     "4. Quan sát lại 4 thẻ.",
     "—",
     "- Bước 2: 4 thẻ GIỮ NGUYÊN (2 / 3 / 6 / 10) dù danh sách chỉ còn 2 dòng.\n"
     "- Bước 4: 4 thẻ ĐỔI THEO đúng số liệu chỉ tính trên Task."),
    (4, "Bấm tiêu đề 1 nhóm chỉ thu gọn/mở rộng đúng nhóm đó", "P1",
     "Cả 7 nhóm đang ở trạng thái mặc định (Hôm nay mở, các nhóm khác theo mặc định).",
     "1. Bấm tiêu đề nhóm \"Tuần sau\" để thu gọn.\n"
     "2. Quan sát các nhóm còn lại.",
     "—",
     "- Chỉ nhóm \"Tuần sau\" đổi trạng thái thu gọn.\n"
     "- Các nhóm khác (Hôm nay, Quá hạn…) giữ nguyên trạng thái đang có, không bị ảnh hưởng."),
    (5, "Nhóm luôn hiện tiêu đề dù thu gọn hoặc bằng 0", "P2",
     "Nhóm \"Ngày mai\" hiện có 0 việc.",
     "1. Quan sát nhóm \"Ngày mai\" trong danh sách.",
     "—",
     "- Tiêu đề nhóm \"Ngày mai\" vẫn hiện kèm số đếm (0), không bị ẩn khỏi màn hình."),
    (6, "Task Hoàn thành/Huỷ bị lọc bỏ ở tab danh sách nhưng vẫn còn ở tab lịch", "P0",
     "Task \"Sửa lỗi giao diện\" ở trạng thái Hoàn thành, có hạn trong tháng hiện tại.",
     "1. Ở tab \"Công việc của tôi\", chọn Trạng thái = \"Tất cả\", tìm Task \"Sửa lỗi giao diện\".\n"
     "2. Chuyển sang tab \"Lịch làm việc\", tìm đúng ngày hạn của Task đó.",
     "Trạng thái Task: Hoàn thành",
     "- ⚠️ Bước 1: Task này KHÔNG xuất hiện dù Trạng thái đang chọn \"Tất cả\" — tab danh sách "
     "luôn loại bỏ trạng thái kết thúc (Hoàn thành/Huỷ/Từ chối/Từ chối bắt đầu), không phụ thuộc "
     "bộ lọc Trạng thái.\n"
     "- Bước 2: Task này VẪN xuất hiện trên lịch (làm mờ), vì tab lịch hiện mọi trạng thái."),
    (7, "Badge trạng thái và badge vai trò hiện đúng theo dữ liệu", "P1",
     "Task A giao cho tài khoản đang xem (vai trò Được giao), đang ở trạng thái \"Đang làm\".",
     "1. Quan sát dòng Task A trong danh sách.",
     "—",
     "- Badge vai trò hiện đúng \"Được giao\".\n"
     "- Badge trạng thái hiện đúng chữ và màu theo trạng thái thật \"Đang làm\"."),
    (8, "Ngày hạn tô đỏ đậm khi đã quá hạn", "P1",
     "Task B có hạn hôm qua, còn ở trạng thái Đang làm (chưa xong).",
     "1. Quan sát cột Ngày hạn của Task B.",
     "—",
     "- Ngày hạn hiện tô màu đỏ đậm, kèm việc B nằm ở nhóm \"Quá hạn\"."),
    (9, "Việc đã xong hoặc đã dừng/huỷ không bao giờ tính quá hạn dù hạn đã qua", "P0",
     "Task C có hạn cách đây 10 ngày nhưng đã ở trạng thái Hoàn thành.",
     "1. Chuyển Trạng thái = \"Tất cả\" để thấy Task C.\n"
     "2. Quan sát Task C có bị tính Quá hạn không.",
     "Trạng thái Task C: Hoàn thành, hạn cách đây 10 ngày",
     "- Task C KHÔNG được gắn nhãn/tính vào nhóm \"Quá hạn\" dù hạn đã qua 10 ngày — vì đã Hoàn "
     "thành."),
    (10, "Vòng quay chờ chỉ hiện ở lần tải đầu, không hiện lại khi đồng bộ ngầm", "P2",
     "Đang xem danh sách đã tải xong, có 1 nhắc việc cá nhân đang chờ tick.",
     "1. Bấm tick hoàn thành 1 nhắc việc (kích hoạt đồng bộ ngầm với máy chủ).\n"
     "2. Quan sát có vòng quay chờ che toàn bảng không.",
     "—",
     "- Danh sách KHÔNG hiện lại vòng quay chờ toàn màn, chỉ đổi trạng thái đúng dòng vừa tick."),
]))

# -------------------------------------------------------------------- IV
SECTIONS.append(("IV", "XEM CHI TIẾT CÔNG VIỆC TỪ DANH SÁCH", [
    (1, "Bấm dòng Task mở popup Chi tiết Task", "P0",
     "Danh sách có Task \"Thiết kế màn hình đăng nhập\".",
     "1. Bấm vào phần thân dòng Task \"Thiết kế màn hình đăng nhập\" (không trúng ô tích/nút thao "
     "tác).",
     "—",
     "- Mở popup \"Chi tiết Task\" ở chế độ xem, đúng nội dung Task vừa bấm."),
    (2, "Bấm dòng Issue mở popup Chi tiết Issue", "P0",
     "Danh sách có Issue \"Lỗi không tải được ảnh đại diện\".",
     "1. Bấm vào phần thân dòng Issue nói trên.",
     "—",
     "- Mở popup \"Chi tiết Issue\" ở chế độ xem, đúng nội dung Issue vừa bấm."),
    (3, "Bấm dòng Nhắc việc cá nhân mở popup Chỉnh sửa nhắc việc", "P0",
     "Danh sách có nhắc việc \"Gọi khách hàng Y\".",
     "1. Bấm vào phần thân dòng nhắc việc nói trên.",
     "—",
     "- Mở popup \"Chỉnh sửa nhắc việc cá nhân\", điền sẵn đúng dữ liệu hiện có."),
    (4, "Bấm dòng Meeting/Phiếu công tác/Phiếu giao việc mở panel trượt phải", "P0",
     "Danh sách có Meeting \"Họp review sprint\".",
     "1. Bấm vào phần thân dòng Meeting nói trên.",
     "—",
     "- Panel trượt phải (KHÔNG mở tab trình duyệt mới như bản trước) mở ra, tóm tắt đúng thông "
     "tin Meeting: tên/mã, loại, trạng thái, khoảng thời gian, mục tiêu/nội dung, hình thức, khách "
     "hàng, thành phần, kết luận, người tạo.\n"
     "- Có nút \"Mở chi tiết\" sang màn Meeting đầy đủ."),
    (5, "Panel chi tiết chỉ có 1 bản, mở dòng khác thì thay nội dung", "P1",
     "Đang mở panel chi tiết Meeting \"Họp A\".",
     "1. Trong lúc panel \"Họp A\" đang mở, bấm sang dòng Phiếu công tác \"PCT-005\".",
     "—",
     "- Panel đổi nội dung sang \"PCT-005\", KHÔNG mở thêm panel thứ hai chồng lên panel cũ."),
    (6, "Nút Sửa/Xem biên bản trong panel Meeting theo đúng quyền (xem thêm mục TC-ROLE)", "P1",
     "Meeting do tài khoản đang xem tạo, đã có biên bản.",
     "1. Mở panel Meeting, quan sát nút Sửa và Xem biên bản.",
     "—",
     "- Cả 2 nút đều hiện vì đủ điều kiện (người tạo + đã có biên bản)."),
    (7, "Nút \"Mở chi tiết\" ở 2 loại phiếu mở tab mới, không đóng panel", "P2",
     "Đang mở panel chi tiết Phiếu giao việc \"PGV-010\".",
     "1. Bấm nút \"Mở chi tiết\".",
     "—",
     "- Mở 1 tab trình duyệt mới tới màn chi tiết đầy đủ của phiếu.\n"
     "- Panel ở tab hiện tại VẪN CÒN MỞ, không tự đóng."),
    (8, "Nút đóng (×) đóng panel, không lưu thay đổi gì", "P2",
     "Đang mở panel chi tiết Meeting bất kỳ.",
     "1. Bấm nút đóng (×) ở góc panel.",
     "—",
     "- Panel đóng lại, không có thao tác ghi dữ liệu nào được gọi."),
]))

# -------------------------------------------------------------------- V
SECTIONS.append(("V", "THAO TÁC TRÊN DÒNG QUA MENU", [
    (1, "Rê chuột qua dòng Task hiện đủ dải nút theo quyền của bản ghi", "P0",
     "Task D: người đang đăng nhập được phép Sửa, Nhập kết quả và Duyệt trên đúng bản ghi này "
     "(máy chủ trả đủ cả 3 quyền thao tác cho Task D).",
     "1. Rê chuột qua dòng Task D.",
     "—",
     "- Hiện đủ 5 nút: Xem, Sửa, Nhập kết quả, Duyệt, Lịch sử."),
    (2, "Nút Sửa ẩn hẳn khi bản ghi không cho sửa", "P0",
     "Task E: máy chủ trả cờ không cho sửa bản ghi này.",
     "1. Rê chuột qua dòng Task E.",
     "—",
     "- ⚠️ KHÔNG có nút Sửa trong dải thao tác — ẩn hẳn, KHÔNG hiện nút Sửa dạng xám/khoá."),
    (3, "Issue rê chuột hiện đúng bộ nút Xem/Sửa/Xử lý/Lịch sử", "P0",
     "Issue F: có quyền Xử lý trên bản ghi này.",
     "1. Rê chuột qua dòng Issue F.",
     "—",
     "- Hiện đủ 4 nút: Xem, Sửa, Xử lý, Lịch sử (Issue không có nút Nhập kết quả/Duyệt)."),
    (4, "Task ở nhóm cần nhập/duyệt kết quả → nút Xem đổi hướng sang popup Nhập kết quả", "P1",
     "Task G đang ở trạng thái \"Review\" (thuộc 4 trạng thái cuối cần nhập/duyệt kết quả).",
     "1. Rê chuột qua dòng Task G, bấm nút \"Xem\".",
     "Trạng thái Task G: Review",
     "- Mở popup \"Nhập kết quả\" ở CHẾ ĐỘ CHỈ XEM, thay vì popup \"Chi tiết Task\" thông thường."),
    (5, "Bấm nút thao tác không mở kèm popup chi tiết của việc bấm-vào-dòng", "P1",
     "Task H có đủ nút Sửa.",
     "1. Rê chuột qua dòng Task H, bấm thẳng nút \"Sửa\" (không bấm vào phần thân dòng).",
     "—",
     "- CHỈ mở popup Sửa của Task H, KHÔNG mở kèm popup \"Chi tiết Task\" (không nổi bọt sự kiện "
     "lên dòng)."),
]))

# -------------------------------------------------------------------- VI
SECTIONS.append(("VI", "ĐÁNH DẤU HOÀN THÀNH CÔNG VIỆC", [
    (1, "Tích nhắc việc cha từ chưa xong sang xong hiện hộp xác nhận", "P0",
     "Nhắc việc \"Chuẩn bị hợp đồng\" đang ở trạng thái chưa xong.",
     "1. Bấm ô tích của nhắc việc \"Chuẩn bị hợp đồng\".",
     "—",
     "- Hiện hộp \"Xác nhận hoàn thành\" nêu đúng tên việc \"Chuẩn bị hợp đồng\" trong ngoặc kép.\n"
     "- Trạng thái CHƯA đổi cho tới khi người dùng xác nhận."),
    (2, "Bấm \"Hoàn thành\" trong hộp xác nhận đổi trạng thái ngay và gọi đồng bộ", "P0",
     "Đang mở hộp xác nhận của nhắc việc \"Chuẩn bị hợp đồng\" (tiếp nối TC trên).",
     "1. Bấm \"Hoàn thành\" trong hộp xác nhận.",
     "—",
     "- Dòng \"Chuẩn bị hợp đồng\" đổi trạng thái Hoàn thành NGAY trên màn (không chờ phản hồi máy "
     "chủ), hộp xác nhận đóng lại."),
    (3, "Bấm \"Hủy\" trong hộp xác nhận không đổi gì", "P1",
     "Đang mở hộp xác nhận của 1 nhắc việc.",
     "1. Bấm \"Hủy\" trong hộp xác nhận.",
     "—",
     "- Hộp đóng lại, trạng thái nhắc việc GIỮ NGUYÊN như trước khi bấm tích."),
    (4, "Bỏ đánh dấu hoàn thành (xong → chưa xong) đổi ngay, không hỏi xác nhận", "P0",
     "Nhắc việc \"Gửi báo giá\" đang ở trạng thái Hoàn thành.",
     "1. Bấm ô tích của nhắc việc \"Gửi báo giá\" để bỏ tích.",
     "—",
     "- Đổi ngay về trạng thái chưa xong, KHÔNG hiện hộp xác nhận nào."),
    (5, "Tích việc cha lan xuống mọi bước con", "P0",
     "Nhắc việc \"Tổ chức sự kiện\" có 3 bước con, cả 3 đang chưa xong.",
     "1. Bấm tích nhắc việc cha \"Tổ chức sự kiện\", bấm \"Hoàn thành\" trong hộp xác nhận.",
     "3 bước con: Đặt địa điểm, Mời khách, Chuẩn bị quà tặng",
     "- Cả 3 bước con đồng loạt chuyển sang trạng thái đã tích/hoàn thành theo việc cha."),
    (6, "Tích đủ hết bước con thì việc cha tự chuyển Hoàn thành", "P0",
     "Nhắc việc \"Chuẩn bị workshop\" có 2 bước con, 1 bước đã tích, 1 bước chưa tích. Việc cha "
     "đang chưa xong.",
     "1. Tích nốt bước con còn lại.",
     "—",
     "- Ngay khi bước con cuối cùng được tích, việc cha \"Chuẩn bị workshop\" tự động chuyển sang "
     "Hoàn thành, không cần thao tác gì thêm trên dòng cha."),
    (7, "Bỏ tích 1 bước con thì việc cha lập tức bỏ Hoàn thành", "P0",
     "Nhắc việc \"Chuẩn bị workshop\" đã Hoàn thành (đủ 2/2 bước con đã tích — tiếp nối TC trên).",
     "1. Bỏ tích 1 trong 2 bước con.",
     "—",
     "- Việc cha lập tức chuyển về trạng thái chưa xong, dù bước con còn lại vẫn đang tích."),
    (8, "Gọi API lỗi thì hoàn tác đúng phần vừa đổi và báo lỗi", "P1",
     "Đang tích 1 nhắc việc, mô phỏng mất kết nối mạng ngay khi gọi đồng bộ.",
     "1. Bấm tích nhắc việc, xác nhận Hoàn thành trong lúc mạng bị chặn.",
     "—",
     "- Sau khi gọi đồng bộ thất bại, dòng vừa tích HOÀN TÁC về đúng trạng thái trước đó (không để "
     "hiển thị sai lệch với máy chủ).\n"
     "- Hiện thông báo lỗi \"Không thể cập nhật trạng thái\"."),
    (9, "Việc vừa hoàn thành bị bộ lọc Trạng thái=Chưa xong loại ra thì mờ dần rồi trượt khỏi danh sách", "P2",
     "Trạng thái đang lọc = \"Chưa xong\". Nhắc việc \"Đặt vé máy bay\" đang hiện trong danh sách.",
     "1. Tích hoàn thành nhắc việc \"Đặt vé máy bay\", xác nhận Hoàn thành.",
     "Trạng thái đang lọc: Chưa xong",
     "- Dòng \"Đặt vé máy bay\" mờ dần rồi trượt ra khỏi danh sách bằng hiệu ứng chuyển động, "
     "KHÔNG biến mất đột ngột ngay lập tức."),
    (10, "Chỉ Nhắc việc cá nhân tích được tại đây, các loại khác không có ô tích", "P1",
     "Danh sách có Task, Issue, Meeting, Phiếu giao việc và Nhắc việc cá nhân.",
     "1. Quan sát cột đầu dòng của từng loại việc.",
     "—",
     "- Chỉ dòng Nhắc việc cá nhân có ô tích hoàn thành.\n"
     "- Task/Issue/Meeting/Phiếu giao việc/Phiếu công tác KHÔNG có ô tích tại đây — muốn đổi trạng "
     "thái phải vào đúng màn/popup gốc của loại đó."),
]))

# -------------------------------------------------------------------- VII
SECTIONS.append(("VII", "TẠO & SỬA NHẮC VIỆC CÁ NHÂN", [
    (1, "Tạo nhắc việc mới với đủ thông tin", "P0",
     "Đã có danh sách cá nhân \"Mặc định\" và \"Công việc tuần\".",
     "1. Bấm \"Tạo nhắc việc cá nhân\" trên thanh lọc.\n"
     "2. Nhập Tiêu đề \"Soạn hợp đồng thuê văn phòng\", Mô tả \"Gửi bản nháp cho phòng pháp chế\", "
     "thêm 2 bước \"Soạn nội dung\" và \"Trình ký\", chọn Danh sách = \"Công việc tuần\", chọn Ngày "
     "hạn = 20/09/2026.\n"
     "3. Bấm \"Tạo nhắc việc\".",
     "Tiêu đề: Soạn hợp đồng thuê văn phòng | Danh sách: Công việc tuần | Ngày hạn: 20/09/2026",
     "- Hiện thông báo \"Đã tạo nhắc việc mới\".\n"
     "- Popup đóng lại.\n"
     "- Danh sách, 4 thẻ thống kê, cột danh sách cá nhân và tab Lịch làm việc đều tải lại, nhắc "
     "việc mới xuất hiện đúng nhóm theo hạn 20/09/2026."),
    (2, "Bỏ trắng Tiêu đề báo lỗi ngay dưới ô, không đóng popup", "P0",
     "Đang mở popup Tạo nhắc việc, đã chọn Danh sách, chưa nhập Tiêu đề.",
     "1. Để trống Tiêu đề, bấm \"Tạo nhắc việc\".",
     "Tiêu đề: (trống)",
     "- Hiện lỗi đỏ \"Tiêu đề không được để trống\" ngay dưới ô Tiêu đề.\n"
     "- Popup KHÔNG đóng, dữ liệu đã nhập ở ô khác vẫn còn nguyên."),
    (3, "Chưa chọn Danh sách báo lỗi", "P0",
     "Đang mở popup Tạo nhắc việc, đã nhập Tiêu đề, chưa chọn Danh sách.",
     "1. Để trống Danh sách, bấm \"Tạo nhắc việc\".",
     "Danh sách: -- Chọn danh sách --",
     "- Hiện lỗi đỏ \"Vui lòng chọn danh sách\" ngay dưới ô Danh sách, popup không đóng."),
    (4, "Cả 2 lỗi Tiêu đề và Danh sách hiện đồng thời", "P0",
     "Đang mở popup Tạo nhắc việc, cả Tiêu đề và Danh sách đều để trống.",
     "1. Bấm \"Tạo nhắc việc\" khi cả 2 ô đang trống.",
     "—",
     "- Hiện ĐỒNG THỜI cả 2 lỗi: \"Tiêu đề không được để trống\" và \"Vui lòng chọn danh sách\" — "
     "không bắt sửa từng ô một."),
    (5, "Bước bị xoá trắng chữ báo lỗi riêng", "P1",
     "Đã thêm 1 bước \"Gọi khách hàng\" rồi xoá hết chữ trong ô bước đó nhưng chưa xoá cả dòng "
     "bước.",
     "1. Xoá trắng nội dung của bước đã thêm, bấm \"Tạo nhắc việc\".",
     "—",
     "- Hiện lỗi \"Nội dung bước không được để trống\"."),
    (6, "Nội dung đang gõ dở ở ô Thêm bước vẫn được tính khi bấm Lưu", "P1",
     "Đang gõ \"Chuẩn bị tài liệu\" vào ô \"Thêm bước…\" nhưng CHƯA bấm Enter để thêm vào danh "
     "sách.",
     "1. Nhập đủ Tiêu đề, chọn Danh sách.\n"
     "2. Gõ \"Chuẩn bị tài liệu\" vào ô Thêm bước, KHÔNG bấm Enter.\n"
     "3. Bấm \"Tạo nhắc việc\" luôn.",
     "Ô thêm bước đang gõ dở: Chuẩn bị tài liệu",
     "- Nội dung đang gõ dở vẫn được ghi nhận thành 1 bước con của nhắc việc mới, KHÔNG bị mất."),
    (7, "Bấm \"Lưu và tiếp tục\" giữ popup mở để tạo tiếp", "P1",
     "Đang mở popup Tạo nhắc việc, đã nhập đủ Tiêu đề + Danh sách hợp lệ.",
     "1. Bấm \"Lưu và tiếp tục\".",
     "—",
     "- Ghi nhắc việc thành công, hiện thông báo tạo thành công.\n"
     "- Popup VẪN MỞ, toàn bộ ô được xoá trắng, con trỏ focus quay lại ô Tiêu đề để nhập tiếp."),
    (8, "Nút \"Lưu và tiếp tục\" chỉ có ở màn Tạo mới, không có ở màn Sửa", "P1",
     "Có sẵn 1 nhắc việc cá nhân.",
     "1. Mở popup Tạo nhắc việc mới, quan sát các nút.\n"
     "2. Đóng popup, bấm vào dòng nhắc việc có sẵn để mở popup Sửa, quan sát các nút.",
     "—",
     "- Popup Tạo mới: có 3 nút Tạo nhắc việc / Lưu và tiếp tục / Đóng.\n"
     "- Popup Sửa: chỉ có 2 nút Lưu / Đóng — KHÔNG có \"Lưu và tiếp tục\"."),
    (9, "Sửa nhắc việc điền sẵn đúng dữ liệu hiện có", "P0",
     "Nhắc việc \"Kiểm tra kho\" có Mô tả \"Kiểm hàng tồn quý 3\", 1 bước \"Đếm hàng\", Danh sách "
     "\"Mặc định\", Ngày hạn 18/09/2026.",
     "1. Bấm vào thân dòng nhắc việc \"Kiểm tra kho\".",
     "—",
     "- Popup \"Chỉnh sửa nhắc việc cá nhân\" mở ra, điền sẵn đúng Tiêu đề, Mô tả, bước \"Đếm "
     "hàng\", Danh sách \"Mặc định\", Ngày hạn 18/09/2026."),
    (10, "Đổi Danh sách khi sửa chuyển nhắc việc sang danh sách mới", "P1",
     "Nhắc việc \"Kiểm tra kho\" đang thuộc danh sách \"Mặc định\".",
     "1. Mở popup Sửa, đổi Danh sách sang \"Công việc tuần\", bấm Lưu.\n"
     "2. Mở lại cột danh sách cá nhân, kiểm tra danh sách \"Mặc định\" và \"Công việc tuần\".",
     "Danh sách mới: Công việc tuần",
     "- Nhắc việc \"Kiểm tra kho\" không còn trong danh sách \"Mặc định\", đã chuyển hẳn sang "
     "\"Công việc tuần\"."),
    (11, "Bấm Enter ở ô Thêm bước thêm 1 bước và xoá trắng ô nhập", "P2",
     "Đang mở popup Tạo/Sửa nhắc việc, ô Thêm bước đang trống.",
     "1. Gõ \"Xác nhận với khách\" vào ô Thêm bước, bấm Enter.",
     "—",
     "- Thêm dòng bước mới \"Xác nhận với khách\" vào danh sách bước phía trên.\n"
     "- Ô Thêm bước trở về trống để gõ bước tiếp theo."),
    (12, "Khoá nút Tạo/Lưu trong lúc đang gửi để tránh tạo trùng", "P2",
     "Đang mở popup Tạo nhắc việc với dữ liệu hợp lệ.",
     "1. Bấm \"Tạo nhắc việc\", ngay lập tức bấm thêm lần nữa trong lúc đang xử lý.",
     "—",
     "- Nút bị khoá ngay sau lần bấm đầu tiên cho tới khi xử lý xong, không tạo ra 2 nhắc việc "
     "trùng nhau."),
]))

# -------------------------------------------------------------------- VIII
SECTIONS.append(("VIII", "QUẢN LÝ DANH SÁCH CÁ NHÂN", [
    (1, "Tạo danh sách cá nhân mới", "P0",
     "Đã có sẵn danh sách \"Mặc định\".",
     "1. Bấm \"+ Tạo danh sách mới\" ở cột phải.\n"
     "2. Nhập Tên danh sách \"Ý tưởng cải tiến\", Mô tả \"Ghi nhanh ý tưởng khi họp\".\n"
     "3. Bấm Lưu.",
     "Tên danh sách: Ý tưởng cải tiến",
     "- Hiện thông báo \"Đã tạo danh sách\".\n"
     "- Danh sách mới \"Ý tưởng cải tiến\" xuất hiện ở cột phải, cạnh \"Mặc định\"."),
    (2, "Bỏ trống Tên danh sách báo lỗi, không đóng popup", "P0",
     "Đang mở popup Tạo danh sách.",
     "1. Để trống Tên danh sách, bấm Lưu.",
     "Tên danh sách: (trống)",
     "- Hiện lỗi đỏ \"Tên danh sách không được để trống\", popup không đóng."),
    (3, "Ô Tên danh sách giữ đúng dấu cách khi gõ tiếng Việt", "P1",
     "Đang mở popup Tạo danh sách.",
     "1. Gõ chậm từng chữ \"Công việc tuần\" vào ô Tên danh sách, đặc biệt gõ dấu cách giữa các "
     "từ bằng bộ gõ tiếng Việt (không dán nguyên cụm).",
     "Tên danh sách: Công việc tuần",
     "- ⚠️ Ô giữ đúng dấu cách giữa \"Công\", \"việc\", \"tuần\" — không bị dính liền thành \"Công "
     "việctuần\" (ô này không dùng cắt khoảng trắng khi đang gõ)."),
    (4, "Sửa tên/mô tả danh sách", "P1",
     "Danh sách \"Ý tưởng cải tiến\" đang có Mô tả \"Ghi nhanh ý tưởng khi họp\".",
     "1. Mở màn xem riêng danh sách này, bấm \"Sửa\".\n"
     "2. Đổi Mô tả thành \"Ghi ý tưởng và phân loại theo phòng ban\", bấm Lưu.",
     "Mô tả mới: Ghi ý tưởng và phân loại theo phòng ban",
     "- Hiện thông báo \"Đã cập nhật danh sách\", mô tả hiển thị đúng nội dung mới."),
    (5, "Xoá danh sách yêu cầu xác nhận, nêu rõ việc bên trong cũng bị xoá", "P0",
     "Danh sách \"Ý tưởng cải tiến\" đang có 3 nhắc việc bên trong.",
     "1. Mở màn xem riêng danh sách này, bấm \"Xoá\".",
     "—",
     "- Hiện hộp xác nhận nêu rõ \"Tất cả việc trong danh sách sẽ bị xoá\" trước khi xoá thật.\n"
     "- Bấm xác nhận: xoá cả danh sách và toàn bộ 3 nhắc việc bên trong, hiện \"Đã xoá danh "
     "sách\", quay về màn danh sách chính."),
    (6, "Huỷ hộp xác nhận xoá thì không mất dữ liệu", "P1",
     "Danh sách \"Ý tưởng cải tiến\" đang có 3 nhắc việc.",
     "1. Bấm \"Xoá\", ở hộp xác nhận bấm Huỷ/đóng hộp.",
     "—",
     "- Danh sách và 3 nhắc việc bên trong vẫn còn nguyên, không có gì bị xoá."),
    (7, "Kéo-thả biểu tượng ⋮⋮ đổi thứ tự danh sách", "P2",
     "Cột phải đang hiện thứ tự: Mặc định, Công việc tuần, Ý tưởng cải tiến.",
     "1. Kéo-thả \"Ý tưởng cải tiến\" lên vị trí đầu tiên.",
     "—",
     "- Thứ tự hiển thị đổi ngay trên màn thành: Ý tưởng cải tiến, Mặc định, Công việc tuần.\n"
     "- Tải lại trang: thứ tự mới vẫn được giữ nguyên (đã lưu xuống máy chủ)."),
    (8, "Kéo-thả lỗi lưu thì tải lại đúng thứ tự cũ và báo lỗi", "P2",
     "Đang kéo-thả đổi thứ tự danh sách trong lúc mất kết nối mạng.",
     "1. Kéo-thả đổi vị trí 2 danh sách trong lúc mạng bị chặn.",
     "—",
     "- Thứ tự tự động tải lại về đúng thứ tự cũ trên máy chủ.\n"
     "- Hiện thông báo \"Không thể sắp xếp danh sách\"."),
    (9, "Bấm tên danh sách mở màn xem riêng đúng nội dung", "P0",
     "Danh sách \"Công việc tuần\" có 4 nhắc việc chưa xong, 2 nhắc việc đã xong.",
     "1. Bấm vào tên \"Công việc tuần\" ở cột phải.",
     "—",
     "- Mở màn xem riêng: breadcrumb \"Lịch làm việc của tôi > Công việc tuần\", số việc/số hoàn "
     "thành đúng 4/6 (hoặc hiển thị tương ứng), danh sách 4 việc chưa xong trước rồi tới khối \"Đã "
     "hoàn thành\" (2 việc)."),
    (10, "Bấm breadcrumb quay lại danh sách gộp", "P1",
     "Đang ở màn xem riêng \"Công việc tuần\".",
     "1. Bấm phần đầu breadcrumb \"Lịch làm việc của tôi\".",
     "—",
     "- Đóng màn xem riêng, quay về danh sách gộp 6 nguồn, tải lại dữ liệu."),
    (11, "Ô Thêm việc mới tạo nhanh 1 nhắc việc, không mở popup đầy đủ", "P1",
     "Đang ở màn xem riêng \"Công việc tuần\".",
     "1. Gõ \"Gọi lại khách A\" vào ô \"Thêm việc mới…\", bấm Enter.",
     "—",
     "- Tạo ngay 1 nhắc việc \"Gọi lại khách A\" thuộc thẳng danh sách \"Công việc tuần\" (không "
     "có Mô tả/Ngày hạn vì tạo kiểu nhanh), ô nhập xoá trắng, danh sách tải lại."),
    (12, "Enter khi ô Thêm việc mới đang trống thì không gửi, không báo lỗi", "P2",
     "Đang ở màn xem riêng bất kỳ, ô \"Thêm việc mới…\" đang trống.",
     "1. Bấm Enter khi ô đang trống.",
     "—",
     "- Không có gì xảy ra: không gọi tạo mới, không báo lỗi."),
    (13, "Thêm bước con ngay trong màn xem danh sách", "P2",
     "Nhắc việc \"Gọi lại khách A\" đang không có bước con nào, đang ở màn xem riêng danh sách.",
     "1. Gõ \"Xác nhận lịch hẹn\" vào ô thêm bước con của đúng dòng \"Gọi lại khách A\", bấm Enter.",
     "—",
     "- Thêm đúng 1 bước con \"Xác nhận lịch hẹn\" cho dòng \"Gọi lại khách A\", không ảnh hưởng "
     "các dòng khác."),
    (14, "Chưa có việc nào trong danh sách hiện đúng thông báo", "P2",
     "Danh sách \"Ý tưởng cải tiến\" vừa tạo, chưa có nhắc việc nào.",
     "1. Mở màn xem riêng danh sách này.",
     "—",
     "- Hiện dòng chữ \"Chưa có việc gì\" kèm icon minh hoạ."),
]))

# -------------------------------------------------------------------- IX
SECTIONS.append(("IX", "XEM LỊCH LÀM VIỆC — LƯỚI THÁNG/TUẦN", [
    (1, "Lưới Tháng luôn vẽ đủ 42 ô, ngày liền kề hiện mờ", "P0",
     "Tháng 9/2026 bắt đầu từ Thứ Ba — cần thêm ô của cuối tháng 8 để đủ hàng đầu, và ô đầu tháng "
     "10 để đủ 6 hàng.",
     "1. Vào tab Lịch làm việc, chế độ Tháng, xem tháng 9/2026.\n"
     "2. Đếm tổng số ô trên lưới.",
     "—",
     "- Lưới có đúng 42 ô (6 hàng × 7 cột).\n"
     "- Các ngày cuối tháng 8 và đầu tháng 10 hiện mờ hơn để phân biệt với ngày thuộc tháng 9, "
     "nhưng vẫn bấm được để tạo mới."),
    (2, "Mỗi ô Tháng tối đa 3 thẻ, dư ra gộp vào \"+N khác\"", "P1",
     "Ngày 15/09/2026 có 5 việc đến hạn.",
     "1. Quan sát ô ngày 15/09/2026 trên lưới Tháng.",
     "—",
     "- Ô vẽ trực tiếp 3 thẻ đầu, kèm nút \"+2 khác\" cho 2 việc còn lại."),
    (3, "Chuyển sang chế độ Tuần hiện hàng Cả ngày + lưới giờ", "P0",
     "Tuần 07–13/09/2026 có 1 việc Cả ngày và nhiều việc có giờ cụ thể.",
     "1. Bấm nút \"Tuần\".",
     "—",
     "- Hiện hàng \"Cả ngày\" cố định phía trên, việc không có giờ cụ thể nằm ở hàng này.\n"
     "- Bên dưới là lưới giờ 24 hàng (0h–23h), mỗi ô là khoảng 1 giờ của 1 ngày, cuộn được."),
    (4, "Nút lùi/tiến kỳ đúng bước nhảy theo từng chế độ", "P1",
     "Đang xem Tháng 9/2026 ở chế độ Tháng.",
     "1. Bấm mũi tên tiến kỳ, quan sát nhãn kỳ.\n"
     "2. Chuyển sang chế độ Tuần, bấm mũi tên tiến kỳ, quan sát nhãn kỳ.",
     "—",
     "- Chế độ Tháng: nhãn chuyển thành \"Tháng 10/2026\" (lùi/tiến đúng 1 tháng).\n"
     "- Chế độ Tuần: nhãn chuyển sang đúng 7 ngày kế tiếp (lùi/tiến đúng 7 ngày)."),
    (5, "Nút \"Hôm nay\" đưa lịch về đúng kỳ chứa ngày hiện tại", "P1",
     "Đang xem tháng 12/2026 (đã lùi/tiến xa), hôm nay là 11/09/2026.",
     "1. Bấm nút \"Hôm nay\".",
     "—",
     "- Lịch quay về đúng kỳ chứa ngày 11/09/2026 (Tháng 9/2026)."),
    (6, "Việc nhiều ngày vẽ thành thanh trải ngang, cắt đúng biên tuần", "P0",
     "Phiếu công tác \"PCT-020\" có thời gian từ 10/09/2026 đến 16/09/2026 (trải qua 2 tuần).",
     "1. Xem chế độ Tuần của tuần 07–13/09 và tuần 14–20/09.",
     "Phiếu công tác PCT-020: 10/09 → 16/09/2026",
     "- Tuần 07–13/09: thanh trải từ ngày 10 đến hết ngày 13, có dấu hiệu (mũi tên) cho biết còn "
     "tràn sang tuần sau.\n"
     "- Tuần 14–20/09: thanh tiếp tục từ ngày 14 đến 16, cắt đúng biên tuần, không vẽ lố sang ngày "
     "17."),
    (7, "Việc nhiều ngày hiện ở mọi ngày trong khoảng, không chỉ ngày bắt đầu", "P0",
     "Phiếu công tác \"PCT-021\": 12/09 → 14/09/2026.",
     "1. Quan sát lưới Tháng ở các ngày 12, 13, 14/09/2026.",
     "—",
     "- Thanh của PCT-021 xuất hiện ở cả 3 ngày 12, 13, 14 — không chỉ hiện ở ngày bắt đầu (12)."),
    (8, "Dữ liệu bẩn: ngày kết thúc trước ngày bắt đầu thì coi end = start, không vẽ thanh âm", "P2",
     "1 việc có dữ liệu lỗi: ngày kết thúc 08/09/2026 sớm hơn ngày bắt đầu 10/09/2026.",
     "1. Quan sát việc này trên lưới Tháng/Tuần.",
     "Ngày bắt đầu: 10/09 | Ngày kết thúc (lỗi): 08/09",
     "- Hệ thống coi ngày kết thúc = ngày bắt đầu (10/09), vẽ đúng 1 ô ngày 10/09, KHÔNG vẽ thanh "
     "chạy ngược hay gây lỗi hiển thị."),
    (9, "Việc chưa có hạn không lên lịch, dù vẫn còn ở tab danh sách", "P0",
     "Task \"Việc chưa gán hạn\" không có ngày bắt đầu/hạn.",
     "1. Ở tab danh sách, xác nhận Task này nằm ở nhóm \"Không hạn\".\n"
     "2. Chuyển qua tab Lịch làm việc, dò khắp lưới Tháng và Tuần.",
     "—",
     "- Task \"Việc chưa gán hạn\" KHÔNG xuất hiện ở bất kỳ ô nào trên lịch."),
    (10, "Tab lịch hiện mọi trạng thái, kể cả chưa duyệt/đã xong/đã huỷ", "P0",
     "Phiếu giao việc \"PGV-030\" đang ở trạng thái \"Chờ duyệt\" (chưa duyệt); Meeting \"Họp Z\" "
     "đã Huỷ.",
     "1. Ở tab danh sách với Trạng thái = Tất cả, tìm PGV-030 và Họp Z.\n"
     "2. Chuyển sang tab Lịch làm việc, tìm đúng ngày hạn của cả 2.",
     "—",
     "- Tab danh sách: KHÔNG thấy cả 2 (bị lọc bỏ vì chưa duyệt/đã huỷ).\n"
     "- Tab lịch: THẤY cả 2, vẽ đúng thẻ (Họp Z hiện mờ + gạch ngang vì đã Huỷ)."),
    (11, "Việc Đã xong/Dừng-Huỷ làm mờ thẻ", "P1",
     "Issue \"Đã đóng ticket X\" ở trạng thái \"Đã đóng\" (nhóm Đã xong).",
     "1. Quan sát thẻ Issue này trên lưới.",
     "—",
     "- Thẻ hiện mờ hơn (giảm độ đậm) so với các thẻ đang mở."),
    (12, "Chỉ trạng thái kết thúc hẳn mới gạch ngang tiêu đề", "P0",
     "Task \"Task bị huỷ\" ở trạng thái Huỷ; Task \"Task tạm dừng\" ở trạng thái Tạm dừng.",
     "1. Quan sát 2 thẻ Task trên lưới.",
     "Task bị huỷ: trạng thái Huỷ | Task tạm dừng: trạng thái Tạm dừng",
     "- \"Task bị huỷ\": mờ VÀ gạch ngang tiêu đề (Huỷ thuộc nhóm kết thúc hẳn).\n"
     "- ⚠️ \"Task tạm dừng\": CHỈ mờ, KHÔNG gạch ngang tiêu đề — vì Tạm dừng còn chạy tiếp được, "
     "không phải trạng thái kết thúc hẳn."),
    (13, "Badge đỏ \"Quá hạn\" hiện đúng điều kiện trên thẻ lịch", "P1",
     "Task \"Task trễ hạn\" hạn hôm qua, còn ở trạng thái Đang làm.",
     "1. Quan sát thẻ Task này trên lưới.",
     "—",
     "- Thẻ có badge đỏ \"Quá hạn\"."),
    (14, "Vòng quay chờ hiện khi tải lại theo kỳ hoặc bộ lọc mới", "P2",
     "Đang xem Tháng 9/2026.",
     "1. Bấm mũi tên tiến kỳ sang Tháng 10/2026, quan sát ngay khoảnh khắc chuyển.",
     "—",
     "- Hiện vòng quay chờ trong lúc tải dữ liệu tháng mới, biến mất khi tải xong."),
]))

# -------------------------------------------------------------------- X
SECTIONS.append(("X", "TẠO MỚI TỪ TAB LỊCH LÀM VIỆC", [
    (1, "Bấm nút \"Tạo mới\" trên thanh công cụ mở menu 5 loại, không ngày điền sẵn", "P0",
     "Đang ở tab Lịch làm việc.",
     "1. Bấm nút \"Tạo mới\" trên thanh công cụ.",
     "—",
     "- Mở menu đúng 5 loại theo thứ tự: Task, Issue, Nhắc việc cá nhân, Meeting, Phiếu giao "
     "việc.\n"
     "- KHÔNG có dòng ngày/giờ điền sẵn trong menu.\n"
     "- ⚠️ KHÔNG có lựa chọn \"Phiếu công tác\" — loại này chỉ lập được từ phiếu đề xuất công tác "
     "đã duyệt, không tạo trực tiếp tại đây."),
    (2, "Bấm ô ngày trống trên lưới Tháng mở menu kèm ngày điền sẵn", "P0",
     "Đang xem lưới Tháng, ô ngày 22/09/2026 đang trống (không có thẻ nào).",
     "1. Bấm vào vùng trống của ô ngày 22/09/2026.",
     "—",
     "- Mở menu 5 loại, có thêm dòng hiển thị ngày 22/09/2026 đã điền sẵn.\n"
     "- KHÔNG có giờ điền sẵn (ô lưới Tháng không có khái niệm giờ)."),
    (3, "Bấm ô giờ cụ thể trên lưới Tuần mở menu kèm cả ngày và giờ", "P1",
     "Đang xem lưới Tuần, ô giờ 14:00 ngày 23/09/2026 đang trống.",
     "1. Bấm vào ô giờ 14:00 ngày 23/09/2026.",
     "—",
     "- Mở menu 5 loại, dòng ngày/giờ điền sẵn hiện đúng dạng \"23/09/2026 — 14:00\"."),
    (4, "Chọn Task/Issue/Nhắc việc cá nhân mở popup tại chỗ, có ngày điền sẵn", "P0",
     "Đang mở menu Tạo mới từ ô ngày 22/09/2026 (tiếp nối TC X.2).",
     "1. Chọn \"Task\" trong menu.",
     "—",
     "- Đóng menu, mở đúng popup tạo mới Task tại màn hiện tại (không rời khỏi màn Lịch làm "
     "việc).\n"
     "- Ngày hạn trong popup được điền sẵn 22/09/2026."),
    (5, "Chọn Meeting/Phiếu giao việc chuyển hẳn sang trang tạo mới tương ứng", "P0",
     "Đang mở menu Tạo mới bất kỳ.",
     "1. Chọn \"Meeting\" trong menu.\n"
     "2. Quay lại tab Lịch làm việc, mở lại menu Tạo mới, chọn \"Phiếu giao việc\".",
     "—",
     "- Chọn \"Meeting\": rời khỏi màn Lịch làm việc, chuyển sang trang \"Tạo Meeting\".\n"
     "- Chọn \"Phiếu giao việc\": rời khỏi màn, chuyển sang trang \"Tạo phiếu giao việc\" — cả 2 "
     "loại này KHÔNG mở popup tại chỗ."),
    (6, "Lưu Task/Issue/Nhắc việc từ menu tạo mới tải lại cả 2 tab", "P1",
     "Vừa tạo 1 Task mới từ menu \"Tạo mới\" ở tab Lịch làm việc, có hạn hôm nay.",
     "1. Lưu Task mới thành công.\n"
     "2. Quan sát tab Lịch làm việc rồi chuyển qua tab Công việc của tôi.",
     "—",
     "- Task mới xuất hiện đúng ô ngày trên lịch NGAY sau khi lưu.\n"
     "- Chuyển sang tab danh sách, Task mới cũng đã có trong nhóm \"Hôm nay\", 4 thẻ thống kê cập "
     "nhật theo."),
]))

# -------------------------------------------------------------------- XI
SECTIONS.append(("XI", "XEM ĐỦ VIỆC TRONG NGÀY QUA \"+N KHÁC\"", [
    (1, "Bấm \"+N khác\" mở popover liệt kê đủ N việc còn lại", "P0",
     "Ngày 15/09/2026 có 5 việc, lưới Tháng vẽ 3 thẻ và nút \"+2 khác\".",
     "1. Bấm nút \"+2 khác\" ở ô ngày 15/09/2026.",
     "—",
     "- Mở popover cạnh ô ngày, liệt kê đủ cả 5 việc của ngày 15/09/2026 (không chỉ 2 việc dư), "
     "mỗi việc vẽ dạng thẻ giống hệt thẻ trên lưới chính."),
    (2, "Tiêu đề popover ghi cứng chữ \"Meeting\" dù nội dung là loại khác", "P2",
     "Ngày 11/09/2026 có 5 việc gồm cả Task, Issue (không phải toàn Meeting).",
     "1. Bấm \"+N khác\" ở ô ngày 11/09/2026, đọc tiêu đề popover.",
     "—",
     "- ⚠️ Tiêu đề vẫn ghi dạng \"Meeting ngày 11/09/2026 (5)\" dù bên trong có cả Task/Issue — đây "
     "là hạn chế đã biết của nhãn hiển thị, KHÔNG phải lỗi hiển thị sai loại việc bên trong "
     "popover."),
    (3, "Bấm ra ngoài đóng popover, không đổi gì khác", "P2",
     "Popover \"+N khác\" đang mở.",
     "1. Bấm vào vùng trống ngoài popover.",
     "—",
     "- Popover đóng lại, lưới lịch không có gì thay đổi khác."),
    (4, "Bấm 1 thẻ trong popover đóng popover rồi mở đúng chi tiết", "P0",
     "Popover đang mở, có 1 thẻ Meeting \"Họp Y\" bên trong.",
     "1. Bấm vào thẻ \"Họp Y\" trong popover.",
     "—",
     "- Popover đóng lại TRƯỚC, sau đó mở panel chi tiết Meeting \"Họp Y\"."),
    (5, "Popover tự lật vị trí nếu tràn màn hình", "P2",
     "Ô ngày cuối lưới (hàng cuối cùng) có nhiều hơn 3 việc, popover mặc định mở phía dưới sẽ tràn "
     "khỏi màn hình.",
     "1. Bấm \"+N khác\" ở ô ngày thuộc hàng cuối cùng của lưới.",
     "—",
     "- Popover tự lật lên trên hoặc kéo vào trong để không bị tràn/khuất khỏi màn hình."),
    (6, "Đang mở menu Tạo mới mà bấm \"+N khác\" ô khác thì đóng menu trước", "P2",
     "Menu \"Tạo mới\" (mở từ 1 ô ngày) đang hiện trên màn.",
     "1. Trong lúc menu đang mở, bấm nút \"+N khác\" của 1 ô ngày khác.",
     "—",
     "- Menu \"Tạo mới\" đóng lại trước, sau đó popover \"+N khác\" mới mở ra."),
]))

# -------------------------------------------------------------------- XII
SECTIONS.append(("XII", "XEM CHI TIẾT CÔNG VIỆC TỪ LỊCH", [
    (1, "Bấm thẻ Meeting/Phiếu công tác/Phiếu giao việc trên lưới mở panel dùng chung với tab danh sách", "P0",
     "Lưới đang hiện thẻ Phiếu công tác \"PCT-020\".",
     "1. Bấm vào thẻ \"PCT-020\" trên lưới.",
     "—",
     "- Mở panel chi tiết giống hệt cơ chế ở tab danh sách (FR-03): header nền theo loại, nút "
     "\"Mở chi tiết\"."),
    (2, "Bấm thẻ Task/Issue/Nhắc việc cá nhân mở đúng popup sẵn có", "P0",
     "Lưới đang hiện thẻ Task \"Task hạn hôm nay\".",
     "1. Bấm vào thẻ Task này.",
     "—",
     "- Mở popup \"Chi tiết Task\", giống hệt cách mở từ tab danh sách."),
    (3, "Toàn bộ diện tích thẻ bấm được kể cả khi đang mờ", "P2",
     "Thẻ Task \"Task đã xong\" đang hiện mờ (do trạng thái Hoàn thành).",
     "1. Bấm vào bất kỳ vị trí nào trên thẻ mờ này (kể cả sát mép).",
     "—",
     "- Vẫn mở đúng popup chi tiết Task, thẻ mờ không cản trở việc bấm."),
    (4, "Đang mở panel của thẻ này, bấm thẻ khác thì thay nội dung, không mở thêm", "P1",
     "Panel chi tiết Meeting \"Họp A\" (mở từ lưới) đang hiển thị.",
     "1. Bấm sang thẻ Phiếu giao việc \"PGV-011\" trên lưới.",
     "—",
     "- Panel đổi nội dung sang \"PGV-011\", không mở thêm panel thứ hai."),
    (5, "Bấm thẻ trong popover \"+N khác\" đóng popover trước khi mở chi tiết", "P1",
     "Popover \"+N khác\" của ngày 11/09/2026 đang mở, có thẻ Issue \"Issue Z\" bên trong.",
     "1. Bấm vào thẻ \"Issue Z\" trong popover.",
     "—",
     "- Popover đóng lại trước, sau đó mở đúng popup \"Chi tiết Issue\" của \"Issue Z\"."),
]))

# -------------------------------------------------------------------- XIII
SECTIONS.append(("XIII", "RÀNG BUỘC NHẬP LIỆU", [
    (1, "Tiêu đề nhắc việc giới hạn 0–255 ký tự", "P2",
     "Đang mở popup Tạo nhắc việc.",
     "1. Nhập Tiêu đề dài 256 ký tự, chọn Danh sách hợp lệ, bấm Tạo.",
     "Tiêu đề: chuỗi 256 ký tự",
     "- Hệ thống báo lỗi độ dài vượt quá cho phép ngay dưới ô Tiêu đề, KHÔNG tự cắt bớt chữ đã "
     "nhập, không tạo được nhắc việc."),
    (2, "Mô tả nhắc việc giới hạn 0–2000 ký tự", "P2",
     "Đang mở popup Tạo nhắc việc, đã nhập Tiêu đề và Danh sách hợp lệ.",
     "1. Nhập Mô tả dài 2001 ký tự, bấm Tạo.",
     "Mô tả: chuỗi 2001 ký tự",
     "- Báo lỗi vượt quá độ dài cho phép, giữ nguyên nội dung đã gõ, không tạo được nhắc việc."),
    (3, "Mỗi bước giới hạn 0–255 ký tự", "P2",
     "Đang mở popup Tạo nhắc việc, đã nhập Tiêu đề và Danh sách hợp lệ.",
     "1. Gõ vào ô Thêm bước 1 chuỗi 256 ký tự, bấm Enter.",
     "Nội dung bước: chuỗi 256 ký tự",
     "- Báo lỗi độ dài vượt quá cho phép, không thêm được bước này vào danh sách."),
    (4, "Tên danh sách giới hạn 0–255 ký tự, Mô tả danh sách giới hạn 0–1000 ký tự", "P2",
     "Đang mở popup Tạo danh sách.",
     "1. Nhập Tên danh sách dài 256 ký tự, bấm Lưu.\n"
     "2. Sửa lại Tên hợp lệ, nhập Mô tả dài 1001 ký tự, bấm Lưu.",
     "Tên: chuỗi 256 ký tự | Mô tả: chuỗi 1001 ký tự",
     "- Cả 2 trường hợp đều báo lỗi vượt quá độ dài cho phép đúng ô tương ứng, không lưu được."),
    (5, "Ngày hạn và Giờ hạn cùng quyết định việc có \"Cả ngày\" trên lịch hay không", "P1",
     "Tạo nhắc việc A chỉ chọn Ngày hạn, để trống Giờ hạn. Tạo nhắc việc B chọn cả Ngày hạn và Giờ "
     "hạn 09:00.",
     "1. Tạo nhắc việc A và B như trên, xem cả 2 trên lưới Tuần.",
     "A: chỉ Ngày hạn | B: Ngày hạn + Giờ hạn 09:00",
     "- Nhắc việc A hiện ở hàng \"Cả ngày\".\n"
     "- Nhắc việc B hiện đúng ô giờ 09:00 trong lưới giờ."),
    (6, "Khoá nút Lưu trong lúc đang lưu ở popup Sửa nhắc việc", "P2",
     "Đang mở popup Sửa nhắc việc với dữ liệu hợp lệ.",
     "1. Bấm Lưu, ngay lập tức bấm thêm lần nữa trong lúc đang xử lý.",
     "—",
     "- Nút Lưu bị khoá sau lần bấm đầu, không gửi 2 yêu cầu cập nhật trùng nhau."),
]))

# -------------------------------------------------------------------- XIV
SECTIONS.append(("XIV", "CÔ LẬP DỮ LIỆU & ĐỒNG BỘ GIỮA 2 TAB", [
    (1, "Tạo nhắc việc ở tab danh sách cập nhật ngay sang tab lịch", "P0",
     "Đang ở tab \"Công việc của tôi\", chưa có việc nào hạn 25/09/2026.",
     "1. Tạo nhắc việc mới với Ngày hạn 25/09/2026.\n"
     "2. Chuyển sang tab Lịch làm việc, xem ô ngày 25/09/2026.",
     "Ngày hạn: 25/09/2026",
     "- Nhắc việc mới xuất hiện đúng ô ngày 25/09/2026 trên lịch mà không cần tải lại thủ công."),
    (2, "Sửa/xoá nhắc việc ở màn xem danh sách cá nhân cũng đồng bộ sang lịch", "P1",
     "Nhắc việc \"Gọi lại khách A\" (thuộc danh sách \"Công việc tuần\") đang có hạn 25/09/2026, "
     "đã hiện trên lịch.",
     "1. Ở màn xem riêng danh sách, sửa hạn của nhắc việc thành 28/09/2026.\n"
     "2. Kiểm tra ô ngày 25/09 và 28/09 trên lịch.",
     "Hạn cũ: 25/09 | Hạn mới: 28/09",
     "- Ô ngày 25/09 không còn thẻ này; ô ngày 28/09 xuất hiện đúng thẻ đã sửa."),
    (3, "Việc của tài khoản khác không rò rỉ vào bất kỳ khối nào của màn (danh sách, lịch, lịch mini, thẻ thống kê)", "P0",
     "Tài khoản A có 6 việc trong tháng; tài khoản B có 4 việc khác, không giao nhau với A.",
     "1. Đăng nhập tài khoản A, ghi nhận Tổng việc = 6, đếm chấm trên lịch mini, đếm số trên 6 "
     "chip ở tab lịch.\n"
     "2. Đăng nhập tài khoản B, ghi nhận lại toàn bộ các số liệu tương tự.",
     "Tài khoản A: 6 việc | Tài khoản B: 4 việc (khác nhau hoàn toàn)",
     "- Số liệu và danh sách của tài khoản A và B tách biệt hoàn toàn ở MỌI khối trên màn (4 thẻ "
     "thống kê, danh sách theo nhóm, lịch mini, 6 chip loại, lưới Tháng/Tuần) — không việc nào của "
     "A lọt sang B hay ngược lại."),
    (4, "Xoá danh sách cá nhân không ảnh hưởng nhắc việc của danh sách khác", "P1",
     "Có 2 danh sách: \"Mặc định\" (2 việc) và \"Công việc tuần\" (3 việc).",
     "1. Xoá danh sách \"Công việc tuần\".\n"
     "2. Kiểm tra danh sách \"Mặc định\".",
     "—",
     "- Chỉ 3 việc thuộc \"Công việc tuần\" bị xoá.\n"
     "- 2 việc thuộc \"Mặc định\" còn nguyên, không bị ảnh hưởng."),
]))

# -------------------------------------------------------------------- XV
SECTIONS.append(("XV", "LUỒNG NGHIỆP VỤ ĐẦU CUỐI (E2E)", [
    (1, "Luồng đầy đủ: tạo nhắc việc → xuất hiện đúng chỗ ở cả 2 tab → tick hoàn thành → biến mất khỏi bộ lọc Chưa xong", "P0",
     "Trạng thái đang lọc ở tab danh sách = \"Chưa xong\" (mặc định). Chưa có việc nào hạn hôm "
     "nay.",
     "1. Bấm \"Tạo nhắc việc cá nhân\", nhập Tiêu đề \"Duyệt hồ sơ ứng viên\", chọn Danh sách "
     "\"Mặc định\", Ngày hạn = hôm nay, bấm Tạo.\n"
     "2. Ở tab danh sách, xác nhận việc mới nằm ở nhóm \"Hôm nay\" và \"Tuần này\", thẻ \"Hôm "
     "nay\" tăng thêm 1.\n"
     "3. Chuyển tab Lịch làm việc, xác nhận thẻ việc xuất hiện đúng ô ngày hôm nay.\n"
     "4. Quay lại tab danh sách, tích hoàn thành nhắc việc vừa tạo, xác nhận Hoàn thành trong hộp "
     "thoại.\n"
     "5. Quan sát danh sách đang lọc Trạng thái = Chưa xong.",
     "Tiêu đề: Duyệt hồ sơ ứng viên | Ngày hạn: hôm nay",
     "- Bước 2: việc mới hiện đúng ở 2 nhóm nói trên, đúng theo nhóm bao trùm.\n"
     "- Bước 3: thẻ việc hiện đúng ngày hôm nay trên lịch, màu theo loại Nhắc việc cá nhân.\n"
     "- Bước 4-5: sau khi hoàn thành, dòng mờ dần rồi trượt khỏi danh sách (đang lọc Chưa xong); "
     "quay lại tab lịch, thẻ này hiện mờ vì đã chuyển nhóm Hoàn thành."),
    (2, "Luồng đầy đủ: tạo từ ô ngày trên lịch → xuất hiện ở tab danh sách đúng nhóm theo hạn", "P0",
     "Đang ở tab Lịch làm việc, chế độ Tháng, ô ngày 30/09/2026 đang trống (thuộc nhóm \"Sau đó\" "
     "so với hôm nay 11/09/2026).",
     "1. Bấm vào ô ngày 30/09/2026, chọn \"Task\" trong menu Tạo mới.\n"
     "2. Điền Tên Task \"Tổng kết tháng 9\", lưu lại (ngày hạn đã điền sẵn 30/09/2026).\n"
     "3. Chuyển sang tab \"Công việc của tôi\", mở nhóm \"Sau đó\".",
     "Ngày hạn: 30/09/2026 (hôm nay 11/09/2026)",
     "- Task \"Tổng kết tháng 9\" xuất hiện đúng nhóm \"Sau đó\" ở tab danh sách, không lọt vào "
     "nhóm nào khác."),
    (3, "Luồng đầy đủ: tạo danh sách mới → thêm nhanh việc → xem trên cả tab lịch", "P1",
     "Chưa có danh sách nào tên \"Việc phát sinh\".",
     "1. Tạo danh sách cá nhân mới \"Việc phát sinh\".\n"
     "2. Mở màn xem riêng danh sách này, gõ \"Kiểm tra máy in\" vào ô Thêm việc mới, Enter (không "
     "có ngày hạn vì tạo nhanh).\n"
     "3. Chuyển sang tab Lịch làm việc, dò khắp lưới tìm thẻ \"Kiểm tra máy in\".\n"
     "4. Quay lại tab danh sách gộp, tìm nhóm \"Không hạn\".",
     "—",
     "- Bước 3: KHÔNG tìm thấy thẻ nào trên lịch — việc tạo nhanh không có ngày hạn nên không lên "
     "lịch.\n"
     "- Bước 4: việc \"Kiểm tra máy in\" nằm đúng ở nhóm \"Không hạn\"."),
]))

# ============================================================ BUILD
if __name__ == "__main__":
    build(
        output_file=OUTPUT_FILE,
        sheet_name="Trang tính1",
        feature_name=FEATURE_NAME,
        module_name=MODULE_NAME,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
        role_section_title="Phạm vi dữ liệu theo sở hữu",
    )
