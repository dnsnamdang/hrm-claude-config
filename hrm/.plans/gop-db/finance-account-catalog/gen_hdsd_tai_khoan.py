# -*- coding: utf-8 -*-
"""Sinh HDSD cho man Danh muc tai khoan (phan he Tai chinh).

Chay:  python gen_hdsd_tai_khoan.py
"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "hdsd-documenter", "assets"))

from hdsd_engine import HdsdBuilder  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

b = HdsdBuilder(
    output=os.path.join(HERE, "HDSD_Danh muc tai khoan.docx"),
    shots_dir=os.path.join(HERE, "hdsd_shots"),
    cover_title="(Màn hình: Danh mục tài khoản)",
    doc_title="HDSD - Danh mục tài khoản",
)

# ============================================================================
b.h1("TỔNG QUAN")

b.h2("1. Mục tiêu")
b.para("Màn hình “Danh mục tài khoản” dùng để khai báo và quản lý hệ thống tài khoản kế toán ba "
       "bậc của toàn hệ thống. Đây là danh mục nền của phân hệ Tài chính: mọi nghiệp vụ hạch "
       "toán, sổ sách, báo cáo tài chính và theo dõi công nợ đều lấy tài khoản từ đây.")
b.para("Lưu ý quan trọng: danh mục này dùng CHUNG dữ liệu với màn tương ứng bên phần mềm cũ. "
       "Sửa ở cổng nào thì cổng còn lại cũng thấy ngay, không cần đồng bộ thủ công.")

b.h2("2. Đường dẫn truy cập")
b.para("Trên menu trái của phân hệ Tài chính, vào nhóm “Danh mục” rồi chọn “Danh mục tài khoản” "
       "(đường dẫn: /finance/accounts).")
b.para("Mục menu chỉ hiển thị khi tài khoản có ít nhất một trong hai quyền “Quản lý danh mục tài "
       "khoản” hoặc “Xem danh mục tài khoản”. Không có quyền nào thì mục menu bị ẩn; gõ thẳng "
       "đường dẫn sẽ bị chuyển sang trang báo không tìm thấy.")

b.h2("3. Vai trò tham gia")
b.table([
    ["Vai trò", "Thao tác chính"],
    ["Kế toán lập hệ thống tài khoản",
     "Thêm mới, Sửa tài khoản; nhập danh sách từ Excel; in và xuất danh sách."],
    ["Người tạo tài khoản",
     "Riêng người ĐÃ TẠO tài khoản mới được Khóa, Mở khóa và Xóa chính tài khoản đó."],
    ["Người dùng chỉ xem",
     "Xem danh sách, xem lịch sử chỉnh sửa, tìm kiếm, lọc, in danh sách và xuất Excel."],
    ["Bộ phận hạch toán",
     "Là bên sử dụng danh mục này khi lập chứng từ kế toán."],
])

b.h2("4. Cấu trúc cây tài khoản ba bậc")
b.para("Tài khoản được tổ chức thành cây ba bậc, gắn kết với nhau theo SỐ tài khoản chứ không "
       "theo tên:")
b.table([
    ["Bậc", "Số tài khoản", "Tài khoản mẹ", "Ví dụ"],
    ["Bậc 1", "3 chữ số", "Không có — nằm ở gốc cây", "131"],
    ["Bậc 2", "4 chữ số", "Bắt buộc, phải là một tài khoản bậc 1", "1311 (mẹ là 131)"],
    ["Bậc 3", "từ 5 chữ số", "Bắt buộc, phải là một tài khoản bậc 2", "13111 (mẹ là 1311)"],
])
b.para("Ba quy tắc bắt buộc của cây, hệ thống luôn kiểm tra khi lưu:")
b.bullet("Tài khoản mẹ phải đúng bậc liền trên. Tài khoản bậc 3 không được chọn mẹ là bậc 1.")
b.bullet("Số tài khoản con phải BẮT ĐẦU BẰNG số tài khoản mẹ. Mẹ là 131 thì con phải là 1311, "
         "1312… Nếu không, dòng đó sẽ nằm sai chỗ trên cây và không cách nào kéo về đúng vị trí.")
b.bullet("Tài khoản ĐANG CÓ tài khoản con thì không được đổi Bậc và không được đổi Số tài khoản. "
         "Muốn đổi phải chuyển hoặc xóa các tài khoản con trước.")

b.h2("5. Các trạng thái")
b.table([
    ["Trạng thái", "Ý nghĩa"],
    ["Hoạt động", "Tài khoản đang dùng được; chọn được khi hạch toán chứng từ mới; sửa được."],
    ["Khóa", "Ngừng sử dụng. Không còn chọn được khi hạch toán chứng từ mới và KHÔNG sửa được — "
             "muốn sửa phải Mở khóa trước. Các chứng từ đã hạch toán vẫn hiển thị đúng tài khoản này."],
])

b.h2("6. Luồng sử dụng")
b.bullet("Bước 1 — Khai báo các loại tài khoản ở màn “Danh mục loại tài khoản”.")
b.bullet("Bước 2 — Ở màn này, khai tài khoản bậc 1 trước, sau đó mới khai bậc 2 và bậc 3 dưới nó.")
b.bullet("Bước 3 — Bộ phận hạch toán chọn tài khoản khi lập chứng từ.")
b.bullet("Bước 4 (khi cần điều chỉnh) — Sửa tên hoặc loại tài khoản; mọi thay đổi được ghi vào "
         "lịch sử chỉnh sửa.")
b.bullet("Bước 5 (khi ngừng dùng) — Chuyển tài khoản sang trạng thái Khóa. Chỉ xóa hẳn khi tài "
         "khoản chưa có con và chưa từng được hạch toán.")

# ============================================================================
b.h1("PHẦN 1: DANH SÁCH & TÌM KIẾM")

b.image("tk-01-danh-sach.png", "Màn hình danh sách Danh mục tài khoản")

b.h2("1. Bố cục màn hình")
b.bullet("Khối trên — “Bộ lọc danh mục tài khoản”: ô tìm nhanh, nút Tìm kiếm, nút Làm mới, nút "
         "Tìm kiếm nâng cao ở góc phải.")
b.bullet("Khối dưới — bảng “Danh mục tài khoản” cùng bốn nút Tạo mới, In danh sách, Xuất Excel, "
         "Import Excel ở đầu bảng và phần phân trang ở cuối bảng.")

b.h2("2. Các cột của bảng")
b.table([
    ["Cột", "Nội dung"],
    ["STT", "Số thứ tự tính theo trang đang xem."],
    ["Cấp 1 / Cấp 2 / Cấp 3", "Ba cột này KHÔNG phải ba giá trị khác nhau. Số tài khoản chỉ xuất "
                              "hiện MỘT lần trên mỗi dòng, được đặt vào đúng cột theo bậc của nó, "
                              "hai cột còn lại để trống. Nhờ vậy nhìn ngang là thấy cây thụt lề."],
    ["Tên tài khoản", "Tên đầy đủ; ngay dưới có dòng phụ “Tài khoản mẹ: …”. Tài khoản bậc 1 hiện "
                      "dấu gạch ngang ở dòng phụ vì không có mẹ."],
    ["Loại tài khoản", "Tên loại tài khoản bằng tiếng Việt, lấy từ Danh mục loại tài khoản. "
                       "Chưa gán loại thì để trống."],
    ["Theo dõi công nợ", "Hiện dấu đánh dấu nếu tài khoản có bật theo dõi công nợ; không bật thì "
                         "hiện dấu gạch ngang."],
    ["Ngày tạo", "Ngày tạo bản ghi kèm tên người tạo."],
    ["Cập nhật", "Ngày thay đổi gần nhất kèm tên người cập nhật."],
    ["Trạng thái", "Nhãn Hoạt động hoặc Khóa. Nút Khóa / Mở khóa nằm NGAY TRONG cột này."],
    ["Hành động", "Ba nút: Sửa, Lịch sử chỉnh sửa, Xóa."],
])
b.para("Màn hình này KHÔNG có nút Xem riêng như các danh mục khác. Muốn xem chi tiết một tài "
       "khoản thì mở trang Sửa rồi bấm Quay lại.")

b.h2("3. Tìm nhanh")
b.para("Ô tìm nhanh có dòng gợi ý “Tìm theo số hoặc tên tài khoản...”, quét cả Số tài khoản và "
       "Tên tài khoản. Gõ một phần chuỗi là đủ — kể cả phần nằm ở GIỮA tên, ví dụ gõ “khách hàng” "
       "vẫn ra “Phải thu của khách hàng ngắn hạn”. Không phân biệt chữ hoa chữ thường. Phải bấm "
       "nút Tìm kiếm hoặc nhấn Enter thì danh sách mới lọc.")

b.h2("4. Tìm kiếm nâng cao")
b.table([
    ["Tiêu chí lọc", "Cách dùng"],
    ["Bậc tài khoản", "Chọn 1, 2 hoặc 3 để chỉ xem tài khoản của một bậc."],
    ["Loại tài khoản", "Chọn một loại từ Danh mục loại tài khoản."],
    ["Theo dõi công nợ", "Chọn Có hoặc Không."],
    ["Trạng thái", "Chọn Hoạt động hoặc Khóa."],
    ["Người tạo", "Chọn một người; danh sách chỉ liệt kê những người thực sự đã tạo bản ghi."],
    ["Người cập nhật", "Chọn một người; kết quả là các tài khoản do người đó sửa gần nhất."],
])
b.para("Các điều kiện được kết hợp theo kiểu VÀ: kết quả phải thỏa đồng thời mọi điều kiện đã "
       "chọn. Nút Làm mới xóa toàn bộ điều kiện và nạp lại danh sách ngay. Hệ thống ghi nhớ bộ "
       "lọc trong 10 phút.")

b.h2("5. Thứ tự hiển thị và phân trang")
b.bullet("Khi chưa lọc và chưa sắp xếp, danh sách xếp theo cây: tài khoản con nằm ngay dưới tài "
         "khoản mẹ của nó.")
b.bullet("Cuối bảng có dòng “Hiển thị a – b / N”: N là tổng số tài khoản khớp bộ lọc hiện tại.")
b.bullet("Ô “Số dòng/trang” cho chọn 5, 10, 20 hoặc 50 dòng mỗi trang.")

# ============================================================================
b.h1("PHẦN 2: PHÂN QUYỀN & HƯỚNG DẪN THEO QUYỀN")

b.h2("1. Bảng quyền của màn hình")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / khu vực tương ứng"],
    ["Xem danh mục tài khoản",
     "Vào màn hình, xem danh sách, tìm kiếm và lọc, xem lịch sử chỉnh sửa, in danh sách, xuất Excel.",
     "Nút Lịch sử chỉnh sửa trên mỗi dòng; nút In danh sách và Xuất Excel."],
    ["Quản lý danh mục tài khoản",
     "Toàn bộ quyền trên, cộng thêm: thêm mới, sửa, khóa, mở khóa, xóa và nhập danh sách từ Excel.",
     "Nút Tạo mới và Import Excel; nút Sửa, nút Xóa trên mỗi dòng; nút Khóa / Mở khóa trong cột "
     "Trạng thái."],
])
b.para("Danh mục này KHÔNG phân quyền theo công ty, phòng ban hay bộ phận: mọi người vào được màn "
       "đều nhìn thấy cùng một danh sách.")

b.h2("2. Ràng buộc riêng: chỉ người tạo mới khóa, mở khóa và xóa được")
b.para("Ngoài quyền, màn hình này còn một ràng buộc riêng không có ở các danh mục khác: các thao "
       "tác Khóa, Mở khóa và Xóa chỉ dành cho CHÍNH NGƯỜI ĐÃ TẠO tài khoản đó. Người khác dù có "
       "quyền “Quản lý danh mục tài khoản” cũng sẽ thấy ba nút này bị làm mờ.")
b.para("Riêng thao tác Sửa thì không bị ràng buộc này: người có quyền quản lý sửa được tài khoản "
       "do người khác tạo.")

b.h2("3. Người dùng có quyền “Xem danh mục tài khoản”")
b.para("Vào được màn hình, thấy đầy đủ danh sách nhưng KHÔNG có nút Tạo mới và Import Excel; trên "
       "mỗi dòng chỉ còn nút Lịch sử chỉnh sửa; cột Trạng thái chỉ hiện nhãn mà không có nút "
       "Khóa / Mở khóa. Hai nút In danh sách và Xuất Excel vẫn dùng được bình thường.")

b.h2("4. Người dùng có quyền “Quản lý danh mục tài khoản”")
b.para("Thấy đầy đủ bốn nút Tạo mới, In danh sách, Xuất Excel, Import Excel; trên mỗi dòng có Sửa, "
       "Lịch sử chỉnh sửa, Xóa. Nút Khóa / Mở khóa và nút Xóa chỉ bấm được trên các tài khoản do "
       "chính mình tạo.")
b.para("Nếu không có quyền này, các nút trên sẽ không hiển thị; trường hợp truy cập trực tiếp bằng "
       "đường dẫn hoặc bằng công cụ ngoài giao diện, hệ thống từ chối và báo không có quyền.")

# ============================================================================
b.h1("PHẦN 3: THÊM MỚI TÀI KHOẢN")
b.para("Yêu cầu quyền “Quản lý danh mục tài khoản”.")
b.para("Bấm nút “Tạo mới” ở đầu bảng. Khác với các danh mục khác, hệ thống mở một TRANG RIÊNG "
       "chứ không phải cửa sổ nhỏ.")
b.image("tk-02-them.png", "Trang Thêm tài khoản")

b.h2("1. Bố cục trang")
b.para("Trang chia làm hai khối:")
b.bullet("“Vị trí trong hệ thống tài khoản” — Số tài khoản, Bậc tài khoản, Tài khoản mẹ.")
b.bullet("“Thông tin tài khoản” — Tên tài khoản, Loại tài khoản, Trạng thái và ô đánh dấu "
         "“Tài khoản theo dõi công nợ”.")
b.para("Góc trên bên phải có ba nút: Lưu, Lưu & Thêm tiếp, Quay lại.")

b.h2("2. Các trường nhập")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị mặc định khi mở trang", "Ghi chú"],
    ["Số tài khoản", "Ô số", "Có", "Để trống", "Chỉ nhập chữ số, từ 3 đến 15 chữ số. Phải duy "
                                              "nhất. Dưới ô có dòng nhắc: 3 chữ số là cấp 1, "
                                              "4 số cấp 2, từ 5 số cấp 3."],
    ["Bậc tài khoản", "Danh sách chọn", "Có", "Chưa chọn", "Chọn 1, 2 hoặc 3."],
    ["Tài khoản mẹ", "Danh sách chọn", "Chỉ bắt buộc với bậc 2 và bậc 3", "Chưa chọn — ô bị khóa "
                                                                        "cho tới khi chọn Bậc",
     "Danh sách chỉ liệt kê tài khoản đúng bậc liền trên bậc đang chọn."],
    ["Tên tài khoản", "Ô chữ", "Có", "Để trống", "Được phép trùng với tài khoản khác. Tối đa 255 ký tự."],
    ["Loại tài khoản", "Danh sách chọn", "Có", "Chưa chọn", "Lấy từ Danh mục loại tài khoản; chỉ "
                                                           "hiện các loại đang Hoạt động."],
    ["Trạng thái", "Danh sách chọn", "Không", "Hoạt động", "Chọn Hoạt động hoặc Khóa."],
    ["Tài khoản theo dõi công nợ", "Ô đánh dấu", "Không", "Không đánh dấu", "Bật khi tài khoản "
                                                                           "dùng để theo dõi công "
                                                                           "nợ phải thu / phải trả "
                                                                           "theo từng khách hàng, "
                                                                           "nhà cung cấp."],
])
b.para("Các trường bắt buộc có dấu sao đỏ bên cạnh nhãn. Với tài khoản bậc 1, ô Tài khoản mẹ "
       "không có dấu sao và dưới ô có dòng nhắc “Tài khoản cấp 1 nằm ở gốc cây nên không có tài "
       "khoản mẹ”.")

b.h2("3. Các nút")
b.table([
    ["Nút", "Tác dụng"],
    ["Lưu", "Lưu tài khoản rồi quay về danh sách."],
    ["Lưu & Thêm tiếp", "Lưu tài khoản nhưng ở lại trang và xóa trắng các ô để nhập bản ghi tiếp "
                        "theo. Dùng khi cần khai nhiều tài khoản liên tiếp."],
    ["Quay lại", "Về danh sách. Nếu đang nhập dở, hệ thống cảnh báo dữ liệu chưa được lưu và hỏi "
                 "xác nhận."],
])

b.h2("4. Thông báo lỗi thường gặp")
b.table([
    ["Tình huống", "Hệ thống báo"],
    ["Bỏ trống ô bắt buộc", "“Bắt buộc phải nhập” (với ô gõ chữ) hoặc “Bắt buộc phải chọn” "
                            "(với ô chọn), hiện chữ đỏ ngay dưới ô."],
    ["Số tài khoản có chữ cái hoặc dấu chấm", "“Số tài khoản chỉ được nhập chữ số, từ 3 đến 15 "
                                              "chữ số”."],
    ["Số tài khoản ngắn hơn 3 hoặc dài hơn 15 chữ số", "Cùng thông báo trên."],
    ["Số tài khoản đã có trong danh mục", "“Số tài khoản đã tồn tại”."],
    ["Bậc 2 hoặc 3 mà bỏ trống Tài khoản mẹ", "“Bắt buộc phải chọn tài khoản mẹ với bậc 2 và 3”."],
    ["Tài khoản mẹ sai bậc", "Thông báo nêu rõ tài khoản mẹ phải là bậc nào và mẹ đang là bậc mấy."],
    ["Số tài khoản con không bắt đầu bằng số mẹ", "Thông báo nêu rõ quy tắc và gợi ý dạng đúng, "
                                                 "ví dụ mẹ là 131 thì con phải là 1311, 1312…"],
])

# ============================================================================
b.h1("PHẦN 4: SỬA VÀ LỊCH SỬ CHỈNH SỬA")

b.h2("1. Sửa tài khoản")
b.para("Yêu cầu quyền “Quản lý danh mục tài khoản”. Bấm nút Sửa (hình bút chì) trên dòng cần sửa; "
       "hệ thống mở trang sửa với bố cục và các trường giống hệt trang Thêm mới, dữ liệu đã điền sẵn.")
b.bullet("Nếu tài khoản đang ở trạng thái Khóa thì nút Sửa bị làm mờ; rê chuột vào hiện chú thích "
         "“Tài khoản đã khóa → không cho sửa”. Muốn sửa phải Mở khóa trước.")
b.bullet("Nếu tài khoản ĐANG CÓ tài khoản con thì không đổi được Bậc và Số tài khoản. Hệ thống "
         "chặn kèm thông báo nêu rõ tài khoản đang có bao nhiêu con và gợi ý chuyển hoặc xóa các "
         "con trước. Tên, Loại tài khoản, Trạng thái và ô theo dõi công nợ vẫn sửa được bình thường.")
b.bullet("Giữ nguyên số tài khoản của chính bản ghi đang sửa là hợp lệ, hệ thống không báo trùng.")
b.bullet("Bấm Quay lại khi đang sửa dở, hệ thống cảnh báo dữ liệu chưa được lưu và hỏi xác nhận.")

b.h2("2. Xem chi tiết")
b.para("Màn hình này không có nút Xem riêng. Muốn xem chi tiết một tài khoản thì bấm nút Sửa để "
       "mở trang, đọc thông tin rồi bấm Quay lại. Nếu không đổi gì thì trang đóng ngay, không hỏi lại.")

b.h2("3. Lịch sử chỉnh sửa")
b.para("Bấm nút Lịch sử chỉnh sửa (hình đồng hồ quay ngược) trên dòng cần xem. Cửa sổ “Lịch sử "
       "chỉnh sửa tài khoản” liệt kê các lần thay đổi, mới nhất nằm trên cùng, mỗi dòng ghi thời "
       "điểm, người thực hiện và trường nào đổi từ giá trị cũ sang giá trị mới.")
b.para("Cửa sổ có bốn ô lọc: Trường thay đổi, Người thực hiện, Từ ngày và Đến ngày. Giá trị trạng "
       "thái và loại tài khoản hiển thị bằng nhãn tiếng Việt chứ không phải con số. Người chỉ có "
       "quyền “Xem danh mục tài khoản” vẫn mở được cửa sổ này.")

# ============================================================================
b.h1("PHẦN 5: KHÓA, MỞ KHÓA VÀ XÓA")
b.para("Cả ba thao tác đều yêu cầu quyền “Quản lý danh mục tài khoản” VÀ người thực hiện phải là "
       "người đã tạo tài khoản đó.")

b.h2("1. Khóa và Mở khóa")
b.bullet("Bước 1: Nhìn sang cột Trạng thái của dòng cần thao tác.")
b.bullet("Bước 2: Bấm nút hình ổ khóa nằm cạnh nhãn trạng thái.")
b.bullet("Bước 3: Xác nhận trong hộp “Xác nhận khóa” (hoặc “Xác nhận mở khóa”), hộp có nêu tên "
         "tài khoản để đối chiếu.")
b.para("Sau khi khóa: dòng đổi nhãn sang Khóa, nút Sửa của dòng đó chuyển sang mờ, và tài khoản "
       "không còn được chọn khi hạch toán chứng từ mới. Các chứng từ đã hạch toán trước đó vẫn "
       "hiển thị đúng tài khoản này và lưu lại không bị mất dữ liệu.")
b.para("Khóa một tài khoản mẹ KHÔNG tự khóa các tài khoản con của nó; muốn khóa cả nhánh phải "
       "khóa từng tài khoản.")

b.h2("2. Xóa")
b.para("Một tài khoản chỉ xóa được khi thỏa ĐỦ ba điều kiện:")
b.bullet("Người thực hiện chính là người đã tạo tài khoản đó.")
b.bullet("Tài khoản KHÔNG có tài khoản con nào.")
b.bullet("Tài khoản CHƯA từng được hạch toán ở chứng từ nào.")
b.para("Thiếu bất kỳ điều kiện nào thì nút Xóa bị làm mờ; rê chuột vào nút sẽ hiện chú thích nêu "
       "rõ lý do. Khi đủ điều kiện, bấm nút Xóa, đọc hộp “Xác nhận xóa” rồi bấm “Xóa”.")
b.para("Muốn xóa cả một nhánh thì phải xóa từ dưới lên: xóa hết tài khoản con trước, khi đó nút "
       "Xóa của tài khoản mẹ mới chuyển từ mờ sang bấm được.")

# ============================================================================
b.h1("PHẦN 6: IN DANH SÁCH, XUẤT EXCEL VÀ IMPORT EXCEL")

b.h2("1. In danh sách")
b.para("Mọi người vào được màn hình đều dùng được. Đặt bộ lọc mong muốn rồi bấm “In danh sách”; "
       "hệ thống mở bản in trong một thẻ mới của trình duyệt.")
b.image("tk-03-in-danh-sach.png", "Bản in danh mục tài khoản")
b.para("Bản in lấy đúng tập dữ liệu đang lọc chứ không phải toàn bộ danh mục, và giữ nguyên cấu "
       "trúc ba cột Cấp 1 / Cấp 2 / Cấp 3 như trên màn hình. Nên xem trước trong hộp thoại in của "
       "trình duyệt để chắc chắn nội dung nằm gọn trong khổ giấy.")

b.h2("2. Xuất Excel")
b.para("Đặt bộ lọc rồi bấm “Xuất Excel”, chờ thông báo thành công và mở file tải về. File lấy đúng "
       "tập dữ liệu đang lọc và lấy đủ mọi dòng khớp bộ lọc chứ không chỉ trang đang xem.")

b.h2("3. Import Excel")
b.para("Yêu cầu quyền “Quản lý danh mục tài khoản”. Bấm nút “Import Excel” ở đầu bảng; cửa sổ "
       "nhập liệu có các nút Chọn file Excel, Tải file mẫu, Load lên bảng, Validate, Import và "
       "Chỉ dòng lỗi.")
b.table([
    ["Nút trong cửa sổ", "Tác dụng"],
    ["Chọn file Excel", "Chọn file dữ liệu cần nhập từ máy."],
    ["Tải file mẫu", "Tải về file mẫu có sẵn đúng các cột cần thiết."],
    ["Load lên bảng", "Đọc file đã chọn và hiển thị nội dung lên bảng xem trước."],
    ["Validate", "Kiểm tra từng dòng. Dòng hợp lệ bị khóa lại không sửa được nữa; dòng lỗi được "
                 "đánh dấu kèm lý do và vẫn cho sửa tại chỗ."],
    ["Import", "Ghi các dòng hợp lệ vào danh mục."],
    ["Chỉ dòng lỗi", "Lọc bảng xem trước để chỉ hiển thị các dòng đang lỗi."],
])
b.para("Dữ liệu nhập vào cũng phải tuân thủ đủ ba quy tắc của cây tài khoản nêu ở phần Tổng quan. "
       "Dòng sai quy tắc hoặc trùng số tài khoản sẽ bị đánh dấu lỗi và không được ghi vào. "
       "Nên nhập theo thứ tự bậc 1 trước, rồi bậc 2, rồi bậc 3.")

# ============================================================================
b.h1("PHẦN CHI TIẾT: THAO TÁC TỪNG BƯỚC")

b.h2("A. Khai một nhánh tài khoản mới đủ ba bậc")
b.bullet("Bước A1: Vào phân hệ Tài chính → Danh mục → Danh mục tài khoản, bấm “Tạo mới”.")
b.bullet("Bước A2: Nhập Số tài khoản 3 chữ số (ví dụ 138), chọn Bậc = 1, bỏ trống Tài khoản mẹ.")
b.bullet("Bước A3: Nhập Tên tài khoản, chọn Loại tài khoản, bấm “Lưu”.")
b.bullet("Bước A4: Bấm “Tạo mới” lần nữa, chọn Bậc = 2, chọn Tài khoản mẹ là 138.")
b.bullet("Bước A5: Nhập Số tài khoản 1381 (phải bắt đầu bằng 138), nhập tên, chọn loại, bấm “Lưu”.")
b.bullet("Bước A6: Làm tương tự cho bậc 3 với số 13811, mẹ là 1381.")
b.bullet("Bước A7: Về danh sách, kiểm tra ba dòng nằm liền nhau và số nằm đúng cột Cấp 1, Cấp 2, "
         "Cấp 3.")

b.h2("B. Bật theo dõi công nợ cho một tài khoản")
b.bullet("Bước B1: Tìm tài khoản bằng ô tìm nhanh.")
b.bullet("Bước B2: Bấm nút Sửa.")
b.bullet("Bước B3: Bấm vào ô đánh dấu “Tài khoản theo dõi công nợ” trong khối Thông tin tài khoản.")
b.bullet("Bước B4: Bấm “Lưu”, kiểm tra cột Theo dõi công nợ của dòng đó đã có dấu đánh dấu.")

b.h2("C. Sửa lại một tài khoản đang có tài khoản con")
b.bullet("Bước C1: Bấm nút Sửa trên tài khoản mẹ.")
b.bullet("Bước C2: Thử đổi Số tài khoản hoặc Bậc — hệ thống sẽ chặn và nêu rõ số tài khoản con "
         "đang có.")
b.bullet("Bước C3: Giữ nguyên Số và Bậc, chỉ sửa Tên hoặc Loại tài khoản, bấm “Lưu”.")
b.bullet("Bước C4: Bấm nút Lịch sử chỉnh sửa để kiểm tra thay đổi đã được ghi nhận.")

b.h2("D. Ngừng sử dụng một tài khoản")
b.bullet("Bước D1: Thử bấm nút Xóa. Nếu nút bị mờ, rê chuột đọc chú thích để biết lý do "
         "(không phải người tạo / còn tài khoản con / đã được hạch toán).")
b.bullet("Bước D2: Nếu không xóa được, bấm nút hình ổ khóa trong cột Trạng thái để chuyển sang Khóa.")
b.bullet("Bước D3: Xác nhận trong hộp “Xác nhận khóa”.")
b.bullet("Bước D4: Kiểm tra ở màn hạch toán chứng từ — tài khoản đó không còn trong danh sách chọn.")
b.bullet("Bước D5: Mở một chứng từ cũ đã hạch toán vào tài khoản đó để chắc chắn dữ liệu cũ "
         "không bị mất.")

b.finish()
