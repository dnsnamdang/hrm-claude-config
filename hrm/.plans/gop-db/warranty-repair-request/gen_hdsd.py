# -*- coding: utf-8 -*-
"""Sinh tai lieu HDSD man "Yeu cau kiem tra sua chua - bao hanh".

Anh chup that: .plans/gop-db/warranty-repair-request/wrr_shots/ (Playwright, 1440x900, 03/09/2026)
Chay:  python3 .plans/gop-db/warranty-repair-request/gen_hdsd.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))                      # .plans/gop-db (lop mac)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "hdsd-documenter", "assets"))
from _mac_docx import patch_hdsd, renumber_figure_index  # noqa: E402

patch_hdsd()
from hdsd_engine import HdsdBuilder  # noqa: E402

b = HdsdBuilder(
    output=os.path.join(HERE, "HDSD_Yeu cau kiem tra sua chua - bao hanh.docx"),
    shots_dir=os.path.join(HERE, "wrr_shots"),
    cover_title="(Màn hình: Yêu cầu kiểm tra sửa chữa – bảo hành)",
    doc_title="HDSD - Yêu cầu kiểm tra sửa chữa – bảo hành")

# Engine tu kiem bang cach doi chieu tieu de chuong cua FILE KHUNG voi noi dung moi.
# Tai lieu nay CO Y dung lai dung ten chuong "TONG QUAN PHAN MEM" (skill hdsd-documenter
# bat buoc chuong nay), nen phai bo no khoi danh sach doi chieu — neu khong assert se bao
# nham la muc luc chua duoc cap nhat. Cac tieu de con lai cua file khung van duoc kiem.
b.template_headings = [h for h in b.template_headings if h != "TỔNG QUAN PHẦN MỀM"]

# ======================================================= TONG QUAN PHAN MEM
b.h1("TỔNG QUAN PHẦN MỀM")

b.h2("1. Bảng các thuật ngữ")
b.table([
    ["Thuật ngữ", "Giải thích"],
    ["Phiếu yêu cầu", "Một bản ghi trên màn hình này. Là chứng từ mở đầu của luồng dịch vụ: "
                      "ghi nhận việc khách hàng báo thiết bị cần kiểm tra, sửa chữa hoặc bảo hành."],
    ["Phòng tiếp nhận xử lý", "Phòng ban bạn gửi phiếu tới. Chỉ người của phòng này (và có quyền "
                              "xử lý) mới tạo phiếu xử lý, chuyển phòng hoặc từ chối phiếu."],
    ["Phiếu xử lý yêu cầu", "Chứng từ tiếp theo, do phòng tiếp nhận lập từ phiếu yêu cầu của bạn."],
    ["Lưu nháp", "Lưu lại phiếu để hoàn thiện sau. Phiếu ở trạng thái Đang tạo và chỉ mình bạn "
                 "nhìn thấy."],
    ["Lưu và gửi", "Gửi phiếu cho phòng tiếp nhận. Phiếu chuyển sang Chờ xử lý và không sửa được nữa."],
    ["Số BBBGNT / BBXNCV", "Số biên bản bàn giao nghiệm thu hoặc biên bản xác nhận công việc đã ký "
                           "với khách hàng."],
    ["Trang thiết bị hiện có của khách hàng", "Danh mục thiết bị khách đang sở hữu — gồm thiết bị "
                                              "mua của Tân Phát và thiết bị mua của nơi khác."],
])

b.h2("2. Bảng cập nhật nội dung tài liệu")
b.table([
    ["Ngày", "Nội dung cập nhật", "Người thực hiện"],
    ["03/09/2026", "Biên soạn lần đầu theo phiên bản màn hình trên hệ thống HRM.", "Nhóm phát triển"],
])

b.h2("3. Giới thiệu chung")
b.para("Màn hình Yêu cầu kiểm tra sửa chữa – bảo hành dùng để ghi nhận yêu cầu của khách hàng khi "
       "thiết bị cần kiểm tra, sửa chữa hoặc bảo hành, rồi chuyển yêu cầu đó cho phòng chuyên môn "
       "xử lý. Đây là bước đầu tiên của cả luồng dịch vụ.")
b.para("Luồng nghiệp vụ đi qua các bước sau:")
b.bullet("Bạn (nhân viên kinh doanh hoặc chăm sóc khách hàng) lập phiếu yêu cầu, ghi rõ khách "
         "hàng, người liên hệ, địa chỉ sửa chữa và danh sách thiết bị cần xử lý.")
b.bullet("Bạn gửi phiếu cho phòng tiếp nhận. Toàn bộ nhân viên phòng đó nhận được thông báo.")
b.bullet("Phòng tiếp nhận có ba lựa chọn: lập Phiếu xử lý yêu cầu để đi tiếp, chuyển phiếu sang "
         "phòng khác phù hợp hơn, hoặc từ chối và trả phiếu về cho bạn kèm lý do.")
b.bullet("Nếu phiếu đi tiếp, các chứng từ phía sau (phiếu cung cấp thông tin, báo giá, hợp đồng) "
         "sẽ tự cập nhật ngược trạng thái lên phiếu yêu cầu của bạn — bạn theo dõi được tiến độ "
         "ngay ở cột Trạng thái.")
b.para("Đường dẫn màn hình: /customer-care/warranty-repair-requests")

b.h2("4. Quyền và phạm vi dữ liệu")
b.para("Màn hình này KHÔNG yêu cầu quyền riêng để xem và lập phiếu: ai đăng nhập được cũng tự lập "
       "phiếu của mình. Quyền chỉ quyết định hai việc: bạn nhìn thấy phiếu của những ai, và bạn có "
       "làm được ba thao tác của phòng tiếp nhận hay không.")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / tab tương ứng", "Ghi chú"],
    ["Xử lý yêu cầu sửa chữa",
     "Xử lý phiếu gửi về phòng mình: lập phiếu xử lý, chuyển phòng tiếp nhận, từ chối.",
     "Tạo phiếu xử lý yêu cầu · Chuyển phòng tiếp nhận · Từ chối",
     "Chỉ áp dụng cho phiếu đang ở Chờ xử lý, gửi đúng phòng của bạn và chưa có phiếu xử lý."],
    ["Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng công ty",
     "Nhìn thấy phiếu của mọi công ty.", "Khối lọc Công ty – Phòng ban",
     "Cấp rộng nhất."],
    ["Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo công ty",
     "Nhìn thấy phiếu thuộc công ty của mình.", "Khối lọc Công ty – Phòng ban", "—"],
    ["Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo phòng ban",
     "Nhìn thấy phiếu thuộc các phòng mình được phân quản lý.", "Khối lọc Công ty – Phòng ban",
     "Kèm theo luôn cả phiếu do chính mình lập."],
    ["(Không có quyền nào)", "Chỉ nhìn thấy phiếu do chính mình lập.", "—",
     "Vẫn lập, sửa, xóa, in, xuất Excel được với phiếu của mình."],
])

b.h3("4.1. Người dùng không có quyền nào")
b.para("Bạn vẫn vào được màn hình và làm đủ việc với phiếu của mình: lập phiếu, sửa, xóa khi chưa "
       "gửi, in, xuất Excel, xem lịch sử. Danh sách chỉ hiện phiếu do bạn lập. Ba nút Tạo phiếu xử "
       "lý yêu cầu, Chuyển phòng tiếp nhận và Từ chối không hiển thị. Khối lọc Công ty – Phòng ban "
       "cũng không hiện.")

b.h3("4.2. Người dùng có quyền “Xử lý yêu cầu sửa chữa”")
b.para("Ngoài phiếu của mình, bạn nhìn thấy thêm mọi phiếu được gửi về phòng bạn. Với những phiếu "
       "đang ở trạng thái Chờ xử lý của phòng bạn và chưa có phiếu xử lý, bạn thấy thêm ba thao "
       "tác: Tạo phiếu xử lý yêu cầu, Chuyển phòng tiếp nhận, Từ chối. Hướng dẫn từng thao tác ở "
       "PHẦN 6.")
b.para("Nếu không có quyền này, ba nút trên sẽ không hiển thị; trường hợp truy cập trực tiếp bằng "
       "đường dẫn, hệ thống báo lỗi không có quyền.")

b.h3("4.3. Người dùng có quyền xem theo cấp (tổng công ty / công ty / phòng ban)")
b.para("Bạn nhìn thấy phiếu của nhiều người khác theo đúng cấp được cấp quyền, và khối lọc Công ty "
       "– Phòng ban xuất hiện trong Tìm kiếm nâng cao để bạn lọc theo đơn vị. Có nhiều cấp cùng lúc "
       "thì hệ thống áp cấp rộng nhất.")
b.para("Một điểm quan trọng áp cho MỌI cấp quyền: phiếu ở trạng thái Đang tạo (phiếu nháp) của "
       "người khác không bao giờ hiển thị với bạn, kể cả khi bạn là quản trị hệ thống. Phiếu nháp "
       "chỉ người lập nhìn thấy.")

# ============================================ PHAN 1: TRUY CAP & BO CUC
b.h1("PHẦN 1: TRUY CẬP MÀN HÌNH VÀ BỐ CỤC")

b.h2("1. Vào màn này bằng cách nào")
b.para("Màn hình vào được từ hai chỗ, và HAI LỐI VÀO CHO HAI DANH SÁCH KHÁC NHAU:")
b.table([
    ["Vào từ", "Bấm theo đường", "Danh sách hiện ra"],
    ["CSKH", "Chọn phân hệ CSKH → nhóm “Kiểm tra bảo hành sửa chữa” → bấm “Yêu cầu kiểm tra sửa "
              "chữa - bảo hành”", "Toàn bộ phiếu trong phạm vi quyền của bạn"],
    ["Bán hàng", "Chọn phân hệ Bán hàng → nhóm “Bán dịch vụ” → “Báo giá dịch vụ SC-BD-BT” → bấm "
                 "“Yêu cầu sửa chữa - bảo hành”", "Chỉ phiếu do chính bạn lập"],
])
b.para("Nếu mở màn mà danh sách trống hoặc ít hơn mong đợi, hãy kiểm tra bạn đang vào từ menu nào "
       "— hai lối vào hiển thị phạm vi khác nhau.")

b.h2("2. Bố cục màn hình")
b.image("01-danh-sach.png", "Màn Yêu cầu kiểm tra sửa chữa – bảo hành")
b.para("Màn hình chia làm hai khối:")
b.bullet("Khối trên là Bộ lọc danh sách: ô tìm nhanh, nút Tìm kiếm, nút Làm mới, nút Cài đặt bộ "
         "lọc và nút Tìm kiếm nâng cao.")
b.bullet("Khối dưới là bảng danh sách: thanh công cụ (Tạo mới, Xuất Excel, In danh sách, biểu "
         "tượng Cấu hình cột hiển thị), bảng dữ liệu và phân trang.")

b.h2("3. Các cột của bảng danh sách")
b.table([
    ["Cột", "Nội dung", "Mặc định"],
    ["STT", "Số thứ tự dòng, chạy liên tục qua các trang.", "Hiện"],
    ["Số phiếu", "Số phiếu do hệ thống sinh. Bấm vào để mở màn chi tiết.", "Hiện"],
    ["Khách hàng", "Mã và tên khách hàng.", "Hiện"],
    ["Tên thiết bị liên quan", "Danh sách thiết bị trong phiếu; nhiều hơn 2 dòng thì có liên kết "
                               "“Xem thêm”.", "Hiện"],
    ["Địa chỉ sửa chữa", "Nơi thực hiện việc kiểm tra, sửa chữa.", "Ẩn"],
    ["Ngày gửi yêu cầu", "Thời điểm bạn bấm Lưu và gửi.", "Ẩn"],
    ["Người xử lý / Ngày xử lý", "Người và thời điểm phòng tiếp nhận xử lý phiếu.", "Ẩn"],
    ["Người tạo / Ngày tạo", "Người lập phiếu và thời điểm lập.", "Hiện"],
    ["Người cập nhật / Ngày cập nhật", "Người sửa gần nhất; trống nếu phiếu chưa ai sửa.", "Ẩn"],
    ["Trạng thái", "Tình trạng hiện tại của phiếu, xem bảng ở mục 4.", "Hiện"],
    ["Hành động", "Các nút thao tác của từng dòng.", "Hiện"],
])
b.para("Muốn bật thêm cột đang ẩn, xem PHẦN 2 mục 4.")

b.h2("4. Ý nghĩa các trạng thái")
b.table([
    ["Trạng thái", "Nghĩa là gì", "Do đâu mà có"],
    ["Đang tạo", "Phiếu nháp, chưa gửi đi. Chỉ mình bạn nhìn thấy.",
     "Bạn bấm Lưu nháp, hoặc phiếu bị phòng tiếp nhận từ chối trả về."],
    ["Chờ xử lý", "Đã gửi cho phòng tiếp nhận, đang chờ họ xử lý.", "Bạn bấm Lưu và gửi."],
    ["Đang xử lý", "Phòng tiếp nhận đang xem xét.", "Trạng thái kế thừa dữ liệu cũ."],
    ["Đang CCTT", "Đang lập phiếu cung cấp thông tin làm báo giá.", "Chứng từ phía sau cập nhật."],
    ["Đã CCTT báo giá", "Đã có đủ thông tin để làm báo giá.", "Chứng từ phía sau cập nhật."],
    ["Đã báo giá", "Đã lập báo giá dịch vụ gửi khách.", "Chứng từ phía sau cập nhật."],
    ["Đã lập hợp đồng", "Đã ký hợp đồng dịch vụ với khách.", "Chứng từ phía sau cập nhật."],
    ["Đã xử lý", "Phòng tiếp nhận đã lập phiếu xử lý và gửi đi.", "Chứng từ phía sau cập nhật."],
    ["Đã tư vấn điện thoại", "Xử lý xong bằng tư vấn qua điện thoại, không cần báo giá.",
     "Phòng tiếp nhận chọn hướng xử lý là tư vấn điện thoại."],
])

# ============================================= PHAN 2: TIM KIEM VA LOC
b.h1("PHẦN 2: TÌM KIẾM, LỌC VÀ TÙY CHỈNH HIỂN THỊ")

b.h2("1. Tìm nhanh")
b.para("Gõ từ khóa vào ô ở đầu màn hình rồi nhấn Enter hoặc bấm nút Tìm kiếm. Ô này tìm theo ba "
       "thứ: mã phiếu, tên khách hàng và tên người tạo phiếu. Gõ một phần cũng tìm ra, không cần "
       "gõ đủ.")
b.para("Bấm dấu × ở cuối ô để xóa nhanh từ khóa, hoặc bấm Làm mới để xóa toàn bộ điều kiện lọc.")

b.h2("2. Tìm kiếm nâng cao")
b.para("Bấm nút Tìm kiếm nâng cao ở góc phải khối lọc; khối tiêu chí mở ra ngay bên dưới. Bấm lần "
       "nữa (chữ đổi thành Ẩn tìm kiếm nâng cao) để thu lại.")
b.image("02-bo-loc-nang-cao.png", "Khối Tìm kiếm nâng cao")
b.table([
    ["Ô lọc", "Cách dùng"],
    ["Trạng thái", "Chọn một trạng thái trong danh sách 9 giá trị ở PHẦN 1 mục 4."],
    ["Khách hàng", "Bấm vào ô rồi gõ tên hoặc mã khách; danh sách gợi ý hiện dần."],
    ["Tên thiết bị", "Gõ tên thiết bị rồi nhấn Enter. Gõ một phần tên cũng tìm ra."],
    ["Người yêu cầu", "Chọn người đã lập phiếu."],
    ["Tỉnh/TP", "Chọn tỉnh/thành phố của khách hàng."],
    ["Ngày yêu cầu từ / đến", "Chọn khoảng ngày lập phiếu. Chọn cùng một ngày ở cả hai ô để xem "
                             "đúng ngày đó."],
    ["Công ty – Phòng ban", "Chỉ hiện nếu bạn có quyền xem theo cấp. Lọc theo đơn vị của người lập "
                            "phiếu. Ô nào có biểu tượng ổ khóa là ô bạn không được đổi."],
])
b.para("Chọn xong bấm Tìm kiếm. Các ô dạng danh sách tự tìm lại ngay khi bạn chọn; riêng ô gõ tay "
       "thì phải nhấn Enter hoặc bấm Tìm kiếm.")
b.para("Lưu ý: nút Làm mới xóa hết điều kiện lọc nhưng KHÔNG đổi lối vào — vào từ Bán hàng thì làm "
       "mới xong vẫn chỉ thấy phiếu của bạn.")

b.h2("3. Cài đặt bộ lọc — chọn ô lọc nào hiện ra")
b.para("Bấm nút Cài đặt bộ lọc. Cửa sổ liệt kê 8 ô lọc, mỗi ô có ô tích chọn và số thứ tự.")
b.image("03-cai-dat-bo-loc.png", "Cửa sổ Cài đặt bộ lọc")
b.bullet("Bỏ tích ô nào thì ô lọc đó không hiện ở khối Tìm kiếm nâng cao nữa.")
b.bullet("Kéo biểu tượng chấm ở đầu mỗi dòng để đổi thứ tự các ô lọc.")
b.bullet("Bấm Lưu để áp dụng; bấm Khôi phục mặc định để trở lại như ban đầu; bấm Đóng để thoát mà "
         "không lưu.")
b.para("Cài đặt được ghi nhớ riêng cho từng người và từng màn hình.")

b.h2("4. Tùy chỉnh cột — chọn cột nào hiện trên bảng")
b.para("Bấm biểu tượng hình cột ở cuối thanh công cụ (chỉ dẫn hiện chữ “Cấu hình cột hiển thị”).")
b.image("05-cau-hinh-cot.png", "Cửa sổ Tùy chỉnh cột")
b.bullet("Tích chọn cột muốn hiện, bỏ tích cột muốn ẩn.")
b.bullet("Cột STT và Số phiếu có biểu tượng ổ khóa — luôn hiển thị, không tắt được.")
b.bullet("Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.")
b.bullet("Bấm Lưu. Lần sau vào lại màn hình, bảng vẫn giữ đúng các cột bạn đã chọn.")

# ============================================= PHAN 3: LAP PHIEU
b.h1("PHẦN 3: LẬP PHIẾU YÊU CẦU")

b.h2("1. Mở màn lập phiếu")
b.para("Ở màn danh sách, bấm nút Tạo mới (màu xanh, có dấu cộng) trên thanh công cụ. Hệ thống mở "
       "màn “Tạo yêu cầu kiểm tra sửa chữa – bảo hành” với các ô còn trống.")
b.image("06-tao-moi.png", "Màn Lập phiếu yêu cầu lúc mới mở")
b.para("Màn hình chia làm ba khối, làm lần lượt từ trên xuống:")
b.bullet("Thông tin khách hàng — chọn khách và nơi sửa chữa.")
b.bullet("Danh sách thiết bị cần kiểm tra sửa chữa – bảo hành — các thiết bị bạn đưa vào phiếu.")
b.bullet("Danh mục trang thiết bị hiện có của khách hàng — kho thiết bị của khách để bạn chọn ra.")

b.h2("2. Bước 1 — Chọn khách hàng")
b.para("Bấm vào ô Khách hàng (chữ mờ ghi “Nhấn vào đây để chọn khách hàng”). Cửa sổ Chọn khách "
       "hàng mở ra.")
b.image("07-chon-khach-hang.png", "Cửa sổ Chọn khách hàng")
b.bullet("Tìm khách bằng một trong ba ô: Tên / Mã khách hàng, Mã số thuế, Số điện thoại. Nhập rồi "
         "bấm Tìm kiếm.")
b.bullet("Bấm vào mã khách hàng ở cột thứ hai để chọn. Cửa sổ tự đóng.")
b.bullet("Nếu danh sách quá dài, dùng ô Số dòng/trang và các nút phân trang ở cuối cửa sổ.")
b.para("Sau khi chọn khách, hệ thống tự làm ba việc: điền Loại hình tổ chức, nạp danh sách Người "
       "liên hệ và Địa chỉ sửa chữa của khách, và nạp danh mục thiết bị của khách vào bảng dưới "
       "cùng.")
b.para("Đổi sang khách khác thì các thiết bị đã chọn của khách cũ sẽ bị bỏ — hãy chọn đúng khách "
       "ngay từ đầu.")

b.h2("3. Bước 2 — Điền thông tin khách hàng")
b.table([
    ["Trường", "Cách nhập", "Bắt buộc", "Giá trị điền sẵn"],
    ["Khách hàng", "Bấm ô để mở cửa sổ chọn khách.", "Có (cả khi Lưu nháp)", "Trống"],
    ["Người liên hệ", "Chọn trong danh sách người liên hệ của khách.",
     "Có khi Lưu và gửi", "Trống. Khách là cá nhân thì tự điền tên khách."],
    ["Số điện thoại liên hệ", "Không nhập được — hệ thống tự điền theo người liên hệ.", "Không",
     "Tự động theo người liên hệ"],
    ["Địa chỉ sửa chữa", "Chọn trong danh sách địa chỉ của khách.", "Có khi Lưu và gửi", "Trống"],
    ["Loại hình tổ chức", "Không nhập được — hệ thống tự điền theo khách hàng.", "Không",
     "Tự động theo khách hàng"],
    ["Ghi chú", "Gõ nội dung cần lưu ý cho phòng tiếp nhận.", "Có khi Lưu và gửi", "Trống"],
    ["Phòng tiếp nhận xử lý", "Chọn phòng sẽ nhận và xử lý phiếu.", "Có khi Lưu và gửi", "Trống"],
])
b.para("Ba ô Người liên hệ, Địa chỉ sửa chữa và Loại hình tổ chức bị khóa cho tới khi bạn chọn "
       "khách hàng.")
b.para("Chọn đúng Phòng tiếp nhận xử lý là việc quan trọng nhất ở khối này: toàn bộ nhân viên phòng "
       "đó sẽ nhận thông báo, và chỉ họ mới xử lý được phiếu.")

b.h2("4. Bước 3 — Đưa thiết bị vào phiếu")
b.para("Cuộn xuống bảng “Danh mục trang thiết bị hiện có của khách hàng”. Bảng liệt kê thiết bị "
       "khách đang có: thiết bị mua của Tân Phát và thiết bị mua của nơi khác.")
b.bullet("Gõ mã, model hoặc tên thiết bị vào ô tìm rồi bấm Tìm kiếm để lọc nhanh.")
b.bullet("Bấm nút dấu cộng ở cột Hành động của dòng thiết bị — thiết bị được đưa lên bảng “Danh "
         "sách thiết bị cần kiểm tra sửa chữa – bảo hành”.")
b.bullet("Thiết bị khách có nhưng chưa khai trong danh mục: bấm nút “Thêm trang thiết bị của khách "
         "hàng”, chọn loại (thiết bị Tân Phát cung cấp hay mua của nơi khác) rồi khai thông tin.")
b.bullet("Cần tăng số lượng của một thiết bị: bấm liên kết “Thêm số lượng” ở cột Số lượng, nhập số "
         "cần thêm. Ô này chỉ nhận số dương.")

b.h2("5. Bước 4 — Điền chi tiết cho từng thiết bị")
b.para("Ở bảng “Danh sách thiết bị cần kiểm tra sửa chữa – bảo hành”, mỗi thiết bị là một dòng. "
       "Cuộn ngang bảng để thấy hết các cột.")
b.table([
    ["Cột", "Cách nhập", "Bắt buộc"],
    ["Tên thiết bị", "Không gõ được — lấy từ thiết bị bạn vừa chọn.", "Có (cả khi Lưu nháp)"],
    ["Thương hiệu / Model", "Không gõ được — theo danh mục thiết bị.", "Không"],
    ["Serial", "Chọn serial trong danh sách. Thiết bị chưa khai đủ serial thì bấm “Nhập serial "
               "tạm” để gõ tay.", "Có khi Lưu và gửi"],
    ["Số BBBGNT / BBXNCV", "Gõ số biên bản đã ký với khách.", "Không"],
    ["Nội dung yêu cầu", "Mô tả tình trạng hỏng hoặc việc khách yêu cầu làm.", "Có khi Lưu và gửi"],
    ["File đính kèm", "Bấm Chọn tệp để tải ảnh hiện trạng hoặc biên bản. Nhận PDF, ảnh, Word, "
                      "Excel; tối đa 20MB mỗi tệp.", "Không"],
    ["Hành động", "Bấm biểu tượng thùng rác để bỏ thiết bị khỏi phiếu.", "—"],
])
b.para("Hai lỗi hay gặp ở cột Serial:")
b.bullet("Hai dòng cùng một serial — hệ thống báo “Bị trùng serial thiết bị”. Mỗi thiết bị thực tế "
         "là một dòng riêng với serial riêng.")
b.bullet("Gõ tay một serial vốn đã có trong danh mục — hệ thống báo “Serial đã có trong danh mục, "
         "vui lòng chọn từ danh sách”. Khi đó hãy bấm “Chọn serial” và chọn đúng serial đó.")

b.h2("6. Bước 5 — Lưu phiếu")
b.para("Cuối màn hình có ba nút: Lưu nháp, Lưu và gửi, Quay lại.")
b.h3("6.1. Lưu nháp")
b.para("Dùng khi bạn chưa có đủ thông tin và muốn hoàn thiện sau. Hệ thống chỉ bắt buộc bạn điền "
       "Khách hàng và tên thiết bị; các ô còn lại để trống cũng lưu được.")
b.para("Sau khi lưu, hệ thống báo “Lưu thành công” và quay về danh sách. Phiếu ở trạng thái Đang "
       "tạo và CHỈ MÌNH BẠN nhìn thấy — người khác, kể cả quản trị hệ thống, không thấy phiếu này.")
b.h3("6.2. Lưu và gửi")
b.para("Dùng khi phiếu đã đầy đủ và bạn muốn chuyển cho phòng tiếp nhận. Hệ thống hỏi xác nhận "
       "“Bạn đồng ý lưu và gửi?”; bấm Đồng ý để tiếp tục.")
b.para("Lúc này hệ thống bắt buộc đủ: Khách hàng, Người liên hệ, Địa chỉ sửa chữa, Ghi chú, Phòng "
       "tiếp nhận xử lý, và mỗi thiết bị phải có Serial và Nội dung yêu cầu. Thiếu ô nào thì ô đó "
       "viền đỏ và có dòng chữ đỏ “Bắt buộc phải nhập” ngay bên dưới; cửa sổ không đóng, dữ liệu "
       "bạn đã nhập vẫn còn nguyên.")
b.para("Gửi thành công, hệ thống báo “Gửi yêu cầu thành công”, phiếu chuyển sang Chờ xử lý và toàn "
       "bộ nhân viên phòng tiếp nhận nhận được thông báo trên chuông thông báo. Từ lúc này bạn "
       "KHÔNG sửa và KHÔNG xóa phiếu được nữa.")
b.h3("6.3. Quay lại")
b.para("Bấm Quay lại để về danh sách. Nếu bạn đã nhập gì đó mà chưa lưu, hệ thống hỏi xác nhận "
       "trước khi rời trang để bạn khỏi mất dữ liệu.")

# ============================================= PHAN 4: SUA PHIEU
b.h1("PHẦN 4: SỬA PHIẾU YÊU CẦU")

b.h2("1. Khi nào sửa được")
b.para("Bạn chỉ sửa được phiếu ở trạng thái Đang tạo và do chính bạn lập. Phiếu đã gửi đi (Chờ xử "
       "lý trở đi) thì nút Sửa không hiển thị. Phiếu bị từ chối quay về Đang tạo nên sửa lại được.")
b.para("Nếu bạn gõ thẳng đường dẫn màn sửa của một phiếu đã gửi, hệ thống tự chuyển bạn về màn chi "
       "tiết và không cho lưu.")

b.h2("2. Các bước sửa")
b.bullet("Cách 1: ở danh sách, bấm biểu tượng bút chì ở cột Hành động của dòng phiếu.")
b.bullet("Cách 2: mở màn chi tiết phiếu rồi bấm nút Sửa ở cuối trang.")
b.image("11-sua.png", "Màn Sửa phiếu yêu cầu")
b.para("Màn sửa giống hệt màn lập phiếu, chỉ khác là các ô đã có sẵn dữ liệu và tiêu đề trang có "
       "kèm số phiếu. Bạn đổi thông tin liên hệ, thêm hoặc bớt thiết bị, sửa nội dung yêu cầu rồi "
       "bấm Lưu nháp hoặc Lưu và gửi giống như khi lập mới.")
b.para("Mọi thay đổi đều được ghi vào Lịch sử: trường nào đổi, giá trị cũ là gì, giá trị mới là "
       "gì, ai đổi và lúc nào. Xem PHẦN 9.")

# ============================================= PHAN 5: XEM CHI TIET
b.h1("PHẦN 5: XEM CHI TIẾT PHIẾU")

b.h2("1. Mở màn chi tiết")
b.para("Ở danh sách, bấm vào số phiếu ở cột thứ hai. Màn chi tiết mở ra ở chế độ chỉ đọc.")
b.image("08-chi-tiet.png", "Màn Chi tiết phiếu yêu cầu")

b.h2("2. Nội dung màn chi tiết")
b.bullet("Khối Thông tin khách hàng: các ô chỉ đọc; góc phải ghi người yêu cầu và thời điểm lập "
         "phiếu.")
b.bullet("Dòng “Lý do từ chối gần nhất”: chỉ hiện nếu phiếu từng bị phòng tiếp nhận từ chối.")
b.bullet("Khối Danh sách thiết bị: đầy đủ thiết bị, serial, nội dung yêu cầu và tệp đính kèm.")
b.bullet("Khối Lịch sử: bấm “Xem lịch sử” để mở, xem PHẦN 9.")
b.bullet("Thanh nút cuối trang: chỉ hiện những thao tác bạn được phép làm với phiếu này.")
b.para("Các nút ở cuối màn chi tiết luôn khớp với các nút ở dòng tương ứng ngoài danh sách: ngoài "
       "danh sách không thấy nút nào thì trong chi tiết cũng không có nút đó.")

b.h2("3. Trường hợp không mở được")
b.para("Nếu phiếu không thuộc phạm vi bạn được xem, hoặc phiếu đã bị xóa, hệ thống chuyển sang "
       "trang báo không tìm thấy. Đây là cách hệ thống bảo vệ dữ liệu, không phải lỗi.")

# ================================= PHAN 6: THAO TAC CUA PHONG TIEP NHAN
b.h1("PHẦN 6: BA THAO TÁC CỦA PHÒNG TIẾP NHẬN")

b.para("Phần này dành cho người có quyền “Xử lý yêu cầu sửa chữa”. Ba thao tác dưới đây chỉ hiện "
       "khi phiếu thỏa mãn ĐỦ các điều kiện sau:")
b.bullet("Phiếu đang ở trạng thái Chờ xử lý.")
b.bullet("Phòng tiếp nhận xử lý của phiếu là phòng của bạn.")
b.bullet("Phiếu chưa có phiếu xử lý nào được lập.")
b.para("Thiếu một điều kiện là cả ba nút biến mất. Người quản trị hệ thống được bỏ qua điều kiện "
       "phòng ban.")
b.image("15-menu-hanh-dong.png", "Các thao tác của một phiếu đang ở trạng thái Chờ xử lý")
b.para("Hai thao tác đầu hiện thẳng ở cột Hành động; các thao tác còn lại nằm trong menu ba chấm "
       "(chỉ dẫn ghi “Hành động khác”).")

b.h2("1. Tạo phiếu xử lý yêu cầu")
b.para("Đây là hướng đi tiếp của luồng. Bấm biểu tượng thêm tài liệu ở cột Hành động, hoặc bấm nút "
       "“Tạo phiếu xử lý yêu cầu” ở cuối màn chi tiết.")
b.para("Hệ thống mở màn lập Phiếu xử lý yêu cầu, chép sẵn thông tin khách hàng và toàn bộ thiết bị "
       "của phiếu yêu cầu. Cách điền phiếu xử lý xem tài liệu hướng dẫn của màn đó.")
b.para("Mỗi phiếu yêu cầu chỉ lập được MỘT phiếu xử lý. Lập xong thì cả ba nút ở phần này biến "
       "mất khỏi phiếu yêu cầu.")

b.h2("2. Chuyển phòng tiếp nhận")
b.para("Dùng khi phiếu gửi nhầm phòng, hoặc phòng khác phù hợp hơn để xử lý. Bấm biểu tượng hai "
       "mũi tên ở cột Hành động, hoặc nút “Chuyển phòng tiếp nhận” ở màn chi tiết.")
b.image("17-chuyen-phong.png", "Cửa sổ Chuyển phòng tiếp nhận")
b.bullet("Cửa sổ hiện số phiếu và dòng “Phòng tiếp nhận hiện tại” để bạn đối chiếu.")
b.bullet("Chọn phòng ở ô “Phòng tiếp nhận mới”. Danh sách không liệt kê phòng hiện tại nên không "
         "chọn nhầm được.")
b.bullet("Bấm Xác nhận. Hệ thống báo “Chuyển phòng tiếp nhận thành công”.")
b.para("Sau khi chuyển: phiếu VẪN ở trạng thái Chờ xử lý (thao tác này không đổi trạng thái), phòng "
       "mới nhận được thông báo, và từ lúc này phòng cũ không còn thấy ba nút thao tác nữa.")
b.para("Không nhập phòng mới mà bấm Xác nhận thì hệ thống báo “Bắt buộc phải nhập”.")

b.h2("3. Từ chối yêu cầu")
b.para("Dùng khi thông tin trên phiếu chưa đủ hoặc yêu cầu không hợp lệ. Mở menu ba chấm ở cột "
       "Hành động rồi chọn Từ chối, hoặc bấm nút Từ chối ở màn chi tiết.")
b.image("16-tu-choi.png", "Cửa sổ Từ chối yêu cầu")
b.bullet("Nhập Lý do từ chối — bắt buộc. Viết rõ để người lập biết phải sửa gì.")
b.bullet("Bấm nút Từ chối (màu đỏ). Hệ thống báo “Từ chối yêu cầu thành công”.")
b.para("Sau khi từ chối: phiếu quay về trạng thái Đang tạo, người lập phiếu nhận được thông báo "
       "kèm lý do, và lý do cũng hiện ở màn chi tiết dưới dòng “Lý do từ chối gần nhất”. Người lập "
       "sửa lại rồi gửi lần nữa.")
b.para("Lưu ý: phiếu quay về Đang tạo nghĩa là bạn KHÔNG còn nhìn thấy phiếu đó nữa — phiếu nháp "
       "chỉ người lập nhìn thấy.")

# ============================================= PHAN 7: XOA PHIEU
b.h1("PHẦN 7: XÓA PHIẾU")

b.para("Bạn chỉ xóa được phiếu ở trạng thái Đang tạo và do chính bạn lập — cùng điều kiện với việc "
       "sửa. Phiếu đã gửi đi thì nút Xóa không hiển thị.")
b.bullet("Cách 1: ở danh sách, bấm biểu tượng thùng rác đỏ ở cột Hành động.")
b.bullet("Cách 2: mở màn chi tiết rồi bấm nút Xóa ở cuối trang.")
b.image("10-xac-nhan-xoa.png", "Hộp xác nhận xóa phiếu")
b.para("Hộp thoại “Xác nhận xóa” hiện lên kèm số phiếu để bạn đối chiếu. Bấm Xóa để thực hiện, "
       "bấm Hủy để bỏ qua.")
b.para("Xóa xong hệ thống báo “Xóa thành công”. Xóa phiếu là xóa cả các dòng thiết bị của phiếu và "
       "KHÔNG khôi phục được, nên hãy đọc kỹ số phiếu trong hộp thoại trước khi bấm.")

# ============================================= PHAN 8: IN VA XUAT EXCEL
b.h1("PHẦN 8: IN PHIẾU, IN DANH SÁCH VÀ XUẤT EXCEL")

b.h2("1. In một phiếu")
b.para("Bấm biểu tượng máy in ở cột Hành động của dòng phiếu, hoặc nút In ở cuối màn chi tiết. Cửa "
       "sổ “Xem trước phiếu yêu cầu” mở ra ngay trên màn hình.")
b.image("12-ban-in.png", "Xem trước bản in một phiếu")
b.para("Bản in gồm: tiêu đề công ty (logo, địa chỉ, điện thoại), tên phiếu và số phiếu, thông tin "
       "khách hàng và người yêu cầu, bảng thiết bị, và bốn ô ký tên (Người yêu cầu, Trưởng phòng "
       "yêu cầu, Phòng nhận yêu cầu, Ban giám đốc).")
b.para("Bấm nút In màu xanh ở góc trái trên để mở hộp thoại in của trình duyệt; bản gửi ra máy in "
       "không kèm nút và khung viền của cửa sổ xem trước. Bấm dấu × hoặc phím Esc để đóng.")

b.h2("2. In danh sách")
b.para("Bấm nút In danh sách trên thanh công cụ. Bản in lấy ĐÚNG các phiếu đang hiển thị theo bộ "
       "lọc hiện tại, nên hãy lọc trước rồi mới in.")
b.image("14-in-danh-sach-ok.png", "Xem trước bản in danh sách")
b.para("Bản in danh sách nằm ngang, có hai dòng “Thời gian” và “Phòng yêu cầu” cho biết bạn đang "
       "in theo điều kiện nào (không lọc thì ghi “Tất cả”). Mỗi phiếu là một dòng; phiếu có nhiều "
       "thiết bị thì các thiết bị xuống dòng trong cùng một ô.")
b.para("Danh sách quá dài thì hệ thống không in:")
b.image("13-in-danh-sach.png", "Lời nhắc khi danh sách vượt mức in tối đa")
b.para("Bản in danh sách chỉ dựng được tối đa 2.000 dòng. Vượt mức đó, cửa sổ chỉ hiện lời nhắc "
       "nền vàng đề nghị bạn thu hẹp bộ lọc (theo khoảng thời gian, trạng thái…) hoặc dùng Xuất "
       "Excel. Đây là cách hệ thống tránh làm treo trình duyệt, không phải lỗi.")

b.h2("3. Xuất Excel")
b.para("Bấm nút Xuất Excel trên thanh công cụ. Cửa sổ “Chọn trường xuất file” mở ra với 6 trường "
       "được chọn sẵn trong tổng số 13.")
b.image("04-xuat-excel.png", "Cửa sổ Chọn trường xuất file")
b.bullet("Bấm vào ô Trường xuất để mở danh sách và tích thêm trường cần xuất; bấm dấu × trên mỗi "
         "thẻ để bỏ trường.")
b.bullet("Thứ tự cột trong tệp chạy đúng theo thứ tự bạn chọn — dòng chữ ngay dưới ô cho bạn xem "
         "trước thứ tự đó. Muốn đổi vị trí thì bỏ chọn rồi chọn lại theo trình tự mong muốn.")
b.bullet("Bấm Chọn tất cả để lấy hết 13 trường, hoặc Bỏ chọn hết rồi chọn lại từ đầu.")
b.bullet("Bấm Xuất file. Trong lúc chờ, cạnh nút hiện dòng “Đã tải …/… dòng” rồi “Đang dựng file "
         "…/… dòng”. Xong thì tệp tự tải về máy.")
b.para("Tệp xuất theo đúng bộ lọc đang áp dụng chứ không chỉ trang bạn đang xem. Bộ lọc không ra "
       "dòng nào thì hệ thống báo không có dữ liệu để xuất.")

# ============================================= PHAN 9: LICH SU
b.h1("PHẦN 9: LỊCH SỬ THAY ĐỔI")

b.para("Lịch sử cho biết ai đã làm gì với phiếu: tạo mới, sửa trường nào (giá trị cũ → giá trị "
       "mới), đổi trạng thái và lý do kèm theo. Xem được ở hai chỗ, nội dung như nhau.")

b.h2("1. Xem từ danh sách")
b.para("Mở menu ba chấm ở cột Hành động của dòng phiếu rồi chọn Lịch sử.")
b.image("18-lich-su-popup.png", "Cửa sổ Lịch sử thay đổi")

b.h2("2. Xem từ màn chi tiết")
b.para("Mở màn chi tiết, cuộn xuống khối Lịch sử rồi bấm nút “Xem lịch sử”. Bấm “Thu gọn” để đóng "
       "lại.")
b.image("09-lich-su.png", "Khối Lịch sử trong màn chi tiết")

b.h2("3. Cách đọc lịch sử")
b.bullet("Các mục xếp theo thời gian, mới nhất ở trên cùng.")
b.bullet("Mỗi mục ghi: thời điểm, tên hành động (Tạo mới / Thay đổi thông tin / Thay đổi trạng "
         "thái), người thực hiện kèm phòng ban, rồi tới khối chi tiết thay đổi.")
b.bullet("Trong khối chi tiết, giá trị cũ màu đỏ và giá trị mới màu xanh, có mũi tên nối giữa hai "
         "giá trị.")
b.bullet("Thay đổi ở bảng thiết bị được ghi rõ: thiết bị nào thêm mới, thiết bị nào bị xóa, thiết "
         "bị nào sửa và sửa đúng trường nào.")
b.bullet("Thao tác Từ chối hiện kèm lý do đã nhập, nên bạn tra lại được vì sao phiếu bị trả về.")
b.para("Bấm nút Bộ lọc để lọc theo Loại hoạt động, Người thực hiện hoặc khoảng ngày; bấm Làm mới "
       "để nạp lại danh sách lịch sử.")

# ============================================= PHAN 10: LUU Y
b.h1("PHẦN 10: NHỮNG LƯU Ý THƯỜNG GẶP")

b.h2("1. Vào màn mà không thấy phiếu mình vừa lập")
b.para("Kiểm tra bạn đang vào từ menu nào. Vào từ Bán hàng chỉ thấy phiếu của chính bạn; vào từ "
       "CSKH thấy toàn bộ phiếu trong phạm vi quyền. Ngoài ra, nếu bạn đang lọc theo điều kiện cũ "
       "thì bấm Làm mới để xóa bộ lọc.")

b.h2("2. Người khác không thấy phiếu tôi vừa lưu nháp")
b.para("Đúng như thiết kế. Phiếu ở trạng thái Đang tạo chỉ người lập nhìn thấy, kể cả quản trị hệ "
       "thống cũng không thấy. Muốn người khác thấy thì bấm Lưu và gửi.")

b.h2("3. Không thấy nút Sửa hoặc nút Xóa")
b.para("Hai nút này chỉ có ở phiếu Đang tạo do chính bạn lập. Phiếu đã gửi đi thì không sửa và "
       "không xóa được nữa — nếu cần sửa, hãy nhờ phòng tiếp nhận từ chối để phiếu quay về Đang "
       "tạo.")

b.h2("4. Không thấy ba nút của phòng tiếp nhận")
b.para("Kiểm tra lần lượt: bạn có quyền “Xử lý yêu cầu sửa chữa” không, phiếu có đang ở Chờ xử lý "
       "không, phòng tiếp nhận của phiếu có phải phòng bạn không, và phiếu đã có phiếu xử lý chưa. "
       "Thiếu một điều kiện là cả ba nút không hiện.")

b.h2("5. Trạng thái phiếu tự đổi mà tôi không làm gì")
b.para("Bình thường. Các chứng từ phía sau (phiếu xử lý, phiếu cung cấp thông tin, báo giá, hợp "
       "đồng) tự cập nhật ngược trạng thái lên phiếu yêu cầu, kèm Người xử lý và Ngày xử lý, để bạn "
       "theo dõi tiến độ.")

b.h2("6. Bản in danh sách báo vượt mức 2.000 dòng")
b.para("Hãy thu hẹp bộ lọc trước khi in — lọc theo khoảng ngày, theo trạng thái hoặc theo khách "
       "hàng. Cần danh sách dài hơn thì dùng Xuất Excel, chức năng này không giới hạn số dòng.")

b.finish()

# macOS: Word ghi danh muc hinh anh voi so thu tu deu la 1 -> danh so lai (xem _mac_docx.py)
renumber_figure_index(os.path.join(HERE, "HDSD_Yeu cau kiem tra sua chua - bao hanh.docx"))
