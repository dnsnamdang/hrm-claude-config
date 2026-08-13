# -*- coding: utf-8 -*-
"""Sinh 2 file HDSD cho 2 danh muc bao duong (phan he CSKH):
  - Cap dich vu bao duong
  - Danh muc ghi chu kiem tra bao duong

Chay:  python gen_hdsd.py
"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "hdsd-documenter", "assets"))

from hdsd_engine import HdsdBuilder  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "hdsd_shots")

# ############################################################################
# MAN 1 — CAP DICH VU BAO DUONG
# ############################################################################
b = HdsdBuilder(
    output=os.path.join(HERE, "HDSD_Cap dich vu bao duong.docx"),
    shots_dir=SHOTS,
    cover_title="(Màn hình: Cấp dịch vụ bảo dưỡng)",
    doc_title="HDSD - Cấp dịch vụ bảo dưỡng",
)

b.h1("TỔNG QUAN")

b.h2("1. Mục tiêu")
b.para("Màn hình “Cấp dịch vụ bảo dưỡng” dùng để khai báo danh sách các cấp bảo dưỡng như "
       "“Cấp 1 (6T)”, “Cấp 2 (12T)”, “Cấp 2 (24T/6000H)”… Cấp dịch vụ là mức phân loại công việc "
       "bảo dưỡng theo mốc thời gian hoặc số giờ vận hành của thiết bị.")
b.para("Danh mục này được dùng lại ở năm nơi: gói bảo dưỡng, cấp bảo dưỡng của gói dịch vụ, "
       "báo giá dịch vụ, hợp đồng dịch vụ, phiếu phân công công việc và phiếu nhập kết quả. "
       "Vì vậy một cấp đã được dùng ở bất kỳ chứng từ nào sẽ không xóa được.")
b.para("Lưu ý quan trọng: danh mục này dùng CHUNG dữ liệu với màn tương ứng bên phần mềm cũ. "
       "Sửa ở cổng nào thì cổng còn lại cũng thấy ngay.")

b.h2("2. Đường dẫn truy cập")
b.para("Trên menu trái của phân hệ Chăm sóc khách hàng, vào nhóm “Danh mục - Dịch vụ” rồi chọn "
       "“Cấp dịch vụ bảo dưỡng” (đường dẫn: /customer-care/levels).")
b.para("Mục menu chỉ hiển thị khi tài khoản có ít nhất một trong hai quyền “Quản lý cấp dịch vụ "
       "bảo dưỡng” hoặc “Xem cấp dịch vụ bảo dưỡng”. Không có quyền nào thì mục menu bị ẩn; gõ "
       "thẳng đường dẫn sẽ bị chuyển sang trang báo không tìm thấy.")

b.h2("3. Vai trò tham gia")
b.table([
    ["Vai trò", "Thao tác chính"],
    ["Người quản lý danh mục dịch vụ", "Thêm mới, Sửa, Xóa cấp dịch vụ; xuất Excel."],
    ["Người dùng chỉ xem", "Xem danh sách, mở xem chi tiết, tìm kiếm và xuất Excel."],
    ["Bộ phận kỹ thuật / dịch vụ", "Là bên sử dụng danh mục này khi lập gói bảo dưỡng, báo giá "
                                   "dịch vụ, hợp đồng dịch vụ, phân công công việc và nhập kết quả."],
])

b.h2("4. Đặc điểm riêng của màn hình")
b.para("Khác với phần lớn danh mục khác trong hệ thống, màn hình này KHÔNG có trạng thái "
       "Hoạt động / Khóa. Chỉ có ba thao tác: Thêm mới, Sửa và Xóa. Muốn ngừng dùng một cấp dịch "
       "vụ thì chỉ có cách xóa, và chỉ xóa được khi cấp đó chưa xuất hiện ở chứng từ nào.")

b.h2("5. Điều kiện chặn xóa")
b.para("Một cấp dịch vụ không xóa được nếu đang xuất hiện ở bất kỳ nơi nào trong năm nhóm sau:")
b.table([
    ["Nơi đang sử dụng", "Nghĩa là"],
    ["Gói bảo dưỡng", "Cấp dịch vụ đã được đưa vào một gói bảo dưỡng."],
    ["Cấp bảo dưỡng của gói dịch vụ", "Cấp dịch vụ đã được cấu hình chi tiết trong gói."],
    ["Báo giá dịch vụ", "Đã có báo giá dịch vụ dùng cấp này."],
    ["Hợp đồng dịch vụ", "Đã có hợp đồng dịch vụ dùng cấp này."],
    ["Phiếu phân công công việc", "Đã có phiếu phân công dùng cấp này."],
])
b.para("Ngoài ra còn tính cả phiếu nhập kết quả. Khi bị chặn, hệ thống hiện thông báo nêu tên tối "
       "đa ba nơi đang dùng, dù thực tế có thể nhiều hơn.")
b.para("Lưu ý cho người kiểm thử và người dùng cũ: ở phần mềm cũ, cấp dịch vụ CHỈ bị chặn khi "
       "được dùng trong gói bảo dưỡng — bốn nhóm còn lại không được kiểm, nên có thể xóa nhầm một "
       "cấp đang nằm trong hợp đồng hoặc báo giá. Bản mới đã kiểm đủ.")

b.h2("6. Luồng sử dụng")
b.bullet("Bước 1 — Khai báo các cấp dịch vụ cần dùng ở màn này.")
b.bullet("Bước 2 — Sang màn Danh mục gói bảo dưỡng, chọn cấp dịch vụ cho từng gói.")
b.bullet("Bước 3 — Bộ phận dịch vụ dùng gói bảo dưỡng để lập báo giá, hợp đồng, phân công công "
         "việc và nhập kết quả.")
b.bullet("Bước 4 (khi cần điều chỉnh) — Sửa tên cấp; các chứng từ đang dùng sẽ hiển thị tên mới.")

# ---------------------------------------------------------------------------
b.h1("PHẦN 1: DANH SÁCH & TÌM KIẾM")

b.image("lv-01-danh-sach.png", "Màn hình danh sách Cấp dịch vụ bảo dưỡng")

b.h2("1. Bố cục màn hình")
b.bullet("Khối trên — “Bộ lọc cấp dịch vụ bảo dưỡng” với dòng phụ “Tìm kiếm theo tên cấp dịch vụ "
         "bảo dưỡng”: chỉ có ô tìm nhanh, nút Tìm kiếm và nút Làm mới. Màn này không có tìm kiếm "
         "nâng cao vì chỉ có một trường dữ liệu.")
b.bullet("Khối dưới — bảng “Cấp dịch vụ bảo dưỡng” cùng hai nút Tạo mới và Xuất Excel ở đầu bảng.")

b.h2("2. Các cột của bảng")
b.table([
    ["Cột", "Nội dung"],
    ["STT", "Số thứ tự tính theo trang đang xem."],
    ["Tên cấp", "Tên cấp dịch vụ, là giá trị duy nhất trong danh mục."],
    ["Cập nhật", "Ngày giờ thay đổi gần nhất."],
    ["Hành động", "Ba nút: Xem, Sửa, Xóa."],
])
b.para("Bảng KHÔNG có cột Trạng thái và không có nút Khóa / Mở khóa.")

b.h2("3. Tìm nhanh")
b.para("Ô tìm nhanh có dòng gợi ý “Tìm theo tên cấp...”. Gõ một phần chuỗi là đủ — gõ “6T” vẫn ra "
       "“Cấp 1 (6T)”. Không phân biệt chữ hoa chữ thường. Phải bấm nút Tìm kiếm hoặc nhấn Enter "
       "thì danh sách mới lọc.")
b.para("Nút Làm mới xóa nội dung ô tìm nhanh VÀ nạp lại danh sách ngay. Hệ thống ghi nhớ điều "
       "kiện tìm kiếm trong 10 phút, nên khi thấy danh sách thiếu so với mong đợi hãy bấm Làm mới "
       "trước.")

b.h2("4. Sắp xếp và phân trang")
b.bullet("Bấm tiêu đề cột Tên cấp hoặc cột Cập nhật để sắp xếp; bấm lần nữa để đảo chiều.")
b.bullet("Cuối bảng có dòng “Hiển thị a – b / N”: N là tổng số cấp dịch vụ khớp điều kiện tìm kiếm.")
b.bullet("Ô “Số dòng/trang” cho chọn 5, 10, 20 hoặc 50 dòng mỗi trang.")

# ---------------------------------------------------------------------------
b.h1("PHẦN 2: PHÂN QUYỀN & HƯỚNG DẪN THEO QUYỀN")

b.h2("1. Bảng quyền của màn hình")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / khu vực tương ứng"],
    ["Xem cấp dịch vụ bảo dưỡng",
     "Vào màn hình, xem danh sách, tìm kiếm, mở xem chi tiết, xuất Excel.",
     "Nút Xem trên mỗi dòng; nút Xuất Excel."],
    ["Quản lý cấp dịch vụ bảo dưỡng",
     "Toàn bộ quyền trên, cộng thêm: thêm mới, sửa và xóa cấp dịch vụ.",
     "Nút Tạo mới; nút Sửa và nút Xóa trên mỗi dòng."],
])
b.para("Danh mục này KHÔNG phân quyền theo công ty, phòng ban hay bộ phận.")

b.h2("2. Người dùng có quyền “Xem cấp dịch vụ bảo dưỡng”")
b.para("Vào được màn hình và thấy đầy đủ danh sách, nhưng KHÔNG có nút Tạo mới; mỗi dòng chỉ có "
       "nút Xem. Nút Xuất Excel vẫn dùng được bình thường.")

b.h2("3. Người dùng có quyền “Quản lý cấp dịch vụ bảo dưỡng”")
b.para("Thấy đầy đủ nút Tạo mới và Xuất Excel; trên mỗi dòng có đủ Xem, Sửa, Xóa.")
b.para("Nếu không có quyền này, các nút trên sẽ không hiển thị; trường hợp truy cập trực tiếp "
       "bằng đường dẫn hoặc bằng công cụ ngoài giao diện, hệ thống từ chối và báo không có quyền.")

# ---------------------------------------------------------------------------
b.h1("PHẦN 3: THÊM MỚI, SỬA VÀ XEM")

b.h2("1. Thêm mới")
b.para("Yêu cầu quyền “Quản lý cấp dịch vụ bảo dưỡng”. Bấm nút “Tạo mới” ở đầu bảng; hệ thống mở "
       "cửa sổ “Thêm cấp dịch vụ”.")
b.image("lv-02-them.png", "Cửa sổ Thêm cấp dịch vụ")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị mặc định khi mở form", "Ghi chú"],
    ["Tên cấp", "Ô chữ", "Có", "Để trống", "Phải là duy nhất trong danh mục. Tối đa 255 ký tự. "
                                          "Gợi ý nhập trong ô: “VD: Cấp 1 (6T)”."],
])
b.para("Cửa sổ chỉ có duy nhất một ô nhập, cuối cửa sổ có ba nút:")
b.table([
    ["Nút", "Tác dụng"],
    ["Lưu", "Lưu cấp dịch vụ, đóng cửa sổ và nạp lại danh sách."],
    ["Lưu & Tiếp tục", "Lưu cấp dịch vụ nhưng GIỮ cửa sổ mở và xóa trắng ô để nhập tiếp. "
                       "Dùng khi cần khai nhiều cấp liên tiếp."],
    ["Đóng", "Đóng cửa sổ. Nếu đang nhập dở, hệ thống hỏi xác nhận trước khi đóng."],
])

b.h2("2. Thông báo lỗi thường gặp")
b.table([
    ["Tình huống", "Hệ thống báo"],
    ["Bỏ trống Tên cấp", "Ô viền đỏ, hiện chữ đỏ “Bắt buộc phải nhập” ngay dưới ô; cửa sổ không đóng."],
    ["Chỉ nhập toàn khoảng trắng", "Cũng báo “Bắt buộc phải nhập” — hệ thống cắt khoảng trắng "
                                   "đầu và cuối trước khi kiểm tra."],
    ["Tên cấp đã có trong danh mục", "“Tên cấp đã tồn tại”."],
    ["Nhập quá 255 ký tự", "“Tối đa 255 ký tự”."],
])
b.para("Khoảng trắng thừa ở đầu và cuối được tự động cắt bỏ, nên không tạo được hai cấp mà mắt "
       "thường nhìn thấy tên giống hệt nhau.")

b.h2("3. Sửa")
b.para("Bấm nút Sửa (hình bút chì) trên dòng cần sửa; cửa sổ “Sửa cấp dịch vụ” mở ra với ô Tên "
       "cấp đã điền sẵn. Ràng buộc giống hệt phần Thêm mới; giữ nguyên tên của chính bản ghi đang "
       "sửa là hợp lệ. Cửa sổ Sửa chỉ có hai nút Lưu và Đóng — nút Lưu & Tiếp tục chỉ dành cho "
       "thêm mới.")
b.para("Cấp dịch vụ đang được sử dụng ở chứng từ VẪN sửa được. Sau khi sửa, các chứng từ đang "
       "dùng cấp này sẽ hiển thị tên mới. Việc đang được sử dụng chỉ chặn thao tác Xóa.")
b.para("Nếu đã sửa nội dung mà bấm Đóng hoặc bấm dấu X ở góc trên bên phải, hệ thống cảnh báo dữ "
       "liệu chưa được lưu và hỏi xác nhận. Nếu chưa sửa gì thì cửa sổ đóng ngay.")

b.h2("4. Xem chi tiết")
b.para("Bấm nút Xem (hình con mắt). Cửa sổ “Xem cấp dịch vụ” mở ra với ô Tên cấp bị làm mờ, không "
       "gõ được và không có nút Lưu — chỉ có nút Đóng.")

# ---------------------------------------------------------------------------
b.h1("PHẦN 4: XÓA CẤP DỊCH VỤ")
b.para("Yêu cầu quyền “Quản lý cấp dịch vụ bảo dưỡng”.")

b.h2("1. Các bước")
b.bullet("Bước 1: Bấm nút Xóa (hình thùng rác màu đỏ) trên dòng cần xóa.")
b.bullet("Bước 2: Đọc hộp “Xác nhận xóa” — câu hỏi có nêu tên cấp dịch vụ để đối chiếu.")
b.bullet("Bước 3: Bấm “Xóa” để thực hiện hoặc “Hủy” để bỏ qua.")
b.image("lv-03-chan-xoa.png", "Hộp xác nhận xóa cấp dịch vụ")

b.h2("2. Khi cấp dịch vụ đang được sử dụng")
b.para("Nếu cấp dịch vụ đã xuất hiện ở gói bảo dưỡng, báo giá dịch vụ, hợp đồng dịch vụ, phiếu "
       "phân công công việc hoặc phiếu nhập kết quả, hệ thống KHÔNG mở hộp xác nhận mà hiện ngay "
       "thông báo đỏ nêu tên tối đa ba nơi đang dùng. Cấp dịch vụ vẫn giữ nguyên trong danh mục.")
b.para("Việc kiểm tra được thực hiện lại tại đúng thời điểm bấm Xóa, nên nếu người khác vừa đưa "
       "cấp này vào một chứng từ thì thao tác xóa vẫn bị chặn.")

b.h2("3. Sau khi xóa thành công")
b.para("Hiện thông báo “Xóa thành công”, dòng biến mất khỏi danh sách và tổng số dưới bảng giảm "
       "đi một. Nếu đó là dòng cuối cùng của trang, màn hình tự lùi về trang trước.")
b.para("Xóa là thao tác không lùi lại được và màn hình này không lưu lịch sử thay đổi, nên cần "
       "kiểm tra kỹ trước khi xác nhận.")

# ---------------------------------------------------------------------------
b.h1("PHẦN 5: XUẤT EXCEL")
b.para("Mọi người vào được màn hình đều dùng được chức năng này.")
b.bullet("Bước 1: Gõ điều kiện tìm kiếm và thứ tự sắp xếp mong muốn.")
b.bullet("Bước 2: Bấm nút “Xuất Excel” ở đầu bảng.")
b.bullet("Bước 3: Chờ thông báo “Xuất Excel thành công” rồi mở file tải về.")
b.para("File xuất ra lấy đúng tập dữ liệu đang tìm kiếm chứ không phải toàn bộ danh mục, và lấy "
       "đủ mọi dòng khớp điều kiện chứ không chỉ trang đang xem.")

# ---------------------------------------------------------------------------
b.h1("PHẦN CHI TIẾT: THAO TÁC TỪNG BƯỚC")

b.h2("A. Khai báo một cấp dịch vụ mới")
b.bullet("Bước A1: Vào phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → Cấp dịch vụ bảo dưỡng.")
b.bullet("Bước A2: Bấm “Tạo mới”.")
b.bullet("Bước A3: Nhập Tên cấp theo quy ước của đơn vị, ví dụ “Cấp 3 (36T/9000H)”.")
b.bullet("Bước A4: Bấm “Lưu”, kiểm tra dòng mới đã xuất hiện trong danh sách.")
b.bullet("Bước A5: Sang màn Danh mục gói bảo dưỡng, mở danh sách chọn cấp dịch vụ để kiểm tra "
         "cấp vừa tạo đã dùng được.")

b.h2("B. Đổi tên một cấp dịch vụ đang được sử dụng")
b.bullet("Bước B1: Tìm cấp dịch vụ bằng ô tìm nhanh.")
b.bullet("Bước B2: Bấm nút Sửa, đổi Tên cấp, bấm “Lưu”.")
b.bullet("Bước B3: Mở một hợp đồng dịch vụ đang dùng cấp đó để kiểm tra tên đã đổi theo.")

b.h2("C. Xóa một cấp dịch vụ khai nhầm")
b.bullet("Bước C1: Tìm cấp dịch vụ cần xóa.")
b.bullet("Bước C2: Bấm nút Xóa. Nếu hệ thống chặn và nêu nơi đang dùng, dừng lại — cấp này đã "
         "phát sinh nghiệp vụ, không được xóa.")
b.bullet("Bước C3: Nếu hộp “Xác nhận xóa” mở ra, đọc lại tên cấp cho chắc rồi bấm “Xóa”.")
b.bullet("Bước C4: Kiểm tra danh sách, tổng số dưới bảng đã giảm đi một.")

b.finish()

print("=" * 70)

# ############################################################################
# MAN 2 — DANH MUC GHI CHU KIEM TRA BAO DUONG
# ############################################################################
b = HdsdBuilder(
    output=os.path.join(HERE, "HDSD_Danh muc ghi chu kiem tra bao duong.docx"),
    shots_dir=SHOTS,
    cover_title="(Màn hình: Danh mục ghi chú kiểm tra bảo dưỡng)",
    doc_title="HDSD - Danh mục ghi chú kiểm tra bảo dưỡng",
)

b.h1("TỔNG QUAN")

b.h2("1. Mục tiêu")
b.para("Màn hình “Danh mục ghi chú kiểm tra bảo dưỡng” dùng để khai báo các hạng mục cần ghi chú "
       "khi kiểm tra bảo dưỡng thiết bị, ví dụ “Kiểm tra ngoại quan không tháo lắp”, "
       "“Đo kiểm, kiểm tra bằng dụng cụ chuyên dùng”, “Bôi trơn bạc đạn, cốt, trục xoay”.")
b.para("Mỗi hạng mục có một Ký hiệu viết tắt (ví dụ KTBM, DK, CC) để nhân viên kỹ thuật ghi nhanh "
       "trên phiếu hiện trường. Danh mục này được gắn vào cấp bảo dưỡng của từng gói dịch vụ.")
b.para("Lưu ý quan trọng: danh mục này dùng CHUNG dữ liệu với màn tương ứng bên phần mềm cũ. "
       "Sửa ở cổng nào thì cổng còn lại cũng thấy ngay.")

b.h2("2. Đường dẫn truy cập")
b.para("Trên menu trái của phân hệ Chăm sóc khách hàng, vào nhóm “Danh mục - Dịch vụ” rồi chọn "
       "“Danh mục ghi chú kiểm tra bảo dưỡng” (đường dẫn: /customer-care/note-maintenances).")
b.para("Mục menu chỉ hiển thị khi tài khoản có ít nhất một trong hai quyền “Quản lý ghi chú kiểm "
       "tra bảo dưỡng” hoặc “Xem ghi chú kiểm tra bảo dưỡng”.")

b.h2("3. Vai trò tham gia")
b.table([
    ["Vai trò", "Thao tác chính"],
    ["Người quản lý danh mục dịch vụ", "Thêm mới, Sửa, Xóa ghi chú; xuất Excel."],
    ["Người dùng chỉ xem", "Xem danh sách, mở xem chi tiết, tìm kiếm và xuất Excel."],
    ["Bộ phận kỹ thuật", "Là bên sử dụng các ghi chú này khi cấu hình cấp bảo dưỡng của gói dịch "
                         "vụ và khi ghi kết quả kiểm tra tại hiện trường."],
])

b.h2("4. Đặc điểm riêng của màn hình")
b.bullet("Màn hình KHÔNG có trạng thái Hoạt động / Khóa. Chỉ có ba thao tác: Thêm mới, Sửa và Xóa.")
b.bullet("Ghi chú đang được gắn vào cấp bảo dưỡng của gói dịch vụ thì KHÔNG xóa được.")
b.bullet("Ở phần mềm cũ, màn này KHÔNG chặn xóa gì cả, dù phần lớn ghi chú đang được sử dụng — "
         "xóa xong là gói dịch vụ mất ghi chú. Bản mới đã chặn lại.")
b.bullet("Ở phần mềm cũ, thêm và sửa mở ra một trang riêng; bản mới đưa về cửa sổ nhỏ ngay trên "
         "danh sách cho đồng bộ với các danh mục khác. Đây là thay đổi có chủ ý.")

b.h2("5. Luồng sử dụng")
b.bullet("Bước 1 — Khai báo các hạng mục ghi chú cần dùng ở màn này.")
b.bullet("Bước 2 — Sang màn Danh mục gói bảo dưỡng, gắn ghi chú vào từng cấp bảo dưỡng của gói.")
b.bullet("Bước 3 — Nhân viên kỹ thuật dùng ký hiệu để ghi nhanh kết quả kiểm tra tại hiện trường.")
b.bullet("Bước 4 (khi cần điều chỉnh) — Sửa lại hạng mục, ký hiệu hoặc mô tả; các gói dịch vụ "
         "đang dùng sẽ hiển thị nội dung mới.")

# ---------------------------------------------------------------------------
b.h1("PHẦN 1: DANH SÁCH & TÌM KIẾM")

b.image("nm-01-danh-sach.png", "Màn hình danh sách Danh mục ghi chú kiểm tra bảo dưỡng")

b.h2("1. Bố cục màn hình")
b.bullet("Khối trên — “Bộ lọc ghi chú kiểm tra bảo dưỡng” với dòng phụ “Tìm kiếm theo hạng mục "
         "hoặc ký hiệu”: chỉ có ô tìm nhanh, nút Tìm kiếm và nút Làm mới.")
b.bullet("Khối dưới — bảng “Danh mục ghi chú kiểm tra bảo dưỡng” cùng nút Tạo mới và Xuất Excel "
         "ở đầu bảng.")
b.para("Trong ảnh minh họa, nút Xóa ở mọi dòng đều bị làm mờ vì các ghi chú này đang được gắn "
       "vào cấp bảo dưỡng của gói dịch vụ — xem Phần 4 để hiểu điều kiện xóa.")

b.h2("2. Các cột của bảng")
b.table([
    ["Cột", "Nội dung"],
    ["STT", "Số thứ tự tính theo trang đang xem."],
    ["Hạng mục", "Nội dung hạng mục kiểm tra, là giá trị duy nhất trong danh mục."],
    ["Ký hiệu", "Mã viết tắt của hạng mục, cũng phải duy nhất. Hiển thị dạng nhãn nhỏ."],
    ["Mô tả", "Diễn giải chi tiết; để trống thì hiện dấu gạch ngang. Nội dung dài được xuống dòng "
              "trong ô, không cắt cụt."],
    ["Cập nhật", "Ngày giờ thay đổi gần nhất."],
    ["Hành động", "Ba nút: Xem, Sửa, Xóa."],
])

b.h2("3. Tìm nhanh")
b.para("Ô tìm nhanh có dòng gợi ý “Tìm theo hạng mục hoặc ký hiệu...”. Ô này quét hai trường "
       "Hạng mục và Ký hiệu — KHÔNG quét cột Mô tả. Gõ một chuỗi chỉ có trong Mô tả sẽ ra kết quả "
       "rỗng; đây là hành vi đúng theo thiết kế.")
b.para("Gõ một phần chuỗi là đủ, không phân biệt chữ hoa chữ thường. Phải bấm nút Tìm kiếm hoặc "
       "nhấn Enter thì danh sách mới lọc. Nút Làm mới xóa nội dung ô tìm nhanh và nạp lại danh "
       "sách ngay.")

b.h2("4. Sắp xếp và phân trang")
b.bullet("Bấm tiêu đề cột Hạng mục, Ký hiệu hoặc Cập nhật để sắp xếp; bấm lần nữa để đảo chiều.")
b.bullet("Cột Mô tả không sắp xếp được.")
b.bullet("Cuối bảng có dòng “Hiển thị a – b / N”: N là tổng số ghi chú khớp điều kiện tìm kiếm.")

# ---------------------------------------------------------------------------
b.h1("PHẦN 2: PHÂN QUYỀN & HƯỚNG DẪN THEO QUYỀN")

b.h2("1. Bảng quyền của màn hình")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / khu vực tương ứng"],
    ["Xem ghi chú kiểm tra bảo dưỡng",
     "Vào màn hình, xem danh sách, tìm kiếm, mở xem chi tiết, xuất Excel.",
     "Nút Xem trên mỗi dòng; nút Xuất Excel."],
    ["Quản lý ghi chú kiểm tra bảo dưỡng",
     "Toàn bộ quyền trên, cộng thêm: thêm mới, sửa và xóa ghi chú.",
     "Nút Tạo mới; nút Sửa và nút Xóa trên mỗi dòng."],
])
b.para("Danh mục này KHÔNG phân quyền theo công ty, phòng ban hay bộ phận.")

b.h2("2. Người dùng có quyền “Xem ghi chú kiểm tra bảo dưỡng”")
b.para("Vào được màn hình và thấy đầy đủ danh sách, nhưng KHÔNG có nút Tạo mới; mỗi dòng chỉ có "
       "nút Xem, không có nút Sửa và nút Xóa. Nút Xuất Excel vẫn dùng được bình thường.")

b.h2("3. Người dùng có quyền “Quản lý ghi chú kiểm tra bảo dưỡng”")
b.para("Thấy đầy đủ nút Tạo mới và Xuất Excel; trên mỗi dòng có đủ Xem, Sửa, Xóa.")
b.para("Nếu không có quyền này, các nút trên sẽ không hiển thị; trường hợp truy cập trực tiếp "
       "bằng đường dẫn hoặc bằng công cụ ngoài giao diện, hệ thống từ chối và báo không có quyền.")

# ---------------------------------------------------------------------------
b.h1("PHẦN 3: THÊM MỚI, SỬA VÀ XEM")

b.h2("1. Thêm mới")
b.para("Yêu cầu quyền “Quản lý ghi chú kiểm tra bảo dưỡng”. Bấm nút “Tạo mới” ở đầu bảng; hệ "
       "thống mở CỬA SỔ NHỎ “Thêm ghi chú kiểm tra” ngay trên danh sách.")
b.image("nm-03-them.png", "Cửa sổ Thêm ghi chú kiểm tra")
b.table([
    ["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị mặc định khi mở form", "Ghi chú"],
    ["Hạng mục", "Ô chữ", "Có", "Để trống", "Phải duy nhất. Trùng sẽ báo “Hạng mục đã tồn tại”. "
                                           "Tối đa 255 ký tự. Gợi ý trong ô: “VD: Kiểm tra ngoại "
                                           "quan không tháo lắp.”."],
    ["Ký hiệu", "Ô chữ", "Có", "Để trống", "Cũng phải duy nhất. Trùng sẽ báo “Ký hiệu đã tồn tại”. "
                                          "Tối đa 255 ký tự. Gợi ý trong ô: “VD: KTBM”."],
    ["Mô tả", "Ô chữ nhiều dòng", "Không", "Để trống", "Diễn giải chi tiết hạng mục kiểm tra. "
                                                      "Tối đa 255 ký tự."],
])
b.para("Hai trường bắt buộc — Hạng mục và Ký hiệu — có dấu sao đỏ bên cạnh nhãn. "
       "Cuối cửa sổ có ba nút:")
b.table([
    ["Nút", "Tác dụng"],
    ["Lưu", "Lưu ghi chú, đóng cửa sổ và nạp lại danh sách."],
    ["Lưu & Tiếp tục", "Lưu ghi chú nhưng GIỮ cửa sổ mở và xóa trắng các ô để nhập tiếp. "
                       "Dùng khi cần khai nhiều hạng mục liên tiếp."],
    ["Đóng", "Đóng cửa sổ. Nếu đang nhập dở, hệ thống hỏi xác nhận trước khi đóng."],
])

b.h2("2. Thông báo lỗi thường gặp")
b.table([
    ["Tình huống", "Hệ thống báo"],
    ["Bỏ trống ô bắt buộc", "Ô viền đỏ, hiện chữ đỏ “Bắt buộc phải nhập” ngay dưới ô; "
                            "cửa sổ không đóng, dữ liệu đã nhập vẫn còn."],
    ["Hạng mục đã có trong danh mục", "“Hạng mục đã tồn tại”."],
    ["Ký hiệu đã có trong danh mục", "“Ký hiệu đã tồn tại”."],
    ["Nhập quá 255 ký tự", "“Tối đa 255 ký tự”."],
])

b.h2("3. Sửa")
b.para("Bấm nút Sửa (hình bút chì); cửa sổ “Sửa ghi chú kiểm tra” mở ra với cả ba ô đã điền sẵn. "
       "Ràng buộc giống hệt phần Thêm mới; giữ nguyên hạng mục và ký hiệu của chính bản ghi đang "
       "sửa là hợp lệ. Cửa sổ Sửa chỉ có hai nút Lưu và Đóng — nút Lưu & Tiếp tục chỉ dành cho "
       "thêm mới.")
b.para("Ghi chú đang được sử dụng ở gói dịch vụ VẪN sửa được. Sau khi sửa, các gói dịch vụ đang "
       "dùng sẽ hiển thị nội dung mới. Việc đang được sử dụng chỉ chặn thao tác Xóa.")
b.para("Nếu đã sửa nội dung mà bấm Đóng, hệ thống cảnh báo dữ liệu chưa được lưu và hỏi xác nhận.")

b.h2("4. Xem chi tiết")
b.para("Bấm nút Xem (hình con mắt). Cửa sổ “Xem ghi chú kiểm tra” mở ra với đầy đủ ba ô nhưng đều "
       "bị làm mờ, không gõ được và không có nút Lưu — chỉ có nút Đóng.")
b.image("nm-02-xem.png", "Cửa sổ Xem ghi chú kiểm tra ở chế độ chỉ đọc")

# ---------------------------------------------------------------------------
b.h1("PHẦN 4: XÓA GHI CHÚ")
b.para("Yêu cầu quyền “Quản lý ghi chú kiểm tra bảo dưỡng”.")

b.h2("1. Khi nào xóa được")
b.para("Chỉ xóa được ghi chú CHƯA được gắn vào cấp bảo dưỡng của bất kỳ gói dịch vụ nào. Với ghi "
       "chú đang được sử dụng, nút Xóa bị làm mờ và không bấm được; rê chuột vào nút sẽ hiện chú "
       "thích “Ghi chú đang được sử dụng ở nghiệp vụ khác, không thể xóa”.")
b.para("Trong thực tế phần lớn ghi chú đều đang được sử dụng, nên nút Xóa thường ở trạng thái mờ. "
       "Đây là hành vi đúng, không phải lỗi.")

b.h2("2. Các bước xóa")
b.bullet("Bước 1: Bấm nút Xóa (hình thùng rác màu đỏ) trên dòng cần xóa.")
b.bullet("Bước 2: Đọc hộp “Xác nhận xóa” — câu hỏi có nêu tên hạng mục để đối chiếu.")
b.bullet("Bước 3: Bấm “Xóa” để thực hiện hoặc “Hủy” để bỏ qua.")
b.para("Sau khi xóa: hiện thông báo “Xóa thành công”, dòng biến mất và tổng số dưới bảng giảm đi "
       "một. Nếu đó là dòng cuối cùng của trang, màn hình tự lùi về trang trước.")
b.para("Việc kiểm tra được thực hiện lại tại đúng thời điểm bấm Xóa, nên nếu người khác vừa gắn "
       "ghi chú này vào một gói dịch vụ thì thao tác xóa vẫn bị chặn.")

# ---------------------------------------------------------------------------
b.h1("PHẦN 5: XUẤT EXCEL")
b.para("Mọi người vào được màn hình đều dùng được chức năng này.")
b.bullet("Bước 1: Gõ điều kiện tìm kiếm mong muốn.")
b.bullet("Bước 2: Bấm nút “Xuất Excel” ở đầu bảng.")
b.bullet("Bước 3: Chờ thông báo “Xuất Excel thành công” rồi mở file tải về.")
b.para("File xuất ra có các cột Hạng mục, Ký hiệu và Mô tả, lấy đúng tập dữ liệu đang tìm kiếm và "
       "đủ mọi dòng khớp điều kiện chứ không chỉ trang đang xem. Nội dung mô tả dài vẫn giữ "
       "nguyên, không bị cắt cụt.")

# ---------------------------------------------------------------------------
b.h1("PHẦN CHI TIẾT: THAO TÁC TỪNG BƯỚC")

b.h2("A. Khai báo một hạng mục ghi chú mới")
b.bullet("Bước A1: Vào phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → Danh mục ghi chú kiểm "
         "tra bảo dưỡng.")
b.bullet("Bước A2: Bấm “Tạo mới”.")
b.bullet("Bước A3: Nhập Hạng mục, ví dụ “Kiểm tra siết lực bu lông đế máy”.")
b.bullet("Bước A4: Nhập Ký hiệu viết tắt, ví dụ “KTSL”. Ký hiệu nên ngắn và dễ nhớ vì nhân viên "
         "kỹ thuật dùng để ghi nhanh tại hiện trường.")
b.bullet("Bước A5: Nhập Mô tả chi tiết nếu cần, bấm “Lưu”.")
b.bullet("Bước A6: Sang màn Danh mục gói bảo dưỡng, vào phần cấp bảo dưỡng, kiểm tra ghi chú vừa "
         "tạo đã có trong danh sách chọn.")

b.h2("B. Sửa nội dung một ghi chú đang được sử dụng")
b.bullet("Bước B1: Tìm ghi chú bằng ô tìm nhanh theo hạng mục hoặc ký hiệu.")
b.bullet("Bước B2: Bấm nút Sửa, chỉnh lại Hạng mục hoặc Mô tả, bấm “Lưu”.")
b.bullet("Bước B3: Mở một gói dịch vụ đang dùng ghi chú đó để kiểm tra nội dung đã đổi theo.")

b.h2("C. Xóa một ghi chú khai nhầm")
b.bullet("Bước C1: Tìm ghi chú cần xóa.")
b.bullet("Bước C2: Rê chuột vào nút Xóa. Nếu nút bị mờ, đọc chú thích — ghi chú đã được gắn vào "
         "gói dịch vụ, không xóa được.")
b.bullet("Bước C3: Nếu nút bấm được, bấm Xóa, đọc lại tên hạng mục trong hộp xác nhận rồi bấm “Xóa”.")
b.bullet("Bước C4: Kiểm tra danh sách, tổng số dưới bảng đã giảm đi một.")

b.finish()
