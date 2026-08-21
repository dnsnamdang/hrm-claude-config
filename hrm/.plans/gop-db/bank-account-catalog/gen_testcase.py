# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man 'Danh muc tai khoan ngan hang' (/finance/account-banks).

Ban nay THAY THE `generate-testcase.py` (form cu 15 cot) — dung engine chung
`.claude/skills/testcase-documenter/assets/tc_engine.py` (form 17 cot, 2 khoi summary DNS/TP).

Nguon doi chieu (doc truc tiep tu code nhanh gop_db, 2026-08-17):
  BE  Modules/Finance/Routes/api.php (prefix /account-banks — 7 route, TAT CA gan
      checkPermission:'Quan ly danh muc tai khoan ngan hang'; route update con gan recordNotLocked)
      Modules/Finance/Http/Controllers/V1/CompanyAccountController.php
      Modules/Finance/Services/CompanyAccountService.php
      Modules/Finance/Entities/CompanyAccount/CompanyAccount.php
      Modules/Finance/Http/Requests/CompanyAccount/CompanyAccountRequest.php
      Modules/Finance/Transformers/CompanyAccountResource/*.php
      app/Services/CatalogHistoryService.php (bang `company_accounts`)
  FE  hrm-client/pages/finance/account-banks/{index.vue,AccountBankModal.vue}
      hrm-client/components/subsystem-menu/finance.js (menu Tai chinh -> Danh muc)

Chay:  python .plans/gop-db/bank-account-catalog/gen_testcase.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "DM tài khoản ngân hàng"

# ============================================================ 9 MUC MO TA
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý danh mục tài khoản ngân hàng CỦA CÔNG TY (không phải tài khoản cá nhân của nhân "
     "viên): số tài khoản, chủ tài khoản, ngân hàng, chi nhánh, loại tiền tệ và trạng thái sử "
     "dụng.\n"
     "Dữ liệu của màn này là nguồn cho các nghiệp vụ thu chi, đề nghị thanh toán và các chứng từ "
     "cần chọn tài khoản nhận / chuyển tiền của công ty.\n"
     "Người dùng làm được: xem danh sách, tìm kiếm, lọc, tạo mới, sửa, xem chi tiết, khóa / mở "
     "khóa và xem lịch sử thay đổi. Màn hình KHÔNG có chức năng Xóa, Xuất Excel, Nhập Excel, In."),

    ("2. Đối tượng được tính / hiển thị",
     "Danh sách chỉ hiển thị tài khoản ngân hàng THUỘC CÔNG TY của người đang đăng nhập:\n"
     "- Tài khoản trạng thái Hoạt động — nhãn xanh, có đủ nút Sửa / Khóa / Lịch sử.\n"
     "- Tài khoản trạng thái Khóa — nhãn đỏ, chỉ còn nút Mở khóa / Lịch sử (nút Sửa bị ẩn).\n"
     "- Tài khoản gắn ngân hàng đã bị khóa ở danh mục ngân hàng vẫn hiển thị bình thường, tên "
     "ngân hàng vẫn hiện đúng vì được lưu kèm ngay trên bản ghi.\n"
     "- Tài khoản chưa có loại tiền tệ (dữ liệu cũ) vẫn hiển thị, ô Loại tiền tệ hiện dấu gạch "
     "ngang."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Tài khoản ngân hàng của công ty KHÁC: không hiển thị, tìm kiếm cũng không ra, mở trực tiếp "
     "cũng báo không tìm thấy.\n"
     "- Người dùng chưa được gắn công ty trong hồ sơ nhân sự: danh sách trống hoàn toàn và không "
     "tạo mới được.\n"
     "- Nút Sửa bị ẩn hẳn (không phải làm mờ) khi tài khoản đang ở trạng thái Khóa.\n"
     "- Nút Tạo mới, Sửa, Khóa / Mở khóa bị ẩn khi tài khoản đăng nhập không có quyền quản lý.\n"
     "- Trong ô chọn Ngân hàng của cửa sổ Thêm/Sửa: ngân hàng đang bị khóa KHÔNG xuất hiện.\n"
     "- Trong ô chọn Loại tiền tệ: loại tiền tệ đang bị khóa KHÔNG xuất hiện."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng. Màn hình không có bộ lọc theo khoảng thời gian; hai cột Ngày tạo và Ngày cập "
     "nhật chỉ dùng để hiển thị và sắp xếp."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Mỗi tài khoản ngân hàng của công ty gắn với 3 danh mục khác:\n"
     "- Ngân hàng — lấy từ màn Danh mục ngân hàng (phân hệ Danh mục chung).\n"
     "- Chi nhánh — phải là chi nhánh THUỘC ĐÚNG ngân hàng đã chọn; đổi ngân hàng thì ô Chi nhánh "
     "tự xoá trắng.\n"
     "- Loại tiền tệ — lấy từ màn Danh mục tiền tệ (phân hệ Tài chính).\n"
     "Tên ngân hàng và tên chi nhánh được chép sẵn vào bản ghi tại thời điểm lưu, nên sau này danh "
     "mục ngân hàng đổi tên thì danh sách vẫn hiện tên cũ cho tới khi mở Sửa và lưu lại."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Số tài khoản là duy nhất trên toàn hệ thống, không phân biệt công ty: công ty khác đã dùng "
     "số tài khoản đó thì công ty mình không tạo trùng được (dù không nhìn thấy bản ghi kia).\n"
     "- Ô tìm nhanh quét đồng thời Số tài khoản, Chủ tài khoản và Ngân hàng; một bản ghi khớp "
     "nhiều trường vẫn chỉ hiện một dòng.\n"
     "- Không có phép cộng dồn nào khác trên màn hình."),

    ("7. Phân quyền cấp",
     "Màn hình dùng ĐÚNG MỘT quyền: \"Quản lý danh mục tài khoản ngân hàng\" (nhóm quyền Danh mục "
     "tài chính).\n"
     "- Có quyền: nhìn thấy mục menu, xem danh sách và làm được mọi thao tác (tạo mới, sửa, khóa, "
     "mở khóa, xem lịch sử).\n"
     "- Không có quyền: mục menu bị ẩn; gõ thẳng đường dẫn thì hệ thống từ chối, danh sách không "
     "tải được.\n"
     "Ngoài quyền trên, còn một lớp giới hạn nữa KHÔNG phụ thuộc quyền: người dùng chỉ thấy tài "
     "khoản của công ty mình (lấy theo công ty ghi trong hồ sơ nhân sự). Không có phân quyền theo "
     "phòng ban hay bộ phận."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a–b / N\" dưới bảng: a là số thứ tự dòng đầu trang đang xem, b là dòng cuối, "
     "N là tổng số tài khoản khớp bộ lọc TRONG CÔNG TY của người đăng nhập.\n"
     "- Ô \"Số dòng/trang\": chọn 5 / 10 / 20 / 50 / 100, mặc định 10; đổi số dòng thì quay về "
     "trang 1.\n"
     "- Cột STT đánh liên tục theo trang: trang 2 với 10 dòng/trang bắt đầu từ 11.\n"
     "- Danh sách mặc định xếp theo Ngày tạo mới nhất trước."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1. ⚠️ Chủ tài khoản và Ngân hàng được hệ thống TỰ CHUYỂN THÀNH CHỮ IN HOA khi lưu. Nhập "
     "chữ thường vẫn đúng, đừng ghi Failed; nhưng phải kiểm tra đúng là in hoa sau khi lưu.\n"
     "2. ⚠️ Số tài khoản trùng bị chặn trên TOÀN HỆ THỐNG, kể cả khi bản ghi trùng thuộc công ty "
     "khác mà mình không nhìn thấy — thông báo là \"Số tài khoản đã tồn tại\".\n"
     "3. ⚠️ Tài khoản đang Khóa KHÔNG sửa được: nút Sửa bị ẩn, và nếu cố gọi thẳng chức năng Sửa "
     "thì hệ thống chặn kèm thông báo yêu cầu mở khóa trước.\n"
     "4. ⚠️ Mở Sửa một tài khoản mà ngân hàng (hoặc loại tiền tệ) của nó đã bị khóa: ô đó bị xoá "
     "trắng kèm thông báo yêu cầu chọn lại. Đây là hành vi ĐÚNG, không phải mất dữ liệu.\n"
     "5. ⚠️ Cửa sổ Xem vẫn hiển thị tên ngân hàng đã khóa (lấy từ tên lưu sẵn trên bản ghi), khác "
     "với cửa sổ Sửa. Đừng ghi Failed vì \"hai màn hiện khác nhau\".\n"
     "6. Chỉ ô Chủ tài khoản bị chặn ngay khi bấm Lưu; 4 ô còn lại (Số tài khoản, Loại tiền tệ, "
     "Ngân hàng, Chi nhánh) báo lỗi đỏ sau khi hệ thống kiểm tra — cả 5 lỗi đều hiện ngay dưới ô.\n"
     "7. Trạng thái mặc định khi tạo mới là Hoạt động; ô Trạng thái có sẵn trên cửa sổ Thêm nên "
     "vẫn đổi được ngay lúc tạo.\n"
     "8. Bộ lọc được ghi nhớ 10 phút: rời màn rồi quay lại vẫn còn điều kiện lọc cũ — bấm Làm mới "
     "trước khi sang ca test khác.\n"
     "9. Số liệu tham chiếu của môi trường test khi viết tài liệu: lọc từ khoá \"TRANG TEST\" ra 5 "
     "tài khoản, trong đó tài khoản \"NGÂN HÀNG TRANG TEST 001\" đang ở trạng thái Khóa và tài "
     "khoản \"78787\" gắn ngân hàng đã bị khóa."),
]

# ============================================================ TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản CÓ quyền quản lý vào được màn hình", "P0",
     "Tài khoản được gán quyền \"Quản lý danh mục tài khoản ngân hàng\"; công ty của người đăng "
     "nhập có ít nhất 5 tài khoản ngân hàng",
     "1. Đăng nhập bằng tài khoản có quyền\n"
     "2. Vào phân hệ Tài chính\n"
     "3. Mở nhóm menu Danh mục\n"
     "4. Bấm mục Danh mục tài khoản ngân hàng",
     "Quyền: Quản lý danh mục tài khoản ngân hàng",
     "- Mục menu hiển thị\n"
     "- Vào được màn hình, danh sách hiện các tài khoản của công ty mình\n"
     "- Có nút Tạo mới ở góc phải trên bảng"),

    ("01", "Tài khoản có quyền làm được mọi thao tác trên dòng", "P0",
     "Vẫn tài khoản ở TC-ROLE-00; dòng \"cv1\" đang Hoạt động, dòng \"NGÂN HÀNG TRANG TEST 001\" "
     "đang Khóa",
     "1. Quan sát cột Hành động của dòng cv1\n2. Quan sát cột Hành động của dòng đang Khóa",
     "—",
     "- Dòng Hoạt động: hiện đủ Sửa, Khóa, Lịch sử\n"
     "- Dòng đang Khóa: chỉ còn Mở khóa và Lịch sử, KHÔNG có Sửa"),

    ("02", "Tài khoản KHÔNG có quyền không thấy mục menu", "P0",
     "Tài khoản nhân viên thường, KHÔNG được gán quyền \"Quản lý danh mục tài khoản ngân hàng\"",
     "1. Đăng nhập bằng tài khoản không có quyền\n"
     "2. Vào phân hệ Tài chính\n"
     "3. Mở nhóm menu Danh mục và tìm mục Danh mục tài khoản ngân hàng",
     "Tài khoản: nhân viên thường",
     "- Mục Danh mục tài khoản ngân hàng KHÔNG hiển thị trên menu"),

    ("03", "Tài khoản KHÔNG có quyền gõ thẳng đường dẫn", "P0",
     "Vẫn tài khoản không có quyền ở TC-ROLE-02",
     "1. Gõ thẳng /finance/account-banks vào thanh địa chỉ\n2. Nhấn Enter",
     "Đường dẫn: /finance/account-banks",
     "- Hệ thống từ chối, báo không có quyền truy cập\n"
     "- Không hiển thị bất kỳ tài khoản ngân hàng nào"),

    ("04", "Gọi thẳng chức năng Xem danh sách khi không có quyền", "P0",
     "Tài khoản không có quyền quản lý danh mục tài khoản ngân hàng",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xem danh sách tài khoản ngân hàng, bỏ qua "
     "giao diện",
     "—",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- ⚠️ Màn này chặn quyền ở CẢ chức năng xem danh sách, không chỉ các thao tác ghi"),

    ("05", "Gọi thẳng chức năng Tạo mới khi không có quyền", "P0",
     "Tài khoản không có quyền quản lý danh mục tài khoản ngân hàng",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Tạo mới tài khoản ngân hàng, bỏ qua giao "
     "diện\n2. Đăng nhập lại bằng tài khoản có quyền và kiểm tra danh sách",
     "Số tài khoản: QA-BYPASS-01",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- Danh sách không phát sinh bản ghi QA-BYPASS-01"),

    ("06", "Gọi thẳng chức năng Khóa khi không có quyền", "P1",
     "Tài khoản không có quyền; tài khoản ngân hàng \"cv1\" đang Hoạt động",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Khóa cho tài khoản cv1, bỏ qua giao diện\n"
     "2. Đăng nhập lại bằng tài khoản có quyền, kiểm tra trạng thái dòng cv1",
     "Tài khoản: cv1",
     "- Hệ thống từ chối, báo không có quyền\n- Dòng cv1 vẫn ở trạng thái Hoạt động"),

    ("07", "Chưa đăng nhập thì không vào được màn hình", "P0",
     "Trình duyệt ở chế độ ẩn danh, chưa đăng nhập",
     "1. Mở trình duyệt ẩn danh\n2. Gõ thẳng /finance/account-banks\n3. Nhấn Enter",
     "—",
     "- Hệ thống chuyển sang màn Đăng nhập\n- Không hiển thị dữ liệu nào"),

    ("08", "Xem lịch sử không cần quyền riêng", "P1",
     "Tài khoản có quyền quản lý danh mục tài khoản ngân hàng",
     "1. Mở màn hình danh sách\n2. Bấm nút Lịch sử ở một dòng bất kỳ",
     "—",
     "- Cửa sổ Lịch sử thay đổi mở bình thường\n"
     "- ⚠️ Vào được màn là xem được lịch sử, không có quyền riêng cho chức năng này"),
]

# ============================================================ SECTIONS
S1 = [
    (1, "Vào màn hình từ menu", "P0",
     "Tài khoản có quyền quản lý danh mục tài khoản ngân hàng",
     "1. Vào phân hệ Tài chính\n2. Mở nhóm menu Danh mục\n3. Bấm Danh mục tài khoản ngân hàng",
     "—",
     "- Tiêu đề trang hiển thị \"Danh mục tài khoản ngân hàng\"\n"
     "- Khối \"Bộ lọc danh sách\" nằm trên, bảng \"Danh sách tài khoản ngân hàng\" nằm dưới\n"
     "- Danh sách tải xong hiện tối đa 10 dòng đầu tiên"),

    (2, "Bố cục mặc định của bảng", "P0",
     "Tài khoản chưa từng chỉnh Tuỳ chỉnh cột ở màn này",
     "1. Vào màn hình\n2. Quan sát tiêu đề các cột từ trái sang phải",
     "—",
     "- Hiển thị sẵn: STT, Số tài khoản, Chủ tài khoản, Ngân hàng, Người tạo, Ngày tạo, Trạng "
     "thái, Hành động\n"
     "- Các cột Loại tiền tệ, Chi nhánh, Người cập nhật, Ngày cập nhật mặc định KHÔNG hiển thị\n"
     "- Cột Hành động nằm cuối bảng"),

    (3, "Thanh công cụ trên bảng", "P1",
     "Đang ở màn hình danh sách, tài khoản có quyền quản lý",
     "1. Quan sát góc phải phía trên bảng",
     "—",
     "- Có nút Tạo mới (nền xanh, dấu cộng)\n"
     "- Có nút Cấu hình cột hiển thị (biểu tượng cột)\n"
     "- Không có nút Xuất Excel, Nhập Excel hay In"),

    (4, "Hiển thị nhãn trạng thái", "P0",
     "Danh sách có cả tài khoản Hoạt động và tài khoản Khóa",
     "1. Quan sát cột Trạng thái của các dòng",
     "—",
     "- Tài khoản đang dùng: nhãn \"Hoạt động\" nền xanh\n"
     "- Tài khoản đã khóa: nhãn \"Khóa\" nền đỏ\n"
     "- Không hiển thị giá trị số ở cột này"),

    (5, "Bộ nút hành động của dòng Hoạt động", "P0",
     "Dòng \"cv1\" đang ở trạng thái Hoạt động",
     "1. Quan sát cột Hành động của dòng cv1",
     "Tài khoản: cv1",
     "- Hiện 3 nút: Sửa (bút chì), Khóa (ổ khoá), Lịch sử (đồng hồ)\n"
     "- Không có nút Xóa — màn hình không có chức năng xóa"),

    (6, "Bộ nút hành động của dòng đang Khóa", "P0",
     "Dòng \"NGÂN HÀNG TRANG TEST 001\" đang ở trạng thái Khóa",
     "1. Quan sát cột Hành động của dòng đó",
     "—",
     "- Chỉ còn 2 nút: Mở khóa và Lịch sử\n- Nút Sửa bị ẩn hẳn, không phải làm mờ"),

    (7, "Bấm số tài khoản để xem nhanh", "P0",
     "Danh sách đang hiển thị dòng cv1",
     "1. Bấm vào chữ cv1 ở cột Số tài khoản",
     "—",
     "- Mở cửa sổ \"Xem tài khoản ngân hàng\", không điều hướng sang trang khác\n"
     "- Mọi ô ở chế độ chỉ đọc"),

    (8, "Hiển thị khi ô dữ liệu để trống", "P1",
     "Có tài khoản dữ liệu cũ chưa gắn loại tiền tệ; đã bật cột Loại tiền tệ",
     "1. Bật cột Loại tiền tệ ở Cấu hình cột\n2. Quan sát dòng chưa có tiền tệ",
     "—",
     "- Ô Loại tiền tệ hiện dấu gạch ngang (—), không để trắng và không hiện chữ null"),

    (9, "Trạng thái danh sách rỗng", "P1",
     "Công ty của người đăng nhập có ít nhất 5 tài khoản",
     "1. Nhập vào ô tìm nhanh chuỗi không tồn tại\n2. Bấm Tìm kiếm",
     "Từ khoá: zzz-khong-ton-tai",
     "- Bảng hiện dòng \"Không có dữ liệu phù hợp bộ lọc.\"\n"
     "- Dòng thống kê hiện \"Hiển thị 0–0 / 0\", không báo lỗi"),

    (10, "Hiệu ứng chờ khi tải danh sách", "P2",
     "Đường truyền bình thường",
     "1. Bấm Làm mới\n2. Quan sát vùng bảng trong lúc chờ",
     "—",
     "- Có hiệu ứng đang tải, không hiện bảng trắng nhấp nháy\n- Tải xong hiệu ứng biến mất"),

    (11, "Tiêu đề tab trình duyệt", "P2",
     "Đang ở màn hình danh sách",
     "1. Quan sát tên tab trên trình duyệt",
     "—",
     "- Tab hiển thị \"Danh mục tài khoản ngân hàng\", không phải tên mặc định của phần mềm"),
]

S2 = [
    (1, "Tìm nhanh theo số tài khoản", "P0",
     "Công ty có tài khoản số \"0987656789\"",
     "1. Nhập từ khoá vào ô \"Tìm theo số tài khoản, chủ tài khoản, ngân hàng\"\n2. Bấm Tìm kiếm",
     "Từ khoá: 098765",
     "- Kết quả chỉ còn tài khoản có số chứa chuỗi 098765\n"
     "- Dòng thống kê cập nhật đúng số bản ghi tìm được"),

    (2, "Tìm nhanh theo chủ tài khoản", "P0",
     "Công ty có tài khoản chủ tài khoản \"LE HUYEN TRANG\"",
     "1. Nhập từ khoá\n2. Bấm Tìm kiếm",
     "Từ khoá: HUYEN",
     "- Dòng có chủ tài khoản LE HUYEN TRANG nằm trong kết quả"),

    (3, "Tìm nhanh theo tên ngân hàng", "P0",
     "Công ty có tài khoản gắn ngân hàng \"NGÂN HÀNG TRANG TEST 001\"",
     "1. Nhập từ khoá\n2. Bấm Tìm kiếm",
     "Từ khoá: TRANG TEST",
     "- Kết quả gồm các tài khoản có số, chủ tài khoản hoặc tên ngân hàng chứa chuỗi TRANG TEST\n"
     "- Với dữ liệu mẫu: ra 5 dòng"),

    (4, "Tìm nhanh khớp một phần ở giữa chuỗi", "P1",
     "Công ty có tài khoản chủ tài khoản \"TRANG TEST CHECK\"",
     "1. Nhập từ khoá\n2. Bấm Tìm kiếm",
     "Từ khoá: TEST CHE",
     "- Vẫn tìm ra dòng TRANG TEST CHECK dù chuỗi nằm giữa"),

    (5, "Tìm nhanh không phân biệt chữ hoa chữ thường", "P1",
     "Công ty có tài khoản chủ tài khoản in hoa \"TRANG TEST 01\"",
     "1. Nhập từ khoá chữ thường, bấm Tìm kiếm\n2. Nhập lại bằng chữ hoa, bấm Tìm kiếm",
     "Từ khoá: trang test → TRANG TEST",
     "- Hai lần tìm cho cùng một danh sách kết quả"),

    (6, "Nhấn Enter trong ô tìm nhanh", "P1",
     "Đang ở màn hình danh sách",
     "1. Nhập từ khoá vào ô tìm nhanh\n2. Nhấn phím Enter",
     "Từ khoá: cv1",
     "- Danh sách lọc ngay, không cần bấm nút Tìm kiếm"),

    (7, "Gõ từ khoá nhưng chưa bấm Tìm kiếm", "P0",
     "Danh sách đang hiển thị đầy đủ",
     "1. Gõ từ khoá vào ô tìm nhanh\n2. Chờ 3 giây, không bấm gì thêm",
     "Từ khoá: cv1",
     "- Danh sách GIỮ NGUYÊN, chưa lọc\n"
     "- ⚠️ Ô tìm nhanh chỉ có tác dụng khi bấm Tìm kiếm hoặc nhấn Enter"),

    (8, "Xoá nhanh từ khoá bằng dấu x", "P2",
     "Ô tìm nhanh đang chứa từ khoá và danh sách đang lọc",
     "1. Bấm dấu x ở cuối ô tìm nhanh\n2. Bấm Tìm kiếm",
     "—",
     "- Ô tìm nhanh trống, danh sách trở lại đầy đủ"),

    (9, "Lọc theo tên chi nhánh", "P0",
     "Công ty có tài khoản gắn chi nhánh \"TRang test\" và chi nhánh \"Bắc Hải Phòng\"",
     "1. Nhập vào ô \"Nhập tên chi nhánh\"\n2. Bấm Tìm kiếm",
     "Chi nhánh: Bắc",
     "- Kết quả chỉ gồm tài khoản có tên chi nhánh chứa chuỗi Bắc\n"
     "- Tài khoản chi nhánh khác bị loại khỏi danh sách"),

    (10, "Lọc theo trạng thái Hoạt động", "P0",
     "Danh sách có cả tài khoản Hoạt động và Khóa",
     "1. Chọn ô Trạng thái = Hoạt động\n2. Quan sát danh sách",
     "Trạng thái: Hoạt động",
     "- Danh sách tự lọc ngay khi chọn, không cần bấm Tìm kiếm\n"
     "- Mọi dòng đều mang nhãn Hoạt động"),

    (11, "Lọc theo trạng thái Khóa", "P0",
     "Có ít nhất 1 tài khoản đang Khóa (\"NGÂN HÀNG TRANG TEST 001\")",
     "1. Chọn ô Trạng thái = Khóa",
     "Trạng thái: Khóa",
     "- Kết quả chỉ gồm tài khoản đang Khóa\n"
     "- ⚠️ Trạng thái Khóa lưu giá trị 0 — kiểm tra kỹ bộ lọc có bỏ sót dòng nào không"),

    (12, "Bỏ chọn trạng thái để lấy lại tất cả", "P1",
     "Đang lọc Trạng thái = Khóa",
     "1. Bấm dấu x để bỏ chọn ở ô Trạng thái",
     "—",
     "- Danh sách trở lại đủ cả tài khoản Hoạt động lẫn Khóa"),

    (13, "Kết hợp từ khoá và trạng thái", "P0",
     "Từ khoá TRANG TEST ra 5 dòng, trong đó 1 dòng đang Khóa",
     "1. Nhập ô tìm nhanh: TRANG TEST\n2. Bấm Tìm kiếm\n3. Chọn Trạng thái = Khóa",
     "Từ khoá: TRANG TEST | Trạng thái: Khóa",
     "- ⚠️ Kiểm TỪNG DÒNG: mỗi dòng phải vừa khớp từ khoá vừa đang Khóa\n"
     "- Với dữ liệu mẫu: còn đúng 1 dòng"),

    (14, "Kết hợp chi nhánh và trạng thái", "P1",
     "Có tài khoản chi nhánh \"TRang test\" ở cả 2 trạng thái",
     "1. Nhập Chi nhánh: TRang test\n2. Chọn Trạng thái = Hoạt động",
     "Chi nhánh: TRang test | Trạng thái: Hoạt động",
     "- Kết quả thoả mãn đồng thời hai điều kiện"),

    (15, "Nút Làm mới xoá toàn bộ điều kiện lọc", "P0",
     "Đang lọc từ khoá + chi nhánh + trạng thái",
     "1. Bấm nút Làm mới\n2. Quan sát cả ô lọc lẫn danh sách",
     "—",
     "- Cả 3 ô lọc trở về trống\n- Danh sách tải lại đầy đủ ngay lập tức"),

    (16, "Lọc xong luôn quay về trang 1", "P1",
     "Danh sách có nhiều hơn 1 trang",
     "1. Sang trang 2\n2. Nhập từ khoá và bấm Tìm kiếm",
     "Từ khoá: TRANG",
     "- Kết quả hiển thị từ trang 1, dòng thống kê bắt đầu bằng \"Hiển thị 1–\""),

    (17, "Từ khoá chứa ký tự đặc biệt", "P1",
     "Công ty có ít nhất 5 tài khoản",
     "1. Nhập ký tự % vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "Từ khoá: %",
     "- Không được trả về toàn bộ danh sách\n"
     "- Kết quả rỗng hoặc chỉ gồm bản ghi thật sự chứa ký tự %"),

    (18, "Hệ thống ghi nhớ bộ lọc khi rời màn rồi quay lại", "P1",
     "Đang lọc Trạng thái = Khóa",
     "1. Lọc Trạng thái = Khóa\n2. Sang màn khác trong phân hệ Tài chính\n"
     "3. Trong vòng 10 phút quay lại màn Danh mục tài khoản ngân hàng",
     "Trạng thái: Khóa",
     "- Ô Trạng thái vẫn giữ giá trị Khóa và danh sách vẫn đang lọc\n"
     "- ⚠️ Là hành vi cố ý (nhớ 10 phút), không phải lỗi không làm mới"),

    (19, "Bộ lọc hết hạn ghi nhớ", "P2",
     "Đã lọc rồi rời màn quá 10 phút",
     "1. Lọc theo trạng thái\n2. Rời màn quá 10 phút\n3. Quay lại màn hình",
     "—",
     "- Bộ lọc trở về trống, danh sách hiển thị đầy đủ"),
]

S3 = [
    (1, "Phân trang mặc định", "P0",
     "Công ty có nhiều hơn 10 tài khoản ngân hàng",
     "1. Vào màn hình\n2. Quan sát vùng dưới bảng",
     "—",
     "- Mỗi trang 10 dòng\n- Dòng thống kê dạng \"Hiển thị 1–10 / N\"\n- Ô số dòng/trang hiện 10"),

    (2, "Chuyển sang trang kế tiếp", "P0",
     "Danh sách có ít nhất 2 trang",
     "1. Bấm số trang 2 hoặc mũi tên sang phải",
     "—",
     "- Hiển thị 10 dòng tiếp theo\n- Cột STT bắt đầu từ 11\n- Dòng thống kê cập nhật đúng"),

    (3, "Chuyển tới trang cuối và về trang đầu", "P1",
     "Danh sách có ít nhất 3 trang",
     "1. Bấm nút về trang cuối\n2. Bấm nút về trang đầu",
     "—",
     "- Trang cuối hiện số dòng còn lại, nút sang trang tiếp bị vô hiệu hoá\n"
     "- Về trang đầu thì nút lùi bị vô hiệu hoá"),

    (4, "Đổi số dòng/trang", "P0",
     "Công ty có nhiều hơn 10 tài khoản",
     "1. Chọn ô Số dòng/trang = 50",
     "Số dòng/trang: 50",
     "- Danh sách hiện tối đa 50 dòng và quay về trang 1\n- Dòng thống kê cập nhật đúng"),

    (5, "Danh sách các mức số dòng/trang", "P2",
     "Đang ở màn hình danh sách",
     "1. Mở ô Số dòng/trang",
     "—",
     "- Có đúng 5 lựa chọn: 5, 10, 20, 50, 100"),

    (6, "Phân trang giữ nguyên bộ lọc", "P0",
     "Đang lọc Trạng thái = Hoạt động và kết quả nhiều hơn 1 trang",
     "1. Lọc Trạng thái = Hoạt động\n2. Sang trang 2\n3. Kiểm tra nhãn trạng thái mọi dòng",
     "Trạng thái: Hoạt động",
     "- Trang 2 vẫn chỉ chứa tài khoản Hoạt động\n- Ô lọc không bị xoá khi chuyển trang"),

    (7, "Không trùng và không sót dữ liệu giữa các trang", "P0",
     "Danh sách có ít nhất 2 trang",
     "1. Ghi lại số tài khoản của tất cả các trang\n2. Đối chiếu danh sách thu được",
     "—",
     "- Không số tài khoản nào lặp ở 2 trang\n- Tổng số dòng đếm được bằng N ở dòng thống kê"),

    (8, "Thứ tự mặc định của danh sách", "P0",
     "Vừa tạo mới một tài khoản trong hôm nay",
     "1. Tạo mới 1 tài khoản\n2. Quay về danh sách, không bấm sắp xếp gì",
     "—",
     "- Tài khoản vừa tạo nằm ở dòng đầu tiên\n- Danh sách xếp theo Ngày tạo mới nhất trước"),

    (9, "Sắp xếp theo Số tài khoản", "P0",
     "Danh sách có ít nhất 5 dòng với số tài khoản khác nhau",
     "1. Bấm vào tiêu đề cột Số tài khoản\n2. Quan sát thứ tự\n3. Bấm lần nữa",
     "—",
     "- Lần 1: xếp tăng dần theo số tài khoản\n- Lần 2: xếp giảm dần\n"
     "- Dữ liệu thực sự đổi thứ tự, không chỉ đổi mũi tên"),

    (10, "Sắp xếp theo Chủ tài khoản", "P0",
     "Danh sách có ít nhất 5 dòng",
     "1. Bấm tiêu đề cột Chủ tài khoản\n2. Đối chiếu thứ tự chữ cái đầu",
     "—",
     "- Xếp đúng theo bảng chữ cái, bấm lần 2 đảo chiều"),

    (11, "Sắp xếp theo Ngày tạo", "P1",
     "Danh sách có bản ghi tạo ở nhiều ngày khác nhau",
     "1. Bấm tiêu đề cột Ngày tạo",
     "—",
     "- Xếp đúng theo ngày giờ tạo, bấm lần 2 đảo chiều"),

    (12, "Sắp xếp theo Ngày cập nhật", "P1",
     "Đã bật cột Ngày cập nhật ở Cấu hình cột",
     "1. Bật cột Ngày cập nhật\n2. Bấm tiêu đề cột đó",
     "—",
     "- Xếp đúng theo ngày giờ cập nhật gần nhất"),

    (13, "Cột không cho sắp xếp", "P2",
     "Đang ở màn hình danh sách",
     "1. Bấm lần lượt tiêu đề Ngân hàng, Chi nhánh, Trạng thái, Hành động",
     "—",
     "- Các cột này không có biểu tượng sắp xếp, bấm vào không xảy ra gì và không báo lỗi"),

    (14, "Sắp xếp giữ nguyên bộ lọc", "P1",
     "Đang lọc Trạng thái = Hoạt động",
     "1. Lọc Trạng thái = Hoạt động\n2. Bấm sắp xếp theo Số tài khoản",
     "—",
     "- Kết quả vừa đúng thứ tự vừa chỉ gồm tài khoản Hoạt động"),

    (15, "Mở cửa sổ Cấu hình cột", "P0",
     "Đang ở màn hình danh sách",
     "1. Bấm nút biểu tượng cột bên cạnh nút Tạo mới",
     "—",
     "- Mở cửa sổ \"Tuỳ chỉnh cột\" liệt kê đủ 12 cột\n- Có nút Lưu và nút Đóng"),

    (16, "Cột bị khoá trong Cấu hình cột", "P0",
     "Cửa sổ Tuỳ chỉnh cột đang mở",
     "1. Thử bỏ tích dòng STT\n2. Thử bỏ tích dòng Số tài khoản",
     "—",
     "- Hai dòng này hiện biểu tượng ổ khoá, không bỏ tích được\n"
     "- ⚠️ Cột Số tài khoản là lối vào cửa sổ Xem nên không được phép ẩn"),

    (17, "Bật thêm cột và lưu lại", "P0",
     "Cột Loại tiền tệ đang tắt",
     "1. Mở Tuỳ chỉnh cột\n2. Tích dòng Loại tiền tệ\n3. Bấm Lưu\n4. Tải lại trang",
     "Cột bật thêm: Loại tiền tệ",
     "- Bảng hiện thêm cột Loại tiền tệ\n- Tải lại trang vẫn giữ (ghi nhớ theo tài khoản)"),

    (18, "Tắt bớt cột", "P1",
     "Cột Chi nhánh đang hiện",
     "1. Mở Tuỳ chỉnh cột\n2. Bỏ tích dòng Chi nhánh\n3. Bấm Lưu",
     "—",
     "- Cột Chi nhánh biến mất, các cột còn lại giữ nguyên thứ tự"),

    (19, "Đổi vị trí cột bằng kéo thả", "P1",
     "Cửa sổ Tuỳ chỉnh cột đang mở",
     "1. Kéo dòng Ngân hàng lên trên dòng Chủ tài khoản\n2. Bấm Lưu",
     "—",
     "- Bảng hiển thị cột theo thứ tự mới\n- Dữ liệu từng cột vẫn đúng, không lệch cột"),

    (20, "Đóng cửa sổ Cấu hình cột không lưu", "P1",
     "Đã tích thêm một cột nhưng chưa bấm Lưu",
     "1. Tích thêm cột bất kỳ\n2. Bấm Đóng",
     "—",
     "- Cửa sổ đóng, bảng KHÔNG đổi"),
]

S4 = [
    (1, "Mở cửa sổ Tạo mới", "P0",
     "Tài khoản có quyền quản lý, đang ở màn hình danh sách",
     "1. Bấm nút Tạo mới",
     "—",
     "- Mở cửa sổ tiêu đề \"Tạo tài khoản ngân hàng\"\n"
     "- Có 5 ô: Số tài khoản, Loại tiền tệ, Chủ tài khoản, Ngân hàng, Chi nhánh — đều có dấu sao "
     "đỏ; thêm ô Trạng thái\n"
     "- Chân cửa sổ có 2 nút: Lưu và Đóng"),

    (2, "Giá trị điền sẵn khi tạo mới", "P0",
     "Vừa mở cửa sổ Tạo tài khoản ngân hàng",
     "1. Quan sát toàn bộ các ô",
     "—",
     "- 5 ô bắt buộc đều trống\n- Ô Trạng thái điền sẵn \"Hoạt động\"\n"
     "- Ô Chi nhánh bị khoá cho tới khi chọn Ngân hàng\n"
     "- Ô Chủ tài khoản có dòng gợi ý \"Hệ thống tự chuyển thành CHỮ IN HOA khi lưu\""),

    (3, "Tạo mới đầy đủ thông tin", "P0",
     "Danh mục chưa có số tài khoản QA0001; ngân hàng \"Ngân hàng TMCP An Bình\" đang Hoạt động và "
     "có chi nhánh",
     "1. Bấm Tạo mới\n2. Nhập Số tài khoản, chọn Loại tiền tệ, nhập Chủ tài khoản\n"
     "3. Chọn Ngân hàng rồi chọn Chi nhánh\n4. Bấm Lưu",
     "Số tài khoản: QA0001 | Loại tiền tệ: VNĐ | Chủ tài khoản: Nguyễn Văn Kiểm Thử | "
     "Ngân hàng: Ngân hàng TMCP An Bình | Chi nhánh: (chi nhánh bất kỳ của ngân hàng đó)",
     "- Hệ thống báo \"Thêm mới thành công\"\n- Cửa sổ đóng, danh sách tải lại\n"
     "- Dòng QA0001 nằm đầu danh sách, trạng thái Hoạt động\n"
     "- ⚠️ Chủ tài khoản hiển thị IN HOA: NGUYỄN VĂN KIỂM THỬ"),

    (4, "Tạo mới với trạng thái Khóa ngay từ đầu", "P1",
     "Danh mục chưa có số tài khoản QA0002",
     "1. Bấm Tạo mới\n2. Nhập đủ 5 ô bắt buộc\n3. Đổi ô Trạng thái sang Khóa\n4. Bấm Lưu",
     "Số tài khoản: QA0002 | Trạng thái: Khóa",
     "- Lưu thành công\n- Dòng QA0002 mang nhãn Khóa và KHÔNG có nút Sửa"),

    (5, "Bỏ trống toàn bộ rồi bấm Lưu", "P0",
     "Vừa mở cửa sổ Tạo tài khoản ngân hàng",
     "1. Bấm Tạo mới\n2. Bấm ngay nút Lưu",
     "—",
     "- Ô Chủ tài khoản viền đỏ kèm dòng \"Bắt buộc phải nhập\"\n"
     "- Cửa sổ KHÔNG đóng, không tạo bản ghi nào"),

    (6, "Chỉ nhập Chủ tài khoản rồi bấm Lưu", "P0",
     "Vừa mở cửa sổ Tạo tài khoản ngân hàng",
     "1. Nhập Chủ tài khoản\n2. Bỏ trống 4 ô còn lại\n3. Bấm Lưu",
     "Chủ tài khoản: Nguyễn Văn Kiểm Thử",
     "- Hiện lỗi đỏ \"Bắt buộc phải nhập\" dưới CẢ 4 ô: Số tài khoản, Loại tiền tệ, Ngân hàng, "
     "Chi nhánh\n"
     "- Dữ liệu đã nhập vẫn còn nguyên, cửa sổ không đóng"),

    (7, "Trùng số tài khoản trong cùng công ty", "P0",
     "Công ty đã có tài khoản số \"cv1\"",
     "1. Bấm Tạo mới\n2. Nhập Số tài khoản trùng và các ô còn lại hợp lệ\n3. Bấm Lưu",
     "Số tài khoản: cv1",
     "- Lỗi đỏ \"Số tài khoản đã tồn tại\" hiện dưới ô Số tài khoản\n- Không tạo bản ghi mới"),

    (8, "Trùng số tài khoản với công ty khác", "P0",
     "Công ty B (không phải công ty của người đăng nhập) đã có tài khoản số QA-KHACCTY",
     "1. Đăng nhập bằng tài khoản thuộc công ty A\n2. Tạo mới với số tài khoản QA-KHACCTY\n"
     "3. Bấm Lưu",
     "Số tài khoản: QA-KHACCTY",
     "- Vẫn bị chặn với thông báo \"Số tài khoản đã tồn tại\"\n"
     "- ⚠️ Ràng buộc trùng áp dụng TOÀN HỆ THỐNG, dù người dùng không nhìn thấy bản ghi của công "
     "ty khác — đây là hành vi đúng, không phải lỗi"),

    (9, "Ô Chi nhánh khoá cho tới khi chọn Ngân hàng", "P0",
     "Cửa sổ Tạo tài khoản ngân hàng đang mở, chưa chọn ngân hàng",
     "1. Bấm vào ô Chi nhánh khi chưa chọn Ngân hàng\n2. Chọn một Ngân hàng\n3. Bấm lại ô Chi nhánh",
     "Ngân hàng: Ngân hàng TMCP An Bình",
     "- Trước khi chọn ngân hàng: ô Chi nhánh không mở được\n"
     "- Sau khi chọn: ô Chi nhánh mở và chỉ liệt kê chi nhánh CỦA ngân hàng vừa chọn"),

    (10, "Đổi ngân hàng thì chi nhánh bị xoá trắng", "P0",
     "Đã chọn Ngân hàng A và Chi nhánh của A",
     "1. Chọn Ngân hàng A, chọn Chi nhánh của A\n2. Đổi sang Ngân hàng B\n3. Quan sát ô Chi nhánh",
     "—",
     "- Ô Chi nhánh tự xoá trắng, bắt chọn lại theo ngân hàng mới\n"
     "- ⚠️ Không được giữ lại chi nhánh của ngân hàng cũ"),

    (11, "Ngân hàng đang khóa không xuất hiện trong ô chọn", "P0",
     "Ngân hàng \"TRANG TEST 78\" đang bị khóa ở Danh mục ngân hàng",
     "1. Bấm Tạo mới\n2. Mở ô Ngân hàng và tìm ngân hàng đang khóa",
     "Ngân hàng: TRANG TEST 78 (đang khóa)",
     "- Ngân hàng đang khóa KHÔNG có trong danh sách chọn"),

    (12, "Loại tiền tệ đang khóa không xuất hiện trong ô chọn", "P0",
     "Có ít nhất 1 loại tiền tệ đang bị khóa ở Danh mục tiền tệ",
     "1. Bấm Tạo mới\n2. Mở ô Loại tiền tệ và tìm loại tiền tệ đang khóa",
     "—",
     "- Loại tiền tệ đang khóa KHÔNG có trong danh sách chọn"),

    (13, "Hiển thị của ô Loại tiền tệ", "P2",
     "Cửa sổ Tạo tài khoản ngân hàng đang mở",
     "1. Mở ô Loại tiền tệ và quan sát cách hiển thị các lựa chọn",
     "—",
     "- Mỗi lựa chọn hiện dạng \"Mã — Tên\", ví dụ \"VNĐ — VietNamDong\""),

    (14, "Mở cửa sổ Sửa", "P0",
     "Tài khoản \"cv1\" đang Hoạt động",
     "1. Bấm nút Sửa ở dòng cv1",
     "—",
     "- Cửa sổ tiêu đề \"Sửa tài khoản ngân hàng\"\n- Các ô điền sẵn dữ liệu hiện tại\n"
     "- Chân cửa sổ có nút Lưu và Đóng"),

    (15, "Sửa và lưu thành công", "P0",
     "Tài khoản QA0001 vừa tạo ở TC_04.003",
     "1. Bấm Sửa dòng QA0001\n2. Đổi Chủ tài khoản\n3. Bấm Lưu",
     "Chủ tài khoản mới: Trần Thị Kiểm Thử",
     "- Báo \"Cập nhật thành công\", cửa sổ đóng\n- Danh sách hiện tên mới IN HOA\n"
     "- Cột Người cập nhật và Ngày cập nhật đổi theo người đang đăng nhập"),

    (16, "Sửa và bỏ trống ô bắt buộc", "P0",
     "Đang mở cửa sổ Sửa của QA0001",
     "1. Xoá trắng ô Chủ tài khoản\n2. Bấm Lưu",
     "Chủ tài khoản: (để trống)",
     "- Lỗi đỏ \"Bắt buộc phải nhập\" dưới ô Chủ tài khoản, không lưu"),

    (17, "Sửa số tài khoản thành số đã tồn tại", "P0",
     "Đang sửa QA0001; công ty đã có tài khoản cv1",
     "1. Bấm Sửa dòng QA0001\n2. Đổi Số tài khoản thành cv1\n3. Bấm Lưu",
     "Số tài khoản: cv1",
     "- Lỗi đỏ \"Số tài khoản đã tồn tại\", không lưu"),

    (18, "Sửa mà giữ nguyên số tài khoản của chính nó", "P0",
     "Đang sửa QA0001 (số tài khoản QA0001)",
     "1. Bấm Sửa dòng QA0001\n2. Giữ nguyên số tài khoản, chỉ đổi Loại tiền tệ\n3. Bấm Lưu",
     "Loại tiền tệ: AUD",
     "- Lưu thành công, KHÔNG báo trùng với chính nó"),

    (19, "Sửa tài khoản có ngân hàng đã bị khóa", "P0",
     "Tài khoản \"78787\" gắn ngân hàng \"TRANG TEST 78\" — ngân hàng này đã bị khóa",
     "1. Bấm Sửa dòng 78787\n2. Quan sát ô Ngân hàng và ô Chi nhánh",
     "Tài khoản: 78787",
     "- Ô Ngân hàng bị XOÁ TRẮNG kèm thông báo \"Ngân hàng của tài khoản này đã bị khóa, vui lòng "
     "chọn ngân hàng khác\"\n"
     "- Ô Chi nhánh cũng trống theo\n"
     "- ⚠️ Đây là hành vi ĐÚNG, không phải mất dữ liệu; muốn lưu phải chọn ngân hàng khác"),

    (20, "Sửa tài khoản có loại tiền tệ đã bị khóa", "P1",
     "Có tài khoản gắn loại tiền tệ vừa bị khóa ở Danh mục tiền tệ",
     "1. Bấm Sửa dòng đó\n2. Quan sát ô Loại tiền tệ",
     "—",
     "- Ô Loại tiền tệ bị xoá trắng kèm thông báo \"Loại tiền tệ của tài khoản này đã bị khóa, vui "
     "lòng chọn loại tiền tệ khác\""),

    (21, "Không sửa được tài khoản đang Khóa", "P0",
     "Tài khoản \"NGÂN HÀNG TRANG TEST 001\" đang ở trạng thái Khóa",
     "1. Quan sát cột Hành động của dòng đó",
     "—",
     "- Không có nút Sửa\n- Muốn sửa phải Mở khóa trước"),

    (22, "Gọi thẳng chức năng Sửa với tài khoản đang Khóa", "P0",
     "Tài khoản đang Khóa, nút Sửa đã bị ẩn ngoài danh sách",
     "1. Ghi lại định danh tài khoản đang Khóa\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa cho tài khoản đó, bỏ qua giao diện",
     "—",
     "- Hệ thống từ chối kèm thông báo yêu cầu mở khoá trước khi cập nhật\n"
     "- Dữ liệu của tài khoản không thay đổi\n"
     "- ⚠️ Đây là chốt chặn quan trọng: giao diện ẩn nút chỉ là lớp ngoài"),

    (23, "Mở cửa sổ Xem", "P0",
     "Tài khoản cv1 đang hiển thị trên danh sách",
     "1. Bấm vào số tài khoản cv1",
     "—",
     "- Cửa sổ tiêu đề \"Xem tài khoản ngân hàng\"\n- Mọi ô ở chế độ chỉ đọc\n"
     "- Chân cửa sổ chỉ có nút Đóng, không có nút Lưu\n- Có khối Lịch sử ở cuối"),

    (24, "Xem tài khoản có ngân hàng đã bị khóa", "P0",
     "Tài khoản 78787 gắn ngân hàng đã bị khóa",
     "1. Bấm vào số tài khoản 78787",
     "—",
     "- Ô Ngân hàng VẪN hiện tên ngân hàng đã khóa (lấy từ tên lưu sẵn trên bản ghi)\n"
     "- ⚠️ Khác cửa sổ Sửa (ô bị xoá trắng) — đây là chủ đích, không phải lỗi"),

    (25, "Xem tài khoản đang Khóa", "P1",
     "Tài khoản \"NGÂN HÀNG TRANG TEST 001\" đang Khóa",
     "1. Bấm vào số tài khoản đó",
     "—",
     "- Vẫn mở được cửa sổ Xem\n- Ô Trạng thái hiện \"Khóa\""),

    (26, "Mở Sửa ngay sau khi đóng Xem", "P0",
     "Vừa xem tài khoản cv1 và đã đóng cửa sổ",
     "1. Bấm số tài khoản cv1 để xem\n2. Bấm Đóng\n3. Bấm nút Sửa của chính dòng đó",
     "—",
     "- Cửa sổ mở ở chế độ Sửa: tiêu đề \"Sửa tài khoản ngân hàng\", các ô nhập được, có nút Lưu\n"
     "- ⚠️ Không được kẹt ở chế độ chỉ đọc"),

    (27, "Mở Sửa hai dòng liên tiếp", "P0",
     "Danh sách có dòng cv1 và dòng 0123456",
     "1. Bấm Sửa dòng cv1, xem dữ liệu rồi Đóng\n2. Bấm Sửa dòng 0123456",
     "—",
     "- Cửa sổ lần 2 hiển thị đúng dữ liệu của 0123456\n- Không sót dữ liệu của cv1"),

    (28, "Bấm Lưu nhiều lần liên tiếp", "P0",
     "Cửa sổ Tạo mới đã nhập đủ dữ liệu hợp lệ",
     "1. Nhập đủ 5 ô bắt buộc\n2. Bấm nút Lưu 3 lần thật nhanh\n3. Đếm số dòng trong danh sách",
     "Số tài khoản: QA0003",
     "- Chỉ tạo ra ĐÚNG 1 tài khoản QA0003\n- Nút Lưu bị vô hiệu hoá trong lúc đang xử lý"),

    (29, "Đóng cửa sổ khi đang nhập dở", "P1",
     "Cửa sổ Tạo mới đang mở",
     "1. Nhập Chủ tài khoản\n2. Bấm nút Đóng",
     "Chủ tài khoản: Nguyễn Văn Kiểm Thử",
     "- Mong đợi: hệ thống hỏi lại \"Thông tin chưa lưu\" trước khi đóng\n"
     "- ⚠️ Thực tế trên bản đang chạy cửa sổ đóng thẳng, mất dữ liệu đang nhập — ghi nhận Failed"),
]

S5 = [
    (1, "Mở hộp xác nhận Khóa", "P0",
     "Tài khoản \"78787\" đang Hoạt động",
     "1. Bấm nút Khóa (ổ khoá) ở dòng 78787",
     "—",
     "- Hộp thoại tiêu đề \"Xác nhận khóa\"\n"
     "- Nội dung: \"Bạn có chắc muốn khóa tài khoản '78787'?\"\n- Hai nút: Khóa và Hủy"),

    (2, "Khóa tài khoản", "P0",
     "Tài khoản QA0001 đang Hoạt động",
     "1. Bấm Khóa ở dòng QA0001\n2. Bấm nút Khóa trong hộp xác nhận",
     "Tài khoản: QA0001",
     "- Báo \"Khóa thành công\"\n- Dòng QA0001 chuyển nhãn Khóa\n"
     "- Cột Hành động của dòng đó chỉ còn Mở khóa và Lịch sử"),

    (3, "Hủy thao tác Khóa", "P0",
     "Tài khoản QA0003 đang Hoạt động",
     "1. Bấm Khóa ở dòng QA0003\n2. Bấm nút Hủy",
     "—",
     "- Hộp thoại đóng, trạng thái giữ nguyên Hoạt động, không có thông báo nào"),

    (4, "Mở khóa tài khoản", "P0",
     "Tài khoản QA0001 đang Khóa",
     "1. Bấm nút Mở khóa ở dòng QA0001\n2. Bấm nút Mở khóa trong hộp xác nhận",
     "Tài khoản: QA0001",
     "- Hộp thoại tiêu đề \"Xác nhận mở khóa\"\n- Báo \"Mở khóa thành công\"\n"
     "- Dòng trở lại nhãn Hoạt động và hiện lại nút Sửa"),

    (5, "Trạng thái sau khi tải lại trang", "P1",
     "Vừa khóa tài khoản QA0001",
     "1. Khóa QA0001\n2. Nhấn F5 tải lại trang\n3. Tìm lại dòng QA0001",
     "—",
     "- Sau khi tải lại, QA0001 vẫn ở trạng thái Khóa (đã ghi thật, không chỉ đổi trên màn hình)"),

    (6, "Khóa rồi lọc theo trạng thái", "P1",
     "Vừa khóa QA0001",
     "1. Chọn Trạng thái = Khóa",
     "Trạng thái: Khóa",
     "- QA0001 nằm trong kết quả lọc"),

    (7, "Đổi trạng thái bằng cách Sửa", "P1",
     "Tài khoản QA0003 đang Hoạt động",
     "1. Bấm Sửa dòng QA0003\n2. Đổi ô Trạng thái sang Khóa\n3. Bấm Lưu",
     "Trạng thái: Khóa",
     "- Báo cập nhật thành công, dòng chuyển sang nhãn Khóa\n"
     "- ⚠️ Có 2 đường đổi trạng thái: nút Khóa ngoài danh sách và ô Trạng thái trong cửa sổ Sửa — "
     "kết quả phải như nhau"),

    (8, "Tài khoản đã khóa có còn chọn được ở màn nghiệp vụ khác không", "P1",
     "Tài khoản QA0001 đang ở trạng thái Khóa",
     "1. Khóa QA0001\n2. Vào một màn nghiệp vụ có chọn tài khoản ngân hàng của công ty\n"
     "3. Mở ô chọn tài khoản và tìm QA0001",
     "Tài khoản: QA0001",
     "- Ghi nhận kết quả thực tế: tài khoản đã khóa có còn xuất hiện trong ô chọn hay không\n"
     "- ⚠️ Nghiệp vụ mong đợi tài khoản đã khóa không được chọn mới; nếu vẫn chọn được thì báo lại"),

    (9, "Lịch sử ghi nhận thao tác Khóa", "P0",
     "Vừa khóa tài khoản QA0001",
     "1. Bấm nút Lịch sử ở dòng QA0001",
     "—",
     "- Mốc mới nhất là \"Khóa\"\n- Dòng chi tiết: Trạng thái: Hoạt động → Khóa\n"
     "- Ghi đúng tên người thực hiện và thời điểm"),

    (10, "Lịch sử ghi nhận thao tác Mở khóa", "P0",
     "Vừa mở khóa tài khoản QA0001",
     "1. Bấm nút Lịch sử ở dòng QA0001",
     "—",
     "- Mốc mới nhất là \"Mở khóa\", chi tiết: Trạng thái: Khóa → Hoạt động"),
]

S6 = [
    (1, "Nhập số tài khoản chỉ gồm khoảng trắng", "P0",
     "Cửa sổ Tạo mới đang mở",
     "1. Nhập 3 dấu cách vào ô Số tài khoản\n2. Nhập đủ các ô còn lại\n3. Bấm Lưu",
     "Số tài khoản: (3 dấu cách)",
     "- Mong đợi: hệ thống coi là chưa nhập và báo lỗi bắt buộc\n"
     "- ⚠️ Nếu lưu được số tài khoản rỗng thì báo lại: danh mục sẽ có dòng không tra cứu được"),

    (2, "Khoảng trắng đầu cuối bị cắt khi lưu", "P1",
     "Cửa sổ Tạo mới đang mở",
     "1. Nhập Số tài khoản có dấu cách ở đầu và cuối\n2. Nhập các ô còn lại, bấm Lưu\n"
     "3. Mở lại cửa sổ Sửa của bản ghi vừa tạo",
     "Số tài khoản: \"  QA0004  \"",
     "- Giá trị lưu là QA0004, đã cắt sạch khoảng trắng đầu cuối\n"
     "- Danh sách hiển thị không bị thụt lề bất thường"),

    (3, "Chủ tài khoản tự chuyển thành chữ in hoa", "P0",
     "Cửa sổ Tạo mới đang mở",
     "1. Nhập Chủ tài khoản bằng chữ thường có dấu\n2. Nhập đủ các ô còn lại, bấm Lưu\n"
     "3. Quan sát danh sách",
     "Chủ tài khoản: nguyễn thị hoa",
     "- Danh sách hiển thị NGUYỄN THỊ HOA\n"
     "- ⚠️ Dấu tiếng Việt phải còn nguyên sau khi in hoa"),

    (4, "Nhập số tài khoản dài quá giới hạn", "P1",
     "Cửa sổ Tạo mới đang mở",
     "1. Nhập Số tài khoản 300 ký tự\n2. Nhập đủ các ô còn lại, bấm Lưu",
     "Số tài khoản: chuỗi 300 ký tự",
     "- Không được lưu chuỗi bị cắt cụt một cách âm thầm\n"
     "- Hoặc chặn kèm thông báo, hoặc lưu đủ và hiển thị lại đúng chuỗi đã nhập"),

    (5, "Nhập chủ tài khoản dài quá giới hạn", "P2",
     "Cửa sổ Tạo mới đang mở",
     "1. Nhập Chủ tài khoản 300 ký tự\n2. Nhập đủ các ô còn lại, bấm Lưu",
     "Chủ tài khoản: chuỗi 300 ký tự",
     "- Không lưu sai lệch âm thầm; danh sách vẫn hiển thị được, ô tự xuống dòng"),

    (6, "Nhập ký tự đặc biệt vào số tài khoản", "P1",
     "Cửa sổ Tạo mới đang mở",
     "1. Nhập Số tài khoản có ký tự đặc biệt\n2. Nhập đủ các ô còn lại, bấm Lưu\n3. Xem danh sách",
     "Số tài khoản: QA-0005/TEST",
     "- Danh sách hiển thị đúng nguyên văn chuỗi đã nhập, không làm vỡ bố cục bảng"),

    (7, "Nhập ký tự chữ vào số tài khoản", "P2",
     "Cửa sổ Tạo mới đang mở",
     "1. Nhập Số tài khoản gồm cả chữ và số\n2. Lưu",
     "Số tài khoản: STK-QA-006",
     "- Lưu bình thường: ô Số tài khoản không giới hạn chỉ chữ số\n"
     "- Tìm nhanh theo chuỗi đó vẫn ra kết quả"),

    (8, "Dán nội dung từ nguồn khác", "P2",
     "Đã sao chép đoạn văn bản có định dạng từ tài liệu Word",
     "1. Dán vào ô Chủ tài khoản\n2. Bấm Lưu",
     "—",
     "- Chỉ phần chữ được nhận, không kèm định dạng, không làm hỏng cửa sổ nhập liệu"),

    (9, "Chọn chi nhánh không thuộc ngân hàng bằng cách gọi thẳng chức năng", "P0",
     "Ngân hàng A và chi nhánh của ngân hàng B",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Tạo mới, truyền ngân hàng A kèm chi nhánh "
     "của ngân hàng B",
     "Ngân hàng: A | Chi nhánh: của B",
     "- Hệ thống từ chối kèm thông báo \"Chi nhánh không thuộc ngân hàng đã chọn\"\n"
     "- ⚠️ Đây là ràng buộc được kiểm tra ở máy chủ, không chỉ lọc ở giao diện"),

    (10, "Chọn ngân hàng đang khóa bằng cách gọi thẳng chức năng", "P0",
     "Ngân hàng \"TRANG TEST 78\" đang bị khóa",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Tạo mới với ngân hàng đang khóa",
     "—",
     "- Hệ thống từ chối kèm thông báo \"Ngân hàng không tồn tại hoặc đã bị khóa\""),

    (11, "Chọn loại tiền tệ đang khóa bằng cách gọi thẳng chức năng", "P1",
     "Có loại tiền tệ đang bị khóa",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Tạo mới với loại tiền tệ đang khóa",
     "—",
     "- Hệ thống từ chối kèm thông báo \"Loại tiền tệ không tồn tại hoặc đã bị khóa\""),

    (12, "Truyền trạng thái không hợp lệ", "P2",
     "Trạng thái chỉ nhận Hoạt động hoặc Khóa",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Tạo mới với giá trị trạng thái lạ",
     "Trạng thái: 9",
     "- Hệ thống từ chối kèm thông báo \"Trạng thái không hợp lệ\""),
]

S7 = [
    (1, "Chỉ thấy tài khoản của công ty mình", "P0",
     "Người dùng A thuộc công ty 1; công ty 2 có tài khoản QA-CTY2",
     "1. Đăng nhập bằng người dùng A\n2. Vào màn hình danh sách\n"
     "3. Tìm QA-CTY2 bằng ô tìm nhanh",
     "Từ khoá: QA-CTY2",
     "- Danh sách không chứa QA-CTY2\n- Tìm kiếm cũng không ra kết quả nào"),

    (2, "Mở trực tiếp bản ghi của công ty khác", "P0",
     "Người dùng A thuộc công ty 1; biết định danh bản ghi QA-CTY2 của công ty 2",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xem chi tiết bản ghi QA-CTY2",
     "—",
     "- Hệ thống báo không tìm thấy tài khoản ngân hàng\n"
     "- ⚠️ Không được để lộ nội dung bản ghi của công ty khác"),

    (3, "Sửa bản ghi của công ty khác", "P0",
     "Người dùng A thuộc công ty 1; bản ghi QA-CTY2 thuộc công ty 2",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa cho bản ghi QA-CTY2",
     "—",
     "- Hệ thống báo không tìm thấy tài khoản ngân hàng\n- Dữ liệu công ty 2 không thay đổi"),

    (4, "Khóa bản ghi của công ty khác", "P1",
     "Người dùng A thuộc công ty 1; bản ghi QA-CTY2 đang Hoạt động",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Khóa cho bản ghi QA-CTY2",
     "—",
     "- Hệ thống báo không tìm thấy\n- Trạng thái bản ghi công ty 2 giữ nguyên"),

    (5, "Tài khoản mới tạo gắn đúng công ty người tạo", "P0",
     "Người dùng A thuộc công ty 1",
     "1. Đăng nhập bằng A, tạo tài khoản QA0007\n"
     "2. Đăng nhập bằng người dùng B thuộc công ty 2, tìm QA0007",
     "Số tài khoản: QA0007",
     "- Người dùng A thấy QA0007 trong danh sách\n- Người dùng B không thấy"),

    (6, "Người dùng chưa được gắn công ty", "P0",
     "Tài khoản đăng nhập có quyền nhưng hồ sơ nhân sự chưa gắn công ty",
     "1. Đăng nhập bằng tài khoản đó\n2. Vào màn hình danh sách\n3. Bấm Tạo mới, nhập đủ và Lưu",
     "—",
     "- Danh sách trống hoàn toàn (không phải danh sách của công ty khác)\n"
     "- Khi lưu: hệ thống báo \"Tài khoản đăng nhập chưa gắn công ty, không thể thao tác\"\n"
     "- ⚠️ Tuyệt đối không được tạo ra bản ghi không thuộc công ty nào"),

    (7, "Đổi công ty của người dùng rồi vào lại màn hình", "P2",
     "Người dùng A đang thuộc công ty 1, sau đó hồ sơ được chuyển sang công ty 2",
     "1. Ghi lại danh sách nhìn thấy khi ở công ty 1\n2. Chuyển hồ sơ sang công ty 2\n"
     "3. Đăng nhập lại và vào màn hình",
     "—",
     "- Danh sách đổi theo công ty mới, không còn tài khoản của công ty cũ"),
]

S8 = [
    (1, "Hai người cùng sửa một tài khoản", "P0",
     "Người A và người B cùng công ty, cùng mở cửa sổ Sửa của QA0001",
     "1. Người A đổi Chủ tài khoản rồi Lưu\n2. Người B (đang mở dữ liệu cũ) đổi Loại tiền tệ rồi "
     "Lưu\n3. Cả hai bấm Làm mới",
     "A: đổi chủ tài khoản | B: đổi loại tiền tệ",
     "- Ghi nhận kết quả thực tế: bản lưu sau ghi đè bản trước hay hệ thống cảnh báo\n"
     "- ⚠️ Kiểm cửa sổ Lịch sử: phải có đủ 2 mốc thay đổi của 2 người"),

    (2, "Khóa trong khi người khác đang mở cửa sổ Sửa", "P0",
     "Người A đang mở cửa sổ Sửa của QA0001",
     "1. Người B khóa QA0001 từ danh sách\n2. Người A bấm Lưu",
     "—",
     "- Người A nhận thông báo yêu cầu mở khoá trước khi cập nhật, dữ liệu không bị ghi\n"
     "- Màn hình không treo"),

    (3, "Bản ghi bị xoá trạng thái trong lúc thao tác", "P1",
     "Người A đang mở danh sách với dữ liệu cũ trên màn",
     "1. Người B khóa QA0001\n2. Người A (chưa làm mới) bấm nút Sửa của dòng QA0001",
     "—",
     "- Người A nhận thông báo \"Tài khoản ngân hàng đang bị khóa, không thể sửa\"\n"
     "- Không mở cửa sổ Sửa"),

    (4, "Hai người cùng tạo trùng số tài khoản", "P1",
     "Người A và người B cùng nhập số tài khoản QA0008",
     "1. Cả hai nhập cùng số tài khoản\n2. Cùng bấm Lưu gần như đồng thời",
     "Số tài khoản: QA0008",
     "- Chỉ một người lưu thành công, người còn lại nhận lỗi \"Số tài khoản đã tồn tại\"\n"
     "- Danh sách chỉ có 1 dòng QA0008"),

    (5, "Danh sách tự làm mới sau thao tác ghi", "P0",
     "Đang ở trang 1 với bộ lọc rỗng",
     "1. Tạo mới một tài khoản\n2. Không tải lại trang, quan sát danh sách",
     "Số tài khoản: QA0009",
     "- Danh sách tự cập nhật, hiện ngay tài khoản vừa tạo\n- Dòng thống kê tăng đúng 1"),

    (6, "Thao tác ghi khi mất kết nối", "P2",
     "Cửa sổ Tạo mới đã nhập đủ dữ liệu hợp lệ",
     "1. Ngắt kết nối mạng\n2. Bấm Lưu\n3. Nối lại mạng và bấm Lưu",
     "Số tài khoản: QA0010",
     "- Lần 1: hệ thống báo lỗi, cửa sổ không đóng, dữ liệu đã nhập còn nguyên\n"
     "- Lần 2: lưu thành công, chỉ tạo ra 1 bản ghi"),
]

S9 = [
    (1, "Mở cửa sổ Lịch sử từ danh sách", "P0",
     "Tài khoản QA0001 đã từng bị sửa và khóa",
     "1. Bấm nút Lịch sử ở dòng QA0001",
     "—",
     "- Cửa sổ tiêu đề \"Lịch sử thay đổi\", dòng phụ ghi \"Tài khoản ngân hàng: <số> - <chủ tài "
     "khoản>\"\n"
     "- Các mốc xếp mới nhất trước"),

    (2, "Nội dung một mốc lịch sử", "P0",
     "QA0001 vừa được đổi Chủ tài khoản",
     "1. Mở cửa sổ Lịch sử của QA0001\n2. Đọc mốc trên cùng",
     "—",
     "- Hiện ngày giờ, nhãn hành động (\"Thay đổi thông tin\"), tên người thực hiện kèm phòng ban\n"
     "- Dòng chi tiết dạng \"Chủ tài khoản: giá trị cũ → giá trị mới\""),

    (3, "Lịch sử ghi nhận việc tạo mới", "P0",
     "Vừa tạo tài khoản QA0011",
     "1. Tạo QA0011\n2. Mở cửa sổ Lịch sử của QA0011",
     "Số tài khoản: QA0011",
     "- Có đúng 1 mốc \"Tạo mới\" với người thực hiện là người vừa tạo"),

    (4, "Lịch sử ghi nhận từng trường thay đổi", "P0",
     "QA0011 vừa đổi Số tài khoản và Loại tiền tệ",
     "1. Sửa 2 ô trên rồi Lưu\n2. Mở cửa sổ Lịch sử",
     "Số tài khoản: QA0011B | Loại tiền tệ: AUD",
     "- Mốc \"Thay đổi thông tin\" liệt kê cả hai trường với giá trị cũ → giá trị mới\n"
     "- ⚠️ Loại tiền tệ hiển thị bằng TÊN tiền tệ, không phải con số"),

    (5, "Lịch sử ghi nhận đổi ngân hàng và chi nhánh", "P1",
     "QA0011 vừa đổi sang ngân hàng khác",
     "1. Sửa QA0011, đổi Ngân hàng và Chi nhánh, Lưu\n2. Mở cửa sổ Lịch sử",
     "—",
     "- Mốc thay đổi ghi rõ tên ngân hàng cũ → tên ngân hàng mới và chi nhánh cũ → chi nhánh mới"),

    (6, "Sửa mà không thay đổi gì", "P1",
     "QA0011 đã có lịch sử",
     "1. Bấm Sửa QA0011\n2. Không sửa ô nào\n3. Bấm Lưu\n4. Mở cửa sổ Lịch sử",
     "—",
     "- Vẫn báo cập nhật thành công\n"
     "- Cửa sổ Lịch sử KHÔNG phát sinh thêm mốc \"Thay đổi thông tin\""),

    (7, "Lọc lịch sử theo loại hoạt động", "P1",
     "Bản ghi có cả mốc Tạo mới, Thay đổi thông tin và Thay đổi trạng thái",
     "1. Mở cửa sổ Lịch sử\n2. Bấm nút Bộ lọc\n3. Chọn loại hoạt động \"Thay đổi trạng thái\"",
     "Loại hoạt động: Thay đổi trạng thái",
     "- Chỉ còn các mốc Khóa / Mở khóa\n"
     "- Danh sách loại hoạt động có đúng 3 nhóm: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái"),

    (8, "Lịch sử của bản ghi chưa từng thay đổi", "P1",
     "Tài khoản cũ chưa phát sinh thao tác nào từ khi có chức năng lịch sử",
     "1. Bấm nút Lịch sử ở dòng đó",
     "—",
     "- Hiển thị \"Chưa có lịch sử thao tác nào.\"\n- Không báo lỗi"),

    (9, "Khối Lịch sử trong cửa sổ Xem", "P0",
     "QA0011 đã có lịch sử",
     "1. Bấm số tài khoản QA0011\n2. Bấm nút Xem lịch sử ở cuối cửa sổ",
     "—",
     "- Khối Lịch sử mở ngay trong cửa sổ Xem\n"
     "- Nội dung giống hệt cửa sổ Lịch sử mở từ nút ngoài danh sách\n"
     "- Có nút Làm mới và nút Thu gọn"),

    (10, "Luồng đầy đủ: tạo → sửa → khóa → mở khóa", "P0",
     "Danh mục chưa có số tài khoản QA0020",
     "1. Tạo tài khoản QA0020 với đủ 5 ô bắt buộc\n2. Sửa Chủ tài khoản\n3. Khóa QA0020\n"
     "4. Mở khóa QA0020\n5. Mở cửa sổ Lịch sử và đối chiếu",
     "Số tài khoản: QA0020 | Chủ tài khoản: Kiểm thử luồng",
     "- Mỗi bước có thông báo thành công tương ứng và danh sách cập nhật ngay\n"
     "- Cửa sổ Lịch sử có đủ 4 mốc theo đúng thứ tự: Tạo mới, Thay đổi thông tin, Khóa, Mở khóa"),

    (11, "Dữ liệu vừa tạo dùng được ngay ở nghiệp vụ khác", "P0",
     "Vừa tạo tài khoản QA0021 trạng thái Hoạt động",
     "1. Tạo QA0021\n2. Vào một màn nghiệp vụ có chọn tài khoản ngân hàng của công ty\n"
     "3. Mở ô chọn và tìm QA0021",
     "Số tài khoản: QA0021",
     "- QA0021 có trong danh sách chọn của màn nghiệp vụ"),

    (12, "Dọn dữ liệu sau khi test", "P1",
     "Đã tạo các tài khoản QA0001 … QA0021 trong quá trình test",
     "1. Lọc theo từ khoá QA\n2. Khóa toàn bộ tài khoản kiểm thử\n3. Báo quản trị dọn dữ liệu test",
     "Từ khoá: QA",
     "- ⚠️ Màn hình KHÔNG có chức năng Xóa nên dữ liệu test chỉ khóa được, không xoá được\n"
     "- Ghi lại danh sách số tài khoản đã tạo để bộ phận kỹ thuật dọn ở cơ sở dữ liệu"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "TẠO MỚI / SỬA / XEM TÀI KHOẢN", S4),
    ("V", "KHÓA / MỞ KHÓA", S5),
    ("VI", "RÀNG BUỘC NHẬP LIỆU", S6),
    ("VII", "PHẠM VI DỮ LIỆU THEO CÔNG TY", S7),
    ("VIII", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S8),
    ("IX", "LỊCH SỬ THAY ĐỔI & LUỒNG TỔNG THỂ", S9),
]

build(output_file=OUT,
      sheet_name="Trang tính1",
      feature_name="Danh mục tài khoản ngân hàng - Cập nhật ngày 17/08/2026",
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
