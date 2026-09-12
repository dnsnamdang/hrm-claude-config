# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man "Bao cao ket qua cham soc khach hang tiem nang".

Chay:  python .plans/bao-cao-cskh-tiem-nang/gen_testcase.py
Engine dung chung: .claude/skills/testcase-documenter/assets/tc_engine.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

MODULE = "BC kết quả CSKH tiềm năng"

# ============================================================== 9 MỤC MÔ TẢ
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Theo dõi kết quả chăm sóc khách hàng tiềm năng trong một kỳ: có bao nhiêu nhu cầu đầu tư đang "
     "theo dõi, bao nhiêu nhu cầu đã chuyển đổi thành dự án tiền khả thi (dự án TKT), bao nhiêu nhu "
     "cầu phải đóng lại vì hết hạn.\n"
     "Nguồn số liệu là các NHU CẦU ĐẦU TƯ mà kinh doanh thu thập được khi đi họp khách hàng: trong "
     "biên bản của meeting loại \"Họp tìm hiểu & Giới thiệu sản phẩm\", khách trả lời CÓ nhu cầu đầu "
     "tư, mỗi nhóm ngành khách quan tâm được ghi thành MỘT dòng nhu cầu kèm giá trị đầu tư dự kiến "
     "và thời gian dự kiến triển khai.\n"
     "Đường vào: menu Báo cáo ▸ Kết quả CSKH tiềm năng."),

    ("2. Đối tượng được tính / hiển thị",
     "Một dòng nhu cầu được đưa vào báo cáo khi thoả ĐỦ các điều kiện sau:\n"
     "- Nằm trong biên bản của meeting loại \"Họp tìm hiểu & Giới thiệu sản phẩm\".\n"
     "- Meeting đó ở trạng thái \"Hoàn thành\".\n"
     "- Biên bản trả lời khách CÓ nhu cầu đầu tư.\n"
     "- Người xem có quyền nhìn thấy meeting đó (xem mục 7).\n"
     "Nhu cầu có 3 trạng thái, cả 3 đều được tính (khác nhau ở chỗ rơi vào chỉ tiêu nào):\n"
     "- \"Đang theo dõi\": chưa lập dự án TKT và chưa tới ngày dự kiến triển khai.\n"
     "- \"Đã lập dự án TKT\": đã được gắn vào một dự án tiền khả thi.\n"
     "- \"Không tiếp tục\": đã quá ngày dự kiến triển khai mà vẫn chưa lập dự án."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Nhu cầu thuộc meeting KHÁC loại \"Họp tìm hiểu & Giới thiệu sản phẩm\".\n"
     "- Nhu cầu thuộc meeting chưa \"Hoàn thành\" (Nháp, Chốt lịch, Đã huỷ…).\n"
     "- Nhu cầu thuộc biên bản trả lời khách KHÔNG có nhu cầu đầu tư.\n"
     "- Nhu cầu đã bị đóng từ KỲ TRƯỚC (ngày đóng nằm trước ngày đầu kỳ đang xem) — không tính vào "
     "bất kỳ chỉ tiêu nào của kỳ này.\n"
     "- Nhu cầu của meeting mà người đang xem không có quyền nhìn."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô \"Kỳ báo cáo\" quyết định khoảng [ngày đầu kỳ – ngày cuối kỳ]. Có 4 lựa chọn: Tháng này, "
     "Quý này, Năm nay, Tuỳ chỉnh (chọn Tuỳ chỉnh mới hiện thêm 2 ô Từ ngày / Đến ngày).\n"
     "Khoảng thời gian này soi vào 2 mốc khác nhau tuỳ chỉ tiêu:\n"
     "- Nhóm \"Tổng nhu cầu trong kỳ\" soi NGÀY HỌP của meeting thu thập nhu cầu.\n"
     "- Nhóm \"Tổng nhu cầu bị đóng trong kỳ\" soi NGÀY ĐÓNG của nhu cầu.\n"
     "⚠️ Ngày đóng của nhu cầu hết hạn được ghi bằng đúng NGÀY DỰ KIẾN TRIỂN KHAI, không phải ngày "
     "hệ thống chạy tác vụ đóng — nên tác vụ chạy trễ vài ngày cũng không làm lệch kỳ."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng theo dõi có tối đa 3 phần, mỗi phần 2 cấp cha ▸ con:\n"
     "- Phần I \"Theo lĩnh vực công ty kinh doanh / Nhóm ngành\": Lĩnh vực ▸ Nhóm ngành.\n"
     "- Phần II \"Theo thị trường\": Tỉnh / Thành phố ▸ Phường / xã.\n"
     "- Phần III \"Theo phòng ban / Nhân viên\": Phòng ban ▸ Kinh doanh chủ trì.\n"
     "Ô \"Tiêu chí theo dõi\" quyết định hiện phần nào: chọn \"Tất cả\" hiện đủ 3 phần; chọn 1 tiêu "
     "chí thì chỉ hiện đúng phần đó, đồng thời khối lọc riêng của tiêu chí đó mới hiện ra.\n"
     "Dòng tiêu đề của mỗi phần MANG LUÔN số tổng của phần (không có dòng \"Tổng cộng\" riêng ở "
     "cuối). Nút \"Hiện chi tiết\" trong ô tiêu đề bung/thu toàn bộ cấp con của cả 3 phần."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Mỗi nhu cầu chỉ được đếm MỘT lần trong một phần, kể cả khi cùng khách hàng có nhiều nhu cầu "
     "(mỗi nhóm ngành là một nhu cầu riêng, đếm riêng).\n"
     "- Tổng của cả 3 phần luôn BẰNG NHAU và bằng \"Tổng nhu cầu trong kỳ\" — vì 3 phần chỉ là 3 "
     "cách bổ dọc cùng một tập nhu cầu.\n"
     "- Nhu cầu thiếu thông tin phân nhóm (chưa có lĩnh vực, khách chưa gán tỉnh/phường, meeting "
     "chưa có phòng ban) được gom vào dòng \"Chưa xác định …\" chứ không bị loại khỏi tổng.\n"
     "- Một nhu cầu vừa \"phát sinh trong kỳ\" vừa \"bị đóng trong kỳ\" thì được đếm ở CẢ hai khối "
     "(khối trên là tập đang theo dõi, khối dưới là kết quả xử lý trong kỳ) — đây không phải trùng."),

    ("7. Phân quyền cấp",
     "Có 3 quyền, đặt trong nhóm quyền \"Báo cáo kết quả chăm sóc khách hàng tiềm năng\":\n"
     "- \"Xem báo cáo kết quả chăm sóc khách hàng tiềm năng theo tổng công ty\": thấy nhu cầu của "
     "mọi công ty.\n"
     "- \"Xem báo cáo kết quả chăm sóc khách hàng tiềm năng theo công ty\": chỉ thấy trong công ty "
     "của mình.\n"
     "- \"Xem báo cáo kết quả chăm sóc khách hàng tiềm năng theo phòng ban\": chỉ thấy các phòng ban "
     "mình quản lý.\n"
     "Không có quyền nào trong 3 quyền trên: vẫn vào được màn nhưng CHỈ thấy nhu cầu từ meeting do "
     "chính mình chủ trì hoặc mình có tham dự.\n"
     "Nút \"+ Tạo mới\" (tạo dự án TKT từ nhu cầu) trong cửa sổ chi tiết chỉ hiện khi có quyền "
     "\"Quản lý dự án tiền khả thi\"."),

    ("8. Cách tính các ô thống kê",
     "KHỐI \"TỔNG NHU CẦU TRONG KỲ\" = (a) + (b), trong đó:\n"
     "  (a) \"Tổng nhu cầu còn hiệu lực theo dõi\" = nhu cầu họp từ TRƯỚC ngày đầu kỳ, tới đầu kỳ "
     "vẫn chưa bị đóng.\n"
     "  (b) \"Tổng nhu cầu phát sinh trong kỳ\" = nhu cầu có ngày họp nằm trong kỳ.\n"
     "KHỐI \"TỔNG NHU CẦU BỊ ĐÓNG TRONG KỲ\" = (c) + (d), trong đó:\n"
     "  (c) \"Chuyển đổi thành dự án TKT\" = nhu cầu trạng thái \"Đã lập dự án TKT\" có ngày đóng "
     "trong kỳ.\n"
     "  (d) \"Hết hạn, không tiếp tục\" = nhu cầu trạng thái \"Không tiếp tục\" có ngày đóng trong kỳ.\n"
     "3 ô KẾT QUẢ KPI:\n"
     "  \"Tỷ lệ chuyển đổi thành công\" = (c) chia \"Tổng nhu cầu trong kỳ\".\n"
     "  \"Thành công / tổng nhu cầu đóng\" = (c) chia \"Tổng nhu cầu bị đóng trong kỳ\".\n"
     "  \"Thất bại / tổng nhu cầu đóng\" = (d) chia \"Tổng nhu cầu bị đóng trong kỳ\".\n"
     "Mỗi dòng bảng theo dõi: \"Tỷ lệ thành công\" = Chuyển đổi thành công chia Số nhu cầu của chính "
     "dòng đó. \"Tỷ trọng giá trị\": dòng CHA so với tổng giá trị cả kỳ; dòng CON so trong nội bộ "
     "dòng cha (tổng các dòng con của một cha luôn bằng 100%).\n"
     "Mẫu số bằng 0 thì ô tỷ lệ hiện 0,0% (không để trống, không báo lỗi)."),

    ("9. Ghi chú đọc bảng",
     "⚠️ Các bẫy dễ sai nhất của màn này:\n"
     "- Tiền ở BẢNG THEO DÕI được rút gọn theo tỷ (ví dụ 7,1 tỷ); tiền trong CỬA SỔ CHI TIẾT để số "
     "đầy đủ. So 2 nơi phải quy về cùng đơn vị trước khi kết luận lệch.\n"
     "- Cột \"Thời gian triển khai\" trong cửa sổ chi tiết chỉ hiện THÁNG/NĂM, không có ngày.\n"
     "- Ba phần của bảng phải có cùng một con số tổng. Lệch nhau là lỗi, không phải do lọc.\n"
     "- Tỷ trọng giá trị của các dòng CON cộng lại là 100% trong phạm vi dòng cha, KHÔNG phải 100% "
     "toàn bảng — đừng cộng dọc cả cột rồi báo sai.\n"
     "- Đổi \"Tiêu chí theo dõi\" thì các ô lọc của tiêu chí cũ bị XOÁ GIÁ TRỊ và ẩn đi; số liệu sẽ "
     "đổi theo. Đây là hành vi đúng, không phải mất bộ lọc.\n"
     "- Cửa sổ chi tiết ẩn ô lọc của chính cơ cấu đang xem (đang xem theo thị trường thì không có ô "
     "lọc Tỉnh/Thành phố nữa) và cũng bỏ cơ cấu đó khỏi khối \"Phân bổ nhu cầu theo cơ cấu\".\n"
     "- Cửa sổ chi tiết của nhóm \"Hết hạn, không tiếp tục\" KHÔNG có khối kết quả KPI (vì luôn là "
     "0% / 0% / 100%, không nói lên điều gì).\n"
     "- Nhu cầu KHÔNG có ngày dự kiến triển khai thì không bao giờ tự đóng, sẽ nằm mãi ở \"Đang theo "
     "dõi\".\n"
     "- Số 0 vẫn hiển thị là 0 và vẫn bấm được để mở cửa sổ chi tiết (danh sách rỗng), không bị ẩn."),
]

# ============================================================== PHÂN QUYỀN
P_ALL = "Xem báo cáo kết quả chăm sóc khách hàng tiềm năng theo tổng công ty"
P_COM = "Xem báo cáo kết quả chăm sóc khách hàng tiềm năng theo công ty"
P_DEP = "Xem báo cáo kết quả chăm sóc khách hàng tiềm năng theo phòng ban"
P_PRJ = "Quản lý dự án tiền khả thi"

ROLE_TCS = [
    ("01",
     "Có quyền xem theo tổng công ty thì thấy nhu cầu của mọi công ty",
     "P0",
     "Trong Tháng này có 3 nhu cầu của công ty A và 2 nhu cầu của công ty B.\n"
     "Tài khoản T thuộc công ty A, chỉ được gán quyền \"" + P_ALL + "\".",
     "1. Đăng nhập bằng tài khoản T.\n"
     "2. Vào menu Báo cáo ▸ Kết quả CSKH tiềm năng.\n"
     "3. Để Kỳ báo cáo = Tháng này, Tiêu chí theo dõi = Tất cả.\n"
     "4. Đọc ô \"TỔNG NHU CẦU TRONG KỲ\".",
     "Kỳ báo cáo: Tháng này",
     "- Ô \"TỔNG NHU CẦU TRONG KỲ\" hiện 5 nhu cầu (gộp cả 2 công ty).\n"
     "- Ô lọc \"Công ty\" CÓ hiện trên màn và chọn được cả công ty A lẫn công ty B.\n"
     "- Phần III \"Theo phòng ban / Nhân viên\" liệt kê phòng ban của cả 2 công ty."),

    ("02",
     "Có quyền xem theo công ty thì chỉ thấy nhu cầu trong công ty mình",
     "P0",
     "Dữ liệu như trường hợp trên (công ty A: 3 nhu cầu, công ty B: 2 nhu cầu).\n"
     "Tài khoản T thuộc công ty A, chỉ được gán quyền \"" + P_COM + "\".",
     "1. Đăng nhập bằng tài khoản T.\n"
     "2. Vào Báo cáo ▸ Kết quả CSKH tiềm năng.\n"
     "3. Đọc ô \"TỔNG NHU CẦU TRONG KỲ\" và mở cửa sổ chi tiết bằng cách bấm vào con số đó.",
     "Kỳ báo cáo: Tháng này",
     "- Ô \"TỔNG NHU CẦU TRONG KỲ\" hiện 3 nhu cầu, KHÔNG có nhu cầu nào của công ty B.\n"
     "- Cửa sổ chi tiết liệt kê đúng 3 dòng, mọi dòng đều thuộc công ty A.\n"
     "- ⚠️ Ô lọc \"Công ty\" KHÔNG hiện (chỉ cấp tổng công ty mới có ô này)."),

    ("03",
     "Có quyền xem theo phòng ban thì chỉ thấy phòng ban mình quản lý",
     "P0",
     "Trong Tháng này: phòng P1 có 4 nhu cầu, phòng P2 có 3 nhu cầu (cùng công ty A).\n"
     "Tài khoản T được đặt làm quản lý phòng P1, chỉ được gán quyền \"" + P_DEP + "\".",
     "1. Đăng nhập bằng tài khoản T.\n"
     "2. Vào Báo cáo ▸ Kết quả CSKH tiềm năng.\n"
     "3. Đọc phần III \"Theo phòng ban / Nhân viên\".",
     "Kỳ báo cáo: Tháng này",
     "- Phần III chỉ có dòng phòng P1 với 4 nhu cầu; KHÔNG có dòng phòng P2.\n"
     "- Ô \"TỔNG NHU CẦU TRONG KỲ\" hiện 4 nhu cầu.\n"
     "- Ô lọc \"Phòng ban\" chỉ liệt kê phòng P1."),

    ("04",
     "Không có quyền nào thì chỉ thấy nhu cầu từ meeting của chính mình",
     "P0",
     "Trong Tháng này có 6 nhu cầu, trong đó 2 nhu cầu thuộc meeting do tài khoản T chủ trì, "
     "1 nhu cầu thuộc meeting T có tham dự, 3 nhu cầu còn lại T không liên quan.\n"
     "Tài khoản T KHÔNG được gán bất kỳ quyền nào trong 3 quyền xem báo cáo này.",
     "1. Đăng nhập bằng tài khoản T.\n"
     "2. Vào Báo cáo ▸ Kết quả CSKH tiềm năng.\n"
     "3. Đọc ô \"TỔNG NHU CẦU TRONG KỲ\" rồi bấm vào con số để mở cửa sổ chi tiết.",
     "Kỳ báo cáo: Tháng này",
     "- ⚠️ Màn vẫn mở được, KHÔNG chặn vào màn.\n"
     "- Ô \"TỔNG NHU CẦU TRONG KỲ\" hiện đúng 3 nhu cầu (2 chủ trì + 1 tham dự).\n"
     "- ⚠️ Đây là điểm dễ lọt lỗ hổng nhất: nếu thấy đủ 6 nhu cầu thì báo lỗi ngay, hệ thống đang "
     "để lộ dữ liệu của người khác."),

    ("05",
     "Tài khoản mới tinh, chưa gắn meeting nào thì báo cáo rỗng chứ không lỗi",
     "P0",
     "Tài khoản M vừa tạo, không có quyền xem báo cáo, chưa chủ trì và chưa tham dự meeting nào.",
     "1. Đăng nhập bằng tài khoản M.\n"
     "2. Vào Báo cáo ▸ Kết quả CSKH tiềm năng.",
     "—",
     "- Mọi ô của khối tổng hợp hiện 0 nhu cầu · 0 đ.\n"
     "- 3 ô kết quả KPI hiện 0,0%.\n"
     "- Bảng theo dõi hiện đủ 3 dòng tiêu đề phần với số 0, không có dòng con.\n"
     "- ⚠️ Không có thông báo lỗi đỏ, không trang trắng."),

    ("06",
     "Gọi thẳng chức năng lấy số liệu, bỏ qua giao diện, vẫn bị chặn theo quyền",
     "P0",
     "Tài khoản T không có quyền xem báo cáo và không liên quan meeting nào trong kỳ.",
     "1. Đăng nhập bằng tài khoản T, lấy phiên đăng nhập hiện tại.\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy số liệu báo cáo, bỏ qua giao diện.\n"
     "3. Đọc kết quả trả về.",
     "Kỳ báo cáo: Tháng này",
     "- Kết quả trả về rỗng (0 nhu cầu), không kèm dữ liệu của người khác.\n"
     "- ⚠️ Phải kiểm cả cách này: giao diện có ẩn đi nhưng chức năng vẫn trả dữ liệu thì vẫn là lỗ "
     "hổng."),

    ("07",
     "Gọi thẳng chức năng xuất tệp Excel, bỏ qua giao diện, vẫn bị chặn theo quyền",
     "P1",
     "Tài khoản T như trường hợp trên.",
     "1. Đăng nhập bằng tài khoản T.\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xuất Excel của báo cáo và của danh sách chi "
     "tiết, bỏ qua giao diện.\n"
     "3. Mở 2 tệp tải về.",
     "Kỳ báo cáo: Tháng này",
     "- Tệp tải về vẫn mở được nhưng không có dòng dữ liệu nào của người khác.\n"
     "- Tệp danh sách chi tiết chỉ còn dòng tiêu đề và dòng \"Không có dữ liệu\"."),

    ("08",
     "Nút \"+ Tạo mới\" dự án TKT chỉ hiện khi có quyền quản lý dự án tiền khả thi",
     "P1",
     "Tài khoản T có quyền xem báo cáo theo công ty nhưng KHÔNG có quyền \"" + P_PRJ + "\".\n"
     "Trong kỳ có ít nhất 1 nhu cầu trạng thái \"Đang theo dõi\".",
     "1. Đăng nhập bằng tài khoản T.\n"
     "2. Mở báo cáo, bấm vào con số của ô \"TỔNG NHU CẦU TRONG KỲ\".\n"
     "3. Xem cột cuối của bảng trong cửa sổ chi tiết.",
     "—",
     "- Cột cuối KHÔNG có nút \"+ Tạo mới\" ở bất kỳ dòng nào.\n"
     "- ⚠️ Nút phải bị ẩn hẳn, không được hiện dạng xám bấm không ăn.\n"
     "- Gán thêm quyền \"" + P_PRJ + "\" rồi tải lại màn thì nút xuất hiện."),
]

# ============================================================== SECTIONS
S1 = [
    (1, "Vào màn từ menu Báo cáo", "P0",
     "Tài khoản có quyền \"" + P_ALL + "\".",
     "1. Đăng nhập.\n2. Bấm menu Báo cáo ở cột trái.\n3. Bấm mục \"Kết quả CSKH tiềm năng\".",
     "—",
     "- Mở đúng màn, tiêu đề trên thanh trên cùng là \"Báo cáo kết quả chăm sóc khách hàng tiềm năng\".\n"
     "- Mục \"Kết quả CSKH tiềm năng\" nằm ngay dưới mục \"Kết quả meeting theo thị trường\"."),

    (2, "Thứ tự các khối trên màn", "P0",
     "Kỳ hiện tại có ít nhất 5 nhu cầu.",
     "1. Mở màn báo cáo.\n2. Đọc từ trên xuống.",
     "—",
     "- Thứ tự đúng: bộ lọc → dải tổng hợp (2 khối) → 3 ô kết quả KPI → bảng theo dõi.\n"
     "- Dải tổng hợp có dòng \"Tổng hợp kỳ dd/mm/yyyy – dd/mm/yyyy\" kèm tổng số nhu cầu và tổng giá "
     "trị đầu tư dự kiến."),

    (3, "Mặc định khi mới vào màn", "P0",
     "Hôm nay là một ngày bất kỳ trong tháng.",
     "1. Mở màn báo cáo lần đầu (chưa đụng vào bộ lọc).",
     "—",
     "- Ô \"Kỳ báo cáo\" mặc định \"Tháng này\"; ô \"Tiêu chí theo dõi\" mặc định \"Tất cả\".\n"
     "- Số liệu đã tải sẵn, không phải bấm \"Tìm kiếm\" mới có.\n"
     "- Khối bộ lọc đang ở trạng thái thu gọn, nút bên phải ghi \"Hiện bộ lọc\"."),

    (4, "Hai khối tổng hợp có đủ ô con", "P0",
     "Kỳ hiện tại có dữ liệu.",
     "1. Mở màn báo cáo.\n2. Đọc dải tổng hợp.",
     "—",
     "- Khối trái: \"TỔNG NHU CẦU TRONG KỲ\" + 2 ô con \"Tổng nhu cầu còn hiệu lực theo dõi\" và "
     "\"Tổng nhu cầu phát sinh trong kỳ\".\n"
     "- Khối phải: \"TỔNG NHU CẦU BỊ ĐÓNG TRONG KỲ\" + 2 ô con \"Chuyển đổi thành dự án TKT\" và "
     "\"Hết hạn, không tiếp tục\".\n"
     "- Mỗi ô hiện SỐ NHU CẦU (chữ to) kèm GIÁ TRỊ rút gọn theo tỷ ở bên cạnh."),

    (5, "Ba ô kết quả KPI có đủ nhãn và tử/mẫu", "P0",
     "Kỳ hiện tại có ít nhất 1 nhu cầu bị đóng.",
     "1. Mở màn báo cáo.\n2. Đọc khối \"KẾT QUẢ KPI\".",
     "—",
     "- Đủ 3 ô: \"Tỷ lệ chuyển đổi thành công\", \"Thành công / tổng nhu cầu đóng\", \"Thất bại / "
     "tổng nhu cầu đóng\".\n"
     "- Mỗi ô hiện phần trăm 1 chữ số thập phân kèm tử số / mẫu số bên cạnh (ví dụ 25,0% và 2 / 8).\n"
     "- Mỗi ô có thanh tiến độ dài đúng theo tỷ lệ."),

    (6, "Nút thu gọn dải tổng hợp", "P1",
     "Kỳ hiện tại có dữ liệu.",
     "1. Mở màn báo cáo.\n2. Bấm nút \"Thu gọn\" ở góc phải dải tổng hợp.\n3. Bấm lại nút đó.",
     "—",
     "- Lần 1: 2 khối tổng hợp và 3 ô KPI bị ẩn, bảng theo dõi trồi lên; chữ trên nút đổi thành "
     "\"Mở rộng\".\n"
     "- Lần 2: mọi thứ hiện lại như cũ, chữ trên nút quay về \"Thu gọn\"."),

    (7, "Icon chữ i giải thích từng chỉ tiêu", "P1",
     "Kỳ hiện tại có dữ liệu.",
     "1. Mở màn báo cáo.\n2. Rê chuột / bấm vào icon chữ i cạnh dòng \"Tổng hợp kỳ…\", cạnh tên 2 "
     "khối, cạnh 4 ô con và cạnh tiêu đề \"KẾT QUẢ KPI\".",
     "—",
     "- Mỗi icon bung một khung giải thích ngắn nói rõ chỉ tiêu đó lấy dữ liệu như thế nào.\n"
     "- Nội dung có ghép số liệu thật của kỳ đang xem, không phải chữ mẫu."),

    (8, "Cột trong bảng theo dõi đúng và đủ", "P0",
     "Kỳ hiện tại có dữ liệu.",
     "1. Mở màn báo cáo.\n2. Đọc dòng tiêu đề của bảng theo dõi.",
     "—",
     "- Đủ 8 cột theo thứ tự: STT, Nội dung theo dõi, Số nhu cầu, Giá trị dự kiến, Chuyển đổi thành "
     "công, Tỷ lệ thành công, Không tiếp tục, Tỷ trọng giá trị.\n"
     "- ⚠️ Cột thứ 7 phải là \"Không tiếp tục\", KHÔNG phải \"Hết hạn theo dõi\"."),

    (9, "Ba phần của bảng theo dõi", "P0",
     "Kỳ hiện tại có dữ liệu đủ cả 3 cơ cấu.",
     "1. Mở màn báo cáo với Tiêu chí theo dõi = Tất cả.\n2. Đọc bảng theo dõi.",
     "—",
     "- Đủ 3 dòng tiêu đề phần đánh số I, II, III: \"THEO LĨNH VỰC CÔNG TY KINH DOANH / NHÓM NGÀNH\", "
     "\"THEO THỊ TRƯỜNG\", \"THEO PHÒNG BAN / NHÂN VIÊN\".\n"
     "- 3 dòng tiêu đề này MANG LUÔN số tổng, không có dòng \"Tổng cộng\" riêng phía dưới."),

    (10, "Kỳ không có dữ liệu", "P0",
     "Chọn một kỳ chắc chắn không có nhu cầu nào (ví dụ một tháng của năm trước).",
     "1. Mở màn báo cáo.\n2. Bấm \"Hiện bộ lọc\", chọn Kỳ báo cáo = Tuỳ chỉnh.\n"
     "3. Nhập Từ ngày / Đến ngày là một tháng không có dữ liệu.\n4. Bấm \"Tìm kiếm\".",
     "Từ ngày: 01/01/2020 — Đến ngày: 31/01/2020",
     "- Mọi ô của 2 khối tổng hợp hiện 0 nhu cầu · 0 đ.\n"
     "- 3 ô KPI hiện 0,0%.\n"
     "- Bảng vẫn hiện đủ 3 dòng tiêu đề phần với số 0, không có dòng con.\n"
     "- ⚠️ Không có thông báo lỗi đỏ."),

    (11, "Tải lại trang giữ nguyên kết quả đang xem", "P2",
     "Đang xem báo cáo với Kỳ = Quý này, Tiêu chí = Thị trường.",
     "1. Nhấn phím tải lại trang.\n2. Đợi màn tải xong.",
     "—",
     "- Màn tải lại bình thường, không lỗi.\n"
     "- ⚠️ Bộ lọc quay về mặc định (Tháng này / Tất cả) — đây là hành vi hiện tại, ghi nhận đúng như "
     "vậy khi test."),

    (12, "Màn hiển thị đúng ở độ phân giải nhỏ", "P2",
     "Kỳ hiện tại có nhiều dòng dữ liệu.",
     "1. Thu nhỏ cửa sổ trình duyệt còn khoảng chiều rộng của laptop 13 inch.\n"
     "2. Đọc bảng theo dõi.",
     "—",
     "- Bảng có thanh cuộn ngang riêng, KHÔNG làm cả trang trượt ngang.\n"
     "- Ô tiêu đề của cột đầu vẫn nhìn thấy khi cuộn ngang.\n"
     "- Nút \"Hiện chi tiết\" trong ô tiêu đề không bị dòng tiêu đề che mất."),
]

S2 = [
    (1, "Mở / đóng khối bộ lọc", "P1",
     "Đang ở màn báo cáo.",
     "1. Bấm nút \"Hiện bộ lọc\" ở góc phải khối bộ lọc.\n2. Bấm lại nút đó.",
     "—",
     "- Lần 1: các ô lọc bung ra, chữ trên nút đổi thành \"Ẩn bộ lọc\".\n"
     "- Lần 2: các ô lọc thu lại, chữ quay về \"Hiện bộ lọc\"."),

    (2, "Kỳ báo cáo có đủ 4 lựa chọn", "P0",
     "Đang mở khối bộ lọc.",
     "1. Bấm vào ô \"Kỳ báo cáo\".\n2. Đọc danh sách.",
     "—",
     "- Đủ 4 lựa chọn theo thứ tự: Tháng này, Quý này, Năm nay, Tuỳ chỉnh.\n"
     "- ⚠️ KHÔNG có lựa chọn \"Tất cả\" — báo cáo luôn tính theo một kỳ."),

    (3, "Chọn Tháng này ra đúng mốc đầu/cuối tháng", "P0",
     "Hôm nay là 26/08/2026.",
     "1. Chọn Kỳ báo cáo = Tháng này.\n2. Bấm \"Tìm kiếm\".\n3. Đọc dòng \"Tổng hợp kỳ…\".",
     "Kỳ báo cáo: Tháng này",
     "- Dòng ghi \"Tổng hợp kỳ 01/08/2026 – 31/08/2026\"."),

    (4, "Chọn Quý này ra đúng mốc đầu/cuối quý", "P0",
     "Hôm nay là 26/08/2026 (quý 3).",
     "1. Chọn Kỳ báo cáo = Quý này.\n2. Bấm \"Tìm kiếm\".",
     "Kỳ báo cáo: Quý này",
     "- Dòng \"Tổng hợp kỳ 01/07/2026 – 30/09/2026\".\n"
     "- Số nhu cầu lớn hơn hoặc bằng khi chọn Tháng này (kỳ rộng hơn)."),

    (5, "Chọn Năm nay ra đúng mốc đầu/cuối năm", "P1",
     "Hôm nay là 26/08/2026.",
     "1. Chọn Kỳ báo cáo = Năm nay.\n2. Bấm \"Tìm kiếm\".",
     "Kỳ báo cáo: Năm nay",
     "- Dòng \"Tổng hợp kỳ 01/01/2026 – 31/12/2026\"."),

    (6, "Chọn Tuỳ chỉnh mới hiện 2 ô ngày", "P0",
     "Đang mở khối bộ lọc, Kỳ báo cáo đang là Tháng này.",
     "1. Đọc hàng lọc (chưa có ô ngày).\n2. Đổi Kỳ báo cáo sang Tuỳ chỉnh.\n3. Đọc lại hàng lọc.",
     "Kỳ báo cáo: Tuỳ chỉnh",
     "- Trước khi đổi: không có ô \"Từ ngày\" và \"Đến ngày\".\n"
     "- Sau khi đổi: 2 ô xuất hiện ngay sau ô \"Kỳ báo cáo\", trước ô \"Tiêu chí theo dõi\".\n"
     "- Hàng lọc vẫn đủ một hàng, không bị hụt nửa hàng."),

    (7, "Kỳ tuỳ chỉnh lọc đúng khoảng ngày", "P0",
     "Có 3 nhu cầu họp ngày 05/08/2026 và 2 nhu cầu họp ngày 20/08/2026.",
     "1. Chọn Kỳ báo cáo = Tuỳ chỉnh.\n2. Nhập Từ ngày 01/08/2026, Đến ngày 10/08/2026.\n"
     "3. Bấm \"Tìm kiếm\".",
     "Từ ngày: 01/08/2026 — Đến ngày: 10/08/2026",
     "- Ô \"Tổng nhu cầu phát sinh trong kỳ\" chỉ đếm 3 nhu cầu ngày 05/08.\n"
     "- 2 nhu cầu ngày 20/08 không xuất hiện trong cửa sổ chi tiết của ô đó."),

    (8, "Nhập ngược mốc Từ ngày / Đến ngày", "P1",
     "Có dữ liệu trong tháng 8/2026.",
     "1. Chọn Kỳ báo cáo = Tuỳ chỉnh.\n2. Nhập Từ ngày 31/08/2026, Đến ngày 01/08/2026.\n"
     "3. Bấm \"Tìm kiếm\".",
     "Từ ngày: 31/08/2026 — Đến ngày: 01/08/2026",
     "- ⚠️ Hệ thống tự đảo lại thành 01/08/2026 – 31/08/2026 và ra số liệu bình thường.\n"
     "- KHÔNG trả về kỳ rỗng làm mọi chỉ tiêu bằng 0 một cách khó hiểu."),

    (9, "Chọn Tuỳ chỉnh mà bỏ trống ngày", "P1",
     "Có dữ liệu trong tháng hiện tại.",
     "1. Chọn Kỳ báo cáo = Tuỳ chỉnh, để trống cả 2 ô ngày.\n2. Bấm \"Tìm kiếm\".",
     "Từ ngày: (trống) — Đến ngày: (trống)",
     "- Hệ thống lấy mặc định là tháng hiện tại, dòng \"Tổng hợp kỳ…\" hiện đúng đầu/cuối tháng này.\n"
     "- Không báo lỗi, không trang trắng."),

    (10, "Tiêu chí theo dõi có đủ 4 lựa chọn", "P0",
     "Đang mở khối bộ lọc.",
     "1. Bấm ô \"Tiêu chí theo dõi\".\n2. Đọc danh sách.",
     "—",
     "- Đủ 4: Tất cả; Lĩnh vực công ty kinh doanh / Nhóm ngành; Thị trường; Phòng ban / Nhân viên."),

    (11, "Chọn tiêu chí Lĩnh vực thì bảng chỉ còn phần I", "P0",
     "Kỳ hiện tại có dữ liệu đủ 3 cơ cấu.",
     "1. Đổi Tiêu chí theo dõi sang \"Lĩnh vực công ty kinh doanh / Nhóm ngành\".\n"
     "2. Đọc bảng theo dõi và hàng lọc.",
     "Tiêu chí theo dõi: Lĩnh vực công ty kinh doanh / Nhóm ngành",
     "- Bảng chỉ còn MỘT phần \"THEO LĨNH VỰC CÔNG TY KINH DOANH / NHÓM NGÀNH\".\n"
     "- Hàng lọc hiện thêm 2 ô \"Lĩnh vực công ty kinh doanh\" và \"Nhóm ngành\".\n"
     "- Các ô Tỉnh/Thành phố, Phường/xã, Công ty, Phòng ban, Nhân viên biến mất.\n"
     "- Bảng tự tải lại ngay, không phải bấm \"Tìm kiếm\"."),

    (12, "Chọn tiêu chí Thị trường thì bảng chỉ còn phần II", "P0",
     "Kỳ hiện tại có dữ liệu đủ 3 cơ cấu.",
     "1. Đổi Tiêu chí theo dõi sang \"Thị trường\".\n2. Đọc bảng và hàng lọc.",
     "Tiêu chí theo dõi: Thị trường",
     "- Bảng chỉ còn phần \"THEO THỊ TRƯỜNG\".\n"
     "- Hàng lọc hiện 2 ô \"Tỉnh / Thành phố\" và \"Phường / xã\"."),

    (13, "Chọn tiêu chí Phòng ban thì bảng chỉ còn phần III", "P0",
     "Kỳ hiện tại có dữ liệu đủ 3 cơ cấu; tài khoản có quyền xem theo tổng công ty.",
     "1. Đổi Tiêu chí theo dõi sang \"Phòng ban / Nhân viên\".\n2. Đọc bảng và hàng lọc.",
     "Tiêu chí theo dõi: Phòng ban / Nhân viên",
     "- Bảng chỉ còn phần \"THEO PHÒNG BAN / NHÂN VIÊN\".\n"
     "- Hàng lọc hiện các ô Công ty, Phòng ban, Nhân viên.\n"
     "- ⚠️ KHÔNG có ô \"Bộ phận\" — ô này đã bỏ hẳn theo bản thiết kế đã duyệt."),

    (14, "Đổi tiêu chí thì xoá giá trị của khối lọc cũ", "P0",
     "Đang chọn Tiêu chí = Thị trường và đã chọn Tỉnh/Thành phố = Thành phố Hà Nội, số liệu đang bị "
     "lọc còn 6 nhu cầu (tổng kỳ là 8).",
     "1. Đổi Tiêu chí theo dõi sang \"Lĩnh vực công ty kinh doanh / Nhóm ngành\".\n"
     "2. Đọc lại ô \"TỔNG NHU CẦU TRONG KỲ\".\n3. Đổi ngược về \"Thị trường\", xem ô Tỉnh/Thành phố.",
     "Tỉnh / Thành phố: Thành phố Hà Nội",
     "- Sau bước 1: số quay về 8 nhu cầu (giá trị lọc theo Hà Nội đã bị xoá, không lọc ngầm).\n"
     "- Sau bước 3: ô \"Tỉnh / Thành phố\" trống trở lại, không tự nhớ giá trị cũ.\n"
     "- ⚠️ Đây là điểm dễ sai nhất của bộ lọc: giữ lại giá trị cũ mà ẩn ô đi sẽ khiến người dùng "
     "thấy số liệu bị lọc mà không hiểu vì sao."),

    (15, "Cascade Lĩnh vực ▸ Nhóm ngành", "P0",
     "Kỳ hiện tại có 2 lĩnh vực; lĩnh vực \"Công nghiệp\" có 3 nhóm ngành, lĩnh vực còn lại có 2 nhóm.",
     "1. Chọn Tiêu chí = Lĩnh vực công ty kinh doanh / Nhóm ngành.\n"
     "2. Mở ô \"Nhóm ngành\", đếm số mục.\n3. Chọn \"Lĩnh vực công ty kinh doanh\" = Công nghiệp.\n"
     "4. Mở lại ô \"Nhóm ngành\", đếm số mục.",
     "Lĩnh vực công ty kinh doanh: Công nghiệp",
     "- Bước 2: ô Nhóm ngành liệt kê cả 5 nhóm.\n"
     "- Bước 4: chỉ còn 3 nhóm thuộc lĩnh vực Công nghiệp."),

    (16, "Đổi ô cha thì xoá giá trị ô con", "P0",
     "Đã chọn Lĩnh vực = Công nghiệp và Nhóm ngành = Luyện Kim.",
     "1. Đổi ô \"Lĩnh vực công ty kinh doanh\" sang lĩnh vực khác.\n2. Nhìn ô \"Nhóm ngành\".",
     "—",
     "- Ô \"Nhóm ngành\" bị xoá trắng, không còn treo giá trị Luyện Kim vốn không thuộc lĩnh vực mới."),

    (17, "Cascade Tỉnh/Thành phố ▸ Phường/xã", "P0",
     "Kỳ hiện tại có nhu cầu ở Thành phố Hà Nội (2 phường) và Thành phố Cần Thơ (1 phường).",
     "1. Chọn Tiêu chí = Thị trường.\n2. Mở ô \"Phường / xã\", đếm số mục.\n"
     "3. Chọn Tỉnh / Thành phố = Thành phố Hà Nội.\n4. Mở lại ô \"Phường / xã\".",
     "Tỉnh / Thành phố: Thành phố Hà Nội",
     "- Bước 2: liệt kê cả 3 phường.\n- Bước 4: chỉ còn 2 phường của Hà Nội."),

    (18, "Cascade Phòng ban ▸ Nhân viên", "P0",
     "Kỳ hiện tại có 2 phòng ban, mỗi phòng có ít nhất 1 người chủ trì meeting.",
     "1. Chọn Tiêu chí = Phòng ban / Nhân viên.\n2. Mở ô \"Nhân viên\", đếm số mục.\n"
     "3. Chọn một phòng ban.\n4. Mở lại ô \"Nhân viên\".",
     "—",
     "- Sau bước 3, ô \"Nhân viên\" chỉ còn người thuộc phòng ban vừa chọn."),

    (19, "Ô lọc chỉ liệt kê mục CÓ dữ liệu trong kỳ", "P1",
     "Danh mục có 20 nhóm ngành, nhưng kỳ đang xem chỉ có nhu cầu thuộc 3 nhóm ngành.",
     "1. Mở ô \"Nhóm ngành\" khi Tiêu chí = Lĩnh vực.\n2. Đếm số mục.",
     "—",
     "- Chỉ liệt kê 3 nhóm ngành thật sự có nhu cầu trong kỳ.\n"
     "- ⚠️ Không đổ toàn bộ danh mục ra để người dùng chọn rồi nhận về bảng rỗng."),

    (20, "Lọc theo phòng ban ra đúng số liệu", "P0",
     "Trong kỳ: phòng \"PHÒNG THIẾT BỊ Ô TÔ 2\" có 5 nhu cầu, các phòng khác có 3 nhu cầu.",
     "1. Chọn Tiêu chí = Phòng ban / Nhân viên.\n2. Chọn Phòng ban = PHÒNG THIẾT BỊ Ô TÔ 2.\n"
     "3. Bấm \"Tìm kiếm\".",
     "Phòng ban: PHÒNG THIẾT BỊ Ô TÔ 2",
     "- Ô \"TỔNG NHU CẦU TRONG KỲ\" hiện 5 nhu cầu.\n"
     "- Bảng chỉ còn dòng của phòng ban đó.\n"
     "- ⚠️ Kiểm cả việc chọn xong bấm Tìm kiếm thì con số THẬT SỰ đổi — bộ lọc gắn sai thì chọn xong "
     "số vẫn nguyên."),

    (21, "Lọc theo nhân viên chủ trì", "P0",
     "Trong kỳ có 2 người chủ trì meeting, người A có 5 nhu cầu, người B có 3 nhu cầu.",
     "1. Chọn Tiêu chí = Phòng ban / Nhân viên.\n2. Chọn Nhân viên = người A.\n3. Bấm \"Tìm kiếm\".",
     "—",
     "- Tổng còn 5 nhu cầu; cửa sổ chi tiết chỉ có meeting do người A chủ trì."),

    (22, "Nút Xóa lọc trả mọi ô về mặc định", "P0",
     "Đã chọn Kỳ = Quý này, Tiêu chí = Thị trường, Tỉnh/Thành phố = Thành phố Cần Thơ.",
     "1. Bấm nút \"Xóa lọc\".\n2. Đọc lại các ô lọc và số liệu.",
     "—",
     "- Kỳ báo cáo về \"Tháng này\", Tiêu chí về \"Tất cả\", mọi ô lọc còn lại trống.\n"
     "- Bảng hiện lại đủ 3 phần và số liệu tải lại ngay."),

    (23, "Bố cục hàng lọc không vỡ", "P0",
     "Tài khoản có quyền xem theo tổng công ty (có thêm ô Công ty).",
     "1. Mở khối bộ lọc với Tiêu chí = Tất cả.\n2. Quan sát vị trí các ô.\n"
     "3. Lần lượt đổi Tiêu chí sang 3 lựa chọn còn lại và quan sát lại.",
     "—",
     "- Các ô lọc nằm thẳng hàng, rộng bằng nhau, không có ô nào co lại bằng nửa ô khác.\n"
     "- ⚠️ Khối Công ty / Phòng ban / Nhân viên phải nằm CÙNG lưới với ô \"Kỳ báo cáo\", không bị "
     "thụt vào thành cột hẹp xếp dọc."),

    (24, "Ô lọc giữ nguyên khi chỉ mở/đóng khối bộ lọc", "P2",
     "Đã chọn Tiêu chí = Thị trường và Tỉnh/Thành phố = Thành phố Hà Nội.",
     "1. Bấm \"Ẩn bộ lọc\".\n2. Bấm \"Hiện bộ lọc\".\n3. Đọc lại các ô.",
     "—",
     "- Mọi giá trị đang chọn còn nguyên, số liệu không đổi."),

    (25, "Lọc ra tập rỗng", "P1",
     "Chọn tổ hợp chắc chắn không có dữ liệu (ví dụ Tỉnh/Thành phố có nhu cầu nhưng Phường/xã thuộc "
     "tỉnh khác).",
     "1. Chọn Tiêu chí = Thị trường.\n2. Chọn một Tỉnh/Thành phố.\n"
     "3. Chọn Phường/xã, rồi đổi Tỉnh/Thành phố sang tỉnh khác.\n4. Bấm \"Tìm kiếm\".",
     "—",
     "- Vì đổi tỉnh đã xoá phường nên kết quả vẫn hợp lệ, không ra tập rỗng vô lý.\n"
     "- Nếu cố tình lọc ra tập rỗng thì mọi ô hiện 0 và bảng không có dòng con, không lỗi."),

    (26, "Bộ lọc áp dụng đồng thời cho bảng, cửa sổ chi tiết và tệp xuất ra", "P0",
     "Kỳ hiện tại có 8 nhu cầu, lọc theo Tỉnh/Thành phố = Thành phố Hà Nội còn 6 nhu cầu.",
     "1. Chọn Tiêu chí = Thị trường, Tỉnh/Thành phố = Thành phố Hà Nội, bấm \"Tìm kiếm\".\n"
     "2. Đọc ô \"TỔNG NHU CẦU TRONG KỲ\".\n3. Bấm vào con số đó để mở cửa sổ chi tiết, đếm dòng.\n"
     "4. Đóng cửa sổ, bấm \"Xuất Excel\", mở tệp và đếm dòng dữ liệu.",
     "Tỉnh / Thành phố: Thành phố Hà Nội",
     "- Cả 3 nơi đều là 6 nhu cầu.\n"
     "- ⚠️ Lệch nhau là lỗi nghiêm trọng: tệp gửi cho lãnh đạo sẽ khác số trên màn."),
]

S3 = [
    (1, "Khối trên bằng tổng 2 ô con", "P0",
     "Kỳ hiện tại: còn hiệu lực theo dõi 3 nhu cầu, phát sinh trong kỳ 5 nhu cầu.",
     "1. Mở màn báo cáo.\n2. Cộng tay 2 ô con rồi so với ô \"TỔNG NHU CẦU TRONG KỲ\".",
     "Kỳ báo cáo: Tháng này",
     "- \"TỔNG NHU CẦU TRONG KỲ\" = 8 = 3 + 5.\n"
     "- Giá trị tiền của ô tổng cũng bằng tổng tiền 2 ô con."),

    (2, "Khối dưới bằng tổng 2 ô con", "P0",
     "Kỳ hiện tại: chuyển đổi thành dự án TKT 2 nhu cầu, hết hạn không tiếp tục 1 nhu cầu.",
     "1. Mở màn báo cáo.\n2. Cộng tay 2 ô con rồi so với ô \"TỔNG NHU CẦU BỊ ĐÓNG TRONG KỲ\".",
     "Kỳ báo cáo: Tháng này",
     "- \"TỔNG NHU CẦU BỊ ĐÓNG TRONG KỲ\" = 3 = 2 + 1."),

    (3, "Ô Còn hiệu lực theo dõi lấy đúng nhu cầu kỳ trước", "P0",
     "Có nhu cầu N1 họp ngày 15/07/2026, tới 01/08/2026 vẫn \"Đang theo dõi\".\n"
     "Có nhu cầu N2 họp ngày 10/07/2026, đã đóng ngày 20/07/2026.",
     "1. Chọn Kỳ = Tuỳ chỉnh, Từ 01/08/2026 đến 31/08/2026.\n"
     "2. Bấm vào con số ô \"Tổng nhu cầu còn hiệu lực theo dõi\".",
     "Từ ngày: 01/08/2026 — Đến ngày: 31/08/2026",
     "- Danh sách CÓ nhu cầu N1.\n"
     "- ⚠️ KHÔNG có nhu cầu N2 (đã đóng từ kỳ trước, phải bị loại hoàn toàn)."),

    (4, "Ô Phát sinh trong kỳ lấy đúng theo ngày họp", "P0",
     "Nhu cầu N3 thuộc meeting họp ngày 12/08/2026.",
     "1. Chọn Kỳ = Tháng này (tháng 8/2026).\n"
     "2. Bấm con số ô \"Tổng nhu cầu phát sinh trong kỳ\", tìm N3.",
     "—",
     "- N3 có trong danh sách.\n"
     "- Đổi kỳ sang tháng 7/2026 thì N3 biến mất khỏi ô này."),

    (5, "Nhu cầu vừa phát sinh vừa bị đóng trong cùng kỳ", "P0",
     "Nhu cầu N4 họp ngày 05/08/2026, được gắn dự án TKT ngày 20/08/2026 (đóng trong cùng tháng).",
     "1. Chọn Kỳ = Tháng 8/2026.\n2. Mở cửa sổ chi tiết của ô \"Tổng nhu cầu phát sinh trong kỳ\".\n"
     "3. Mở cửa sổ chi tiết của ô \"Chuyển đổi thành dự án TKT\".",
     "—",
     "- N4 xuất hiện ở CẢ HAI danh sách.\n"
     "- ⚠️ Đây KHÔNG phải đếm trùng: khối trên là tập đang theo dõi, khối dưới là kết quả xử lý."),

    (6, "Ô KPI thứ nhất tính đúng", "P0",
     "Kỳ hiện tại: tổng nhu cầu 8, chuyển đổi thành dự án TKT 2.",
     "1. Đọc ô \"Tỷ lệ chuyển đổi thành công\".",
     "—",
     "- Hiện 25,0% kèm 2 / 8.\n- Tử số bằng đúng số của ô \"Chuyển đổi thành dự án TKT\"; mẫu số "
     "bằng đúng ô \"TỔNG NHU CẦU TRONG KỲ\"."),

    (7, "Ô KPI thứ hai tính đúng", "P0",
     "Kỳ hiện tại: bị đóng 3, chuyển đổi 2.",
     "1. Đọc ô \"Thành công / tổng nhu cầu đóng\".",
     "—",
     "- Hiện 66,7% kèm 2 / 3 (làm tròn 1 chữ số thập phân)."),

    (8, "Ô KPI thứ ba tính đúng", "P0",
     "Kỳ hiện tại: bị đóng 3, không tiếp tục 1.",
     "1. Đọc ô \"Thất bại / tổng nhu cầu đóng\".",
     "—",
     "- Hiện 33,3% kèm 1 / 3.\n- Ô KPI thứ hai và thứ ba cộng lại xấp xỉ 100% (sai số làm tròn)."),

    (9, "Mẫu số bằng 0 thì KPI hiện 0,0%", "P0",
     "Chọn một kỳ có nhu cầu nhưng chưa nhu cầu nào bị đóng.",
     "1. Chọn kỳ đó.\n2. Đọc 3 ô KPI.",
     "—",
     "- Ô \"Tỷ lệ chuyển đổi thành công\" hiện 0,0% kèm 0 / (tổng kỳ).\n"
     "- 2 ô còn lại hiện 0,0% kèm 0 / 0.\n"
     "- ⚠️ Không hiện dấu gạch, không để trống, không báo lỗi chia cho 0."),

    (10, "Số tiền của các ô khớp với danh sách chi tiết", "P0",
     "Kỳ hiện tại có tổng giá trị đầu tư dự kiến là 7.100.000.000 đ.",
     "1. Đọc giá trị bên cạnh ô \"TỔNG NHU CẦU TRONG KỲ\" (dạng rút gọn theo tỷ).\n"
     "2. Bấm con số để mở cửa sổ chi tiết, đọc dòng tóm tắt trên đầu cửa sổ.",
     "—",
     "- Màn chính hiện 7,1 tỷ; cửa sổ chi tiết hiện 7.100.000.000 đ.\n"
     "- ⚠️ Hai nơi khác đơn vị là ĐÚNG THIẾT KẾ, phải quy đổi trước khi so."),

    (11, "Dòng Tổng hợp kỳ khớp với ô tổng", "P1",
     "Kỳ hiện tại có 8 nhu cầu, tổng 7.100.000.000 đ.",
     "1. Đọc dòng \"Tổng hợp kỳ 01/08/2026 – 31/08/2026 · 8 nhu cầu · Tổng giá trị đầu tư dự kiến "
     "7,1 tỷ\".",
     "—",
     "- Số nhu cầu và số tiền trên dòng này bằng đúng ô \"TỔNG NHU CẦU TRONG KỲ\"."),

    (12, "Bấm được vào mọi con số của khối tổng hợp", "P0",
     "Kỳ hiện tại có dữ liệu.",
     "1. Lần lượt bấm vào con số của 6 ô: tổng trong kỳ, còn hiệu lực, phát sinh, tổng bị đóng, "
     "chuyển đổi, hết hạn.",
     "—",
     "- Mỗi lần mở đúng một cửa sổ chi tiết, tiêu đề ghi đúng tên chỉ tiêu vừa bấm.\n"
     "- Số dòng trong cửa sổ bằng đúng con số vừa bấm."),

    (13, "Bấm vào ô có số 0", "P1",
     "Chọn kỳ mà ô \"Hết hạn, không tiếp tục\" đang là 0.",
     "1. Bấm vào con số 0 của ô đó.",
     "—",
     "- Cửa sổ chi tiết vẫn mở, bảng hiện dòng \"Không có nhu cầu nào khớp bộ lọc.\"\n"
     "- ⚠️ Không được chặn bấm, không báo lỗi."),

    (14, "Đổi kỳ thì mọi ô tổng hợp và KPI đổi theo", "P0",
     "Tháng này có 8 nhu cầu; Quý này có 15 nhu cầu.",
     "1. Đọc 2 khối và 3 ô KPI ở kỳ Tháng này.\n2. Đổi Kỳ báo cáo sang Quý này, bấm \"Tìm kiếm\".\n"
     "3. Đọc lại.",
     "—",
     "- Mọi con số đổi theo kỳ mới; tỷ lệ KPI tính lại trên mẫu số mới."),

    (15, "Giá trị rút gọn theo tỷ hiển thị đúng", "P1",
     "Có kỳ tổng 7.100.000.000 đ và kỳ khác tổng 950.000.000 đ.",
     "1. Đọc giá trị bên cạnh ô tổng ở cả 2 kỳ.",
     "—",
     "- Kỳ thứ nhất hiện 7,1 tỷ.\n- Kỳ thứ hai hiện dạng nhỏ hơn 1 tỷ đúng quy ước, không hiện 0 tỷ.\n"
     "- Dấu thập phân là dấu phẩy theo chuẩn tiếng Việt."),

    (16, "Lọc theo cơ cấu thì khối tổng hợp cũng bị lọc", "P0",
     "Kỳ hiện tại 8 nhu cầu; riêng Thành phố Hà Nội 6 nhu cầu.",
     "1. Chọn Tiêu chí = Thị trường, Tỉnh/Thành phố = Thành phố Hà Nội, bấm \"Tìm kiếm\".\n"
     "2. Đọc ô \"TỔNG NHU CẦU TRONG KỲ\" và 3 ô KPI.",
     "Tỉnh / Thành phố: Thành phố Hà Nội",
     "- Ô tổng hiện 6 nhu cầu (không phải 8).\n"
     "- Mẫu số của ô KPI thứ nhất cũng là 6.\n"
     "- ⚠️ Khối tổng hợp mà không đổi theo bộ lọc là lỗi."),

    (17, "Icon chữ i của ô KPI nói đúng công thức", "P2",
     "Kỳ hiện tại có dữ liệu.",
     "1. Bấm icon chữ i cạnh tiêu đề \"KẾT QUẢ KPI\".",
     "—",
     "- Khung giải thích nói rõ từng ô lấy tử số và mẫu số từ đâu, bằng lời chứ không phải ký hiệu."),

    (18, "Thanh tiến độ của ô KPI vẽ đúng tỷ lệ", "P2",
     "Ba ô KPI lần lượt 25,0% · 66,7% · 33,3%.",
     "1. Nhìn độ dài 3 thanh tiến độ.",
     "—",
     "- Thanh dài nhất là ô 66,7%, ngắn nhất là ô 25,0%.\n"
     "- Không có thanh nào tràn ra ngoài khung."),
]

S4 = [
    (1, "Dòng tiêu đề phần mang số tổng", "P0",
     "Kỳ hiện tại có 8 nhu cầu, tổng 7.100.000.000 đ.",
     "1. Đọc dòng \"I. THEO LĨNH VỰC CÔNG TY KINH DOANH / NHÓM NGÀNH\".",
     "—",
     "- Dòng này có luôn Số nhu cầu 8, Giá trị dự kiến 7,1 tỷ, tỷ trọng 100,0%.\n"
     "- Không có dòng \"Tổng cộng\" riêng ở cuối phần."),

    (2, "Ba phần có cùng số tổng", "P0",
     "Kỳ hiện tại có dữ liệu đủ 3 cơ cấu.",
     "1. Đọc Số nhu cầu ở 3 dòng tiêu đề phần I, II, III.\n2. So với ô \"TỔNG NHU CẦU TRONG KỲ\".",
     "—",
     "- Cả 4 con số bằng nhau.\n"
     "- ⚠️ Lệch nhau nghĩa là có nhu cầu bị rơi ở một cơ cấu — lỗi nghiêm trọng, báo ngay."),

    (3, "Nút Hiện chi tiết bung toàn bộ cấp con", "P0",
     "Kỳ hiện tại có ít nhất 2 dòng cha mỗi phần, mỗi cha có cấp con.",
     "1. Bấm nút \"Hiện chi tiết\" trong ô tiêu đề cột \"Nội dung theo dõi\".\n2. Bấm lại nút đó.",
     "—",
     "- Lần 1: toàn bộ cấp con của CẢ 3 phần bung ra cùng lúc, chữ trên nút đổi thành \"Ẩn chi tiết\".\n"
     "- Lần 2: thu hết lại.\n"
     "- ⚠️ Nút không bị dòng tiêu đề che khi cuộn bảng."),

    (4, "Bung / thu từng dòng cha", "P1",
     "Phần I có dòng cha \"Công nghiệp\" với 3 nhóm ngành con.",
     "1. Bấm mũi tên ở đầu dòng \"Công nghiệp\".\n2. Bấm lại.",
     "—",
     "- Chỉ dòng cha đó bung ra 3 dòng con; các dòng cha khác giữ nguyên trạng thái.\n"
     "- Mũi tên xoay theo trạng thái bung / thu."),

    (5, "Dòng cha bằng tổng các dòng con", "P0",
     "Dòng cha \"Công nghiệp\" có 3 nhóm ngành con lần lượt 3, 4, 1 nhu cầu.",
     "1. Bung dòng cha.\n2. Cộng tay Số nhu cầu của 3 dòng con.",
     "—",
     "- Tổng 3 dòng con = 8 = Số nhu cầu của dòng cha.\n"
     "- Cột Giá trị dự kiến cũng cộng đúng."),

    (6, "Tỷ lệ thành công của từng dòng", "P0",
     "Dòng \"Giáo dục đào tạo\": 3 nhu cầu, 2 chuyển đổi thành công.",
     "1. Đọc cột \"Tỷ lệ thành công\" của dòng đó.",
     "—",
     "- Hiện 66,7% (2 chia 3, làm tròn 1 chữ số thập phân)."),

    (7, "Tỷ trọng giá trị dòng cha so với tổng kỳ", "P0",
     "Tổng kỳ 7.100.000.000 đ; dòng cha \"Thành phố Hà Nội\" 6.100.000.000 đ.",
     "1. Đọc cột \"Tỷ trọng giá trị\" của dòng \"Thành phố Hà Nội\".",
     "—",
     "- Hiện khoảng 85,9%.\n- Cộng tỷ trọng của TẤT CẢ dòng cha trong một phần được 100,0%."),

    (8, "Tỷ trọng giá trị dòng con so trong nội bộ cha", "P0",
     "Dòng cha \"Thành phố Hà Nội\" 6.100.000.000 đ, có 2 phường: 3.800.000.000 đ và 2.300.000.000 đ.",
     "1. Bung dòng cha.\n2. Đọc cột \"Tỷ trọng giá trị\" của 2 dòng con và cộng lại.",
     "—",
     "- Hai dòng con khoảng 62,3% và 37,7%, cộng lại 100,0%.\n"
     "- ⚠️ KHÔNG phải tỷ trọng so với toàn kỳ — đừng cộng dọc cả cột của cả bảng rồi báo sai."),

    (9, "Dòng con sắp theo giá trị giảm dần", "P1",
     "Dòng cha có 3 dòng con với giá trị khác nhau rõ rệt.",
     "1. Bung dòng cha, đọc cột \"Giá trị dự kiến\" từ trên xuống.",
     "—",
     "- Dòng con nhiều tiền nhất đứng trên cùng, giảm dần xuống dưới."),

    (10, "Dòng cha sắp theo giá trị giảm dần", "P1",
     "Một phần có ít nhất 3 dòng cha.",
     "1. Đọc cột \"Giá trị dự kiến\" của các dòng cha trong một phần.",
     "—",
     "- Sắp giảm dần từ trên xuống."),

    (11, "Nhóm Chưa xác định khi thiếu thông tin", "P0",
     "Có 3 nhu cầu thuộc meeting chưa gán phòng ban.",
     "1. Đọc phần III \"THEO PHÒNG BAN / NHÂN VIÊN\".",
     "—",
     "- Có dòng \"Chưa xác định phòng ban\" với 3 nhu cầu.\n"
     "- ⚠️ 3 nhu cầu này VẪN được tính vào tổng của phần, không bị loại."),

    (12, "Không có 2 dòng trùng nhãn Chưa xác định", "P1",
     "Có nhu cầu mà phòng ban đã bị xoá khỏi danh mục và nhu cầu khác chưa gán phòng ban.",
     "1. Đọc phần III.",
     "—",
     "- ⚠️ Chỉ có ĐÚNG MỘT dòng \"Chưa xác định phòng ban\", gộp cả 2 loại trên.\n"
     "- Không xuất hiện 2 dòng cùng nhãn nằm cạnh nhau."),

    (13, "Bấm con số trong bảng mở cửa sổ chi tiết", "P0",
     "Dòng \"Công nghiệp\" có 8 nhu cầu.",
     "1. Bấm vào con số 8 ở cột \"Số nhu cầu\" của dòng đó.",
     "—",
     "- Cửa sổ chi tiết mở với đúng 8 dòng.\n"
     "- Tiêu đề cửa sổ ghi đúng tên dòng vừa bấm."),

    (14, "Bấm số ở cột Chuyển đổi thành công", "P0",
     "Dòng \"Công nghiệp\": 8 nhu cầu, 2 chuyển đổi thành công.",
     "1. Bấm vào số 2 ở cột \"Chuyển đổi thành công\".",
     "—",
     "- Cửa sổ chi tiết chỉ có 2 dòng, cả 2 đều ở trạng thái \"Đã lập dự án TKT\"."),

    (15, "Bấm số ở cột Không tiếp tục", "P0",
     "Dòng có 1 nhu cầu không tiếp tục.",
     "1. Bấm vào số 1 ở cột \"Không tiếp tục\".",
     "—",
     "- Cửa sổ chi tiết chỉ có 1 dòng ở trạng thái \"Không tiếp tục\".\n"
     "- ⚠️ Cửa sổ này KHÔNG có khối kết quả KPI."),

    (16, "Bấm số ở dòng CON", "P0",
     "Dòng con \"Phường Đống Đa\" có 4 nhu cầu.",
     "1. Bung dòng cha \"Thành phố Hà Nội\".\n2. Bấm vào số 4 của dòng con.",
     "—",
     "- Cửa sổ chi tiết có đúng 4 dòng, tất cả thuộc Phường Đống Đa."),

    (17, "Ba tông màu phân biệt 3 phần", "P2",
     "Bảng đang hiện đủ 3 phần.",
     "1. Nhìn màu chữ / nền của 3 dòng tiêu đề phần.",
     "—",
     "- Phần I tông xanh lá, phần II tông tím, phần III tông cam — 3 tông rõ rệt, không trùng nhau."),

    (18, "Chữ trong ô bảng để thường", "P2",
     "Bảng đang có dữ liệu.",
     "1. Nhìn các ô dữ liệu (không phải dòng tiêu đề phần).",
     "—",
     "- Chữ để thường, không in đậm.\n- Chỉ dòng tiêu đề phần mới in đậm."),

    (19, "Thanh tỷ trọng vẽ đúng", "P2",
     "Một phần có dòng cha tỷ trọng 85,9% và 14,1%.",
     "1. Nhìn 2 thanh ở cột \"Tỷ trọng giá trị\".",
     "—",
     "- Thanh của dòng 85,9% dài hơn hẳn; con số phần trăm nằm ngay cạnh thanh."),

    (20, "Bảng tràn ngang có thanh cuộn riêng", "P1",
     "Thu nhỏ cửa sổ trình duyệt cho bảng rộng hơn khung.",
     "1. Cuộn ngang bảng.",
     "—",
     "- Bảng cuộn ngang trong khung riêng, cả trang không trượt ngang.\n"
     "- Dòng tiêu đề bảng vẫn dính khi cuộn dọc."),
]

S5 = [
    (1, "Tiêu đề cửa sổ chi tiết", "P0",
     "Bấm mở cửa sổ chi tiết từ dòng \"Thành phố Hà Nội\".",
     "1. Đọc phần đầu cửa sổ.",
     "—",
     "- Dòng dẫn mờ \"Bạn đang xem kết quả CSKH tiềm năng:\" và ngay sau là TÊN đối tượng in đậm "
     "trắng \"Thành phố Hà Nội\".\n"
     "- Dòng dưới ghi số nhu cầu · tổng tiền · kỳ đang xem."),

    (2, "Bố cục cửa sổ chi tiết", "P0",
     "Cửa sổ chi tiết đang mở từ ô \"TỔNG NHU CẦU TRONG KỲ\".",
     "1. Đọc từ trên xuống.",
     "—",
     "- Thứ tự: tiêu đề → hàng lọc → khối kết quả KPI → khối \"Phân bổ nhu cầu theo cơ cấu\" → bảng "
     "chi tiết → hàng nút dưới cùng."),

    (3, "Cửa sổ chi tiết không tràn khỏi màn hình", "P0",
     "Mở cửa sổ chi tiết của một nhóm có nhiều dòng (từ 20 dòng trở lên).",
     "1. Quan sát mép trên và mép dưới cửa sổ.\n2. Cuộn trong cửa sổ.",
     "—",
     "- Cửa sổ nằm gọn trong màn hình, mép dưới không bị cắt.\n"
     "- Chỉ phần thân cuộn; tiêu đề và hàng nút dưới cùng đứng yên.\n"
     "- ⚠️ Không có cảnh cuộn lồng trong cuộn."),

    (4, "Nút phóng to toàn màn hình", "P1",
     "Cửa sổ chi tiết đang mở.",
     "1. Bấm nút mũi tên chéo ở góc phải tiêu đề.\n2. Bấm lại nút đó.",
     "—",
     "- Lần 1: cửa sổ phủ kín màn hình, không hở 4 mép.\n- Lần 2: quay về kích thước thường."),

    (5, "Nút thu gọn khối tổng hợp trong cửa sổ", "P1",
     "Cửa sổ chi tiết đang mở, có cả khối KPI và khối phân bổ.",
     "1. Bấm nút \"Thu gọn\".\n2. Bấm lại.",
     "—",
     "- Lần 1: khối KPI và khối phân bổ bị ẩn, bảng chi tiết trồi lên, chữ đổi thành \"Mở rộng\".\n"
     "- Lần 2: hiện lại như cũ."),

    (6, "Hàng lọc trong cửa sổ đủ ô và đúng thứ tự", "P0",
     "Mở cửa sổ chi tiết từ ô \"TỔNG NHU CẦU TRONG KỲ\" (nhóm tổng, không theo cơ cấu nào).",
     "1. Đọc hàng lọc từ trái sang phải.",
     "—",
     "- Ô tìm kiếm \"Tìm khách hàng / meeting...\" đứng đầu.\n"
     "- Sau đó 3 cặp cha ▸ con liền nhau: Lĩnh vực ▸ Nhóm ngành; Tỉnh/Thành phố ▸ Phường/xã; "
     "Phòng ban ▸ Nhân viên chủ trì.\n- Ô \"Trạng thái nhu cầu\" đứng cuối cùng."),

    (7, "Nút Xoá lọc nằm cùng hàng với các ô lọc", "P1",
     "Cửa sổ chi tiết đang mở.",
     "1. Nhìn vị trí nút Xoá lọc (biểu tượng mũi tên xoay).",
     "—",
     "- ⚠️ Nút nằm NGAY SAU ô lọc cuối cùng trên cùng hàng, KHÔNG chiếm riêng một dòng.\n"
     "- Nút \"Thu gọn\" và số đếm \"n / N nhu cầu\" nằm ở mép phải cùng hàng đó."),

    (8, "Ẩn ô lọc của chính cơ cấu đang xem", "P0",
     "Mở cửa sổ chi tiết từ dòng \"Thành phố Hà Nội\" (đang xem theo thị trường).",
     "1. Đọc hàng lọc.",
     "—",
     "- KHÔNG có ô \"Tỉnh / Thành phố\" và \"Phường / xã\".\n"
     "- ⚠️ Vẫn còn đủ các ô của 2 cơ cấu kia."),

    (9, "Khối Phân bổ bỏ đúng cơ cấu đang xem", "P0",
     "Mở cửa sổ chi tiết từ dòng \"Thành phố Hà Nội\".",
     "1. Đọc khối \"Phân bổ nhu cầu theo cơ cấu\".",
     "—",
     "- Chỉ còn 2 hàng: \"Lĩnh vực KD\" và \"Phòng ban\".\n- KHÔNG có hàng \"Thị trường\"."),

    (10, "Khối Phân bổ đủ 3 cơ cấu khi mở từ nhóm tổng", "P0",
     "Mở cửa sổ chi tiết từ ô \"TỔNG NHU CẦU TRONG KỲ\".",
     "1. Đọc khối \"Phân bổ nhu cầu theo cơ cấu\".",
     "—",
     "- Đủ 3 hàng: Lĩnh vực KD, Thị trường, Phòng ban.\n"
     "- Mỗi hàng liệt kê các mục kèm số nhu cầu, phần trăm và tiền."),

    (11, "Khối Phân bổ chỉ có MỘT thanh cuộn chung", "P1",
     "Mở cửa sổ chi tiết có nhiều mục trong mỗi cơ cấu.",
     "1. Cuộn ngang khối \"Phân bổ nhu cầu theo cơ cấu\".",
     "—",
     "- ⚠️ Cả 3 hàng cuộn cùng nhau bằng MỘT thanh cuộn, các mục thẳng cột.\n"
     "- Nhãn cơ cấu bên trái đứng yên khi cuộn."),

    (12, "Bấm chip lọc nhanh", "P0",
     "Cửa sổ chi tiết mở từ nhóm tổng, khối phân bổ có mục \"Thành phố Hà Nội: 6\".",
     "1. Bấm vào chip \"Thành phố Hà Nội\".\n2. Đọc số đếm và bảng.\n3. Bấm lại chip đó.",
     "—",
     "- Sau bước 1: bảng chỉ còn nhu cầu của Hà Nội, số đếm đổi thành \"6 / 8 nhu cầu\", chip được "
     "tô sáng.\n- Sau bước 3: bỏ lọc, quay về đủ 8 dòng, chip hết tô sáng."),

    (13, "Ô tìm kiếm trong cửa sổ", "P0",
     "Cửa sổ chi tiết có nhu cầu của khách \"NGUYỄN TUẤN ANH\" và khách khác.",
     "1. Gõ \"NGUYỄN\" vào ô \"Tìm khách hàng / meeting...\".",
     "NGUYỄN",
     "- Bảng lọc còn dòng của khách có tên chứa \"NGUYỄN\".\n"
     "- ⚠️ Con trỏ KHÔNG bị mất khi đang gõ.\n"
     "- Tìm được theo cả tên khách, mã khách và tên meeting."),

    (14, "Cascade trong cửa sổ chi tiết", "P0",
     "Cửa sổ chi tiết mở từ nhóm tổng, có 2 tỉnh và 3 phường.",
     "1. Mở ô \"Chọn phường / xã\", đếm mục.\n2. Chọn \"Chọn tỉnh / thành phố\" = Thành phố Hà Nội.\n"
     "3. Mở lại ô phường / xã.",
     "—",
     "- Sau bước 3 chỉ còn phường thuộc Hà Nội.\n"
     "- Đổi tỉnh thì giá trị phường đang chọn bị xoá."),

    (15, "Lọc theo Trạng thái nhu cầu", "P0",
     "Cửa sổ chi tiết có đủ 3 trạng thái.",
     "1. Chọn \"Chọn trạng thái nhu cầu\" = Đã lập dự án TKT.",
     "Trạng thái nhu cầu: Đã lập dự án TKT",
     "- Bảng chỉ còn dòng có trạng thái đó.\n- Số đếm \"n / N nhu cầu\" cập nhật đúng."),

    (16, "Nút Xoá lọc trong cửa sổ", "P0",
     "Đang lọc trong cửa sổ bằng ô tìm kiếm và 2 ô lọc.",
     "1. Bấm nút Xoá lọc.",
     "—",
     "- Mọi ô lọc và ô tìm kiếm trắng trở lại, bảng quay về đủ dòng ban đầu.\n"
     "- Chip đang tô sáng cũng hết tô sáng."),

    (17, "Thứ tự cột bám theo khối phân bổ", "P0",
     "Mở cửa sổ chi tiết từ dòng \"Thành phố Hà Nội\".",
     "1. Đọc dòng tiêu đề bảng chi tiết.",
     "—",
     "- Sau cột STT là các cột của cơ cấu theo ĐÚNG thứ tự hàng trong khối phân bổ (Lĩnh vực KD, "
     "Nhóm ngành, rồi Phòng, Kinh doanh chủ trì).\n"
     "- Cột \"Khách hàng\" đứng SAU nhóm cột cơ cấu."),

    (18, "Nội dung một dòng trong bảng chi tiết", "P0",
     "Có nhu cầu: khách 29TPHPDO-1 NGUYỄN TUẤN ANH, giá trị 1.000.000.000 đ, dự kiến triển khai "
     "01/02/2027, trạng thái Đang theo dõi.",
     "1. Tìm dòng đó trong cửa sổ chi tiết và đọc từng cột.",
     "—",
     "- Cột Khách hàng hiện cả mã và tên.\n- Cột giá trị hiện số đầy đủ 1.000.000.000.\n"
     "- ⚠️ Cột \"Thời gian triển khai\" chỉ hiện 02/2027 (tháng/năm), KHÔNG có ngày.\n"
     "- Cột Trạng thái là nhãn màu ghi \"Đang theo dõi\"."),

    (19, "Màu nhãn trạng thái đúng bộ 3", "P1",
     "Cửa sổ chi tiết có đủ 3 trạng thái.",
     "1. Nhìn màu 3 nhãn trạng thái.",
     "—",
     "- \"Đang theo dõi\" màu xanh dương nhạt, \"Đã lập dự án TKT\" màu xanh lá, \"Không tiếp tục\" "
     "màu xám.\n- 3 màu khác nhau rõ ràng."),

    (20, "Cột Dự án TKT của nhu cầu đã chuyển đổi", "P0",
     "Nhu cầu đã gắn dự án TKT mã DA-001.",
     "1. Tìm dòng đó, đọc cột cuối.",
     "—",
     "- Hiện mã và tên dự án đã gắn.\n- Nhu cầu chưa gắn dự án thì ô này để trống."),

    (21, "Cột DV sửa chữa", "P1",
     "Có meeting mà biên bản ghi khách CÓ nhu cầu bảo trì / sửa chữa và meeting khác thì không.",
     "1. Đọc cột \"DV sửa chữa\" của 2 dòng tương ứng.",
     "—",
     "- Một dòng hiện \"Có\", dòng kia hiện \"Không\".\n"
     "- ⚠️ Thông tin này ở cấp MEETING nên mọi nhu cầu cùng một meeting có cùng giá trị."),

    (22, "Nút + Tạo mới điều hướng sang màn tạo dự án", "P0",
     "Tài khoản có quyền \"" + P_PRJ + "\"; có nhu cầu \"Đang theo dõi\" của khách NGUYỄN TUẤN ANH.",
     "1. Mở cửa sổ chi tiết.\n2. Bấm nút \"+ Tạo mới\" ở dòng nhu cầu đó.",
     "—",
     "- Mở TAB MỚI vào màn tạo dự án tiền khả thi, khách hàng đã được chọn sẵn.\n"
     "- ⚠️ Tab báo cáo cũ vẫn giữ nguyên bộ lọc đang xem, không bị mất."),

    (23, "Đóng cửa sổ chi tiết", "P0",
     "Cửa sổ chi tiết đang mở.",
     "1. Bấm nút tròn dấu X ở góc phải tiêu đề.\n2. Mở lại cửa sổ khác, bấm nút \"Đóng\" ở hàng nút "
     "dưới cùng.",
     "—",
     "- Cả 2 cách đều đóng cửa sổ, trở về màn báo cáo với bộ lọc và bảng nguyên vẹn."),

    (24, "Mở cửa sổ mới thì bộ lọc riêng được đặt lại", "P1",
     "Mở cửa sổ chi tiết, lọc theo trạng thái, rồi đóng lại.",
     "1. Bấm mở cửa sổ chi tiết của một ô số khác.\n2. Đọc hàng lọc.",
     "—",
     "- Mọi ô lọc riêng của cửa sổ đều trắng, không giữ lựa chọn của lần mở trước."),

    (25, "Cửa sổ chi tiết của nhóm Hết hạn không có khối KPI", "P0",
     "Kỳ hiện tại có ít nhất 1 nhu cầu \"Không tiếp tục\".",
     "1. Bấm con số của ô \"Hết hạn, không tiếp tục\".",
     "—",
     "- ⚠️ Cửa sổ KHÔNG có khối kết quả KPI (vì luôn là 0% / 0% / 100%).\n"
     "- Vẫn có khối \"Phân bổ nhu cầu theo cơ cấu\" và bảng chi tiết."),

    (26, "Số đếm trong cửa sổ khớp bảng", "P0",
     "Cửa sổ chi tiết mở với 8 nhu cầu, sau đó lọc còn 6.",
     "1. Đọc số đếm ở mép phải hàng lọc trước và sau khi lọc.\n2. Đếm số dòng thật trong bảng.",
     "—",
     "- Trước khi lọc: \"8 / 8 nhu cầu\", bảng 8 dòng.\n"
     "- Sau khi lọc: \"6 / 8 nhu cầu\", bảng 6 dòng.\n- Dòng tóm tắt trên tiêu đề ghi thêm \"đang lọc "
     "trong 6 nhu cầu\"."),
]

S6 = [
    (1, "Nhu cầu mới thu thập vào trạng thái Đang theo dõi", "P0",
     "Meeting M loại \"Họp tìm hiểu & Giới thiệu sản phẩm\" họp ngày trong kỳ, biên bản ghi khách CÓ "
     "nhu cầu đầu tư, chọn 2 nhóm ngành.",
     "1. Vào màn Meeting, mở biên bản của M, chọn 2 nhóm ngành kèm giá trị và thời gian dự kiến.\n"
     "2. Bấm Hoàn thành meeting.\n3. Mở báo cáo với kỳ chứa ngày họp.",
     "—",
     "- Ô \"Tổng nhu cầu phát sinh trong kỳ\" tăng thêm 2.\n"
     "- Cả 2 nhu cầu ở trạng thái \"Đang theo dõi\" trong cửa sổ chi tiết."),

    (2, "Meeting chưa Hoàn thành thì chưa vào báo cáo", "P0",
     "Meeting M2 cùng loại, đã có biên bản với 2 nhu cầu, nhưng trạng thái vẫn là \"Chốt lịch\".",
     "1. Mở báo cáo với kỳ chứa ngày họp của M2.\n2. Mở cửa sổ chi tiết của ô tổng.",
     "—",
     "- ⚠️ KHÔNG có nhu cầu nào của M2 trong báo cáo.\n"
     "- Sau khi chuyển M2 sang Hoàn thành và tải lại thì 2 nhu cầu mới xuất hiện."),

    (3, "Meeting khác loại thì không vào báo cáo", "P0",
     "Meeting M3 loại khác (không phải \"Họp tìm hiểu & Giới thiệu sản phẩm\"), đã Hoàn thành.",
     "1. Mở báo cáo với kỳ chứa ngày họp của M3.",
     "—",
     "- Không có nhu cầu nào của M3."),

    (4, "Biên bản trả lời KHÔNG có nhu cầu đầu tư", "P0",
     "Meeting M4 đúng loại, đã Hoàn thành, biên bản ghi khách KHÔNG có nhu cầu đầu tư.",
     "1. Mở báo cáo với kỳ chứa ngày họp của M4.",
     "—",
     "- Không có nhu cầu nào của M4 trong báo cáo."),

    (5, "Gắn nhu cầu vào dự án TKT thì chuyển trạng thái", "P0",
     "Nhu cầu N của khách K đang \"Đang theo dõi\".",
     "1. Vào màn Quản lý dự án TKT, bấm Thêm mới.\n2. Chọn khách hàng K.\n"
     "3. Ở ô \"Nhu cầu khách hàng\" chọn nhu cầu N.\n4. Lưu dự án.\n5. Mở lại báo cáo.",
     "—",
     "- Nhu cầu N chuyển sang \"Đã lập dự án TKT\".\n"
     "- Ô \"Chuyển đổi thành dự án TKT\" tăng thêm 1.\n"
     "- Cột \"Dự án TKT\" của dòng N hiện mã và tên dự án vừa tạo."),

    (6, "Ô Nhu cầu khách hàng chỉ liệt kê nhu cầu hợp lệ", "P0",
     "Khách K có: nhu cầu N1 \"Đang theo dõi\" (meeting đã Hoàn thành, do chính mình chủ trì), "
     "nhu cầu N2 đã gắn dự án khác, nhu cầu N3 thuộc meeting chưa Hoàn thành.",
     "1. Mở màn tạo dự án TKT, chọn khách K.\n2. Mở ô \"Nhu cầu khách hàng\".",
     "—",
     "- Chỉ có N1 trong danh sách.\n- N2 và N3 không xuất hiện."),

    (7, "Đổi nhu cầu gắn cho dự án thì trả nhu cầu cũ về theo dõi", "P0",
     "Dự án D đang gắn nhu cầu N1; khách đó còn nhu cầu N5 đang theo dõi.",
     "1. Mở màn Sửa dự án D.\n2. Đổi ô \"Nhu cầu khách hàng\" từ N1 sang N5.\n3. Lưu.\n"
     "4. Mở báo cáo, tìm N1 và N5.",
     "—",
     "- N1 quay về \"Đang theo dõi\", cột Dự án TKT trống trở lại.\n"
     "- N5 chuyển sang \"Đã lập dự án TKT\"."),

    (8, "Bỏ chọn nhu cầu ở dự án", "P0",
     "Dự án D đang gắn nhu cầu N5.",
     "1. Mở Sửa dự án D, xoá lựa chọn ở ô \"Nhu cầu khách hàng\".\n2. Lưu.\n3. Mở báo cáo.",
     "—",
     "- N5 quay về \"Đang theo dõi\".\n- Ô \"Chuyển đổi thành dự án TKT\" giảm 1."),

    (9, "Cảnh báo khi lưu dự án mà chưa chọn nhu cầu", "P1",
     "Đang tạo dự án TKT cho khách có nhu cầu đang theo dõi, nhưng để trống ô \"Nhu cầu khách hàng\".",
     "1. Điền các thông tin bắt buộc, bấm Lưu.",
     "—",
     "- Hệ thống hỏi lại bằng một cửa sổ xác nhận, nhắc chưa chọn nhu cầu khách hàng.\n"
     "- ⚠️ Bấm Hủy thì KHÔNG lưu, ở lại màn với dữ liệu đã nhập.\n"
     "- Bấm đồng ý thì vẫn lưu được (chỉ cảnh báo, không chặn)."),

    (10, "Sửa biên bản không làm mất liên kết dự án", "P0",
     "Meeting M có 3 nhu cầu, trong đó N1 đã gắn dự án TKT.",
     "1. Mở lại biên bản của M, thêm 1 nhóm ngành mới rồi lưu.\n2. Mở báo cáo, tìm N1.",
     "—",
     "- ⚠️ N1 VẪN ở trạng thái \"Đã lập dự án TKT\" và vẫn giữ mã dự án.\n"
     "- Nhu cầu mới thêm ở trạng thái \"Đang theo dõi\".\n"
     "- Đây là điểm rất dễ hỏng: lưu biên bản mà mất liên kết dự án thì báo cáo sai ngay."),

    (11, "Bỏ nhu cầu đã gắn dự án ở biên bản bị chặn", "P0",
     "Meeting M có nhu cầu N1 đã gắn dự án TKT.",
     "1. Mở biên bản của M, bỏ tích nhóm ngành ứng với N1.\n2. Bấm Lưu.",
     "—",
     "- Hệ thống chặn lại, báo lỗi nói rõ nhu cầu đang gắn dự án, muốn bỏ thì gỡ ở màn Dự án TKT "
     "trước.\n- Biên bản không bị lưu, dữ liệu trên màn còn nguyên."),

    (12, "Nhu cầu quá ngày dự kiến triển khai bị đóng tự động", "P0",
     "Nhu cầu N6 có thời gian dự kiến triển khai là 06/08/2026, chưa gắn dự án; hôm nay sau ngày đó.",
     "1. Chờ tác vụ tự động chạy (hoặc nhờ kỹ thuật chạy tay tác vụ đóng nhu cầu quá hạn).\n"
     "2. Mở báo cáo kỳ tháng 8/2026.",
     "—",
     "- N6 chuyển sang \"Không tiếp tục\".\n"
     "- ⚠️ Ngày đóng ghi đúng 06/08/2026 (bằng ngày dự kiến triển khai), KHÔNG phải ngày tác vụ chạy.\n"
     "- N6 nằm trong ô \"Hết hạn, không tiếp tục\" của kỳ tháng 8."),

    (13, "Nhu cầu không có ngày dự kiến triển khai không bị đóng", "P0",
     "Nhu cầu N7 để trống thời gian dự kiến triển khai, đã quá lâu.",
     "1. Chạy tác vụ đóng nhu cầu quá hạn.\n2. Mở báo cáo.",
     "—",
     "- ⚠️ N7 VẪN ở \"Đang theo dõi\", không bị đóng.\n"
     "- Cột \"Thời gian triển khai\" của N7 hiện dấu gạch."),

    (14, "Chạy lại tác vụ đóng nhiều lần không nhân đôi", "P1",
     "Đã có 1 nhu cầu bị đóng do quá hạn.",
     "1. Chạy tác vụ đóng nhu cầu quá hạn thêm 2 lần nữa.\n2. Mở báo cáo.",
     "—",
     "- Số ở ô \"Hết hạn, không tiếp tục\" KHÔNG tăng thêm.\n- Ngày đóng của nhu cầu không đổi."),
]

S7 = [
    (1, "Nút In báo cáo và Xuất Excel nằm trên thanh bộ lọc", "P0",
     "Đang ở màn báo cáo.",
     "1. Nhìn góc phải khối bộ lọc.",
     "—",
     "- Có nút \"In báo cáo\" (biểu tượng máy in) và nút \"Xuất Excel\" (biểu tượng tải xuống)."),

    (2, "Cửa sổ chọn kiểu in có 2 lựa chọn", "P0",
     "Đang ở màn báo cáo.",
     "1. Bấm nút \"In báo cáo\".\n2. Đọc cửa sổ mở ra.",
     "—",
     "- Tiêu đề \"In báo cáo\", dòng nhắc \"Bản in A4 ngang, bám đúng bộ lọc đang áp dụng.\"\n"
     "- Đúng 2 lựa chọn: \"In bảng theo dõi\" (được chọn sẵn) và \"In danh sách chi tiết\".\n"
     "- Hàng nút dưới cùng có \"Hủy\" và \"In\"."),

    (3, "Bấm Hủy ở cửa sổ chọn kiểu in", "P1",
     "Cửa sổ chọn kiểu in đang mở.",
     "1. Bấm \"Hủy\".",
     "—",
     "- Cửa sổ đóng, không mở bản xem trước, màn báo cáo giữ nguyên."),

    (4, "In bảng theo dõi ra bản xem trước", "P0",
     "Kỳ hiện tại có dữ liệu, Tiêu chí = Tất cả.",
     "1. Bấm \"In báo cáo\", giữ lựa chọn \"In bảng theo dõi\", bấm \"In\".\n2. Đọc bản xem trước.",
     "—",
     "- Mở cửa sổ xem trước khổ ngang, đầu trang có ảnh tiêu đề thư của công ty.\n"
     "- Tiêu đề \"BÁO CÁO KẾT QUẢ CHĂM SÓC KHÁCH HÀNG TIỀM NĂNG\", dưới là dòng kỳ và tiêu chí.\n"
     "- Có bảng chỉ tiêu kèm cột kết quả KPI, rồi bảng theo dõi đủ 3 phần.\n"
     "- Cuối trang có dòng \"Ngày in\"."),

    (5, "Bản in bám đúng bộ lọc đang áp dụng", "P0",
     "Đang lọc Tiêu chí = Thị trường, Tỉnh/Thành phố = Thành phố Hà Nội, còn 6 nhu cầu.",
     "1. Bấm \"In báo cáo\" ▸ \"In bảng theo dõi\" ▸ \"In\".\n2. Đọc bản xem trước.",
     "Tỉnh / Thành phố: Thành phố Hà Nội",
     "- Bản in chỉ có phần \"THEO THỊ TRƯỜNG\".\n- Tổng trên bản in là 6 nhu cầu.\n"
     "- Dòng dưới tiêu đề ghi rõ kỳ và các bộ lọc đang áp dụng."),

    (6, "In danh sách chi tiết từ màn báo cáo", "P0",
     "Kỳ hiện tại có 8 nhu cầu.",
     "1. Bấm \"In báo cáo\", chọn \"In danh sách chi tiết\", bấm \"In\".\n2. Đọc bản xem trước.",
     "—",
     "- Tiêu đề \"DANH SÁCH NHU CẦU KHÁCH HÀNG TIỀM NĂNG\".\n"
     "- Bảng có 8 dòng, mỗi nhu cầu một dòng, đủ các cột Lĩnh vực KD, Nhóm ngành, Tỉnh/TP, "
     "Phường/xã, Phòng ban, Kinh doanh chủ trì, Khách hàng, Giá trị dự kiến, Triển khai, Meeting, "
     "Trạng thái."),

    (7, "In danh sách từ cửa sổ chi tiết mang đủ thông tin", "P0",
     "Mở cửa sổ chi tiết từ dòng \"Thành phố Hà Nội\", lọc thêm Trạng thái = Đã lập dự án TKT còn "
     "2 nhu cầu.",
     "1. Bấm nút \"In danh sách\" ở hàng nút dưới cùng của cửa sổ.\n2. Đọc bản xem trước.",
     "Trạng thái nhu cầu: Đã lập dự án TKT",
     "- Dòng đầu ghi tên đối tượng đang xem (\"Thành phố Hà Nội\").\n"
     "- Có dòng kỳ + tiêu chí, VÀ dòng \"Lọc trong danh sách: Trạng thái: Đã lập dự án TKT\".\n"
     "- Có dòng tổng \"2 nhu cầu · <tiền> đ\".\n"
     "- ⚠️ Có khối kết quả KPI VÀ khối \"Phân bổ nhu cầu theo cơ cấu\" giống hệt trên cửa sổ.\n"
     "- Bảng đúng 2 dòng."),

    (8, "Bản in từ cửa sổ khớp số liệu với cửa sổ", "P0",
     "Cửa sổ chi tiết đang hiện \"6 / 8 nhu cầu\" và 3 ô KPI.",
     "1. Ghi lại 3 con số KPI trên cửa sổ.\n2. Bấm \"In danh sách\", so 3 con số trên bản in.",
     "—",
     "- 3 con số KPI trên bản in bằng đúng trên cửa sổ.\n"
     "- Các mục trong khối phân bổ cũng trùng khớp."),

    (9, "Bấm nút In trong bản xem trước", "P1",
     "Bản xem trước đang mở.",
     "1. Bấm nút \"In\" cạnh tiêu đề bản xem trước.",
     "—",
     "- Mở hộp thoại in của trình duyệt, khổ giấy đề xuất là A4 ngang.\n"
     "- Nội dung xem trước trong hộp thoại KHÔNG dính menu bên trái và thanh trên cùng của hệ thống.\n"
     "- Ảnh tiêu đề thư của công ty có trong bản in."),

    (10, "Đóng bản xem trước không đóng nhầm cửa sổ chi tiết", "P0",
     "Mở cửa sổ chi tiết rồi bấm \"In danh sách\" (2 cửa sổ chồng nhau).",
     "1. Bấm dấu X đóng bản xem trước.",
     "—",
     "- ⚠️ Chỉ bản xem trước đóng lại; cửa sổ chi tiết vẫn mở và vẫn bấm nút được.\n"
     "- Trang nền không bị kẹt trạng thái không cuộn được."),

    (11, "Xuất Excel bảng theo dõi", "P0",
     "Kỳ hiện tại có 8 nhu cầu.",
     "1. Bấm nút \"Xuất Excel\".\n2. Mở tệp tải về.",
     "—",
     "- Tệp tải về có đuôi .xlsx, tên tệp mô tả đúng nội dung báo cáo.\n"
     "- ⚠️ Trên trình duyệt Safari cũng phải ra tệp có đuôi .xlsx, KHÔNG phải tệp tên ngẫu nhiên "
     "không đuôi.\n"
     "- Nội dung gồm 3 phần: tổng hợp kỳ, kết quả KPI, bảng theo dõi."),

    (12, "Số trong tệp Excel là số thật, cộng được", "P0",
     "Đã tải tệp Excel của bảng theo dõi.",
     "1. Mở tệp, chọn một cột số tiền.\n2. Nhìn ô tổng ở thanh trạng thái của Excel.\n"
     "3. Bấm vào một ô tiền bất kỳ.",
     "—",
     "- Excel tính được tổng cho cột đó.\n"
     "- ⚠️ KHÔNG có ô nào hiện tam giác xanh với lời nhắc số đang lưu dưới dạng chữ.\n"
     "- Ô phần trăm hiện dạng 25,0% và cũng là số thật."),

    (13, "Bề rộng cột trong tệp Excel đọc được", "P1",
     "Đã tải tệp Excel của bảng theo dõi.",
     "1. Mở tệp, nhìn cột \"Nội dung theo dõi\".",
     "—",
     "- Không có cột nào bị bóp hẹp làm chữ bị cắt.\n- Không phải chỉnh tay mới đọc được."),

    (14, "Phân cấp trong tệp Excel nhìn ra được", "P0",
     "Bảng theo dõi có dòng cha và dòng con.",
     "1. Mở tệp Excel, đọc cột STT và cột \"Nội dung theo dõi\".",
     "—",
     "- Dòng tiêu đề phần có số La Mã I, II, III; dòng cha có số 1, 2, 3.\n"
     "- ⚠️ Dòng CON để trống ô STT và tên bắt đầu bằng dấu gạch dài, nhờ đó phân biệt được cấp.\n"
     "- Không có 2 dòng con nào trùng số thứ tự."),

    (15, "Xuất Excel danh sách từ cửa sổ chi tiết", "P0",
     "Cửa sổ chi tiết đang hiện 6 nhu cầu sau khi lọc.",
     "1. Bấm nút \"Xuất Excel danh sách\".\n2. Mở tệp tải về, đếm dòng dữ liệu.",
     "—",
     "- Tệp có đúng 6 dòng dữ liệu, khớp con số trên cửa sổ.\n"
     "- Đủ 16 cột kể cả Mã KH và Ngày đóng."),

    (16, "Tệp Excel danh sách luôn đủ cột dù cửa sổ đổi thứ tự cột", "P1",
     "Mở cửa sổ chi tiết từ dòng \"Thành phố Hà Nội\" (cửa sổ đang ẩn cột thị trường).",
     "1. Bấm \"Xuất Excel danh sách\", mở tệp.",
     "—",
     "- ⚠️ Tệp VẪN có đủ cột Tỉnh/Thành phố và Phường/xã, dù trên cửa sổ chúng bị ẩn.\n"
     "- Thứ tự cột trong tệp cố định, không đổi theo cơ cấu đang xem."),

    (17, "Xuất Excel khi tập rỗng", "P1",
     "Lọc ra tập không có nhu cầu nào.",
     "1. Bấm \"Xuất Excel danh sách\", mở tệp.",
     "—",
     "- Tệp vẫn tải về được và mở được.\n- Chỉ có dòng tiêu đề và dòng \"Không có dữ liệu\"."),

    (18, "Xuất Excel không làm mất bộ lọc đang xem", "P1",
     "Đang lọc Tiêu chí = Thị trường, Tỉnh/Thành phố = Thành phố Cần Thơ.",
     "1. Bấm \"Xuất Excel\".\n2. Nhìn lại màn báo cáo.",
     "—",
     "- Màn báo cáo giữ nguyên bộ lọc và số liệu, không tải lại, không nhảy về mặc định."),

    (19, "Tệp Excel bảng theo dõi chỉ có phần đang xem", "P0",
     "Đang chọn Tiêu chí = Lĩnh vực công ty kinh doanh / Nhóm ngành.",
     "1. Bấm \"Xuất Excel\", mở tệp.",
     "—",
     "- Phần bảng theo dõi trong tệp CHỈ có phần theo lĩnh vực, không có 2 phần còn lại."),

    (20, "Tiêu đề tệp Excel ghi rõ kỳ và bộ lọc", "P1",
     "Đang lọc kỳ tuỳ chỉnh 01/08/2026 – 31/08/2026, Tiêu chí = Tất cả.",
     "1. Bấm \"Xuất Excel\", mở tệp, đọc 2 dòng đầu.",
     "—",
     "- Dòng 1 là tên báo cáo.\n"
     "- Dòng 2 ghi \"Kỳ 01/08/2026 – 31/08/2026 · Tiêu chí theo dõi: Tất cả\" kèm các bộ lọc khác "
     "nếu có."),
]

S8 = [
    (1, "Nhu cầu có giá trị đầu tư bằng 0", "P1",
     "Có nhu cầu N8 nhập giá trị đầu tư dự kiến là 0.",
     "1. Mở báo cáo kỳ chứa N8.\n2. Tìm dòng chứa N8 trong bảng và trong cửa sổ chi tiết.",
     "—",
     "- N8 VẪN được đếm vào Số nhu cầu.\n- Cột Giá trị dự kiến của N8 hiện 0.\n"
     "- Tỷ trọng giá trị của dòng chứa N8 hiện 0,0%, không báo lỗi."),

    (2, "Toàn bộ nhu cầu trong kỳ đều có giá trị 0", "P2",
     "Chọn kỳ mà mọi nhu cầu đều có giá trị đầu tư bằng 0.",
     "1. Mở báo cáo kỳ đó.",
     "—",
     "- Cột \"Tỷ trọng giá trị\" của mọi dòng hiện 0,0% (mẫu số bằng 0).\n"
     "- Không có ô nào hiện dấu vô cực hay chữ lỗi."),

    (3, "Giá trị đầu tư rất lớn", "P2",
     "Có nhu cầu giá trị 999.000.000.000 đ.",
     "1. Đọc dòng đó ở bảng theo dõi, cửa sổ chi tiết, bản in và tệp Excel.",
     "—",
     "- Bảng theo dõi hiện dạng rút gọn theo tỷ, không tràn ô.\n"
     "- Cửa sổ chi tiết, bản in, tệp Excel hiện số đầy đủ có dấu phân cách hàng nghìn."),

    (4, "Khách hàng chưa gán tỉnh / phường", "P0",
     "Có 2 nhu cầu của khách chưa gán tỉnh và phường.",
     "1. Đọc phần II \"THEO THỊ TRƯỜNG\".",
     "—",
     "- Có dòng gom nhóm \"Chưa xác định\" chứa 2 nhu cầu đó.\n"
     "- Tổng của phần II vẫn bằng tổng của phần I và phần III."),

    (5, "Nhu cầu chưa gán lĩnh vực kinh doanh", "P0",
     "Có nhu cầu chưa có lĩnh vực công ty kinh doanh.",
     "1. Đọc phần I.",
     "—",
     "- Có dòng \"Chưa xác định lĩnh vực\" chứa nhu cầu đó.\n"
     "- Trong tệp Excel danh sách, ô lĩnh vực của dòng đó ghi \"Chưa xác định lĩnh vực\", không để "
     "trống."),

    (6, "Người chủ trì meeting đã nghỉ việc", "P1",
     "Meeting M có người chủ trì đã nghỉ việc.",
     "1. Mở báo cáo, đọc phần III và cột \"Kinh doanh chủ trì\" trong cửa sổ chi tiết.",
     "—",
     "- ⚠️ Tên người chủ trì VẪN hiện đúng, không để trống, không hiện mã số.\n"
     "- Nhu cầu vẫn được tính vào tổng."),

    (7, "Tên khách hàng rất dài", "P2",
     "Có khách hàng tên dài trên 80 ký tự.",
     "1. Mở cửa sổ chi tiết, nhìn cột Khách hàng.\n2. Xuất Excel và mở tệp.",
     "—",
     "- Trên cửa sổ: chữ xuống dòng hoặc cắt gọn, không phá vỡ bố cục bảng.\n"
     "- Trong tệp Excel: chữ hiển thị đầy đủ."),

    (8, "Tên có ký tự đặc biệt", "P1",
     "Có nhóm ngành tên chứa dấu và ký tự đặc biệt, ví dụ \"Dịch vụ Tư vấn & Kỹ thuật\".",
     "1. Đọc tên đó ở bảng theo dõi, cửa sổ chi tiết, bản in và tệp Excel.",
     "—",
     "- ⚠️ Cả 4 nơi hiện đúng \"Dịch vụ Tư vấn & Kỹ thuật\".\n"
     "- Không hiện thành chuỗi ký tự lạ, bảng không bị vỡ ở chỗ có ký tự đặc biệt."),

    (9, "Nhiều nhu cầu cùng một khách hàng", "P0",
     "Khách K có 3 nhu cầu thuộc 3 nhóm ngành khác nhau trong cùng kỳ.",
     "1. Mở cửa sổ chi tiết của ô tổng, tìm khách K.",
     "—",
     "- Có ĐÚNG 3 dòng của khách K, mỗi dòng một nhóm ngành.\n"
     "- ⚠️ Đây là đúng thiết kế (mỗi nhóm ngành là một nhu cầu), không phải trùng dữ liệu."),

    (10, "Một meeting sinh nhiều nhu cầu", "P1",
     "Meeting M có 4 nhóm ngành được chọn.",
     "1. Mở cửa sổ chi tiết, lọc theo tên meeting M.",
     "—",
     "- Ra 4 dòng, cột Meeting của cả 4 dòng đều là M.\n"
     "- Cột \"DV sửa chữa\" của cả 4 dòng giống nhau."),

    (11, "Kỳ chỉ có đúng 1 ngày", "P2",
     "Có nhu cầu họp đúng ngày 12/08/2026.",
     "1. Chọn Kỳ = Tuỳ chỉnh, Từ ngày và Đến ngày cùng là 12/08/2026.\n2. Bấm \"Tìm kiếm\".",
     "Từ ngày: 12/08/2026 — Đến ngày: 12/08/2026",
     "- Vẫn ra đúng nhu cầu họp trong ngày đó, không bị coi là kỳ rỗng."),

    (12, "Nhu cầu đóng đúng ngày đầu kỳ hoặc cuối kỳ", "P0",
     "Nhu cầu N9 có ngày đóng đúng 01/08/2026; nhu cầu N10 có ngày đóng đúng 31/08/2026.",
     "1. Chọn kỳ 01/08/2026 – 31/08/2026.\n2. Mở cửa sổ chi tiết của ô \"TỔNG NHU CẦU BỊ ĐÓNG TRONG "
     "KỲ\".",
     "Từ ngày: 01/08/2026 — Đến ngày: 31/08/2026",
     "- ⚠️ Cả N9 và N10 đều CÓ trong danh sách — mốc đầu kỳ và cuối kỳ đều tính vào (khoảng đóng "
     "2 đầu)."),
]

S9 = [
    (1, "Hai người xem cùng lúc với quyền khác nhau", "P0",
     "Tài khoản A có quyền xem theo tổng công ty; tài khoản B chỉ có quyền theo phòng ban.",
     "1. Mở 2 trình duyệt, đăng nhập A và B.\n2. Cùng mở báo cáo với kỳ Tháng này.\n3. So số liệu.",
     "—",
     "- Số của A lớn hơn hoặc bằng số của B.\n"
     "- ⚠️ B không bao giờ thấy nhu cầu ngoài phòng ban mình quản lý, kể cả khi A đang mở cùng lúc."),

    (2, "Dữ liệu thay đổi trong lúc đang xem", "P1",
     "Tài khoản A đang mở báo cáo. Tài khoản B gắn một nhu cầu vào dự án TKT mới.",
     "1. B thực hiện gắn nhu cầu.\n2. A bấm \"Tìm kiếm\" trên màn đang mở.",
     "—",
     "- Số của A cập nhật theo thay đổi của B.\n- Không cần tải lại cả trang."),

    (3, "Mở cửa sổ chi tiết trong lúc dữ liệu vừa đổi", "P1",
     "Nhu cầu N vừa được gắn dự án TKT bởi người khác, màn A vẫn hiện số cũ.",
     "1. A bấm vào con số của ô \"Chuyển đổi thành dự án TKT\" (số cũ).",
     "—",
     "- Cửa sổ mở bình thường và hiện danh sách MỚI NHẤT.\n"
     "- ⚠️ Không treo trang, không báo lỗi đỏ dù con số trên nền là số cũ."),

    (4, "Đổi bộ lọc liên tục", "P1",
     "Đang ở màn báo cáo.",
     "1. Đổi Tiêu chí theo dõi 5 lần liên tiếp thật nhanh.",
     "—",
     "- Kết quả cuối cùng khớp với lựa chọn CUỐI CÙNG.\n"
     "- ⚠️ Không xảy ra cảnh bảng hiện kết quả của lần chọn trước đó."),

    (5, "Gõ tìm kiếm liên tục trong cửa sổ chi tiết", "P2",
     "Cửa sổ chi tiết đang mở với nhiều dòng.",
     "1. Gõ nhanh 10 ký tự vào ô tìm kiếm rồi xoá dần.",
     "—",
     "- Bảng lọc theo đúng chuỗi cuối cùng.\n- Con trỏ không bị nhảy ra khỏi ô."),

    (6, "Mở nhiều tab báo cáo cùng lúc", "P2",
     "Mở 2 tab cùng vào màn báo cáo với 2 bộ lọc khác nhau.",
     "1. Ở tab 1 chọn Tiêu chí = Thị trường; tab 2 chọn Tiêu chí = Phòng ban / Nhân viên.\n"
     "2. Chuyển qua lại 2 tab.",
     "—",
     "- Mỗi tab giữ đúng bộ lọc và số liệu của nó, không ảnh hưởng lẫn nhau."),
]

S10 = [
    (1, "Trọn vòng đời một nhu cầu từ họp tới lập dự án", "P0",
     "Khách K chưa có nhu cầu nào. Tài khoản có đủ quyền xem báo cáo và quyền \"" + P_PRJ + "\".",
     "1. Tạo meeting loại \"Họp tìm hiểu & Giới thiệu sản phẩm\" với khách K, chọn Người chủ trì là "
     "chính mình.\n2. Nhập biên bản: khách CÓ nhu cầu đầu tư, chọn 1 nhóm ngành, nhập giá trị và "
     "thời gian dự kiến.\n3. Bấm Hoàn thành meeting.\n4. Mở báo cáo kỳ chứa ngày họp, kiểm số.\n"
     "5. Vào Dự án TKT, tạo dự án cho khách K và chọn nhu cầu vừa tạo.\n6. Quay lại báo cáo, kiểm số.",
     "—",
     "- Sau bước 4: \"Tổng nhu cầu phát sinh trong kỳ\" tăng 1, nhu cầu ở trạng thái \"Đang theo "
     "dõi\".\n- Sau bước 6: \"Chuyển đổi thành dự án TKT\" tăng 1, trạng thái đổi thành \"Đã lập dự "
     "án TKT\", ô \"Tỷ lệ chuyển đổi thành công\" tăng theo."),

    (2, "Trọn vòng đời một nhu cầu bị hết hạn", "P0",
     "Khách K2, tạo nhu cầu có thời gian dự kiến triển khai là ngày đã qua.",
     "1. Tạo meeting + biên bản như trên, thời gian dự kiến triển khai đặt vào quá khứ.\n"
     "2. Hoàn thành meeting.\n3. Chạy tác vụ đóng nhu cầu quá hạn.\n4. Mở báo cáo kỳ chứa ngày dự "
     "kiến triển khai đó.",
     "—",
     "- Nhu cầu chuyển sang \"Không tiếp tục\", ngày đóng bằng đúng ngày dự kiến triển khai.\n"
     "- Ô \"Hết hạn, không tiếp tục\" tăng 1, ô \"Thất bại / tổng nhu cầu đóng\" tăng theo."),

    (3, "Từ báo cáo tạo thẳng dự án TKT", "P0",
     "Có nhu cầu \"Đang theo dõi\"; tài khoản có quyền \"" + P_PRJ + "\".",
     "1. Mở báo cáo, bấm số ô tổng để mở cửa sổ chi tiết.\n2. Bấm \"+ Tạo mới\" ở dòng nhu cầu đó.\n"
     "3. Ở tab mới, điền thông tin và chọn đúng nhu cầu ở ô \"Nhu cầu khách hàng\", lưu.\n"
     "4. Quay lại tab báo cáo, bấm \"Tìm kiếm\".",
     "—",
     "- Nhu cầu chuyển sang \"Đã lập dự án TKT\" và cột Dự án TKT hiện mã dự án vừa tạo.\n"
     "- Tab báo cáo vẫn giữ nguyên bộ lọc đang xem trước đó."),

    (4, "Đối chiếu số liệu 4 nơi", "P0",
     "Kỳ hiện tại có dữ liệu, đang lọc theo một phòng ban.",
     "1. Ghi số ở ô \"TỔNG NHU CẦU TRONG KỲ\".\n2. Mở cửa sổ chi tiết, đếm dòng.\n"
     "3. Xuất Excel danh sách, đếm dòng trong tệp.\n4. In danh sách chi tiết, đếm dòng trên bản in.",
     "—",
     "- ⚠️ Cả 4 nơi phải ra CÙNG MỘT con số.\n"
     "- Lệch bất kỳ nơi nào là lỗi phải báo ngay."),

    (5, "Kịch bản duyệt báo cáo cuối tháng", "P1",
     "Cuối tháng, cần gửi kết quả cho lãnh đạo.",
     "1. Chọn Kỳ = Tháng này, Tiêu chí = Tất cả.\n2. Đọc 2 khối và 3 ô KPI.\n"
     "3. Bấm \"In báo cáo\" ▸ \"In bảng theo dõi\" ▸ \"In\" và in ra giấy.\n"
     "4. Bấm \"Xuất Excel\" để lưu tệp.\n5. So bản giấy với tệp Excel và với màn hình.",
     "Kỳ báo cáo: Tháng này",
     "- 3 nơi cùng số liệu, cùng kỳ, cùng bộ lọc.\n"
     "- Bản giấy có ảnh tiêu đề thư của công ty và ngày in.\n"
     "- Tệp Excel cộng được tổng bằng công cụ của Excel."),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "KHỐI TỔNG HỢP KỲ & KẾT QUẢ KPI", S3),
    ("IV", "BẢNG THEO DÕI", S4),
    ("V", "CỬA SỔ DANH SÁCH NHU CẦU CHI TIẾT", S5),
    ("VI", "VÒNG ĐỜI NHU CẦU & LIÊN KẾT DỰ ÁN TKT", S6),
    ("VII", "XUẤT EXCEL / IN", S7),
    ("VIII", "RÀNG BUỘC DỮ LIỆU & TRƯỜNG HỢP BIÊN", S8),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S9),
    ("X", "LUỒNG NGHIỆP VỤ TỪ ĐẦU ĐẾN CUỐI", S10),
]

if __name__ == "__main__":
    build(
        output_file=os.path.join(HERE, "testcase.xlsx"),
        sheet_name="Trang tính1",
        feature_name="Báo cáo kết quả chăm sóc khách hàng tiềm năng - Cập nhật ngày 26/08/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
