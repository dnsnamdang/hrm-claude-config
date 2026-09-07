# -*- coding: utf-8 -*-
"""Sinh tai lieu HDSD (.docx) cho man "Phieu uy nhiem chi" (phan he Tai chinh).

Dung engine chung .claude/skills/hdsd-documenter/assets/hdsd_engine.py.
Anh that: unc_shots/ (chup 04/09/2026 tren cong dev hrm-crm.eteksofts.com, 1440x900).

Chay:  python .plans/gop-db/finance-bill-payment-authorization/gen_hdsd.py
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

SHOTS = os.path.join(HERE, "unc_shots")
OUTPUT = os.path.join(HERE, "HDSD_Phiếu ủy nhiệm chi.docx")

b = HdsdBuilder(output=OUTPUT, shots_dir=SHOTS,
                cover_title="(Màn hình: Phiếu ủy nhiệm chi)",
                doc_title="HDSD - Phiếu ủy nhiệm chi")

MENU = "Tài chính → Quản lý tiền → Thanh toán tiền mặt → Phiếu ủy nhiệm chi"

# ═══════════════════════════════════════════════════════════ TỔNG QUAN
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ sử dụng trong tài liệu")
b.table([
    ["Thuật ngữ", "Giải thích"],
    ["Phiếu ủy nhiệm chi",
     "Chứng từ kế toán ghi nhận khoản tiền doanh nghiệp chi ra bằng hình thức CHUYỂN KHOẢN. "
     "Tài liệu này viết tắt là “phiếu”."],
    ["Phiếu đề nghị thanh toán",
     "Chứng từ do bộ phận nghiệp vụ lập để đề nghị chi tiền. Phiếu ủy nhiệm chi được lập từ "
     "phiếu này. Trong tài liệu gọi tắt là “phiếu đề nghị”."],
    ["Phiếu chi tiền",
     "Màn hình song sinh của Phiếu ủy nhiệm chi, dành cho các phiếu đề nghị thanh toán bằng "
     "TIỀN MẶT. Hai màn không bao giờ nhận cùng một phiếu đề nghị."],
    ["Đang tạo",
     "Trạng thái phiếu nháp. Chỉ người lập nhìn thấy. Sửa và xóa được. Chưa ghi gì vào sổ kế "
     "toán."],
    ["Đã hạch toán",
     "Trạng thái phiếu đã ghi bút toán vào sổ kế toán. Không sửa, không xóa được nữa."],
    ["Lưu nháp",
     "Lưu phiếu tạm để làm tiếp sau. Chỉ bắt buộc chọn Loại chi."],
    ["Lưu và duyệt",
     "Chốt phiếu: ghi bút toán vào sổ kế toán ngay và khoá phiếu vĩnh viễn."],
    ["Tài khoản có / Tài khoản nợ",
     "Cặp tài khoản kế toán để ghi bút toán. Tài khoản có là tài khoản tiền bị trừ; tài khoản "
     "nợ là tài khoản công nợ được tất toán."],
    ["Số tiền đề nghị chi / Số tiền duyệt chi",
     "Số tiền bộ phận nghiệp vụ đề nghị và số tiền kế toán chốt chi. Số duyệt chi không được "
     "lớn hơn số đề nghị chi."],
])

b.h2("2. Lịch sử cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Người thực hiện", "Nội dung"],
    ["1.0", "04/09/2026", "Nhóm phát triển HRM",
     "Ban hành lần đầu cho màn Phiếu ủy nhiệm chi (phân hệ Tài chính)."],
])

b.h2("3. Giới thiệu chung")
b.para(
    "Màn hình Phiếu ủy nhiệm chi dùng để lập và theo dõi các khoản chi bằng CHUYỂN KHOẢN của "
    "doanh nghiệp. Đây là bản song sinh chuyển khoản của màn Phiếu chi tiền: cả hai cùng lấy "
    "phiếu đề nghị thanh toán đang ở trạng thái “Chờ tạo phiếu chi”, nhưng màn này chỉ nhận "
    "những phiếu đề nghị có hình thức thanh toán là chuyển khoản.")
b.para("Màn hình phục vụ hai luồng lập phiếu khác hẳn nhau:")
b.bullet(
    "Lập TỪ phiếu đề nghị — áp dụng cho 6 loại chi: Chi trả nhà cung cấp, Chi trả lại khách "
    "hàng, Chi thưởng NVKD, Chi thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận "
    "chuyển NCC. Kế toán chọn phiếu đề nghị, hệ thống kéo toàn bộ thông tin và các dòng chi "
    "tiết về; kế toán chỉ chốt lại số tiền duyệt chi và khai tài khoản chuyển tiền.",
    bold_prefix="Luồng 1")
b.bullet(
    "Lập TRỰC TIẾP cho loại chi “Chi thu nhập cho nhân viên” — không qua phiếu đề nghị. Kế "
    "toán chọn phòng ban, hệ thống tự lấy số thu nhập còn phải trả của từng nhân viên phòng đó "
    "từ sổ kế toán.",
    bold_prefix="Luồng 2")
b.para(
    "Điểm khác biệt quan trọng nhất so với màn Phiếu chi tiền: màn này KHÔNG có bước gửi duyệt, "
    "KHÔNG có nút Duyệt hay Hủy riêng, KHÔNG có chức năng In và KHÔNG có chức năng Xuất Excel. "
    "Người lập phiếu chính là người duyệt: bấm “Lưu và duyệt” là phiếu vào sổ kế toán ngay và "
    "không sửa được nữa. Đây là thiết kế cố ý để giống hệ thống cũ, không phải thiếu sót.")
b.para("Đường dẫn vào màn hình:")
b.bullet("Đường dẫn menu: " + MENU)
b.bullet("Đường dẫn trực tiếp trên thanh địa chỉ: /finance/bill-payment-authorizations")
b.image("25-duong-dan-menu.png", "Đường dẫn menu tới màn Phiếu ủy nhiệm chi")

b.h2("4. Quyền và phạm vi dữ liệu")
b.para(
    "Mục menu “Phiếu ủy nhiệm chi” hiển thị với mọi người vào được phân hệ Tài chính. Việc "
    "kiểm soát nằm ở hai chỗ: bạn NHÌN THẤY được những phiếu nào, và bạn LÀM được những thao "
    "tác nào. Ba tên quyền liên quan tới màn này:")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / phần tương ứng trên màn hình", "Ghi chú"],
    ["Xem tất cả phiếu ủy nhiệm chi của tổng công ty",
     "Nhìn thấy phiếu của mọi công ty.",
     "Danh sách phiếu.",
     "Không mở được phiếu nháp của người khác."],
    ["Xem tất cả phiếu ủy nhiệm chi của công ty",
     "Nhìn thấy phiếu thuộc công ty của mình, cộng phiếu do chính mình lập và phiếu do chính "
     "mình duyệt ở công ty khác.",
     "Danh sách phiếu.",
     "Không mở được phiếu nháp của người khác."],
    ["Kế toán thanh toán",
     "Lập phiếu, sửa phiếu, xóa phiếu; mở được cửa sổ Chọn phiếu đề nghị chi; lấy được số liệu "
     "thu nhập nhân viên theo phòng ban.",
     "Nút “Lưu nháp”, “Lưu và duyệt”, nút Sửa, nút Xóa, ô “Số phiếu đề nghị”, ô “Phòng ban” của "
     "phiếu Chi thu nhập cho nhân viên.",
     "Đây là quyền dùng chung của nhiều màn phân hệ Tài chính, không phải quyền riêng của màn "
     "này. Không có quyền duyệt riêng."],
])
b.para(
    "Không có quyền xem nào trong hai quyền đầu: bạn vẫn vào được màn hình, nhưng chỉ nhìn thấy "
    "những phiếu do chính bạn lập hoặc chính bạn duyệt.")
b.para(
    "Quy tắc phủ lên MỌI cấp quyền: phiếu ở trạng thái “Đang tạo” chỉ người lập nhìn thấy. "
    "Người quản trị hệ thống và người có quyền xem toàn tổng công ty cũng không nhìn thấy phiếu "
    "nháp của người khác.", bold_prefix="Lưu ý quan trọng")

# ═══════════════════════════════════════════════ PHẦN 1
b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

b.h2("1.1. Các bước truy cập")
b.para("Thực hiện lần lượt:")
b.bullet("Bước 1: Đăng nhập hệ thống bằng địa chỉ email và mật khẩu của bạn.")
b.bullet("Bước 2: Ở màn chọn phân hệ, bấm vào phân hệ “Tài chính”.")
b.bullet("Bước 3: Ở thanh menu bên trái, bấm mục “Quản lý tiền”.")
b.bullet("Bước 4: Trong nhóm “THANH TOÁN TIỀN MẶT”, bấm “Phiếu ủy nhiệm chi”.")
b.para(
    "Bạn cũng có thể gõ thẳng /finance/bill-payment-authorizations vào thanh địa chỉ trình "
    "duyệt. Kết quả giống hệt khi vào bằng menu.")

b.h2("1.2. Bố cục màn hình danh sách")
b.image("01-danh-sach.png", "Màn hình danh sách phiếu ủy nhiệm chi")
b.para("Màn hình gồm hai khối xếp trên dưới:")
b.bullet(
    "Chứa ô tìm nhanh theo mã phiếu, nút “Tìm kiếm”, nút “Làm mới”, nút “Cài đặt bộ lọc” và "
    "nút “Tìm kiếm nâng cao”. Khối lọc chi tiết mặc định thu gọn.",
    bold_prefix="Khối “Bộ lọc danh sách” (phía trên)")
b.bullet(
    "Chứa nút “Tạo mới”, nút cấu hình cột, bảng dữ liệu và thanh phân trang.",
    bold_prefix="Khối “Danh sách phiếu ủy nhiệm chi” (phía dưới)")
b.para(
    "Khi danh sách rỗng, bảng hiện dòng chữ “Không có dữ liệu phù hợp bộ lọc.” và dòng thống kê "
    "phía dưới hiện “Không có phiếu nào.”. Trong lúc hệ thống đang nạp dữ liệu, bảng hiện “Đang "
    "tải dữ liệu...”.")

# ═══════════════════════════════════════════════ PHẦN 2
b.h1("PHẦN 2: HƯỚNG DẪN THEO TỪNG QUYỀN")
b.para(
    "Phần này cho bạn biết chính xác phần nào của tài liệu áp dụng cho mình. Nếu chỉ có một "
    "trong ba quyền, bạn chỉ cần đọc đúng mục tương ứng.")

b.h2("2.1. Người dùng có quyền “Xem tất cả phiếu ủy nhiệm chi của tổng công ty”")
b.para("Bạn nhìn thấy gì:")
b.bullet("Toàn bộ phiếu ủy nhiệm chi của mọi công ty trong hệ thống.")
b.bullet(
    "KHÔNG nhìn thấy phiếu nháp (trạng thái “Đang tạo”) của người khác — chỉ nhìn thấy phiếu "
    "nháp do chính bạn lập.")
b.para("Bạn làm được gì:")
b.bullet("Lọc, sắp xếp, chuyển trang, bật tắt cột hiển thị.")
b.bullet("Mở màn xem chi tiết của mọi phiếu trong phạm vi trên.")
b.bullet("Xem lịch sử thay đổi của mọi phiếu trong phạm vi trên.")
b.para(
    "Nếu bạn KHÔNG đồng thời có quyền “Kế toán thanh toán” thì cột “Hành động” của mọi dòng chỉ "
    "có biểu tượng Lịch sử; bấm nút “Tạo mới” vẫn mở được form nhưng khi bấm Lưu hệ thống sẽ "
    "báo bạn không có quyền lập phiếu ủy nhiệm chi.")

b.h2("2.2. Người dùng có quyền “Xem tất cả phiếu ủy nhiệm chi của công ty”")
b.para("Bạn nhìn thấy gì:")
b.bullet("Phiếu thuộc công ty của bạn.")
b.bullet(
    "Cộng thêm phiếu do chính bạn lập và phiếu do chính bạn duyệt, kể cả khi phiếu đó thuộc "
    "công ty khác.")
b.bullet("KHÔNG nhìn thấy phiếu nháp của người khác.")
b.para(
    "Nếu bạn dùng ô lọc “Công ty” chọn sang một công ty khác, danh sách sẽ rỗng — đó là đúng, "
    "không phải lỗi hệ thống.")

b.h2("2.3. Người dùng không có quyền xem theo cấp nào")
b.para(
    "Bạn vẫn vào được màn hình và vẫn thấy mục menu, nhưng danh sách chỉ có những phiếu do "
    "chính bạn lập hoặc chính bạn duyệt. Nếu bạn chưa lập phiếu nào, danh sách sẽ rỗng.")

b.h2("2.4. Người dùng có quyền “Kế toán thanh toán”")
b.para("Đây là quyền then chốt của màn hình. Có quyền này bạn mới:")
b.bullet("Mở được cửa sổ “Chọn phiếu đề nghị chi” và kéo dữ liệu phiếu đề nghị về form.")
b.bullet("Lấy được số liệu thu nhập nhân viên khi lập phiếu Chi thu nhập cho nhân viên.")
b.bullet("Lưu được phiếu (cả “Lưu nháp” lẫn “Lưu và duyệt”).")
b.bullet("Sửa và xóa được phiếu nháp DO CHÍNH BẠN lập.")
b.para(
    "Nếu không có quyền này, ô “Số phiếu đề nghị” bấm vào sẽ không nạp được danh sách và hệ "
    "thống báo bạn không có quyền xem danh sách phiếu đề nghị chi; trường hợp gõ thẳng đường "
    "dẫn màn lập phiếu, hệ thống vẫn chặn ở bước lưu.")

b.h2("2.5. Điều kiện Sửa và Xóa — phải đủ CẢ BA")
b.para(
    "Nút “Sửa” và nút “Xóa” dùng chung một bộ điều kiện. Thiếu một trong ba thì nút không hiển "
    "thị, và gõ thẳng đường dẫn màn Sửa cũng bị chặn:")
b.bullet("Phiếu đang ở trạng thái “Đang tạo”.")
b.bullet("Bạn đúng là người đã lập phiếu đó.")
b.bullet("Bạn có quyền “Kế toán thanh toán”.")
b.para(
    "Người quản trị hệ thống KHÔNG được miễn trừ ba điều kiện này. Đây là điểm siết chặt hơn hệ "
    "thống cũ: hệ thống cũ chỉ kiểm trạng thái nên ai gọi được đường dẫn cũng xóa được phiếu "
    "của người khác.", bold_prefix="Lưu ý")

# ═══════════════════════════════════════════════ PHẦN 3
b.h1("PHẦN 3: TRA CỨU DANH SÁCH PHIẾU")

b.h2("3.1. Tìm nhanh theo mã phiếu")
b.bullet("Bước 1: Gõ mã phiếu hoặc một đoạn của mã vào ô “Tìm theo mã phiếu ủy nhiệm chi...”.")
b.bullet("Bước 2: Bấm nút “Tìm kiếm” hoặc nhấn phím Enter.")
b.para(
    "Ô này KHÔNG tự tìm trong lúc bạn đang gõ — bạn phải bấm Tìm kiếm hoặc nhấn Enter. Bấm dấu "
    "× trong ô để xoá nhanh nội dung đã gõ.")

b.h2("3.2. Bộ lọc nâng cao")
b.para(
    "Bấm nút “Tìm kiếm nâng cao” ở góc phải khối lọc để mở đầy đủ các ô lọc. Khi đang mở, nút "
    "đổi chữ thành “Ẩn tìm kiếm nâng cao”.")
b.image("03-loc-nang-cao.png", "Khối tìm kiếm nâng cao với đầy đủ các ô lọc")
b.table([
    ["Ô lọc", "Kiểu nhập", "Lọc theo cái gì"],
    ["Mã phiếu", "Ô gõ tay",
     "Mã phiếu ủy nhiệm chi. Ô này độc lập với ô tìm nhanh; điền cả hai thì hai điều kiện cộng "
     "dồn với nhau."],
    ["Mã phiếu đề nghị chi", "Ô gõ tay", "Mã phiếu đề nghị đã dùng để lập phiếu."],
    ["Loại chi", "Danh sách chọn",
     "6 lựa chọn: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD, Chi thưởng "
     "thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận chuyển NCC. Ô này cố ý KHÔNG có "
     "“Chi thu nhập cho nhân viên”."],
    ["Trạng thái", "Danh sách chọn", "2 lựa chọn: Đang tạo, Đã hạch toán."],
    ["Người lập", "Danh sách chọn", "Người lập phiếu ủy nhiệm chi."],
    ["Người đề nghị", "Danh sách chọn",
     "Người lập PHIẾU ĐỀ NGHỊ — thường khác với người lập phiếu ủy nhiệm chi."],
    ["Công ty", "Danh sách chọn", "Đơn vị ghi trên phiếu."],
    ["Phòng ban", "Danh sách chọn", "Phòng ban của người lập phiếu."],
    ["Bộ phận", "Danh sách chọn", "Bộ phận của người lập phiếu."],
    ["Ngày lập từ / Ngày lập đến", "Chọn ngày",
     "Ngày TẠO PHIẾU (đúng cột “Ngày tạo” trên bảng). Lấy cả hai ngày đầu mút. Điền một đầu "
     "cũng lọc được."],
])
b.para(
    "Ô dạng danh sách chọn và ô ngày lọc lại NGAY khi bạn chọn. Ba ô gõ tay (Mã phiếu ở ô tìm "
    "nhanh, Mã phiếu, Mã phiếu đề nghị chi) phải bấm “Tìm kiếm” hoặc nhấn Enter.")
b.para(
    "Bấm nút “Làm mới” để xoá toàn bộ điều kiện và quay về danh sách đầy đủ. Nếu bạn mở một "
    "phiếu rồi bấm “Quay lại” trong vòng 10 phút, hệ thống ghi nhớ và khôi phục lại bộ lọc cũ.")

b.h2("3.3. Cài đặt bộ lọc — chọn hiển thị ô lọc nào")
b.bullet("Bước 1: Bấm nút “Cài đặt bộ lọc”.")
b.bullet("Bước 2: Bỏ tích những ô lọc bạn không dùng, hoặc kéo tay nắm để đổi thứ tự.")
b.bullet("Bước 3: Bấm “Lưu”. Bấm “Khôi phục mặc định” nếu muốn đưa về đủ 10 mục ban đầu.")
b.image("04-cai-dat-bo-loc.png", "Cửa sổ Cài đặt bộ lọc")

b.h2("3.4. Tuỳ chỉnh cột hiển thị")
b.bullet("Bước 1: Bấm nút biểu tượng cột nằm ngay bên phải nút “Tạo mới”.")
b.bullet("Bước 2: Tích hoặc bỏ tích cột; kéo tay nắm để đổi thứ tự.")
b.bullet("Bước 3: Bấm “Lưu”.")
b.image("05-cau-hinh-cot.png", "Cửa sổ Tuỳ chỉnh cột")
b.para(
    "Ba cột STT, Mã phiếu và Hành động có biểu tượng ổ khoá: không bỏ tích và không kéo đổi vị "
    "trí được. Hai cột “Số tiền duyệt chi” và “Ngày hạch toán” mặc định ĐANG TẮT — muốn xem "
    "phải tự bật ở đây. Cấu hình được ghi nhớ riêng cho tài khoản của bạn, vẫn còn sau khi "
    "đăng xuất và đăng nhập lại.")

b.h2("3.5. Các cột của bảng danh sách")
b.image("02-danh-sach-cot-phai.png", "Các cột bên phải của bảng danh sách và cột Hành động")
b.table([
    ["Cột", "Nội dung"],
    ["STT", "Số thứ tự theo trang đang xem."],
    ["Mã phiếu",
     "Mã do hệ thống tự sinh, dạng <mã công ty>.UNC<tháng năm>.<5 chữ số>, ví dụ "
     "TPE.UNC0826.00014. Bấm vào mã để mở màn xem chi tiết trong cùng thẻ."],
    ["Mã phiếu đề nghị chi",
     "Mã phiếu đề nghị nguồn. Bấm vào mã để mở màn chi tiết phiếu đề nghị ở thẻ mới. Phiếu Chi "
     "thu nhập cho nhân viên hiển thị dấu gạch ngang vì không có phiếu đề nghị."],
    ["Loại chi", "Loại chi của phiếu."],
    ["Người đề nghị", "Người lập phiếu đề nghị."],
    ["Ngày tạo / Người tạo", "Thời điểm và người lập phiếu ủy nhiệm chi."],
    ["Ngày cập nhật / Người cập nhật", "Lần chỉnh sửa gần nhất."],
    ["Trạng thái",
     "Nhãn màu: “Đã hạch toán” nền xanh lá, “Đang tạo” nền xám."],
    ["Số tiền duyệt chi",
     "Tổng số tiền duyệt chi đã quy đổi của mọi dòng chi tiết. Mặc định ẩn."],
    ["Ngày hạch toán", "Ngày ghi sổ kế toán của phiếu. Mặc định ẩn."],
    ["Hành động", "Chứa các nút thao tác trên từng dòng — xem mục 3.6."],
])
b.para(
    "Mặc định danh sách sắp xếp theo Ngày tạo giảm dần (phiếu mới nhất lên đầu). Bấm vào tiêu "
    "đề cột có biểu tượng mũi tên để đổi cách sắp xếp; 6 cột sắp xếp được là Mã phiếu, Ngày "
    "tạo, Ngày cập nhật, Trạng thái, Ngày hạch toán và Số tiền duyệt chi. Thứ tự sắp xếp áp "
    "dụng cho toàn bộ dữ liệu, không chỉ trang đang xem.")

b.h2("3.6. Các nút thao tác trên từng dòng")
b.table([
    ["Nút", "Biểu tượng", "Khi nào hiện", "Quyền yêu cầu"],
    ["Sửa", "Bút chì",
     "Phiếu đang ở trạng thái “Đang tạo” và do chính bạn lập.", "Kế toán thanh toán"],
    ["Xóa", "Thùng rác đỏ",
     "Cùng điều kiện với nút Sửa.", "Kế toán thanh toán"],
    ["Lịch sử", "Đồng hồ quay ngược",
     "Luôn hiện với mọi dòng, kể cả phiếu đã hạch toán.", "Không yêu cầu quyền riêng"],
])
b.para(
    "Hệ thống ẩn hẳn nút không dùng được chứ không hiện nút xám mờ. Nếu bạn không thấy nút Sửa "
    "hoặc Xóa, hãy kiểm tra lần lượt ba điều kiện ở mục 2.5.")

b.h2("3.7. Phân trang")
b.para(
    "Dòng dưới bảng hiển thị “Hiển thị a–b / N”, trong đó N là tổng số phiếu khớp bộ lọc và nằm "
    "trong phạm vi quyền của bạn. Ô “Số dòng/trang” có 5 mức: 5, 10, 20, 50, 100; mặc định là "
    "10. Thanh phân trang có nút về trang đầu, lùi một trang, số trang, tiến một trang và về "
    "trang cuối. Mỗi lần bạn đổi điều kiện lọc, danh sách quay về trang 1.")

# ═══════════════════════════════════════════════ PHẦN 4
b.h1("PHẦN 4: LẬP PHIẾU TỪ PHIẾU ĐỀ NGHỊ THANH TOÁN")
b.para(
    "Áp dụng cho 6 loại chi: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD, "
    "Chi thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận chuyển NCC. "
    "Yêu cầu quyền “Kế toán thanh toán”.")

b.h2("4.1. Mở form lập phiếu")
b.para(
    "Ở màn danh sách, bấm nút “Tạo mới” (nút xanh có dấu cộng, nằm phía trên bên phải bảng). "
    "Hệ thống mở màn “Thêm phiếu ủy nhiệm chi”.")
b.image("06-tao-moi.png", "Form Thêm phiếu ủy nhiệm chi khi vừa mở")

b.h2("4.2. Giá trị hệ thống điền sẵn khi vừa mở form")
b.table([
    ["Trường", "Giá trị điền sẵn"],
    ["Loại chi", "Chi trả nhà cung cấp"],
    ["Ngày hạch toán", "Ngày hôm nay"],
    ["Tỷ giá (VND)", "1"],
    ["Hình thức thanh toán", "CK (chuyển khoản) — ô này luôn khoá, không sửa được"],
    ["Loại tiền, Người đề nghị, Phòng ban, Lý do chi",
     "Để trống, hiện dòng gợi ý “Theo phiếu đề nghị” — sẽ tự điền sau khi bạn chọn phiếu đề nghị"],
    ["Bảng Chi tiết", "Trống, hiện dòng chữ “Chưa chọn phiếu đề nghị chi”"],
])

b.h2("4.3. Bước 1 — Chọn loại chi (nếu cần)")
b.para(
    "Ô “Loại chi” đã chọn sẵn “Chi trả nhà cung cấp”. Bấm vào ô để đổi sang loại khác. Ô này "
    "không có dấu × nên bạn chỉ đổi được sang loại khác chứ không xoá trắng được.")
b.image("07-chon-loai-chi.png", "Danh sách 7 loại chi ở form lập phiếu")
b.para(
    "Sau khi bạn chọn phiếu đề nghị ở bước sau, ô “Loại chi” sẽ bị khoá lại (loại chi lấy theo "
    "phiếu đề nghị). Muốn đổi loại chi thì phải bỏ phiếu đề nghị và làm lại từ đầu.",
    bold_prefix="Lưu ý")

b.h2("4.4. Bước 2 — Chọn phiếu đề nghị chi")
b.bullet("Bước 2.1: Bấm vào ô “Số phiếu đề nghị” (ô có dòng chữ “Nhấn vào đây để chọn phiếu đề "
         "nghị chi”). Bạn không gõ tay được vào ô này.")
b.bullet("Bước 2.2: Hệ thống mở cửa sổ “Chọn phiếu đề nghị chi”.")
b.image("08-popup-chon-de-nghi.png", "Cửa sổ Chọn phiếu đề nghị chi")
b.para(
    "Cửa sổ chỉ liệt kê phiếu đề nghị đang ở trạng thái “Chờ tạo phiếu chi” VÀ có hình thức "
    "thanh toán là chuyển khoản — đúng như dòng phụ đề của cửa sổ. Phiếu đề nghị thanh toán "
    "tiền mặt không bao giờ xuất hiện ở đây; chúng thuộc màn Phiếu chi tiền.")
b.para("Trong cửa sổ có 3 ô lọc:")
b.bullet("Mã phiếu đề nghị — gõ tay, nhấn Enter hoặc bấm “Tìm kiếm”.")
b.bullet(
    "Loại chi — chọn từ 4 lựa chọn: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng "
    "thực hiện hợp đồng, Thanh toán chi phí vận chuyển NCC. Chọn xong hệ thống lọc ngay.")
b.bullet("Người lập — chọn nhân viên, chọn xong hệ thống lọc ngay.")
b.bullet("Bước 2.3: Bấm vào DÒNG của phiếu đề nghị muốn chọn (bấm ở bất kỳ ô nào trên dòng).")
b.para(
    "Cửa sổ tự đóng và hệ thống kéo toàn bộ dữ liệu phiếu đề nghị về form.")
b.image("09-form-da-chon-de-nghi.png",
        "Form sau khi chọn phiếu đề nghị — dữ liệu và dòng chi tiết đã được kéo về")

b.h2("4.5. Những gì hệ thống tự điền sau khi chọn phiếu đề nghị")
b.table([
    ["Trường", "Giá trị tự điền"],
    ["Tài khoản có", "Tài khoản tiền gửi ngân hàng (1121 - Tiền Việt Nam)"],
    ["Tài khoản nợ",
     "Tài khoản công nợ tương ứng loại chi. Riêng loại chi “Chi thưởng thực hiện hợp đồng” thì "
     "ô này ẩn đi vì tài khoản nợ được khai theo từng dòng chi tiết"],
    ["Loại tiền, Tỷ giá (VND)", "Lấy theo phiếu đề nghị"],
    ["Người đề nghị, Phòng ban, Lý do chi", "Lấy theo phiếu đề nghị, ở chế độ chỉ đọc"],
    ["Khách hàng / Nhà cung cấp / Nhân viên",
     "Hiện đúng một ô tương ứng với đối tượng nhận tiền của phiếu đề nghị"],
    ["Khối “TÀI KHOẢN NHẬN TIỀN”",
     "Số tài khoản, Tên tài khoản, Tên ngân hàng, Chi nhánh, Thành phố của người nhận"],
    ["Bảng Chi tiết",
     "Toàn bộ dòng chi tiết của phiếu đề nghị. Cột “Số tiền duyệt chi” điền sẵn BẰNG ĐÚNG cột "
     "“Số tiền đề nghị chi”"],
])
b.para(
    "Nếu người nhận tiền là nhà cung cấp NƯỚC NGOÀI, form hiện thêm ô “Phí” và hai khối "
    "“NGÂN HÀNG” và “NGÂN HÀNG TRUNG GIAN” (Số tài khoản, Tài khoản, Tên ngân hàng, Swift Code, "
    "IBAN Number, Địa chỉ). Khi đó khối “TÀI KHOẢN NHẬN TIỀN” không hiện.")

b.h2("4.6. Bước 3 — Chốt số tiền duyệt chi trên từng dòng")
b.para(
    "Cột “Số tiền duyệt chi” là cột DUY NHẤT bạn nhập ở bảng chi tiết (ngoài ô Ghi chú). Hệ "
    "thống đã điền sẵn bằng số tiền đề nghị chi; nếu chi ít hơn thì sửa lại.")
b.bullet(
    "Nhập số LỚN HƠN số tiền đề nghị chi của dòng: ô viền đỏ, hiện chữ đỏ “Không được lớn hơn "
    "số tiền đề nghị chi (…)”. Hệ thống chặn cả hai nút lưu và hiện thông báo nêu rõ số thứ tự "
    "dòng đang sai.")
b.bullet("Nhập số ÂM: hệ thống tự đưa về 0.")
b.bullet(
    "Đổi ô “Tỷ giá (VND)”: hệ thống tính lại cột quy đổi của TOÀN BỘ các dòng và dòng “Tổng "
    "cộng”.")
b.bullet("Ô “Ghi chú” của từng dòng là tuỳ chọn, không bắt buộc.")

b.h2("4.7. Bước 4 — Khai tài khoản chuyển tiền")
b.para("Ba ô này bắt buộc khi bấm “Lưu và duyệt”:")
b.bullet(
    "Phương thức thanh toán — chọn “Tiền tự có” hoặc “Tiền vay”.")
b.bullet(
    "Ngân hàng chuyển — chọn ngân hàng của doanh nghiệp. Chọn xong hệ thống lọc lại danh sách "
    "số tài khoản theo đúng ngân hàng đó và XOÁ số tài khoản bạn đang chọn (nếu có).")
b.image("11-chon-ngan-hang-chuyen.png", "Chọn ngân hàng chuyển")
b.bullet(
    "Số tài khoản chuyển khoản — chọn tài khoản của ngân hàng vừa chọn. Nếu ngân hàng đó chỉ có "
    "ĐÚNG MỘT tài khoản và bạn đã chọn “Tiền tự có”, hệ thống tự điền giúp; có từ hai tài khoản "
    "trở lên thì bạn phải tự chọn.")
b.image("12-chon-so-tai-khoan-chuyen.png",
        "Danh sách số tài khoản chuyển khoản đã lọc theo ngân hàng")

b.h2("4.8. Bước 5 — Lưu phiếu")
b.para("Chân form có ba nút:")
b.table([
    ["Nút", "Tác dụng", "Bắt buộc nhập gì"],
    ["Lưu nháp",
     "Lưu phiếu tạm ở trạng thái “Đang tạo”. Chưa ghi gì vào sổ kế toán, chưa đổi trạng thái "
     "phiếu đề nghị. Sửa và xóa lại được.",
     "CHỈ bắt buộc ô “Loại chi”. Mọi ô khác để trống vẫn lưu được."],
    ["Lưu và duyệt",
     "Chốt phiếu, ghi bút toán vào sổ kế toán ngay. Phiếu chuyển sang “Đã hạch toán” và KHÔNG "
     "sửa, KHÔNG xóa được nữa.",
     "Bắt buộc đầy đủ — xem Phần 6."],
    ["Quay lại", "Về màn danh sách. Nếu đã nhập dở, hệ thống hỏi xác nhận trước khi rời.", "—"],
])
b.para(
    "Sau khi lưu thành công, hệ thống hiện thông báo xanh và tự quay về màn danh sách; phiếu "
    "mới nằm ở đầu danh sách.")

b.h2("4.9. Cảnh báo khi thoát mà chưa lưu")
b.para(
    "Nếu bạn đã nhập hoặc chọn dữ liệu rồi bấm “Quay lại” (hoặc chuyển sang màn khác), hệ thống "
    "hiện cửa sổ “Thông tin chưa lưu” với nội dung “Bạn có thông tin chưa lưu. Có chắc chắn "
    "muốn thoát?”.")
b.image("13-canh-bao-chua-luu.png", "Cửa sổ cảnh báo thông tin chưa lưu")
b.bullet("Bấm “Ở lại” để quay về form, dữ liệu vẫn còn nguyên.")
b.bullet("Bấm “Thoát” để rời màn và bỏ mọi thay đổi.")
b.para(
    "Nếu bạn chưa chạm vào ô nào, hoặc vừa lưu thành công, hệ thống KHÔNG hỏi câu này.")

# ═══════════════════════════════════════════════ PHẦN 5
b.h1("PHẦN 5: LẬP PHIẾU CHI THU NHẬP CHO NHÂN VIÊN")
b.para(
    "Luồng này KHÔNG qua phiếu đề nghị. Hệ thống tự lấy số thu nhập còn phải trả của từng nhân "
    "viên trong một phòng ban từ sổ kế toán. Yêu cầu quyền “Kế toán thanh toán”.")

b.h2("5.1. Chuyển sang luồng Chi thu nhập cho nhân viên")
b.bullet("Bước 1: Bấm “Tạo mới” ở màn danh sách.")
b.bullet("Bước 2: Ở ô “Loại chi”, chọn “Chi thu nhập cho nhân viên”.")
b.para("Ngay khi chọn, form thay đổi hẳn:")
b.image("16-form-chi-thu-nhap-nv.png", "Form khi chọn loại chi Chi thu nhập cho nhân viên")
b.table([
    ["Thay đổi", "Chi tiết"],
    ["Ẩn đi",
     "Ô “Số phiếu đề nghị”, ô “Tài khoản nợ”, ô “Ngày hạch toán”, ô “Phương thức thanh toán”, "
     "toàn bộ khối thông tin đối tượng nhận tiền và khối ngân hàng người nhận."],
    ["Hiện thêm",
     "Ô “Người nhận” (bắt buộc), ô “Phòng ban” dạng danh sách chọn với gợi ý “Chọn phòng ban "
     "chi” (bắt buộc), ô “Lý do chi” chuyển thành ô nhập tay (bắt buộc)."],
    ["Khoá cứng",
     "Tài khoản có = 1121 - Tiền Việt Nam; Loại tiền = VietNamDong; Tỷ giá (VND) = 1."],
    ["Điền sẵn", "Người đề nghị = tên người đang đăng nhập."],
    ["Ngày hạch toán",
     "Không hiện trên form; hệ thống tự lấy ngày hôm nay khi lưu."],
])

b.h2("5.2. Chọn phòng ban để lấy số liệu nhân viên")
b.bullet("Bước 1: Bấm ô “Phòng ban”, chọn phòng ban cần chi.")
b.bullet(
    "Bước 2: Chờ hệ thống lấy số liệu. Trong lúc chờ, bảng chi tiết hiện “Đang lấy số liệu nhân "
    "viên...”.")
b.para(
    "Trước khi chọn phòng ban, bảng chi tiết hiện dòng chữ “Chưa chọn phòng ban chi — chọn "
    "phòng ban để hệ thống lấy số liệu thu nhập nhân viên.”. Nếu phòng ban không có nhân viên "
    "nào còn số dư thu nhập, bảng hiện “Không có dữ liệu phù hợp”.")
b.image("17-bang-thu-nhap-nhan-vien.png",
        "Bảng nhân viên sau khi chọn phòng ban (phòng chưa có số dư thu nhập)")
b.para(
    "Hệ thống chỉ lấy nhân viên thuộc CÔNG TY của bạn. Nhân viên không còn khoản nào chưa chi "
    "sẽ không xuất hiện trong bảng.", bold_prefix="Lưu ý")

b.h2("5.3. Hai tab của bảng chi tiết")
b.para("Bảng chi tiết của luồng này có hai tab:")
b.bullet(
    "Ô tích “Cần thanh toán”, STT, Số tài khoản nợ, Tên tài khoản, Nhân viên, Số dư, Số tiền "
    "chi, Tài khoản, Tên ngân hàng, Chi nhánh và dòng Tổng cộng. Đây là nơi bạn khai TỔNG số "
    "tiền chi cho từng người.",
    bold_prefix="Tab “Chi tiết”")
b.bullet(
    "Tách tổng đó thành 5 khoản: Chênh lệch lương, Hoa hồng tháng, Hoa hồng quý, Thưởng quý, "
    "Tiền vận chuyển. Mỗi khoản có một cột “Số dư” (chỉ đọc) và một cột “Số tiền chi” (nhập "
    "được).",
    bold_prefix="Tab “Chi tiết vụ việc”")
b.image("18-tab-chi-tiet-vu-viec.png", "Tab Chi tiết vụ việc với 5 khoản thu nhập")
b.para(
    "Bảng CỐ Ý chỉ có 5 khoản, không có khoản “Chi phí khác” như màn Phiếu chi tiền. Lý do: ở "
    "luồng ủy nhiệm chi, tiền nhập vào khoản đó sẽ không bao giờ được ghi vào sổ kế toán.",
    bold_prefix="Lưu ý")

b.h2("5.4. Khai số tiền chi cho từng nhân viên")
b.bullet(
    "Bước 1: Ở tab “Chi tiết”, bỏ tích ô “Cần thanh toán” ở đầu dòng của những nhân viên KHÔNG "
    "chi đợt này. Dòng bị bỏ tích sẽ mờ đi, mọi ô nhập của dòng bị khoá và dòng đó không được "
    "lưu vào phiếu. Ô tích ở đầu bảng cho phép chọn hoặc bỏ chọn tất cả cùng lúc.")
b.bullet(
    "Bước 2: Nhập ô “Số tiền chi” cho từng nhân viên còn tích. Nhập vượt quá cột “Số dư”, hệ "
    "thống tự kẹp về đúng số dư. Nhân viên có số dư bằng 0 thì ô này bị khoá.")
b.bullet(
    "Bước 3: Chuyển sang tab “Chi tiết vụ việc”, tách số tiền vừa khai thành 5 khoản. Nếu bạn "
    "chưa khai tổng ở tab “Chi tiết”, 5 ô khoản của dòng đó vẫn đang khoá.")
b.bullet(
    "Bước 4 (tuỳ chọn): Đổi ô “Số tài khoản nợ”. Đổi ở DÒNG ĐẦU TIÊN thì hệ thống áp cho toàn "
    "bộ các dòng còn lại; đổi ở dòng thứ hai trở đi thì chỉ đổi riêng dòng đó.")
b.para(
    "Tổng 5 khoản của một nhân viên PHẢI bằng ô “Số tiền chi” của nhân viên đó (chênh lệch cho "
    "phép tối đa 0,5 đồng). Nếu lệch, khi bấm “Lưu và duyệt” hệ thống chặn và báo “Tổng số tiền "
    "chi theo mã vụ việc và tổng số tiền đề nghị chi khác nhau!”.", bold_prefix="Quan trọng")

b.h2("5.5. Hoàn tất và lưu")
b.bullet("Bước 1: Nhập ô “Người nhận” (tên người nhận tiền).")
b.bullet("Bước 2: Nhập ô “Lý do chi”.")
b.bullet("Bước 3: Chọn “Ngân hàng chuyển” và “Số tài khoản chuyển khoản”.")
b.bullet("Bước 4: Bấm “Lưu nháp” để lưu tạm, hoặc “Lưu và duyệt” để chốt phiếu.")

# ═══════════════════════════════════════════════ PHẦN 6
b.h1("PHẦN 6: LƯU VÀ DUYỆT PHIẾU")
b.para("Yêu cầu quyền “Kế toán thanh toán”.")

b.h2("6.1. Các bước thực hiện")
b.bullet("Bước 1: Ở màn lập phiếu hoặc màn sửa phiếu, bấm nút “Lưu và duyệt”.")
b.bullet(
    "Bước 2: Hệ thống hiện cửa sổ “Xác nhận lưu và duyệt” với câu hỏi “Bạn đồng ý lưu và "
    "duyệt?”.")
b.image("14-xac-nhan-luu-va-duyet.png", "Cửa sổ xác nhận lưu và duyệt")
b.bullet("Bước 3: Bấm “Xác nhận” để chốt phiếu, hoặc “Hủy” để đóng cửa sổ và không lưu gì.")

b.h2("6.2. Những ô bắt buộc khi Lưu và duyệt")
b.para(
    "Nếu thiếu, hệ thống hiện thông báo đỏ “Vui lòng kiểm tra lại dữ liệu nhập” ở góc phải màn "
    "hình, đồng thời các ô thiếu bị viền đỏ kèm chữ “Bắt buộc nhập” ngay bên dưới. Phiếu KHÔNG "
    "được lưu.")
b.image("15-loi-validate.png", "Báo lỗi khi bấm Lưu và duyệt với form còn trống")
b.table([
    ["Luồng", "Các ô bắt buộc"],
    ["Lập từ phiếu đề nghị",
     "Số phiếu đề nghị, Tài khoản có, Tài khoản nợ, Ngày hạch toán, Loại chi, Phương thức thanh "
     "toán, Ngân hàng chuyển, Số tài khoản chuyển khoản, và bảng chi tiết phải có ít nhất một "
     "dòng với số tiền duyệt chi lớn hơn 0."],
    ["Chi thu nhập cho nhân viên",
     "Loại chi, Người nhận, Phòng ban, Lý do chi, Ngân hàng chuyển, Số tài khoản chuyển khoản, "
     "và bảng nhân viên phải có ít nhất một dòng."],
])

b.h2("6.3. Quy tắc ngày hạch toán")
b.para(
    "Khi bấm “Lưu và duyệt”, ô “Ngày hạch toán” phải BẰNG hoặc LỚN HƠN ngày hôm nay. Lịch chọn "
    "ngày đã làm mờ sẵn mọi ngày trong quá khứ. Nếu ngày trên phiếu đã cũ, hệ thống báo “Ngày "
    "hạch toán không được nhỏ hơn ngày hôm nay”.")
b.para(
    "Phiếu nháp lưu hôm qua, hôm nay mở ra bấm “Lưu và duyệt” mà quên đổi ngày sẽ bị chặn. Chỉ "
    "cần chọn lại ngày hạch toán là hôm nay rồi duyệt tiếp. Riêng nút “Lưu nháp” thì ngày quá "
    "khứ vẫn lưu được bình thường.", bold_prefix="Trường hợp thường gặp")

b.h2("6.4. Hệ thống làm gì sau khi bạn bấm Xác nhận")
b.bullet("Ghi phiếu sang trạng thái “Đã hạch toán” và ghi nhận bạn là người duyệt.")
b.bullet(
    "Đẩy số tiền duyệt chi về các dòng của phiếu đề nghị và chuyển phiếu đề nghị ra khỏi trạng "
    "thái “Chờ tạo phiếu chi” — từ lúc này phiếu đề nghị đó không còn xuất hiện trong cửa sổ "
    "chọn phiếu đề nghị.")
b.bullet("Ghi bút toán vào sổ kế toán.")
b.bullet("Ghi lịch sử thay đổi và quay về màn danh sách kèm thông báo thành công.")
b.para(
    "Toàn bộ các việc trên nằm trong MỘT giao dịch: nếu có lỗi ở bất kỳ bước nào thì mọi thay "
    "đổi bị huỷ, phiếu vẫn ở trạng thái cũ.")

b.h2("6.5. Ba đặc điểm ghi sổ cần biết")
b.para(
    "Ba điểm dưới đây là hành vi CỐ Ý giữ đúng hệ thống cũ để hai hệ thống đối chiếu được với "
    "nhau. Nếu bạn thấy khác với suy nghĩ thông thường thì đó không phải lỗi:")
b.bullet(
    "Với phiếu có nhiều dòng chi tiết, bút toán bên CÓ được ghi bằng số tiền của DÒNG CUỐI "
    "trong bảng chi tiết, không phải tổng các dòng.", bold_prefix="Bút toán bên Có")
b.bullet(
    "Phiếu loại “Chi khác” duyệt xong vẫn chuyển sang “Đã hạch toán” nhưng KHÔNG sinh bút toán "
    "nào.", bold_prefix="Loại chi “Chi khác”")
b.bullet(
    "Một phiếu đề nghị có thể bị hai người lập thành hai phiếu ủy nhiệm chi nháp khác nhau — hệ "
    "thống không chặn ở bước lưu nháp. Nghiệp vụ cần tự kiểm soát để không chi hai lần. Sau khi "
    "một phiếu được duyệt thì phiếu đề nghị rời trạng thái “Chờ tạo phiếu chi” nên không chọn "
    "lại được nữa.", bold_prefix="Trùng phiếu đề nghị")

# ═══════════════════════════════════════════════ PHẦN 7
b.h1("PHẦN 7: SỬA PHIẾU")
b.para("Yêu cầu đủ ba điều kiện ở mục 2.5.")

b.h2("7.1. Các cách mở màn sửa")
b.bullet("Cách 1: Ở màn danh sách, bấm biểu tượng bút chì ở cột “Hành động” của dòng phiếu.")
b.bullet("Cách 2: Mở màn xem chi tiết của phiếu rồi bấm nút “Sửa” ở chân màn.")
b.image("23-sua-phieu.png", "Màn sửa phiếu ủy nhiệm chi")

b.h2("7.2. Khác biệt so với màn lập phiếu")
b.bullet("Tiêu đề màn là “Sửa phiếu ủy nhiệm chi”.")
b.bullet("Hiện thêm ba ô chỉ đọc: “Mã phiếu”, “Người lập”, “Ngày lập”.")
b.bullet(
    "Ô “Loại chi” bị khoá, không đổi được. Muốn đổi loại chi thì phải xóa phiếu và lập lại từ "
    "đầu.")
b.bullet("Mọi ô còn lại và bảng chi tiết giống hệt màn lập phiếu.")
b.para(
    "Nếu bạn gõ thẳng đường dẫn màn sửa của một phiếu không đủ điều kiện sửa (đã hạch toán, "
    "hoặc do người khác lập), hệ thống tự đưa bạn về màn xem chi tiết. Trường hợp thao tác vòng "
    "qua giao diện, hệ thống từ chối với thông báo “Chỉ sửa được phiếu ủy nhiệm chi ở trạng "
    "thái Đang tạo do chính bạn lập”.")

b.h2("7.3. Lưu lại phiếu đã sửa")
b.bullet("Bấm “Lưu nháp” để giữ phiếu ở trạng thái “Đang tạo”.")
b.bullet(
    "Bấm “Lưu và duyệt” để chốt phiếu — xem Phần 6. Nhớ kiểm tra lại ô “Ngày hạch toán” trước "
    "khi duyệt.")
b.para(
    "Mỗi lần lưu, hệ thống ghi một dòng lịch sử thay đổi ghi rõ giá trị cũ và giá trị mới của "
    "từng ô đã đổi. Một lần bấm “Lưu và duyệt” trên phiếu nháp sinh ra hai dòng lịch sử: một "
    "dòng nội dung sửa và một dòng chuyển trạng thái.")

# ═══════════════════════════════════════════════ PHẦN 8
b.h1("PHẦN 8: XEM CHI TIẾT VÀ LỊCH SỬ THAY ĐỔI")

b.h2("8.1. Mở màn xem chi tiết")
b.para(
    "Ở màn danh sách, bấm vào MÃ PHIẾU ở cột “Mã phiếu”. Hệ thống mở màn chi tiết trong cùng "
    "thẻ trình duyệt, tiêu đề là “Chi tiết phiếu ủy nhiệm chi: <mã phiếu>”.")
b.image("19-chi-tiet-da-hach-toan.png",
        "Màn chi tiết một phiếu đã hạch toán (nhà cung cấp nước ngoài, thanh toán bằng ngoại tệ)")
b.para(
    "Toàn bộ ô ở chế độ chỉ đọc: không gõ được, không mở được cửa sổ chọn phiếu đề nghị. Bảng "
    "chi tiết hiển thị dạng chữ, số căn phải, ô ghi chú trống hiển thị dấu gạch ngang.")

b.h2("8.2. Các nút ở chân màn chi tiết")
b.table([
    ["Nút", "Khi nào hiện", "Quyền yêu cầu"],
    ["Sửa", "Phiếu “Đang tạo” và do chính bạn lập.", "Kế toán thanh toán"],
    ["Xóa", "Cùng điều kiện với nút Sửa.", "Kế toán thanh toán"],
    ["Quay lại", "Luôn hiện.", "—"],
])
b.image("21-chi-tiet-dang-tao.png",
        "Màn chi tiết một phiếu “Đang tạo” — chân màn có thêm nút Sửa và Xóa")
b.para(
    "Với phiếu đã hạch toán, chân màn CHỈ có nút “Quay lại”. Màn hình không có nút In và không "
    "có nút Xuất Excel.")

b.h2("8.3. Xem lịch sử thay đổi")
b.para("Có hai chỗ xem lịch sử, nội dung như nhau:")
b.bullet(
    "Cách 1 — từ danh sách: bấm biểu tượng đồng hồ ở cột “Hành động”. Hệ thống mở cửa sổ “Lịch "
    "sử thay đổi” kèm dòng “Phiếu: <mã phiếu>”. Nút này luôn hiện với mọi dòng, kể cả phiếu đã "
    "hạch toán.")
b.image("24-popup-lich-su.png", "Cửa sổ Lịch sử thay đổi của một phiếu chưa từng bị sửa")
b.bullet(
    "Cách 2 — từ màn chi tiết: cuộn xuống cuối trang, bấm “Xem lịch sử” ở khối “Lịch sử”. Khối "
    "này mặc định thu gọn; khi mở có thêm nút “Làm mới” và “Thu gọn”.")
b.para(
    "Mỗi dòng lịch sử cho biết thời điểm, người thao tác, loại thao tác và các ô đã đổi kèm giá "
    "trị cũ so với giá trị mới. Phiếu chưa từng bị thay đổi hiện dòng chữ “Chưa có lịch sử thao "
    "tác nào.”.")

# ═══════════════════════════════════════════════ PHẦN 9
b.h1("PHẦN 9: XÓA PHIẾU")
b.para("Yêu cầu đủ ba điều kiện ở mục 2.5 — giống hệt điều kiện sửa.")

b.h2("9.1. Các bước thực hiện")
b.bullet(
    "Bước 1: Bấm biểu tượng thùng rác ở cột “Hành động” của màn danh sách, hoặc nút “Xóa” ở "
    "chân màn xem chi tiết.")
b.bullet(
    "Bước 2: Hệ thống hiện cửa sổ “Xác nhận xóa” với nội dung “Bạn có chắc muốn xóa phiếu ủy "
    "nhiệm chi ‘<mã phiếu>’?”.")
b.image("22-xac-nhan-xoa.png", "Cửa sổ xác nhận xóa phiếu")
b.bullet("Bước 3: Bấm “Xóa” để xóa, hoặc “Hủy” để đóng cửa sổ và giữ nguyên phiếu.")

b.h2("9.2. Kết quả sau khi xóa")
b.bullet("Phiếu bị xóa vĩnh viễn cùng toàn bộ dòng chi tiết của nó.")
b.bullet("Hệ thống hiện thông báo xóa thành công và tải lại danh sách.")
b.bullet(
    "Xóa từ màn chi tiết thì hệ thống đưa bạn về màn danh sách.")
b.para(
    "Xóa phiếu nháp KHÔNG làm thay đổi trạng thái phiếu đề nghị, vì lúc lưu nháp hệ thống cũng "
    "chưa hề đổi trạng thái phiếu đề nghị. Phiếu đề nghị đó vẫn chọn lại được để lập phiếu "
    "khác.")
b.para(
    "Phiếu đã hạch toán KHÔNG xóa được: nút Xóa không hiển thị, và nếu thao tác vòng qua giao "
    "diện thì hệ thống từ chối với thông báo “Chỉ xóa được phiếu ủy nhiệm chi ở trạng thái Đang "
    "tạo do chính bạn lập”.", bold_prefix="Lưu ý")

# ═══════════════════════════════════════════════ PHẦN 10
b.h1("PHẦN 10: TÌNH HUỐNG THƯỜNG GẶP")
b.table([
    ["Tình huống", "Nguyên nhân và cách xử lý"],
    ["Không thấy nút “Sửa” hoặc “Xóa” trên phiếu của mình",
     "Kiểm tra lần lượt: phiếu còn ở trạng thái “Đang tạo” không; bạn có đúng là người lập phiếu "
     "không; tài khoản của bạn có quyền “Kế toán thanh toán” không. Thiếu một trong ba là nút "
     "không hiện."],
    ["Bấm vào ô “Số phiếu đề nghị” nhưng cửa sổ không có dữ liệu",
     "Tài khoản của bạn chưa có quyền “Kế toán thanh toán”. Liên hệ quản trị hệ thống để được "
     "cấp quyền."],
    ["Không tìm thấy phiếu đề nghị cần lập trong cửa sổ chọn",
     "Ba khả năng: (1) phiếu đề nghị đó thanh toán bằng TIỀN MẶT nên thuộc màn Phiếu chi tiền; "
     "(2) phiếu đề nghị chưa ở trạng thái “Chờ tạo phiếu chi”; (3) phiếu đề nghị đã có phiếu ủy "
     "nhiệm chi được duyệt trước đó."],
    ["Bấm “Lưu và duyệt” báo “Ngày hạch toán không được nhỏ hơn ngày hôm nay”",
     "Phiếu nháp lập từ hôm trước. Chọn lại ô “Ngày hạch toán” là ngày hôm nay rồi duyệt tiếp."],
    ["Ô “Số tiền duyệt chi” viền đỏ, báo không được lớn hơn số tiền đề nghị chi",
     "Bạn nhập vượt số bộ phận nghiệp vụ đề nghị. Sửa lại cho nhỏ hơn hoặc bằng. Muốn chi nhiều "
     "hơn thì phải sửa lại phiếu đề nghị trước."],
    ["Bảng nhân viên trống dù đã chọn phòng ban",
     "Phòng ban đó không có nhân viên nào còn số dư thu nhập chưa chi, hoặc nhân viên thuộc "
     "công ty khác với công ty của bạn."],
    ["Bấm “Lưu và duyệt” báo tổng số tiền chi theo mã vụ việc khác tổng số tiền đề nghị chi",
     "Ở tab “Chi tiết vụ việc”, tổng 5 khoản của một nhân viên chưa khớp ô “Số tiền chi” của "
     "nhân viên đó ở tab “Chi tiết”. Rà lại từng dòng."],
    ["Danh sách rỗng dù biết chắc có phiếu",
     "Kiểm tra bộ lọc đang áp dụng (bấm “Làm mới” để xoá hết), sau đó kiểm tra phạm vi quyền "
     "xem ở Phần 2. Riêng phiếu nháp của người khác thì không ai nhìn thấy."],
    ["Không thấy cột “Số tiền duyệt chi” hoặc “Ngày hạch toán”",
     "Hai cột này mặc định tắt. Bật ở cửa sổ “Tuỳ chỉnh cột” (nút biểu tượng cột cạnh nút “Tạo "
     "mới”)."],
    ["Muốn in phiếu hoặc xuất Excel",
     "Màn hình này không có chức năng In và Xuất Excel — đây là thiết kế cố ý giống hệ thống "
     "cũ."],
])

b.finish()
