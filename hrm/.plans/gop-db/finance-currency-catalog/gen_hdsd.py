# -*- coding: utf-8 -*-
"""Sinh HDSD cho man Danh muc tien te (phan he Tai chinh).

Chay:  python gen_hdsd.py
"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "hdsd-documenter", "assets"))

from hdsd_engine import HdsdBuilder  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

b = HdsdBuilder(
    output=os.path.join(HERE, "HDSD_Danh muc tien te.docx"),
    shots_dir=os.path.join(HERE, "hdsd_shots"),
    cover_title="(Màn hình: Danh mục tiền tệ)",
    doc_title="HDSD - Danh mục tiền tệ",
)

# ============================================================================
b.h1("TỔNG QUAN")

b.h2("1. Mục tiêu")
b.para("Màn hình “Danh mục tiền tệ” dùng để khai báo và quản lý danh sách các loại tiền tệ cùng "
       "tỷ giá quy đổi ra Đồng Việt Nam. Đây là danh mục nền, được dùng lại ở rất nhiều nghiệp vụ "
       "phía sau: báo giá, hợp đồng, đề nghị thu tiền, đề nghị chi tiền, công nợ khách hàng và "
       "nhà cung cấp, các phiếu kế toán.")
b.para("Lưu ý quan trọng: danh mục này dùng CHUNG dữ liệu với màn tương ứng bên phần mềm cũ. "
       "Sửa ở cổng nào thì cổng còn lại cũng thấy ngay, không cần đồng bộ thủ công. Vì vậy mọi "
       "thay đổi ở đây đều ảnh hưởng tới cả hai hệ thống.")

b.h2("2. Đường dẫn truy cập")
b.para("Trên menu trái của phân hệ Tài chính, vào nhóm “Danh mục” rồi chọn “Danh mục tiền tệ” "
       "(đường dẫn: /finance/currencies).")
b.para("Mục menu này chỉ hiển thị khi tài khoản có ít nhất một trong hai quyền “Quản lý danh mục "
       "tiền tệ” hoặc “Xem danh mục tiền tệ”. Nếu không có quyền nào, mục menu bị ẩn; trường hợp "
       "gõ thẳng đường dẫn, hệ thống chuyển sang trang báo không tìm thấy và không trả về dữ liệu.")

b.h2("3. Vai trò tham gia")
b.table([
    ["Vai trò", "Thao tác chính"],
    ["Người quản lý danh mục tiền tệ",
     "Thêm mới, Sửa, Khóa / Mở khóa, Xóa tiền tệ; xem và xuất Excel."],
    ["Người dùng chỉ xem",
     "Xem danh sách, mở xem chi tiết, tìm kiếm, lọc và Xuất Excel."],
    ["Bộ phận nghiệp vụ (báo giá, hợp đồng, kế toán)",
     "Là bên sử dụng danh mục này khi lập chứng từ có ngoại tệ."],
])

b.h2("4. Các trạng thái")
b.table([
    ["Trạng thái", "Ý nghĩa"],
    ["Hoạt động", "Tiền tệ đang dùng được; chọn được khi lập chứng từ mới."],
    ["Khóa", "Ngừng sử dụng. Không còn chọn được khi lập chứng từ mới, nhưng các chứng từ đã lập "
             "trước đó vẫn hiển thị đúng tiền tệ này."],
])
b.para("Khóa và Xóa khác nhau: Khóa chỉ ngăn dùng MỚI và luôn thực hiện được; Xóa là bỏ hẳn khỏi "
       "danh mục và bị chặn nếu tiền tệ đã được dùng ở bất kỳ chứng từ nào.")

b.h2("5. Tỷ giá được cập nhật tự động hằng ngày")
b.para("Hệ thống tự cập nhật lại tỷ giá của toàn bộ danh mục vào 03:00 sáng mỗi ngày, lấy theo "
       "tỷ giá bán của Vietcombank và khớp theo Mã tiền tệ. Riêng đồng Việt Nam được bỏ qua.")
b.para("Vì vậy, tỷ giá được sửa tay hôm nay có thể thay đổi vào sáng hôm sau — đây là hành vi "
       "đúng theo thiết kế, không phải mất dữ liệu. Nếu cần một tỷ giá cố định cho một chứng từ "
       "cụ thể thì phải khai ngay trên chứng từ đó, không dựa vào danh mục.")

b.h2("6. Luồng sử dụng")
b.para("Đây là màn danh mục, không có luồng trình duyệt nhiều cấp. Trình tự sử dụng thông thường:")
b.bullet("Bước 1 — Người quản lý danh mục thêm mới tiền tệ, khai Mã, Tên và Tỷ giá.")
b.bullet("Bước 2 — Bộ phận nghiệp vụ chọn tiền tệ từ danh mục này khi lập chứng từ.")
b.bullet("Bước 3 (khi cần điều chỉnh) — Người quản lý sửa lại tỷ giá hoặc tên; các chứng từ đã "
         "lập trước đó không bị tính lại.")
b.bullet("Bước 4 (khi ngừng dùng) — Chuyển tiền tệ sang trạng thái Khóa. Chỉ xóa hẳn khi tiền tệ "
         "chưa từng được dùng ở chứng từ nào.")

# ============================================================================
b.h1("PHẦN 1: DANH SÁCH & TÌM KIẾM")

b.image("01-danh-sach.png", "Màn hình danh sách Danh mục tiền tệ")

b.h2("1. Bố cục màn hình")
b.para("Màn hình gồm hai khối xếp trên dưới:")
b.bullet("Khối trên — “Bộ lọc danh mục tiền tệ”: ô tìm nhanh, nút Tìm kiếm, nút Làm mới và nút "
         "Tìm kiếm nâng cao ở góc phải.")
b.bullet("Khối dưới — bảng “Danh mục tiền tệ”: danh sách tiền tệ, các nút thao tác ở đầu bảng và "
         "phần phân trang ở cuối bảng.")

b.h2("2. Các cột của bảng")
b.table([
    ["Cột", "Nội dung"],
    ["STT", "Số thứ tự tính theo trang đang xem. Sang trang 2 với cỡ trang 10 thì bắt đầu từ 11."],
    ["Mã tiền tệ", "Mã viết tắt, ví dụ USD, EUR, VNĐ. Là giá trị duy nhất trong danh mục."],
    ["Tên tiền tệ", "Tên đầy đủ. Nếu tiền tệ có khai Tên gọi khác thì hiện thêm một dòng phụ "
                    "“Tên gọi khác: …” ngay dưới tên."],
    ["Tỷ giá (VNĐ)", "Một đơn vị tiền tệ đó bằng bao nhiêu Đồng Việt Nam. Hiển thị dạng "
                     "26.520,00 — dấu chấm ngăn hàng nghìn, dấu phẩy ngăn phần thập phân."],
    ["Cập nhật", "Ngày giờ thay đổi gần nhất. Chưa có thì hiện dấu gạch ngang."],
    ["Trạng thái", "Nhãn Hoạt động hoặc Khóa. Nút Khóa / Mở khóa nằm NGAY TRONG cột này."],
    ["Hành động", "Ba nút: Xem (hình con mắt), Sửa (hình bút chì), Xóa (hình thùng rác)."],
])
b.para("Lưu ý: nút Khóa / Mở khóa không nằm ở cột Hành động mà nằm cạnh nhãn trạng thái. "
       "Đây là điểm nhiều người tìm nhầm chỗ.")

b.h2("3. Tìm nhanh")
b.para("Ô tìm nhanh nằm ngay dưới tiêu đề khối lọc, có dòng gợi ý “Tìm theo mã, tên hoặc tên gọi "
       "khác...”. Ô này quét đồng thời cả ba trường: Mã tiền tệ, Tên tiền tệ và Tên gọi khác.")
b.bullet("Gõ một phần chuỗi là đủ, không cần gõ đúng nguyên mã. Gõ “US” vẫn ra USD.")
b.bullet("Không phân biệt chữ hoa và chữ thường.")
b.bullet("Phải bấm nút Tìm kiếm (hoặc nhấn Enter) thì danh sách mới lọc. Gõ xong để đó thì bảng "
         "vẫn giữ nguyên.")

b.h2("4. Tìm kiếm nâng cao")
b.para("Bấm nút “Tìm kiếm nâng cao” ở góc phải khối lọc để mở thêm ô lọc Trạng thái.")
b.image("02-bo-loc-nang-cao.png", "Khối tìm kiếm nâng cao với ô lọc Trạng thái")
b.table([
    ["Tiêu chí lọc", "Cách dùng"],
    ["Trạng thái", "Chọn Hoạt động hoặc Khóa. Ô này không có lựa chọn “Tất cả”; muốn bỏ lọc thì "
                   "bấm dấu x trên ô để xóa giá trị đang chọn."],
])
b.para("Nút Làm mới xóa toàn bộ điều kiện đang lọc VÀ nạp lại danh sách ngay, không cần bấm "
       "Tìm kiếm thêm lần nữa.")
b.para("Hệ thống ghi nhớ bộ lọc trong 10 phút: rời màn rồi quay lại trong khoảng thời gian đó thì "
       "điều kiện lọc cũ vẫn còn. Nếu thấy danh sách không đủ như mong đợi, hãy bấm Làm mới trước.")

b.h2("5. Sắp xếp và phân trang")
b.bullet("Bấm vào tiêu đề các cột Mã tiền tệ, Tên tiền tệ, Tỷ giá (VNĐ), Cập nhật, Trạng thái để "
         "sắp xếp. Bấm lần nữa để đảo chiều.")
b.bullet("Cột STT và cột Hành động không sắp xếp được.")
b.bullet("Cuối bảng có dòng “Hiển thị a – b / N”: a và b là khoảng dòng đang xem, N là tổng số "
         "tiền tệ khớp bộ lọc hiện tại.")
b.bullet("Ô “Số dòng/trang” cho chọn 5, 10, 20 hoặc 50 dòng mỗi trang.")

# ============================================================================
b.h1("PHẦN 2: PHÂN QUYỀN & HƯỚNG DẪN THEO QUYỀN")

b.h2("1. Bảng quyền của màn hình")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / khu vực tương ứng"],
    ["Xem danh mục tiền tệ",
     "Vào màn hình, xem danh sách, tìm kiếm và lọc, mở xem chi tiết, xuất Excel.",
     "Nút Xem trên mỗi dòng; nút Xuất Excel."],
    ["Quản lý danh mục tiền tệ",
     "Toàn bộ quyền trên, cộng thêm: thêm mới, sửa, khóa, mở khóa và xóa tiền tệ.",
     "Nút Tạo mới; nút Sửa và nút Xóa trên mỗi dòng; nút Khóa / Mở khóa trong cột Trạng thái."],
])
b.para("Danh mục này KHÔNG phân quyền theo công ty, phòng ban hay bộ phận: mọi người vào được "
       "màn đều nhìn thấy cùng một danh sách.")

b.h2("2. Người dùng có quyền “Xem danh mục tiền tệ”")
b.para("Vào được màn hình và thấy đầy đủ danh sách. Trên màn hình sẽ KHÔNG có nút Tạo mới; mỗi "
       "dòng chỉ có nút Xem; cột Trạng thái chỉ hiện nhãn mà không có nút Khóa / Mở khóa. "
       "Nút Xuất Excel vẫn dùng được bình thường.")
b.bullet("Xem chi tiết một tiền tệ: bấm nút Xem (hình con mắt) trên dòng cần xem.")
b.bullet("Tìm kiếm và lọc: dùng ô tìm nhanh và ô lọc Trạng thái như hướng dẫn ở Phần 1.")
b.bullet("Kết xuất: bấm Xuất Excel để tải danh sách theo đúng bộ lọc đang áp dụng.")

b.h2("3. Người dùng có quyền “Quản lý danh mục tiền tệ”")
b.para("Thấy đầy đủ mọi nút: Tạo mới, Xuất Excel; trên mỗi dòng có Xem, Sửa, Xóa; trong cột "
       "Trạng thái có nút Khóa hoặc Mở khóa tùy trạng thái hiện tại của dòng đó.")
b.bullet("Thêm mới — xem Phần 3.")
b.bullet("Sửa và xem chi tiết — xem Phần 4.")
b.bullet("Khóa và Mở khóa — xem Phần 5.")
b.bullet("Xóa — xem Phần 6.")

b.h2("4. Khi thiếu quyền")
b.para("Nếu không có quyền tương ứng, nút thao tác sẽ không hiển thị. Trường hợp truy cập trực "
       "tiếp bằng đường dẫn hoặc bằng công cụ ngoài giao diện, hệ thống từ chối và báo không có "
       "quyền; dữ liệu không bị thay đổi.")

# ============================================================================
b.h1("PHẦN 3: THÊM MỚI TIỀN TỆ")
b.para("Yêu cầu quyền “Quản lý danh mục tiền tệ”.")

b.para("Bấm nút “Tạo mới” ở đầu bảng. Hệ thống mở cửa sổ “Thêm tiền tệ”.")
b.image("03-them-tien-te.png", "Cửa sổ Thêm tiền tệ")

b.h2("1. Các trường nhập")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị mặc định khi mở form", "Ghi chú"],
    ["Mã tiền tệ", "Ô chữ", "Có", "Để trống", "Phải là duy nhất. Trùng sẽ báo “Mã tiền tệ đã tồn "
                                              "tại”. Tối đa 255 ký tự."],
    ["Trạng thái", "Danh sách chọn", "Không", "Hoạt động", "Chọn Hoạt động hoặc Khóa."],
    ["Tên tiền tệ", "Ô chữ", "Có", "Để trống", "Được phép trùng với tiền tệ khác. Tối đa 255 ký tự."],
    ["Tên gọi khác", "Ô chữ", "Không", "Để trống", "Tên gọi thông dụng, ví dụ “Đô la Mỹ”. Nếu có "
                                                  "nhập, danh sách sẽ hiện thêm dòng phụ."],
    ["Tỷ giá (VNĐ)", "Ô số", "Có", "Để trống", "Phải lớn hơn 0, tối đa 999.999,99. Dùng dấu phẩy "
                                              "làm dấu thập phân theo chuẩn Việt Nam."],
])
b.para("Ba trường bắt buộc — Mã tiền tệ, Tên tiền tệ và Tỷ giá (VNĐ) — có dấu sao đỏ bên cạnh nhãn.")

b.h2("2. Các nút của cửa sổ")
b.table([
    ["Nút", "Tác dụng"],
    ["Lưu", "Lưu tiền tệ, đóng cửa sổ, báo “Thêm mới thành công” và nạp lại danh sách."],
    ["Lưu & Tiếp tục", "Lưu tiền tệ nhưng GIỮ cửa sổ mở và xóa trắng các ô để nhập bản ghi tiếp "
                       "theo. Dùng khi cần khai nhiều tiền tệ liên tiếp."],
    ["Đóng", "Đóng cửa sổ. Nếu đang nhập dở, hệ thống hỏi xác nhận trước khi đóng."],
])

b.h2("3. Thông báo lỗi thường gặp")
b.table([
    ["Tình huống", "Hệ thống báo"],
    ["Bỏ trống ô bắt buộc", "Ô viền đỏ, hiện chữ đỏ “Bắt buộc phải nhập” ngay dưới ô. "
                            "Cửa sổ không đóng, dữ liệu đã nhập vẫn còn."],
    ["Mã tiền tệ đã có trong danh mục", "“Mã tiền tệ đã tồn tại”."],
    ["Tỷ giá nhập chữ", "“Tỷ giá phải là số”."],
    ["Tỷ giá bằng 0 hoặc số âm", "“Tỷ giá phải lớn hơn 0”."],
    ["Tỷ giá lớn hơn 999.999,99", "“Tỷ giá tối đa 999.999,99”."],
])

# ============================================================================
b.h1("PHẦN 4: SỬA VÀ XEM CHI TIẾT")

b.h2("1. Xem chi tiết")
b.para("Bấm nút Xem (hình con mắt) trên dòng cần xem. Cửa sổ “Xem tiền tệ” mở ra với đầy đủ "
       "thông tin nhưng mọi ô đều bị làm mờ, không gõ được và không có nút Lưu — chỉ có nút Đóng. "
       "Người chỉ có quyền “Xem danh mục tiền tệ” vẫn mở được cửa sổ này.")
b.image("04-xem-tien-te.png", "Cửa sổ Xem tiền tệ ở chế độ chỉ đọc")

b.h2("2. Sửa")
b.para("Yêu cầu quyền “Quản lý danh mục tiền tệ”. Bấm nút Sửa (hình bút chì) trên dòng cần sửa. "
       "Cửa sổ “Sửa tiền tệ” mở ra với các ô đã điền sẵn dữ liệu hiện có; cạnh tiêu đề có hiện "
       "thông tin lần cập nhật gần nhất.")
b.bullet("Các trường và ràng buộc giống hệt phần Thêm mới.")
b.bullet("Cửa sổ Sửa KHÔNG có nút “Lưu & Tiếp tục” — chỉ có Lưu và Đóng.")
b.bullet("Giữ nguyên mã của chính tiền tệ đang sửa là hợp lệ, hệ thống không báo trùng.")
b.bullet("Lưu xong hiện thông báo “Cập nhật thành công”, danh sách nạp lại và cột Cập nhật đổi "
         "sang thời điểm vừa sửa.")

b.h2("3. Cảnh báo khi thoát lúc chưa lưu")
b.para("Nếu đã sửa nội dung mà bấm Đóng hoặc bấm dấu X ở góc trên bên phải, hệ thống cảnh báo dữ "
       "liệu chưa được lưu và hỏi xác nhận. Chọn ở lại thì cửa sổ vẫn giữ nguyên nội dung đang gõ; "
       "chọn thoát thì dữ liệu cũ không bị thay đổi. Nếu chưa sửa gì thì cửa sổ đóng ngay, "
       "không hỏi lại.")

# ============================================================================
b.h1("PHẦN 5: KHÓA VÀ MỞ KHÓA")
b.para("Yêu cầu quyền “Quản lý danh mục tiền tệ”.")

b.h2("1. Khóa một tiền tệ")
b.bullet("Bước 1: Tìm dòng cần khóa, nhìn sang cột Trạng thái.")
b.bullet("Bước 2: Bấm nút hình ổ khóa đóng nằm cạnh nhãn “Hoạt động”.")
b.bullet("Bước 3: Hệ thống mở hộp “Xác nhận khóa” có nêu tên tiền tệ. Bấm “Khóa” để thực hiện, "
         "hoặc “Hủy” để bỏ qua.")
b.image("05-xac-nhan-khoa.png", "Hộp xác nhận khóa tiền tệ")
b.para("Sau khi khóa: hiện thông báo “Khóa thành công”, dòng đổi nhãn sang “Khóa” và nút trong "
       "cột Trạng thái đổi thành hình ổ khóa mở.")

b.h2("2. Mở khóa")
b.para("Làm ngược lại: bấm nút hình ổ khóa mở cạnh nhãn “Khóa”, xác nhận trong hộp “Xác nhận mở "
       "khóa”. Hệ thống báo “Mở khóa thành công” và dòng quay lại nhãn “Hoạt động”.")

b.h2("3. Điều gì xảy ra sau khi khóa")
b.bullet("Tiền tệ không còn xuất hiện trong danh sách chọn khi lập chứng từ MỚI.")
b.bullet("Các chứng từ đã lập trước đó vẫn hiển thị đúng tiền tệ này, mở ra sửa vẫn thấy đủ và "
         "lưu lại không mất dữ liệu.")
b.bullet("Tiền tệ vẫn nằm trong danh sách của màn này và tìm lại được bằng bộ lọc Trạng thái = Khóa.")
b.para("Khóa luôn thực hiện được, kể cả với tiền tệ đang được dùng ở nhiều chứng từ. Đây là cách "
       "khuyến nghị để ngừng sử dụng một loại tiền tệ.")

# ============================================================================
b.h1("PHẦN 6: XÓA TIỀN TỆ")
b.para("Yêu cầu quyền “Quản lý danh mục tiền tệ”.")

b.h2("1. Khi nào xóa được")
b.para("Chỉ xóa được tiền tệ CHƯA từng được dùng ở bất kỳ chứng từ nào. Với các tiền tệ đang "
       "được dùng, nút Xóa bị làm mờ và không bấm được; rê chuột vào nút sẽ hiện chú thích cho "
       "biết tiền tệ đang được sử dụng.")
b.para("Trạng thái mờ này xuất hiện chậm hơn bảng khoảng vài trăm mili giây. Nếu bấm ngay khi màn "
       "vừa hiện, hệ thống vẫn chặn lại và hiện thông báo đỏ nêu tên tối đa ba nơi đang dùng, kèm "
       "gợi ý chuyển tiền tệ sang trạng thái Khóa thay vì xóa.")

b.h2("2. Các bước xóa")
b.bullet("Bước 1: Bấm nút Xóa (hình thùng rác màu đỏ) trên dòng cần xóa.")
b.bullet("Bước 2: Đọc hộp “Xác nhận xóa” — câu hỏi có nêu tên tiền tệ để đối chiếu.")
b.bullet("Bước 3: Bấm “Xóa” để thực hiện hoặc “Hủy” để bỏ qua.")
b.image("06-xac-nhan-xoa.png", "Hộp xác nhận xóa tiền tệ")
b.para("Sau khi xóa: hiện thông báo “Xóa thành công”, dòng biến mất khỏi danh sách và tổng số "
       "dưới bảng giảm đi một. Nếu đó là dòng cuối cùng của trang, màn hình tự lùi về trang trước.")

b.h2("3. Khuyến nghị")
b.para("Trong thực tế nên ưu tiên Khóa thay vì Xóa. Xóa là thao tác không lùi lại được và màn "
       "hình này không lưu lịch sử thay đổi.")

# ============================================================================
b.h1("PHẦN 7: XUẤT EXCEL")
b.para("Mọi người vào được màn hình đều dùng được chức năng này.")
b.bullet("Bước 1: Đặt bộ lọc và thứ tự sắp xếp mong muốn trên màn hình.")
b.bullet("Bước 2: Bấm nút “Xuất Excel” ở đầu bảng.")
b.bullet("Bước 3: Chờ thông báo “Xuất Excel thành công” rồi mở file tải về.")
b.para("File xuất ra lấy đúng tập dữ liệu đang lọc chứ không phải toàn bộ danh mục, và lấy đủ mọi "
       "dòng khớp bộ lọc chứ không chỉ trang đang xem. Nếu kết quả lọc rỗng, hệ thống báo không "
       "có dữ liệu để xuất.")

# ============================================================================
b.h1("PHẦN CHI TIẾT: THAO TÁC TỪNG BƯỚC")

b.h2("A. Khai báo một loại tiền tệ mới")
b.bullet("Bước A1: Vào phân hệ Tài chính → Danh mục → Danh mục tiền tệ.")
b.bullet("Bước A2: Bấm “Tạo mới”.")
b.bullet("Bước A3: Nhập Mã tiền tệ (ví dụ SGD), Tên tiền tệ (ví dụ SGD), Tên gọi khác nếu có "
         "(ví dụ Đô la Singapore).")
b.bullet("Bước A4: Nhập Tỷ giá (VNĐ) theo chuẩn Việt Nam, dùng dấu phẩy cho phần thập phân — "
         "ví dụ 19.850,50.")
b.bullet("Bước A5: Để Trạng thái là “Hoạt động” nếu muốn dùng ngay.")
b.bullet("Bước A6: Bấm “Lưu”. Kiểm tra dòng mới đã xuất hiện trong danh sách với đúng tỷ giá.")

b.h2("B. Điều chỉnh tỷ giá của một loại tiền tệ")
b.bullet("Bước B1: Tìm tiền tệ bằng ô tìm nhanh.")
b.bullet("Bước B2: Bấm nút Sửa trên dòng đó.")
b.bullet("Bước B3: Sửa ô Tỷ giá (VNĐ), bấm “Lưu”.")
b.bullet("Bước B4: Đối chiếu lại giá trị trên danh sách. Nhớ rằng hệ thống sẽ tự cập nhật lại tỷ "
         "giá này vào 03:00 sáng hôm sau theo tỷ giá bán của Vietcombank.")

b.h2("C. Ngừng sử dụng một loại tiền tệ")
b.bullet("Bước C1: Thử bấm nút Xóa. Nếu tiền tệ đang được dùng, hệ thống chặn và gợi ý chuyển "
         "sang trạng thái Khóa.")
b.bullet("Bước C2: Bấm nút hình ổ khóa trong cột Trạng thái, xác nhận trong hộp “Xác nhận khóa”.")
b.bullet("Bước C3: Kiểm tra lại ở một màn lập chứng từ — tiền tệ đó không còn trong danh sách chọn.")
b.bullet("Bước C4: Mở một chứng từ cũ đã dùng tiền tệ đó để chắc chắn dữ liệu cũ không bị mất.")

b.h2("D. Kết xuất danh mục ra Excel")
b.bullet("Bước D1: Đặt bộ lọc, ví dụ Trạng thái = Hoạt động.")
b.bullet("Bước D2: Bấm “Xuất Excel”.")
b.bullet("Bước D3: Mở file tải về, đối chiếu số dòng với tổng ghi ở cuối bảng trên màn hình.")

b.finish()
