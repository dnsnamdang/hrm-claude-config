# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho Redmine #11386 — Màn Danh sách Nhu cầu khách hàng
(4 phần: danh sách + phân quyền 5 cấp · hạn xử lý · đóng thủ công · bàn giao) và tab
"Nhu cầu của khách hàng" ở Công việc của tôi (#11390).

Chạy:  python .plans/customer-demand-list/gen_testcase.py
Nhánh code tham chiếu: tpe-develop-assign (đã merge task_11386 / task_11377 / #11390).
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", ".claude", "skills",
                                       "testcase-documenter", "assets"))
sys.path.insert(0, ASSETS)

from tc_engine import build  # noqa: E402

FEATURE = "Danh sách Nhu cầu khách hàng (#11386) - Cập nhật ngày 17/09/2026"
MODULE = "Nhu cầu khách hàng"
OUT = os.path.join(HERE, "testcase.xlsx")

P_ALL = "Xem danh sách nhu cầu khách hàng theo tổng công ty"
P_COMPANY = "Xem danh sách nhu cầu khách hàng theo công ty"
P_DEPT = "Xem danh sách nhu cầu khách hàng theo phòng ban"
P_PART = "Xem danh sách nhu cầu khách hàng theo bộ phận"
P_HANDOVER = "Bàn giao nhu cầu khách hàng"
P_CLOSE = "Đóng nhu cầu khách hàng"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Màn Meetings › Nhu cầu khách hàng: gom toàn bộ nhu cầu đầu tư mà kinh doanh thu thập được trong biên bản "
     "cuộc họp, để theo dõi tới khi chuyển thành Dự án tiền khả thi (Dự án TKT) hoặc bị đóng.\n"
     "Bốn nhóm việc trên màn:\n"
     "- Xem danh sách 13 cột theo 5 cấp phân quyền dữ liệu;\n"
     "- Theo dõi hạn xử lý nhu cầu (ngày hết hạn + cảnh báo sắp hết hạn);\n"
     "- Đóng nhu cầu thủ công kèm ghi chú bắt buộc;\n"
     "- Bàn giao nhu cầu cho người khác (một nhu cầu hoặc nhiều nhu cầu cùng lúc) kèm thông báo và lưu vết.\n"
     "Cùng bảng này còn hiện ở thẻ 'Nhu cầu của khách hàng' trong màn Công việc của tôi, nhưng chỉ lấy nhu cầu do "
     "chính người đăng nhập phụ trách."),

    ("2. Đối tượng được tính / hiển thị",
     "Mỗi dòng là 1 nhu cầu ghi trong khối Khảo sát của biên bản cuộc họp, gồm cả 3 trạng thái:\n"
     "- 'Đang theo dõi' (xanh dương): nhu cầu còn mở, được đóng / bàn giao / lập Dự án TKT;\n"
     "- 'Đã lập dự án TKT' (xanh lá): đã chuyển thành dự án, cột Dự án TKT hiện mã và tên dự án bấm được;\n"
     "- 'Đóng' (xám): do người dùng đóng tay hoặc hệ thống tự đóng vì quá hạn.\n"
     "Phạm vi dữ liệu theo 5 cấp: tổng công ty › công ty › phòng ban › bộ phận › cá nhân. Cấp cá nhân là mặc định "
     "khi tài khoản không có quyền quản lý nào — chỉ thấy nhu cầu do chính mình đang phụ trách.\n"
     "Phạm vi tính theo NGƯỜI ĐANG PHỤ TRÁCH: đã bàn giao thì tính theo người nhận, chưa bàn giao thì tính theo "
     "người chủ trì cuộc họp."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Không ẩn dòng nào theo trạng thái; muốn xem riêng thì dùng bộ lọc Trạng thái.\n"
     "- Nút [Tạo Dự án TKT] chỉ hiện với nhu cầu 'Đang theo dõi' và chưa gắn dự án; nhu cầu đã đóng hoặc đã lập "
     "dự án thì ẩn hẳn (không hiện nút mờ).\n"
     "- Biểu tượng Bàn giao và Đóng nhu cầu chỉ hiện với nhu cầu 'Đang theo dõi' chưa gắn dự án.\n"
     "- Ô tích đầu dòng bị khoá ở nhu cầu không bàn giao được, nên không gom được chúng vào lô bàn giao.\n"
     "- Người không có quyền quản lý nào vẫn vào được màn nhưng chỉ thấy nhu cầu của chính mình — không có chuyện "
     "màn trắng hay bị chặn."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Màn không có bộ lọc khoảng thời gian. Các mốc thời gian hiển thị:\n"
     "- 'Thời gian khánh thành dự án' = thời gian dự kiến bắt đầu mà kinh doanh nhập trong biên bản, dạng "
     "dd/mm/yyyy;\n"
     "- 'Thời gian hết hạn nhu cầu' = ngày cuộc họp Hoàn thành + số ngày hiệu lực khai ở Lĩnh vực Công ty kinh "
     "doanh; tô cam kèm ghi chú khi đã vào vùng cảnh báo (số ngày cảnh báo khai ở Cấu hình chung, mặc định 3);\n"
     "- Cột Meeting hiện tên cuộc họp, bấm vào mở chi tiết cuộc họp.\n"
     "Bộ lọc đang chọn được nhớ trong 10 phút khi đi sang chi tiết cuộc họp / dự án rồi bấm quay lại."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Cuộc họp (loại có khảo sát nhu cầu) → nhiều Nhu cầu khách hàng → mỗi nhu cầu gắn 1 Lĩnh vực Công ty kinh "
     "doanh + 1 Nhóm ngành, và có thể sinh ra 1 Dự án TKT.\n"
     "13 cột theo đúng thứ tự khách chốt: STT · Khách hàng · Lĩnh vực Công ty kinh doanh · Nhóm ngành · Giá trị "
     "đầu tư dự kiến · Thời gian khánh thành dự án · Thời gian hết hạn nhu cầu · Meeting · Trạng thái · Dự án TKT "
     "· Kinh doanh chủ trì · Phòng ban · Thao tác. Ngoài ra còn 2 cột Người tạo / Ngày tạo khai sẵn nhưng mặc "
     "định ẩn, bật lại bằng nút Cấu hình cột hiển thị.\n"
     "Màn không có trang chi tiết riêng: lịch sử xem bằng popup 'Lịch sử cập nhật nhu cầu' ngay trên dòng."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Bàn giao cho đúng người đang giữ nhu cầu thì hệ thống bỏ qua, không ghi thêm dòng lịch sử vô nghĩa.\n"
     "- Bàn giao hàng loạt mà trong lô có nhu cầu không còn 'Đang theo dõi' thì CHẶN CẢ LÔ, không bàn giao một "
     "phần rồi báo thành công.\n"
     "- Tích chọn dòng sẽ tự bỏ khi dòng đó không còn trên trang đang xem (đổi trang, đổi bộ lọc) để không bàn "
     "giao nhầm bản ghi không nhìn thấy.\n"
     "- Bàn giao KHÔNG tính lại hạn: mốc cuộc họp Hoàn thành và ngày hết hạn giữ nguyên."),

    ("7. Phân quyền cấp",
     "Xem dữ liệu (chọn cấp cao nhất mà tài khoản có):\n"
     "- \"%s\" · \"%s\" · \"%s\" · \"%s\";\n"
     "- không có quyền nào ở trên = cấp cá nhân, chỉ thấy nhu cầu mình đang phụ trách.\n"
     "Thao tác:\n"
     "- \"%s\": bàn giao được nhu cầu của người khác. Người ĐANG phụ trách nhu cầu tự bàn giao được mà KHÔNG cần "
     "quyền này.\n"
     "- \"%s\": đóng được nhu cầu của người khác. Người đang phụ trách tự đóng được mà không cần quyền này."
     % (P_ALL, P_COMPANY, P_DEPT, P_PART, P_HANDOVER, P_CLOSE)),

    ("8. Cách tính các ô thống kê",
     "- Cột STT liên tục theo trang: trang 2 cỡ 10 dòng thì dòng đầu là 11.\n"
     "- Dòng 'Hiển thị a-b / N' dưới bảng: N là tổng số nhu cầu khớp bộ lọc VÀ nằm trong phạm vi quyền của tài "
     "khoản đang xem.\n"
     "- Dòng chữ trên thanh công cụ khi tích chọn: 'Đã chọn X nhu cầu' — X là số dòng đang tích.\n"
     "- Giá trị đầu tư dự kiến hiển thị theo chuẩn quốc tế: dấu phẩy ngăn hàng nghìn, ví dụ 1,250,000,000; "
     "ô trống hiện dấu '—'.\n"
     "- Ghi chú cạnh ngày hết hạn: '(còn X ngày)' · '(hết hạn hôm nay)' · '(quá hạn X ngày)'."),

    ("9. Ghi chú đọc bảng",
     "Bẫy dễ sai:\n"
     "- Cột 'Thời gian hết hạn nhu cầu' hiện 'Không thời hạn' là ĐÚNG khi Lĩnh vực Công ty kinh doanh của nhu cầu "
     "đang để số ngày hiệu lực = 0, hoặc cuộc họp chưa Hoàn thành, hoặc nhu cầu đã đóng / đã lập dự án. Muốn thấy "
     "ngày hết hạn thì phải khai số ngày hiệu lực ở danh mục trước. ⚠️ QA đã báo lỗi ngày 16/09 'chỉ thấy Không "
     "thời hạn' — kiểm đúng điều kiện trên trước khi kết luận lỗi.\n"
     "- Người đang phụ trách ≠ người chủ trì cuộc họp gốc sau khi bàn giao; cột 'Kinh doanh chủ trì' hiện người "
     "ĐANG phụ trách.\n"
     "- Bàn giao xong, cấp quản lý của phòng cũ KHÔNG còn thấy nhu cầu đó nữa — đúng thiết kế, không phải mất dữ "
     "liệu.\n"
     "- Nút không dùng được thì ẩn hẳn, không hiện mờ. Đừng báo lỗi 'thiếu nút Đóng' ở nhu cầu đã đóng.\n"
     "- Báo cáo CSKH tiềm năng CỐ Ý vẫn gom theo người chủ trì cuộc họp gốc, nên số liệu báo cáo không đổi sau khi "
     "bàn giao.\n"
     "- Ghi chú khi đóng nhu cầu là BẮT BUỘC và tối đa 1000 ký tự.\n"
     "- ⚠️ 5 lỗi QA báo ngày 16/09 cần kiểm lại trong bộ này: sau khi tạo Dự án TKT phải quay về danh sách · "
     "Cấu hình cột hiển thị lưu được · bảng không vỡ khi bật nhiều cột · popup Tìm kiếm nâng cao chọn được người "
     "nhận · thông báo lỗi khi tạo dự án phải chỉ rõ trường còn thiếu."),
]

ROLE_TCS = [
    ("00", "Cấp tổng công ty thấy nhu cầu của mọi công ty", "P0",
     "Tài khoản A có quyền \"%s\". Toàn hệ thống có 47 nhu cầu, thuộc 3 công ty." % P_ALL,
     "1. Đăng nhập tài khoản A\n2. Vào Meetings › Nhu cầu khách hàng\n3. Đọc dòng 'Hiển thị ... / N' dưới bảng",
     "—",
     "- Tổng N = 47\n- Lọc lần lượt từng công ty đều ra dữ liệu, không công ty nào bị chặn"),

    ("01", "Cấp công ty chỉ thấy nhu cầu công ty mình", "P0",
     "Tài khoản B có quyền \"%s\", thuộc công ty 1. Công ty 1 có 20 nhu cầu, công ty 2 có 27 nhu cầu." % P_COMPANY,
     "1. Đăng nhập tài khoản B\n2. Vào màn Nhu cầu khách hàng\n3. Đọc tổng số dưới bảng",
     "—",
     "- Tổng = 20, toàn bộ thuộc công ty 1\n- Không có dòng nào của công ty 2"),

    ("02", "Cấp phòng ban chỉ thấy nhu cầu phòng mình quản lý", "P0",
     "Tài khoản C có quyền \"%s\" và đang quản lý phòng Kinh doanh 1 (6 nhân sự, 12 nhu cầu). Phòng Kinh doanh 2 "
     "có 9 nhu cầu." % P_DEPT,
     "1. Đăng nhập tài khoản C\n2. Vào màn Nhu cầu khách hàng",
     "—",
     "- Thấy đúng 12 nhu cầu của phòng Kinh doanh 1 (cộng thêm nhu cầu của chính mình nếu có)\n"
     "- Không thấy nhu cầu của phòng Kinh doanh 2"),

    ("03", "Cấp bộ phận chỉ thấy nhu cầu bộ phận mình quản lý", "P0",
     "Tài khoản D có quyền \"%s\", quản lý bộ phận Kinh doanh dự án (3 nhân sự, 5 nhu cầu)." % P_PART,
     "1. Đăng nhập tài khoản D\n2. Vào màn Nhu cầu khách hàng",
     "—",
     "- Thấy đúng 5 nhu cầu của bộ phận mình\n- Không thấy nhu cầu của bộ phận khác cùng phòng"),

    ("04", "Không có quyền quản lý nào thì chỉ thấy nhu cầu của chính mình", "P0",
     "Tài khoản E là nhân viên kinh doanh, không có 4 quyền xem theo cấp. E đang phụ trách 4 nhu cầu; đồng nghiệp "
     "cùng phòng có 8 nhu cầu.",
     "1. Đăng nhập tài khoản E\n2. Vào Meetings › Nhu cầu khách hàng",
     "—",
     "- Vào được màn bình thường, thấy đúng 4 nhu cầu của mình\n"
     "- ⚠️ Không bị chặn vào màn, không hiện thông báo thiếu quyền"),

    ("05", "Người đang phụ trách tự bàn giao được dù không có quyền bàn giao", "P0",
     "Tài khoản E không có quyền \"%s\", đang phụ trách nhu cầu #101 trạng thái Đang theo dõi." % P_HANDOVER,
     "1. Đăng nhập tài khoản E\n2. Tìm dòng #101\n3. Bấm biểu tượng Bàn giao nhu cầu\n4. Chọn người nhận và bấm "
     "Bàn giao",
     "Người nhận: Trần Văn B",
     "- Bàn giao thành công\n- Dòng #101 đổi Kinh doanh chủ trì thành Trần Văn B"),

    ("06", "Không có quyền bàn giao thì không bàn giao được nhu cầu của người khác", "P0",
     "Tài khoản E không có quyền \"%s\". Nhu cầu #102 do người khác phụ trách nhưng E vẫn nhìn thấy (cùng phòng)."
     % P_HANDOVER,
     "1. Đăng nhập tài khoản E\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Bàn giao cho nhu cầu #102, bỏ qua "
     "giao diện\n3. Mở lại danh sách",
     "Nhu cầu: #102",
     "- Hệ thống từ chối kèm câu 'Bạn chỉ bàn giao được nhu cầu do chính mình phụ trách.'\n"
     "- Người phụ trách nhu cầu #102 không đổi"),

    ("07", "Cấp quản lý có quyền bàn giao thì bàn giao được nhu cầu của nhân viên", "P0",
     "Tài khoản C có quyền \"%s\" và quyền xem theo phòng ban. Nhu cầu #102 do nhân viên E phụ trách." % P_HANDOVER,
     "1. Đăng nhập tài khoản C\n2. Bấm biểu tượng Bàn giao ở dòng #102\n3. Chọn người nhận và bấm Bàn giao",
     "Người nhận: Nguyễn Thị Cần",
     "- Bàn giao thành công, cột Kinh doanh chủ trì và Phòng ban đổi theo người nhận"),

    ("08", "Người đang phụ trách tự đóng được nhu cầu dù không có quyền đóng", "P0",
     "Tài khoản E không có quyền \"%s\", đang phụ trách nhu cầu #103 Đang theo dõi." % P_CLOSE,
     "1. Đăng nhập tài khoản E\n2. Bấm biểu tượng Đóng nhu cầu ở dòng #103\n3. Nhập ghi chú và bấm Xác nhận đóng",
     "Ghi chú: Khách dừng kế hoạch đầu tư",
     "- Đóng thành công, trạng thái #103 chuyển 'Đóng'"),

    ("09", "Không có quyền đóng thì không đóng được nhu cầu của người khác", "P0",
     "Tài khoản E không có quyền \"%s\". Nhu cầu #104 do người khác phụ trách." % P_CLOSE,
     "1. Đăng nhập tài khoản E\n2. Gọi thẳng chức năng Đóng nhu cầu #104, bỏ qua giao diện",
     "Ghi chú: thử đóng lén",
     "- Hệ thống từ chối kèm câu 'Bạn chỉ đóng được nhu cầu do chính mình phụ trách.'\n"
     "- Nhu cầu #104 vẫn Đang theo dõi"),

    ("10", "Gọi thẳng danh sách không vượt được phạm vi quyền", "P0",
     "Tài khoản E cấp cá nhân, đang phụ trách 4 nhu cầu; hệ thống có 47 nhu cầu.",
     "1. Đăng nhập tài khoản E\n2. Dùng công cụ kiểm thử gọi thẳng chức năng lấy danh sách nhu cầu, kèm điều kiện "
     "lọc theo công ty khác\n3. Đếm số bản ghi trả về",
     "—",
     "- Chỉ trả về 4 nhu cầu của E\n- ⚠️ Lọc theo công ty / phòng ban khác KHÔNG mở rộng được phạm vi"),
]

S1 = [
    (1, "Vào màn bằng menu Meetings", "P0",
     "Tài khoản có quyền xem theo công ty, công ty có 20 nhu cầu.",
     "1. Đăng nhập\n2. Mở nhóm menu Meetings\n3. Bấm mục Nhu cầu khách hàng",
     "—",
     "- Mở màn 'Nhu cầu khách hàng'\n- Bảng hiện 10 dòng đầu, dưới bảng ghi 'Hiển thị 1-10 / 20'"),

    (2, "Thứ tự 13 cột đúng như khách chốt", "P0",
     "Màn danh sách đang mở, chưa đổi cấu hình cột.",
     "1. Đọc dòng tiêu đề bảng từ trái sang phải",
     "—",
     "- Ô tích · STT · Khách hàng · Lĩnh vực Công ty kinh doanh · Nhóm ngành · Giá trị đầu tư dự kiến · Thời gian "
     "khánh thành dự án · Thời gian hết hạn nhu cầu · Meeting · Trạng thái · Dự án TKT · Kinh doanh chủ trì · "
     "Phòng ban · Thao tác\n"
     "- ⚠️ Cột Trạng thái nằm TRƯỚC cột Dự án TKT (theo yêu cầu khách), không nằm cuối bảng"),

    (3, "Bật cột Người tạo / Ngày tạo bằng Cấu hình cột hiển thị", "P0",
     "Hai cột Người tạo và Ngày tạo đang ẩn mặc định.",
     "1. Bấm nút Cấu hình cột hiển thị (biểu tượng cột) trên thanh công cụ\n2. Tích chọn Người tạo và Ngày tạo\n"
     "3. Bấm lưu\n4. Quan sát bảng",
     "—",
     "- Popup mở ra liệt kê đủ các cột của bảng\n- Sau khi lưu, 2 cột xuất hiện trên bảng\n"
     "- ⚠️ QA báo lỗi 'Tùy chỉnh cột đang thất bại' ngày 16/09 — kiểm kỹ cả thông báo lưu lẫn kết quả trên bảng"),

    (4, "Cấu hình cột được nhớ sau khi tải lại trang", "P0",
     "Vừa bật thêm 2 cột ở mục 3.",
     "1. Tải lại trang (F5)\n2. Quan sát bảng",
     "—",
     "- 2 cột vừa bật vẫn còn\n- Thứ tự các cột khác không đổi"),

    (5, "Tắt bớt cột", "P1",
     "Bảng đang bật đủ 15 cột.",
     "1. Mở Cấu hình cột hiển thị, bỏ chọn cột Phòng ban\n2. Lưu",
     "—",
     "- Cột Phòng ban biến mất, bảng không bị lệch tiêu đề so với dữ liệu"),

    (6, "Bảng không vỡ khi bật nhiều cột", "P0",
     "Bật toàn bộ cột có thể bật.",
     "1. Quan sát bảng ở màn hình rộng và sau đó thu hẹp cửa sổ trình duyệt\n2. Cuộn ngang bảng",
     "—",
     "- Tiêu đề luôn thẳng hàng với dữ liệu, không có cột nào tràn ra ngoài khung\n"
     "- Có thanh cuộn ngang ở cả trên và dưới bảng, cột STT và Khách hàng đứng yên khi cuộn\n"
     "- ⚠️ QA báo 'Bảng đang vỡ' ngày 16/09 — chụp lại màn hình nếu còn tái hiện"),

    (7, "Thẻ Nhu cầu của khách hàng trong Công việc của tôi chỉ hiện nhu cầu của mình", "P0",
     "Tài khoản C có quyền xem theo phòng ban, phòng có 12 nhu cầu, riêng C đang phụ trách 3.",
     "1. Vào Công việc của tôi\n2. Mở thẻ 'Nhu cầu của khách hàng'\n3. Đọc tổng số dưới bảng",
     "—",
     "- Chỉ 3 nhu cầu do chính C phụ trách\n"
     "- ⚠️ Cùng tài khoản nhưng vào Meetings › Nhu cầu khách hàng thì thấy đủ 12 — hai lối vào khác phạm vi là "
     "đúng thiết kế"),

    (8, "Hai lối vào dùng chung một bảng", "P1",
     "Như trên.",
     "1. So sánh cột và thao tác giữa màn Nhu cầu khách hàng và thẻ Nhu cầu của khách hàng",
     "—",
     "- Cùng bộ cột, cùng bộ lọc, cùng các thao tác trên dòng\n- Khác nhau duy nhất ở phạm vi dữ liệu"),

    (9, "Bộ lọc được nhớ khi sang chi tiết rồi quay lại", "P1",
     "Đang lọc Trạng thái = Đang theo dõi ở màn Nhu cầu khách hàng.",
     "1. Bấm tên cuộc họp ở cột Meeting để sang chi tiết cuộc họp\n2. Bấm nút quay lại của trình duyệt",
     "—",
     "- Màn danh sách giữ nguyên điều kiện lọc và trang đang xem\n- Không phải chọn lại bộ lọc từ đầu"),

    (10, "Danh sách rỗng", "P1",
     "Lọc ra điều kiện chắc chắn không có dữ liệu.",
     "1. Gõ chuỗi vô nghĩa vào ô tìm nhanh",
     "Tìm nhanh: zzzzzz",
     "- Bảng hiện 'Không có dữ liệu phù hợp bộ lọc.'\n- ⚠️ Dòng chữ này không được tô đỏ"),
]

S2 = [
    (1, "Tìm nhanh theo tên khách hàng", "P0",
     "Có nhu cầu của khách 'Công ty ABC' và khách 'Công ty XYZ'.",
     "1. Gõ 'ABC' vào ô tìm nhanh",
     "Tìm nhanh: ABC",
     "- Bảng chỉ còn nhu cầu của Công ty ABC\n- Bảng tự lọc, không cần bấm nút tìm"),

    (2, "Tìm nhanh theo mã hoặc tên cuộc họp", "P0",
     "Cuộc họp 'MT-0012 - Khảo sát dây chuyền sơn' sinh ra 2 nhu cầu.",
     "1. Gõ 'MT-0012' vào ô tìm nhanh\n2. Xoá đi, gõ 'dây chuyền sơn'",
     "Tìm nhanh: MT-0012 / dây chuyền sơn",
     "- Cả 2 lần đều ra đúng 2 nhu cầu của cuộc họp đó"),

    (3, "Tìm nhanh theo nhóm ngành", "P0",
     "Có nhu cầu thuộc nhóm ngành 'Luyện Kim'.",
     "1. Gõ 'Luyện Kim' vào ô tìm nhanh",
     "Tìm nhanh: Luyện Kim",
     "- Bảng chỉ còn nhu cầu có cột Nhóm ngành là Luyện Kim"),

    (4, "Câu gợi ý trong ô tìm nhanh nói đúng phạm vi tìm", "P1",
     "Ô tìm nhanh đang trống.",
     "1. Đọc chữ mờ trong ô tìm nhanh",
     "—",
     "- Ghi 'Tìm theo tên khách hàng, mã/tên meeting, nhóm ngành'"),

    (5, "Lọc theo Công ty", "P0",
     "Tài khoản xem theo tổng công ty. Công ty 1 có 20 nhu cầu, công ty 2 có 27.",
     "1. Mở bộ lọc nâng cao\n2. Chọn Công ty = Công ty 1",
     "Công ty: Công ty 1",
     "- Bảng còn 20 dòng, tổng dưới bảng cũng là 20"),

    (6, "Lọc Phòng ban phụ thuộc Công ty đã chọn", "P0",
     "Công ty 1 có 3 phòng, công ty 2 có 2 phòng.",
     "1. Chọn Công ty = Công ty 1\n2. Mở ô Phòng ban",
     "—",
     "- Danh sách chỉ liệt kê 3 phòng của Công ty 1\n- Đổi công ty thì ô Phòng ban tự xoá lựa chọn cũ"),

    (7, "Lọc theo Bộ phận và Nhân viên", "P0",
     "Phòng Kinh doanh 1 có bộ phận 'Kinh doanh dự án' (3 nhân sự).",
     "1. Chọn Phòng ban = Kinh doanh 1\n2. Chọn Bộ phận = Kinh doanh dự án\n3. Chọn Nhân viên = Nguyễn Thị Cần",
     "—",
     "- Sau mỗi bước bảng thu hẹp dần\n- Bước 3 chỉ còn nhu cầu do Nguyễn Thị Cần phụ trách"),

    (8, "Ô chọn nhân viên hiển thị đúng khuôn tên - mã phòng - mã nhân viên", "P1",
     "Nhân viên Nguyễn Thị Cần thuộc phòng HN_KD1, mã 11010057.",
     "1. Mở ô Nhân viên, gõ 'Cần'",
     "—",
     "- Dòng gợi ý hiện 'Nguyễn Thị Cần - HN_KD1 - 11010057'"),

    (9, "Lọc theo Lĩnh vực Công ty kinh doanh", "P0",
     "Có 8 nhu cầu thuộc lĩnh vực Công nghiệp.",
     "1. Mở bộ lọc nâng cao\n2. Chọn Lĩnh vực Công ty kinh doanh = Công nghiệp",
     "Lĩnh vực: Công nghiệp",
     "- Bảng còn 8 dòng, cột Lĩnh vực toàn 'Công nghiệp'"),

    (10, "Danh sách Lĩnh vực và Nhóm ngành có dữ liệu", "P0",
     "Hệ thống có ít nhất 5 lĩnh vực và 20 nhóm ngành đang hoạt động.",
     "1. Mở bộ lọc nâng cao\n2. Mở lần lượt ô Lĩnh vực Công ty kinh doanh và ô Nhóm ngành",
     "—",
     "- Cả 2 ô đều liệt kê dữ liệu, không ô nào rỗng trơn\n"
     "- Nhóm ngành không bị lặp tên dù nhiều lĩnh vực cùng chứa"),

    (11, "Lọc theo Nhóm ngành", "P0",
     "Nhóm ngành 'Sơn - phủ (Coating)' có 3 nhu cầu.",
     "1. Chọn Nhóm ngành = Sơn - phủ (Coating)",
     "Nhóm ngành: Sơn - phủ (Coating)",
     "- Bảng còn đúng 3 dòng"),

    (12, "Lọc theo từng trạng thái", "P0",
     "Dữ liệu: 30 Đang theo dõi, 10 Đã lập dự án TKT, 7 Đóng.",
     "1. Chọn Trạng thái = Đang theo dõi\n2. Đổi sang Đã lập dự án TKT\n3. Đổi sang Đóng",
     "—",
     "- Ba lần cho ra lần lượt 30, 10, 7 dòng, cột Trạng thái đồng nhất trong từng lần"),

    (13, "Nhiều điều kiện lọc cùng lúc", "P0",
     "Phòng Kinh doanh 1 có 4 nhu cầu Đang theo dõi thuộc lĩnh vực Công nghiệp.",
     "1. Chọn Phòng ban = Kinh doanh 1\n2. Chọn Lĩnh vực = Công nghiệp\n3. Chọn Trạng thái = Đang theo dõi",
     "—",
     "- Bảng còn đúng 4 dòng thoả cả 3 điều kiện"),

    (14, "Nút Làm mới xoá hết điều kiện lọc", "P0",
     "Đang lọc nhiều điều kiện, bảng còn 4 dòng.",
     "1. Bấm Làm mới",
     "—",
     "- Mọi ô lọc và ô tìm nhanh về trống\n- Bảng tải lại đủ dữ liệu theo phạm vi quyền, về trang 1"),

    (15, "Lọc xong quay về trang 1", "P1",
     "Đang ở trang 3.",
     "1. Chọn thêm 1 điều kiện lọc bất kỳ",
     "—",
     "- Bảng nhảy về trang 1, không hiện trang rỗng"),
]

S3 = [
    (1, "Thứ tự mặc định theo cuộc họp mới nhất", "P0",
     "Các nhu cầu sinh từ nhiều cuộc họp có ngày khác nhau.",
     "1. Vào màn, chưa bấm sắp xếp cột nào\n2. Đối chiếu cột Meeting của vài dòng đầu",
     "—",
     "- Nhu cầu của cuộc họp diễn ra gần đây nhất đứng trên"),

    (2, "Sắp xếp theo Khách hàng", "P1",
     "Có nhiều khách hàng khác nhau.",
     "1. Bấm tiêu đề cột Khách hàng\n2. Bấm lần nữa",
     "—",
     "- Lần 1 xếp tăng dần theo bảng chữ cái, lần 2 đảo lại"),

    (3, "Sắp xếp theo Giá trị đầu tư dự kiến", "P0",
     "Giá trị đầu tư: 500,000,000 · 1,250,000,000 · 80,000,000.",
     "1. Bấm tiêu đề cột Giá trị đầu tư dự kiến",
     "—",
     "- Sắp đúng theo giá trị số (80,000,000 → 500,000,000 → 1,250,000,000), không sắp theo chuỗi ký tự"),

    (4, "Sắp xếp theo Thời gian khánh thành dự án", "P1",
     "3 nhu cầu có thời gian khánh thành 01/10/2026, 15/12/2026, 03/03/2027.",
     "1. Bấm tiêu đề cột Thời gian khánh thành dự án",
     "—",
     "- Sắp đúng theo thời gian, không theo chuỗi ngày/tháng"),

    (5, "Sắp xếp giữ nguyên khi chuyển trang", "P1",
     "Đang sắp theo Giá trị đầu tư giảm dần, có 3 trang.",
     "1. Sang trang 2",
     "—",
     "- Giá trị ở trang 2 tiếp nối trang 1, không bị xáo lại từ đầu"),

    (6, "Sắp xếp kết hợp bộ lọc", "P1",
     "Lọc Trạng thái = Đang theo dõi còn 30 dòng.",
     "1. Bấm sắp xếp theo Khách hàng",
     "—",
     "- Vẫn chỉ gồm nhu cầu Đang theo dõi, thứ tự đã đổi, tổng vẫn 30"),

    (7, "Phân trang mặc định 10 dòng", "P0",
     "Phạm vi quyền có 47 nhu cầu.",
     "1. Vào màn, đọc dòng thông tin dưới bảng",
     "—",
     "- Ghi 'Hiển thị 1-10 / 47', có 5 trang"),

    (8, "Đổi số dòng mỗi trang", "P0",
     "Như trên.",
     "1. Chọn 50 dòng/trang",
     "Số dòng/trang: 50",
     "- Bảng hiện đủ 47 dòng, tự về trang 1"),

    (9, "STT liên tục theo trang", "P1",
     "47 nhu cầu, cỡ trang 10.",
     "1. Sang trang 3\n2. Đọc cột STT",
     "—",
     "- Dòng đầu trang 3 là 21, dòng cuối là 30"),
]

S4 = [
    (1, "Cột Khách hàng và Nhóm ngành hiển thị đúng", "P0",
     "Nhu cầu #101 của khách 'Công ty ABC', lĩnh vực Công nghiệp, nhóm ngành Luyện Kim.",
     "1. Đối chiếu 3 cột đầu của dòng #101 với biên bản cuộc họp gốc",
     "—",
     "- Ba cột khớp dữ liệu trong biên bản\n- Chữ để thường, không in đậm"),

    (2, "Định dạng số tiền theo chuẩn quốc tế", "P0",
     "Nhu cầu #101 có giá trị đầu tư 1250000000.",
     "1. Đọc cột Giá trị đầu tư dự kiến của dòng #101",
     "—",
     "- Hiện '1,250,000,000' — dấu phẩy ngăn hàng nghìn\n- ⚠️ Không dùng dấu chấm ngăn nghìn"),

    (3, "Giá trị đầu tư để trống", "P2",
     "Nhu cầu #105 chưa nhập giá trị đầu tư.",
     "1. Đọc cột Giá trị đầu tư dự kiến của dòng #105",
     "—",
     "- Hiện dấu '—', không hiện số 0"),

    (4, "Bấm tên cuộc họp mở chi tiết cuộc họp", "P0",
     "Nhu cầu #101 sinh từ cuộc họp MT-0012.",
     "1. Bấm tên cuộc họp ở cột Meeting của dòng #101",
     "—",
     "- Mở màn chi tiết đúng cuộc họp MT-0012"),

    (5, "Badge trạng thái đúng chữ và màu", "P0",
     "Có đủ 3 nhu cầu ở 3 trạng thái.",
     "1. Đọc cột Trạng thái của 3 dòng đó",
     "—",
     "- 'Đang theo dõi' màu xanh dương · 'Đã lập dự án TKT' màu xanh lá · 'Đóng' màu xám\n"
     "- ⚠️ Yêu cầu gốc viết 'Đã lập dự án' và 'Đã đóng'; chữ đang dùng là bản khách duyệt sau — không tính là lỗi"),

    (6, "Cột Dự án TKT với nhu cầu đã có dự án", "P0",
     "Nhu cầu #106 đã gắn dự án DA-0007 - Nhà máy sơn Bắc Ninh.",
     "1. Đọc cột Dự án TKT của dòng #106\n2. Bấm vào liên kết đó",
     "—",
     "- Hiện mã dự án bấm được\n- Bấm vào mở đúng chi tiết dự án DA-0007"),

    (7, "Nút Tạo Dự án TKT với nhu cầu đang mở", "P0",
     "Nhu cầu #101 Đang theo dõi, chưa có dự án.",
     "1. Đọc cột Dự án TKT của dòng #101",
     "—",
     "- Hiện nút '+ Tạo Dự án TKT'"),

    (8, "Bấm Tạo Dự án TKT mở form kèm sẵn nhu cầu nguồn", "P0",
     "Nhu cầu #101 của khách Công ty ABC.",
     "1. Bấm nút Tạo Dự án TKT ở dòng #101\n2. Quan sát form dự án mở ra",
     "—",
     "- Mở màn tạo Dự án TKT\n- Thông tin khách hàng và nhu cầu nguồn đã được điền sẵn theo nhu cầu #101"),

    (9, "Lưu Dự án TKT xong quay về danh sách", "P0",
     "Đang ở form tạo Dự án TKT mở từ nhu cầu #101, đã điền đủ thông tin bắt buộc.",
     "1. Bấm Lưu",
     "—",
     "- Báo lưu thành công và quay về màn DANH SÁCH (Dự án TKT hoặc Nhu cầu khách hàng theo lối vào), không ở lại "
     "màn chi tiết\n"
     "- ⚠️ QA báo lỗi ngày 16/09: 'Tạo dự án TKT xong đang ra màn hình detail chứ không phải màn hình list'"),

    (10, "Thiếu trường bắt buộc khi tạo Dự án TKT phải báo rõ trường nào", "P0",
     "Đang ở form tạo Dự án TKT, bỏ trống một vài trường bắt buộc (trong đó có người liên hệ).",
     "1. Bấm Lưu\n2. Đọc thông báo và quan sát các ô trên form",
     "—",
     "- Từng ô còn thiếu hiện viền đỏ + dòng lỗi ngay dưới ô, màn tự cuộn tới ô lỗi đầu tiên\n"
     "- ⚠️ QA báo ngày 16/09: thông báo hiện chưa nói rõ phải điền trường nào; riêng người liên hệ thêm nhanh thì "
     "phải lưu trước mới chọn được — cần validate thẳng tại trường đó"),

    (11, "Nhu cầu đã đóng ẩn nút Tạo Dự án TKT", "P0",
     "Nhu cầu #107 trạng thái Đóng.",
     "1. Đọc cột Dự án TKT của dòng #107",
     "—",
     "- Chỉ có dấu '—', không có nút Tạo Dự án TKT (ẩn hẳn, không hiện mờ)"),

    (12, "Cột Kinh doanh chủ trì và Phòng ban", "P0",
     "Nhu cầu #101 do Nguyễn Thị Cần (phòng Kinh doanh 1) phụ trách.",
     "1. Đọc 2 cột Kinh doanh chủ trì và Phòng ban của dòng #101",
     "—",
     "- Hiện 'Nguyễn Thị Cần' và 'Kinh doanh 1'\n- Tên người không kèm mã nhân viên"),

    (13, "Cột Thời gian hết hạn nhu cầu khi lĩnh vực có khai số ngày hiệu lực", "P0",
     "Lĩnh vực Công nghiệp khai 30 ngày hiệu lực; cuộc họp của nhu cầu #101 Hoàn thành ngày 20/08/2026.",
     "1. Đọc cột Thời gian hết hạn nhu cầu của dòng #101",
     "—",
     "- Hiện '19/09/2026'\n"
     "- ⚠️ QA báo ngày 16/09 'chỉ thấy Không thời hạn': kiểm lại lĩnh vực đã khai số ngày hiệu lực chưa và cuộc "
     "họp đã Hoàn thành chưa trước khi kết luận lỗi"),

    (14, "Cột hạn tô cam khi sắp hết hạn", "P0",
     "Số ngày cảnh báo chung = 3; nhu cầu #108 hết hạn sau 2 ngày.",
     "1. Đọc cột Thời gian hết hạn nhu cầu của dòng #108",
     "—",
     "- Ngày hết hạn tô CAM, đậm, có biểu tượng cảnh báo, kèm '(còn 2 ngày)'\n- Không dùng màu đỏ"),

    (15, "Cột hạn ghi Không thời hạn đúng trường hợp", "P0",
     "Nhu cầu #109 thuộc lĩnh vực đang để 0 ngày hiệu lực; nhu cầu #110 có cuộc họp chưa Hoàn thành.",
     "1. Đọc cột hạn của 2 dòng này",
     "—",
     "- Cả 2 đều ghi 'Không thời hạn' màu xám\n- Đây là trạng thái đúng, không phải lỗi hiển thị"),
]

S5 = [
    (1, "Biểu tượng Đóng nhu cầu chỉ hiện với nhu cầu đang mở", "P0",
     "Dòng #101 Đang theo dõi; dòng #106 Đã lập dự án TKT; dòng #107 Đóng.",
     "1. So sánh cột Thao tác của 3 dòng",
     "—",
     "- Dòng #101 có biểu tượng Đóng nhu cầu\n- Dòng #106 và #107 KHÔNG có (ẩn hẳn)"),

    (2, "Popup xác nhận đóng hiển thị đúng", "P0",
     "Nhu cầu #101 Đang theo dõi.",
     "1. Bấm biểu tượng Đóng nhu cầu ở dòng #101",
     "—",
     "- Popup tiêu đề 'Xác nhận đóng nhu cầu'\n- Có ô nhập nhiều dòng nhãn 'Ghi chú chi tiết' kèm chữ gợi ý 'Nhập "
     "lý do đóng nhu cầu'\n- Hai nút: 'Xác nhận đóng' và 'Hủy'"),

    (3, "Ghi chú bỏ trống thì không đóng được", "P0",
     "Đang mở popup đóng nhu cầu #101.",
     "1. Để trống ô Ghi chú chi tiết\n2. Bấm Xác nhận đóng",
     "Ghi chú: (trống)",
     "- Popup KHÔNG đóng\n- Hiện lỗi ngay trong popup: 'Vui lòng nhập ghi chú chi tiết lý do đóng nhu cầu'\n"
     "- Nhu cầu vẫn Đang theo dõi"),

    (4, "Ghi chú chỉ toàn khoảng trắng", "P1",
     "Đang mở popup đóng nhu cầu.",
     "1. Gõ vài dấu cách vào ô Ghi chú\n2. Bấm Xác nhận đóng",
     "Ghi chú: '     '",
     "- Vẫn báo thiếu ghi chú, không đóng nhu cầu"),

    (5, "Đóng nhu cầu thành công", "P0",
     "Nhu cầu #101 Đang theo dõi, do chính tài khoản đang đăng nhập phụ trách.",
     "1. Bấm Đóng nhu cầu\n2. Nhập ghi chú\n3. Bấm Xác nhận đóng",
     "Ghi chú: Khách dừng kế hoạch đầu tư trong năm nay",
     "- Hiện thông báo 'Đã đóng nhu cầu'\n- Dòng #101 chuyển trạng thái 'Đóng' màu xám\n"
     "- Cột Dự án TKT không còn nút Tạo Dự án TKT\n- Biểu tượng Bàn giao và Đóng biến mất khỏi dòng đó"),

    (6, "Bấm Hủy trong popup đóng", "P0",
     "Đang mở popup đóng nhu cầu #102, đã gõ ghi chú.",
     "1. Bấm Hủy",
     "—",
     "- Popup đóng, không có thông báo\n- Nhu cầu #102 vẫn Đang theo dõi"),

    (7, "Ghi chú vượt 1000 ký tự", "P1",
     "Đang mở popup đóng nhu cầu.",
     "1. Dán chuỗi 1200 ký tự vào ô Ghi chú\n2. Bấm Xác nhận đóng",
     "Ghi chú: chuỗi 1200 ký tự",
     "- Báo lỗi 'Ghi chú chi tiết tối đa 1000 ký tự.'\n- ⚠️ Không tự cắt bớt nội dung người dùng đã gõ"),

    (8, "Đóng nhu cầu ghi lại người đóng và ghi chú", "P0",
     "Vừa đóng nhu cầu #101 với ghi chú ở mục 5.",
     "1. Bấm biểu tượng Lịch sử cập nhật ở dòng #101",
     "—",
     "- Popup lịch sử có 1 dòng hành động 'Đóng nhu cầu'\n- Cột Nội dung hiện tên người đang phụ trách kèm ghi chú "
     "đã nhập\n- Cột Người thực hiện là tài khoản vừa bấm đóng"),

    (9, "Đóng nhu cầu vừa bị người khác đóng trước đó", "P0",
     "Người 1 đã đóng nhu cầu #103; người 2 vẫn đang mở danh sách cũ.",
     "1. Người 2 bấm Đóng nhu cầu ở dòng #103, nhập ghi chú và xác nhận",
     "Ghi chú: đóng lần hai",
     "- Báo 'Nhu cầu không còn ở trạng thái Đang theo dõi nên không đóng được. Vui lòng tải lại danh sách.'\n"
     "- Ghi chú và người đóng lần đầu không bị ghi đè"),

    (10, "Gọi thẳng chức năng đóng mà không gửi ghi chú", "P0",
     "Nhu cầu #104 Đang theo dõi, tài khoản có quyền đóng.",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Đóng nhu cầu, không gửi ghi chú",
     "—",
     "- Bị từ chối kèm câu yêu cầu nhập ghi chú chi tiết\n- Nhu cầu không bị đóng\n"
     "- ⚠️ Chốt chặn phải nằm ở phía máy chủ, không chỉ ở popup"),

    (11, "Đóng nhu cầu đã lập dự án", "P0",
     "Nhu cầu #106 đã gắn Dự án TKT.",
     "1. Gọi thẳng chức năng Đóng nhu cầu #106",
     "Ghi chú: thử đóng",
     "- Bị từ chối vì không còn ở trạng thái Đang theo dõi\n- Liên kết dự án không bị ảnh hưởng"),
]

S6 = [
    (1, "Biểu tượng Bàn giao chỉ hiện với nhu cầu đang mở", "P0",
     "Dòng #101 Đang theo dõi; dòng #106 Đã lập dự án; dòng #107 Đóng.",
     "1. So sánh cột Thao tác của 3 dòng",
     "—",
     "- Chỉ dòng #101 có biểu tượng Bàn giao nhu cầu"),

    (2, "Popup bàn giao hiển thị đúng", "P0",
     "Nhu cầu #101 Đang theo dõi.",
     "1. Bấm biểu tượng Bàn giao ở dòng #101",
     "—",
     "- Popup tiêu đề 'Bàn giao nhu cầu'\n- Dòng mô tả: 'Bàn giao 1 nhu cầu cho người khác tiếp tục xử lý. Hạn xử "
     "lý giữ nguyên, không tính lại từ đầu.'\n"
     "- Ô 'Người nhận bàn giao' có dấu * đỏ, kèm liên kết 'Tìm kiếm nâng cao'\n- Ô 'Lý do bàn giao' nhập nhiều dòng"
     "\n- Hai nút: Bàn giao và Hủy"),

    (3, "Chọn người nhận bằng cách gõ tìm trong ô", "P0",
     "Nhân viên Trần Văn B đang hoạt động.",
     "1. Mở ô Người nhận bàn giao\n2. Gõ 'Trần Văn B'\n3. Chọn dòng gợi ý",
     "Người nhận: Trần Văn B",
     "- Danh sách lọc theo chữ đã gõ\n- Chọn xong ô hiện tên người nhận theo khuôn tên - mã phòng - mã nhân viên"),

    (4, "Chọn người nhận bằng popup Tìm kiếm nâng cao", "P0",
     "Như trên.",
     "1. Bấm 'Tìm kiếm nâng cao'\n2. Trong popup, tìm và tích chọn Trần Văn B\n3. Bấm nút đồng ý của popup",
     "Người nhận: Trần Văn B",
     "- Popup chọn nhân sự mở ra (đúng popup chọn thành phần tham gia của màn tạo cuộc họp)\n"
     "- Sau khi chọn, ô Người nhận bàn giao hiện đúng tên vừa chọn\n"
     "- ⚠️ QA báo lỗi ngày 16/09: chọn xong không thấy thể hiện đã chọn — kiểm kỹ ca này"),

    (5, "Bỏ trống người nhận", "P0",
     "Đang mở popup bàn giao.",
     "1. Không chọn người nhận\n2. Bấm Bàn giao",
     "—",
     "- Popup không đóng, hiện lỗi đỏ ngay dưới ô Người nhận bàn giao\n- Không có thay đổi dữ liệu"),

    (6, "Bàn giao thành công đổi người phụ trách và phòng ban", "P0",
     "Nhu cầu #101 do Nguyễn Thị Cần (phòng Kinh doanh 1) phụ trách. Trần Văn B thuộc phòng Kinh doanh 2.",
     "1. Bàn giao #101 cho Trần Văn B kèm lý do\n2. Quan sát dòng #101 sau khi bảng tải lại",
     "Người nhận: Trần Văn B · Lý do: Chuyển vùng phụ trách",
     "- Cột Kinh doanh chủ trì đổi thành Trần Văn B\n- Cột Phòng ban đổi thành Kinh doanh 2"),

    (7, "Bàn giao không tính lại hạn xử lý", "P0",
     "Nhu cầu #101 đang hết hạn 19/09/2026.",
     "1. Bàn giao #101 cho người khác\n2. Đọc lại cột Thời gian hết hạn nhu cầu",
     "—",
     "- Hạn vẫn là 19/09/2026\n- ⚠️ Không được đẩy lùi hạn theo ngày bàn giao"),

    (8, "Lý do bàn giao để trống vẫn bàn giao được", "P1",
     "Đang mở popup bàn giao #102.",
     "1. Chọn người nhận, để trống ô Lý do bàn giao\n2. Bấm Bàn giao",
     "—",
     "- Bàn giao thành công (lý do không bắt buộc)\n- Lịch sử vẫn ghi dòng Bàn giao, phần ghi chú để trống"),

    (9, "Bàn giao cho chính người đang giữ", "P1",
     "Nhu cầu #102 do Nguyễn Thị Cần phụ trách.",
     "1. Bàn giao #102 cho chính Nguyễn Thị Cần",
     "Người nhận: Nguyễn Thị Cần",
     "- Hệ thống bỏ qua, không báo lỗi gãy màn\n- Lịch sử KHÔNG sinh thêm dòng bàn giao vô nghĩa"),

    (10, "Bàn giao nhu cầu vừa bị đóng", "P0",
     "Người 1 vừa đóng nhu cầu #103; người 2 đang mở danh sách cũ.",
     "1. Người 2 bấm Bàn giao ở dòng #103, chọn người nhận và xác nhận",
     "—",
     "- Báo 'Có 1 nhu cầu không còn ở trạng thái Đang theo dõi nên không bàn giao được. Vui lòng tải lại danh "
     "sách.'\n- Không đổi người phụ trách"),

    (11, "Bấm Hủy trong popup bàn giao", "P1",
     "Đang mở popup bàn giao, đã chọn người nhận.",
     "1. Bấm Hủy",
     "—",
     "- Popup đóng, không bàn giao\n- Mở lại popup thì ô Người nhận đã trống, không giữ lựa chọn cũ"),
]

S7 = [
    (1, "Tích chọn 1 dòng hiện nút Bàn giao hàng loạt", "P0",
     "Trang đang xem có ít nhất 3 nhu cầu Đang theo dõi.",
     "1. Tích ô đầu dòng của 1 nhu cầu\n2. Quan sát thanh công cụ",
     "—",
     "- Hiện dòng chữ 'Đã chọn 1 nhu cầu' và nút 'Bàn giao hàng loạt'"),

    (2, "Ô tích bị khoá ở nhu cầu không bàn giao được", "P0",
     "Trang có nhu cầu Đóng và nhu cầu Đã lập dự án TKT.",
     "1. Thử tích ô đầu dòng của 2 nhu cầu đó",
     "—",
     "- Ô tích ở trạng thái khoá, không tích được\n- Số đếm 'Đã chọn' không tăng"),

    (3, "Tích chọn cả trang", "P0",
     "Trang 10 dòng, trong đó 6 dòng Đang theo dõi, 4 dòng không bàn giao được.",
     "1. Tích ô ở tiêu đề cột đầu",
     "—",
     "- Chỉ 6 dòng hợp lệ được tích\n- Dòng chữ ghi 'Đã chọn 6 nhu cầu'"),

    (4, "Bỏ tích cả trang", "P1",
     "Đang tích 6 dòng như trên.",
     "1. Bấm lại ô tích ở tiêu đề",
     "—",
     "- Mọi dòng bỏ tích, nút Bàn giao hàng loạt và dòng 'Đã chọn' biến mất"),

    (5, "Bàn giao hàng loạt thành công", "P0",
     "Đã tích 3 nhu cầu Đang theo dõi do chính mình phụ trách.",
     "1. Bấm Bàn giao hàng loạt\n2. Chọn người nhận, nhập lý do\n3. Bấm Bàn giao",
     "Người nhận: Trần Văn B · Lý do: Nghỉ thai sản",
     "- Popup ghi 'Bàn giao 3 nhu cầu cho người khác tiếp tục xử lý...'\n- Cả 3 dòng đổi Kinh doanh chủ trì thành "
     "Trần Văn B\n- Sau khi xong, các dòng tự bỏ tích, nút Bàn giao hàng loạt biến mất"),

    (6, "Lô có lẫn nhu cầu không hợp lệ thì chặn cả lô", "P0",
     "Tích 3 nhu cầu; trong lúc đó người khác đóng 1 trong 3 nhu cầu đó.",
     "1. Bấm Bàn giao hàng loạt, chọn người nhận, xác nhận",
     "—",
     "- Báo 'Có 1 nhu cầu không còn ở trạng thái Đang theo dõi nên không bàn giao được. Vui lòng tải lại danh "
     "sách.'\n- ⚠️ KHÔNG bàn giao 2 nhu cầu còn lại rồi báo thành công — phải chặn cả lô"),

    (7, "Tích chọn tự bỏ khi đổi trang", "P1",
     "Đang tích 3 dòng ở trang 1.",
     "1. Sang trang 2\n2. Quan sát thanh công cụ",
     "—",
     "- Không còn dòng 'Đã chọn ... nhu cầu' cho các dòng đã rời khỏi trang\n"
     "- ⚠️ Tránh bàn giao nhầm bản ghi mà người dùng không còn nhìn thấy"),

    (8, "Tích chọn tự bỏ khi đổi bộ lọc", "P1",
     "Đang tích vài dòng.",
     "1. Đổi bộ lọc Trạng thái sang 'Đóng'",
     "—",
     "- Các dòng đã tích không còn trên bảng, số đếm về 0"),

    (9, "Bàn giao hàng loạt nhu cầu của người khác khi không có quyền", "P0",
     "Tài khoản E không có quyền bàn giao; tích 2 nhu cầu, trong đó 1 của người khác.",
     "1. Bấm Bàn giao hàng loạt, chọn người nhận, xác nhận",
     "—",
     "- Bị từ chối với câu 'Bạn chỉ bàn giao được nhu cầu do chính mình phụ trách.'\n- Không nhu cầu nào đổi chủ"),

    (10, "Số lượng trong popup khớp số đã tích", "P2",
     "Đã tích 5 nhu cầu.",
     "1. Bấm Bàn giao hàng loạt\n2. Đọc dòng mô tả trong popup",
     "—",
     "- Ghi đúng 'Bàn giao 5 nhu cầu...'"),
]

S8 = [
    (1, "Mở popup Lịch sử cập nhật", "P0",
     "Nhu cầu #101 đã bàn giao 1 lần và bị đóng 1 lần.",
     "1. Bấm biểu tượng Lịch sử cập nhật ở dòng #101",
     "—",
     "- Popup tiêu đề 'Lịch sử cập nhật nhu cầu'\n- Bảng có 4 cột: Thời gian · Hành động · Nội dung · Người thực "
     "hiện\n- Có đủ 2 dòng (Bàn giao và Đóng nhu cầu)"),

    (2, "Dòng lịch sử bàn giao ghi đủ từ ai sang ai", "P0",
     "Nhu cầu #101 bàn giao từ Nguyễn Thị Cần sang Trần Văn B, lý do 'Chuyển vùng phụ trách'.",
     "1. Đọc dòng hành động 'Bàn giao' trong popup lịch sử",
     "—",
     "- Cột Nội dung ghi 'Nguyễn Thị Cần → Trần Văn B' kèm dòng lý do bên dưới\n"
     "- Cột Thời gian là lúc bấm bàn giao, Người thực hiện là người bấm"),

    (3, "Dòng lịch sử đóng nhu cầu không vẽ mũi tên", "P1",
     "Nhu cầu #101 đã bị đóng kèm ghi chú.",
     "1. Đọc dòng hành động 'Đóng nhu cầu'",
     "—",
     "- Cột Nội dung chỉ hiện tên người đang phụ trách kèm ghi chú, KHÔNG có mũi tên trỏ vào dấu gạch ngang"),

    (4, "Nhu cầu chưa có thay đổi nào", "P1",
     "Nhu cầu #105 chưa bàn giao, chưa đóng.",
     "1. Mở popup lịch sử của dòng #105",
     "—",
     "- Popup ghi 'Nhu cầu này chưa có thay đổi nào được ghi nhận.'\n- Không hiện bảng rỗng trơ khung"),

    (5, "Thứ tự các dòng lịch sử", "P2",
     "Nhu cầu #101 có 3 lần bàn giao và 1 lần đóng.",
     "1. Mở popup lịch sử, đọc cột Thời gian",
     "—",
     "- Các dòng xếp theo thời gian nhất quán (mới nhất hoặc cũ nhất trước, nhưng không xáo trộn)"),

    (6, "Biểu tượng Lịch sử có ở mọi dòng", "P2",
     "Bảng có nhu cầu ở cả 3 trạng thái.",
     "1. Quan sát cột Thao tác của các dòng",
     "—",
     "- Mọi dòng đều có biểu tượng Lịch sử cập nhật, kể cả nhu cầu đã đóng"),
]

S9 = [
    (1, "Người nhận bàn giao nhận được thông báo", "P0",
     "Bàn giao nhu cầu #101 (khách Công ty ABC, nhóm ngành Luyện Kim) cho Trần Văn B; nhu cầu còn 5 ngày tới hạn.",
     "1. Thực hiện bàn giao\n2. Đăng nhập tài khoản Trần Văn B\n3. Mở chuông thông báo",
     "—",
     "- Có 1 thông báo mới nêu tên khách hàng - nhóm ngành, cho biết được bàn giao từ ai và còn bao nhiêu ngày xử "
     "lý\n- Bấm vào thông báo mở đúng màn Nhu cầu khách hàng"),

    (2, "Thông báo khi nhu cầu đã quá hạn", "P1",
     "Nhu cầu #111 đã quá hạn 2 ngày nhưng chưa bị đóng; bàn giao cho Trần Văn B.",
     "1. Bàn giao và mở chuông thông báo của người nhận",
     "—",
     "- Nội dung ghi đã quá hạn 2 ngày, không ghi số ngày âm"),

    (3, "Bàn giao hàng loạt gửi thông báo cho từng nhu cầu", "P1",
     "Bàn giao 3 nhu cầu cùng lúc cho Trần Văn B.",
     "1. Thực hiện bàn giao hàng loạt\n2. Mở chuông thông báo của Trần Văn B",
     "—",
     "- Nhận 3 thông báo, mỗi thông báo nêu đúng 1 nhu cầu"),

    (4, "Người bàn giao không tự nhận thông báo", "P2",
     "Nguyễn Thị Cần bàn giao nhu cầu cho Trần Văn B.",
     "1. Mở chuông thông báo của Nguyễn Thị Cần",
     "—",
     "- Không có thông báo bàn giao gửi cho chính người thực hiện"),

    (5, "Phạm vi xem dịch sang phòng của người nhận", "P0",
     "Nhu cầu #101 thuộc phòng Kinh doanh 1. Trưởng phòng C xem theo phòng Kinh doanh 1, trưởng phòng D xem theo "
     "phòng Kinh doanh 2. Bàn giao #101 cho nhân sự phòng Kinh doanh 2.",
     "1. Sau khi bàn giao, đăng nhập C mở màn Nhu cầu khách hàng\n2. Đăng nhập D mở màn Nhu cầu khách hàng",
     "—",
     "- C KHÔNG còn thấy nhu cầu #101\n- D bắt đầu thấy nhu cầu #101\n"
     "- ⚠️ Đây là thiết kế đúng, không phải mất dữ liệu"),

    (6, "Người bàn giao vẫn thấy nhu cầu nếu còn quyền theo cấp", "P1",
     "Nguyễn Thị Cần (cấp cá nhân) bàn giao nhu cầu của mình cho người khác phòng.",
     "1. Sau khi bàn giao, Cần mở lại màn Nhu cầu khách hàng",
     "—",
     "- Cần không còn thấy nhu cầu đó (đã hết phạm vi cá nhân)\n- Cần vẫn thấy các nhu cầu còn lại của mình"),

    (7, "Báo cáo CSKH tiềm năng không đổi số sau khi bàn giao", "P1",
     "Trước khi bàn giao, Báo cáo CSKH tiềm năng đếm nhu cầu #101 cho Nguyễn Thị Cần.",
     "1. Bàn giao #101 cho Trần Văn B\n2. Mở lại Báo cáo CSKH tiềm năng cùng kỳ",
     "—",
     "- Báo cáo vẫn gom nhu cầu #101 theo người chủ trì cuộc họp gốc\n"
     "- ⚠️ Cố ý giữ như vậy để không đổi số liệu kỳ đã chốt"),
]

S10 = [
    (1, "Luồng đầy đủ: xem - bàn giao - đóng - xem lịch sử", "P0",
     "Tài khoản có quyền xem theo công ty, quyền bàn giao và quyền đóng. Nhu cầu #120 Đang theo dõi.",
     "1. Vào Meetings › Nhu cầu khách hàng, lọc tới nhu cầu #120\n2. Bàn giao #120 cho Trần Văn B kèm lý do\n"
     "3. Đăng nhập Trần Văn B, mở màn và kiểm tra nhu cầu #120\n4. Trần Văn B đóng nhu cầu kèm ghi chú\n"
     "5. Mở popup Lịch sử cập nhật của #120",
     "Người nhận: Trần Văn B · Ghi chú đóng: Khách hoãn đầu tư",
     "- Bước 2: đổi người phụ trách và phòng ban, hạn giữ nguyên\n- Bước 3: Trần Văn B thấy nhu cầu và nhận được "
     "thông báo\n- Bước 4: trạng thái chuyển 'Đóng', nút Tạo Dự án TKT biến mất\n"
     "- Bước 5: lịch sử có đủ 2 dòng Bàn giao và Đóng nhu cầu, đúng người đúng thời điểm"),

    (2, "Luồng chuyển nhu cầu thành Dự án TKT", "P0",
     "Nhu cầu #121 Đang theo dõi, chưa có dự án.",
     "1. Bấm nút Tạo Dự án TKT ở dòng #121\n2. Điền đủ thông tin bắt buộc và lưu\n3. Quay lại màn Nhu cầu khách "
     "hàng, tìm #121",
     "—",
     "- Sau khi lưu, hệ thống quay về màn danh sách\n- Nhu cầu #121 chuyển trạng thái 'Đã lập dự án TKT'\n"
     "- Cột Dự án TKT hiện mã dự án bấm được\n- Biểu tượng Bàn giao và Đóng biến mất khỏi dòng đó"),

    (3, "Luồng bàn giao hàng loạt khi nhân sự nghỉ việc", "P1",
     "Nhân viên E nghỉ việc, đang phụ trách 5 nhu cầu (4 Đang theo dõi, 1 đã đóng). Tài khoản quản lý có quyền bàn "
     "giao.",
     "1. Lọc Nhân viên = E\n2. Tích ô chọn cả trang\n3. Bàn giao hàng loạt cho Trần Văn B\n4. Lọc lại Nhân viên = E",
     "Người nhận: Trần Văn B · Lý do: E nghỉ việc",
     "- Bước 2: chỉ 4 nhu cầu Đang theo dõi được tích, nhu cầu đã đóng bị khoá ô tích\n"
     "- Bước 3: bàn giao thành công 4 nhu cầu\n- Bước 4: chỉ còn 1 nhu cầu đã đóng thuộc về E"),

    (4, "Luồng kiểm tra phạm vi 5 cấp trên cùng một tập dữ liệu", "P0",
     "Cùng 1 nhu cầu #122 của nhân viên phòng Kinh doanh 1, công ty 1.",
     "1. Lần lượt đăng nhập 5 tài khoản: cấp tổng công ty, cấp công ty (công ty 2), cấp phòng ban (phòng Kinh "
     "doanh 2), cấp bộ phận (bộ phận khác), và chính người phụ trách\n2. Mỗi lần mở màn và tìm nhu cầu #122",
     "—",
     "- Cấp tổng công ty: thấy\n- Cấp công ty của công ty 2: KHÔNG thấy\n- Cấp phòng ban của phòng khác: KHÔNG "
     "thấy\n- Cấp bộ phận của bộ phận khác: KHÔNG thấy\n- Chính người phụ trách: thấy"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "CỘT DỮ LIỆU & LIÊN KẾT SANG MÀN KHÁC", S4),
    ("V", "ĐÓNG NHU CẦU THỦ CÔNG", S5),
    ("VI", "BÀN GIAO NHU CẦU (ĐƠN LẺ)", S6),
    ("VII", "BÀN GIAO HÀNG LOẠT", S7),
    ("VIII", "LỊCH SỬ CẬP NHẬT", S8),
    ("IX", "THÔNG BÁO & DỊCH PHẠM VI XEM", S9),
    ("X", "E2E FLOW", S10),
]

if __name__ == "__main__":
    build(output_file=OUT, sheet_name="Trang tính1", feature_name=FEATURE, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
