# -*- coding: utf-8 -*-
"""Sinh HDSD cho man Cap nhat nhanh gia dich vu (CSKH).

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
    output=os.path.join(HERE, "HDSD_Cap nhat nhanh gia dich vu.docx"),
    shots_dir=os.path.join(HERE, "hdsd_shots"),
    cover_title="(Màn hình: Cập nhật nhanh giá dịch vụ)",
    doc_title="HDSD - Cập nhật nhanh giá dịch vụ",
)

# ============================================================================
b.h1("TỔNG QUAN")

b.h2("1. Mục tiêu")
b.para("Màn hình “Cập nhật nhanh giá dịch vụ” dùng để đặt hai thông số chung áp cho toàn bộ gói "
       "bảo dưỡng trong hệ thống: Hệ số giá bán dịch vụ và Định mức đàm phán giá (%).")
b.para("Thay vì phải vào sửa từng gói một, người quản lý chỉ cần nhập hai con số ở đây và bấm "
       "Lưu; hệ thống áp ngay cho tất cả gói bảo dưỡng và tính lại giá gốc của các cấp dịch vụ.")

b.h2("2. ⚠️ Màn hình có sức ảnh hưởng lớn nhất trong nhóm danh mục dịch vụ")
b.para("Một lần bấm Lưu là thay đổi giá của hàng trăm gói bảo dưỡng. Ba điểm phải nắm trước khi "
       "dùng:")
b.bullet("MỌI gói bảo dưỡng đều bị áp lại, KỂ CẢ gói đã được chỉnh riêng trước đó. Giá trị riêng "
         "của gói sẽ bị ghi đè, không giữ lại được.")
b.bullet("Màn hình KHÔNG lưu lịch sử thay đổi, cũng không có chức năng hoàn tác. Bấm nhầm là "
         "phải nhập lại giá trị cũ bằng tay.")
b.bullet("Nên ghi lại (hoặc chụp màn hình) giá trị hai thông số hiện tại TRƯỚC khi thay đổi, để "
         "còn quay lại được nếu cần.")
b.para("Để giảm rủi ro, hệ thống luôn hiện một hộp xác nhận nêu rõ số gói và số cấp dịch vụ bị "
       "ảnh hưởng trước khi ghi. Ở phần mềm cũ, bấm Lưu là chạy luôn, không hỏi.")

b.h2("3. Đường dẫn truy cập")
b.para("Trên menu trái của phân hệ Chăm sóc khách hàng, vào nhóm “Danh mục - Dịch vụ” rồi chọn "
       "“Cập nhật nhanh giá dịch vụ” (đường dẫn: /customer-care/service-price-config).")

b.h2("4. Vai trò tham gia")
b.table([
    ["Vai trò", "Thao tác chính"],
    ["Người phụ trách giá dịch vụ", "Xem và cập nhật hai thông số chung."],
    ["Bộ phận lập báo giá dịch vụ", "Là bên chịu ảnh hưởng: giá dịch vụ trên báo giá mới được "
                                    "tính theo hai thông số này."],
    ["Người quản lý gói bảo dưỡng", "Cần biết rằng giá trị chỉnh riêng ở từng gói sẽ bị ghi đè "
                                    "mỗi khi màn này được lưu."],
])

b.h2("5. Ý nghĩa hai thông số")
b.table([
    ["Thông số", "Ý nghĩa", "Giới hạn"],
    ["Hệ số giá bán dịch vụ", "Hệ số nhân từ giá vốn ra giá bán của dịch vụ. Khi hệ số này thay "
                              "đổi, giá gốc của các cấp dịch vụ được tính lại.",
     "Bắt buộc nhập. Phải lớn hơn 0, tối đa 999,99."],
    ["Định mức đàm phán giá (%)", "Mức phần trăm tối đa mà người bán được phép giảm khi đàm phán "
                                  "giá với khách hàng.",
     "Không bắt buộc. Từ 0 đến 99."],
])

b.h2("6. Quy tắc áp giá — điểm quan trọng nhất")
b.bullet("Hệ số và định mức LUÔN được ghi đè cho mọi gói bảo dưỡng mỗi lần bấm Lưu, kể cả khi "
         "giá trị không đổi.")
b.bullet("Giá gốc của cấp dịch vụ CHỈ được tính lại khi Hệ số giá bán dịch vụ THỰC SỰ thay đổi. "
         "Nếu chỉ đổi Định mức đàm phán giá thì giá gốc giữ nguyên.")
b.bullet("Gói bảo dưỡng không xác định được đơn giá công của công ty sẽ được BỎ QUA, không bị ghi "
         "giá về 0. Sau khi lưu, hệ thống báo lại số gói đã bỏ qua. (Ở phần mềm cũ, những gói này "
         "bị đưa giá gốc về 0 — tức là mất giá.)")
b.bullet("Thông số chỉ áp cho việc lập chứng từ MỚI. Các báo giá và hợp đồng dịch vụ đã lập trước "
         "đó giữ nguyên giá, không bị tính lại.")

# ============================================================================
b.h1("PHẦN 1: BỐ CỤC MÀN HÌNH")

b.image("01-man-hinh.png", "Màn hình Cập nhật nhanh giá dịch vụ")

b.para("Màn hình rất gọn, chỉ gồm một khung nhập đặt giữa trang. Không có bảng danh sách, không "
       "có bộ lọc, không có phân trang.")

b.h2("1. Các thành phần")
b.table([
    ["Thành phần", "Nội dung"],
    ["Hệ số giá bán dịch vụ", "Ô nhập số, bắt buộc — có dấu (*) màu đỏ bên cạnh nhãn. Khi mở màn, "
                             "ô hiện giá trị đang lưu của hệ thống."],
    ["Định mức đàm phán giá (%)", "Ô nhập số, không bắt buộc. Cũng hiện giá trị đang lưu."],
    ["Dòng ghi chú", "Nằm ngay dưới hai ô, nêu SỐ GÓI BẢO DƯỠNG sẽ bị áp lại và nhắc rằng giá trị "
                     "đã chỉnh riêng ở từng gói sẽ bị ghi đè."],
    ["Dòng “Cập nhật gần nhất”", "Cho biết thời điểm hai thông số này được thay đổi lần cuối. "
                                 "Nếu hệ thống chưa từng lưu lần nào thì dòng này không hiện."],
    ["Nút Lưu", "Nằm ở góc dưới bên phải khung. Trong lúc hệ thống đang xử lý, nút đổi chữ thành "
                "“Đang lưu...” và không bấm lại được."],
])

b.h2("2. Khi hệ thống chưa từng đặt thông số")
b.para("Nếu đây là lần đầu sử dụng, hai ô sẽ để trống và không có dòng “Cập nhật gần nhất”. Màn "
       "hình vẫn mở bình thường — chỉ cần nhập giá trị rồi lưu như hướng dẫn ở Phần 3.")

# ============================================================================
b.h1("PHẦN 2: PHÂN QUYỀN & HƯỚNG DẪN THEO QUYỀN")

b.h2("1. Bảng quyền của màn hình")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút / khu vực tương ứng"],
    ["Cập nhật nhanh giá dịch vụ",
     "Vào màn hình, xem hai thông số hiện tại và lưu thay đổi.",
     "Toàn bộ màn hình và nút Lưu."],
])
b.para("Màn hình chỉ có DUY NHẤT một quyền. Có quyền thì vừa xem vừa sửa được; không có quyền thì "
       "không vào được màn hình.")

b.h2("2. Quyền này tồn tại ở cả hai cổng")
b.para("Quyền “Cập nhật nhanh giá dịch vụ” được khai ở CẢ hai hệ thống dưới cùng một tên. Người "
       "được cấp quyền ở phần mềm cũ HOẶC ở cổng mới đều vào được màn này.")
b.para("Vì vậy khi rà soát phân quyền, cần kiểm cả hai đường cấp quyền. Nếu một người đã được cấp "
       "quyền ở phần mềm cũ mà vào cổng mới lại bị chặn, đó là lỗi cần báo lại ngay.")

b.h2("3. Người dùng không có quyền")
b.para("Mục menu “Cập nhật nhanh giá dịch vụ” không hiển thị. Trường hợp gõ thẳng đường dẫn, hệ "
       "thống chuyển sang trang báo không tìm thấy và không trả về giá trị thông số nào. Việc "
       "kiểm soát được thực hiện cả ở giao diện lẫn ở tầng dữ liệu, nên không thể lưu thông số "
       "bằng cách đi vòng qua giao diện.")

b.h2("4. Màn hình không phân quyền theo cấp")
b.para("Toàn hệ thống chỉ có DUY NHẤT một bộ thông số này, dùng chung cho mọi công ty. Không có "
       "chuyện mỗi công ty một hệ số riêng.")

# ============================================================================
b.h1("PHẦN 3: CẬP NHẬT THÔNG SỐ")
b.para("Yêu cầu quyền “Cập nhật nhanh giá dịch vụ”.")

b.h2("1. Các bước")
b.bullet("Bước 1: Ghi lại giá trị hiện tại của hai ô để còn quay lại được nếu cần.")
b.bullet("Bước 2: Nhập Hệ số giá bán dịch vụ mới. Nếu chỉ muốn đổi định mức thì giữ nguyên ô này.")
b.bullet("Bước 3: Nhập Định mức đàm phán giá (%) nếu cần.")
b.bullet("Bước 4: Bấm nút “Lưu” ở góc dưới bên phải.")
b.bullet("Bước 5: Đọc kỹ hộp xác nhận, đối chiếu số gói và số cấp dịch vụ bị ảnh hưởng.")
b.bullet("Bước 6: Bấm “Đồng ý” để thực hiện, hoặc “Hủy” để dừng lại — bấm Hủy thì hệ thống không "
         "ghi gì cả.")

b.h2("2. Hộp xác nhận")
b.image("02-xac-nhan.png", "Hộp xác nhận cập nhật giá dịch vụ")
b.para("Hộp có tiêu đề “Xác nhận cập nhật giá dịch vụ” và nêu ba thông tin:")
b.bullet("Số gói bảo dưỡng sẽ bị cập nhật, kèm cảnh báo ghi đè giá trị đã chỉnh riêng ở từng gói.")
b.bullet("Số cấp dịch vụ sẽ được tính lại giá gốc, với điều kiện hệ số thay đổi.")
b.bullet("Câu hỏi xác nhận cuối cùng.")
b.para("Hai con số này lấy trực tiếp từ dữ liệu thực tế của hệ thống tại thời điểm bấm, không "
       "phải số cố định. Hãy đọc kỹ trước khi bấm “Đồng ý”.")

b.h2("3. Kết quả sau khi lưu")
b.para("Hệ thống hiện thông báo kết quả nêu số gói đã cập nhật, số cấp dịch vụ đã tính lại giá "
       "và số gói bị bỏ qua (nếu có). Nạp lại màn hình thì hai ô hiện giá trị mới và dòng "
       "“Cập nhật gần nhất” đổi sang thời điểm vừa lưu.")
b.para("Với khoảng 200 gói bảo dưỡng, quá trình này mất vài giây. Trong lúc đó nút Lưu bị vô hiệu "
       "nên không thể chạy hai lượt ghi chồng lên nhau.")

b.h2("4. Kiểm tra lại sau khi lưu")
b.para("Màn hình này không hiện danh sách gói, nên muốn kiểm chứng phải sang màn “Danh mục gói "
       "bảo dưỡng”, mở vài gói bất kỳ và đối chiếu hệ số, định mức cùng giá gốc của cấp dịch vụ.")

# ============================================================================
b.h1("PHẦN 4: RÀNG BUỘC NHẬP LIỆU")

b.h2("1. Bảng lỗi và thông báo")
b.table([
    ["Tình huống", "Hệ thống báo"],
    ["Bỏ trống Hệ số giá bán dịch vụ", "“Bắt buộc phải nhập”."],
    ["Hệ số bằng 0 hoặc số âm", "“Phải lớn hơn 0”."],
    ["Hệ số nhập chữ", "“Phải là số”."],
    ["Hệ số lớn hơn 999,99", "“Tối đa 999,99”."],
    ["Định mức là số âm", "“Không được nhỏ hơn 0”."],
    ["Định mức lớn hơn 99", "“Tối đa 99”."],
    ["Định mức nhập chữ", "“Phải là số”."],
])
b.para("Khi có lỗi, ô sai được viền đỏ và hiện chữ đỏ ngay dưới ô; hệ thống KHÔNG mở hộp xác nhận "
       "và không ghi gì cả.")

b.h2("2. Lỗi chỉ hiện sau lần bấm Lưu đầu tiên")
b.para("Khi vừa mở màn hình, các ô không viền đỏ dù đang để trống. Chữ báo lỗi chỉ xuất hiện sau "
       "khi bấm Lưu lần đầu. Đây là hành vi đúng theo thiết kế, giúp màn hình không bị đỏ ngay từ "
       "lúc mới vào.")

b.h2("3. Hai điểm dễ nhầm")
b.bullet("Định mức đàm phán giá bỏ trống là HỢP LỆ — ô này không bắt buộc.")
b.bullet("Nhập Định mức bằng 0 cũng hợp lệ và được lưu thật. Sau khi lưu, nạp lại màn hình phải "
         "thấy số 0 chứ không phải ô trống.")

# ============================================================================
b.h1("PHẦN 5: CẢNH BÁO KHI CHƯA LƯU")
b.para("Nếu đã sửa giá trị trong ô mà chưa bấm Lưu rồi chuyển sang màn khác, hệ thống cảnh báo dữ "
       "liệu chưa được lưu và hỏi xác nhận.")
b.bullet("Chọn ở lại: màn hình giữ nguyên giá trị đang gõ.")
b.bullet("Chọn thoát: giá trị cũ không bị thay đổi, hệ thống không ghi gì.")
b.para("Nếu chưa sửa gì thì chuyển màn ngay, không hỏi lại. Sau khi đã lưu thành công cũng không "
       "còn cảnh báo nữa.")

# ============================================================================
b.h1("PHẦN CHI TIẾT: THAO TÁC TỪNG BƯỚC")

b.h2("A. Điều chỉnh hệ số giá bán cho toàn hệ thống")
b.bullet("Bước A1: Vào phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → Cập nhật nhanh giá dịch vụ.")
b.bullet("Bước A2: Ghi lại giá trị hiện tại của cả hai ô.")
b.bullet("Bước A3: Sang màn Danh mục gói bảo dưỡng, ghi lại giá của vài gói tiêu biểu để đối "
         "chiếu về sau.")
b.bullet("Bước A4: Quay lại màn này, nhập Hệ số giá bán dịch vụ mới.")
b.bullet("Bước A5: Bấm “Lưu”, đọc kỹ hộp xác nhận, bấm “Đồng ý”.")
b.bullet("Bước A6: Đọc thông báo kết quả, ghi lại số gói đã cập nhật và số gói bị bỏ qua.")
b.bullet("Bước A7: Sang màn Danh mục gói bảo dưỡng, mở lại các gói đã ghi ở bước A3 để đối chiếu.")

b.h2("B. Chỉ điều chỉnh định mức đàm phán giá")
b.bullet("Bước B1: GIỮ NGUYÊN ô Hệ số giá bán dịch vụ, không sửa gì.")
b.bullet("Bước B2: Nhập giá trị mới vào ô Định mức đàm phán giá (%).")
b.bullet("Bước B3: Bấm “Lưu” và “Đồng ý”.")
b.bullet("Bước B4: Kiểm tra ở màn Danh mục gói bảo dưỡng: định mức của các gói đã đổi, còn giá "
         "gốc của cấp dịch vụ giữ nguyên vì hệ số không thay đổi.")

b.h2("C. Kiểm tra ảnh hưởng tới báo giá dịch vụ")
b.bullet("Bước C1: Trước khi đổi thông số, mở một báo giá dịch vụ đã lập và ghi lại tổng tiền.")
b.bullet("Bước C2: Đổi hệ số ở màn này và lưu.")
b.bullet("Bước C3: Mở lại báo giá cũ — tổng tiền phải GIỮ NGUYÊN.")
b.bullet("Bước C4: Lập một báo giá dịch vụ MỚI với cùng gói bảo dưỡng — giá phải tính theo hệ số mới.")

b.h2("D. Quay lại giá trị cũ khi bấm nhầm")
b.bullet("Bước D1: Lấy lại giá trị cũ đã ghi trước đó (màn hình không có chức năng hoàn tác).")
b.bullet("Bước D2: Nhập lại đúng hai giá trị cũ vào hai ô.")
b.bullet("Bước D3: Bấm “Lưu” và “Đồng ý”.")
b.bullet("Bước D4: Đối chiếu lại giá của vài gói bảo dưỡng với số liệu đã ghi ban đầu.")
b.para("Lưu ý: nếu gói bảo dưỡng nào đã được chỉnh riêng trước đó thì giá trị riêng ấy KHÔNG quay "
       "lại được bằng cách này — phải vào sửa lại từng gói ở màn Danh mục gói bảo dưỡng.")

b.finish()
