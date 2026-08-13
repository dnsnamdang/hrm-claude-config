# -*- coding: utf-8 -*-
"""Sinh HDSD cho man Danh muc loai tai khoan (phan he Tai chinh).

Chay:  python gen_hdsd_loai_tai_khoan.py
"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "hdsd-documenter", "assets"))

from hdsd_engine import HdsdBuilder  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

b = HdsdBuilder(
    output=os.path.join(HERE, "HDSD_Danh muc loai tai khoan.docx"),
    shots_dir=os.path.join(HERE, "hdsd_shots"),
    cover_title="(Màn hình: Danh mục loại tài khoản)",
    doc_title="HDSD - Danh mục loại tài khoản",
)

# ============================================================================
b.h1("TỔNG QUAN")

b.h2("1. Mục tiêu")
b.para("Màn hình “Danh mục loại tài khoản” dùng để khai báo các nhóm phân loại tài khoản kế toán "
       "(tài khoản tài sản, tài khoản nguồn vốn, tài khoản doanh thu…). Mỗi tài khoản trong "
       "“Danh mục tài khoản” đều được gán về một loại lấy từ danh mục này, nhờ đó hệ thống gom "
       "nhóm được tài khoản khi lên sổ sách và báo cáo.")
b.para("Lưu ý quan trọng: danh mục này dùng CHUNG dữ liệu với màn tương ứng bên phần mềm cũ. "
       "Sửa ở cổng nào thì cổng còn lại cũng thấy ngay, không cần đồng bộ thủ công.")

b.h2("2. Đường dẫn truy cập")
b.para("Trên menu trái của phân hệ Tài chính, vào nhóm “Danh mục” rồi chọn “Danh mục loại tài "
       "khoản” (đường dẫn: /finance/type-accounts).")
b.para("Mục menu chỉ hiển thị khi tài khoản có ít nhất một trong hai quyền “Quản lý danh mục loại "
       "tài khoản” hoặc “Xem danh mục loại tài khoản”. Không có quyền nào thì mục menu bị ẩn; gõ "
       "thẳng đường dẫn sẽ bị chuyển sang trang báo không tìm thấy.")

b.h2("3. Vai trò tham gia")
b.table([
    ["Vai trò", "Thao tác chính"],
    ["Người quản lý danh mục loại tài khoản",
     "Thêm mới, Sửa, Khóa / Mở khóa, Xóa; nhập danh sách từ Excel."],
    ["Người dùng chỉ xem",
     "Xem danh sách, mở xem chi tiết, xem lịch sử chỉnh sửa, tìm kiếm, lọc và xuất Excel."],
    ["Kế toán lập hệ thống tài khoản",
     "Là bên sử dụng danh mục này khi khai báo tài khoản ở màn Danh mục tài khoản."],
])

b.h2("4. Các trạng thái")
b.table([
    ["Trạng thái", "Ý nghĩa"],
    ["Hoạt động", "Loại tài khoản đang dùng được; chọn được khi khai báo tài khoản mới; sửa được."],
    ["Khóa", "Ngừng sử dụng. Không còn chọn được khi khai báo tài khoản mới và KHÔNG sửa được — "
             "muốn sửa phải Mở khóa trước. Các tài khoản đã gán loại này vẫn giữ nguyên."],
])

b.h2("5. Ràng buộc khi loại tài khoản đang được sử dụng")
b.para("Nếu đã có tài khoản nào được gán về một loại tài khoản, thì loại đó KHÔNG xóa được VÀ "
       "cũng KHÔNG khóa được. Đây là điểm khác so với Danh mục tiền tệ, nơi khóa vẫn luôn thực "
       "hiện được.")
b.para("Muốn ngừng dùng một loại tài khoản đang có tài khoản gán vào, phải chuyển hết các tài "
       "khoản đó sang loại khác trước, sau đó mới khóa hoặc xóa được.")

b.h2("6. Luồng sử dụng")
b.bullet("Bước 1 — Kế toán khai báo các loại tài khoản cần dùng ở màn này.")
b.bullet("Bước 2 — Sang màn Danh mục tài khoản, mỗi tài khoản chọn một loại từ danh sách này.")
b.bullet("Bước 3 (khi cần điều chỉnh) — Sửa lại tên hoặc ghi chú; mọi thay đổi được ghi vào lịch "
         "sử chỉnh sửa của dòng đó.")
b.bullet("Bước 4 (khi ngừng dùng) — Chuyển các tài khoản sang loại khác, rồi Khóa hoặc Xóa.")

# ============================================================================
b.h1("PHẦN 1: DANH SÁCH & TÌM KIẾM")

b.image("ltk-01-danh-sach.png", "Màn hình danh sách Danh mục loại tài khoản")

b.h2("1. Bố cục màn hình")
b.bullet("Khối trên — “Bộ lọc danh mục loại tài khoản”: ô tìm nhanh, nút Tìm kiếm, nút Làm mới, "
         "nút Tìm kiếm nâng cao ở góc phải.")
b.bullet("Khối dưới — bảng “Danh mục loại tài khoản” cùng ba nút Tạo mới, Xuất Excel, Import Excel "
         "ở đầu bảng và phần phân trang ở cuối bảng.")

b.h2("2. Các cột của bảng")
b.table([
    ["Cột", "Nội dung"],
    ["STT", "Số thứ tự tính theo trang đang xem."],
    ["Mã loại tài khoản", "Mã viết tắt, là giá trị duy nhất trong danh mục."],
    ["Tên loại tài khoản", "Tên đầy đủ, cũng phải là duy nhất. Ngay dưới tên có dòng phụ ghi "
                           "người tạo và ngày lập bản ghi."],
    ["Ghi chú", "Nội dung ghi chú thêm; để trống thì hiện dấu gạch ngang. Nội dung dài được "
                "xuống dòng trong ô, không cắt cụt."],
    ["Cập nhật", "Ngày thay đổi gần nhất kèm tên người cập nhật."],
    ["Trạng thái", "Nhãn Hoạt động hoặc Khóa. Nút Khóa / Mở khóa nằm NGAY TRONG cột này."],
    ["Hành động", "Bốn nút: Xem, Sửa, Lịch sử chỉnh sửa, Xóa."],
])

b.h2("3. Tìm nhanh")
b.para("Ô tìm nhanh có dòng gợi ý “Tìm theo mã hoặc tên loại tài khoản...”, quét cả hai trường "
       "Mã và Tên. Gõ một phần chuỗi là đủ, không phân biệt chữ hoa chữ thường. Phải bấm nút "
       "Tìm kiếm hoặc nhấn Enter thì danh sách mới lọc.")

b.h2("4. Tìm kiếm nâng cao")
b.image("ltk-02-bo-loc-nang-cao.png", "Khối tìm kiếm nâng cao với 5 tiêu chí lọc")
b.table([
    ["Tiêu chí lọc", "Cách dùng"],
    ["Trạng thái", "Chọn Hoạt động hoặc Khóa. Bỏ lọc bằng cách bấm dấu x trên ô."],
    ["Người tạo", "Chọn một người trong danh sách. Danh sách này chỉ liệt kê những người thực sự "
                  "đã tạo bản ghi, không phải toàn bộ nhân viên."],
    ["Người cập nhật", "Chọn một người; kết quả là các loại tài khoản do người đó sửa gần nhất."],
    ["Cập nhật từ", "Chọn ngày bắt đầu. Lọc theo NGÀY CẬP NHẬT (giá trị ở cột Cập nhật), "
                    "không phải ngày tạo. Tính cả ngày được chọn."],
    ["Cập nhật đến", "Chọn ngày kết thúc. Cũng tính cả ngày được chọn."],
])
b.para("Được phép chỉ nhập một trong hai ô ngày. Nút Làm mới xóa toàn bộ điều kiện và nạp lại "
       "danh sách ngay. Hệ thống ghi nhớ bộ lọc trong 10 phút, nên khi thấy danh sách thiếu so với "
       "mong đợi hãy bấm Làm mới trước.")

b.h2("5. Sắp xếp và phân trang")
b.bullet("Bấm tiêu đề cột Mã loại tài khoản hoặc Tên loại tài khoản để sắp xếp; bấm lần nữa để "
         "đảo chiều.")
b.bullet("Cuối bảng có dòng “Hiển thị a – b / N”: N là tổng số loại tài khoản khớp bộ lọc hiện tại.")
b.bullet("Ô “Số dòng/trang” cho chọn 5, 10, 20 hoặc 50 dòng mỗi trang.")

# ============================================================================
b.h1("PHẦN 2: PHÂN QUYỀN & HƯỚNG DẪN THEO QUYỀN")

b.h2("1. Bảng quyền của màn hình")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / khu vực tương ứng"],
    ["Xem danh mục loại tài khoản",
     "Vào màn hình, xem danh sách, tìm kiếm và lọc, mở xem chi tiết, xem lịch sử chỉnh sửa, "
     "xuất Excel.",
     "Nút Xem và nút Lịch sử chỉnh sửa trên mỗi dòng; nút Xuất Excel."],
    ["Quản lý danh mục loại tài khoản",
     "Toàn bộ quyền trên, cộng thêm: thêm mới, sửa, khóa, mở khóa, xóa và nhập danh sách từ Excel.",
     "Nút Tạo mới và Import Excel; nút Sửa, nút Xóa trên mỗi dòng; nút Khóa / Mở khóa trong cột "
     "Trạng thái."],
])
b.para("Danh mục này KHÔNG phân quyền theo công ty, phòng ban hay bộ phận.")

b.h2("2. Người dùng có quyền “Xem danh mục loại tài khoản”")
b.para("Vào được màn hình, thấy đầy đủ danh sách nhưng KHÔNG có nút Tạo mới và Import Excel; mỗi "
       "dòng chỉ có nút Xem và nút Lịch sử chỉnh sửa; cột Trạng thái chỉ hiện nhãn mà không có "
       "nút Khóa / Mở khóa. Nút Xuất Excel vẫn dùng được.")

b.h2("3. Người dùng có quyền “Quản lý danh mục loại tài khoản”")
b.para("Thấy đầy đủ ba nút Tạo mới, Xuất Excel, Import Excel; trên mỗi dòng có đủ Xem, Sửa, "
       "Lịch sử chỉnh sửa, Xóa; trong cột Trạng thái có nút Khóa hoặc Mở khóa.")
b.para("Nếu không có quyền này, các nút trên sẽ không hiển thị; trường hợp truy cập trực tiếp "
       "bằng đường dẫn hoặc bằng công cụ ngoài giao diện, hệ thống từ chối và báo không có quyền.")

# ============================================================================
b.h1("PHẦN 3: THÊM MỚI LOẠI TÀI KHOẢN")
b.para("Yêu cầu quyền “Quản lý danh mục loại tài khoản”.")
b.para("Bấm nút “Tạo mới” ở đầu bảng, hệ thống mở cửa sổ “Thêm loại tài khoản”.")
b.image("ltk-03-them.png", "Cửa sổ Thêm loại tài khoản")

b.h2("1. Các trường nhập")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị mặc định khi mở form", "Ghi chú"],
    ["Mã loại tài khoản", "Ô chữ", "Có", "Để trống", "Phải duy nhất. Trùng sẽ báo “Mã loại tài "
                                                    "khoản đã tồn tại”. Tối đa 255 ký tự."],
    ["Trạng thái", "Danh sách chọn", "Không", "Hoạt động", "Chọn Hoạt động hoặc Khóa."],
    ["Tên loại tài khoản", "Ô chữ", "Có", "Để trống", "Cũng phải duy nhất. Trùng sẽ báo “Tên loại "
                                                     "tài khoản đã tồn tại”. Tối đa 255 ký tự."],
    ["Ghi chú", "Ô chữ nhiều dòng", "Không", "Để trống", "Tối đa 255 ký tự."],
])
b.para("Hai trường bắt buộc — Mã và Tên loại tài khoản — có dấu sao đỏ bên cạnh nhãn.")

b.h2("2. Các nút của cửa sổ")
b.table([
    ["Nút", "Tác dụng"],
    ["Lưu", "Lưu bản ghi, đóng cửa sổ, báo thêm mới thành công và nạp lại danh sách."],
    ["Đóng", "Đóng cửa sổ. Nếu đang nhập dở, hệ thống hỏi xác nhận trước khi đóng."],
])

b.h2("3. Thông báo lỗi thường gặp")
b.table([
    ["Tình huống", "Hệ thống báo"],
    ["Bỏ trống ô bắt buộc", "Ô viền đỏ, hiện chữ đỏ “Bắt buộc phải nhập” ngay dưới ô; "
                            "cửa sổ không đóng, dữ liệu đã nhập vẫn còn."],
    ["Mã đã có trong danh mục", "“Mã loại tài khoản đã tồn tại”."],
    ["Tên đã có trong danh mục", "“Tên loại tài khoản đã tồn tại”."],
    ["Nhập quá 255 ký tự", "“Tối đa 255 ký tự”."],
])

# ============================================================================
b.h1("PHẦN 4: SỬA, XEM VÀ LỊCH SỬ CHỈNH SỬA")

b.h2("1. Xem chi tiết")
b.para("Bấm nút Xem (hình con mắt). Cửa sổ “Xem loại tài khoản” mở ra với đầy đủ thông tin nhưng "
       "mọi ô đều mờ, không gõ được và không có nút Lưu. Xem được cả bản ghi đang ở trạng thái Khóa.")

b.h2("2. Sửa")
b.para("Yêu cầu quyền “Quản lý danh mục loại tài khoản”. Bấm nút Sửa (hình bút chì); cửa sổ "
       "“Sửa loại tài khoản” mở ra với dữ liệu điền sẵn, cạnh tiêu đề hiện thông tin lần cập nhật "
       "gần nhất.")
b.bullet("Các trường và ràng buộc giống hệt phần Thêm mới.")
b.bullet("Giữ nguyên mã và tên của chính bản ghi đang sửa là hợp lệ, hệ thống không báo trùng.")
b.bullet("Nếu bản ghi đang ở trạng thái Khóa thì nút Sửa bị làm mờ; rê chuột vào sẽ hiện chú "
         "thích “Loại tài khoản đã khóa → không cho sửa”. Muốn sửa phải Mở khóa trước.")
b.bullet("Lưu xong hiện thông báo cập nhật thành công; cột Cập nhật đổi sang thời điểm và tên "
         "người vừa sửa.")
b.para("Nếu đã sửa nội dung mà bấm Đóng, hệ thống cảnh báo dữ liệu chưa được lưu và hỏi xác nhận.")

b.h2("3. Lịch sử chỉnh sửa")
b.para("Bấm nút Lịch sử chỉnh sửa (hình đồng hồ quay ngược) trên dòng cần xem. Cửa sổ “Lịch sử "
       "chỉnh sửa loại tài khoản” liệt kê các lần thay đổi, mới nhất nằm trên cùng.")
b.image("ltk-04-lich-su.png", "Cửa sổ Lịch sử chỉnh sửa loại tài khoản")
b.para("Mỗi dòng lịch sử cho biết thời điểm, người thực hiện và trường nào đã đổi từ giá trị cũ "
       "sang giá trị mới. Giá trị trạng thái hiển thị bằng nhãn tiếng Việt (Hoạt động / Khóa).")
b.table([
    ["Ô lọc trong cửa sổ lịch sử", "Cách dùng"],
    ["Trường thay đổi", "Chỉ xem các lần thay đổi của một trường cụ thể. Mặc định là Tất cả."],
    ["Người thực hiện", "Chỉ xem các lần thay đổi do một người thực hiện. Mặc định là Tất cả."],
    ["Từ ngày / Đến ngày", "Giới hạn khoảng thời gian của các lần thay đổi."],
])
b.para("Người chỉ có quyền “Xem danh mục loại tài khoản” vẫn mở được cửa sổ lịch sử này.")

# ============================================================================
b.h1("PHẦN 5: KHÓA, MỞ KHÓA VÀ XÓA")
b.para("Cả ba thao tác đều yêu cầu quyền “Quản lý danh mục loại tài khoản”.")

b.h2("1. Khóa và Mở khóa")
b.bullet("Bước 1: Nhìn sang cột Trạng thái của dòng cần thao tác.")
b.bullet("Bước 2: Bấm nút hình ổ khóa nằm cạnh nhãn trạng thái.")
b.bullet("Bước 3: Xác nhận trong hộp “Xác nhận khóa” (hoặc “Xác nhận mở khóa”). Hộp có nêu tên "
         "loại tài khoản để đối chiếu.")
b.para("Sau khi khóa: dòng đổi nhãn sang Khóa, nút Sửa của dòng đó chuyển sang mờ, và loại tài "
       "khoản không còn được chọn khi khai báo tài khoản mới. Mở khóa thì mọi thứ trở lại như cũ.")
b.para("Nếu loại tài khoản đang được tài khoản nào đó sử dụng thì nút Khóa bị làm mờ; rê chuột "
       "vào sẽ hiện chú thích “Đang được sử dụng, không thể khóa”.")

b.h2("2. Xóa")
b.bullet("Bước 1: Bấm nút Xóa (hình thùng rác màu đỏ) trên dòng cần xóa.")
b.bullet("Bước 2: Đọc hộp “Xác nhận xóa” — câu hỏi có nêu tên loại tài khoản.")
b.bullet("Bước 3: Bấm “Xóa” để thực hiện hoặc “Hủy” để bỏ qua.")
b.para("Nếu loại tài khoản đang được sử dụng thì nút Xóa bị làm mờ, rê chuột hiện chú thích "
       "“Loại tài khoản đang được sử dụng, không thể xóa”. Trạng thái Khóa không cản việc xóa: "
       "loại tài khoản đang Khóa mà chưa ai dùng vẫn xóa được.")
b.para("Sau khi xóa, dòng biến mất và tổng số dưới bảng giảm đi một; nếu đó là dòng cuối cùng của "
       "trang thì màn hình tự lùi về trang trước.")

# ============================================================================
b.h1("PHẦN 6: XUẤT EXCEL VÀ IMPORT EXCEL")

b.h2("1. Xuất Excel")
b.para("Mọi người vào được màn hình đều dùng được. Đặt bộ lọc mong muốn rồi bấm “Xuất Excel”, chờ "
       "thông báo thành công và mở file tải về.")
b.para("File xuất ra lấy đúng tập dữ liệu đang lọc chứ không phải toàn bộ danh mục, và lấy đủ mọi "
       "dòng khớp bộ lọc chứ không chỉ trang đang xem.")

b.h2("2. Import Excel")
b.para("Yêu cầu quyền “Quản lý danh mục loại tài khoản”. Bấm nút “Import Excel” ở đầu bảng.")
b.image("ltk-05-import.png", "Cửa sổ Import loại tài khoản")
b.table([
    ["Nút trong cửa sổ", "Tác dụng"],
    ["Chọn file Excel", "Chọn file dữ liệu cần nhập từ máy."],
    ["Tải file mẫu", "Tải về file mẫu có sẵn đúng các cột cần thiết. Nên dùng file mẫu này để "
                     "tránh sai tên cột."],
    ["Load lên bảng", "Đọc file đã chọn và hiển thị nội dung lên bảng xem trước."],
    ["Validate", "Kiểm tra từng dòng. Dòng hợp lệ sẽ bị khóa lại không sửa được nữa; dòng lỗi "
                 "được đánh dấu kèm lý do và vẫn cho sửa tại chỗ."],
    ["Import", "Ghi các dòng hợp lệ vào danh mục."],
    ["Chỉ dòng lỗi", "Lọc bảng xem trước để chỉ hiển thị các dòng đang lỗi, tiện sửa nhanh."],
])

b.h2("3. Các cột trong file Excel")
b.table([
    ["Cột", "Bắt buộc", "Ghi chú"],
    ["Mã loại tài khoản", "Có", "Không được trùng với mã đã có trong danh mục, cũng không được "
                               "trùng nhau trong cùng một file."],
    ["Tên loại tài khoản", "Có", "Không được trùng với tên đã có trong danh mục."],
    ["Ghi chú", "Không", "Tối đa 255 ký tự."],
    ["Trạng thái", "Không", "Bỏ trống thì hiểu là Hoạt động."],
])
b.para("Chỉ những dòng hợp lệ mới được ghi vào danh mục; các dòng lỗi bị bỏ qua và người dùng có "
       "thể sửa rồi kiểm tra lại. Chọn file sai định dạng thì hệ thống báo file không hợp lệ.")

# ============================================================================
b.h1("PHẦN CHI TIẾT: THAO TÁC TỪNG BƯỚC")

b.h2("A. Khai báo một loại tài khoản mới")
b.bullet("Bước A1: Vào phân hệ Tài chính → Danh mục → Danh mục loại tài khoản.")
b.bullet("Bước A2: Bấm “Tạo mới”.")
b.bullet("Bước A3: Nhập Mã loại tài khoản (ví dụ TKTS) và Tên loại tài khoản "
         "(ví dụ Tài khoản tài sản).")
b.bullet("Bước A4: Nhập Ghi chú nếu cần, để Trạng thái là Hoạt động.")
b.bullet("Bước A5: Bấm “Lưu”, kiểm tra dòng mới đã xuất hiện trong danh sách.")
b.bullet("Bước A6: Sang màn Danh mục tài khoản, mở form thêm tài khoản và kiểm tra loại vừa tạo "
         "đã có trong danh sách chọn.")

b.h2("B. Sửa tên một loại tài khoản và kiểm tra lịch sử")
b.bullet("Bước B1: Tìm loại tài khoản bằng ô tìm nhanh.")
b.bullet("Bước B2: Bấm nút Sửa, đổi Tên loại tài khoản, bấm “Lưu”.")
b.bullet("Bước B3: Bấm nút Lịch sử chỉnh sửa của dòng đó.")
b.bullet("Bước B4: Kiểm tra dòng lịch sử mới nhất nằm trên cùng, ghi đúng tên cũ và tên mới.")

b.h2("C. Ngừng sử dụng một loại tài khoản")
b.bullet("Bước C1: Thử bấm nút Xóa. Nếu nút bị mờ, rê chuột đọc chú thích để biết loại tài khoản "
         "đang được sử dụng.")
b.bullet("Bước C2: Sang màn Danh mục tài khoản, lọc theo loại tài khoản đó để biết những tài "
         "khoản nào đang dùng.")
b.bullet("Bước C3: Chuyển các tài khoản đó sang loại khác.")
b.bullet("Bước C4: Quay lại màn này, nút Khóa và nút Xóa đã bấm được. Chọn Khóa nếu muốn giữ lại "
         "bản ghi, chọn Xóa nếu muốn bỏ hẳn.")

b.h2("D. Nhập một danh sách loại tài khoản từ Excel")
b.bullet("Bước D1: Bấm “Import Excel”, bấm “Tải file mẫu” và điền dữ liệu vào file mẫu.")
b.bullet("Bước D2: Bấm “Chọn file Excel” rồi chọn file vừa điền.")
b.bullet("Bước D3: Bấm “Load lên bảng” để xem trước nội dung.")
b.bullet("Bước D4: Bấm “Validate”. Nếu có dòng lỗi, bấm “Chỉ dòng lỗi” để lọc ra và sửa tại chỗ, "
         "rồi kiểm tra lại.")
b.bullet("Bước D5: Bấm “Import”, sau đó đóng cửa sổ và đối chiếu danh sách.")

b.finish()
