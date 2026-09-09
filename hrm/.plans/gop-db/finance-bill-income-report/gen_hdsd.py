# -*- coding: utf-8 -*-
"""Sinh HDSD (huong dan su dung) man PHIEU BAO CO + TONG HOP TIEN VE NGAN HANG.

Chay:  python .plans/gop-db/finance-bill-income-report/gen_hdsd.py
Anh:   bir_shots/ (chup that bang Playwright MCP 1440x900, dung chung voi SRS).
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

SHOTS = os.path.join(HERE, "bir_shots")
OUT = os.path.join(HERE, "HDSD_Phieu_bao_co.docx")

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title="(Màn hình: Phiếu báo có – Tổng hợp tiền về ngân hàng)",
                doc_title="HDSD - Phiếu báo có")

# ============================================================ TONG QUAN
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ dùng trong tài liệu")
b.table([
    ["Thuật ngữ", "Ý nghĩa"],
    ["Phiếu báo có",
     "Chứng từ ghi nhận tiền về tài khoản ngân hàng của công ty theo sao kê, gắn khoản tiền "
     "đó với khách hàng / nhà cung cấp / hợp đồng."],
    ["Đang tạo",
     "Phiếu mới lập, còn là bản nháp. Người lập còn sửa và xóa được; chưa ghi vào sổ kế toán."],
    ["Đã duyệt",
     "Phiếu đã được duyệt, hệ thống đã ghi bút toán vào sổ kế toán. Phiếu không sửa, không xóa "
     "được nữa."],
    ["Ghi bút toán vào sổ cái",
     "Hệ thống tự sinh các dòng hạch toán Nợ / Có của phiếu vào sổ kế toán chung. Đây là số liệu "
     "kế toán thật, không hoàn tác được."],
    ["Loại thu",
     "Ba loại: Thu bán hàng, Thu nhà cung cấp, Thu khác. Loại thu quyết định bảng Chi tiết có "
     "những cột nào."],
    ["KHÁCH KHÔNG RÕ",
     "Khách hàng mặc định hệ thống điền sẵn khi chưa biết tiền của ai. Sau đó dùng màn Tổng hợp "
     "tiền về ngân hàng để gán lại đúng khách."],
    ["Không báo tiền về",
     "Đánh dấu một dòng chi tiết là không cần đối chiếu công nợ. Dòng đã đánh dấu sẽ không xuất "
     "hiện ở màn Tổng hợp tiền về ngân hàng."],
    ["Số tiền chưa điều chỉnh",
     "Phần tiền của một dòng chưa được xử lý bằng phiếu yêu cầu điều chỉnh công nợ."],
    ["Hợp đồng nguyên tắc",
     "Loại hợp đồng bán mà mỗi lần thu tiền phải gắn với một phiếu yêu cầu xuất hàng cụ thể, "
     "hoặc phải đánh dấu là thu số dư nợ đầu kì."],
    ["Phiếu YC xuất hàng", "Phiếu yêu cầu xuất hàng."],
])

b.h2("2. Lịch sử cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Nội dung", "Người thực hiện"],
    ["1.0", "05/09/2026", "Ban hành lần đầu cho màn Phiếu báo có và màn Tổng hợp tiền về "
                          "ngân hàng.", "Nhóm phát triển HRM"],
])

b.h2("3. Giới thiệu chung")
b.para("Phiếu báo có là chứng từ kế toán dùng để ghi nhận tiền về tài khoản ngân hàng của công "
       "ty. Mỗi khoản tiền về trên sao kê được lập thành một phiếu, trong phiếu chia thành các "
       "dòng chi tiết; mỗi dòng gắn số tiền với một khách hàng, nhà cung cấp hoặc hợp đồng cụ "
       "thể. Khi kế toán duyệt phiếu, hệ thống ghi bút toán tương ứng vào sổ kế toán.")
b.para("Khoản tiền chưa biết của ai thì để khách hàng KHÁCH KHÔNG RÕ. Sau đó kế toán vào màn "
       "Tổng hợp tiền về ngân hàng, chọn dòng tiền đó và chuyển sang màn Phiếu yêu cầu điều "
       "chỉnh công nợ để gán lại đúng khách hàng và hợp đồng.")
b.para("Phiếu báo có chỉ có hai trạng thái: Đang tạo và Đã duyệt. Không có bước gửi duyệt, "
       "không có từ chối, không có hủy.")
b.para("Đường dẫn màn hình:", bold_prefix="")
b.bullet("Phiếu báo có: menu Tài chính → Quản lý tiền → Thanh toán tiền mặt → Phiếu báo có "
         "(địa chỉ /finance/bill-income-reports).")
b.bullet("Tổng hợp tiền về ngân hàng: menu Tài chính → Quản lý tiền → Thanh toán tiền mặt → "
         "Tổng hợp tiền về ngân hàng (địa chỉ /finance/bill-income-reports/summarize-money).")

b.h2("4. Quyền và phạm vi dữ liệu")
b.para("Màn Phiếu báo có gắn với ba quyền sau. Người dùng chỉ nhìn thấy và làm được đúng phần "
       "quyền mình có.")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút/tab tương ứng trên giao diện", "Ghi chú"],
    ["Quản lý phiếu báo có",
     "Tạo mới, Sửa, Xóa, Duyệt phiếu; Import Excel; tích ô Không báo tiền về.",
     "Nút Tạo mới, nút Import Excel, nút Sửa, nút Xóa, mục Duyệt trong menu hành động, ô tích "
     "Không báo tiền về ở màn chi tiết.",
     "Sửa và Xóa còn phải thỏa: phiếu ở trạng thái Đang tạo và do chính mình lập."],
    ["Xem tất cả phiếu báo có của tổng công ty",
     "Xem phiếu của toàn hệ thống.",
     "Không có nút riêng; quyết định số lượng phiếu nhìn thấy trong danh sách. Có quyền này thì "
     "bộ lọc nâng cao hiện thêm ô Công ty – Phòng ban – Bộ phận.",
     "Chỉ là quyền XEM, không kèm quyền thao tác."],
    ["Xem tất cả phiếu báo có của công ty",
     "Xem phiếu của công ty mình.",
     "Không có nút riêng; quyết định số lượng phiếu nhìn thấy trong danh sách.",
     "Chỉ là quyền XEM, không kèm quyền thao tác."],
])
b.para("Quy tắc chung áp dụng cho mọi người dùng: phiếu ở trạng thái Đang tạo của người khác "
       "luôn bị ẩn, kể cả với người có quyền xem của tổng công ty. Người không có quyền xem "
       "theo cấp nào vẫn vào được màn, nhưng chỉ thấy phiếu do chính mình lập.")
b.para("Nếu không có quyền Quản lý phiếu báo có, các nút Tạo mới, Import Excel, Sửa, Xóa, Duyệt "
       "sẽ không hiển thị; trường hợp truy cập trực tiếp bằng đường dẫn, hệ thống báo lỗi không "
       "có quyền.")

# ============================================ PHAN 1
b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

b.h2("1.1. Cách vào màn hình")
b.para("Bước 1: Đăng nhập hệ thống bằng địa chỉ email và mật khẩu của bạn.")
b.para("Bước 2: Ở trang chọn phân hệ, bấm vào phân hệ Tài chính.")
b.para("Bước 3: Ở thanh menu bên trái, bấm nhóm Quản lý tiền → mục Thanh toán tiền mặt.")
b.para("Bước 4: Bấm dòng Phiếu báo có. Hệ thống mở màn Danh sách phiếu báo có.")
b.para("Muốn vào màn đối chiếu tiền về, bấm dòng Tổng hợp tiền về ngân hàng ngay bên dưới.")

b.h2("1.2. Bố cục màn Danh sách phiếu báo có")
b.image("01-danh-sach.png", "Màn Danh sách phiếu báo có lúc mới vào")
b.para("Màn hình chia làm hai khối:")
b.bullet("Khối trên là Bộ lọc danh sách: ô tìm nhanh theo mã phiếu, nút Tìm kiếm, nút Làm mới, "
         "nút Cài đặt bộ lọc và nút Tìm kiếm nâng cao.")
b.bullet("Khối dưới là bảng danh sách: bên phải tiêu đề bảng có nút Tạo mới, nút Import Excel "
         "và biểu tượng Cấu hình cột hiển thị; dưới bảng là dòng “Hiển thị a–b / N” và phần "
         "chuyển trang.")
b.para("Bảng danh sách rộng hơn màn hình nên có thanh cuộn ngang ở trên và dưới bảng. Kéo thanh "
       "cuộn sang phải để thấy cột Trạng thái và cột Hành động.")
b.image("02-danh-sach-cot-phai.png",
        "Phần bên phải của bảng: cột Trạng thái và cột Hành động")

# ============================================ PHAN 2
b.h1("PHẦN 2: XEM, TÌM KIẾM VÀ TUỲ CHỈNH DANH SÁCH")

b.h2("2.1. Ý nghĩa các cột trong danh sách")
b.table([
    ["Cột", "Nội dung hiển thị"],
    ["STT", "Số thứ tự dòng, chạy liên tục theo trang."],
    ["Mã phiếu", "Mã phiếu báo có. Bấm vào mã để mở màn chi tiết."],
    ["Loại thu", "Thu bán hàng / Thu nhà cung cấp / Thu khác."],
    ["Tổng PS", "Tổng số tiền của phiếu theo loại tiền đã chọn."],
    ["Tỷ giá", "Tỷ giá quy đổi sang đồng Việt Nam. Phiếu tiền Việt luôn là 1."],
    ["Tổng PS VND", "Tổng số tiền quy đổi ra đồng Việt Nam."],
    ["Ghi chú", "Diễn giải chung của phiếu."],
    ["Khách hàng", "Khách hàng (hoặc nhà cung cấp) của dòng chi tiết đầu tiên, dạng Mã - Tên."],
    ["Ngày tạo", "Ngày giờ lập phiếu."],
    ["Ngày hạch toán", "Ngày ghi nhận tiền về ngân hàng."],
    ["Người tạo", "Người lập phiếu."],
    ["Phòng ban", "Phòng ban của người lập. Cột này mặc định ẩn."],
    ["Số TK ngân hàng", "Số tài khoản công ty nhận tiền. Cột này mặc định ẩn."],
    ["Ngày cập nhật", "Lần sửa gần nhất. Cột này mặc định ẩn."],
    ["Người cập nhật", "Người sửa gần nhất. Cột này mặc định ẩn."],
    ["Trạng thái", "Đang tạo (nhãn xám) hoặc Đã duyệt (nhãn xanh)."],
    ["Hành động", "Các nút thao tác của dòng, hiện theo trạng thái phiếu và quyền của bạn."],
])
b.para("Các cột Mã phiếu, Tổng PS, Tổng PS VND, Ngày tạo, Ngày hạch toán có biểu tượng hai mũi "
       "tên ở tiêu đề: bấm vào để sắp xếp tăng dần hoặc giảm dần. Mặc định danh sách sắp xếp "
       "phiếu mới nhất lên trước.")

b.h2("2.2. Tìm nhanh theo mã phiếu")
b.para("Bước 1: Gõ một phần mã phiếu vào ô “Tìm theo mã phiếu...”.")
b.para("Bước 2: Bấm nút Tìm kiếm (hoặc nhấn phím Enter). Lưu ý ô này chỉ chạy khi bấm nút, "
       "gõ xong mà không bấm thì danh sách chưa đổi.")
b.para("Bước 3: Muốn xóa điều kiện, bấm nút Làm mới — hệ thống xóa mọi điều kiện lọc và tải "
       "lại danh sách đầy đủ.")

b.h2("2.3. Bộ lọc nâng cao")
b.para("Bấm nút Tìm kiếm nâng cao ở góc phải khối lọc để mở bảng lọc. Bấm lần nữa (nút đổi chữ "
       "thành Ẩn tìm kiếm nâng cao) để thu gọn lại.")
b.image("03-bo-loc-nang-cao.png", "Bảng tìm kiếm nâng cao của màn Phiếu báo có")
b.para("Các ô trong bảng lọc tự chạy ngay khi bạn chọn hoặc nhập xong, không cần bấm Tìm kiếm.")
b.table([
    ["Ô lọc", "Cách dùng"],
    ["Công ty – Phòng ban – Bộ phận",
     "Chỉ hiện với người có quyền xem tất cả phiếu báo có của tổng công ty hoặc của công ty. "
     "Chọn đơn vị để xem phiếu của đơn vị đó."],
    ["Loại thu", "Chọn một trong ba loại: Thu bán hàng, Thu nhà cung cấp, Thu khác."],
    ["Trạng thái", "Chọn Đang tạo hoặc Đã duyệt."],
    ["Người tạo", "Chọn nhân viên đã lập phiếu. Đây là cách xem “phiếu của tôi”: chọn chính mình."],
    ["Ngân hàng", "Chọn ngân hàng nhận tiền."],
    ["Tài khoản ngân hàng", "Gõ một phần số tài khoản của công ty."],
    ["Khách hàng", "Gõ tối thiểu 2 ký tự để hệ thống gợi ý, rồi chọn khách trong danh sách."],
    ["Tên khách hàng (gõ tay)",
     "Gõ mã hoặc tên khách hàng khi bạn không muốn chọn từ danh sách gợi ý."],
    ["Ghi chú", "Gõ một phần diễn giải chung của phiếu."],
    ["Không báo tiền về",
     "Chọn “Có” để xem các phiếu có ít nhất một dòng đã đánh dấu không báo tiền về; chọn “Không” "
     "để xem các phiếu không có dòng nào đánh dấu."],
    ["Hạch toán từ / Hạch toán đến", "Chọn khoảng ngày hạch toán. Lấy cả ngày đầu và ngày cuối."],
    ["Ngày tạo từ / Ngày tạo đến", "Chọn khoảng ngày lập phiếu. Lấy cả ngày đầu và ngày cuối."],
])
b.para("Hệ thống ghi nhớ bộ lọc bạn vừa dùng trong 10 phút. Nếu bạn sang màn khác rồi quay lại "
       "trong khoảng thời gian đó, bộ lọc cũ vẫn còn nguyên. Muốn xem lại toàn bộ danh sách thì "
       "bấm Làm mới.")

b.h2("2.4. Cài đặt bộ lọc (chọn ô lọc nào được hiện)")
b.para("Bước 1: Bấm nút Cài đặt bộ lọc.")
b.image("04-cai-dat-bo-loc.png", "Cửa sổ Cài đặt bộ lọc")
b.para("Bước 2: Cửa sổ liệt kê 12 tiêu chí lọc của màn. Bỏ tích tiêu chí bạn không dùng để bảng "
       "lọc gọn lại; tích lại khi cần dùng.")
b.para("Bước 3: Muốn đổi thứ tự, giữ chuột vào biểu tượng sáu chấm bên trái tên tiêu chí rồi kéo "
       "lên hoặc xuống.")
b.para("Bước 4: Bấm Lưu. Hệ thống báo “Cập nhật thành công” và vẽ lại bảng lọc. Cài đặt này lưu "
       "riêng cho tài khoản của bạn.")
b.para("Bấm Khôi phục mặc định để đưa danh sách tiêu chí về như ban đầu. Bấm Đóng để thoát mà "
       "không lưu.")
b.para("Lưu ý: khi bạn bỏ tích một tiêu chí đang có giá trị, hệ thống xóa luôn giá trị đó để "
       "danh sách không bị lọc ngầm bởi ô mà bạn không nhìn thấy.")

b.h2("2.5. Tuỳ chỉnh cột hiển thị")
b.para("Bước 1: Bấm biểu tượng cột (hình khung chia đôi) ở bên phải nút Import Excel.")
b.image("05-cau-hinh-cot.png", "Cửa sổ Tuỳ chỉnh cột")
b.para("Bước 2: Tích để hiện cột, bỏ tích để ẩn cột. Bốn cột Phòng ban, Số TK ngân hàng, "
       "Ngày cập nhật, Người cập nhật mặc định đang tắt — tích vào nếu bạn cần theo dõi.")
b.para("Bước 3: Muốn đổi thứ tự cột, kéo biểu tượng sáu chấm bên phải mỗi dòng.")
b.para("Bước 4: Bấm Lưu. Ba cột STT, Mã phiếu và Hành động có biểu tượng ổ khóa: đây là cột bắt "
       "buộc, không ẩn và không đổi vị trí được.")

b.h2("2.6. Các nút trên thanh công cụ của bảng")
b.table([
    ["Nút", "Công dụng", "Quyền yêu cầu"],
    ["Tạo mới", "Mở màn lập phiếu báo có mới.", "Quản lý phiếu báo có"],
    ["Import Excel", "Nạp file sao kê ngân hàng để tạo hàng loạt phiếu.", "Quản lý phiếu báo có"],
    ["Biểu tượng cột", "Mở cửa sổ Tuỳ chỉnh cột hiển thị.", "Không yêu cầu quyền"],
])

b.h2("2.7. Thao tác trên từng dòng của danh sách")
b.para("Cột Hành động nằm ở cuối bảng (kéo thanh cuộn ngang sang phải để thấy). Các nút chỉ hiện "
       "khi bạn được phép làm thao tác đó — nút không dùng được thì hệ thống ẩn hẳn chứ không "
       "hiện nút mờ.")
b.image("18-menu-hanh-dong.png", "Menu hành động của một dòng phiếu ở trạng thái Đang tạo")
b.table([
    ["Nút", "Điều kiện hiển thị", "Bấm vào thì sao"],
    ["Biểu tượng bút chì (Sửa)",
     "Phiếu Đang tạo, do chính bạn lập, và bạn có quyền Quản lý phiếu báo có.",
     "Mở màn Sửa phiếu báo có."],
    ["Biểu tượng thùng rác (Xóa)",
     "Cùng điều kiện với nút Sửa.",
     "Mở hộp xác nhận xóa phiếu."],
    ["Dấu ba chấm → Duyệt",
     "Phiếu Đang tạo và bạn có quyền Quản lý phiếu báo có (không bắt buộc là người lập).",
     "Mở hộp xác nhận duyệt phiếu."],
    ["Dấu ba chấm → Lịch sử", "Luôn hiện với mọi phiếu bạn xem được.",
     "Mở cửa sổ Lịch sử thay đổi của phiếu."],
])

# ============================================ PHAN 3
b.h1("PHẦN 3: TẠO MỚI PHIẾU BÁO CÓ")

b.h2("3.1. Mở màn tạo mới")
b.para("Ở màn danh sách, bấm nút Tạo mới. Hệ thống mở màn “Thêm phiếu báo có” gồm hai khối: "
       "Thông tin chung ở trên và bảng Chi tiết ở dưới; thanh nút nằm cố định ở đáy màn hình.")
b.para("Yêu cầu quyền: Quản lý phiếu báo có. Không có quyền này thì nút Tạo mới không hiển thị.")
b.image("06-form-tao-moi.png", "Màn Thêm phiếu báo có ngay khi vừa mở")

b.h2("3.2. Khối Thông tin chung — từng trường một")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn khi tạo mới", "Ghi chú"],
    ["Loại thu", "Chọn trong danh sách", "Có", "Thu bán hàng",
     "Ba lựa chọn: Thu bán hàng, Thu nhà cung cấp, Thu khác. Đổi loại thu sẽ xóa hết dòng chi "
     "tiết đang nhập (hệ thống hỏi lại trước khi xóa)."],
    ["Tài khoản nợ", "Chọn trong danh sách", "Có", "1121 - Tiền Việt Nam",
     "Tài khoản ghi Nợ của bút toán, thường là tài khoản tiền gửi ngân hàng."],
    ["Loại tiền", "Chọn trong danh sách", "Có", "VNĐ",
     "Chọn ngoại tệ thì ô Tỷ giá mở khóa và bảng chi tiết hiện thêm cột Số tiền (VND)."],
    ["Tỷ giá (VND)", "Nhập số", "Có", "1",
     "Bị khóa khi loại tiền là VNĐ. Đổi tỷ giá thì cột quy đổi của mọi dòng tính lại ngay."],
    ["Ngày hạch toán", "Chọn ngày", "Có", "Ngày hiện tại",
     "Ngày tiền về ngân hàng, cũng là ngày ghi sổ của bút toán."],
    ["Ngân hàng", "Chọn trong danh sách", "Có", "Trống",
     "Chọn ngân hàng trước thì mới chọn được tài khoản."],
    ["Tài khoản", "Chọn trong danh sách", "Có", "Trống",
     "Bị khóa cho tới khi chọn Ngân hàng. Danh sách chỉ gồm tài khoản của ngân hàng đã chọn."],
    ["Chi nhánh", "Hệ thống tự điền", "Không", "Trống",
     "Tự điền theo tài khoản vừa chọn, không sửa tay được."],
    ["Diễn giải", "Nhập chữ", "Không", "Trống",
     "Diễn giải chung của phiếu, tối đa 500 ký tự."],
])
b.para("Giá trị điền sẵn khi tạo mới: Loại thu là Thu bán hàng; Tài khoản nợ là 1121 - Tiền Việt "
       "Nam; Loại tiền là VNĐ; Tỷ giá là 1; Ngày hạch toán là ngày hôm nay; bảng Chi tiết đã có "
       "sẵn một dòng trống với Số tài khoản có là 1311 và Khách hàng là KHÁCH KHÔNG RÕ.")
b.para("Riêng ở màn Sửa, khối này hiện thêm ba ô chỉ đọc: Mã phiếu, Người lập và Phòng ban.")

b.h2("3.3. Chọn Loại thu")
b.para("Bước 1: Bấm vào ô Loại thu. Danh sách xổ xuống ba lựa chọn.")
b.image("10-dropdown-loai-thu.png", "Danh sách lựa chọn của ô Loại thu")
b.para("Bước 2: Bấm vào loại thu cần dùng. Nếu bảng Chi tiết đã có số tiền, hợp đồng hoặc diễn "
       "giải, hệ thống hỏi: “Đổi loại thu sẽ xóa toàn bộ dòng chi tiết đang nhập. Bạn có chắc "
       "chắn?”. Bấm Đồng ý để đổi (mất dữ liệu đang nhập) hoặc Hủy để giữ nguyên.")
b.para("Loại thu quyết định bảng Chi tiết có cột nào:")
b.bullet("Thu bán hàng: có cột Khách hàng (bắt buộc), Số đơn hàng/Hợp đồng, Phiếu YC xuất hàng, "
         "NVKD. Số tài khoản có mặc định là 1311.")
b.bullet("Thu nhà cung cấp: có cột Nhà cung cấp (bắt buộc), Phiếu xuất hàng, Hợp đồng mua, NVKD. "
         "Số tài khoản có mặc định là 3311.")
b.bullet("Thu khác: chỉ có cột Khách hàng và không bắt buộc chọn. Không có tài khoản có mặc định.")

b.h2("3.4. Chọn Ngân hàng và Tài khoản")
b.para("Bước 1: Bấm ô Ngân hàng, chọn ngân hàng nhận tiền.")
b.para("Bước 2: Bấm ô Tài khoản (lúc này đã mở khóa), chọn số tài khoản của công ty.")
b.para("Bước 3: Ô Chi nhánh tự điền theo tài khoản đã chọn.")
b.para("Lưu ý: nếu đổi lại Ngân hàng, hệ thống xóa Tài khoản và Chi nhánh đã chọn, bạn phải chọn "
       "lại từ đầu.")

b.h2("3.5. Nhập bảng Chi tiết")
b.para("Bảng Chi tiết nằm ngay dưới khối Thông tin chung. Bảng rộng hơn màn hình nên có thanh "
       "cuộn ngang ở trên và dưới bảng; kéo sang phải để thấy các cột Số tiền, Diễn giải, "
       "Không báo tiền về và nút xóa dòng.")
b.image("07-form-bang-chi-tiet-phai.png",
        "Phần bên phải bảng Chi tiết: Số tiền, Diễn giải, Không báo tiền về và nút xóa dòng")
b.para("Bấm nút Thêm dòng (góc phải tiêu đề khối Chi tiết) để thêm dòng mới. Dòng mới tự điền "
       "Số tài khoản có theo loại thu và điền sẵn đối tượng KHÁCH KHÔNG RÕ.")
b.table([
    ["Cột", "Kiểu nhập", "Bắt buộc", "Giá trị điền sẵn", "Ghi chú"],
    ["Số tài khoản có", "Chọn trong danh sách", "Có",
     "1311 (Thu bán hàng) / 3311 (Thu nhà cung cấp) / trống (Thu khác)",
     "Tài khoản ghi Có của dòng."],
    ["Tên tài khoản", "Hệ thống tự điền", "–", "Theo tài khoản đã chọn", "Chỉ để xem."],
    ["Khách hàng", "Bấm để mở cửa sổ chọn", "Có với Thu bán hàng", "29TPHPTH-203 (KHÁCH KHÔNG RÕ)",
     "Chỉ hiện với loại thu Thu bán hàng và Thu khác."],
    ["Tên khách hàng", "Hệ thống tự điền", "–", "KHÁCH KHÔNG RÕ", "Chỉ để xem."],
    ["Nhà cung cấp", "Bấm để mở cửa sổ chọn", "Có với Thu nhà cung cấp", "KHÁCH KHÔNG RÕ",
     "Chỉ hiện với loại thu Thu nhà cung cấp."],
    ["Số đơn hàng/Hợp đồng", "Bấm để mở cửa sổ chọn",
     "Có khi tài khoản có là tài khoản công nợ và khách hàng khác KHÁCH KHÔNG RÕ", "Trống",
     "Phải chọn khách hàng trước."],
    ["Phiếu YC xuất hàng", "Bấm để mở cửa sổ chọn",
     "Có khi hợp đồng là hợp đồng nguyên tắc và không tích dư nợ đầu kì", "Trống",
     "Chỉ hiện khi hợp đồng đã chọn là hợp đồng nguyên tắc."],
    ["Phiếu xuất hàng", "Bấm để mở cửa sổ chọn", "Không", "Trống",
     "Chỉ hiện với loại thu Thu nhà cung cấp. Chọn xong hệ thống tự điền Hợp đồng mua và NVKD."],
    ["Hợp đồng mua", "Hệ thống tự điền", "–", "Trống", "Theo phiếu xuất hàng đã chọn."],
    ["NVKD", "Hệ thống tự điền", "–", "Trống", "Người tạo hợp đồng gắn với dòng."],
    ["Số tiền", "Nhập số", "Có", "0", "Phải lớn hơn 0."],
    ["Số tiền (VND)", "Hệ thống tự tính", "–", "0",
     "Chỉ hiện khi loại tiền là ngoại tệ; bằng Số tiền nhân Tỷ giá."],
    ["Diễn giải", "Nhập chữ", "Có", "Trống", "Tối đa 500 ký tự."],
    ["Không báo tiền về", "Ô tích", "Không", "Không tích",
     "Tích vào thì dòng này không xuất hiện ở màn Tổng hợp tiền về ngân hàng."],
    ["Nút thùng rác", "Bấm", "–", "–", "Xóa dòng khỏi bảng."],
])
b.para("Dòng cuối bảng là dòng Tổng cộng: hệ thống tự cộng số tiền của mọi dòng và cập nhật ngay "
       "khi bạn gõ.")

b.h2("3.6. Chọn khách hàng cho dòng chi tiết")
b.para("Bước 1: Bấm vào ô ở cột Khách hàng của dòng cần sửa (ô có chữ gợi ý “Nhấn để chọn khách "
       "hàng”). Cửa sổ Chọn khách hàng mở ra.")
b.image("08-popup-chon-khach-hang.png", "Cửa sổ Chọn khách hàng")
b.para("Bước 2: Gõ tên hoặc mã khách hàng vào ô “Tên / Mã khách hàng” (hoặc dùng ô Mã số thuế, "
       "ô Số điện thoại) rồi bấm Tìm kiếm.")
b.para("Bước 3: Bấm vào dòng khách hàng cần chọn. Cửa sổ đóng lại, ô Khách hàng điền mã khách, "
       "ô Tên khách hàng điền tên đầy đủ.")
b.para("Lưu ý: đổi khách hàng thì hợp đồng và phiếu yêu cầu xuất hàng đã chọn trước đó trên dòng "
       "sẽ bị xóa, bạn phải chọn lại cho khớp khách mới.")

b.h2("3.7. Chọn đơn hàng / hợp đồng")
b.para("Bước 1: Bấm ô ở cột Số đơn hàng/Hợp đồng. Nếu chưa chọn khách hàng, hệ thống báo "
       "“Chưa chọn khách hàng” và không mở cửa sổ.")
b.image("09-popup-chon-hop-dong.png",
        "Cửa sổ Chọn đơn hàng/hợp đồng — tiêu đề ghi rõ khách hàng đang chọn")
b.para("Bước 2: Cửa sổ chỉ liệt kê hợp đồng của đúng khách hàng đó, kèm Ngày lập, Giá trị hợp "
       "đồng và Số tiền còn nợ. Gõ số hợp đồng vào ô tìm kiếm nếu danh sách dài.")
b.para("Bước 3: Bấm vào dòng hợp đồng cần chọn. Hệ thống điền số hợp đồng vào dòng chi tiết và "
       "điền tên nhân viên kinh doanh vào cột NVKD.")
b.para("Bước 4: Nếu hợp đồng vừa chọn là hợp đồng nguyên tắc, ngay dưới ô hợp đồng xuất hiện ô "
       "tích “Số dư nợ đầu kì: <số tiền>”. Có hai cách xử lý:")
b.bullet("Khoản tiền này là thu dư nợ đầu kỳ: tích vào ô đó, không cần chọn phiếu yêu cầu "
         "xuất hàng.")
b.bullet("Khoản tiền này thu theo một lần xuất hàng cụ thể: để trống ô tích, rồi bấm ô ở cột "
         "Phiếu YC xuất hàng, chọn phiếu tương ứng trong cửa sổ hiện ra.")
b.para("Lưu ý: một hợp đồng chỉ được chọn ở một dòng trong cùng một phiếu; hợp đồng đã dùng ở "
       "dòng khác sẽ không chọn lại được.")

b.h2("3.8. Phiếu loại Thu nhà cung cấp")
b.para("Chọn Loại thu là Thu nhà cung cấp, bảng Chi tiết đổi sang bộ cột của nhà cung cấp.")
b.image("11-form-loai-thu-ncc.png", "Bảng Chi tiết của loại thu Thu nhà cung cấp")
b.para("Bước 1: Bấm ô ở cột Nhà cung cấp, cửa sổ Chọn nhà cung cấp mở ra. Gõ mã hoặc tên nhà "
       "cung cấp rồi bấm Tìm kiếm, sau đó bấm vào dòng cần chọn.")
b.image("12-popup-chon-ncc.png", "Cửa sổ Chọn nhà cung cấp")
b.para("Bước 2: Bấm ô ở cột Phiếu xuất hàng. Nếu chưa chọn nhà cung cấp, hệ thống báo "
       "“Chưa chọn nhà cung cấp”. Cửa sổ chỉ liệt kê phiếu xuất trả hàng cho đúng nhà cung cấp "
       "đó; nhà cung cấp không có phiếu nào thì cửa sổ hiện “Không có phiếu xuất phù hợp.”")
b.image("13-popup-chon-phieu-xuat.png", "Cửa sổ Chọn phiếu xuất hàng")
b.para("Bước 3: Bấm vào dòng phiếu xuất. Hệ thống tự điền Hợp đồng mua và NVKD cho dòng. Nếu "
       "phiếu xuất không có hợp đồng mua tương ứng, hệ thống báo lỗi và không điền gì.")
b.para("Lưu ý: không chọn trùng một phiếu xuất ở hai dòng; hệ thống sẽ báo “Phiếu đã tồn tại!”.")

b.h2("3.9. Phiếu loại Thu khác")
b.para("Chọn Loại thu là Thu khác khi khoản tiền về không gắn với bán hàng hay nhà cung cấp. "
       "Bảng Chi tiết lúc này chỉ còn cột Khách hàng (không bắt buộc), Số tiền và Diễn giải; "
       "bạn phải tự chọn Số tài khoản có vì không có giá trị mặc định.")
b.image("14-form-loai-thu-khac.png", "Bảng Chi tiết của loại thu Thu khác")

b.h2("3.10. Lưu phiếu")
b.para("Thanh nút ở đáy màn hình có bốn nút:")
b.table([
    ["Nút", "Bấm vào thì sao"],
    ["Lưu", "Lưu phiếu ở trạng thái Đang tạo. Hệ thống sinh mã phiếu, báo “Thêm phiếu báo có "
            "thành công!” rồi quay về danh sách. Phiếu vẫn sửa và xóa được."],
    ["Lưu và duyệt", "Hệ thống hỏi xác nhận, sau đó lưu phiếu, chuyển sang trạng thái Đã duyệt "
                     "và GHI BÚT TOÁN VÀO SỔ CÁI ngay. Sau bước này phiếu không sửa, không xóa "
                     "được nữa."],
    ["Lưu và tiếp tục", "Lưu phiếu ở trạng thái Đang tạo rồi ở lại màn Tạo mới với form trống, "
                        "tiện khi nhập nhiều phiếu liên tiếp."],
    ["Quay lại", "Về màn danh sách. Nếu bạn đã nhập gì đó mà chưa lưu, hệ thống hỏi lại trước "
                 "khi rời trang."],
])
b.para("Mã phiếu do hệ thống tự sinh theo dạng: mã công ty + “.PBC” + tháng năm + số thứ tự "
       "(ví dụ TPE.PBC0926.00004). Bạn không nhập mã.")

b.h2("3.11. Các lỗi thường gặp khi lưu")
b.para("Khi thiếu thông tin bắt buộc, hệ thống không rời màn và hiện chữ đỏ ngay dưới từng ô "
       "bị lỗi, dữ liệu bạn đã nhập vẫn còn nguyên.")
b.image("15-loi-bat-buoc.png", "Các thông báo lỗi hiện ngay dưới từng ô bị thiếu")
b.table([
    ["Thông báo", "Nguyên nhân và cách xử lý"],
    ["Bắt buộc chọn (dưới ô Ngân hàng / Tài khoản / Loại thu / Tài khoản nợ / Loại tiền)",
     "Chưa chọn giá trị cho ô đó. Chọn rồi lưu lại."],
    ["Bắt buộc chọn (dưới ô Số tài khoản có của dòng)",
     "Dòng chi tiết chưa chọn tài khoản có — hay gặp ở loại thu Thu khác vì không có giá trị "
     "mặc định."],
    ["Số tiền phải lớn hơn 0", "Ô Số tiền của dòng đang để 0. Nhập số tiền thật của dòng."],
    ["Bắt buộc nhập (dưới ô Diễn giải của dòng)", "Mỗi dòng chi tiết phải có diễn giải."],
    ["Tối đa 500 ký tự", "Diễn giải quá dài, rút ngắn lại."],
    ["Bắt buộc chọn (dưới ô Khách hàng / Nhà cung cấp)",
     "Phiếu Thu bán hàng phải chọn khách hàng; phiếu Thu nhà cung cấp phải chọn nhà cung cấp."],
    ["Bắt buộc chọn (dưới ô Số đơn hàng/Hợp đồng)",
     "Dòng có tài khoản công nợ và khách hàng cụ thể thì bắt buộc gắn hợp đồng."],
    ["Bắt buộc chọn (dưới ô Phiếu YC xuất hàng)",
     "Hợp đồng nguyên tắc mà chưa tích dư nợ đầu kì thì phải chọn phiếu yêu cầu xuất hàng."],
    ["Phải có ít nhất 1 dòng chi tiết", "Bạn đã xóa hết dòng. Bấm Thêm dòng và nhập lại."],
    ["Không đúng định dạng (dưới ô Ngày hạch toán)",
     "Ngày nhập tay không hợp lệ. Bấm biểu tượng lịch để chọn ngày."],
])

# ============================================ PHAN 4
b.h1("PHẦN 4: SỬA, XEM CHI TIẾT, DUYỆT VÀ XÓA PHIẾU")

b.h2("4.1. Sửa phiếu")
b.para("Yêu cầu: phiếu ở trạng thái Đang tạo, do chính bạn lập, và bạn có quyền Quản lý phiếu "
       "báo có. Không thỏa một trong ba điều kiện thì nút Sửa không hiển thị.")
b.para("Bước 1: Ở danh sách, kéo thanh cuộn ngang sang phải rồi bấm biểu tượng bút chì của dòng "
       "cần sửa; hoặc mở màn chi tiết rồi bấm nút Sửa ở thanh dưới cùng.")
b.image("22-man-sua.png", "Màn Sửa phiếu báo có")
b.para("Bước 2: Màn Sửa có bố cục giống hệt màn Tạo mới, dữ liệu đã được điền sẵn. Ba ô Mã phiếu, "
       "Người lập, Phòng ban chỉ để xem, không sửa được.")
b.para("Bước 3: Sửa thông tin chung hoặc bảng chi tiết (thêm dòng, xóa dòng, đổi số tiền…).")
b.para("Bước 4: Bấm Lưu để giữ trạng thái Đang tạo, hoặc Lưu và duyệt để duyệt luôn. Hệ thống báo "
       "“Cập nhật phiếu báo có thành công!” rồi quay về danh sách.")
b.para("Nếu bạn mở màn Sửa bằng đường dẫn trực tiếp trong khi phiếu đã được duyệt (hoặc không "
       "phải phiếu của bạn), hệ thống tự chuyển sang màn chi tiết. Nếu phiếu vừa bị xóa ở nơi "
       "khác, hệ thống báo “Không tìm thấy dữ liệu”.")

b.h2("4.2. Xem chi tiết phiếu")
b.para("Bấm vào Mã phiếu ở danh sách để mở màn chi tiết.")
b.image("19-chi-tiet.png", "Màn Chi tiết phiếu báo có")
b.para("Màn chi tiết gồm bốn phần từ trên xuống:")
b.bullet("Khối Thông tin chung và bảng Chi tiết — hiển thị đúng như lúc nhập nhưng ở chế độ "
         "chỉ đọc.")
b.bullet("Khối Đánh dấu không báo tiền về — bảng liệt kê từng dòng chi tiết kèm ô tích.")
b.bullet("Khối Lịch sử — bấm “Xem lịch sử” để mở.")
b.bullet("Thanh nút dưới cùng — Sửa, Duyệt, Tạo phiếu yêu cầu điều chỉnh công nợ, Xóa, Quay lại. "
         "Các nút chỉ hiện khi bạn được phép làm thao tác đó.")

b.h2("4.3. Duyệt phiếu")
b.para("Yêu cầu: phiếu ở trạng thái Đang tạo và bạn có quyền Quản lý phiếu báo có. Bạn không "
       "nhất thiết phải là người lập phiếu.")
b.para("Bước 1: Bấm nút Duyệt ở màn chi tiết; hoặc ở danh sách bấm dấu ba chấm của dòng rồi chọn "
       "Duyệt.")
b.image("21-xac-nhan-duyet.png", "Hộp xác nhận duyệt phiếu")
b.para("Bước 2: Đọc kỹ nội dung hộp xác nhận: “Duyệt phiếu báo có ‘<mã phiếu>’? Hệ thống sẽ ghi "
       "bút toán vào sổ cái và phiếu không sửa/xóa được nữa.”")
b.para("Bước 3: Bấm Duyệt để xác nhận, hoặc Hủy để đóng hộp thoại mà không làm gì.")
b.para("Sau khi duyệt: phiếu chuyển sang trạng thái Đã duyệt, hệ thống ghi bút toán vào sổ kế "
       "toán, ghi lại một mốc trong Lịch sử và gửi thông báo cho những người có quyền Quản lý "
       "phiếu báo có trong cùng công ty. Hệ thống báo “Duyệt phiếu báo có thành công.”")
b.para("Cảnh báo: đây là thao tác không hoàn tác được. Nếu hai người cùng bấm Duyệt một phiếu, "
       "chỉ lần bấm đầu tiên có hiệu lực; lần sau hệ thống báo phiếu không còn ở trạng thái "
       "Đang tạo.")

b.h2("4.4. Xóa phiếu")
b.para("Yêu cầu: giống nút Sửa — phiếu Đang tạo, do chính bạn lập, và bạn có quyền Quản lý "
       "phiếu báo có. Phiếu đã duyệt không xóa được vì đã ghi vào sổ kế toán.")
b.para("Bước 1: Bấm biểu tượng thùng rác ở dòng danh sách, hoặc nút Xóa (màu đỏ) ở màn chi tiết.")
b.image("17-xac-nhan-xoa.png", "Hộp xác nhận xóa phiếu")
b.para("Bước 2: Hộp thoại hỏi “Bạn có chắc muốn xóa phiếu báo có ‘<mã phiếu>’?”. Bấm Xóa để xác "
       "nhận hoặc Hủy để thoát.")
b.para("Sau khi xóa: hệ thống xóa cả phiếu lẫn các dòng chi tiết, báo “Xóa thành công.” và tải "
       "lại danh sách. Phiếu đã xóa không khôi phục được.")

b.h2("4.5. Đánh dấu không báo tiền về")
b.para("Yêu cầu: bạn xem được phiếu và có quyền Quản lý phiếu báo có. Không có quyền thì ô tích "
       "bị khóa.")
b.para("Bước 1: Mở màn chi tiết phiếu, kéo xuống khối “Đánh dấu không báo tiền về”.")
b.para("Bước 2: Tích ô ở cột Không báo tiền về của dòng bạn không cần đối chiếu công nợ.")
b.para("Bước 3: Hệ thống lưu ngay, báo “Cập nhật thành công.” — không cần bấm nút Lưu nào khác.")
b.para("Ý nghĩa: dòng đã đánh dấu sẽ biến mất khỏi màn Tổng hợp tiền về ngân hàng, tức là kế "
       "toán không phải đối chiếu công nợ cho khoản tiền đó nữa. Bỏ tích thì dòng xuất hiện trở "
       "lại. Mọi lần bật/tắt đều được ghi vào Lịch sử.")

b.h2("4.6. Xem lịch sử thay đổi")
b.para("Cách 1 — từ danh sách: bấm dấu ba chấm ở cột Hành động rồi chọn Lịch sử.")
b.image("23-popup-lich-su.png", "Cửa sổ Lịch sử thay đổi của một phiếu đã duyệt")
b.para("Cách 2 — từ màn chi tiết: kéo xuống cuối trang, bấm nút “Xem lịch sử”.")
b.image("20-khoi-lich-su.png", "Khối Lịch sử ở màn chi tiết")
b.para("Mỗi mốc trong lịch sử cho biết: thời điểm, loại thao tác (Tạo mới, Chỉnh sửa, Thay đổi "
       "trạng thái, Xóa, Import), người thực hiện kèm phòng ban, và những gì đã thay đổi theo "
       "dạng “giá trị cũ → giá trị mới”. Thay đổi ở bảng chi tiết được ghi theo từng dòng: dòng "
       "thêm mới, dòng bị bỏ, dòng bị sửa cột nào.")
b.para("Phiếu chưa có thao tác nào được ghi nhận thì khối lịch sử hiện “Chưa có lịch sử thao "
       "tác”. Bấm nút Bộ lọc trong cửa sổ để lọc theo nhóm thao tác hoặc khoảng thời gian.")

# ============================================ PHAN 5
b.h1("PHẦN 5: IMPORT EXCEL SAO KÊ NGÂN HÀNG")

b.h2("5.1. Khi nào dùng")
b.para("Dùng khi bạn có file sao kê ngân hàng nhiều dòng và muốn tạo nhanh hàng loạt phiếu báo "
       "có. Mỗi dòng trong file trở thành MỘT phiếu báo có loại Thu bán hàng, gắn khách hàng "
       "KHÁCH KHÔNG RÕ, và phiếu đó được duyệt cùng ghi bút toán vào sổ cái ngay.")
b.para("Vì vậy phải kiểm tra file thật kỹ trước khi bấm Import: dữ liệu sai vẫn tạo ra bút toán "
       "trong sổ kế toán. Sau khi import xong, dùng màn Tổng hợp tiền về ngân hàng để gán lại "
       "đúng khách hàng cho từng khoản tiền.")
b.para("Yêu cầu quyền: Quản lý phiếu báo có.")

b.h2("5.2. Các bước import")
b.para("Bước 1: Ở màn danh sách, bấm nút Import Excel. Cửa sổ Import phiếu báo có mở ra.")
b.image("16-import-buoc-1.png", "Cửa sổ Import phiếu báo có")
b.para("Bước 2: Bấm “Tải file mẫu” để tải file Mau_import_phieu_bao_co.xlsx. File mẫu có một "
       "dòng tiêu đề và một dòng ví dụ; hãy điền dữ liệu ngay bên dưới và giữ nguyên dòng tiêu "
       "đề, không thêm dòng ghi chú nào.")
b.para("Bước 3: Bấm “Chọn file Excel”, chọn file đã điền trên máy của bạn.")
b.para("Bước 4: Bấm “Load lên bảng”. Dữ liệu trong file hiện lên bảng xem trước, bạn sửa trực "
       "tiếp trên bảng được.")
b.para("Bước 5: Bấm “Validate”. Hệ thống kiểm tra từng dòng và báo “Kiểm tra xong: X dòng hợp lệ, "
       "Y dòng lỗi”; dòng lỗi được đánh dấu kèm lý do. Bấm “Chỉ dòng lỗi” để lọc nhanh các dòng "
       "cần sửa.")
b.para("Bước 6: Sửa các dòng lỗi rồi bấm Validate lại cho tới khi hết lỗi (hoặc chấp nhận bỏ qua "
       "dòng lỗi).")
b.para("Bước 7: Bấm “Import”. Hệ thống tạo phiếu cho các dòng hợp lệ và báo “Import thành công "
       "X phiếu báo có!”. Danh sách phía sau tự tải lại.")

b.h2("5.3. Các cột trong file import")
b.table([
    ["Cột trong file", "Bắt buộc", "Cách điền"],
    ["Số tiền", "Có", "Số tiền về tài khoản, phải lớn hơn 0. Điền được cả dạng 1.500.000 hoặc "
                      "1,500,000."],
    ["Diễn giải", "Không", "Nội dung giao dịch trên sao kê. Dùng làm diễn giải của phiếu và của "
                           "dòng chi tiết."],
    ["Ngày hạch toán", "Có", "Dạng dd/mm/yyyy (ví dụ 05/09/2026) hoặc yyyy-mm-dd."],
    ["Mã ngân hàng", "Có", "Mã ngân hàng đúng như trong danh mục, ví dụ VIETINBANK."],
    ["Số tài khoản", "Có", "Số tài khoản của công ty đã khai trong danh mục."],
    ["Tên chi nhánh", "Có", "Tên chi nhánh đúng như trong danh mục, ví dụ CN Ha Noi."],
    ["Loại tiền", "Có", "Mã loại tiền, ví dụ VNĐ."],
    ["Tỷ giá", "Không", "Bỏ trống thì hệ thống lấy tỷ giá của loại tiền."],
])

b.h2("5.4. Các lỗi thường gặp khi import")
b.table([
    ["Thông báo lỗi", "Cách xử lý"],
    ["Số tiền phải lớn hơn 0", "Ô số tiền để trống, bằng 0 hoặc không phải số."],
    ["Ngày hạch toán không đúng định dạng",
     "Ngày sai định dạng hoặc là ngày không có thật (ví dụ 31/02). Điền lại theo dd/mm/yyyy."],
    ["Ngân hàng không tồn tại", "Mã ngân hàng sai. Đối chiếu lại danh mục ngân hàng."],
    ["Số tài khoản không tồn tại",
     "Số tài khoản chưa được khai trong danh mục tài khoản công ty."],
    ["Tên chi nhánh không tồn tại", "Tên chi nhánh phải trùng đúng với danh mục."],
    ["Loại tiền không tồn tại", "Mã loại tiền sai."],
    ["Tỷ giá phải lớn hơn 0", "Nếu điền tỷ giá thì phải là số dương; không chắc thì để trống."],
    ["File quá lớn (tối đa 500 dòng)", "Tách file thành nhiều phần, mỗi phần tối đa 500 dòng."],
])

# ============================================ PHAN 6
b.h1("PHẦN 6: TỔNG HỢP TIỀN VỀ NGÂN HÀNG")

b.h2("6.1. Màn này để làm gì")
b.para("Màn Tổng hợp tiền về ngân hàng liệt kê từng DÒNG CHI TIẾT của các phiếu báo có đã duyệt, "
       "để kế toán đối chiếu khoản tiền về với công nợ. Từ đây bạn tích chọn những khoản chưa "
       "gán đúng đối tượng rồi chuyển sang màn Phiếu yêu cầu điều chỉnh công nợ.")
b.para("Một dòng chỉ xuất hiện ở màn này khi thỏa đủ bốn điều kiện: phiếu cha đã duyệt; tài "
       "khoản có của dòng là tài khoản công nợ (1311, 1312, 3311); dòng chưa bị đánh dấu Không "
       "báo tiền về; và phiếu thuộc công ty của bạn.")
b.image("24-tong-hop-tien.png", "Màn Tổng hợp tiền về ngân hàng")

b.h2("6.2. Ý nghĩa các cột")
b.table([
    ["Cột", "Nội dung hiển thị"],
    ["Số báo có", "Mã phiếu báo có chứa dòng này. Bấm vào để mở màn chi tiết phiếu."],
    ["Ngày hạch toán", "Ngày ghi nhận tiền về của phiếu."],
    ["Người lập", "Người lập phiếu báo có."],
    ["Khách hàng", "Khách hàng gắn với dòng, dạng Mã - Tên. Khoản chưa rõ sẽ là KHÁCH KHÔNG RÕ."],
    ["Ghi chú", "Diễn giải của dòng chi tiết."],
    ["Ngân hàng", "Mã ngân hàng nhận tiền."],
    ["STK ngân hàng", "Số tài khoản công ty nhận tiền."],
    ["Số tiền", "Số tiền của dòng, quy ra đồng Việt Nam. Cột này sắp xếp được."],
    ["Số tiền chưa điều chỉnh", "Phần tiền chưa được xử lý bằng phiếu điều chỉnh công nợ."],
    ["Trạng thái", "Chưa điều chỉnh hết công nợ (nhãn vàng) hoặc Đã điều chỉnh hết công nợ "
                   "(nhãn xanh)."],
    ["Điều chỉnh công nợ", "Ô tích để chọn dòng. Dòng đã điều chỉnh hết hiển thị dấu gạch ngang."],
])
b.image("25-tong-hop-cot-phai.png",
        "Phần bên phải: Số tiền chưa điều chỉnh, Trạng thái và ô tích Điều chỉnh công nợ")

b.h2("6.3. Tìm kiếm và lọc")
b.para("Ô tìm nhanh ở trên tìm theo số báo có. Bấm “Tìm kiếm nâng cao” để mở đầy đủ các ô lọc.")
b.image("26-tong-hop-bo-loc.png", "Bảng tìm kiếm nâng cao của màn Tổng hợp tiền về ngân hàng")
b.table([
    ["Ô lọc", "Cách dùng"],
    ["Khách hàng", "Gõ tối thiểu 2 ký tự rồi chọn khách trong danh sách gợi ý."],
    ["Ghi chú", "Gõ một phần diễn giải của dòng chi tiết."],
    ["Ngân hàng", "Gõ mã hoặc tên ngân hàng."],
    ["STK ngân hàng", "Gõ một phần số tài khoản."],
    ["Người lập", "Chọn nhân viên đã lập phiếu."],
    ["Lọc phiếu", "Chọn “Chưa điều chỉnh hết công nợ” để lọc các khoản còn phải xử lý."],
    ["Số tiền từ / đến", "Lọc theo khoảng số tiền của dòng."],
    ["Hạch toán từ / đến", "Lọc theo khoảng ngày hạch toán của phiếu."],
])

b.h2("6.4. Chuyển sang tạo phiếu yêu cầu điều chỉnh công nợ")
b.para("Bước 1: Lọc ra các khoản cần xử lý, ví dụ chọn Lọc phiếu = “Chưa điều chỉnh hết công "
       "nợ”.")
b.para("Bước 2: Tích ô ở cột Điều chỉnh công nợ của những dòng cần gán lại đối tượng. Chỉ dòng "
       "còn tiền chưa điều chỉnh mới có ô tích.")
b.para("Bước 3: Bấm nút “Tạo mới điều chỉnh công nợ”. Hệ thống chuyển sang màn tạo phiếu yêu cầu "
       "điều chỉnh công nợ, mang theo các dòng bạn vừa chọn.")
b.para("Lưu ý quan trọng: một phiếu yêu cầu điều chỉnh công nợ chỉ gắn được với MỘT phiếu báo có. "
       "Nếu bạn tích dòng của hai phiếu báo có khác nhau, hệ thống báo “Không thể chọn 2 phiếu "
       "báo có khác nhau! Vui lòng bỏ chọn dòng cũ trước.” và bỏ tích vừa bấm. Chưa tích dòng "
       "nào mà bấm nút thì hệ thống báo “Vui lòng chọn ít nhất một chi tiết báo có.”")
b.para("Cách khác: mở màn chi tiết một phiếu báo có rồi bấm nút “Tạo phiếu yêu cầu điều chỉnh "
       "công nợ”. Hệ thống mang theo toàn bộ dòng còn tiền chưa điều chỉnh của phiếu đó, và nút "
       "Quay lại ở màn điều chỉnh công nợ sẽ trả bạn về đúng phiếu báo có này.")

b.h2("6.5. Xuất Excel")
b.para("Bước 1: Lọc dữ liệu theo ý muốn (file xuất lấy TOÀN BỘ dòng khớp bộ lọc, không chỉ trang "
       "đang xem).")
b.para("Bước 2: Bấm nút Xuất Excel. Cửa sổ “Chọn trường xuất file” mở ra với 10 trường, mặc định "
       "chọn hết.")
b.image("27-chon-truong-xuat.png", "Cửa sổ Chọn trường xuất file")
b.para("Bước 3: Bấm dấu × trên tên trường để bỏ trường không cần. Thứ tự cột trong file chạy "
       "đúng theo thứ tự bạn chọn — muốn đổi vị trí thì bỏ chọn hết rồi chọn lại theo trình tự "
       "mong muốn. Có sẵn nút “Chọn tất cả” và “Bỏ chọn hết”.")
b.para("Bước 4: Bấm “Xuất file”. Hệ thống tải về file Tong-hop-tien-ve-ngan-hang.xlsx, đầu file "
       "có logo và tiêu đề của công ty; nếu bạn có lọc theo khoảng ngày hạch toán thì file có "
       "thêm dòng “Từ ngày … đến ngày …”.")

# ============================================ PHAN 7
b.h1("PHẦN 7: HƯỚNG DẪN THEO TỪNG QUYỀN")

b.h2("7.1. Người dùng có quyền “Quản lý phiếu báo có”")
b.para("Bạn nhìn thấy: nút Tạo mới và nút Import Excel ở màn danh sách; nút Sửa, Xóa và mục Duyệt "
       "ở cột Hành động (theo trạng thái từng phiếu); nút Sửa, Duyệt, Xóa ở màn chi tiết; ô tích "
       "Không báo tiền về ở màn chi tiết mở khóa.")
b.para("Bạn làm được: lập phiếu mới (Phần 3); sửa và xóa phiếu Đang tạo do chính bạn lập "
       "(mục 4.1 và 4.4); duyệt bất kỳ phiếu Đang tạo nào bạn xem được, kể cả phiếu người khác "
       "lập (mục 4.3); import file sao kê (Phần 5); đánh dấu không báo tiền về (mục 4.5).")
b.para("Bạn KHÔNG làm được: sửa hay xóa phiếu đã duyệt; sửa hay xóa phiếu Đang tạo do người khác "
       "lập (bạn cũng không nhìn thấy phiếu đó trong danh sách).")
b.para("Lưu ý: quyền này KHÔNG mở rộng phạm vi dữ liệu. Nếu bạn chỉ có quyền này mà không có "
       "quyền xem theo cấp nào, bạn vẫn chỉ thấy phiếu do chính mình lập.")

b.h2("7.2. Người dùng có quyền “Xem tất cả phiếu báo có của tổng công ty”")
b.para("Bạn nhìn thấy: toàn bộ phiếu đã duyệt của mọi công ty trong hệ thống, cộng với phiếu "
       "Đang tạo do chính bạn lập. Bộ lọc nâng cao có thêm ô Công ty – Phòng ban – Bộ phận để "
       "khoanh vùng đơn vị cần xem.")
b.para("Bạn làm được: xem danh sách, tìm kiếm và lọc, mở màn chi tiết, xem lịch sử thay đổi, "
       "xem màn Tổng hợp tiền về ngân hàng và xuất Excel màn đó.")
b.para("Bạn KHÔNG làm được (nếu không kèm quyền Quản lý phiếu báo có): tạo mới, sửa, xóa, duyệt "
       "phiếu, import Excel, tích ô Không báo tiền về. Các nút này không hiển thị; nếu truy cập "
       "trực tiếp bằng đường dẫn, hệ thống báo lỗi không có quyền.")

b.h2("7.3. Người dùng có quyền “Xem tất cả phiếu báo có của công ty”")
b.para("Bạn nhìn thấy: phiếu đã duyệt của công ty bạn, cộng với phiếu Đang tạo do chính bạn lập. "
       "Phiếu của công ty khác không hiển thị, kể cả khi bạn biết mã phiếu.")
b.para("Bạn làm được và không làm được: giống mục 7.2, chỉ khác ở phạm vi dữ liệu.")

b.h2("7.4. Người dùng không có quyền nào của màn Phiếu báo có")
b.para("Bạn vẫn mở được màn danh sách nhưng chỉ thấy những phiếu do chính bạn lập (cả Đang tạo "
       "lẫn Đã duyệt). Bạn xem được chi tiết và lịch sử của các phiếu đó, xem được màn Tổng hợp "
       "tiền về ngân hàng của công ty mình.")
b.para("Bạn không có nút Tạo mới, Import Excel, Sửa, Xóa, Duyệt. Muốn được cấp quyền, liên hệ "
       "quản trị hệ thống để bổ sung quyền Quản lý phiếu báo có hoặc quyền xem theo cấp phù hợp.")

# ============================================ PHAN 8
b.h1("PHẦN 8: CÂU HỎI THƯỜNG GẶP")
b.table([
    ["Tình huống", "Giải thích và cách xử lý"],
    ["Tôi không thấy nút Tạo mới.",
     "Tài khoản của bạn chưa có quyền Quản lý phiếu báo có. Liên hệ quản trị hệ thống."],
    ["Phiếu tôi vừa lập không thấy trong danh sách của đồng nghiệp.",
     "Đúng thiết kế: phiếu Đang tạo chỉ người lập nhìn thấy. Sau khi duyệt, những người có quyền "
     "xem theo cấp phù hợp sẽ thấy phiếu."],
    ["Tôi muốn sửa một phiếu đã duyệt.",
     "Phiếu đã duyệt không sửa và không xóa được vì bút toán đã ghi vào sổ kế toán. Trường hợp "
     "sai số liệu, lập phiếu yêu cầu điều chỉnh công nợ hoặc liên hệ kế toán trưởng."],
    ["Ô Tỷ giá bị khóa, không nhập được.",
     "Loại tiền đang là VNĐ nên tỷ giá luôn bằng 1. Chọn loại tiền khác thì ô mở khóa."],
    ["Bấm ô hợp đồng nhưng hệ thống báo “Chưa chọn khách hàng”.",
     "Phải chọn khách hàng cho dòng đó trước, vì cửa sổ hợp đồng chỉ liệt kê hợp đồng của khách "
     "hàng đã chọn."],
    ["Cột Số tiền báo “Số tiền phải lớn hơn 0” dù tôi thấy đã nhập.",
     "Kiểm tra lại đúng dòng đang báo lỗi — bảng chi tiết rộng, hãy kéo thanh cuộn ngang để xem "
     "hết các dòng."],
    ["Khoản tiền về chưa biết của khách nào thì làm sao?",
     "Cứ để khách hàng KHÁCH KHÔNG RÕ và lưu phiếu. Sau đó vào màn Tổng hợp tiền về ngân hàng, "
     "tích dòng đó và tạo phiếu yêu cầu điều chỉnh công nợ để gán lại đúng khách."],
    ["Dòng tiền không thấy ở màn Tổng hợp tiền về ngân hàng.",
     "Kiểm tra bốn điều kiện: phiếu đã duyệt chưa; tài khoản có của dòng có thuộc nhóm 1311, "
     "1312, 3311 không; dòng có bị tích Không báo tiền về không; phiếu có thuộc công ty của bạn "
     "không."],
    ["Import xong thấy phiếu đều gắn KHÁCH KHÔNG RÕ.",
     "Đúng thiết kế: import chỉ ghi nhận tiền về, việc gán đúng khách hàng làm ở bước điều chỉnh "
     "công nợ."],
    ["File Excel xuất ra thiếu cột tôi cần.",
     "Ở cửa sổ Chọn trường xuất file, bấm “Chọn tất cả” rồi bỏ bớt trường không cần; thứ tự cột "
     "trong file chạy theo thứ tự bạn chọn."],
])

b.finish()
