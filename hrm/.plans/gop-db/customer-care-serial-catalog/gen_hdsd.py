# -*- coding: utf-8 -*-
"""Sinh HDSD cho man Danh muc serial thiet bi lam dich vu (CSKH).

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
    output=os.path.join(HERE, "HDSD_Danh muc serial thiet bi lam dich vu.docx"),
    shots_dir=os.path.join(HERE, "hdsd_shots"),
    cover_title="(Màn hình: Danh mục serial thiết bị làm dịch vụ)",
    doc_title="HDSD - Danh mục serial thiết bị làm dịch vụ",
)

# ============================================================================
b.h1("TỔNG QUAN")

b.h2("1. Mục tiêu")
b.para("Màn hình “Danh mục serial thiết bị làm dịch vụ” dùng để TRA CỨU toàn bộ serial thiết bị "
       "đang được làm dịch vụ trong hệ thống, kèm tên hàng và khách hàng đang sở hữu thiết bị đó.")
b.para("Tình huống dùng thường gặp: khách hàng gọi tới báo hỏng và chỉ đọc được số serial trên "
       "máy. Nhân viên tiếp nhận gõ số serial vào màn này để biết ngay đó là thiết bị gì, của "
       "khách hàng nào, còn đang sử dụng hay đã ngưng — trước khi lập phiếu yêu cầu dịch vụ.")

b.h2("2. Đây là màn CHỈ ĐỌC")
b.para("Màn hình này chỉ cho xem, lọc và xuất Excel. KHÔNG có nút Tạo mới, không có nút Sửa, "
       "không có nút Xóa và không có cột Hành động.")
b.para("Mọi thao tác thêm, sửa, đổi trạng thái hay xóa serial được thực hiện ở màn "
       "“Quản lý khách hàng”, tab “Trang thiết bị” của khách hàng tương ứng. Sau khi thay đổi ở "
       "đó, dữ liệu hiện ngay tại màn này.")

b.h2("3. Đường dẫn truy cập")
b.para("Trên menu trái của phân hệ Chăm sóc khách hàng, vào nhóm “Danh mục - Dịch vụ” rồi chọn "
       "“Danh mục serial thiết bị làm dịch vụ” (đường dẫn: /customer-care/serials).")
b.para("Mục menu chỉ hiển thị khi tài khoản có quyền “Xem danh mục serial thiết bị làm dịch vụ”. "
       "Không có quyền thì mục menu bị ẩn; gõ thẳng đường dẫn sẽ bị chuyển sang trang báo không "
       "tìm thấy và không trả về dữ liệu nào.")

b.h2("4. Vai trò tham gia")
b.table([
    ["Vai trò", "Thao tác chính"],
    ["Nhân viên tiếp nhận yêu cầu dịch vụ", "Tra cứu serial để xác định thiết bị và khách hàng."],
    ["Bộ phận kỹ thuật", "Tra cứu danh sách thiết bị của một khách hàng trước khi đi hiện trường."],
    ["Bộ phận quản lý khách hàng", "Là bên khai báo và cập nhật serial ở màn Quản lý khách hàng → "
                                   "tab Trang thiết bị."],
])

b.h2("5. Các trạng thái serial")
b.table([
    ["Trạng thái", "Ý nghĩa"],
    ["Đang sử dụng", "Thiết bị còn đang được khách hàng sử dụng và còn làm dịch vụ."],
    ["Ngưng sử dụng", "Thiết bị đã ngừng sử dụng hoặc không còn làm dịch vụ nữa."],
])
b.para("Lưu ý khi đối chiếu số liệu: trong dữ liệu cũ có một nhóm nhỏ serial (khoảng hơn chục "
       "dòng trên tổng số hơn 21.000) mang giá trị trạng thái không theo quy ước. Những dòng này "
       "vẫn hiện nhãn “Ngưng sử dụng” trên bảng nhưng KHÔNG lọt vào kết quả khi lọc theo trạng "
       "thái. Vì vậy tổng của hai lần lọc (Đang sử dụng + Ngưng sử dụng) sẽ nhỏ hơn tổng khi "
       "không lọc một chút. Đây là dữ liệu tồn từ hệ thống cũ, đang chờ nghiệp vụ chốt cách xử lý.")

b.h2("6. Quy mô dữ liệu")
b.para("Danh mục có khoảng 21.600 serial — lớn hơn nhiều so với các danh mục khác. Hai điều cần "
       "lưu ý khi sử dụng:")
b.bullet("Nên lọc hoặc tìm kiếm trước khi làm việc, thay vì cuộn qua hàng nghìn trang.")
b.bullet("Xuất Excel toàn bộ danh mục mất khoảng 10 đến 20 giây và tải dữ liệu theo nhiều lượt. "
         "Trong lúc đó không nên rời màn hình hoặc bấm lại nút.")

# ============================================================================
b.h1("PHẦN 1: DANH SÁCH & TRA CỨU")

b.image("01-danh-sach.png", "Màn hình Danh mục serial thiết bị làm dịch vụ")

b.h2("1. Bố cục màn hình")
b.bullet("Khối trên — “Bộ lọc serial thiết bị làm dịch vụ”: ô tìm nhanh, nút Tìm kiếm, nút Làm "
         "mới và nút Tìm kiếm nâng cao ở góc phải.")
b.bullet("Khối dưới — bảng “Danh mục serial thiết bị làm dịch vụ” cùng nút Xuất Excel ở đầu bảng "
         "và phần phân trang ở cuối bảng.")

b.h2("2. Các cột của bảng")
b.table([
    ["Cột", "Nội dung"],
    ["STT", "Số thứ tự tính theo trang đang xem."],
    ["Serial thiết bị làm dịch vụ", "Số serial in trên thiết bị."],
    ["Tên hàng", "Tên mặt hàng / thiết bị tương ứng với serial. Nội dung dài được xuống dòng "
                 "trong ô."],
    ["Khách hàng", "Khách hàng đang sở hữu thiết bị, hiển thị dạng mã và tên đầy đủ."],
    ["Trạng thái", "Nhãn Đang sử dụng hoặc Ngưng sử dụng."],
    ["Người tạo", "Người đã khai báo serial."],
    ["Người cập nhật", "Người sửa serial gần nhất. Serial cũ chưa từng được sửa thì ô này để "
                       "trống — đây là bình thường, không phải lỗi."],
    ["Ngày cập nhật", "Ngày thay đổi gần nhất."],
])
b.para("Bảng KHÔNG có cột Hành động vì đây là màn chỉ đọc. So với màn tương ứng ở phần mềm cũ, "
       "bản mới bổ sung ba cột Người tạo, Người cập nhật và Ngày cập nhật.")

b.h2("3. Tìm nhanh")
b.para("Ô tìm nhanh có dòng gợi ý “Tìm theo serial, tên hàng hoặc khách hàng...”. Ô này quét đồng "
       "thời cả ba trường: Serial, Tên hàng và Khách hàng.")
b.bullet("Gõ một phần chuỗi là đủ, kể cả phần nằm ở giữa số serial.")
b.bullet("Không phân biệt chữ hoa và chữ thường.")
b.bullet("Phải bấm nút Tìm kiếm hoặc nhấn Enter thì danh sách mới lọc.")

b.h2("4. Tìm kiếm nâng cao")
b.para("Bấm nút “Tìm kiếm nâng cao” ở góc phải khối lọc để mở thêm bốn tiêu chí.")
b.table([
    ["Tiêu chí lọc", "Cách dùng"],
    ["Khách hàng", "Chọn một khách hàng để xem toàn bộ thiết bị của họ. Đây là cách dùng phổ "
                   "biến nhất trước khi đi hiện trường."],
    ["Trạng thái", "Chọn Đang sử dụng hoặc Ngưng sử dụng."],
    ["Người tạo", "Chọn một người; danh sách chỉ liệt kê những người thực sự đã khai báo serial, "
                  "không phải toàn bộ nhân viên."],
    ["Người cập nhật", "Chọn một người; kết quả là các serial do người đó sửa gần nhất."],
])
b.para("Các điều kiện được kết hợp theo kiểu VÀ: kết quả phải thỏa đồng thời mọi điều kiện đã "
       "chọn, kể cả từ khóa ở ô tìm nhanh. Nút Làm mới xóa toàn bộ điều kiện và nạp lại danh sách "
       "ngay. Hệ thống ghi nhớ bộ lọc trong 10 phút, nên khi thấy danh sách thiếu so với mong đợi "
       "hãy bấm Làm mới trước.")

b.h2("5. Sắp xếp và phân trang")
b.bullet("Bấm tiêu đề các cột Serial, Tên hàng, Khách hàng, Trạng thái, Người tạo, Người cập nhật "
         "và Ngày cập nhật để sắp xếp; bấm lần nữa để đảo chiều. Cột STT không sắp xếp được.")
b.bullet("Thứ tự sắp xếp được giữ nguyên khi chuyển trang và khi đang lọc.")
b.bullet("Cuối bảng có dòng “Hiển thị a – b / N”: N là tổng số serial khớp bộ lọc hiện tại, "
         "không phải tổng toàn bộ danh mục.")
b.bullet("Ô “Số dòng/trang” cho chọn 5, 10, 20 hoặc 50 dòng mỗi trang. Với dữ liệu lớn nên tăng "
         "cỡ trang thay vì bấm chuyển trang liên tục.")

# ============================================================================
b.h1("PHẦN 2: PHÂN QUYỀN & HƯỚNG DẪN THEO QUYỀN")

b.h2("1. Bảng quyền của màn hình")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / khu vực tương ứng"],
    ["Xem danh mục serial thiết bị làm dịch vụ",
     "Vào màn hình, xem danh sách, tìm kiếm, lọc, sắp xếp và xuất Excel.",
     "Toàn bộ màn hình và nút Xuất Excel."],
])
b.para("Màn hình chỉ có DUY NHẤT một quyền vì đây là màn chỉ đọc — không có thao tác ghi dữ liệu "
       "nào nên không cần quyền quản lý riêng.")

b.h2("2. Người dùng có quyền “Xem danh mục serial thiết bị làm dịch vụ”")
b.para("Vào được màn hình, thấy đầy đủ danh sách của mọi khách hàng và mọi công ty, dùng được "
       "toàn bộ chức năng tìm kiếm, lọc, sắp xếp và Xuất Excel.")
b.para("Danh mục này KHÔNG phân quyền theo công ty, phòng ban hay bộ phận: hai người thuộc hai "
       "công ty khác nhau vẫn thấy cùng một tổng số serial.")

b.h2("3. Người dùng không có quyền")
b.para("Mục menu “Danh mục serial thiết bị làm dịch vụ” không hiển thị. Trường hợp gõ thẳng đường "
       "dẫn, hệ thống chuyển sang trang báo không tìm thấy và không trả về bất kỳ dòng dữ liệu "
       "nào. Do dữ liệu này gắn với thông tin khách hàng nên việc kiểm soát quyền được thực hiện "
       "cả ở giao diện lẫn ở tầng dữ liệu.")

# ============================================================================
b.h1("PHẦN 3: XUẤT EXCEL")
b.para("Yêu cầu quyền “Xem danh mục serial thiết bị làm dịch vụ” — tức là mọi người vào được màn "
       "hình đều dùng được.")

b.h2("1. Các bước")
b.bullet("Bước 1: Đặt bộ lọc và thứ tự sắp xếp mong muốn. Nên lọc trước để file gọn và chạy nhanh.")
b.bullet("Bước 2: Bấm nút “Xuất Excel” ở đầu bảng.")
b.bullet("Bước 3: Chờ tới khi hệ thống hiện thông báo kết quả. Trong lúc chờ, nút bị vô hiệu và "
         "KHÔNG nên rời màn hình.")
b.bullet("Bước 4: Mở file tải về và đối chiếu số dòng với con số ghi trong thông báo.")

b.h2("2. Đặc điểm cần biết")
b.bullet("Thông báo sau khi xuất nêu rõ SỐ DÒNG đã xuất — dùng con số này để đối chiếu với tổng "
         "ghi ở cuối bảng.")
b.bullet("File lấy đúng tập dữ liệu đang lọc chứ không phải toàn bộ danh mục, và lấy đủ mọi dòng "
         "khớp bộ lọc chứ không chỉ trang đang xem.")
b.bullet("Thứ tự dòng trong file khớp thứ tự đang hiển thị trên màn hình.")
b.bullet("Nếu kết quả lọc rỗng, hệ thống báo “Không có dữ liệu để xuất” và không tải file rỗng về.")
b.bullet("Xuất toàn bộ hơn 21.000 dòng mất khoảng 10 đến 20 giây. Nếu chuyển sang màn khác giữa "
         "chừng, việc xuất có thể bị hủy — hãy chờ xong rồi mới rời màn.")

# ============================================================================
b.h1("PHẦN 4: QUAN HỆ VỚI MÀN QUẢN LÝ KHÁCH HÀNG")

b.h2("1. Nơi khai báo và sửa serial")
b.para("Toàn bộ dữ liệu của màn này đến từ tab “Trang thiết bị” trong màn “Quản lý khách hàng”. "
       "Muốn thêm một serial mới, sửa thông tin hoặc chuyển serial sang trạng thái Ngưng sử dụng, "
       "phải vào đúng khách hàng ở màn đó.")

b.h2("2. Dữ liệu phản ánh ngay lập tức")
b.table([
    ["Thao tác ở màn Quản lý khách hàng", "Kết quả tại màn này"],
    ["Thêm serial mới cho một khách hàng",
     "Serial xuất hiện trong danh mục với đúng tên hàng, khách hàng; cột Người tạo là người "
     "vừa thao tác."],
    ["Sửa thông tin serial",
     "Danh mục hiện thông tin mới; cột Người cập nhật và Ngày cập nhật đổi theo lần sửa vừa rồi."],
    ["Chuyển serial sang Ngưng sử dụng",
     "Serial đổi nhãn trạng thái và chỉ còn lọt vào kết quả khi lọc Trạng thái = Ngưng sử dụng."],
    ["Xóa serial", "Serial biến mất khỏi danh mục, tổng số dưới bảng giảm đi một."],
])

b.h2("3. Đối chiếu với phần mềm cũ")
b.para("Hai cổng đọc chung một nguồn dữ liệu nên tổng số serial ở hai bên phải bằng nhau. Điểm "
       "khác biệt duy nhất là bản mới hiển thị thêm ba cột Người tạo, Người cập nhật và Ngày cập "
       "nhật, cùng hai tiêu chí lọc tương ứng — đây là bổ sung có chủ ý, không phải sai lệch dữ liệu.")

# ============================================================================
b.h1("PHẦN CHI TIẾT: THAO TÁC TỪNG BƯỚC")

b.h2("A. Tra cứu nhanh một serial khách hàng đọc qua điện thoại")
b.bullet("Bước A1: Vào phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → Danh mục serial thiết "
         "bị làm dịch vụ.")
b.bullet("Bước A2: Gõ số serial vào ô tìm nhanh, bấm “Tìm kiếm”.")
b.bullet("Bước A3: Đọc cột Tên hàng để biết thiết bị gì, cột Khách hàng để biết của ai, cột Trạng "
         "thái để biết còn đang sử dụng hay không.")
b.bullet("Bước A4: Nếu không ra kết quả, thử gõ ngắn hơn (chỉ vài ký tự giữa của serial) vì có "
         "thể khách hàng đọc nhầm một vài ký tự.")

b.h2("B. Lấy danh sách toàn bộ thiết bị của một khách hàng")
b.bullet("Bước B1: Bấm “Tìm kiếm nâng cao”.")
b.bullet("Bước B2: Ở ô Khách hàng, chọn khách hàng cần xem.")
b.bullet("Bước B3: Nếu chỉ muốn thiết bị còn dùng, chọn thêm Trạng thái = Đang sử dụng.")
b.bullet("Bước B4: Bấm “Tìm kiếm”, đọc tổng số ở cuối bảng.")
b.bullet("Bước B5: Bấm “Xuất Excel” để mang danh sách đi hiện trường.")

b.h2("C. Kiểm tra các serial do một nhân viên khai báo")
b.bullet("Bước C1: Bấm “Tìm kiếm nâng cao”.")
b.bullet("Bước C2: Chọn nhân viên ở ô Người tạo, bấm “Tìm kiếm”.")
b.bullet("Bước C3: Sắp xếp theo cột Ngày cập nhật giảm dần để xem các bản ghi mới nhất trước.")

b.h2("D. Xử lý khi serial cần sửa thông tin")
b.bullet("Bước D1: Tra cứu serial tại màn này, ghi lại tên khách hàng đang sở hữu.")
b.bullet("Bước D2: Sang màn Quản lý khách hàng, mở đúng khách hàng đó.")
b.bullet("Bước D3: Vào tab “Trang thiết bị”, tìm serial và sửa tại đó.")
b.bullet("Bước D4: Quay lại màn này, tìm lại serial để xác nhận thông tin đã cập nhật và cột "
         "Người cập nhật đã ghi tên mình.")

b.finish()
