# -*- coding: utf-8 -*-
"""Sinh tai lieu HDSD man "Phieu xu ly yeu cau".

Anh chup that: .plans/gop-db/warranty-repair-handle-request/wrhr_shots/ (Playwright, 03/09/2026)
Chay:  python3 .plans/gop-db/warranty-repair-handle-request/gen_hdsd.py
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
    output=os.path.join(HERE, "HDSD_Phieu xu ly yeu cau.docx"),
    shots_dir=os.path.join(HERE, "wrhr_shots"),
    cover_title="(Màn hình: Phiếu xử lý yêu cầu)",
    doc_title="HDSD - Phiếu xử lý yêu cầu")

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
    ["Phiếu xử lý", "Một bản ghi trên màn hình này. Là chứng từ thứ hai của luồng dịch vụ, do "
                    "phòng tiếp nhận lập sau khi nhận yêu cầu của khách."],
    ["Phiếu yêu cầu gốc", "Phiếu yêu cầu kiểm tra sửa chữa – bảo hành mà phiếu xử lý này được lập "
                          "ra từ đó."],
    ["Nguyên nhân", "Công việc hoặc lỗi thiết bị, lấy từ danh mục công việc – lỗi thiết bị. Mỗi "
                    "hàng hóa có danh sách nguyên nhân riêng."],
    ["Hành động", "Hướng xử lý cho từng thiết bị: “Tư vấn điện thoại” (xong luôn) hoặc “Cung cấp "
                  "thông tin làm báo giá” (đi tiếp)."],
    ["Phiếu cung cấp thông tin (CCTT)", "Chứng từ thứ ba của luồng, dùng để chuẩn bị dữ liệu làm "
                                        "báo giá dịch vụ."],
    ["Hàng hóa tương đương", "Hàng hóa trong danh mục được chọn thay cho thiết bị khách khai tự "
                             "do, để lấy đúng danh sách nguyên nhân và giá dịch vụ."],
    ["Lưu nháp", "Lưu lại để hoàn thiện sau. Phiếu ở trạng thái Đang tạo và chỉ mình bạn nhìn thấy."],
    ["Lưu và gửi", "Gửi phiếu đi. Phiếu chuyển sang Chờ CCTT và không sửa được nữa."],
])

b.h2("2. Bảng cập nhật nội dung tài liệu")
b.table([
    ["Ngày", "Nội dung cập nhật", "Người thực hiện"],
    ["03/09/2026", "Biên soạn lần đầu theo phiên bản màn hình trên hệ thống HRM.", "Nhóm phát triển"],
])

b.h2("3. Giới thiệu chung")
b.para("Màn hình Phiếu xử lý yêu cầu dùng để xử lý yêu cầu khách hàng đã gửi tới: người của phòng "
       "tiếp nhận xem lại từng thiết bị khách báo hỏng, xác định nguyên nhân và quyết định hướng "
       "đi tiếp cho từng thiết bị.")
b.para("Vị trí trong luồng dịch vụ:")
b.bullet("Nhân viên kinh doanh lập Phiếu yêu cầu kiểm tra sửa chữa – bảo hành và gửi cho phòng bạn.")
b.bullet("Bạn mở phiếu yêu cầu đó và bấm “Tạo phiếu xử lý yêu cầu” — phiếu xử lý ra đời từ đây, "
         "màn hình này KHÔNG có nút Tạo mới.")
b.bullet("Với từng thiết bị, bạn chọn Nguyên nhân và Hành động. Chọn “Tư vấn điện thoại” cho TẤT "
         "CẢ thiết bị thì luồng kết thúc luôn; còn lại thì phiếu chuyển tiếp để làm báo giá.")
b.bullet("Người có quyền lập phiếu cung cấp thông tin nhận thông báo, mở phiếu của bạn và lập "
         "Phiếu cung cấp thông tin làm báo giá; nếu thông tin chưa đủ họ có thể Không duyệt và trả "
         "phiếu về cho bạn kèm lý do.")
b.para("Đường dẫn màn hình: /customer-care/warranty-repair-handle-requests")

b.h2("4. Quyền và phạm vi dữ liệu")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / tab tương ứng", "Ghi chú"],
    ["Xử lý yêu cầu sửa chữa", "Lập ra phiếu xử lý từ màn Yêu cầu kiểm tra sửa chữa – bảo hành.",
     "Nút “Tạo phiếu xử lý yêu cầu” ở màn phiếu yêu cầu",
     "Không có quyền này thì không mở được màn lập phiếu."],
    ["Tạo phiếu cung cấp thông tin",
     "Xử lý tiếp phiếu đang Chờ CCTT: lập phiếu cung cấp thông tin hoặc trả phiếu về.",
     "Tạo phiếu cung cấp thông tin · Không duyệt",
     "Không ràng buộc phòng ban: có quyền là làm được."],
    ["Quản lý danh mục công việc - lỗi thiết bị",
     "Khai bổ sung nguyên nhân ngay trong lúc lập phiếu.", "Nút “Thêm nhanh” ở ô Nguyên nhân",
     "Không có quyền thì nút không hiển thị."],
    ["Xem phiếu xử lý yêu cầu … theo tổng công ty", "Nhìn thấy phiếu của mọi công ty.",
     "Khối lọc Công ty – Phòng ban", "Cấp rộng nhất."],
    ["Xem phiếu xử lý yêu cầu … theo công ty", "Nhìn thấy phiếu thuộc công ty của mình.",
     "Khối lọc Công ty – Phòng ban", "—"],
    ["Xem phiếu xử lý yêu cầu … theo phòng ban",
     "Nhìn thấy phiếu thuộc phòng mình quản lý và phòng mình đang công tác.",
     "Khối lọc Công ty – Phòng ban", "Kèm luôn cả phiếu do chính mình lập."],
    ["(Không có quyền nào)", "Chỉ nhìn thấy phiếu do chính mình lập.", "—",
     "Vẫn sửa, xóa, in, xuất Excel được với phiếu của mình."],
])

b.h3("4.1. Người dùng không có quyền nào")
b.para("Danh sách chỉ hiện phiếu do bạn lập. Bạn sửa, xóa (khi phiếu còn Đang tạo), in, xuất Excel "
       "và xem lịch sử bình thường. Hai nút Tạo phiếu cung cấp thông tin và Không duyệt không hiển "
       "thị. Nút Thêm nhanh ở ô Nguyên nhân cũng không hiển thị.")

b.h3("4.2. Người dùng có quyền “Xử lý yêu cầu sửa chữa”")
b.para("Bạn là người LẬP RA phiếu xử lý. Sang màn Yêu cầu kiểm tra sửa chữa – bảo hành, mở phiếu "
       "gửi về phòng bạn rồi bấm “Tạo phiếu xử lý yêu cầu”. Hướng dẫn điền phiếu ở PHẦN 3.")
b.para("Nếu không có quyền này, nút đó không hiển thị; trường hợp truy cập trực tiếp bằng đường "
       "dẫn, hệ thống báo không thể lập phiếu xử lý cho phiếu yêu cầu này.")

b.h3("4.3. Người dùng có quyền “Tạo phiếu cung cấp thông tin”")
b.para("Bạn là người xử lý tiếp. Khi có phiếu chuyển sang Chờ CCTT, bạn nhận được thông báo trên "
       "chuông. Mở phiếu đó, bạn thấy hai nút: “Tạo phiếu cung cấp thông tin” để đi tiếp, và "
       "“Không duyệt” để trả phiếu về cho người xử lý sửa lại. Hướng dẫn ở PHẦN 6.")
b.para("Quyền này KHÔNG ràng buộc phòng ban — có quyền là xử lý được phiếu của mọi phòng trong "
       "phạm vi dữ liệu bạn được xem.")

b.h3("4.4. Người dùng có quyền xem theo cấp")
b.para("Bạn nhìn thấy phiếu của nhiều người khác theo đúng cấp được cấp quyền, và khối lọc Công ty "
       "– Phòng ban xuất hiện trong Tìm kiếm nâng cao. Riêng phiếu ở trạng thái Đang tạo của người "
       "khác thì không ai nhìn thấy, kể cả quản trị hệ thống.")

# ============================================ PHAN 1: TRUY CAP & BO CUC
b.h1("PHẦN 1: TRUY CẬP MÀN HÌNH VÀ BỐ CỤC")

b.h2("1. Vào màn này bằng cách nào")
b.para("Vào phân hệ CSKH → nhóm “Kiểm tra bảo hành sửa chữa” → bấm “Phiếu xử lý yêu cầu”.")
b.para("Đây là lối vào duy nhất có trên menu, và nó hiển thị toàn bộ phiếu trong phạm vi quyền của "
       "bạn. Nếu bạn gõ thẳng đường dẫn màn hình mà không kèm tham số của menu, danh sách sẽ chỉ "
       "hiện phiếu do chính bạn lập — nên hãy luôn vào bằng menu.")
b.para("Nếu mở màn mà danh sách trống hoặc ít hơn mong đợi, hãy kiểm tra bạn vào bằng menu hay gõ "
       "thẳng đường dẫn — hai cách hiển thị phạm vi khác nhau.")

b.h2("2. Bố cục màn hình")
b.image("01-danh-sach.png", "Màn Phiếu xử lý yêu cầu")
b.para("Màn hình chia làm hai khối:")
b.bullet("Khối trên là Bộ lọc danh sách: ô tìm nhanh, nút Tìm kiếm, Làm mới, Cài đặt bộ lọc và "
         "Tìm kiếm nâng cao.")
b.bullet("Khối dưới là bảng danh sách: thanh công cụ (Xuất Excel, In danh sách, biểu tượng Cấu "
         "hình cột hiển thị), bảng dữ liệu và phân trang.")
b.para("Lưu ý: thanh công cụ KHÔNG có nút Tạo mới. Phiếu xử lý chỉ sinh ra từ màn Yêu cầu kiểm tra "
       "sửa chữa – bảo hành.")

b.h2("3. Các cột của bảng danh sách")
b.table([
    ["Cột", "Nội dung", "Mặc định"],
    ["STT", "Số thứ tự dòng, chạy liên tục qua các trang.", "Hiện"],
    ["Số phiếu xử lý", "Số phiếu do hệ thống sinh. Bấm vào để mở màn chi tiết.", "Hiện"],
    ["Khách hàng", "Mã và tên khách hàng, lấy từ phiếu yêu cầu gốc.", "Hiện"],
    ["Số phiếu yêu cầu", "Số của phiếu yêu cầu gốc. Bấm vào để mở phiếu đó.", "Ẩn"],
    ["Tên thiết bị liên quan", "Danh sách thiết bị trong phiếu.", "Ẩn"],
    ["Người yêu cầu / Ngày nhận yêu cầu", "Người lập phiếu yêu cầu gốc và thời điểm gửi.", "Ẩn"],
    ["Địa chỉ sửa chữa", "Nơi thực hiện việc sửa chữa.", "Ẩn"],
    ["Người xử lý", "Người lập phiếu xử lý này.", "Hiện"],
    ["Ngày tạo", "Thời điểm lập phiếu xử lý.", "Hiện"],
    ["Ngày xử lý", "Thời điểm phiếu cung cấp thông tin được gửi đi. Trống nếu chưa tới bước đó.",
     "Ẩn"],
    ["Người cập nhật / Ngày cập nhật", "Người sửa gần nhất; trống nếu phiếu chưa ai sửa.", "Ẩn"],
    ["Trạng thái", "Tình trạng hiện tại của phiếu, xem bảng ở mục 4.", "Hiện"],
    ["Hành động", "Các nút thao tác của từng dòng.", "Hiện"],
])

b.h2("4. Ý nghĩa các trạng thái")
b.table([
    ["Trạng thái", "Nghĩa là gì", "Do đâu mà có"],
    ["Đang tạo", "Phiếu nháp, chưa gửi đi. Chỉ mình bạn nhìn thấy.",
     "Bạn bấm Lưu nháp, hoặc phiếu bị Không duyệt trả về."],
    ["Chờ CCTT", "Đã gửi đi, đang chờ người có quyền lập phiếu cung cấp thông tin xử lý.",
     "Bạn bấm Lưu và gửi."],
    ["Đang CCTT", "Phiếu cung cấp thông tin đã được lập nhưng còn ở dạng nháp.",
     "Chứng từ phía sau cập nhật."],
    ["Đã CCTT", "Phiếu cung cấp thông tin đã gửi đi làm báo giá.", "Chứng từ phía sau cập nhật."],
    ["Đã tư vấn điện thoại", "Xử lý xong bằng tư vấn qua điện thoại, luồng kết thúc tại đây.",
     "Mọi thiết bị trên phiếu đều chọn Hành động “Tư vấn điện thoại”."],
    ["Chờ CCTT bổ sung", "Trạng thái kế thừa dữ liệu cũ; nghiệp vụ hiện tại không sinh ra.", "—"],
])

# ============================================= PHAN 2: TIM KIEM VA LOC
b.h1("PHẦN 2: TÌM KIẾM, LỌC VÀ TÙY CHỈNH HIỂN THỊ")

b.h2("1. Tìm nhanh")
b.para("Gõ từ khóa vào ô ở đầu màn hình rồi nhấn Enter hoặc bấm Tìm kiếm. Ô này tìm theo bốn thứ: "
       "số phiếu xử lý, số phiếu yêu cầu, tên khách hàng và tên người xử lý. Gõ một phần cũng tìm "
       "ra.")

b.h2("2. Tìm kiếm nâng cao")
b.para("Bấm nút Tìm kiếm nâng cao ở góc phải khối lọc; khối tiêu chí mở ra bên dưới.")
b.image("02-bo-loc-nang-cao.png", "Khối Tìm kiếm nâng cao")
b.table([
    ["Ô lọc", "Cách dùng"],
    ["Trạng thái", "Chọn một trạng thái trong danh sách ở PHẦN 1 mục 4."],
    ["Số phiếu yêu cầu", "Gõ số phiếu yêu cầu gốc rồi nhấn Enter."],
    ["Khách hàng", "Bấm vào ô rồi gõ tên hoặc mã khách; danh sách gợi ý hiện dần."],
    ["Tên thiết bị", "Gõ tên thiết bị rồi nhấn Enter."],
    ["Model", "Gõ model thiết bị rồi nhấn Enter."],
    ["Ngày tạo từ / đến", "Chọn khoảng ngày lập phiếu xử lý."],
    ["Công ty – Phòng ban", "Chỉ hiện nếu bạn có quyền xem theo cấp. Lọc theo đơn vị của người lập "
                            "phiếu."],
])
b.para("Các ô dạng danh sách tự tìm lại ngay khi chọn; ô gõ tay thì phải nhấn Enter hoặc bấm Tìm "
       "kiếm. Nút Làm mới xóa hết điều kiện lọc.")

b.h2("3. Cài đặt bộ lọc")
b.para("Bấm nút Cài đặt bộ lọc để chọn ô lọc nào hiện ra ở khối Tìm kiếm nâng cao.")
b.image("14-cai-dat-bo-loc.png", "Cửa sổ Cài đặt bộ lọc")
b.bullet("Bỏ tích ô nào thì ô lọc đó không hiện nữa.")
b.bullet("Kéo biểu tượng chấm ở đầu dòng để đổi thứ tự.")
b.bullet("Bấm Lưu để áp dụng, Khôi phục mặc định để trở lại như ban đầu, Đóng để thoát mà không lưu.")

b.h2("4. Tùy chỉnh cột")
b.para("Bấm biểu tượng hình cột ở cuối thanh công cụ (chỉ dẫn ghi “Cấu hình cột hiển thị”).")
b.image("13-cau-hinh-cot.png", "Cửa sổ Tùy chỉnh cột")
b.bullet("Tích chọn cột muốn hiện, bỏ tích cột muốn ẩn. Cột STT và Số phiếu xử lý có ổ khóa — "
         "luôn hiển thị.")
b.bullet("Kéo biểu tượng ba gạch để đổi thứ tự cột, rồi bấm Lưu.")
b.para("Hai cột đáng bật thêm khi cần theo dõi: “Số phiếu yêu cầu” để đối chiếu với chứng từ gốc, "
       "và “Ngày xử lý” để biết phiếu đã được lập phiếu cung cấp thông tin hay chưa.")

# ============================================= PHAN 3: LAP PHIEU
b.h1("PHẦN 3: LẬP PHIẾU XỬ LÝ")

b.h2("1. Mở màn lập phiếu")
b.para("Màn hình này không có nút Tạo mới. Cách lập phiếu:")
b.bullet("Vào màn Yêu cầu kiểm tra sửa chữa – bảo hành (CSKH → Kiểm tra bảo hành sửa chữa).")
b.bullet("Tìm phiếu yêu cầu đang ở trạng thái Chờ xử lý, gửi về phòng bạn.")
b.bullet("Bấm biểu tượng thêm tài liệu ở cột Hành động, hoặc mở chi tiết phiếu rồi bấm nút “Tạo "
         "phiếu xử lý yêu cầu”.")
b.para("Nếu nút không hiển thị, kiểm tra bốn điều kiện: bạn có quyền “Xử lý yêu cầu sửa chữa” "
       "không, phiếu có đang ở Chờ xử lý không, phòng tiếp nhận có phải phòng bạn không, và phiếu "
       "đã có phiếu xử lý chưa. Mỗi phiếu yêu cầu chỉ lập được MỘT phiếu xử lý.")
b.image("07-lap-phieu.png", "Màn Lập phiếu xử lý với dữ liệu chép sẵn")

b.h2("2. Khối Thông tin yêu cầu — chỉ để đọc")
b.para("Toàn bộ khối trên cùng là dữ liệu chép sẵn từ phiếu yêu cầu gốc, bạn KHÔNG sửa được: Phiếu "
       "yêu cầu, Người yêu cầu, Phòng yêu cầu, Ngày nhận yêu cầu, Khách hàng, Người liên hệ, Số "
       "điện thoại liên hệ, Địa chỉ sửa chữa.")
b.para("Muốn sửa những thông tin này thì phải sửa ở phiếu yêu cầu gốc, không sửa ở đây.")
b.para("Nếu phiếu từng bị trả về, ngay dưới khối này có thêm dòng “Lý do không duyệt” — đọc kỹ dòng "
       "đó để biết cần bổ sung gì trước khi gửi lại.")

b.h2("3. Khối Danh sách thiết bị cần xử lý")
b.para("Toàn bộ thiết bị của phiếu yêu cầu gốc được chép sang đây. Bạn không thêm được dòng mới — "
       "chỉ xóa bớt dòng không cần xử lý. Cuộn ngang bảng để thấy hết các cột.")
b.image("08-lap-phieu-cot-phai.png", "Các cột bên phải: Nguyên nhân, Hành động, File đính kèm")
b.table([
    ["Cột", "Cách nhập", "Bắt buộc", "Giá trị điền sẵn"],
    ["Tên hàng hóa", "Chỉ đọc, lấy từ phiếu yêu cầu gốc.", "—", "Theo phiếu gốc"],
    ["Thương hiệu / Model / Serial / Số BBBGNT-BBXNCV / Nội dung yêu cầu",
     "Chỉ đọc, lấy từ phiếu yêu cầu gốc.", "—", "Theo phiếu gốc"],
    ["Nguyên nhân", "Chọn một hoặc nhiều nguyên nhân trong danh sách của đúng hàng hóa đó.",
     "Có khi Lưu và gửi", "Trống"],
    ["Hành động", "Chọn “Tư vấn điện thoại” hoặc “Cung cấp thông tin làm báo giá”.",
     "Có khi Lưu và gửi", "Trống"],
    ["Nội dung xử lý", "Chỉ hiện khi Hành động là “Tư vấn điện thoại”. Ghi rõ đã tư vấn gì cho "
                       "khách.", "Có — kể cả khi Lưu nháp", "Trống"],
    ["File đính kèm", "Bấm Chọn tệp để tải ảnh hoặc tài liệu. Nhận PDF, ảnh, Word, Excel.",
     "Không", "Trống"],
    ["Hành động (cột cuối)", "Bấm biểu tượng thùng rác để bỏ thiết bị khỏi phiếu.", "—", "—"],
])

b.h3("3.1. Chọn hàng hóa tương đương")
b.para("Thiết bị do khách khai tự do (không có trong danh mục hàng hóa) sẽ có nút “Chọn hàng hóa "
       "tương đương” ngay dưới tên. Bấm nút đó, tìm và chọn hàng hóa gần đúng nhất trong danh mục.")
b.para("Việc này bắt buộc trước khi gửi phiếu, vì hệ thống lấy danh sách nguyên nhân và giá dịch vụ "
       "theo hàng hóa trong danh mục. Chưa chọn mà bấm Lưu và gửi thì hệ thống báo “Phải chọn hàng "
       "hóa tương đương”.")
b.para("Sau khi chọn, dòng thiết bị hiện tên hàng hóa trong danh mục kèm dòng phụ “Thiết bị tương "
       "đương” ghi tên khách khai — bạn vẫn đối chiếu được.")

b.h3("3.2. Chọn nguyên nhân")
b.para("Bấm vào ô Nguyên nhân của dòng thiết bị, danh sách hiện ra. Chọn được nhiều nguyên nhân "
       "cho một thiết bị; mỗi nguyên nhân đã chọn hiện thành một thẻ, bấm dấu × trên thẻ để bỏ.")
b.para("Danh sách chỉ liệt kê nguyên nhân đã khai cho ĐÚNG hàng hóa đó, không phải cả danh mục. "
       "Hàng hóa chưa khai nguyên nhân nào thì ô hiện dòng nhắc “Hàng hóa này chưa khai lỗi thiết "
       "bị nào trong danh mục.” kèm nút Thêm nhanh.")
b.para("Nguyên nhân đã bị khóa trong danh mục vẫn hiện ở phiếu đang dùng nó, có biểu tượng ổ khóa "
       "phía trước để bạn biết là mục đã ngừng dùng.")

b.h3("3.3. Thêm nhanh một nguyên nhân mới")
b.para("Khi hàng hóa chưa có nguyên nhân phù hợp, bấm nút “Thêm nhanh” ngay tại ô Nguyên nhân — "
       "không cần rời màn sang danh mục.")
b.image("09-them-nhanh-nguyen-nhan.png", "Cửa sổ Thêm nhanh công việc / lỗi thiết bị")
b.table([
    ["Trường", "Cách nhập", "Bắt buộc", "Giá trị điền sẵn"],
    ["Loại công việc / lỗi", "Chọn một trong sáu loại: Lỗi đã xác định, Lỗi chưa xác định, Lắp đặt "
                             "bàn giao, Thiết kế nền móng, Tư vấn khảo sát, Giám sát thi công.",
     "Có", "Trống"],
    ["Tên công việc / Tình trạng lỗi", "Gõ tên công việc hoặc mô tả tình trạng lỗi.", "Có", "Trống"],
    ["Định mức công", "Số công định mức cho việc này.", "Không", "Trống"],
    ["Định mức đàm phán giá (%)", "Tỷ lệ được phép đàm phán giá.", "Không", "Trống"],
    ["VAT (%)", "Thuế suất áp dụng.", "Không", "Trống"],
    ["Đơn giá bán", "Giá bán dịch vụ.", "Không", "Trống"],
    ["Hệ số công nghệ", "Hệ số nhân theo mức độ công nghệ.", "Không", "Trống"],
    ["Ghi chú", "Thông tin bổ sung.", "Không", "Trống"],
])
b.para("Bấm Lưu. Nguyên nhân mới được ghi vào danh mục, gắn luôn cho hàng hóa của dòng đang thao "
       "tác và tự tích chọn vào ô Nguyên nhân — bạn không phải chọn lại.")
b.para("Nguyên nhân khai ở đây chỉ gắn cho hàng hóa đang chọn. Muốn dùng cho hàng hóa khác thì vào "
       "Danh mục → Công việc, lỗi thiết bị để khai thêm.")
b.para("Nút Thêm nhanh chỉ hiện với người có quyền “Quản lý danh mục công việc - lỗi thiết bị”.")

b.h3("3.4. Chọn hành động — quyết định hướng đi của phiếu")
b.para("Đây là ô quan trọng nhất của màn hình. Hai lựa chọn:")
b.bullet("“Cung cấp thông tin làm báo giá”: thiết bị này cần báo giá. Phiếu sẽ đi tiếp sang bước "
         "lập phiếu cung cấp thông tin.")
b.bullet("“Tư vấn điện thoại”: đã hướng dẫn khách qua điện thoại, không cần báo giá. Chọn xong thì "
         "ô “Nội dung xử lý” hiện ra ngay dưới và bắt buộc phải nhập — ghi rõ đã tư vấn gì.")
b.para("CẢNH BÁO quan trọng: nếu TẤT CẢ thiết bị trên phiếu đều chọn “Tư vấn điện thoại” thì phiếu "
       "chuyển thẳng sang trạng thái “Đã tư vấn điện thoại” và luồng dịch vụ kết thúc — kể cả khi "
       "bạn chỉ bấm Lưu nháp. Phiếu yêu cầu gốc cũng đóng theo. Chỉ chọn hướng này khi chắc chắn "
       "công việc đã xong.")
b.para("Đổi Hành động từ “Tư vấn điện thoại” sang lựa chọn khác thì ô Nội dung xử lý bị xóa trắng.")

b.h2("4. Lưu phiếu")
b.h3("4.1. Lưu nháp")
b.para("Dùng khi chưa xác định xong nguyên nhân hoặc còn chờ thông tin từ khách. Hệ thống không "
       "bắt buộc Nguyên nhân và Hành động; chỉ bắt buộc Nội dung xử lý cho những dòng đã chọn "
       "“Tư vấn điện thoại”.")
b.para("Lưu xong hệ thống báo “Lưu thành công” và quay về danh sách. Phiếu ở trạng thái Đang tạo, "
       "chỉ mình bạn nhìn thấy.")
b.h3("4.2. Lưu và gửi")
b.para("Dùng khi phiếu đã đầy đủ. Hệ thống hỏi xác nhận “Bạn đồng ý lưu và gửi?”; bấm Đồng ý để "
       "tiếp tục.")
b.para("Lúc này hệ thống bắt buộc: mỗi thiết bị phải có ít nhất một Nguyên nhân và một Hành động; "
       "thiết bị khách khai tự do phải chọn hàng hóa tương đương; phiếu phải còn ít nhất một thiết "
       "bị; không chọn trùng nguyên nhân trong cùng một thiết bị. Thiếu chỗ nào thì chỗ đó viền đỏ "
       "kèm dòng chữ đỏ, cửa sổ không đóng và dữ liệu đã nhập vẫn còn.")
b.para("Gửi thành công, hệ thống báo “Gửi phiếu xử lý thành công”. Ba việc xảy ra cùng lúc:")
b.bullet("Phiếu xử lý chuyển sang Chờ CCTT (hoặc Đã tư vấn điện thoại nếu mọi thiết bị đều tư vấn "
         "điện thoại).")
b.bullet("Phiếu yêu cầu gốc chuyển sang Đã xử lý, và được ghi tên bạn vào cột Người xử lý.")
b.bullet("Mọi người có quyền “Tạo phiếu cung cấp thông tin” cùng công ty với bạn nhận được thông "
         "báo trên chuông.")
b.para("Từ lúc này bạn KHÔNG sửa và KHÔNG xóa phiếu được nữa.")

# ============================================= PHAN 4: SUA PHIEU
b.h1("PHẦN 4: SỬA PHIẾU XỬ LÝ")

b.para("Bạn chỉ sửa được phiếu ở trạng thái Đang tạo và do chính bạn lập. Phiếu đã gửi đi thì nút "
       "Sửa không hiển thị; phiếu bị Không duyệt quay về Đang tạo nên sửa lại được.")
b.bullet("Cách 1: ở danh sách, bấm biểu tượng bút chì ở cột Hành động.")
b.bullet("Cách 2: mở màn chi tiết rồi bấm nút Sửa ở cuối trang.")
b.image("06-sua.png", "Màn Sửa phiếu xử lý")
b.para("Màn sửa giống màn lập phiếu, tiêu đề có kèm số phiếu. Bạn chọn lại nguyên nhân, đổi hành "
       "động, sửa nội dung xử lý, thay tệp đính kèm hoặc bỏ bớt thiết bị, rồi bấm Lưu nháp hoặc "
       "Lưu và gửi.")
b.para("Nếu bạn gõ thẳng đường dẫn màn sửa của một phiếu đã gửi, hệ thống tự chuyển về màn chi tiết "
       "và báo phiếu đã gửi đi nên không cập nhật được.")

# ============================================= PHAN 5: XEM CHI TIET
b.h1("PHẦN 5: XEM CHI TIẾT PHIẾU")

b.para("Ở danh sách, bấm vào số phiếu xử lý ở cột thứ hai.")
b.image("04-chi-tiet.png", "Màn Chi tiết phiếu xử lý")
b.bullet("Khối Thông tin yêu cầu: các ô chỉ đọc; góc phải ghi người xử lý và thời điểm lập phiếu. "
         "Ô “Phiếu yêu cầu” là liên kết mở phiếu yêu cầu gốc.")
b.bullet("Khối Danh sách thiết bị: nguyên nhân liệt kê từng dòng, hành động hiện kèm dòng phụ "
         "“Nội dung xử lý” nếu có.")
b.bullet("Khối Lịch sử: bấm “Xem lịch sử” để mở, xem PHẦN 8.")
b.bullet("Thanh nút cuối trang: chỉ hiện những thao tác bạn được phép làm với phiếu này.")
b.para("Nếu phiếu không thuộc phạm vi bạn được xem, hoặc đã bị xóa, hệ thống chuyển sang trang báo "
       "không tìm thấy — đây là cách bảo vệ dữ liệu, không phải lỗi.")

# ============================ PHAN 6: XU LY PHIEU DANG CHO CCTT
b.h1("PHẦN 6: XỬ LÝ PHIẾU ĐANG CHỜ CCTT")

b.para("Phần này dành cho người có quyền “Tạo phiếu cung cấp thông tin”. Hai thao tác dưới đây chỉ "
       "hiện khi phiếu đang ở trạng thái Chờ CCTT.")
b.image("10-chi-tiet-cho-cctt.png", "Thanh nút của phiếu đang ở trạng thái Chờ CCTT")

b.h2("1. Tạo phiếu cung cấp thông tin")
b.para("Đây là hướng đi tiếp của luồng. Bấm biểu tượng thêm tài liệu ở cột Hành động của danh sách, "
       "hoặc nút “Tạo phiếu cung cấp thông tin” ở cuối màn chi tiết.")
b.para("Hệ thống mở màn lập Phiếu cung cấp thông tin làm báo giá gắn với phiếu xử lý này. Cách "
       "điền phiếu đó xem tài liệu hướng dẫn của màn tương ứng.")
b.para("Diễn biến trạng thái sau đó:")
b.bullet("Bạn lưu nháp phiếu cung cấp thông tin → phiếu xử lý chuyển sang “Đang CCTT”.")
b.bullet("Bạn gửi phiếu cung cấp thông tin đi làm báo giá → phiếu xử lý chuyển sang “Đã CCTT” và "
         "được ghi Ngày xử lý.")
b.bullet("Phiếu cung cấp thông tin bị từ chối tiếp nhận → phiếu xử lý quay lại “Đang CCTT”.")

b.h2("2. Không duyệt phiếu")
b.para("Dùng khi thông tin trên phiếu chưa đủ để làm báo giá — thiếu nguyên nhân, thiếu ảnh hiện "
       "trạng, mô tả không rõ. Mở menu ba chấm ở cột Hành động rồi chọn Không duyệt, hoặc bấm nút "
       "Không duyệt ở màn chi tiết.")
b.image("11-khong-duyet.png", "Cửa sổ Không duyệt phiếu xử lý yêu cầu")
b.bullet("Nhập Lý do không duyệt — bắt buộc. Viết rõ cần bổ sung gì để người xử lý làm đúng ngay "
         "lần sau.")
b.bullet("Bấm nút Không duyệt (màu đỏ). Hệ thống báo “Không duyệt phiếu thành công”.")
b.para("Sau khi không duyệt: phiếu quay về trạng thái Đang tạo, người lập phiếu nhận được thông báo "
       "kèm lý do, và lý do hiện ở màn chi tiết dưới dòng “Lý do không duyệt”.")
b.para("Hai điểm cần nhớ: phiếu quay về Đang tạo nên bạn KHÔNG còn nhìn thấy phiếu đó nữa (phiếu "
       "nháp chỉ người lập nhìn thấy); và phiếu yêu cầu gốc KHÔNG bị đổi trạng thái theo, vẫn ở "
       "“Đã xử lý”.")

# ============================================= PHAN 7: XOA VA IN
b.h1("PHẦN 7: XÓA PHIẾU, IN VÀ XUẤT EXCEL")

b.h2("1. Xóa phiếu")
b.para("Bạn chỉ xóa được phiếu ở trạng thái Đang tạo và do chính bạn lập.")
b.bullet("Cách 1: ở danh sách, bấm biểu tượng thùng rác đỏ ở cột Hành động.")
b.bullet("Cách 2: mở màn chi tiết rồi bấm nút Xóa ở cuối trang.")
b.image("16-xac-nhan-xoa.png", "Hộp xác nhận xóa phiếu xử lý")
b.para("Hộp thoại hiện kèm số phiếu để bạn đối chiếu. Bấm Xóa để thực hiện, Hủy để bỏ qua.")
b.para("Xóa phiếu xử lý còn TRẢ PHIẾU YÊU CẦU GỐC về trạng thái Chờ xử lý và xóa Người xử lý, Ngày "
       "xử lý trên phiếu gốc — nhờ vậy phòng tiếp nhận lập lại được phiếu xử lý mới. Đây là cách "
       "duy nhất để làm lại phiếu xử lý khi lập sai ngay từ đầu.")
b.para("Xóa là vĩnh viễn, không khôi phục được.")

b.h2("2. In một phiếu")
b.para("Bấm biểu tượng máy in ở cột Hành động, hoặc nút In ở cuối màn chi tiết.")
b.image("05-ban-in.png", "Xem trước bản in một phiếu xử lý")
b.para("Bản in gồm tiêu đề công ty, số phiếu xử lý, số phiếu yêu cầu, người và phòng yêu cầu, "
       "thông tin khách hàng, bảng thiết bị (có thêm hai cột Nguyên nhân và Hành động so với phiếu "
       "yêu cầu), và khối ký của người lập phiếu.")
b.para("Bấm nút In màu xanh ở góc trái trên để mở hộp thoại in của trình duyệt. Bấm dấu × hoặc "
       "phím Esc để đóng cửa sổ xem trước.")

b.h2("3. In danh sách")
b.para("Bấm nút In danh sách trên thanh công cụ. Bản in lấy đúng các phiếu theo bộ lọc hiện tại, "
       "nên hãy lọc trước rồi mới in.")
b.image("15-in-danh-sach.png", "Xem trước bản in danh sách")
b.para("Bản in nằm ngang, có hai dòng “Thời gian” và “Phòng xử lý yêu cầu” cho biết bạn đang in "
       "theo điều kiện nào (không lọc thì ghi “Tất cả”).")
b.para("Bản in danh sách chỉ dựng được tối đa 2.000 dòng. Vượt mức đó, cửa sổ chỉ hiện lời nhắc "
       "nền vàng đề nghị thu hẹp bộ lọc hoặc dùng Xuất Excel — đây là cách tránh treo trình duyệt, "
       "không phải lỗi.")

b.h2("4. Xuất Excel")
b.para("Bấm nút Xuất Excel trên thanh công cụ. Cửa sổ “Chọn trường xuất file” mở ra với 6 trường "
       "được chọn sẵn trong tổng số 14.")
b.image("03-xuat-excel.png", "Cửa sổ Chọn trường xuất file")
b.bullet("Bấm vào ô Trường xuất để tích thêm trường; bấm dấu × trên mỗi thẻ để bỏ trường.")
b.bullet("Thứ tự cột trong tệp chạy đúng theo thứ tự bạn chọn — dòng chữ ngay dưới ô cho xem trước "
         "thứ tự đó.")
b.bullet("Bấm Chọn tất cả để lấy hết 14 trường, hoặc Bỏ chọn hết rồi chọn lại.")
b.bullet("Bấm Xuất file. Trong lúc chờ, cạnh nút hiện dòng “Đã tải …/… dòng” rồi “Đang dựng file "
         "…/… dòng”. Xong thì tệp tự tải về máy.")
b.para("Tệp xuất theo đúng bộ lọc đang áp dụng chứ không chỉ trang đang xem.")

# ============================================= PHAN 8: LICH SU
b.h1("PHẦN 8: LỊCH SỬ THAY ĐỔI")

b.para("Lịch sử cho biết ai đã làm gì với phiếu: tạo mới, sửa trường nào, đổi trạng thái và lý do "
       "kèm theo. Xem được ở hai chỗ, nội dung như nhau.")
b.bullet("Từ danh sách: mở menu ba chấm ở cột Hành động rồi chọn Lịch sử.")
b.bullet("Từ màn chi tiết: cuộn xuống khối Lịch sử rồi bấm “Xem lịch sử”.")
b.image("12-lich-su.png", "Khối Lịch sử trong màn chi tiết")
b.bullet("Các mục xếp theo thời gian, mới nhất ở trên cùng.")
b.bullet("Mỗi mục ghi: thời điểm, tên hành động (Tạo mới / Thay đổi thông tin / Thay đổi trạng "
         "thái), người thực hiện kèm phòng ban, rồi tới khối chi tiết thay đổi.")
b.bullet("Giá trị cũ màu đỏ, giá trị mới màu xanh.")
b.bullet("Thao tác Không duyệt hiện kèm lý do đã nhập.")
b.para("Lưu ý: thay đổi ở bảng thiết bị (nguyên nhân, hành động, nội dung xử lý) KHÔNG được ghi vào "
       "lịch sử, vì mỗi lần lưu là hệ thống ghi lại toàn bộ bảng nên nhật ký sẽ rất nhiễu. Lịch sử "
       "chỉ theo dõi phần đầu phiếu và các lần đổi trạng thái.")
b.para("Phiếu tạo từ hệ thống cũ có thể chưa có lịch sử — khi đó khối này hiện “Chưa có lịch sử "
       "thao tác nào”.")

# ============================================= PHAN 9: LUU Y
b.h1("PHẦN 9: NHỮNG LƯU Ý THƯỜNG GẶP")

b.h2("1. Không tìm thấy nút để lập phiếu xử lý")
b.para("Màn hình này không có nút Tạo mới. Phải sang màn Yêu cầu kiểm tra sửa chữa – bảo hành và "
       "bấm “Tạo phiếu xử lý yêu cầu” ở phiếu yêu cầu tương ứng. Nút đó cũng chỉ hiện khi phiếu "
       "đang Chờ xử lý, đúng phòng bạn, chưa có phiếu xử lý và bạn có quyền “Xử lý yêu cầu sửa "
       "chữa”.")

b.h2("2. Ô Nguyên nhân trống trơn, không chọn được gì")
b.para("Hàng hóa đó chưa được khai công việc / lỗi nào trong danh mục. Bấm “Thêm nhanh” ngay tại ô "
       "để khai bổ sung (cần quyền “Quản lý danh mục công việc - lỗi thiết bị”), hoặc nhờ người "
       "quản trị danh mục khai giúp.")

b.h2("3. Bấm Lưu nháp mà phiếu lại đóng luôn")
b.para("Kiểm tra cột Hành động: nếu TẤT CẢ thiết bị đều chọn “Tư vấn điện thoại” thì hệ thống hiểu "
       "công việc đã xong, phiếu chuyển sang “Đã tư vấn điện thoại” và đóng cả phiếu yêu cầu gốc — "
       "bất kể bạn bấm nút nào. Muốn phiếu đi tiếp thì ít nhất một thiết bị phải chọn “Cung cấp "
       "thông tin làm báo giá”.")

b.h2("4. Lập nhầm phiếu xử lý, muốn làm lại")
b.para("Nếu phiếu còn ở Đang tạo và do bạn lập: xóa phiếu đi. Phiếu yêu cầu gốc sẽ tự quay về "
       "Chờ xử lý để bạn lập lại từ đầu. Nếu phiếu đã gửi đi, hãy nhờ người có quyền “Tạo phiếu "
       "cung cấp thông tin” bấm Không duyệt để trả phiếu về cho bạn.")

b.h2("5. Không thấy phiếu mình vừa lưu nháp ở máy người khác")
b.para("Đúng như thiết kế. Phiếu Đang tạo chỉ người lập nhìn thấy, kể cả quản trị hệ thống cũng "
       "không thấy. Muốn người khác xử lý tiếp thì phải bấm Lưu và gửi.")

b.h2("6. Cột Ngày xử lý bỏ trống")
b.para("Cột này chỉ có giá trị khi phiếu cung cấp thông tin đã được gửi đi làm báo giá. Phiếu đang "
       "ở Chờ CCTT thì cột này trống là bình thường — không phải thiếu dữ liệu.")

b.finish()

# macOS: Word ghi danh muc hinh anh voi so thu tu deu la 1 -> danh so lai (xem _mac_docx.py)
renumber_figure_index(os.path.join(HERE, "HDSD_Phieu xu ly yeu cau.docx"))
