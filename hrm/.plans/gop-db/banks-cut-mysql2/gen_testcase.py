# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man 'Danh muc ngan hang' (/human/banks) theo form mau 17 cot.

Ban nay THAY THE `generate-testcase.py` (form cu 15 cot, sinh 2026-08-07) — dung engine chung
`.claude/skills/testcase-documenter/assets/tc_engine.py`.

Nguon doi chieu (doc truc tiep tu code tren nhanh gop_db):
  BE  Modules/Human/Routes/api.php (prefix /human/banks — chi co auth, KHONG co checkPermission)
      Modules/Human/Http/Controllers/Api/V1/BankController.php
      Modules/Human/Services/BankService.php
      Modules/Human/Entities/Bank.php + BankBranch.php
      Modules/Human/Http/Requests/CreateBankRequest.php + CreateBankBranchesRequest.php
      Modules/Human/Transformers/BankResource/*.php
      app/Services/Concerns/LogsCatalogHistory.php + app/Services/CatalogHistoryService.php
  FE  hrm-client/pages/human/banks/index.vue
      hrm-client/pages/human/banks/components/{BankModel,BankBranchesModel,BankBranchesAddModel,BankSearch}.vue
      hrm-client/components/subsystem-menu/master-data.js (menu Danh muc chung -> Ngan hang)

Chay:  python .plans/gop-db/banks-cut-mysql2/gen_testcase.py
"""
import os
import sys

try:  # console Windows mac dinh cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "Danh mục ngân hàng"

# ============================================================ 9 MUC MO TA
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý danh mục ngân hàng dùng chung cho toàn hệ thống: mã, tên, tên viết tắt, tên giao dịch "
     "quốc tế, địa chỉ giao dịch, logo và danh sách chi nhánh của từng ngân hàng.\n"
     "Dữ liệu của màn này là nguồn cho các ô chọn Ngân hàng / Chi nhánh ở hồ sơ nhân sự (tài khoản "
     "ngân hàng của nhân viên, tài khoản uỷ quyền) và cho màn Danh mục tài khoản ngân hàng của công ty.\n"
     "Người dùng làm được: xem danh sách, tìm kiếm, lọc, tạo mới, sửa, xem chi tiết, khóa / mở khóa, "
     "xóa, quản lý chi nhánh và xem lịch sử thay đổi."),

    ("2. Đối tượng được tính / hiển thị",
     "Danh sách hiển thị TẤT CẢ ngân hàng đang có trong danh mục, không phân biệt trạng thái:\n"
     "- Ngân hàng trạng thái Hoạt động — hiển thị nhãn xanh, có đủ nút Sửa / Khóa / Chi nhánh / Lịch sử; "
     "có thêm nút Xóa nếu chưa được sử dụng ở nơi khác.\n"
     "- Ngân hàng trạng thái Khóa — hiển thị nhãn đỏ, chỉ còn nút Mở khóa / Chi nhánh / Lịch sử.\n"
     "- Ngân hàng chưa có chi nhánh nào vẫn hiển thị bình thường, cột Chi nhánh hiện số 0.\n"
     "- Ngân hàng thiếu logo, thiếu tên giao dịch quốc tế hoặc thiếu địa chỉ giao dịch vẫn hiển thị, "
     "ô tương ứng hiện dấu gạch ngang.\n"
     "Trong cửa sổ Chi nhánh: hiển thị các chi nhánh thuộc đúng ngân hàng đang mở và ĐÃ có Tỉnh/Thành phố."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Chi nhánh chưa gán Tỉnh/Thành phố: KHÔNG hiện trong cửa sổ Chi nhánh, nhưng VẪN được cộng vào "
     "con số ở cột Chi nhánh ngoài danh sách (bẫy đối chiếu số liệu, xem mục 9).\n"
     "- Nút Sửa và nút Xóa bị ẩn hẳn (không phải làm mờ) khi ngân hàng đang ở trạng thái Khóa.\n"
     "- Nút Xóa bị ẩn khi ngân hàng đã được dùng ở hồ sơ nhân sự hoặc ở danh mục tài khoản ngân hàng "
     "của công ty.\n"
     "- Nút Xóa của chi nhánh KHÔNG bị ẩn mà bị làm mờ (không bấm được) khi chi nhánh đang được dùng "
     "ở hồ sơ nhân sự — đây là điểm khác biệt có chủ đích so với ngoài danh sách.\n"
     "- Màn hình không có chức năng Xuất Excel, Nhập Excel và In."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng. Màn hình không có bộ lọc theo khoảng thời gian; hai cột thời gian (Ngày tạo, "
     "Ngày cập nhật) chỉ dùng để hiển thị và sắp xếp."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Hai cấp: Ngân hàng → Chi nhánh.\n"
     "- Ngân hàng là bản ghi chính của danh mục, có mã duy nhất và tên duy nhất trên toàn hệ thống.\n"
     "- Chi nhánh luôn thuộc về đúng một ngân hàng; tên chi nhánh chỉ cần duy nhất TRONG PHẠM VI một "
     "ngân hàng (hai ngân hàng khác nhau được phép có cùng tên chi nhánh 'CN Hà Nội').\n"
     "- Xóa ngân hàng sẽ xóa theo toàn bộ chi nhánh của ngân hàng đó.\n"
     "- Chi nhánh không có trạng thái Khóa / Hoạt động riêng."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Cột Chi nhánh ngoài danh sách = tổng số chi nhánh thuộc ngân hàng đó, ĐẾM CẢ chi nhánh chưa "
     "gán Tỉnh/Thành phố.\n"
     "- Không có phép cộng dồn hay khử trùng nào khác trên màn hình.\n"
     "- Ô tìm nhanh quét đồng thời Mã ngân hàng và Tên ngân hàng; một bản ghi khớp cả hai vẫn chỉ "
     "hiện một dòng."),

    ("7. Phân quyền cấp",
     "Màn hình này KHÔNG gắn quyền riêng: mọi tài khoản đã đăng nhập đều nhìn thấy mục menu "
     "\"Ngân hàng\" của phân hệ Danh mục chung và làm được tất cả thao tác (tạo mới, sửa, khóa, xóa, "
     "quản lý chi nhánh).\n"
     "Không có phân quyền theo cấp công ty / phòng ban / bộ phận: mọi người thấy cùng một danh sách.\n"
     "Popup Lịch sử thay đổi cũng không đòi quyền riêng — vào được màn là xem được lịch sử.\n"
     "⚠️ QA lưu ý: đây là hiện trạng đã được rà từ khai báo quyền của hệ thống và từ khai báo menu, "
     "KHÔNG phải lỗi cấu hình của môi trường test. Nếu nghiệp vụ muốn siết lại thì phải bổ sung quyền "
     "mới — khi đó bộ test case này phải sửa lại toàn bộ nhóm Phân quyền & truy cập."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a–b / N\" dưới bảng: a là số thứ tự dòng đầu của trang đang xem, b là số thứ tự "
     "dòng cuối của trang đang xem, N là tổng số ngân hàng khớp bộ lọc (không phải tổng toàn danh mục "
     "khi đang lọc).\n"
     "- Ô \"Số dòng/trang\": chọn 5 / 10 / 20 / 50 / 100, mặc định 10; đổi số dòng thì danh sách quay "
     "về trang 1.\n"
     "- Cột STT đánh liên tục theo trang: trang 2 với 10 dòng/trang bắt đầu từ 11.\n"
     "- Cột Chi nhánh: số chi nhánh của ngân hàng, bấm vào số sẽ mở cửa sổ Chi nhánh."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1. ⚠️ Mũi tên sắp xếp trên tiêu đề cột (Mã ngân hàng, Tên ngân hàng, Ngày tạo, Ngày cập nhật) "
     "hiện ĐỔI CHIỀU nhưng danh sách KHÔNG đổi thứ tự — thứ tự luôn là bản ghi mới nhất trước. Đây là "
     "lỗi đang tồn tại, phải ghi nhận Failed chứ không bỏ qua.\n"
     "2. ⚠️ Cột Chi nhánh và cửa sổ Chi nhánh có thể lệch nhau: chi nhánh chưa gán Tỉnh/Thành phố "
     "được đếm nhưng không hiện trong cửa sổ.\n"
     "3. ⚠️ Ô tìm nhanh khi kết hợp với ô Trạng thái hoặc Tên giao dịch quốc tế: kiểm kỹ kết quả có "
     "thoả mãn ĐỒNG THỜI mọi điều kiện không, đừng chỉ nhìn số dòng.\n"
     "4. ⚠️ Đóng cửa sổ Tạo mới / Sửa khi đang nhập dở: theo thiết kế phải hỏi \"Thông tin chưa lưu\", "
     "thực tế trên môi trường đang dùng cửa sổ đóng thẳng — ghi nhận Failed.\n"
     "5. Chỉ ô Tên ngân hàng bị chặn ngay khi bấm Lưu; ô Mã ngân hàng và Tên viết tắt báo lỗi sau khi "
     "hệ thống kiểm tra, cả ba đều hiện lỗi đỏ ngay dưới ô.\n"
     "6. Trạng thái mặc định của ngân hàng mới tạo luôn là Hoạt động, màn Tạo mới không có ô Trạng thái.\n"
     "7. Bộ lọc được hệ thống ghi nhớ trong 10 phút: rời màn rồi quay lại vẫn còn điều kiện lọc cũ — "
     "test xong nhớ bấm Làm mới trước khi sang ca test khác.\n"
     "8. Danh sách trong cửa sổ Tra cứu là danh sách ngân hàng chuẩn lấy từ dịch vụ tra cứu bên ngoài, "
     "KHÔNG phải dữ liệu của danh mục; bấm chọn chỉ điền sẵn vào form, chưa lưu gì cả.\n"
     "9. Số liệu tham chiếu của môi trường test khi viết tài liệu: 26 ngân hàng, trong đó BIDV có 23 "
     "chi nhánh, VIETCOMBANK có 15, MB có 25."),
]

# ============================================================ TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản bất kỳ đã đăng nhập vào được màn hình", "P0",
     "Tài khoản nhân viên thường, không được gán quyền quản trị nào; danh mục có 26 ngân hàng",
     "1. Đăng nhập bằng tài khoản nhân viên thường\n"
     "2. Vào phân hệ Danh mục chung\n"
     "3. Quan sát menu bên trái\n"
     "4. Bấm mục Ngân hàng",
     "Tài khoản: nhân viên thường (không quyền quản trị)",
     "- Mục Ngân hàng hiển thị trên menu\n"
     "- Vào được màn Danh mục ngân hàng, danh sách hiển thị đủ 26 ngân hàng\n"
     "- ⚠️ Đây là hành vi ĐÚNG theo hiện trạng: màn hình không gắn quyền riêng"),

    ("01", "Tài khoản không quyền quản trị vẫn thấy đủ nút thao tác ghi", "P0",
     "Vẫn tài khoản nhân viên thường ở TC-ROLE-00; dòng ngân hàng ABB đang Hoạt động và chưa được sử dụng",
     "1. Ở màn Danh mục ngân hàng, quan sát thanh công cụ trên bảng\n"
     "2. Quan sát cột Hành động của dòng ABB\n"
     "3. Mở menu ba chấm của dòng đó",
     "—",
     "- Nút Tạo mới hiển thị\n"
     "- Dòng ABB có đủ Sửa, Xóa, Khóa, Chi nhánh, Lịch sử\n"
     "- ⚠️ Không có nút nào bị ẩn vì lý do phân quyền — nếu nghiệp vụ mong đợi bị chặn thì đây là "
     "lỗ hổng cần báo lại, không phải lỗi môi trường"),

    ("02", "Chưa đăng nhập thì không vào được màn hình", "P0",
     "Trình duyệt ở chế độ ẩn danh, chưa đăng nhập hệ thống",
     "1. Mở trình duyệt ẩn danh\n"
     "2. Gõ thẳng đường dẫn /human/banks vào thanh địa chỉ\n"
     "3. Nhấn Enter",
     "Đường dẫn: /human/banks",
     "- Hệ thống chuyển sang màn Đăng nhập\n"
     "- Không hiển thị bất kỳ dữ liệu ngân hàng nào"),

    ("03", "Hết phiên đăng nhập trong lúc đang thao tác", "P1",
     "Đang mở màn Danh mục ngân hàng; phiên đăng nhập đã hết hạn (đăng xuất ở tab khác)",
     "1. Ở tab khác, đăng xuất khỏi hệ thống\n"
     "2. Quay lại tab đang mở màn Danh mục ngân hàng\n"
     "3. Bấm nút Tìm kiếm",
     "—",
     "- Hệ thống đưa về màn Đăng nhập, không treo trang\n"
     "- Không hiển thị dữ liệu cũ như thể vẫn còn đăng nhập"),

    ("04", "Gọi thẳng chức năng Xóa bằng công cụ kiểm thử API, bỏ qua giao diện", "P0",
     "Ngân hàng VIETCOMBANK đang được dùng ở hồ sơ nhân sự nên ngoài danh sách KHÔNG hiện nút Xóa",
     "1. Ghi lại định danh của ngân hàng VIETCOMBANK\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa cho ngân hàng đó, bỏ qua giao diện\n"
     "3. Quay lại màn danh sách, bấm Làm mới",
     "Ngân hàng: VIETCOMBANK",
     "- Hệ thống từ chối, báo \"Không thể xóa bản ghi, ngân hàng đang được sử dụng trên hệ thống\"\n"
     "- Ngân hàng VIETCOMBANK vẫn còn nguyên trong danh sách\n"
     "- ⚠️ Đây là chốt chặn quan trọng nhất của màn: giao diện ẩn nút chỉ là lớp ngoài"),

    ("05", "Gọi thẳng chức năng Khóa bằng công cụ kiểm thử API", "P1",
     "Ngân hàng BIDV đang Hoạt động và đang được sử dụng ở hồ sơ nhân sự",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Khóa cho ngân hàng BIDV\n"
     "2. Quay lại màn danh sách, bấm Làm mới\n"
     "3. Mở popup Lịch sử của BIDV\n"
     "4. Mở khóa lại BIDV để trả môi trường về trạng thái ban đầu",
     "Ngân hàng: BIDV",
     "- Thao tác được chấp nhận: BIDV chuyển sang trạng thái Khóa\n"
     "- Popup Lịch sử ghi nhận mốc Khóa với đúng người thực hiện\n"
     "- ⚠️ Khóa KHÔNG bị chặn dù ngân hàng đang được sử dụng — đúng thiết kế, khác hẳn với Xóa"),
]

# ============================================================ SECTIONS
S1 = [
    (1, "Vào màn hình từ menu", "P0",
     "Đã đăng nhập; danh mục có 26 ngân hàng",
     "1. Vào phân hệ Danh mục chung\n2. Bấm mục Ngân hàng trên menu bên trái",
     "—",
     "- Tiêu đề trang hiển thị \"Danh mục ngân hàng\"\n"
     "- Khối \"Bộ lọc danh sách\" nằm trên, bảng \"Danh mục ngân hàng\" nằm dưới\n"
     "- Danh sách tải xong hiện 10 dòng đầu tiên, dòng dưới bảng ghi \"Hiển thị 1–10 / 26\""),

    (2, "Vào màn hình bằng cách gõ thẳng đường dẫn", "P1",
     "Đã đăng nhập",
     "1. Gõ /human/banks vào thanh địa chỉ\n2. Nhấn Enter",
     "Đường dẫn: /human/banks",
     "- Màn hình hiển thị giống hệt khi vào từ menu\n- Mục Ngân hàng trên menu được tô sáng"),

    (3, "Bố cục mặc định của bảng danh sách", "P0",
     "Tài khoản chưa từng chỉnh Tuỳ chỉnh cột ở màn này",
     "1. Vào màn Danh mục ngân hàng\n2. Quan sát tiêu đề các cột từ trái sang phải",
     "—",
     "- Đúng thứ tự: STT, Mã ngân hàng, Tên ngân hàng, Người tạo, Ngày tạo, Trạng thái, Hành động\n"
     "- Cột Hành động nằm cuối bảng\n"
     "- Các cột Logo, Tên viết tắt, Tên giao dịch quốc tế, Địa chỉ giao dịch, Chi nhánh, Người sửa, "
     "Ngày cập nhật mặc định KHÔNG hiển thị"),

    (4, "Thanh công cụ trên bảng", "P1",
     "Đang ở màn Danh mục ngân hàng",
     "1. Quan sát góc phải phía trên bảng",
     "—",
     "- Có nút Tạo mới (nền xanh, dấu cộng)\n"
     "- Có nút Tuỳ chỉnh cột hiển thị (biểu tượng cột, không có chữ)\n"
     "- Không có nút Xuất Excel, Nhập Excel hay In"),

    (5, "Hiển thị khi ô dữ liệu để trống", "P1",
     "Ngân hàng test01 chưa nhập Tên giao dịch quốc tế; đã bật cột Tên giao dịch quốc tế",
     "1. Bật cột Tên giao dịch quốc tế trong Tuỳ chỉnh cột\n2. Quan sát dòng test01",
     "Ngân hàng: test01",
     "- Ô Tên giao dịch quốc tế hiện dấu gạch ngang (—), không để trắng và không hiện chữ null"),

    (6, "Hiển thị nhãn trạng thái", "P0",
     "Danh mục có cả ngân hàng Hoạt động (test01) và Khóa (trang test 78)",
     "1. Quan sát cột Trạng thái của 2 dòng trên",
     "—",
     "- Dòng test01: nhãn \"Hoạt động\" nền xanh\n"
     "- Dòng trang test 78: nhãn \"Khóa\" nền đỏ\n"
     "- Không hiển thị giá trị số ở cột này"),

    (7, "Bộ nút hành động của dòng đang Hoạt động và chưa được sử dụng", "P0",
     "Ngân hàng 한국은행 đang Hoạt động, chưa gắn với hồ sơ nhân sự nào",
     "1. Quan sát cột Hành động của dòng 한국은행\n2. Mở menu ba chấm",
     "Ngân hàng: 한국은행",
     "- Hiện 2 nút ngoài: Sửa (bút chì), Xóa (thùng rác đỏ)\n"
     "- Menu ba chấm gồm: Khóa, Chi nhánh, Lịch sử"),

    (8, "Bộ nút hành động của dòng đang Hoạt động nhưng đã được sử dụng", "P0",
     "Ngân hàng VIETCOMBANK đang Hoạt động và đã gắn với hồ sơ nhân sự",
     "1. Quan sát cột Hành động của dòng VIETCOMBANK",
     "Ngân hàng: VIETCOMBANK",
     "- Có nút Sửa và nút Khóa\n"
     "- KHÔNG có nút Xóa (ẩn hẳn, không phải làm mờ)\n"
     "- Menu ba chấm còn Chi nhánh và Lịch sử"),

    (9, "Bộ nút hành động của dòng đang Khóa", "P0",
     "Ngân hàng trang test 78 đang ở trạng thái Khóa",
     "1. Quan sát cột Hành động của dòng trang test 78",
     "Ngân hàng: trang test 78",
     "- Chỉ còn Mở khóa, Chi nhánh, Lịch sử\n"
     "- KHÔNG có Sửa, KHÔNG có Xóa"),

    (10, "Bấm mã ngân hàng để xem nhanh", "P0",
     "Danh sách đang hiển thị dòng VIETCOMBANK",
     "1. Bấm vào chữ VIETCOMBANK ở cột Mã ngân hàng",
     "—",
     "- Mở cửa sổ \"Xem ngân hàng\", không điều hướng sang trang khác\n"
     "- Mọi ô đều ở chế độ chỉ đọc"),

    (11, "Trạng thái danh sách rỗng", "P1",
     "Danh mục có 26 ngân hàng",
     "1. Nhập vào ô tìm nhanh chuỗi không tồn tại\n2. Bấm Tìm kiếm",
     "Từ khoá: zzz-khong-ton-tai",
     "- Bảng hiện dòng \"Không có dữ liệu phù hợp bộ lọc.\"\n"
     "- Dòng thống kê hiện \"Hiển thị 0–0 / 0\"\n- Không báo lỗi"),

    (12, "Hiệu ứng chờ khi tải danh sách", "P2",
     "Đường truyền bình thường",
     "1. Bấm Làm mới\n2. Quan sát vùng bảng trong lúc chờ",
     "—",
     "- Có hiệu ứng đang tải, không hiện bảng trắng nhấp nháy\n"
     "- Tải xong thì hiệu ứng biến mất"),

    (13, "Logo hiển thị đúng tỉ lệ trên danh sách", "P2",
     "Đã bật cột Logo; ngân hàng SHB có logo, ngân hàng 한국은행 chưa có logo",
     "1. Bật cột Logo\n2. Quan sát dòng SHB và dòng 한국은행",
     "—",
     "- Dòng SHB: logo hiện gọn trong ô, không méo, không tràn ra ngoài\n"
     "- Dòng 한국은행: ô Logo hiện dấu gạch ngang"),
]

S2 = [
    (1, "Tìm nhanh theo mã ngân hàng", "P0",
     "Danh mục có ngân hàng mã VIETCOMBANK",
     "1. Nhập từ khoá vào ô \"Tìm theo mã, tên ngân hàng...\"\n2. Bấm Tìm kiếm",
     "Từ khoá: VIETCOM",
     "- Kết quả chỉ còn các ngân hàng có mã hoặc tên chứa chuỗi VIETCOM\n"
     "- Dòng thống kê cập nhật đúng số bản ghi tìm được"),

    (2, "Tìm nhanh theo tên ngân hàng", "P0",
     "Danh mục có \"Ngân hàng TMCP An Bình\" mã ABB",
     "1. Nhập từ khoá\n2. Bấm Tìm kiếm",
     "Từ khoá: An Bình",
     "- Dòng ABB nằm trong kết quả\n- Các ngân hàng không chứa chuỗi này bị loại khỏi danh sách"),

    (3, "Tìm nhanh khớp một phần ở giữa chuỗi", "P1",
     "Danh mục có \"Ngân hàng Thương mại Cổ phần Sài Gòn - Hà Nội\"",
     "1. Nhập từ khoá\n2. Bấm Tìm kiếm",
     "Từ khoá: Sài Gòn",
     "- Vẫn tìm ra ngân hàng SHB dù chuỗi nằm giữa tên"),

    (4, "Tìm nhanh không phân biệt chữ hoa chữ thường", "P1",
     "Danh mục có mã ABB",
     "1. Nhập từ khoá chữ thường\n2. Bấm Tìm kiếm\n3. Nhập lại bằng chữ hoa, bấm Tìm kiếm",
     "Từ khoá: abb → ABB",
     "- Hai lần tìm cho ra cùng một danh sách kết quả"),

    (5, "Nhấn Enter trong ô tìm nhanh", "P1",
     "Đang ở màn danh sách",
     "1. Nhập từ khoá vào ô tìm nhanh\n2. Nhấn phím Enter",
     "Từ khoá: BIDV",
     "- Danh sách lọc ngay, không cần bấm nút Tìm kiếm"),

    (6, "Gõ từ khoá nhưng chưa bấm Tìm kiếm", "P0",
     "Danh sách đang hiển thị đủ 26 ngân hàng",
     "1. Gõ từ khoá vào ô tìm nhanh\n2. Chờ 3 giây, KHÔNG bấm gì thêm",
     "Từ khoá: BIDV",
     "- Danh sách GIỮ NGUYÊN 26 dòng, chưa lọc\n"
     "- ⚠️ Ô tìm nhanh chỉ có tác dụng khi bấm Tìm kiếm hoặc nhấn Enter"),

    (7, "Xoá nhanh từ khoá bằng dấu x trong ô", "P2",
     "Ô tìm nhanh đang chứa từ khoá BIDV và danh sách đang lọc",
     "1. Bấm dấu x ở cuối ô tìm nhanh\n2. Bấm Tìm kiếm",
     "—",
     "- Ô tìm nhanh trống\n- Danh sách trở lại đủ 26 ngân hàng"),

    (8, "Lọc theo Tên giao dịch quốc tế", "P0",
     "Ngân hàng SHB có tên giao dịch quốc tế \"Saigon – Hanoi Commercial Joint Stock Bank\"",
     "1. Nhập vào ô \"Nhập tên giao dịch quốc tế\"\n2. Bấm Tìm kiếm",
     "Tên giao dịch quốc tế: Hanoi",
     "- Kết quả chỉ gồm ngân hàng có tên giao dịch quốc tế chứa chuỗi Hanoi\n"
     "- Ngân hàng chưa nhập tên giao dịch quốc tế không xuất hiện"),

    (9, "Lọc theo trạng thái Hoạt động", "P0",
     "Danh mục có 26 ngân hàng, trong đó một số đang Khóa",
     "1. Chọn ô Trạng thái = Hoạt động\n2. Bấm Tìm kiếm",
     "Trạng thái: Hoạt động",
     "- Mọi dòng trong kết quả đều mang nhãn Hoạt động\n- Không còn dòng nào nhãn Khóa"),

    (10, "Lọc theo trạng thái Khóa", "P0",
     "Danh mục có ít nhất 3 ngân hàng đang Khóa (trang test 78, VC, DBS)",
     "1. Chọn ô Trạng thái = Khóa\n2. Bấm Tìm kiếm",
     "Trạng thái: Khóa",
     "- Kết quả chứa đúng các ngân hàng đang Khóa, trong đó có trang test 78, VC, DBS\n"
     "- Mọi dòng đều chỉ còn nút Mở khóa / Chi nhánh / Lịch sử"),

    (11, "Bỏ chọn trạng thái để lấy lại tất cả", "P1",
     "Đang lọc theo Trạng thái = Khóa",
     "1. Bấm dấu x để bỏ chọn ở ô Trạng thái\n2. Bấm Tìm kiếm",
     "—",
     "- Danh sách trở lại đủ 26 ngân hàng, gồm cả Hoạt động lẫn Khóa"),

    (12, "Kết hợp từ khoá và trạng thái", "P0",
     "Ngân hàng \"trang test 78\" đang Khóa; ngân hàng test01 đang Hoạt động; cả hai đều chứa chữ trang",
     "1. Nhập từ khoá vào ô tìm nhanh\n2. Chọn Trạng thái = Khóa\n3. Bấm Tìm kiếm",
     "Từ khoá: trang | Trạng thái: Khóa",
     "- Kết quả chỉ gồm ngân hàng vừa chứa chữ trang vừa đang Khóa\n"
     "- ⚠️ Kiểm TỪNG DÒNG: dòng test01 (Hoạt động) tuyệt đối không được lọt vào kết quả"),

    (13, "Kết hợp từ khoá và Tên giao dịch quốc tế", "P0",
     "Ngân hàng SHB có tên giao dịch quốc tế chứa Hanoi; ngân hàng ABB chưa có tên giao dịch quốc tế",
     "1. Nhập ô tìm nhanh: Ngân hàng\n2. Nhập ô Tên giao dịch quốc tế: Hanoi\n3. Bấm Tìm kiếm",
     "Từ khoá: Ngân hàng | Tên giao dịch quốc tế: Hanoi",
     "- ⚠️ Kiểm từng dòng: mỗi dòng phải thoả ĐỒNG THỜI hai điều kiện\n"
     "- Dòng ABB không được xuất hiện"),

    (14, "Nút Làm mới xoá toàn bộ điều kiện lọc", "P0",
     "Đang lọc: từ khoá BIDV + Trạng thái Hoạt động, danh sách còn 1 dòng",
     "1. Bấm nút Làm mới\n2. Quan sát cả ô lọc lẫn danh sách",
     "—",
     "- Cả 3 ô lọc trở về trống\n"
     "- Danh sách tải lại đủ 26 ngân hàng ngay lập tức (không phải chỉ xoá chữ trong ô)"),

    (15, "Lọc xong luôn quay về trang 1", "P1",
     "Đang đứng ở trang 3 của danh sách",
     "1. Bấm sang trang 3\n2. Nhập từ khoá Ngân hàng\n3. Bấm Tìm kiếm",
     "Từ khoá: Ngân hàng",
     "- Kết quả hiển thị từ trang 1\n- Dòng thống kê bắt đầu bằng \"Hiển thị 1–\""),

    (16, "Từ khoá chứa ký tự đặc biệt của phép tìm gần đúng", "P1",
     "Danh mục có 26 ngân hàng, không ngân hàng nào có tên chứa dấu phần trăm",
     "1. Nhập ký tự % vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "Từ khoá: %",
     "- Không được trả về toàn bộ 26 ngân hàng\n"
     "- Kết quả rỗng hoặc chỉ gồm ngân hàng thật sự có ký tự % trong mã / tên"),

    (17, "Từ khoá chỉ gồm dấu cách", "P2",
     "Danh mục có 26 ngân hàng",
     "1. Nhập 2 dấu cách vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "Từ khoá: (2 dấu cách)",
     "- Hệ thống không báo lỗi\n- Danh sách vẫn hiển thị bình thường"),

    (18, "Hệ thống ghi nhớ bộ lọc khi rời màn rồi quay lại", "P1",
     "Đang lọc Trạng thái = Khóa",
     "1. Bấm Tìm kiếm với Trạng thái = Khóa\n2. Sang màn khác trong cùng phân hệ\n"
     "3. Trong vòng 10 phút, quay lại màn Danh mục ngân hàng",
     "Trạng thái: Khóa",
     "- Ô Trạng thái vẫn giữ giá trị Khóa và danh sách vẫn đang lọc\n"
     "- ⚠️ Đây là hành vi cố ý (nhớ 10 phút), không phải lỗi không làm mới"),

    (19, "Bộ lọc hết hạn ghi nhớ", "P2",
     "Đã lọc Trạng thái = Khóa rồi rời màn hình quá 10 phút",
     "1. Lọc Trạng thái = Khóa\n2. Rời màn quá 10 phút\n3. Quay lại màn Danh mục ngân hàng",
     "—",
     "- Bộ lọc trở về trống\n- Danh sách hiển thị đủ 26 ngân hàng"),
]

S3 = [
    (1, "Phân trang mặc định", "P0",
     "Danh mục có 26 ngân hàng, số dòng/trang mặc định 10",
     "1. Vào màn Danh mục ngân hàng\n2. Quan sát vùng dưới bảng",
     "—",
     "- Có 3 trang\n- Dòng thống kê: \"Hiển thị 1–10 / 26\"\n- Ô số dòng/trang hiện 10"),

    (2, "Chuyển sang trang kế tiếp", "P0",
     "Đang ở trang 1 với 10 dòng/trang, tổng 26 ngân hàng",
     "1. Bấm nút mũi tên sang phải (hoặc số 2)",
     "—",
     "- Hiển thị 10 dòng tiếp theo\n- Dòng thống kê: \"Hiển thị 11–20 / 26\"\n"
     "- Cột STT bắt đầu từ 11"),

    (3, "Chuyển tới trang cuối", "P1",
     "Tổng 26 ngân hàng, 10 dòng/trang",
     "1. Bấm nút về trang cuối (>>)",
     "—",
     "- Trang 3 hiển thị 6 dòng\n- Dòng thống kê: \"Hiển thị 21–26 / 26\"\n"
     "- Nút sang trang tiếp và về trang cuối bị vô hiệu hoá"),

    (4, "Chuyển về trang đầu", "P1",
     "Đang ở trang 3",
     "1. Bấm nút về trang đầu (<<)",
     "—",
     "- Trở về trang 1, hiển thị 10 dòng đầu\n- Nút về trang đầu và trang trước bị vô hiệu hoá"),

    (5, "Đổi số dòng/trang thành 50", "P0",
     "Tổng 26 ngân hàng, đang ở trang 2",
     "1. Chọn ô Số dòng/trang = 50",
     "Số dòng/trang: 50",
     "- Toàn bộ 26 ngân hàng hiển thị trên 1 trang\n"
     "- Quay về trang 1, dòng thống kê: \"Hiển thị 1–26 / 26\""),

    (6, "Đổi số dòng/trang thành 5", "P1",
     "Tổng 26 ngân hàng",
     "1. Chọn ô Số dòng/trang = 5",
     "Số dòng/trang: 5",
     "- Mỗi trang 5 dòng, tổng 6 trang\n- Quay về trang 1"),

    (7, "Danh sách các mức số dòng/trang", "P2",
     "Đang ở màn danh sách",
     "1. Mở ô Số dòng/trang",
     "—",
     "- Có đúng 5 lựa chọn: 5, 10, 20, 50, 100"),

    (8, "Phân trang giữ nguyên bộ lọc", "P0",
     "Đang lọc Trạng thái = Hoạt động và kết quả có hơn 10 dòng",
     "1. Lọc Trạng thái = Hoạt động\n2. Sang trang 2\n3. Kiểm tra nhãn trạng thái của mọi dòng",
     "Trạng thái: Hoạt động",
     "- Trang 2 vẫn chỉ chứa ngân hàng Hoạt động\n- Ô lọc không bị xoá khi chuyển trang"),

    (9, "Không trùng và không sót dữ liệu giữa các trang", "P0",
     "Tổng 26 ngân hàng, 10 dòng/trang",
     "1. Ghi lại mã ngân hàng của cả 3 trang\n2. Đối chiếu 26 mã thu được",
     "—",
     "- Đủ 26 mã, không mã nào lặp lại ở 2 trang\n- Không mã nào bị thiếu"),

    (10, "Sắp xếp theo Mã ngân hàng", "P0",
     "Danh sách đang ở thứ tự mặc định (bản ghi mới nhất trước)",
     "1. Bấm vào tiêu đề cột Mã ngân hàng\n2. Quan sát thứ tự các dòng\n3. Bấm lần nữa để đổi chiều",
     "—",
     "- Mong đợi: danh sách xếp theo mã tăng dần, bấm lần 2 xếp giảm dần\n"
     "- ⚠️ Hiện tại mũi tên đổi chiều nhưng thứ tự dòng KHÔNG đổi — ghi nhận Failed"),

    (11, "Sắp xếp theo Tên ngân hàng", "P0",
     "Danh sách đang ở thứ tự mặc định",
     "1. Bấm tiêu đề cột Tên ngân hàng\n2. Đối chiếu thứ tự chữ cái đầu",
     "—",
     "- Mong đợi: xếp theo tên A→Z, bấm lần 2 xếp Z→A\n"
     "- ⚠️ Cùng lỗi với TC_03.010: thứ tự không đổi"),

    (12, "Sắp xếp theo Ngày tạo", "P1",
     "Danh mục có ngân hàng tạo ngày 11/08/2026 và ngân hàng tạo ngày 25/12/2025",
     "1. Bấm tiêu đề cột Ngày tạo\n2. Quan sát dòng đầu tiên",
     "—",
     "- Mong đợi: xếp theo ngày tạo cũ nhất trước, bấm lần 2 mới nhất trước\n"
     "- ⚠️ Cùng lỗi sắp xếp"),

    (13, "Sắp xếp theo Ngày cập nhật", "P1",
     "Đã bật cột Ngày cập nhật trong Tuỳ chỉnh cột",
     "1. Bật cột Ngày cập nhật\n2. Bấm tiêu đề cột đó",
     "—",
     "- Mong đợi: xếp theo ngày cập nhật\n- ⚠️ Cùng lỗi sắp xếp"),

    (14, "Cột không cho sắp xếp", "P2",
     "Đang ở màn danh sách",
     "1. Bấm lần lượt vào tiêu đề Người tạo, Trạng thái, Hành động",
     "—",
     "- Ba cột này không có biểu tượng sắp xếp và bấm vào không xảy ra gì\n- Không báo lỗi"),

    (15, "Mở popup Tuỳ chỉnh cột", "P0",
     "Đang ở màn danh sách",
     "1. Bấm nút biểu tượng cột bên cạnh nút Tạo mới",
     "—",
     "- Mở popup tiêu đề \"Tuỳ chỉnh cột\"\n"
     "- Liệt kê đủ 13 cột của bảng, cột đang hiện được tích sẵn\n"
     "- Có nút Lưu và nút Đóng"),

    (16, "Cột bị khoá trong Tuỳ chỉnh cột", "P0",
     "Đang mở popup Tuỳ chỉnh cột",
     "1. Thử bỏ tích ở dòng STT\n2. Thử bỏ tích ở dòng Mã ngân hàng",
     "—",
     "- Hai dòng này hiện biểu tượng ổ khoá, không bỏ tích được\n"
     "- ⚠️ Đây là chốt để danh sách luôn còn cột định danh"),

    (17, "Bật thêm cột và lưu lại", "P0",
     "Popup Tuỳ chỉnh cột đang mở, cột Chi nhánh đang tắt",
     "1. Tích vào dòng Chi nhánh\n2. Bấm Lưu\n3. Quan sát bảng",
     "Cột bật thêm: Chi nhánh",
     "- Popup đóng, bảng hiện thêm cột Chi nhánh\n"
     "- Tải lại trang thì cột Chi nhánh vẫn hiện (ghi nhớ theo tài khoản)"),

    (18, "Tắt bớt cột", "P1",
     "Cột Chi nhánh đang hiện",
     "1. Mở Tuỳ chỉnh cột\n2. Bỏ tích dòng Chi nhánh\n3. Bấm Lưu",
     "—",
     "- Cột Chi nhánh biến mất khỏi bảng, các cột còn lại giữ nguyên thứ tự"),

    (19, "Đổi vị trí cột bằng kéo thả", "P1",
     "Popup Tuỳ chỉnh cột đang mở",
     "1. Kéo dòng Tên ngân hàng xuống dưới dòng Người tạo\n2. Bấm Lưu",
     "—",
     "- Bảng hiển thị cột Tên ngân hàng ở vị trí mới\n- Dữ liệu từng cột vẫn đúng, không lệch cột"),

    (20, "Đóng popup Tuỳ chỉnh cột không lưu", "P1",
     "Đã tích thêm cột Logo nhưng chưa bấm Lưu",
     "1. Tích cột Logo\n2. Bấm Đóng",
     "—",
     "- Popup đóng\n- Bảng KHÔNG hiện thêm cột Logo"),
]

S4 = [
    (1, "Mở cửa sổ Tạo mới", "P0",
     "Đang ở màn Danh mục ngân hàng",
     "1. Bấm nút Tạo mới",
     "—",
     "- Mở cửa sổ tiêu đề \"Tạo ngân hàng\"\n"
     "- Đủ các ô: Gợi ý + nút Tra cứu, Mã ngân hàng, Tên ngân hàng, Tên viết tắt, Tên giao dịch "
     "quốc tế, Địa chỉ giao dịch, Logo\n"
     "- Ba ô Mã ngân hàng, Tên ngân hàng, Tên viết tắt có dấu sao đỏ"),

    (2, "Giá trị điền sẵn khi tạo mới", "P0",
     "Vừa mở cửa sổ Tạo ngân hàng",
     "1. Quan sát toàn bộ các ô nhập",
     "—",
     "- Tất cả các ô đều trống\n- Khung Logo hiện chữ \"Chưa có logo\"\n"
     "- KHÔNG có ô Trạng thái (ngân hàng mới luôn ở trạng thái Hoạt động)\n"
     "- Chân cửa sổ có 3 nút: Lưu, Lưu và tiếp tục, Đóng"),

    (3, "Tạo mới đầy đủ thông tin", "P0",
     "Danh mục chưa có mã QA01",
     "1. Bấm Tạo mới\n2. Nhập Mã ngân hàng, Tên ngân hàng, Tên viết tắt, Tên giao dịch quốc tế, "
     "Địa chỉ giao dịch\n3. Bấm Lưu",
     "Mã ngân hàng: QA01 | Tên ngân hàng: Ngân hàng kiểm thử QA01 | Tên viết tắt: QATEST | "
     "Tên giao dịch quốc tế: QA Test Bank | Địa chỉ giao dịch: 123 Nguyễn Trãi, Hà Nội",
     "- Hệ thống báo \"Đã lưu thành công!\"\n- Cửa sổ đóng lại\n"
     "- Ngân hàng QA01 xuất hiện ở đầu danh sách với trạng thái Hoạt động\n"
     "- Cột Người tạo là người đang đăng nhập, Ngày tạo là ngày giờ hiện tại"),

    (4, "Tạo mới chỉ với 3 ô bắt buộc", "P0",
     "Danh mục chưa có mã QA02",
     "1. Bấm Tạo mới\n2. Chỉ nhập Mã ngân hàng, Tên ngân hàng, Tên viết tắt\n3. Bấm Lưu",
     "Mã ngân hàng: QA02 | Tên ngân hàng: Ngân hàng kiểm thử QA02 | Tên viết tắt: QA02",
     "- Lưu thành công\n"
     "- Trên danh sách, ô Tên giao dịch quốc tế và Địa chỉ giao dịch hiện dấu gạch ngang"),

    (5, "Lưu và tiếp tục", "P0",
     "Danh mục chưa có mã QA03 và QA04",
     "1. Bấm Tạo mới\n2. Nhập đủ 3 ô bắt buộc cho QA03\n3. Bấm \"Lưu và tiếp tục\"\n"
     "4. Nhập tiếp QA04 rồi bấm Lưu",
     "Lần 1: QA03 | Lần 2: QA04",
     "- Sau lần 1: báo lưu thành công, cửa sổ VẪN MỞ và mọi ô trở về trống\n"
     "- Sau lần 2: cửa sổ đóng, danh sách có cả QA03 lẫn QA04"),

    (6, "Bỏ trống toàn bộ rồi bấm Lưu", "P0",
     "Vừa mở cửa sổ Tạo ngân hàng, chưa nhập gì",
     "1. Bấm Tạo mới\n2. Bấm ngay nút Lưu",
     "—",
     "- Dòng chữ đỏ \"Bắt buộc phải nhập\" hiện ngay dưới ô Tên ngân hàng\n"
     "- Hệ thống báo \"Vui lòng kiểm tra lại thông tin\"\n"
     "- Cửa sổ KHÔNG đóng, không tạo bản ghi nào"),

    (7, "Chỉ nhập Tên ngân hàng rồi bấm Lưu", "P0",
     "Vừa mở cửa sổ Tạo ngân hàng",
     "1. Nhập Tên ngân hàng\n2. Bỏ trống Mã ngân hàng và Tên viết tắt\n3. Bấm Lưu",
     "Tên ngân hàng: Ngân hàng kiểm thử QA05",
     "- Lỗi đỏ \"Bắt buộc phải nhập\" hiện dưới ô Mã ngân hàng VÀ dưới ô Tên viết tắt\n"
     "- Cửa sổ không đóng, dữ liệu đã nhập vẫn còn nguyên"),

    (8, "Trùng mã ngân hàng", "P0",
     "Danh mục đã có ngân hàng mã VIETCOMBANK",
     "1. Bấm Tạo mới\n2. Nhập Mã ngân hàng trùng, Tên ngân hàng mới, Tên viết tắt bất kỳ\n3. Bấm Lưu",
     "Mã ngân hàng: VIETCOMBANK | Tên ngân hàng: Ngân hàng kiểm thử trùng mã | Tên viết tắt: QATRUNG",
     "- Lỗi đỏ \"Mã ngân hàng này đã tồn tại\" hiện dưới ô Mã ngân hàng\n"
     "- Không tạo bản ghi mới, cửa sổ không đóng"),

    (9, "Trùng tên ngân hàng", "P0",
     "Danh mục đã có \"Ngân hàng TMCP Ngoại thương Việt Nam\"",
     "1. Bấm Tạo mới\n2. Nhập Mã ngân hàng mới nhưng Tên ngân hàng trùng\n3. Bấm Lưu",
     "Mã ngân hàng: QA06 | Tên ngân hàng: Ngân hàng TMCP Ngoại thương Việt Nam | Tên viết tắt: QA06",
     "- Lỗi đỏ \"Tên ngân hàng này đã tồn tại\" hiện dưới ô Tên ngân hàng"),

    (10, "Trùng cả mã và tên", "P1",
     "Danh mục đã có ngân hàng mã VIETCOMBANK tên Ngân hàng TMCP Ngoại thương Việt Nam",
     "1. Bấm Tạo mới\n2. Nhập trùng cả mã lẫn tên\n3. Bấm Lưu",
     "Mã ngân hàng: VIETCOMBANK | Tên ngân hàng: Ngân hàng TMCP Ngoại thương Việt Nam | Tên viết tắt: QA07",
     "- Hai lỗi đỏ hiện đồng thời dưới cả hai ô, không phải lần lượt từng lỗi một"),

    (11, "Mã ngân hàng khác nhau ở chữ hoa chữ thường", "P1",
     "Danh mục đã có mã ABB",
     "1. Bấm Tạo mới\n2. Nhập mã bằng chữ thường\n3. Bấm Lưu",
     "Mã ngân hàng: abb | Tên ngân hàng: Ngân hàng kiểm thử chữ thường | Tên viết tắt: QA08",
     "- Ghi nhận kết quả thực tế: hệ thống có coi abb trùng với ABB hay không\n"
     "- Nếu lưu được thì danh sách phải hiện đủ cả hai dòng, không dòng nào ghi đè dòng nào"),

    (12, "Dùng nút Tra cứu để điền nhanh", "P0",
     "Cửa sổ Tạo ngân hàng đang mở",
     "1. Nhập chữ vietcom vào ô Gợi ý\n2. Bấm nút Tra cứu\n3. Bấm vào dòng Ngân hàng TMCP Ngoại "
     "Thương Việt Nam trong danh sách",
     "Gợi ý: vietcom",
     "- Mở cửa sổ \"Thông tin ngân hàng\" kèm dòng hướng dẫn \"Click vào một dòng để điền nhanh thông tin\"\n"
     "- Danh sách đã lọc theo chữ vietcom\n"
     "- Bấm chọn xong: cửa sổ đóng, các ô Mã ngân hàng, Tên ngân hàng, Tên viết tắt và Logo được "
     "điền sẵn theo dòng đã chọn"),

    (13, "Danh sách tra cứu là nguồn ngoài, không phải danh mục", "P1",
     "Danh mục nội bộ có 26 ngân hàng",
     "1. Mở cửa sổ Tạo ngân hàng\n2. Bấm Tra cứu khi ô Gợi ý còn trống\n3. Đối chiếu với danh sách "
     "ngoài màn hình",
     "—",
     "- Cửa sổ tra cứu liệt kê danh sách ngân hàng chuẩn (nhiều hơn và khác với 26 ngân hàng của danh mục)\n"
     "- ⚠️ Chọn một dòng chỉ điền sẵn vào form, chưa tạo bản ghi nào"),

    (14, "Đóng cửa sổ tra cứu mà không chọn", "P2",
     "Cửa sổ Thông tin ngân hàng đang mở",
     "1. Bấm nút Đóng của cửa sổ tra cứu",
     "—",
     "- Chỉ cửa sổ tra cứu đóng, cửa sổ Tạo ngân hàng vẫn mở\n- Dữ liệu đang nhập dở không bị mất"),

    (15, "Tải logo hợp lệ", "P0",
     "Có sẵn file ảnh logo.png dung lượng 200 KB",
     "1. Mở cửa sổ Tạo ngân hàng\n2. Bấm Tải ảnh lên\n3. Chọn file logo.png",
     "File: logo.png (200 KB)",
     "- Khung xem trước hiện ảnh vừa chọn\n- Xuất hiện thêm nút Xóa ảnh\n- Không báo lỗi"),

    (16, "Tải logo quá dung lượng cho phép", "P0",
     "Có sẵn file ảnh 8 MB",
     "1. Bấm Tải ảnh lên\n2. Chọn file 8 MB",
     "File: logo-lon.png (8 MB)",
     "- Hiện lỗi đỏ \"Dung lượng tối đa: 5MB\" dưới khung Logo\n- Khung xem trước không nhận ảnh"),

    (17, "Tải tệp sai định dạng", "P0",
     "Có sẵn file tài liệu bat-ky.pdf",
     "1. Bấm Tải ảnh lên\n2. Chọn file bat-ky.pdf",
     "File: bat-ky.pdf",
     "- Hiện lỗi đỏ \"File không hợp lệ\"\n- Khung xem trước không nhận tệp\n"
     "- ⚠️ Chỉ chấp nhận .jpg, .jpeg, .png như dòng chú thích cạnh nhãn Logo"),

    (18, "Xoá ảnh đã chọn", "P1",
     "Đã chọn logo hợp lệ trong cửa sổ Tạo ngân hàng",
     "1. Bấm nút Xóa ảnh",
     "—",
     "- Khung xem trước trở lại chữ \"Chưa có logo\"\n- Nút Xóa ảnh biến mất"),

    (19, "Chú thích định dạng ảnh", "P2",
     "Cửa sổ Tạo ngân hàng đang mở",
     "1. Rê chuột vào biểu tượng chấm than cạnh nhãn Logo",
     "—",
     "- Hiện chú thích \"Các loại ảnh có thể tải lên (tối đa 5Mb): .jpg, .jpeg, .png\""),

    (20, "Đóng cửa sổ Tạo mới khi chưa nhập gì", "P1",
     "Vừa mở cửa sổ Tạo ngân hàng",
     "1. Bấm nút Đóng",
     "—",
     "- Cửa sổ đóng ngay, không hỏi lại\n- Danh sách không thay đổi"),

    (21, "Đóng cửa sổ Tạo mới khi đang nhập dở", "P0",
     "Cửa sổ Tạo ngân hàng đang mở",
     "1. Nhập Mã ngân hàng: QA09\n2. Bấm nút Đóng",
     "Mã ngân hàng: QA09",
     "- Mong đợi: hệ thống hỏi lại \"Thông tin chưa lưu\" trước khi đóng\n"
     "- ⚠️ Thực tế hiện tại cửa sổ đóng thẳng, mất dữ liệu đang nhập — ghi nhận Failed"),

    (22, "Mở cửa sổ Sửa", "P0",
     "Ngân hàng VIETCOMBANK đang Hoạt động",
     "1. Bấm nút Sửa (bút chì) ở dòng VIETCOMBANK",
     "—",
     "- Mở cửa sổ tiêu đề \"Sửa ngân hàng\"\n"
     "- Các ô đã điền sẵn dữ liệu hiện tại, khung Logo hiện logo hiện có\n"
     "- Chân cửa sổ chỉ có 2 nút: Lưu và Đóng (KHÔNG có Lưu và tiếp tục)"),

    (23, "Sửa tên ngân hàng và lưu", "P0",
     "Ngân hàng QA01 vừa tạo ở TC_04.003",
     "1. Bấm Sửa dòng QA01\n2. Đổi Tên ngân hàng\n3. Bấm Lưu",
     "Tên ngân hàng mới: Ngân hàng kiểm thử QA01 - đã sửa",
     "- Báo \"Đã lưu thành công!\", cửa sổ đóng\n"
     "- Danh sách hiện tên mới\n- Cột Người sửa và Ngày cập nhật đổi theo người đang đăng nhập"),

    (24, "Sửa và bỏ trống ô bắt buộc", "P0",
     "Đang mở cửa sổ Sửa của ngân hàng QA01",
     "1. Xoá trắng ô Tên viết tắt\n2. Bấm Lưu",
     "Tên viết tắt: (để trống)",
     "- Lỗi đỏ \"Bắt buộc phải nhập\" dưới ô Tên viết tắt\n- Không lưu, dữ liệu cũ trong danh sách giữ nguyên"),

    (25, "Sửa mã trùng với ngân hàng khác", "P0",
     "Đang sửa QA02; danh mục đã có mã VIETCOMBANK",
     "1. Bấm Sửa dòng QA02\n2. Đổi Mã ngân hàng thành VIETCOMBANK\n3. Bấm Lưu",
     "Mã ngân hàng: VIETCOMBANK",
     "- Lỗi đỏ \"Mã ngân hàng này đã tồn tại\"\n- Không lưu"),

    (26, "Sửa mà giữ nguyên chính mã của mình", "P0",
     "Đang sửa ngân hàng QA02 (mã QA02)",
     "1. Bấm Sửa dòng QA02\n2. Giữ nguyên mã, chỉ đổi Địa chỉ giao dịch\n3. Bấm Lưu",
     "Địa chỉ giao dịch: 88 Láng Hạ, Hà Nội",
     "- Lưu thành công, KHÔNG báo trùng mã với chính nó\n- Địa chỉ mới hiển thị đúng"),

    (27, "Đổi logo khi sửa", "P1",
     "Ngân hàng QA01 đang có logo",
     "1. Bấm Sửa dòng QA01\n2. Bấm Tải ảnh lên, chọn ảnh khác\n3. Bấm Lưu",
     "File: logo-moi.png (300 KB)",
     "- Lưu thành công, cột Logo ngoài danh sách hiện ảnh mới\n"
     "- ⚠️ Popup Lịch sử KHÔNG ghi nhận việc đổi logo — đúng thiết kế hiện tại"),

    (28, "Sửa nhưng không thay đổi gì rồi bấm Lưu", "P1",
     "Ngân hàng QA02 đã có lịch sử thay đổi",
     "1. Bấm Sửa dòng QA02\n2. Không sửa ô nào\n3. Bấm Lưu\n4. Mở popup Lịch sử",
     "—",
     "- Vẫn báo lưu thành công\n"
     "- Popup Lịch sử KHÔNG phát sinh thêm mốc \"Thay đổi thông tin\" (không có gì thay đổi thì không ghi)"),

    (29, "Mở cửa sổ Xem", "P0",
     "Ngân hàng VIETCOMBANK đang Hoạt động",
     "1. Bấm vào chữ VIETCOMBANK ở cột Mã ngân hàng",
     "—",
     "- Cửa sổ tiêu đề \"Xem ngân hàng\"\n"
     "- Mọi ô ở chế độ chỉ đọc, không gõ sửa được\n"
     "- Có thêm ô Trạng thái hiện \"Hoạt động\"\n"
     "- Chân cửa sổ chỉ có nút Đóng"),

    (30, "Cửa sổ Xem không có công cụ chỉnh sửa", "P0",
     "Cửa sổ Xem ngân hàng đang mở",
     "1. Quan sát toàn bộ nội dung cửa sổ",
     "—",
     "- Không có ô Gợi ý và nút Tra cứu\n- Không có nút Tải ảnh lên, Xóa ảnh\n"
     "- Không có nút Lưu"),

    (31, "Xem ngân hàng đang Khóa", "P1",
     "Ngân hàng trang test 78 đang Khóa",
     "1. Bấm vào mã trang test 78",
     "—",
     "- Vẫn mở được cửa sổ Xem\n- Ô Trạng thái hiện \"Khoá\""),

    (32, "Mở Sửa ngay sau khi đóng Xem", "P0",
     "Vừa xem ngân hàng VIETCOMBANK và đã đóng cửa sổ",
     "1. Bấm mã VIETCOMBANK để xem\n2. Bấm Đóng\n3. Bấm nút Sửa của chính dòng đó",
     "—",
     "- Cửa sổ mở ở chế độ Sửa: tiêu đề \"Sửa ngân hàng\", các ô nhập được, có nút Lưu\n"
     "- ⚠️ Không được mở nhầm lại chế độ chỉ đọc"),

    (33, "Mở Sửa hai dòng liên tiếp", "P0",
     "Danh sách có dòng VIETCOMBANK và dòng ABB",
     "1. Bấm Sửa dòng VIETCOMBANK, xem dữ liệu rồi bấm Đóng\n2. Bấm Sửa dòng ABB",
     "—",
     "- Cửa sổ lần 2 hiển thị đúng dữ liệu của ABB\n"
     "- ⚠️ Không được còn sót dữ liệu của VIETCOMBANK"),
]

S5 = [
    (1, "Mở hộp xác nhận Khóa", "P0",
     "Ngân hàng BIDV đang Hoạt động",
     "1. Bấm nút Khóa (ổ khoá) ở dòng BIDV",
     "—",
     "- Hộp thoại tiêu đề \"Xác nhận khóa\"\n"
     "- Nội dung: \"Bạn có chắc muốn khóa ngân hàng 'Ngân hàng Thương mại cổ phần Đầu tư và Phát "
     "triển Việt Nam'?\"\n"
     "- Hai nút: Khóa và Hủy"),

    (2, "Khóa ngân hàng", "P0",
     "Ngân hàng QA02 đang Hoạt động",
     "1. Bấm Khóa ở dòng QA02\n2. Bấm nút Khóa trong hộp xác nhận",
     "Ngân hàng: QA02",
     "- Báo \"Khoá thành công\"\n- Dòng QA02 chuyển nhãn Khóa (nền đỏ)\n"
     "- Cột Hành động của dòng đó chỉ còn Mở khóa, Chi nhánh, Lịch sử"),

    (3, "Hủy thao tác Khóa", "P0",
     "Ngân hàng QA01 đang Hoạt động",
     "1. Bấm Khóa ở dòng QA01\n2. Bấm nút Hủy",
     "—",
     "- Hộp thoại đóng\n- QA01 vẫn ở trạng thái Hoạt động\n- Không có thông báo nào"),

    (4, "Mở khóa ngân hàng", "P0",
     "Ngân hàng QA02 đang Khóa",
     "1. Bấm nút Mở khóa ở dòng QA02\n2. Bấm nút Mở khóa trong hộp xác nhận",
     "Ngân hàng: QA02",
     "- Hộp thoại tiêu đề \"Xác nhận mở khóa\"\n- Báo \"Mở khoá thành công\"\n"
     "- Dòng QA02 trở lại nhãn Hoạt động, có lại nút Sửa"),

    (5, "Khóa ngân hàng đang được sử dụng", "P0",
     "Ngân hàng VIETCOMBANK đang được dùng ở hồ sơ nhân sự (không có nút Xóa)",
     "1. Bấm Khóa ở dòng VIETCOMBANK\n2. Xác nhận Khóa\n3. Mở khóa lại để trả môi trường về ban đầu",
     "Ngân hàng: VIETCOMBANK",
     "- Khóa thành công — ⚠️ Khóa KHÔNG bị chặn dù ngân hàng đang được sử dụng, khác với Xóa\n"
     "- Trạng thái đổi đúng và mở khóa lại được"),

    (6, "Ngân hàng đang Khóa vẫn chọn được ở màn khác hay không", "P1",
     "Ngân hàng QA02 đang ở trạng thái Khóa",
     "1. Khóa ngân hàng QA02\n2. Vào hồ sơ nhân sự, mở ô chọn Ngân hàng ở phần tài khoản ngân hàng\n"
     "3. Tìm QA02 trong danh sách chọn",
     "Ngân hàng: QA02",
     "- Ghi nhận kết quả thực tế: ngân hàng đang Khóa có còn xuất hiện trong ô chọn hay không\n"
     "- ⚠️ Nghiệp vụ mong đợi ngân hàng đã khóa không được chọn mới; nếu vẫn chọn được thì báo lại"),

    (7, "Trạng thái sau khi tải lại trang", "P1",
     "Vừa khóa ngân hàng QA02",
     "1. Khóa QA02\n2. Nhấn F5 tải lại trang\n3. Tìm lại dòng QA02",
     "—",
     "- Sau khi tải lại, QA02 vẫn ở trạng thái Khóa (đã lưu thật, không chỉ đổi trên màn hình)"),

    (8, "Khóa rồi lọc theo trạng thái", "P1",
     "Vừa khóa QA02",
     "1. Chọn Trạng thái = Khóa\n2. Bấm Tìm kiếm",
     "Trạng thái: Khóa",
     "- QA02 nằm trong kết quả lọc"),

    (9, "Lịch sử ghi nhận thao tác Khóa", "P0",
     "Vừa khóa ngân hàng QA02",
     "1. Mở menu ba chấm của dòng QA02\n2. Bấm Lịch sử",
     "—",
     "- Mốc mới nhất là \"Khóa\"\n- Dòng chi tiết: Trạng thái: Hoạt động → Khóa\n"
     "- Ghi đúng tên người thực hiện và thời điểm"),

    (10, "Lịch sử ghi nhận thao tác Mở khóa", "P0",
     "Vừa mở khóa ngân hàng QA02",
     "1. Mở popup Lịch sử của QA02",
     "—",
     "- Mốc mới nhất là \"Mở khóa\", chi tiết: Trạng thái: Khóa → Hoạt động"),
]

S6 = [
    (1, "Mở hộp xác nhận Xóa", "P0",
     "Ngân hàng QA03 chưa được dùng ở đâu",
     "1. Bấm nút Xóa (thùng rác) ở dòng QA03",
     "—",
     "- Hộp thoại tiêu đề \"Xác nhận xóa\"\n"
     "- Nội dung: \"Bạn có chắc muốn xóa ngân hàng 'Ngân hàng kiểm thử QA03'?\"\n"
     "- Hai nút: Xóa và Hủy"),

    (2, "Xóa ngân hàng chưa được sử dụng", "P0",
     "Ngân hàng QA03 chưa gắn với hồ sơ nhân sự và chưa có tài khoản ngân hàng công ty",
     "1. Bấm Xóa ở dòng QA03\n2. Bấm nút Xóa trong hộp xác nhận",
     "Ngân hàng: QA03",
     "- Báo \"Xoá ngân hàng thành công\"\n- Dòng QA03 biến mất khỏi danh sách\n"
     "- Tổng số bản ghi ở dòng thống kê giảm đi 1"),

    (3, "Hủy thao tác Xóa", "P0",
     "Ngân hàng QA04 đang hiển thị trong danh sách",
     "1. Bấm Xóa ở dòng QA04\n2. Bấm nút Hủy",
     "—",
     "- Hộp thoại đóng, QA04 còn nguyên trong danh sách"),

    (4, "Xóa kéo theo chi nhánh của ngân hàng", "P0",
     "Ngân hàng QA04 đã có 2 chi nhánh do QA tự tạo",
     "1. Thêm 2 chi nhánh cho QA04\n2. Xóa ngân hàng QA04\n3. Tạo lại ngân hàng mã QA04 rồi mở "
     "cửa sổ Chi nhánh",
     "Chi nhánh: CN Kiểm thử 1, CN Kiểm thử 2",
     "- Ngân hàng bị xóa cùng toàn bộ chi nhánh\n"
     "- Ngân hàng mới tạo lại có danh sách chi nhánh rỗng, không sót chi nhánh cũ"),

    (5, "Không có nút Xóa với ngân hàng đang được dùng ở hồ sơ nhân sự", "P0",
     "Ngân hàng VIETCOMBANK đang được chọn ở tài khoản ngân hàng của ít nhất 1 nhân viên đang làm việc",
     "1. Quan sát cột Hành động của dòng VIETCOMBANK",
     "—",
     "- Không hiển thị nút Xóa\n- ⚠️ Nút bị ẩn hẳn chứ không hiện rồi làm mờ"),

    (6, "Không có nút Xóa với ngân hàng đang dùng ở danh mục tài khoản ngân hàng công ty", "P0",
     "Ngân hàng BIDV đang được chọn trong Danh mục tài khoản ngân hàng của công ty",
     "1. Quan sát cột Hành động của dòng BIDV",
     "—",
     "- Không hiển thị nút Xóa\n"
     "- ⚠️ Điều kiện chặn xóa gồm cả hồ sơ nhân sự lẫn tài khoản ngân hàng của công ty"),

    (7, "Nút Xóa xuất hiện lại sau khi gỡ liên kết", "P1",
     "Ngân hàng QA04 đang được gán cho 1 nhân viên",
     "1. Vào hồ sơ nhân viên đó, đổi sang ngân hàng khác và lưu\n2. Quay lại màn Danh mục ngân hàng, "
     "bấm Làm mới\n3. Quan sát dòng QA04",
     "—",
     "- Nút Xóa hiện trở lại ở dòng QA04"),

    (8, "Xóa ngân hàng đang Khóa", "P1",
     "Ngân hàng QA04 đang ở trạng thái Khóa",
     "1. Quan sát cột Hành động của dòng QA04",
     "—",
     "- Không có nút Xóa (ngân hàng đang Khóa thì ẩn cả Sửa lẫn Xóa)\n"
     "- Muốn xóa phải Mở khóa trước"),

    (9, "Xóa ở trang cuối chỉ còn 1 dòng", "P2",
     "Trang 3 chỉ còn đúng 1 ngân hàng và đó là bản ghi xóa được",
     "1. Sang trang cuối\n2. Xóa dòng duy nhất",
     "—",
     "- Danh sách tự lùi về trang trước, không hiển thị trang trắng\n- Dòng thống kê cập nhật đúng"),
]

S7 = [
    (1, "Mở cửa sổ Chi nhánh từ menu ba chấm", "P0",
     "Ngân hàng BIDV có 23 chi nhánh",
     "1. Mở menu ba chấm dòng BIDV\n2. Bấm Chi nhánh",
     "Ngân hàng: BIDV",
     "- Mở cửa sổ tiêu đề \"Chi nhánh ngân hàng\"\n"
     "- Bảng gồm 4 cột: STT, Tên chi nhánh, Tỉnh/TP, Hành động\n"
     "- Có ô lọc Tỉnh/Thành phố, ô Tên chi nhánh, nút Tìm kiếm, nút Làm mới, nút Tạo mới"),

    (2, "Mở cửa sổ Chi nhánh bằng cách bấm số ở cột Chi nhánh", "P1",
     "Đã bật cột Chi nhánh; dòng BIDV hiện số 23",
     "1. Bật cột Chi nhánh\n2. Bấm vào số 23 ở dòng BIDV",
     "—",
     "- Mở đúng cửa sổ Chi nhánh của BIDV, không điều hướng sang trang khác"),

    (3, "Đối chiếu số chi nhánh với danh sách trong cửa sổ", "P0",
     "Dòng BIDV hiện số 23 ở cột Chi nhánh",
     "1. Ghi lại số ở cột Chi nhánh\n2. Mở cửa sổ Chi nhánh và đếm số dòng thực tế",
     "—",
     "- Mong đợi hai con số bằng nhau\n"
     "- ⚠️ Nếu lệch, kiểm tra xem có chi nhánh nào chưa gán Tỉnh/Thành phố không — chi nhánh loại "
     "này được đếm nhưng không hiện trong cửa sổ"),

    (4, "Ngân hàng chưa có chi nhánh", "P1",
     "Ngân hàng NHB chưa có chi nhánh nào",
     "1. Mở cửa sổ Chi nhánh của NHB",
     "Ngân hàng: NHB",
     "- Bảng hiện dòng \"Chưa có dữ liệu\"\n- Nút Tạo mới vẫn dùng được"),

    (5, "Lọc chi nhánh theo Tỉnh/Thành phố", "P0",
     "BIDV có nhiều chi nhánh ở Thành phố Hà Nội và một số tỉnh khác",
     "1. Mở cửa sổ Chi nhánh của BIDV\n2. Chọn Tỉnh/Thành phố = Thành phố Hà Nội\n3. Bấm Tìm kiếm",
     "Tỉnh/Thành phố: Thành phố Hà Nội",
     "- Mọi dòng kết quả đều có cột Tỉnh/TP là Thành phố Hà Nội"),

    (6, "Lọc chi nhánh theo tên", "P0",
     "BIDV có chi nhánh \"CN Tràng Tiền\"",
     "1. Nhập Tràng vào ô Tên chi nhánh\n2. Bấm Tìm kiếm",
     "Tên chi nhánh: Tràng",
     "- Kết quả chỉ gồm chi nhánh có tên chứa chữ Tràng"),

    (7, "Kết hợp 2 điều kiện lọc chi nhánh", "P1",
     "BIDV có chi nhánh CN Hoàng Mai ở Thành phố Hà Nội",
     "1. Chọn Tỉnh/Thành phố = Thành phố Hà Nội\n2. Nhập Tên chi nhánh = CN\n3. Bấm Tìm kiếm",
     "Tỉnh/Thành phố: Thành phố Hà Nội | Tên chi nhánh: CN",
     "- Kết quả thoả đồng thời cả hai điều kiện"),

    (8, "Làm mới bộ lọc chi nhánh", "P1",
     "Đang lọc chi nhánh theo tên",
     "1. Bấm nút Làm mới trong cửa sổ Chi nhánh",
     "—",
     "- Hai ô lọc trở về trống\n- Danh sách hiện lại toàn bộ chi nhánh của ngân hàng đó"),

    (9, "Mở cửa sổ Thêm chi nhánh", "P0",
     "Đang mở cửa sổ Chi nhánh của BIDV",
     "1. Bấm nút Tạo mới trong cửa sổ Chi nhánh",
     "—",
     "- Cửa sổ tiêu đề \"Thêm chi nhánh ngân hàng\"\n"
     "- Hai ô: Tên chi nhánh ngân hàng (dấu sao đỏ), Tỉnh/Thành phố (dấu sao đỏ), cả hai đang trống\n"
     "- Ba nút: Lưu, Lưu và tiếp tục, Đóng"),

    (10, "Thêm chi nhánh hợp lệ", "P0",
     "Ngân hàng QA04 chưa có chi nhánh tên CN Kiểm thử 1",
     "1. Mở cửa sổ Chi nhánh của QA04\n2. Bấm Tạo mới\n3. Nhập tên và chọn tỉnh\n4. Bấm Lưu",
     "Tên chi nhánh: CN Kiểm thử 1 | Tỉnh/Thành phố: Thành phố Hà Nội",
     "- Báo \"Đã lưu thành công!\"\n- Cửa sổ thêm đóng, danh sách chi nhánh có thêm dòng mới\n"
     "- Số ở cột Chi nhánh ngoài danh sách tăng thêm 1"),

    (11, "Thêm chi nhánh bỏ trống cả hai ô", "P0",
     "Cửa sổ Thêm chi nhánh đang mở",
     "1. Không nhập gì\n2. Bấm Lưu",
     "—",
     "- Lỗi đỏ \"Bắt buộc phải nhập\" hiện dưới CẢ hai ô\n"
     "- Hệ thống báo \"Vui lòng kiểm tra lại thông tin\"\n- Cửa sổ không đóng"),

    (12, "Thêm chi nhánh thiếu Tỉnh/Thành phố", "P0",
     "Cửa sổ Thêm chi nhánh đang mở",
     "1. Chỉ nhập Tên chi nhánh\n2. Bấm Lưu",
     "Tên chi nhánh: CN Thiếu tỉnh",
     "- Lỗi đỏ \"Bắt buộc phải nhập\" dưới ô Tỉnh/Thành phố\n- Không tạo được chi nhánh"),

    (13, "Trùng tên chi nhánh trong cùng ngân hàng", "P0",
     "Ngân hàng QA04 đã có chi nhánh CN Kiểm thử 1",
     "1. Bấm Tạo mới\n2. Nhập đúng tên đã có, chọn tỉnh bất kỳ\n3. Bấm Lưu",
     "Tên chi nhánh: CN Kiểm thử 1 | Tỉnh/Thành phố: Tỉnh Ninh Bình",
     "- Lỗi đỏ \"Tên chi nhánh ngân hàng này đã tồn tại\" dưới ô Tên chi nhánh\n- Không tạo bản ghi mới"),

    (14, "Trùng tên chi nhánh nhưng khác ngân hàng", "P0",
     "Ngân hàng QA04 đã có CN Kiểm thử 1; ngân hàng QA01 chưa có chi nhánh nào",
     "1. Mở cửa sổ Chi nhánh của QA01\n2. Thêm chi nhánh tên CN Kiểm thử 1\n3. Bấm Lưu",
     "Tên chi nhánh: CN Kiểm thử 1 | Tỉnh/Thành phố: Thành phố Hà Nội",
     "- Lưu thành công\n- ⚠️ Tên chi nhánh chỉ cần duy nhất trong phạm vi một ngân hàng"),

    (15, "Lưu và tiếp tục ở cửa sổ chi nhánh", "P1",
     "Đang mở cửa sổ Thêm chi nhánh của QA04",
     "1. Nhập CN Kiểm thử 2, chọn tỉnh\n2. Bấm Lưu và tiếp tục\n3. Nhập tiếp CN Kiểm thử 3 rồi bấm Lưu",
     "Lần 1: CN Kiểm thử 2 | Lần 2: CN Kiểm thử 3",
     "- Sau lần 1: cửa sổ vẫn mở, hai ô trở về trống\n- Cuối cùng danh sách có đủ cả hai chi nhánh mới"),

    (16, "Sửa chi nhánh", "P0",
     "Chi nhánh CN Kiểm thử 2 của QA04 đang thuộc Thành phố Hà Nội",
     "1. Bấm nút Sửa (bút chì) ở dòng CN Kiểm thử 2\n2. Đổi tên và đổi tỉnh\n3. Bấm Lưu",
     "Tên chi nhánh: CN Kiểm thử 2 - đã sửa | Tỉnh/Thành phố: Tỉnh Sơn La",
     "- Cửa sổ tiêu đề \"Sửa chi nhánh ngân hàng\", điền sẵn dữ liệu cũ\n"
     "- Lưu xong danh sách hiện tên mới và tỉnh mới\n"
     "- Cửa sổ Sửa chỉ có 2 nút Lưu và Đóng"),

    (17, "Sửa chi nhánh thành tên đã tồn tại", "P0",
     "QA04 có CN Kiểm thử 1 và CN Kiểm thử 3",
     "1. Bấm Sửa dòng CN Kiểm thử 3\n2. Đổi tên thành CN Kiểm thử 1\n3. Bấm Lưu",
     "Tên chi nhánh: CN Kiểm thử 1",
     "- Lỗi đỏ \"Tên chi nhánh ngân hàng này đã tồn tại\"\n- Không lưu"),

    (18, "Sửa chi nhánh giữ nguyên tên của chính nó", "P1",
     "Đang sửa CN Kiểm thử 1 của QA04",
     "1. Bấm Sửa dòng CN Kiểm thử 1\n2. Giữ nguyên tên, chỉ đổi Tỉnh/Thành phố\n3. Bấm Lưu",
     "Tỉnh/Thành phố: Tỉnh Ninh Bình",
     "- Lưu thành công, không báo trùng tên với chính nó"),

    (19, "Xóa chi nhánh chưa được sử dụng", "P0",
     "Chi nhánh CN Kiểm thử 3 của QA04 chưa gắn với hồ sơ nhân sự nào",
     "1. Bấm nút Xóa (thùng rác) ở dòng đó\n2. Bấm Xóa trong hộp xác nhận",
     "Chi nhánh: CN Kiểm thử 3",
     "- Hộp thoại \"Xác nhận xóa\" ghi đúng tên chi nhánh\n- Báo \"Xoá chi nhánh ngân hàng thành công\"\n"
     "- Dòng biến mất, số ở cột Chi nhánh ngoài danh sách giảm 1"),

    (20, "Hủy thao tác xóa chi nhánh", "P1",
     "Chi nhánh CN Kiểm thử 1 đang hiển thị",
     "1. Bấm Xóa ở dòng đó\n2. Bấm Hủy",
     "—",
     "- Chi nhánh vẫn còn trong danh sách"),

    (21, "Chi nhánh đang được sử dụng thì không xóa được", "P0",
     "Chi nhánh CN Nam Hà Nội của BIDV đang được chọn ở tài khoản ngân hàng của nhân viên",
     "1. Mở cửa sổ Chi nhánh của BIDV\n2. Rê chuột vào nút Xóa của dòng CN Nam Hà Nội\n3. Thử bấm",
     "Chi nhánh: CN Nam Hà Nội",
     "- Nút Xóa bị làm mờ, không bấm được\n"
     "- Rê chuột hiện chú thích \"Không thể xóa bản ghi, chi nhánh đang được sử dụng trên hệ thống\"\n"
     "- ⚠️ Ở đây nút bị LÀM MỜ, khác với ngoài danh sách ngân hàng (ẩn hẳn)"),

    (22, "Gọi thẳng chức năng xóa chi nhánh đang được sử dụng", "P0",
     "Chi nhánh CN Nam Hà Nội đang được sử dụng, nút Xóa đang bị làm mờ",
     "1. Ghi lại định danh chi nhánh\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa chi nhánh, "
     "bỏ qua giao diện\n3. Mở lại cửa sổ Chi nhánh của BIDV",
     "Chi nhánh: CN Nam Hà Nội",
     "- Ghi nhận kết quả thực tế: chi nhánh có bị xóa hay không\n"
     "- ⚠️ Nếu chi nhánh BỊ XÓA thật thì đây là lỗ hổng nghiêm trọng (hồ sơ nhân sự mất chi nhánh "
     "đang tham chiếu) — phải báo ngay, không đánh Passed"),

    (23, "Chi nhánh mở từ ngân hàng khác không lẫn dữ liệu", "P0",
     "BIDV có 23 chi nhánh, VIETCOMBANK có 15 chi nhánh",
     "1. Mở cửa sổ Chi nhánh của BIDV, ghi lại vài tên\n2. Đóng cửa sổ\n3. Mở cửa sổ Chi nhánh của "
     "VIETCOMBANK",
     "—",
     "- Danh sách lần 2 là chi nhánh của VIETCOMBANK\n"
     "- ⚠️ Không được hiện lại danh sách của BIDV"),

    (24, "Đóng cửa sổ chi nhánh", "P2",
     "Cửa sổ Chi nhánh đang mở",
     "1. Bấm nút Đóng",
     "—",
     "- Cửa sổ đóng, quay lại danh sách ngân hàng\n- Con số ở cột Chi nhánh đã cập nhật theo thao tác vừa làm"),

    (25, "Tỉnh/Thành phố hiển thị đúng tên", "P1",
     "BIDV có chi nhánh ở nhiều tỉnh",
     "1. Mở cửa sổ Chi nhánh của BIDV\n2. Quan sát cột Tỉnh/TP",
     "—",
     "- Hiện tên tỉnh/thành phố đầy đủ (ví dụ \"Thành phố Hà Nội\", \"Tỉnh Sơn La\")\n"
     "- Không hiện giá trị số"),
]

S8 = [
    (1, "Nhập tên ngân hàng dài quá giới hạn", "P1",
     "Cửa sổ Tạo ngân hàng đang mở",
     "1. Nhập Tên ngân hàng 300 ký tự\n2. Nhập Mã và Tên viết tắt hợp lệ\n3. Bấm Lưu",
     "Tên ngân hàng: chuỗi 300 ký tự",
     "- Hệ thống không lưu chuỗi bị cắt cụt một cách âm thầm\n"
     "- Hoặc chặn bằng thông báo lỗi, hoặc lưu đủ và hiển thị lại đúng chuỗi đã nhập"),

    (2, "Nhập mã ngân hàng dài quá giới hạn", "P1",
     "Cửa sổ Tạo ngân hàng đang mở",
     "1. Nhập Mã ngân hàng 300 ký tự\n2. Nhập các ô bắt buộc còn lại\n3. Bấm Lưu",
     "Mã ngân hàng: chuỗi 300 ký tự",
     "- Không được lưu sai lệch âm thầm; nếu chặn thì phải có thông báo đọc hiểu được"),

    (3, "Nhập khoảng trắng đầu cuối", "P1",
     "Cửa sổ Tạo ngân hàng đang mở",
     "1. Nhập Tên ngân hàng có khoảng trắng ở đầu và cuối\n2. Bấm Lưu\n3. Mở lại cửa sổ Sửa",
     "Tên ngân hàng: \"  Ngân hàng kiểm thử khoảng trắng  \"",
     "- Ghi nhận kết quả thực tế: chuỗi được cắt khoảng trắng hay giữ nguyên\n"
     "- Danh sách hiển thị tên không bị thụt lề bất thường"),

    (4, "Nhập chỉ toàn khoảng trắng vào ô bắt buộc", "P0",
     "Cửa sổ Tạo ngân hàng đang mở",
     "1. Nhập 3 dấu cách vào ô Tên ngân hàng\n2. Nhập Mã và Tên viết tắt hợp lệ\n3. Bấm Lưu",
     "Tên ngân hàng: (3 dấu cách)",
     "- Mong đợi: hệ thống coi là chưa nhập và báo lỗi bắt buộc\n"
     "- ⚠️ Nếu lưu được ngân hàng tên rỗng thì báo lại — danh mục sẽ có dòng trắng không sửa được theo tên"),

    (5, "Nhập ký tự đặc biệt vào tên ngân hàng", "P1",
     "Cửa sổ Tạo ngân hàng đang mở",
     "1. Nhập tên có ký tự đặc biệt\n2. Nhập các ô bắt buộc còn lại\n3. Bấm Lưu\n4. Quan sát danh sách",
     "Tên ngân hàng: Ngân hàng <b>QA</b> & Co.",
     "- Danh sách hiển thị đúng nguyên văn chuỗi đã nhập\n"
     "- ⚠️ Không được biến thành chữ in đậm hay làm vỡ bố cục bảng"),

    (6, "Nhập tiếng Việt có dấu và tiếng nước ngoài", "P1",
     "Danh mục đã có ngân hàng tên 한국은행",
     "1. Tạo ngân hàng tên có dấu tiếng Việt đầy đủ\n2. Lưu và quan sát danh sách",
     "Tên ngân hàng: Ngân hàng Đầu tư & Phát triển Đông Á",
     "- Hiển thị đủ dấu, không bị lỗi phông chữ\n- Tìm nhanh theo chuỗi có dấu vẫn ra kết quả"),

    (7, "Dán nội dung từ nguồn khác vào ô nhập", "P2",
     "Đã sao chép một đoạn văn bản có định dạng từ tài liệu Word",
     "1. Dán vào ô Tên ngân hàng\n2. Bấm Lưu",
     "Nội dung dán: đoạn text có định dạng",
     "- Chỉ phần chữ được nhận, không kèm định dạng\n- Không làm hỏng cửa sổ nhập liệu"),

    (8, "Nhập số vào ô Tên viết tắt", "P2",
     "Cửa sổ Tạo ngân hàng đang mở",
     "1. Nhập Tên viết tắt gồm cả chữ và số\n2. Lưu",
     "Tên viết tắt: QA123",
     "- Lưu bình thường, ô Tên viết tắt không giới hạn chỉ chữ cái"),

    (9, "Bấm Lưu nhiều lần liên tiếp", "P0",
     "Cửa sổ Tạo ngân hàng đã nhập đủ 3 ô bắt buộc",
     "1. Nhập đủ dữ liệu hợp lệ\n2. Bấm nút Lưu 3 lần thật nhanh\n3. Đếm số bản ghi trong danh sách",
     "Mã ngân hàng: QA10",
     "- Chỉ tạo ra ĐÚNG 1 ngân hàng QA10\n- Nút Lưu bị vô hiệu hoá trong lúc đang xử lý"),

    (10, "Nhập tên chi nhánh dài", "P2",
     "Cửa sổ Thêm chi nhánh đang mở",
     "1. Nhập tên chi nhánh 300 ký tự\n2. Chọn tỉnh\n3. Bấm Lưu",
     "Tên chi nhánh: chuỗi 300 ký tự",
     "- Không lưu sai lệch âm thầm; danh sách chi nhánh vẫn hiển thị được, ô tự xuống dòng"),
]

S9 = [
    (1, "Hai người cùng sửa một ngân hàng", "P0",
     "Người A và người B cùng mở cửa sổ Sửa của ngân hàng QA01",
     "1. Người A đổi Tên ngân hàng rồi bấm Lưu\n2. Người B (đang mở dữ liệu cũ) đổi Địa chỉ giao dịch "
     "rồi bấm Lưu\n3. Cả hai bấm Làm mới",
     "A: đổi tên | B: đổi địa chỉ",
     "- Ghi nhận kết quả thực tế: bản lưu sau ghi đè bản lưu trước hay hệ thống cảnh báo\n"
     "- ⚠️ Kiểm popup Lịch sử: phải có đủ 2 mốc thay đổi của 2 người"),

    (2, "Xóa ngân hàng trong khi người khác đang mở cửa sổ Sửa", "P0",
     "Người A đang mở cửa sổ Sửa ngân hàng QA04; người B ở màn danh sách",
     "1. Người B xóa ngân hàng QA04\n2. Người A bấm Lưu",
     "—",
     "- Người A nhận thông báo lỗi đọc hiểu được, màn hình không treo\n"
     "- Ngân hàng không được tạo lại từ thao tác Lưu của người A"),

    (3, "Khóa ngân hàng trong khi người khác đang mở cửa sổ Sửa", "P1",
     "Người A đang mở cửa sổ Sửa ngân hàng QA01",
     "1. Người B khóa ngân hàng QA01\n2. Người A bấm Lưu\n3. Người A bấm Làm mới",
     "—",
     "- Ghi nhận kết quả thực tế của thao tác Lưu\n"
     "- Sau khi làm mới, dòng QA01 hiển thị đúng trạng thái Khóa và không còn nút Sửa"),

    (4, "Thêm chi nhánh trong khi người khác xóa ngân hàng mẹ", "P1",
     "Người A đang mở cửa sổ Thêm chi nhánh của QA04",
     "1. Người B xóa ngân hàng QA04\n2. Người A bấm Lưu chi nhánh",
     "Tên chi nhánh: CN Đồng thời",
     "- Người A nhận thông báo lỗi, không tạo ra chi nhánh mồ côi\n"
     "- ⚠️ Kiểm lại: không được xuất hiện chi nhánh không thuộc ngân hàng nào"),

    (5, "Hai người cùng thêm chi nhánh trùng tên", "P1",
     "Người A và người B cùng mở cửa sổ Thêm chi nhánh của QA01",
     "1. Cả hai nhập cùng tên chi nhánh\n2. Cùng bấm Lưu gần như đồng thời",
     "Tên chi nhánh: CN Đua nhau",
     "- Chỉ một người lưu thành công, người còn lại nhận lỗi trùng tên\n"
     "- Danh sách chỉ có 1 chi nhánh tên CN Đua nhau"),

    (6, "Danh sách tự làm mới sau thao tác ghi", "P0",
     "Đang ở trang 1 với bộ lọc rỗng",
     "1. Tạo mới một ngân hàng\n2. Không tải lại trang, quan sát danh sách",
     "Mã ngân hàng: QA11",
     "- Danh sách tự cập nhật, hiện ngay ngân hàng vừa tạo\n- Dòng thống kê tăng đúng 1"),

    (7, "Thao tác ghi khi mất kết nối", "P2",
     "Cửa sổ Tạo ngân hàng đã nhập đủ dữ liệu hợp lệ",
     "1. Ngắt kết nối mạng\n2. Bấm Lưu\n3. Nối lại mạng và bấm Lưu",
     "Mã ngân hàng: QA12",
     "- Lần 1: hệ thống báo lỗi, cửa sổ không đóng, dữ liệu đã nhập còn nguyên\n"
     "- Lần 2: lưu thành công, chỉ tạo ra 1 bản ghi"),
]

S10 = [
    (1, "Mở popup Lịch sử từ danh sách", "P0",
     "Ngân hàng test01 đã từng bị khóa rồi mở khóa",
     "1. Mở menu ba chấm dòng test01\n2. Bấm Lịch sử",
     "—",
     "- Popup tiêu đề \"Lịch sử thay đổi\", dòng phụ ghi \"Ngân hàng: test01 - trang\"\n"
     "- Các mốc xếp mới nhất trước\n- Có nút Bộ lọc và nút Đóng"),

    (2, "Nội dung một mốc lịch sử", "P0",
     "Ngân hàng test01 vừa được mở khóa",
     "1. Mở popup Lịch sử của test01\n2. Đọc mốc trên cùng",
     "—",
     "- Hiện ngày giờ, nhãn hành động (\"Mở khóa\"), tên người thực hiện kèm phòng ban\n"
     "- Dòng chi tiết: Trạng thái: Khóa → Hoạt động"),

    (3, "Lọc lịch sử theo loại hoạt động", "P1",
     "Ngân hàng có cả mốc Tạo mới, Thay đổi thông tin và Thay đổi trạng thái",
     "1. Mở popup Lịch sử\n2. Bấm nút Bộ lọc\n3. Chọn loại hoạt động \"Thay đổi trạng thái\"",
     "Loại hoạt động: Thay đổi trạng thái",
     "- Chỉ còn các mốc Khóa / Mở khóa\n"
     "- Danh sách loại hoạt động có đúng 3 nhóm: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái"),

    (4, "Lịch sử của ngân hàng chưa từng thay đổi", "P1",
     "Ngân hàng VIETCOMBANK chưa phát sinh thao tác nào từ khi có chức năng lịch sử",
     "1. Bấm mã VIETCOMBANK để mở cửa sổ Xem\n2. Bấm nút Xem lịch sử",
     "—",
     "- Khối lịch sử hiện \"Chưa có lịch sử thao tác nào.\"\n- Không báo lỗi"),

    (5, "Khối lịch sử trong cửa sổ Xem", "P0",
     "Ngân hàng test01 đã có lịch sử",
     "1. Bấm mã test01\n2. Bấm nút Xem lịch sử ở cuối cửa sổ",
     "—",
     "- Khối Lịch sử mở ra ngay trong cửa sổ Xem\n"
     "- Nội dung giống hệt popup Lịch sử mở từ menu ba chấm\n- Có nút Làm mới và nút Thu gọn"),

    (6, "Lịch sử ghi nhận việc tạo mới", "P0",
     "Vừa tạo ngân hàng QA13",
     "1. Tạo ngân hàng QA13\n2. Mở popup Lịch sử của QA13",
     "Mã ngân hàng: QA13",
     "- Có đúng 1 mốc \"Tạo mới\" với người thực hiện là người vừa tạo"),

    (7, "Lịch sử ghi nhận từng trường thay đổi", "P0",
     "Ngân hàng QA13 vừa được đổi Tên viết tắt và Địa chỉ giao dịch",
     "1. Sửa 2 ô trên rồi Lưu\n2. Mở popup Lịch sử",
     "Tên viết tắt: QA13B | Địa chỉ giao dịch: 99 Trần Duy Hưng",
     "- Mốc \"Thay đổi thông tin\" liệt kê cả hai trường với giá trị cũ → giá trị mới\n"
     "- Nhãn trường là tiếng Việt (Tên viết tắt, Địa chỉ giao dịch)"),

    (8, "Lịch sử không ghi thao tác trên chi nhánh", "P1",
     "Vừa thêm và xoá một chi nhánh của QA13",
     "1. Thêm chi nhánh CN Log rồi xoá luôn\n2. Mở popup Lịch sử của QA13",
     "—",
     "- Popup KHÔNG phát sinh mốc nào cho thao tác chi nhánh\n"
     "- ⚠️ Đây là hiện trạng đã biết: lịch sử chỉ theo dõi thông tin của chính ngân hàng"),

    (9, "Luồng đầy đủ: tạo → sửa → khóa → mở khóa → xóa", "P0",
     "Danh mục chưa có mã QA20",
     "1. Tạo ngân hàng QA20 với đủ 3 ô bắt buộc\n2. Sửa Tên giao dịch quốc tế\n3. Khóa QA20\n"
     "4. Mở khóa QA20\n5. Mở popup Lịch sử và đối chiếu\n6. Xóa QA20",
     "Mã ngân hàng: QA20 | Tên ngân hàng: Ngân hàng kiểm thử luồng | Tên viết tắt: QA20",
     "- Mỗi bước có thông báo thành công tương ứng và danh sách cập nhật ngay\n"
     "- Popup Lịch sử có đủ 4 mốc theo đúng thứ tự: Tạo mới, Thay đổi thông tin, Khóa, Mở khóa\n"
     "- Sau bước 6, QA20 biến mất khỏi danh sách"),

    (10, "Luồng đầy đủ với chi nhánh", "P0",
     "Danh mục chưa có mã QA21",
     "1. Tạo ngân hàng QA21\n2. Mở cửa sổ Chi nhánh, thêm 3 chi nhánh\n3. Sửa 1 chi nhánh\n"
     "4. Xoá 1 chi nhánh\n5. Đóng cửa sổ và đối chiếu cột Chi nhánh\n6. Xóa ngân hàng QA21",
     "Chi nhánh: CN A, CN B, CN C",
     "- Sau bước 4, cửa sổ còn 2 chi nhánh\n- Cột Chi nhánh ngoài danh sách hiện số 2\n"
     "- Sau bước 6, ngân hàng và toàn bộ chi nhánh bị xoá theo"),

    (11, "Dữ liệu vừa tạo dùng được ngay ở hồ sơ nhân sự", "P0",
     "Vừa tạo ngân hàng QA22 kèm chi nhánh CN QA22",
     "1. Tạo ngân hàng QA22 và 1 chi nhánh\n2. Vào hồ sơ một nhân viên, mở phần tài khoản ngân hàng\n"
     "3. Mở ô chọn Ngân hàng, tìm QA22\n4. Chọn QA22 rồi mở ô chọn Chi nhánh",
     "Ngân hàng: QA22 | Chi nhánh: CN QA22",
     "- QA22 có trong ô chọn Ngân hàng\n"
     "- Ô chọn Chi nhánh chỉ liệt kê chi nhánh của QA22, không lẫn chi nhánh ngân hàng khác"),

    (12, "Dọn dữ liệu sau khi test", "P1",
     "Đã tạo các ngân hàng QA01 … QA22 trong quá trình test",
     "1. Lọc theo từ khoá QA\n2. Xóa lần lượt toàn bộ ngân hàng kiểm thử\n3. Bấm Làm mới và đối "
     "chiếu tổng số",
     "Từ khoá: QA",
     "- Danh mục trở về đúng 26 ngân hàng như trước khi test\n"
     "- ⚠️ Ngân hàng nào không xoá được (đã bị gán vào hồ sơ) thì gỡ liên kết trước rồi xoá"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "TẠO MỚI / SỬA / XEM NGÂN HÀNG", S4),
    ("V", "KHÓA / MỞ KHÓA", S5),
    ("VI", "XÓA NGÂN HÀNG", S6),
    ("VII", "QUẢN LÝ CHI NHÁNH NGÂN HÀNG", S7),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", S8),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S9),
    ("X", "LỊCH SỬ THAY ĐỔI & LUỒNG TỔNG THỂ", S10),
]

build(output_file=OUT,
      sheet_name="Trang tính1",
      feature_name="Danh mục ngân hàng - Cập nhật ngày 17/08/2026",
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
