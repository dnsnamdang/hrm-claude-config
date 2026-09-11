# -*- coding: utf-8 -*-
"""Sinh tai lieu HDSD (.docx) cho man "Phieu de nghi thanh toan" (phan he Tai chinh).

Khung + style lay tu `.claude/skills/hdsd-documenter/assets/HDSD_MAU.docx`
(ban HDSD Danh muc khach hang — man mau user chi dinh).

Anh that: dntt_chi_shots/ (cong dev hrm-crm.eteksofts.com, 28/08/2026) — KHONG commit.

Chay:  python .plans/gop-db/finance-bill-payment-request/gen_hdsd.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "hdsd-documenter", "assets"))
from hdsd_engine import HdsdBuilder  # noqa: E402

OUT = os.path.join(HERE, "HDSD_Phiếu đề nghị thanh toán.docx")
SHOTS = os.path.join(HERE, "dntt_chi_shots")

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title="(Màn hình: Phiếu đề nghị thanh toán)",
                doc_title="HDSD - Phiếu đề nghị thanh toán")

# ══════════════════════════════════════════════════════════ TỔNG QUAN
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ và từ viết tắt")
b.table([
    ["Thuật ngữ", "Giải thích"],
    ["Phiếu đề nghị thanh toán",
     "Chứng từ đề nghị chi tiền, do bộ phận kinh doanh lập và phải đi qua luồng duyệt nhiều cấp "
     "trước khi kế toán lập phiếu chi hoặc giấy ủy nhiệm chi."],
    ["Loại chi",
     "Phân loại khoản chi. Bốn giá trị chọn được: Chi trả nhà cung cấp · Chi trả lại khách hàng · "
     "Chi thưởng thực hiện hợp đồng · Thanh toán chi phí vận chuyển NCC."],
    ["Hình thức thanh toán",
     "TM là tiền mặt, CK là chuyển khoản. Hình thức quyết định việc chọn đối tượng nhận tiền một "
     "lần cho cả phiếu (chuyển khoản) hay theo từng dòng chi tiết (tiền mặt), và quyết định có "
     "khối Thông tin ngân hàng hay không."],
    ["Dòng chi tiết",
     "Một dòng trong bảng Chi tiết. Nội dung cột đổi theo loại chi: hợp đồng mua, hợp đồng bán "
     "hoặc chuyến xe."],
    ["Số tiền đề nghị chi", "Số tiền người lập phiếu đề nghị chi trên dòng đó."],
    ["TP duyệt", "Số tiền cấp Trưởng phòng chấp thuận cho dòng chi tiết đó."],
    ["KT công nợ duyệt", "Số tiền cấp Kế toán công nợ chấp thuận."],
    ["KT trưởng / BGĐ duyệt",
     "Số tiền cấp Kế toán trưởng hoặc Ban giám đốc chấp thuận — hai cấp này dùng chung một cột."],
    ["Số tiền chi",
     "Số tiền thực chi, lấy từ phiếu chi hoặc giấy ủy nhiệm chi lập từ phiếu đề nghị này. Chưa "
     "có chứng từ chi thì hiển thị dấu gạch dưới."],
    ["Đang tạo", "Phiếu nháp; chỉ người lập nhìn thấy, sửa và xóa được."],
    ["Chờ TP duyệt", "Phiếu đã gửi, đang chờ Trưởng phòng của phòng ban người lập xử lý."],
    ["Chờ kế toán công nợ duyệt", "Đã qua Trưởng phòng, đang chờ Kế toán công nợ."],
    ["Chờ kế toán trưởng duyệt", "Đã qua Kế toán công nợ, đang chờ Kế toán trưởng."],
    ["Chờ ban giám đốc duyệt", "Kế toán trưởng đã chuyển lên Ban giám đốc."],
    ["Chờ tạo phiếu chi", "Đã duyệt xong, đang chờ kế toán thanh toán lập chứng từ chi."],
    ["Không duyệt",
     "Bị một cấp từ chối (từ Kế toán công nợ trở lên). Người lập sửa lại và gửi lại được."],
    ["Chờ duyệt phiếu chi / Duyệt phiếu chi / Đã hủy",
     "Ba trạng thái do màn Phiếu chi và Ủy nhiệm chi đặt; màn này chỉ hiển thị."],
])

b.h2("2. Cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Nội dung", "Người thực hiện"],
    ["1.0", "28/08/2026",
     "Ban hành lần đầu cho màn Phiếu đề nghị thanh toán (đủ 4 chế độ xem, 4 loại chi và luồng "
     "duyệt 5 cấp).", "Nhóm phát triển HRM"],
])

b.h2("3. Giới thiệu chung")
b.para("Màn hình Phiếu đề nghị thanh toán dùng để lập và xử lý các đề nghị chi tiền giữa bộ phận "
       "kinh doanh và bộ phận kế toán. Người kinh doanh lập phiếu ghi rõ chi cho ai, theo hợp "
       "đồng hoặc chuyến xe nào, bao nhiêu tiền, vì việc gì. Phiếu sau đó đi qua tối đa 4 cấp "
       "duyệt (Trưởng phòng → Kế toán công nợ → Kế toán trưởng → Ban giám đốc) rồi dừng ở trạng "
       "thái Chờ tạo phiếu chi để kế toán thanh toán lập chứng từ chi.")
b.para("Màn hình nằm trong phân hệ Tài chính, có bốn chế độ xem trên cùng một giao diện:")
b.bullet("Tất cả — đường dẫn /finance/bill-payment-requests (mặc định). Vào từ menu Khởi tạo "
         "phiếu yêu cầu - Công nợ - Thu - Chi → Đề nghị thanh toán, hoặc menu Đề nghị → "
         "Đề nghị thanh toán.")
b.bullet("Chờ duyệt — đường dẫn /finance/bill-payment-requests?mode=pending. Vào từ menu "
         "Phê duyệt - Công nợ - Thu - Chi → Phiếu đề nghị thanh toán chờ duyệt.")
b.bullet("Của tôi — đường dẫn /finance/bill-payment-requests?mode=mine. Không có mục menu, gõ "
         "thẳng đường dẫn.")
b.bullet("Đã duyệt — đường dẫn /finance/bill-payment-requests?mode=approved. Không có mục menu, "
         "gõ thẳng đường dẫn.")
b.para("Các màn con: thêm mới /finance/bill-payment-requests/create, xem chi tiết "
       "/finance/bill-payment-requests/{số hiệu bản ghi}, chỉnh sửa "
       "/finance/bill-payment-requests/{số hiệu bản ghi}/edit, bản in "
       "/finance/bill-payment-requests/{số hiệu bản ghi}/print.")

b.h2("4. Quyền và phạm vi dữ liệu")
b.para("Màn hình gắn với 10 quyền, chia làm hai nhóm: bốn quyền quyết định NHÌN THẤY phiếu của "
       "ai, sáu quyền còn lại quyết định vai trò trong luồng duyệt.")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / mục tương ứng trên giao diện"],
    ["Xem tất cả phiếu đề nghị thanh toán của tổng công ty",
     "Ở chế độ Tất cả: nhìn thấy phiếu của mọi công ty.",
     "Bộ lọc nâng cao hiện thêm ô Công ty, Phòng ban, Bộ phận."],
    ["Xem tất cả phiếu đề nghị thanh toán của công ty",
     "Ở chế độ Tất cả: nhìn thấy phiếu thuộc công ty mình.",
     "Bộ lọc nâng cao hiện ô Phòng ban."],
    ["Xem tất cả phiếu đề nghị thanh toán của phòng ban",
     "Ở chế độ Tất cả: nhìn thấy phiếu thuộc các phòng ban mình được giao quản lý.",
     "Bộ lọc nâng cao hiện ô Phòng ban."],
    ["Xem tất cả phiếu đề nghị thanh toán của bộ phận",
     "Ở chế độ Tất cả: nhìn thấy phiếu thuộc các bộ phận mình được giao quản lý.",
     "Bộ lọc nâng cao hiện ô Bộ phận."],
    ["Trưởng phòng duyệt đề nghị thanh toán",
     "Duyệt hoặc từ chối phiếu đang ở Chờ TP duyệt, thuộc phòng ban mình quản lý.",
     "Phiếu xuất hiện ở chế độ Chờ duyệt; màn chi tiết có nút Duyệt và Từ chối."],
    ["Kế toán công nợ duyệt đề nghị thanh toán",
     "Duyệt hoặc từ chối phiếu đang ở Chờ kế toán công nợ duyệt, trong công ty mình.",
     "Phiếu xuất hiện ở chế độ Chờ duyệt; màn chi tiết có nút Duyệt và Từ chối."],
    ["Kế toán trưởng duyệt đề nghi thanh toán",
     "Duyệt thẳng hoặc chuyển lên Ban giám đốc, hoặc từ chối phiếu đang ở Chờ kế toán trưởng "
     "duyệt.",
     "Màn chi tiết có hai nút Duyệt và Chuyển duyệt BGĐ, cùng nút Từ chối."],
    ["Ban giám đốc duyệt đề nghi thanh toán",
     "Duyệt hoặc từ chối phiếu đang ở Chờ ban giám đốc duyệt.",
     "Màn chi tiết có nút Duyệt và Từ chối."],
    ["Kế toán thanh toán",
     "Xử lý phiếu đã duyệt xong: lập phiếu chi (hình thức tiền mặt) hoặc giấy ủy nhiệm chi "
     "(hình thức chuyển khoản).",
     "Phiếu ở Chờ tạo phiếu chi xuất hiện ở chế độ Chờ duyệt; có nút Tạo phiếu chi hoặc "
     "Tạo ủy nhiệm chi."],
    ["Kinh doanh đề nghị thanh toán",
     "Không mở thêm chức năng nào trên màn; dùng để xác định nhóm người nhận thông báo khi phiếu "
     "bị từ chối.",
     "Không có nút riêng."],
])
b.para("Lưu ý về tên quyền: hai quyền của cấp Kế toán trưởng và Ban giám đốc trong hệ thống được "
       "ghi là “duyệt đề nghi thanh toán” (thiếu dấu). Đây là tên gốc của hệ thống cũ, cố ý giữ "
       "nguyên để đối chiếu dữ liệu — không phải lỗi cần sửa.")
b.para("Người dùng không có quyền nào trong bốn quyền xem vẫn vào được màn hình nhưng chỉ nhìn "
       "thấy phiếu do chính mình lập. Việc lập phiếu không gắn quyền: ai vào được màn cũng lập "
       "được phiếu của mình. Sửa và xóa chỉ áp cho phiếu do chính mình lập, khi phiếu còn ở "
       "trạng thái Đang tạo hoặc Không duyệt.")
b.para("Nếu không giữ vai duyệt nào, chế độ Chờ duyệt vẫn mở được nhưng danh sách rỗng.")

# ══════════════════════════════════════════════════════════ PHẦN 1
b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

b.h2("1.1. Cách vào màn hình")
b.para("Bước 1: Đăng nhập hệ thống. Bước 2: Chọn phân hệ Tài chính ở góc trên bên trái. "
       "Bước 3: Ở thanh menu bên trái, bấm nhóm Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi, "
       "sau đó bấm Đề nghị thanh toán. Có thể vào cùng màn này bằng nhóm menu Đề nghị → "
       "Đề nghị thanh toán.")
b.para("Người giữ vai duyệt vào nhóm menu Phê duyệt - Công nợ - Thu - Chi → Phiếu đề nghị thanh "
       "toán chờ duyệt để xử lý phiếu.")

b.h2("1.2. Bố cục chung")
b.image("01-danh-sach.png", "Màn hình danh sách Phiếu đề nghị thanh toán")
b.para("Màn hình chia làm hai khối:")
b.bullet("Khối Bộ lọc danh sách ở trên: ô tìm nhanh theo mã phiếu, nút Tìm kiếm, nút Làm mới, "
         "nút Cài đặt bộ lọc và nút Tìm kiếm nâng cao.")
b.bullet("Khối bảng danh sách ở dưới: tiêu đề bảng, nút Tạo mới, nút Cấu hình cột hiển thị "
         "(biểu tượng hai cột), bảng dữ liệu và thanh phân trang.")

# ══════════════════════════════════════════════════════════ PHẦN 2
b.h1("PHẦN 2: DANH SÁCH VÀ BỐN CHẾ ĐỘ XEM")

b.h2("2.1. Bốn chế độ xem")
b.table([
    ["Chế độ", "Đường dẫn", "Hiển thị phiếu nào", "Khác biệt trên giao diện"],
    ["Tất cả", "/finance/bill-payment-requests",
     "Phiếu trong phạm vi quyền xem của người dùng; phiếu nháp của người khác luôn bị ẩn.",
     "Có nút Tạo mới. Tiêu đề: Phiếu đề nghị thanh toán."],
    ["Của tôi", "/finance/bill-payment-requests?mode=mine",
     "Mọi phiếu do chính mình lập, kể cả phiếu nháp.",
     "Có nút Tạo mới. Tiêu đề: Phiếu đề nghị thanh toán của tôi."],
    ["Chờ duyệt", "/finance/bill-payment-requests?mode=pending",
     "Phiếu trong công ty mình và đang ở đúng trạng thái mà mình có quyền duyệt.",
     "Không có nút Tạo mới. Tiêu đề: Phiếu đề nghị thanh toán chờ duyệt."],
    ["Đã duyệt", "/finance/bill-payment-requests?mode=approved",
     "Phiếu mà chính mình đã duyệt ở bất kỳ cấp nào.",
     "Không có nút Tạo mới. Tiêu đề: Phiếu đề nghị thanh toán đã duyệt."],
])
b.image("06-cho-duyet.png", "Chế độ Chờ duyệt — không có nút Tạo mới")
b.image("26-cua-toi.png", "Chế độ Của tôi")
b.para("Bốn chế độ dùng chung bộ cột và bộ tiêu chí lọc. Riêng giá trị đang lọc thì mỗi chế độ "
       "ghi nhớ riêng: lọc ở chế độ Tất cả không kéo theo sang chế độ Chờ duyệt.")

b.h2("2.2. Phân quyền và hướng dẫn theo quyền")
b.para("Trước khi làm theo các mục sau, hãy xác định mình thuộc nhóm nào — nội dung nhìn thấy "
       "trên cùng một màn hình khác nhau rất nhiều.")
b.h3("2.2.1. Người lập phiếu (không giữ vai duyệt nào)")
b.para("Ở chế độ Tất cả chỉ thấy phiếu trong phạm vi quyền xem của mình; nếu không có quyền xem "
       "nào thì chỉ thấy phiếu do chính mình lập. Có nút Tạo mới, sửa và xóa được phiếu của mình "
       "khi phiếu còn ở trạng thái Đang tạo hoặc Không duyệt. Chế độ Chờ duyệt mở được nhưng "
       "danh sách rỗng.")
b.h3("2.2.2. Người dùng có quyền “Trưởng phòng duyệt đề nghị thanh toán”")
b.para("Chế độ Chờ duyệt hiển thị các phiếu đang ở trạng thái Chờ TP duyệt VÀ thuộc phòng ban mà "
       "người dùng được giao quản lý, trong công ty của mình. Phiếu Chờ TP duyệt của phòng ban "
       "khác không hiện. Ở màn chi tiết có nút Duyệt và nút Từ chối.")
b.h3("2.2.3. Người dùng có quyền “Kế toán công nợ duyệt đề nghị thanh toán”")
b.para("Chế độ Chờ duyệt hiển thị các phiếu đang ở Chờ kế toán công nợ duyệt trong công ty mình. "
       "Cấp này không bị giới hạn theo phòng ban. Ở màn chi tiết có nút Duyệt và Từ chối.")
b.h3("2.2.4. Người dùng có quyền “Kế toán trưởng duyệt đề nghi thanh toán”")
b.para("Chế độ Chờ duyệt hiển thị các phiếu đang ở Chờ kế toán trưởng duyệt trong công ty mình. "
       "Màn chi tiết có HAI nút duyệt: Duyệt (đưa phiếu thẳng sang Chờ tạo phiếu chi) và "
       "Chuyển duyệt BGĐ (đưa phiếu sang Chờ ban giám đốc duyệt), cùng nút Từ chối.")
b.h3("2.2.5. Người dùng có quyền “Ban giám đốc duyệt đề nghi thanh toán”")
b.para("Chế độ Chờ duyệt hiển thị các phiếu đang ở Chờ ban giám đốc duyệt. Màn chi tiết có nút "
       "Duyệt và nút Từ chối.")
b.h3("2.2.6. Người dùng có quyền “Kế toán thanh toán”")
b.para("Chế độ Chờ duyệt hiển thị các phiếu đang ở Chờ tạo phiếu chi. Với phiếu hình thức tiền "
       "mặt có nút Tạo phiếu chi; với phiếu hình thức chuyển khoản có nút Tạo ủy nhiệm chi. Hai "
       "nút này loại trừ nhau.")
b.para("Lưu ý chung: người giữ nhiều vai duyệt sẽ thấy phiếu của tất cả các vai đó trong cùng "
       "danh sách Chờ duyệt; mở từng phiếu thì nút duyệt hiện đúng theo trạng thái của phiếu.")

b.h2("2.3. Tìm kiếm nhanh")
b.para("Ô Tìm theo mã phiếu ở đầu màn hình tìm theo mã phiếu. Gõ một phần mã rồi bấm nút "
       "Tìm kiếm. Đây là ô duy nhất phải bấm nút mới lọc; mọi tiêu chí trong Tìm kiếm nâng cao "
       "lọc ngay khi vừa đổi giá trị.")
b.para("Nút Làm mới xóa sạch mọi tiêu chí đang lọc, kể cả ô tìm nhanh, và tải lại danh sách từ "
       "trang 1.")

b.h2("2.4. Bộ lọc nâng cao")
b.para("Bấm nút Tìm kiếm nâng cao để mở khối tiêu chí; bấm lại (nút đổi tên thành Ẩn tìm kiếm "
       "nâng cao) để thu gọn.")
b.image("02-bo-loc.png", "Bộ lọc nâng cao ở trạng thái mở đầy đủ tiêu chí")
b.table([
    ["Tiêu chí", "Kiểu nhập", "Cách dùng"],
    ["Công ty", "Danh sách chọn",
     "Chỉ hiện với người có quyền xem tổng công ty. Đổi công ty thì ô Phòng ban và Bộ phận tự "
     "xóa giá trị cũ."],
    ["Phòng ban", "Danh sách chọn", "Chỉ liệt kê phòng ban thuộc công ty đang chọn."],
    ["Bộ phận", "Danh sách chọn", "Chỉ hiện với người có quyền xem theo cấp bộ phận."],
    ["Loại chi", "Danh sách chọn", "Bốn giá trị đang dùng."],
    ["Hình thức thanh toán", "Danh sách chọn", "Hai giá trị: TM (tiền mặt) và CK (chuyển khoản)."],
    ["Trạng thái", "Danh sách chọn", "Mười giá trị, xem bảng thuật ngữ ở đầu tài liệu."],
    ["Lý do chi", "Ô gõ tay", "Tìm theo một phần nội dung lý do chi."],
    ["Khách hàng", "Danh sách chọn có tìm kiếm",
     "Gõ từ 2 ký tự để hệ thống gợi ý. Ô này chỉ tìm KHÁCH HÀNG — gõ tên nhà cung cấp sẽ không "
     "ra kết quả."],
    ["Nhà cung cấp", "Danh sách chọn có tìm kiếm", "Gõ từ 2 ký tự để hệ thống gợi ý."],
    ["Người lập", "Danh sách chọn", "Chọn nhân sự đã lập phiếu."],
    ["Số tiền đề nghị từ / đến", "Hai ô số tiền",
     "So sánh trên TỔNG tiền đề nghị chi (đã quy đổi) của cả phiếu. Bỏ trống một đầu thì phía đó "
     "không giới hạn."],
    ["Ngày lập từ / đến", "Hai ô chọn ngày",
     "Lọc theo ngày lập phiếu, không phải Ngày nhận. Cả hai mốc lấy trọn ngày."],
])

b.h2("2.5. Cài đặt bộ lọc (chọn tiêu chí muốn hiển thị)")
b.para("Nút Cài đặt bộ lọc mở cửa sổ cho phép bật/tắt và sắp xếp lại các tiêu chí lọc. Cấu hình "
       "này lưu riêng cho từng tài khoản và từng màn hình.")
b.image("03-cai-dat-bo-loc.png", "Cửa sổ Cài đặt bộ lọc với đủ 10 tiêu chí")
b.bullet("Tích hoặc bỏ tích ô vuông trước tên tiêu chí để hiện hoặc ẩn tiêu chí đó.")
b.bullet("Kéo biểu tượng sáu chấm để đổi thứ tự tiêu chí.")
b.bullet("Bấm Lưu để ghi nhận; hệ thống báo Cập nhật thành công và bộ lọc đổi ngay.")
b.bullet("Bấm Khôi phục mặc định để bật lại đủ 10 tiêu chí theo thiết kế, sau đó vẫn phải bấm Lưu.")
b.bullet("Bấm Đóng để thoát mà không lưu.")
b.para("Lưu ý: bỏ tích một tiêu chí thì giá trị đang lọc của tiêu chí đó cũng bị xóa, danh sách "
       "không bị lọc ngầm bởi ô không nhìn thấy.")

b.h2("2.6. Các cột của danh sách")
b.image("05-danh-sach-hanh-dong.png", "Phần bên phải của bảng: Trạng thái và cột Hành động")
b.table([
    ["Cột", "Ý nghĩa"],
    ["STT", "Số thứ tự, chạy liên tục qua các trang. Cột bắt buộc, không ẩn được."],
    ["Mã phiếu",
     "Mã hệ thống tự sinh theo dạng <mã công ty>.DNTT<tháng năm>.<5 chữ số>. Bấm vào mã để mở "
     "màn chi tiết. Sắp xếp được. Cột bắt buộc."],
    ["Loại chi", "Một trong bốn loại chi đang dùng (phiếu cũ có thể mang loại đã ngừng dùng)."],
    ["Hình thức TT", "TM hoặc CK."],
    ["Khách hàng / Nhà cung cấp",
     "Đối tượng nhận tiền. Nội dung đổi theo loại chi và hình thức thanh toán; với loại "
     "Chi thưởng thực hiện hợp đồng + tiền mặt thì cột này để trống. Sắp xếp được."],
    ["Lý do chi", "Nội dung người lập nhập ở ô Lý do chi."],
    ["Số tiền",
     "Số tiền của cấp duyệt gần nhất đã ghi (chưa qua cấp nào thì là số đề nghị), kèm mã loại "
     "tiền của phiếu."],
    ["Ngày lập", "Ngày giờ lập phiếu. Sắp xếp được."],
    ["Ngày nhận", "Ngày giờ Trưởng phòng duyệt phiếu."],
    ["Người lập", "Người đã lập phiếu."],
    ["Phòng ban", "Phòng ban của người lập tại thời điểm lập phiếu."],
    ["Người cập nhật", "Người sửa hoặc xử lý phiếu gần nhất."],
    ["Ngày cập nhật", "Ngày giờ cập nhật gần nhất. Sắp xếp được."],
    ["Trạng thái",
     "Một trong mười trạng thái. Chỉ Duyệt phiếu chi hiện nền xanh; các trạng thái còn lại nền "
     "đỏ. Sắp xếp được."],
    ["Hành động", "Các nút thao tác của dòng. Cột bắt buộc."],
])

b.h2("2.7. Tuỳ chỉnh cột hiển thị")
b.para("Bấm nút biểu tượng hai cột bên phải nút Tạo mới để mở cửa sổ Tuỳ chỉnh cột.")
b.image("04-cau-hinh-cot.png", "Cửa sổ Tuỳ chỉnh cột")
b.bullet("Bỏ tích một cột để ẩn cột đó khỏi bảng.")
b.bullet("Kéo biểu tượng ba gạch để đổi thứ tự cột.")
b.bullet("Ba cột STT, Mã phiếu và Hành động bị khóa, không ẩn và không đổi vị trí được.")
b.bullet("Bấm Lưu để ghi nhận, bấm Đóng để thoát mà không lưu.")
b.para("Cấu hình cột lưu riêng cho từng tài khoản và dùng chung cho CẢ BỐN chế độ xem.")

b.h2("2.8. Sắp xếp và phân trang")
b.para("Bấm vào tiêu đề các cột có biểu tượng mũi tên (Mã phiếu, Khách hàng / Nhà cung cấp, "
       "Ngày lập, Ngày cập nhật, Trạng thái) để sắp xếp; bấm lần nữa để đảo chiều. Mỗi lần sắp "
       "xếp, danh sách quay về trang 1. Mặc định khi mới vào màn, phiếu lập gần nhất đứng đầu.")
b.para("Dưới bảng có dòng đếm dạng “Hiển thị 1–10 / 4037”: hai số đầu là khoảng dòng của trang "
       "đang xem, số cuối là tổng số phiếu khớp bộ lọc của chế độ đang xem. Ô Số dòng/trang cho "
       "phép đổi số dòng mỗi trang; đổi xong danh sách quay về trang 1.")
b.para("Hệ thống ghi nhớ bộ lọc trong 10 phút: bấm vào một phiếu rồi quay lại, các tiêu chí vừa "
       "đặt vẫn còn. Muốn bắt đầu lại từ đầu thì bấm Làm mới.")

b.h2("2.9. Các nút thao tác trên từng dòng")
b.para("Cột Hành động hiển thị tối đa ba nút; các thao tác còn lại nằm trong nút ba chấm.")
b.image("28-menu-hanh-dong-nhap.png", "Nút ba chấm ở một phiếu nháp: Xuất Excel, Xóa, Lịch sử")
b.image("07-menu-hanh-dong.png", "Nút ba chấm ở một phiếu đang chờ duyệt: Xuất Excel, Lịch sử")
b.table([
    ["Nút", "Tác dụng", "Điều kiện hiển thị"],
    ["Sửa (biểu tượng bút chì)", "Mở màn chỉnh sửa phiếu.",
     "Phiếu do chính người đăng nhập lập và đang ở trạng thái Đang tạo hoặc Không duyệt."],
    ["Duyệt (biểu tượng dấu tích)",
     "Mở màn chi tiết của phiếu để xem và sửa số tiền trước khi duyệt.",
     "Người dùng có quyền duyệt ở đúng trạng thái hiện tại của phiếu."],
    ["Tạo phiếu chi", "Chuyển sang màn lập Phiếu chi, gắn sẵn phiếu đề nghị này.",
     "Người dùng có quyền Kế toán thanh toán, phiếu ở Chờ tạo phiếu chi, hình thức tiền mặt và "
     "chưa có chứng từ chi."],
    ["Tạo ủy nhiệm chi", "Chuyển sang màn lập Giấy ủy nhiệm chi.",
     "Như trên nhưng hình thức chuyển khoản."],
    ["In phiếu (biểu tượng máy in)", "Mở bản in của phiếu ở tab mới.", "Luôn hiển thị."],
    ["Xuất Excel (trong nút ba chấm)", "Tải file Excel của phiếu.", "Luôn hiển thị."],
    ["Xóa (trong nút ba chấm)", "Xóa hẳn phiếu.", "Cùng điều kiện với nút Sửa."],
    ["Lịch sử (trong nút ba chấm)", "Mở cửa sổ Lịch sử thay đổi của phiếu.", "Luôn hiển thị."],
])
b.para("Màn hình không có nút Xem chi tiết riêng — bấm vào mã phiếu ở cột Mã phiếu để mở chi "
       "tiết; bấm chuột phải để mở ở tab mới. Nút Từ chối cũng không có ở danh sách vì thao tác "
       "đó bắt buộc nhập ghi chú, chỉ đặt ở màn chi tiết.")

# ══════════════════════════════════════════════════════════ PHẦN 3
b.h1("PHẦN 3: LẬP PHIẾU ĐỀ NGHỊ THANH TOÁN")

b.h2("3.1. Mở màn lập phiếu")
b.para("Ở màn danh sách (chế độ Tất cả hoặc Của tôi), bấm nút Tạo mới trên thanh công cụ của "
       "bảng. Hệ thống mở màn Thêm phiếu đề nghị thanh toán.")
b.image("14-tao-moi.png", "Màn lập phiếu khi vừa mở")
b.para("Màn hình gồm các khối: Thông tin chung, Thông tin ngân hàng (chỉ với hình thức chuyển "
       "khoản), Chi tiết và File đính kèm; thanh nút Lưu nháp, Lưu và gửi duyệt, Quay lại nằm "
       "cố định ở đáy màn hình.")

b.h2("3.2. Khối Thông tin chung — từng trường nhập")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn khi tạo mới", "Ghi chú"],
    ["Loại chi", "Danh sách chọn", "Có", "Chi trả nhà cung cấp",
     "Bốn giá trị. Quyết định cột của bảng Chi tiết và nguồn hợp đồng."],
    ["Hình thức thanh toán", "Danh sách chọn", "Có", "TM",
     "TM chọn đối tượng theo từng dòng; CK chọn đối tượng một lần và hiện khối ngân hàng."],
    ["Loại tiền", "Danh sách chọn", "Có", "VNĐ — VietNamDong",
     "Hiển thị dạng mã — tên; đổi loại tiền sẽ tự điền tỷ giá tương ứng."],
    ["Tỷ giá (VND)", "Ô số tiền", "Có", "1 (ô bị khóa)",
     "Ô mở khóa khi loại tiền khác VNĐ. Phải lớn hơn 0."],
    ["Đến ngày", "Ô chọn ngày", "Có (chỉ với loại vận chuyển)", "Trống",
     "Chỉ hiện với loại chi Thanh toán chi phí vận chuyển NCC; là mốc để lấy chuyến xe."],
    ["Người tạo", "Ô chữ", "—", "Tên người đang đăng nhập", "Chỉ để xem, không sửa được."],
    ["Phòng ban", "Ô chữ", "—", "Phòng ban của người đang đăng nhập",
     "Chỉ để xem, không sửa được."],
    ["Khách hàng / Nhà cung cấp", "Ô chọn qua cửa sổ", "Có (khi hình thức là CK)", "Trống",
     "Nhãn đổi theo loại chi. Bấm vào ô để mở cửa sổ chọn. Loại vận chuyển luôn có ô Nhà cung "
     "cấp kể cả hình thức tiền mặt."],
    ["Lý do chi", "Ô gõ tay", "Có", "Trống",
     "Bắt buộc ở CẢ hai nút lưu — kể cả Lưu nháp."],
])
b.para("Giá trị điền sẵn khi tạo mới: Loại chi = Chi trả nhà cung cấp; Hình thức thanh toán = TM; "
       "Loại tiền = VNĐ — VietNamDong; Tỷ giá (VND) = 1 và bị khóa; Người tạo và Phòng ban lấy "
       "theo người đang đăng nhập; Lý do chi để trống; bảng Chi tiết và khối File đính kèm rỗng. "
       "Màn lập phiếu KHÔNG có ô Mã phiếu — mã sinh tự động khi lưu.")

b.h2("3.3. Đổi Loại chi và Hình thức thanh toán")
b.para("Đổi Loại chi khi bảng Chi tiết đã có dòng sẽ xóa hết các dòng đó và xóa cả đối tượng đã "
       "chọn. Hệ thống hỏi lại trước khi xóa.")
b.image("23-xac-nhan-doi-loai-chi.png", "Hộp thoại xác nhận khi đổi Loại chi")
b.bullet("Bấm Xác nhận: toàn bộ dòng chi tiết và ô đối tượng bị xóa; tiêu đề cột của bảng Chi "
         "tiết đổi theo loại chi mới.")
b.bullet("Bấm Hủy: mọi thứ giữ nguyên.")
b.para("Đổi Hình thức thanh toán sang CK: khối Thông tin chung hiện thêm ô chọn đối tượng nhận "
       "tiền, xuất hiện khối Thông tin ngân hàng, và bảng Chi tiết BỎ cột đối tượng theo dòng. "
       "Đổi ngược lại về TM thì khối ngân hàng biến mất và bảng Chi tiết hiện lại cột đối tượng.")
b.image("15-tao-moi-ck.png", "Hình thức chuyển khoản: có ô Nhà cung cấp và khối Thông tin ngân hàng")

b.h2("3.4. Bảng Chi tiết theo từng loại chi")
b.para("Cột của bảng Chi tiết đổi theo loại chi và hình thức thanh toán:")
b.table([
    ["Loại chi", "Cột đối tượng (chỉ với hình thức TM)", "Cột hợp đồng", "Cột công nợ"],
    ["Chi trả nhà cung cấp", "Nhà cung cấp", "Số hợp đồng nhập mua", "Số tiền còn nợ"],
    ["Chi trả lại khách hàng", "Khách hàng", "Hợp đồng", "Công nợ còn lại"],
    ["Chi thưởng thực hiện hợp đồng", "Không có", "Số đơn hàng/Hợp đồng", "Số tiền còn lại"],
    ["Thanh toán chi phí vận chuyển NCC", "Không có",
     "Không có — thay bằng nhóm cột Số chuyến xe, Hạch toán, Tổng cước, Đã thanh toán",
     "Số tiền còn lại"],
])
b.image("31-tao-moi-loai2.png", "Bảng Chi tiết của loại Chi trả lại khách hàng, hình thức tiền mặt")

b.h3("3.4.1. Thêm một dòng")
b.para("Bấm dấu cộng ở góc phải hàng tiêu đề của bảng Chi tiết. Một dòng trống được thêm vào với "
       "số thứ tự tăng dần. Ô hợp đồng bị khóa cho tới khi dòng đã có đối tượng (với các loại "
       "chi cần chọn đối tượng theo dòng).")

b.h3("3.4.2. Chọn đối tượng cho dòng")
b.para("Bấm thẳng vào ô đối tượng của dòng, cửa sổ chọn mở ra. Với nhà cung cấp là cửa sổ "
       "Chọn nhà cung cấp; với khách hàng là cửa sổ Chọn khách hàng.")
b.image("16-popup-ncc.png", "Cửa sổ Chọn nhà cung cấp")
b.bullet("Nhập từ khóa vào ô tìm rồi bấm Tìm kiếm; bấm Làm mới để xóa điều kiện tìm.")
b.bullet("Bấm vào dòng cần chọn — cửa sổ tự đóng, ô hiện dạng mã - tên và ô hợp đồng được mở khóa.")
b.bullet("Đổi đối tượng của một dòng đã chọn hợp đồng thì hợp đồng của dòng đó bị xóa và công nợ "
         "về 0; phải chọn lại hợp đồng.")

b.h3("3.4.3. Chọn hợp đồng cho dòng")
b.para("Bấm vào ô hợp đồng của dòng, cửa sổ chọn hợp đồng mở ra và chỉ liệt kê hợp đồng đúng bản "
       "chất của loại chi.")
b.image("18-popup-hop-dong-mua.png", "Cửa sổ Chọn hợp đồng mua của một nhà cung cấp")
b.bullet("Loại Chi trả nhà cung cấp: chỉ hợp đồng MUA của nhà cung cấp đã chọn.")
b.bullet("Loại Chi trả lại khách hàng: chỉ hợp đồng BÁN của khách hàng đã chọn.")
b.bullet("Loại Chi thưởng thực hiện hợp đồng: cửa sổ mở được ngay không cần chọn đối tượng "
         "trước, và chỉ liệt kê hợp đồng mà người lập được hưởng thưởng; cửa sổ có thêm ô lọc "
         "Khách hàng và cột Khách hàng.")
b.bullet("Hợp đồng đã được chọn ở một dòng khác trong cùng phiếu sẽ bị đánh dấu và không chọn "
         "lại được.")
b.para("Chọn xong, cột công nợ của dòng được điền tự động theo sổ kế toán.")

b.h3("3.4.4. Nhập số tiền và ghi chú của dòng")
b.para("Nhập số tiền vào ô Số tiền đề nghị chi. Ô tự thêm dấu phẩy ngăn nghìn. Dòng Tổng cộng ở "
       "cuối bảng cập nhật ngay theo từng phím gõ. Ô Ghi chú của dòng không bắt buộc. Khi dùng "
       "ngoại tệ, cột Số tiền đề nghị chi tách thành hai cột con: nguyên tệ để nhập và VND để "
       "hiển thị số quy đổi (bằng số tiền nhân tỷ giá).")

b.h3("3.4.5. Xóa một dòng")
b.para("Bấm biểu tượng thùng rác ở cuối dòng. Dòng bị xóa ngay, các dòng sau được đánh số lại và "
       "dòng Tổng cộng tính lại.")

b.h3("3.4.6. Loại chi vận chuyển — lấy dữ liệu chuyến xe")
b.para("Loại chi Thanh toán chi phí vận chuyển NCC KHÔNG thêm dòng bằng tay. Các bước:")
b.bullet("Bước 1: Chọn Nhà cung cấp (chủ xe) ở khối Thông tin chung.")
b.bullet("Bước 2: Chọn Đến ngày — mốc để lấy các chuyến xe phát sinh tới ngày đó.")
b.bullet("Bước 3: Bấm nút Lấy dữ liệu ở góc phải tiêu đề bảng Chi tiết. Hệ thống sinh ra các "
         "dòng chuyến xe kèm Tổng cước, Đã thanh toán và Số tiền còn lại.")
b.bullet("Bước 4: Tích chọn những dòng cần thanh toán (ô tích ở đầu mỗi dòng; ô tích ở hàng tiêu "
         "đề để chọn/bỏ chọn tất cả) rồi nhập số tiền cho những dòng đã tích.")
b.para("Thiếu Nhà cung cấp hoặc thiếu Đến ngày thì bấm Lấy dữ liệu sẽ bị hệ thống nhắc chọn "
       "trước. Chỉ những dòng được tích mới bắt buộc nhập số tiền. Bấm vào mã ở cột Hạch toán "
       "của một dòng sẽ mở cửa sổ Chi tiết chuyến xe hiển thị đầy đủ thông tin chuyến xe đó.")
b.image("25-chi-tiet-loai12.png",
        "Bảng Chi tiết của loại vận chuyển ở màn xem (phiếu dùng ngoại tệ nên có 2 cột tiền)")

b.h2("3.5. Lưu phiếu")
b.table([
    ["Nút", "Tác dụng", "Ràng buộc dữ liệu", "Kết quả"],
    ["Lưu nháp", "Lưu phiếu ở trạng thái Đang tạo.",
     "Bắt buộc Lý do chi và tỷ giá lớn hơn 0. KHÔNG bắt buộc dòng chi tiết, file đính kèm và "
     "khối ngân hàng. Dòng chi tiết đã thêm thì vẫn phải đủ hợp đồng và số tiền.",
     "Báo “Lưu phiếu đề nghị thanh toán thành công!”, quay về danh sách, phiếu ở trạng thái "
     "Đang tạo và chỉ người lập nhìn thấy."],
    ["Lưu và gửi duyệt", "Lưu phiếu và chuyển sang trạng thái Chờ TP duyệt.",
     "Bắt buộc đủ: Lý do chi, ít nhất một dòng chi tiết hợp lệ, khối ngân hàng (nếu chuyển "
     "khoản) và ít nhất một file đính kèm (nếu loại Chi trả nhà cung cấp).",
     "Hiện hộp xác nhận; sau khi xác nhận báo “Gửi duyệt phiếu đề nghị thanh toán thành công!” "
     "và gửi thông báo cho nhóm Trưởng phòng duyệt cùng công ty."],
    ["Quay lại", "Thoát về danh sách.", "—", "Nếu đã nhập dở, hệ thống hỏi lại trước khi thoát."],
])
b.image("20-xac-nhan-gui-duyet.png", "Hộp xác nhận trước khi gửi duyệt")

b.h2("3.6. Báo lỗi khi thiếu thông tin bắt buộc")
b.para("Bấm nút lưu khi còn thiếu dữ liệu, hệ thống báo lỗi đỏ ngay dưới từng ô thiếu và không "
       "lưu gì cả.")
b.image("21-loi-validate.png", "Thông báo bắt buộc nhập ở ô Lý do chi và ở ô số tiền của dòng")
b.image("22-loi-file.png", "Lỗi bắt buộc đính kèm file ở loại Chi trả nhà cung cấp")
b.table([
    ["Trường hợp", "Thông báo hiển thị"],
    ["Bỏ trống Lý do chi", "Bắt buộc nhập (ngay dưới ô Lý do chi, ô viền đỏ)"],
    ["Chưa có dòng chi tiết nào khi gửi duyệt", "Bắt buộc nhập (ngay dưới bảng Chi tiết)"],
    ["Dòng chi tiết chưa chọn đối tượng hoặc chưa chọn hợp đồng",
     "Bắt buộc nhập (dưới ô tương ứng của đúng dòng đó)"],
    ["Số tiền đề nghị chi để 0", "Không được nhỏ hơn 1"],
    ["Tỷ giá bằng 0 hoặc bỏ trống", "Phải lớn hơn 0"],
    ["Loại vận chuyển chưa chọn Đến ngày", "Bắt buộc nhập"],
    ["Chuyển khoản mà khối ngân hàng còn trống (khi gửi duyệt)",
     "Bắt buộc nhập ở các ô Số tài khoản, Tên tài khoản, Tên ngân hàng"],
    ["Loại Chi trả nhà cung cấp chưa đính kèm file (khi gửi duyệt)",
     "Bắt buộc đính kèm ít nhất 1 file (khối File đính kèm viền đỏ)"],
])

b.h2("3.7. Cảnh báo khi thoát mà chưa lưu")
b.para("Nếu đã nhập hoặc sửa bất kỳ ô nào rồi bấm Quay lại (hoặc rời khỏi màn hình), hệ thống "
       "hiện hộp thoại Thông tin chưa lưu.")
b.image("24-canh-bao-chua-luu.png", "Hộp thoại cảnh báo thông tin chưa lưu")
b.bullet("Bấm Thoát: rời màn hình, dữ liệu đang nhập bị bỏ, không phiếu nào được tạo.")
b.bullet("Bấm Ở lại: quay lại form, dữ liệu vẫn còn nguyên.")
b.para("Chưa chạm vào ô nào mà bấm Quay lại thì hệ thống thoát thẳng, không hỏi.")

# ══════════════════════════════════════════════════════════ PHẦN 4
b.h1("PHẦN 4: KHỐI THÔNG TIN NGÂN HÀNG")
b.para("Khối này chỉ xuất hiện khi Hình thức thanh toán là CK (chuyển khoản). Toàn bộ các ô "
       "trong khối đều CHỈ ĐỌC — hệ thống tự lấy theo hồ sơ của đối tượng nhận tiền, người dùng "
       "không gõ tay được.")
b.image("17-ngan-hang.png", "Khối Thông tin ngân hàng tự điền sau khi chọn nhà cung cấp")

b.h2("4.1. Đối tượng trong nước")
b.table([
    ["Trường", "Bắt buộc khi gửi duyệt", "Nguồn dữ liệu"],
    ["Số tài khoản", "Có", "Tài khoản ngân hàng khai trong hồ sơ Khách hàng / Nhà cung cấp"],
    ["Tên tài khoản", "Có", "Như trên"],
    ["Tên ngân hàng", "Có", "Như trên"],
    ["Chi nhánh", "Có (trừ khi nguồn dữ liệu không có thông tin này)", "Như trên"],
    ["Thành phố", "Có (trừ khi nguồn dữ liệu không có thông tin này)", "Như trên"],
    ["Tài khoản ngân hàng", "—",
     "Ô chọn, chỉ hiện khi đối tượng có từ 2 tài khoản trở lên; đổi tài khoản thì các ô bên dưới "
     "đổi theo"],
])
b.para("Nếu đối tượng nhận tiền chưa khai tài khoản ngân hàng, khối này để trống và hiện dòng "
       "chữ đỏ hướng dẫn cập nhật ở màn Khách hàng / Nhà cung cấp rồi chọn lại. Phiếu vẫn lưu "
       "nháp được; chỉ khi bấm Lưu và gửi duyệt mới bị chặn.")

b.h2("4.2. Nhà cung cấp nước ngoài")
b.para("Với nhà cung cấp nước ngoài, khối ngân hàng đổi sang bộ trường khác:")
b.table([
    ["Trường", "Bắt buộc khi gửi duyệt", "Ghi chú"],
    ["Ngân hàng", "Có", "Ô chọn trong danh sách ngân hàng đã khai của nhà cung cấp"],
    ["Số tài khoản", "Có", "Tự điền theo ngân hàng đã chọn"],
    ["Tài khoản", "Có", "Tên chủ tài khoản"],
    ["Tên ngân hàng", "Có", "Tự điền"],
    ["Swift Code", "Có", "Tự điền"],
    ["IBAN Number", "Không", "Tự điền nếu có"],
    ["Địa chỉ", "Không", "Địa chỉ ngân hàng"],
    ["Phí", "Có",
     "Ba giá trị: Phí do người chuyển tiền chịu · Phí do người hưởng chịu · Phí chia sẻ cho 2 bên"],
    ["Ngân hàng trung gian và bộ ô (trung gian)", "Không",
     "Số tài khoản, Tài khoản, Tên ngân hàng, Swift Code, IBAN Number, Địa chỉ của ngân hàng "
     "trung gian"],
])

b.h2("4.3. Loại chi thưởng thực hiện hợp đồng")
b.para("Với loại chi này và hình thức chuyển khoản, người nhận tiền luôn là chính người lập "
       "phiếu, nên màn hình không có ô chọn đối tượng. Khối ngân hàng tự điền theo tài khoản "
       "ngân hàng khai trong hồ sơ nhân sự của người lập.")

# ══════════════════════════════════════════════════════════ PHẦN 5
b.h1("PHẦN 5: FILE ĐÍNH KÈM")
b.para("Khối File đính kèm nằm dưới bảng Chi tiết. Với loại chi Chi trả nhà cung cấp, tiêu đề "
       "khối có dấu sao đỏ — bắt buộc ít nhất một file khi gửi duyệt. Ba loại chi còn lại không "
       "bắt buộc.")
b.image("19-file-dinh-kem.png", "Khối File đính kèm với một dòng chờ chọn tệp")

b.h2("5.1. Thêm tài liệu")
b.bullet("Bấm nút Thêm tài liệu ở góc phải tiêu đề khối để thêm một dòng trống.")
b.bullet("Bấm nút Chọn tệp trên dòng đó và chọn file từ máy. Hệ thống tải file lên NGAY lúc chọn "
         "(hiện vòng quay và dòng chữ đang tải), không chờ tới lúc lưu phiếu.")
b.bullet("Tải xong, dòng hiện tên file, dung lượng và các nút Xem trước, Tải xuống, Thay đổi.")
b.para("Định dạng nhận: pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip. Dung lượng tối đa mỗi "
       "file là 20MB. Rê chuột vào nút Thêm tài liệu để xem lại giới hạn này.")

b.h2("5.2. Xem trước, tải xuống, thay đổi và xóa")
b.table([
    ["Nút", "Tác dụng", "Điều kiện"],
    ["Xem trước (biểu tượng con mắt)", "Mở cửa sổ xem nội dung file.",
     "Chỉ với các định dạng xem trước được."],
    ["Tải xuống", "Tải file về máy.", "Luôn có."],
    ["Thay đổi", "Chọn file khác thay cho file hiện tại.",
     "Chỉ với file vừa tải lên mà phiếu CHƯA lưu. File đã lưu vào phiếu thì phải xóa rồi thêm "
     "lại."],
    ["Xóa (thùng rác)", "Xóa dòng file khỏi phiếu.",
     "Có hộp hỏi xác nhận “Bạn có chắc muốn xóa file đính kèm này?”. File đã lưu bị xóa hẳn khỏi "
     "kho lưu trữ, không hoàn tác được."],
])
b.para("Ở màn xem chi tiết, khối File đính kèm chỉ còn tên file, dung lượng và hai nút Xem trước "
       "/ Tải xuống — không có nút Thêm tài liệu và nút Xóa.")

# ══════════════════════════════════════════════════════════ PHẦN 6
b.h1("PHẦN 6: CHỈNH SỬA PHIẾU")
b.para("Yêu cầu: phiếu do CHÍNH người đăng nhập lập và đang ở trạng thái Đang tạo hoặc Không "
       "duyệt. Phiếu của người khác, hoặc phiếu đã gửi duyệt, sẽ không có nút Sửa.")
b.para("Cách mở: bấm nút Sửa (biểu tượng bút chì) ở cột Hành động, hoặc mở chi tiết phiếu rồi "
       "bấm nút Sửa ở thanh nút dưới cùng.")
b.image("29-sua.png", "Màn chỉnh sửa phiếu đề nghị thanh toán")
b.para("So với màn lập mới, màn chỉnh sửa có thêm ô Mã phiếu (chỉ để xem) và dòng ghi người lập "
       "cùng ngày lập ở góc phải tiêu đề khối Thông tin chung. Cách nhập các khối còn lại giống "
       "hệt PHẦN 3 đến PHẦN 5.")
b.para("Trường hợp phiếu bị từ chối: người lập mở phiếu, đọc ghi chú của cấp đã từ chối, sửa lại "
       "nội dung rồi bấm Lưu và gửi duyệt để gửi lại. Phiếu quay về trạng thái Chờ TP duyệt và "
       "phải đi lại luồng duyệt từ cấp đầu tiên.")
b.para("Nếu trong lúc đang sửa, phiếu bị người khác đổi trạng thái (ví dụ mở hai tab và tab kia "
       "vừa gửi duyệt), khi bấm lưu hệ thống sẽ từ chối vì phiếu không còn ở trạng thái cho sửa. "
       "Hãy tải lại trang để xem hiện trạng mới nhất.")

# ══════════════════════════════════════════════════════════ PHẦN 7
b.h1("PHẦN 7: XEM CHI TIẾT PHIẾU")
b.para("Bấm vào mã phiếu ở cột Mã phiếu để mở màn chi tiết. Tiêu đề trang hiển thị "
       "“Chi tiết phiếu đề nghị thanh toán: <mã phiếu>”.")
b.image("08-chi-tiet.png", "Màn chi tiết phiếu đề nghị thanh toán (nhà cung cấp nước ngoài)")
b.para("Màn chi tiết dùng chung bố cục với màn nhập nhưng mọi ô đều bị khóa, và khối Thông tin "
       "chung có thêm ô Trạng thái. Bảng Chi tiết có thêm bốn cột tiền của các cấp duyệt.")
b.image("09-chi-tiet-cot-duyet.png",
        "Bảng Chi tiết ở màn xem: 4 cột tiền của các cấp và khối File đính kèm")
b.table([
    ["Cột thêm ở màn xem", "Ý nghĩa"],
    ["TP duyệt", "Số tiền cấp Trưởng phòng đã duyệt cho dòng đó."],
    ["KT công nợ duyệt", "Số tiền cấp Kế toán công nợ đã duyệt."],
    ["KT trưởng / BGĐ duyệt", "Số tiền cấp Kế toán trưởng hoặc Ban giám đốc đã duyệt."],
    ["Số tiền chi",
     "Số tiền thực chi lấy từ phiếu chi / giấy ủy nhiệm chi. Chưa có chứng từ chi thì hiện dấu "
     "gạch dưới, KHÔNG hiện số 0."],
])
b.para("Khi người dùng đang giữ phiếu ở đúng cấp duyệt của mình, chỉ cột tiền CỦA CẤP ĐÓ là ô "
       "nhập được; ba cột còn lại chỉ đọc.")
b.para("Công nợ trên màn chi tiết được tính lại theo sổ kế toán tại thời điểm mở phiếu, không "
       "phải số đã lưu lúc lập, nên giá trị có thể khác giữa hai lần xem.")
b.para("Thanh nút dưới cùng thay đổi theo trạng thái phiếu và quyền của người xem:")
b.table([
    ["Nút", "Khi nào hiển thị"],
    ["Sửa", "Phiếu do chính mình lập, đang ở Đang tạo hoặc Không duyệt."],
    ["Xóa", "Cùng điều kiện với nút Sửa."],
    ["Duyệt", "Người xem có quyền duyệt ở đúng trạng thái hiện tại của phiếu."],
    ["Chuyển duyệt BGĐ",
     "Người xem là Kế toán trưởng và phiếu đang ở Chờ kế toán trưởng duyệt."],
    ["Từ chối", "Cùng điều kiện với nút Duyệt."],
    ["Tạo phiếu chi",
     "Người xem có quyền Kế toán thanh toán, phiếu ở Chờ tạo phiếu chi, hình thức tiền mặt, chưa "
     "có chứng từ chi."],
    ["Tạo ủy nhiệm chi", "Như trên nhưng hình thức chuyển khoản."],
    ["In", "Luôn hiển thị."],
    ["Xuất Excel", "Luôn hiển thị."],
    ["Quay lại", "Luôn hiển thị, đưa về màn danh sách."],
])
b.para("Cuối màn chi tiết là khối File đính kèm và khối Lịch sử — xem PHẦN 12.")

# ══════════════════════════════════════════════════════════ PHẦN 8
b.h1("PHẦN 8: DUYỆT PHIẾU THEO CẤP")
b.para("Phần này áp dụng cho người giữ một trong các vai duyệt. Luồng duyệt đi theo thứ tự:")
b.table([
    ["Trạng thái phiếu", "Ai duyệt", "Nút trên màn chi tiết", "Trạng thái sau khi duyệt"],
    ["Chờ TP duyệt", "Trưởng phòng của phòng ban người lập", "Duyệt",
     "Chờ kế toán công nợ duyệt"],
    ["Chờ kế toán công nợ duyệt", "Kế toán công nợ", "Duyệt", "Chờ kế toán trưởng duyệt"],
    ["Chờ kế toán trưởng duyệt", "Kế toán trưởng", "Duyệt", "Chờ tạo phiếu chi"],
    ["Chờ kế toán trưởng duyệt", "Kế toán trưởng", "Chuyển duyệt BGĐ", "Chờ ban giám đốc duyệt"],
    ["Chờ ban giám đốc duyệt", "Ban giám đốc", "Duyệt", "Chờ tạo phiếu chi"],
])

b.h2("8.1. Các bước duyệt một phiếu")
b.bullet("Bước 1: Vào menu Phê duyệt - Công nợ - Thu - Chi → Phiếu đề nghị thanh toán chờ duyệt.")
b.bullet("Bước 2: Bấm vào mã phiếu để mở màn chi tiết. (Bấm nút Duyệt ở cột Hành động cũng dẫn "
         "tới đúng màn này chứ không duyệt ngay — số tiền phải được xem trước.)")
b.bullet("Bước 3: Đọc thông tin phiếu và các file đính kèm. Nhập số tiền chấp thuận vào ô ở cột "
         "tiền CỦA CẤP MÌNH cho từng dòng chi tiết.")
b.bullet("Bước 4: Bấm nút Duyệt (hoặc Chuyển duyệt BGĐ nếu là Kế toán trưởng muốn đẩy lên Ban "
         "giám đốc).")
b.bullet("Bước 5: Đọc hộp xác nhận rồi bấm nút xác nhận.")
b.image("12-xac-nhan-duyet.png", "Hộp xác nhận trước khi duyệt, có nêu cấp sẽ nhận phiếu tiếp theo")
b.para("Sau khi duyệt thành công, hệ thống báo duyệt thành công kèm tên cấp sẽ nhận phiếu, "
       "trạng thái phiếu chuyển sang bước kế tiếp và phiếu rời khỏi danh sách Chờ duyệt của "
       "người vừa duyệt. Hệ thống gửi thông báo cho nhóm của cấp kế tiếp (việc cần làm) và gửi "
       "cho người lập cùng cấp vừa duyệt trước đó (việc đã xong).")
b.para("Riêng nút Chuyển duyệt BGĐ có câu hỏi xác nhận khác với nút Duyệt, vì đây là đẩy phiếu "
       "lên cấp trên chứ không phải duyệt xong.")

b.h2("8.2. Sau khi duyệt xong tất cả các cấp")
b.para("Phiếu về trạng thái Chờ tạo phiếu chi và xuất hiện trong danh sách Chờ duyệt của kế toán "
       "thanh toán. Kế toán thanh toán mở phiếu và bấm:")
b.bullet("Tạo phiếu chi — với phiếu hình thức tiền mặt.")
b.bullet("Tạo ủy nhiệm chi — với phiếu hình thức chuyển khoản.")
b.para("Hai nút này loại trừ nhau và chỉ hiện khi phiếu chưa có chứng từ chi nào. Các trạng thái "
       "tiếp theo (Chờ duyệt phiếu chi, Duyệt phiếu chi, Đã hủy) do màn Phiếu chi / Ủy nhiệm chi "
       "đặt, không thao tác ở màn này.")

# ══════════════════════════════════════════════════════════ PHẦN 9
b.h1("PHẦN 9: TỪ CHỐI PHIẾU")
b.para("Người giữ vai duyệt ở đúng cấp có thể từ chối phiếu thay vì duyệt. Bấm nút Từ chối ở "
       "thanh nút dưới cùng của màn chi tiết.")
b.image("11-tu-choi.png", "Cửa sổ Từ chối phiếu")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn", "Ghi chú"],
    ["Ghi chú của <cấp đang giữ phiếu>", "Ô nhiều dòng", "Có", "Trống",
     "Nhãn đổi theo cấp: Ghi chú của Trưởng phòng / Kế toán công nợ / Kế toán trưởng / "
     "Ban giám đốc. Nội dung lưu vào ô ghi chú riêng của cấp đó và hiện trên bản in."],
    ["Lý do không duyệt", "Ô nhiều dòng", "Không", "Trống",
     "Nội dung hiển thị trên thông báo gửi người lập."],
])
b.bullet("Bỏ trống ô ghi chú bắt buộc (hoặc chỉ gõ khoảng trắng) rồi bấm Từ chối: ô viền đỏ, "
         "hiện “Bắt buộc nhập”, cửa sổ không đóng.")
b.bullet("Nhập đủ rồi bấm Từ chối: hệ thống báo thành công, cửa sổ đóng và màn chi tiết nạp lại.")
b.bullet("Bấm Đóng: thoát cửa sổ, phiếu không đổi; mở lại thì hai ô trở về trống.")
b.para("Trạng thái phiếu sau khi bị từ chối phụ thuộc vào cấp thực hiện:")
b.table([
    ["Cấp từ chối", "Trạng thái phiếu sau đó", "Hệ quả"],
    ["Trưởng phòng", "Đang tạo",
     "Phiếu quay về dạng nháp của người lập. Người lập sửa và gửi lại bình thường."],
    ["Kế toán công nợ / Kế toán trưởng / Ban giám đốc", "Không duyệt",
     "Người lập vẫn sửa và gửi lại được; phiếu đi lại luồng duyệt từ cấp Trưởng phòng."],
])
b.para("Đây là quy tắc nghiệp vụ cố ý giữ nguyên từ hệ thống cũ — đừng nhầm là lỗi khi thấy "
       "phiếu bị Trưởng phòng từ chối lại hiện trạng thái Đang tạo.")
b.para("Hệ thống gửi thông báo phiếu bị từ chối cho người lập và cho tất cả các cấp mà phiếu đã "
       "đi qua trước đó; các cấp chưa đi qua không nhận thông báo.")

# ══════════════════════════════════════════════════════════ PHẦN 10
b.h1("PHẦN 10: XÓA PHIẾU")
b.para("Yêu cầu: phiếu do chính người đăng nhập lập và đang ở trạng thái Đang tạo hoặc Không "
       "duyệt. Phiếu đã gửi duyệt hoặc phiếu của người khác không có mục Xóa.")
b.para("Cách 1 — từ danh sách: bấm nút ba chấm ở cột Hành động, chọn Xóa. "
       "Cách 2 — từ màn chi tiết: bấm nút Xóa ở thanh nút dưới cùng.")
b.image("30-xac-nhan-xoa.png", "Hộp thoại xác nhận xóa phiếu")
b.bullet("Hộp thoại Xác nhận xóa hiển thị câu hỏi kèm đúng mã phiếu sắp xóa.")
b.bullet("Bấm Xóa: hệ thống báo xóa thành công, phiếu và các dòng chi tiết bị xóa hẳn, danh sách "
         "tự tải lại.")
b.bullet("Bấm Hủy: đóng hộp thoại, phiếu giữ nguyên.")
b.para("Lưu ý: phiếu đã xóa không khôi phục được, và mã phiếu đã dùng không được cấp lại cho "
       "phiếu mới.")

# ══════════════════════════════════════════════════════════ PHẦN 11
b.h1("PHẦN 11: IN PHIẾU VÀ XUẤT EXCEL")

b.h2("11.1. In phiếu")
b.para("Bấm nút hình máy in ở cột Hành động, hoặc nút In ở màn chi tiết. Hệ thống mở một tab mới "
       "hiển thị bản in. Chức năng này không gắn quyền riêng: ai xem được phiếu thì in được.")
b.image("13-in-phieu.png", "Bản in Phiếu đề nghị thanh toán")
b.para("Bản in gồm các phần:")
b.bullet("Đầu trang: logo và thông tin công ty.")
b.bullet("Tiêu đề PHIẾU ĐỀ NGHỊ THANH TOÁN, dưới là dòng ngày tháng năm và dòng “Số phiếu”.")
b.bullet("Khối thông tin hai cột: Hình thức thanh toán, Ngày lập, Loại thanh toán, Người lập, "
         "Lý do chi, Phòng ban, Tỷ giá; thêm dòng Đến ngày với loại vận chuyển và dòng đối tượng "
         "nhận tiền nếu có.")
b.bullet("Khối ngân hàng (với phiếu chuyển khoản): Chủ tài khoản, Số tài khoản, Ngân hàng, "
         "Chi nhánh, Thành phố; nhà cung cấp nước ngoài in thêm Swift Code, IBAN Number và Phí.")
b.bullet("Bảng chi tiết với tiêu đề hai dòng (dòng dưới ghi đơn vị tiền của từng cột), các cột "
         "số tiền theo cấp duyệt và dòng Tổng cộng. Cột Số tiền chi chỉ in khi phiếu đã ở trạng "
         "thái Duyệt phiếu chi.")
b.bullet("Dòng Ghi chú và Lý do không duyệt nếu phiếu từng bị từ chối.")
b.bullet("Khối ký tên năm ô: BAN GIÁM ĐỐC, KẾ TOÁN TRƯỞNG, KẾ TOÁN CÔNG NỢ, TRƯỞNG PHÒNG, "
         "NGƯỜI ĐỀ NGHỊ. Cấp đã duyệt hiện tên người duyệt kèm chữ “Đã duyệt”; người lập hiện "
         "tên kèm chữ “Đã ký”.")
b.para("Bấm nút In màu xanh ở góc trên bên trái để mở hộp thoại in của trình duyệt. Nút In và "
       "menu bên trái không xuất hiện trên bản in.")

b.h2("11.2. Xuất Excel")
b.para("Bấm mục Xuất Excel trong nút ba chấm ở cột Hành động, hoặc nút Xuất Excel ở màn chi "
       "tiết. Trình duyệt tải về một file có đuôi .xlsx, tên file chứa mã phiếu.")
b.para("File Excel dùng chung dữ liệu với bản in nên số liệu hai đầu ra luôn khớp nhau: cùng "
       "letterhead công ty, cùng bố cục cột theo loại chi và hình thức thanh toán, cùng quy tắc "
       "chỉ in cột Số tiền chi khi phiếu đã ở trạng thái Duyệt phiếu chi.")

# ══════════════════════════════════════════════════════════ PHẦN 12
b.h1("PHẦN 12: LỊCH SỬ THAY ĐỔI")
b.para("Mọi thao tác ghi dữ liệu trên phiếu đều được lưu vết. Chức năng này không gắn quyền "
       "riêng và hiển thị ở cả bốn chế độ xem.")
b.para("Cách 1 — từ danh sách: bấm nút ba chấm ở cột Hành động rồi chọn Lịch sử. "
       "Cách 2 — từ màn chi tiết: cuộn xuống cuối trang, bấm nút Xem lịch sử ở khối Lịch sử.")
b.image("10-lich-su.png", "Khối Lịch sử ở cuối màn chi tiết")
b.para("Mỗi mốc gồm: ngày giờ, tên thao tác (Tạo mới / Thay đổi thông tin / Thay đổi trạng "
       "thái), người thực hiện kèm phòng ban, và phần chi tiết thay đổi:")
b.bullet("Thay đổi thông tin: liệt kê từng trường đã sửa, có mũi tên từ giá trị cũ sang giá trị "
         "mới, dùng tên tiếng Việt.")
b.bullet("Thay đổi trạng thái: ghi trạng thái cũ và trạng thái mới.")
b.bullet("Với thao tác duyệt: kèm khối liệt kê số tiền cấp đó vừa ghi cho TỪNG DÒNG chi tiết, "
         "dạng giá trị cũ → giá trị mới.")
b.bullet("Với thao tác từ chối: kèm ghi chú mà người từ chối đã nhập.")
b.para("Khối Lịch sử ở màn chi tiết có thêm số đếm số mốc, nút Làm mới để nạp lại và nút "
       "Thu gọn để đóng khối. Phiếu chưa từng có thao tác nào trên màn hình này sẽ hiện dòng "
       "“Chưa có lịch sử thao tác nào.”.")

# ══════════════════════════════════════════════════════════ PHẦN 13
b.h1("PHẦN 13: CÂU HỎI THƯỜNG GẶP")
b.table([
    ["Tình huống", "Nguyên nhân và cách xử lý"],
    ["Gõ vào ô Tìm theo mã phiếu nhưng danh sách không đổi",
     "Ô tìm nhanh chờ bấm nút Tìm kiếm mới lọc. Bấm nút Tìm kiếm hoặc nhấn phím Enter."],
    ["Gõ tên nhà cung cấp vào ô lọc Khách hàng không ra kết quả",
     "Hai ô này lấy từ hai danh sách khác nhau. Dùng đúng ô Nhà cung cấp."],
    ["Quay lại màn hình thì vẫn thấy danh sách đang bị lọc",
     "Hệ thống ghi nhớ bộ lọc trong 10 phút. Bấm Làm mới để xóa hết tiêu chí."],
    ["Không thấy một tiêu chí lọc hoặc một cột quen thuộc",
     "Tiêu chí và cột lưu riêng theo tài khoản. Mở Cài đặt bộ lọc hoặc Tuỳ chỉnh cột để bật lại; "
     "ở Cài đặt bộ lọc có nút Khôi phục mặc định."],
    ["Danh sách Chờ duyệt trống trơn",
     "Tài khoản chưa được cấp vai duyệt nào, hoặc hiện không có phiếu nào đang ở đúng cấp của "
     "mình. Trưởng phòng còn bị giới hạn theo phòng ban được giao quản lý."],
    ["Bấm vào ô hợp đồng nhưng không mở được cửa sổ",
     "Dòng đó chưa chọn đối tượng. Gợi ý trong ô ghi rõ phải chọn khách hàng / nhà cung cấp "
     "trước. Riêng loại Chi thưởng thực hiện hợp đồng thì mở được ngay."],
    ["Không tìm thấy hợp đồng cần chọn",
     "Cửa sổ chỉ liệt kê hợp đồng đúng bản chất loại chi và đúng đối tượng của dòng. Loại Chi "
     "thưởng thực hiện hợp đồng chỉ liệt kê hợp đồng người lập được hưởng thưởng."],
    ["Hợp đồng hiện trong danh sách nhưng bấm không chọn được",
     "Hợp đồng đã có ở một dòng khác trong cùng phiếu. Mỗi hợp đồng chỉ chọn một lần."],
    ["Khối ngân hàng trống và không gõ được",
     "Các ô này chỉ đọc. Đối tượng nhận tiền chưa khai tài khoản ngân hàng — cập nhật ở màn "
     "Khách hàng / Nhà cung cấp rồi chọn lại đối tượng."],
    ["Không bấm được Lấy dữ liệu ở loại vận chuyển",
     "Phải chọn Nhà cung cấp và Đến ngày trước."],
    ["Gửi duyệt báo bắt buộc đính kèm file",
     "Loại Chi trả nhà cung cấp bắt buộc ít nhất một file. Ba loại còn lại không bắt buộc."],
    ["Số tiền đề nghị chi để 0 thì không lưu được",
     "Số tiền phải từ 1 trở lên. Dòng không cần thanh toán ở loại vận chuyển thì bỏ tích thay vì "
     "để 0."],
    ["Bị Trưởng phòng từ chối nhưng trạng thái lại là Đang tạo",
     "Đúng thiết kế: từ chối ở cấp Trưởng phòng đưa phiếu về dạng nháp. Các cấp sau mới chuyển "
     "sang Không duyệt."],
    ["Không thấy nút Sửa hoặc nút Xóa",
     "Chỉ người lập phiếu mới sửa và xóa được, và chỉ khi phiếu ở Đang tạo hoặc Không duyệt."],
    ["Không thấy nút Duyệt dù đang giữ quyền duyệt",
     "Nút chỉ hiện khi phiếu đang ở ĐÚNG trạng thái của cấp mình, cùng công ty, và với cấp "
     "Trưởng phòng thì phải đúng phòng ban mình quản lý."],
    ["Cột Số tiền chi hiện dấu gạch dưới",
     "Phiếu chưa có phiếu chi hoặc giấy ủy nhiệm chi. Đây là cách hiển thị cố ý, không phải "
     "thiếu dữ liệu."],
])

info = b.finish()
print(info)
