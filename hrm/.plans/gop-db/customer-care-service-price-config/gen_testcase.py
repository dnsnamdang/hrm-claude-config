# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man Cap nhat nhanh gia dich vu (CSKH).

Chay:  python gen_testcase.py
"""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(HERE, "testcase.xlsx")
SHEET_NAME = "Trang tính1"
FEATURE_NAME = "Cập nhật nhanh giá dịch vụ - Cập nhật ngày 13/08/2026"
MODULE_NAME = "Cập nhật nhanh giá DV"

# ============================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Đặt HAI thông số chung dùng để tính giá bán dịch vụ bảo dưỡng cho toàn hệ thống: "
     "Hệ số giá bán dịch vụ và Định mức đàm phán giá (%).\n"
     "Bấm Lưu là hệ thống áp ngay hai thông số này cho TẤT CẢ gói bảo dưỡng đang có "
     "(khoảng 207 gói) và tính lại giá gốc của các cấp dịch vụ (khoảng 242 cấp).\n"
     "Màn hình nằm ở phân hệ Chăm sóc khách hàng → nhóm menu Danh mục - Dịch vụ → "
     "Cập nhật nhanh giá dịch vụ.\n"
     "⚠️ Đây là màn có SỨC ẢNH HƯỞNG LỚN NHẤT trong nhóm danh mục dịch vụ: một lần bấm Lưu là "
     "đổi giá hàng trăm gói. Trước khi kiểm thử BẮT BUỘC phải sao lưu dữ liệu giá hiện tại."),

    ("2. Đối tượng được tính / hiển thị",
     "- Màn hình chỉ là MỘT khung nhập với 2 ô: Hệ số giá bán dịch vụ (bắt buộc) và "
     "Định mức đàm phán giá (%) (không bắt buộc). Không có bảng danh sách, không có bộ lọc.\n"
     "- Dưới 2 ô có dòng ghi chú nêu rõ SỐ GÓI BẢO DƯỠNG sẽ bị ảnh hưởng, và dòng "
     "\"Cập nhật gần nhất\" cho biết lần thay đổi trước đó.\n"
     "- Khi bấm Lưu: MỌI gói bảo dưỡng đều bị áp lại hệ số và định mức, KỂ CẢ gói đã được chỉnh "
     "riêng trước đó."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Gói bảo dưỡng không xác định được đơn giá công của công ty sẽ bị BỎ QUA, không bị ghi "
     "giá về 0. Sau khi lưu, hệ thống báo lại số gói đã bỏ qua.\n"
     "⚠️ Ở hệ thống cũ những gói này bị ghi giá gốc về 0 — tức là mất giá. Bản mới bỏ qua "
     "và báo lại. Đây là điểm bắt buộc phải kiểm.\n"
     "- Giá gốc của cấp dịch vụ CHỈ được tính lại khi Hệ số giá bán dịch vụ thực sự thay đổi. "
     "Nếu chỉ đổi Định mức đàm phán giá thì giá gốc giữ nguyên."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng. Màn hình không có bộ lọc nào.\n"
     "Dòng \"Cập nhật gần nhất\" chỉ để xem, không phải điều kiện lọc."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Không có cây phân cấp. Toàn hệ thống chỉ có DUY NHẤT một bộ thông số này, dùng chung "
     "cho mọi công ty.\n"
     "Quan hệ với màn khác: hai thông số này chảy xuống Danh mục gói bảo dưỡng "
     "(mỗi gói có hệ số và định mức riêng, nhưng bị màn này ghi đè) và xuống cấp dịch vụ "
     "của từng gói (giá gốc)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Không cộng dồn, không có bản ghi trùng. Mỗi lần Lưu là GHI ĐÈ lên giá trị cũ, "
     "không tạo thêm bản ghi mới.\n"
     "Không có lịch sử thay đổi cho màn này — sai là không lùi lại được bằng giao diện."),

    ("7. Phân quyền cấp",
     "Chỉ MỘT quyền duy nhất: \"Cập nhật nhanh giá dịch vụ\".\n"
     "Có quyền thì vào được màn hình và bấm Lưu được. Không có quyền thì không vào được màn hình.\n"
     "⚠️ Quyền này tồn tại ở CẢ hai cổng dưới cùng một tên. Người được cấp quyền ở cổng cũ HOẶC ở "
     "cổng mới đều dùng được màn này. Khi kiểm thử phân quyền, hãy kiểm đủ cả hai đường cấp quyền.\n"
     "Màn hình KHÔNG phân quyền theo công ty / phòng ban / bộ phận."),

    ("8. Cách tính các ô thống kê",
     "- Con số gói bảo dưỡng trong dòng ghi chú và trong hộp xác nhận = tổng số gói bảo dưỡng "
     "hiện có trong hệ thống, lấy trực tiếp từ dữ liệu chứ không phải số cố định.\n"
     "- Con số cấp dịch vụ trong hộp xác nhận = tổng số cấp dịch vụ sẽ được tính lại giá gốc.\n"
     "- Thông báo sau khi lưu nêu số gói đã cập nhật, số cấp đã tính lại giá và số gói bị bỏ qua."),

    ("9. Ghi chú đọc bảng",
     "- BẮT BUỘC sao lưu giá của các gói bảo dưỡng và cấp dịch vụ TRƯỚC lần bấm Lưu đầu tiên. "
     "Sao lưu sau khi đã lưu là mất dữ liệu gốc, không lấy lại được vì màn này không có lịch sử.\n"
     "- Hệ số giá bán dịch vụ: bắt buộc, phải lớn hơn 0, tối đa 999,99.\n"
     "- Định mức đàm phán giá (%): không bắt buộc, từ 0 đến 99.\n"
     "- Luôn có hộp xác nhận trước khi ghi, nêu rõ số gói và số cấp bị ảnh hưởng. "
     "Hệ thống cũ bấm Lưu là chạy luôn, không hỏi.\n"
     "- Sau khi lưu, muốn kiểm chứng phải sang màn Danh mục gói bảo dưỡng xem giá của gói cụ thể — "
     "màn này không hiện danh sách gói.\n"
     "- Lỗi nhập liệu chỉ hiện SAU lần bấm Lưu đầu tiên, không hiện ngay khi vừa gõ."),
]

# ============================================================================
PRE_PERM = ("Có sẵn 3 tài khoản: A được cấp quyền \"Cập nhật nhanh giá dịch vụ\" ở cổng mới; "
            "B được cấp quyền cùng tên ở cổng cũ; C không được cấp quyền này ở cả hai cổng. "
            "Hệ thống có khoảng 207 gói bảo dưỡng và 242 cấp dịch vụ. "
            "ĐÃ SAO LƯU toàn bộ giá của gói bảo dưỡng và cấp dịch vụ trước khi kiểm thử.")

ROLE_TCS = [
    ("01", "Vào màn hình khi có quyền cấp ở cổng mới", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → Cập nhật nhanh giá dịch vụ",
     "Tài khoản A",
     "- Vào được màn hình\n"
     "- Hai ô nhập hiện giá trị đang lưu\n- Có nút Lưu"),

    ("02", "Vào màn hình khi quyền chỉ được cấp ở cổng cũ", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản B (chỉ được cấp quyền ở cổng cũ)\n"
     "2. Mở phân hệ Chăm sóc khách hàng, tìm mục Cập nhật nhanh giá dịch vụ", "Tài khoản B",
     "- Mục menu HIỆN và vào được màn hình\n"
     "- Nút Lưu dùng được bình thường\n"
     "⚠️ Đây là bẫy lớn nhất của màn: nếu người được cấp quyền ở cổng cũ mà bị đá về trang "
     "không tìm thấy thì là lỗi phân quyền, phải báo ngay"),

    ("03", "Chặn vào màn hình khi không có quyền", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Tìm mục Cập nhật nhanh giá dịch vụ trong phân hệ Chăm sóc khách hàng\n"
     "3. Dán thẳng đường dẫn màn hình vào thanh địa chỉ", "Tài khoản C",
     "- Mục menu KHÔNG hiện\n"
     "- Dán thẳng đường dẫn thì chuyển sang trang báo không tìm thấy, "
     "không hiện giá trị thông số nào"),

    ("04", "Chặn Lưu khi bỏ qua giao diện", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản C, lấy mã đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Lưu cấu hình giá dịch vụ, bỏ qua giao diện\n"
     "3. Đăng nhập lại bằng tài khoản A, mở màn hình kiểm tra\n"
     "4. Sang màn Danh mục gói bảo dưỡng kiểm tra giá",
     "Hệ số: 5; Định mức: 10",
     "- Hệ thống từ chối, báo không có quyền\n"
     "- Hai ô trên màn hình giữ nguyên giá trị cũ\n"
     "- Giá của các gói bảo dưỡng KHÔNG bị đổi\n"
     "⚠️ Đây là phép thử quan trọng nhất về phân quyền: một lần lọt là đổi giá 207 gói"),

    ("05", "Chặn đọc cấu hình khi bỏ qua giao diện", "P1", PRE_PERM,
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy cấu hình giá dịch vụ", "Tài khoản C",
     "- Hệ thống từ chối, báo không có quyền, không trả về giá trị nào"),

    ("06", "Người có quyền lưu được và thấy kết quả", "P0", PRE_PERM,
     "1. Đăng nhập bằng tài khoản A\n2. Đổi Hệ số giá bán dịch vụ\n3. Bấm Lưu và xác nhận",
     "Hệ số: 1,5",
     "- Lưu thành công, có thông báo kết quả\n"
     "- Nạp lại màn hình thì ô Hệ số hiện giá trị mới"),
]

# ============================================================================
PRE = ("Đăng nhập bằng tài khoản có quyền \"Cập nhật nhanh giá dịch vụ\". "
       "Hệ thống có khoảng 207 gói bảo dưỡng và 242 cấp dịch vụ. "
       "Hệ số giá bán dịch vụ đang là 1,2 và Định mức đàm phán giá đang là 10. "
       "ĐÃ SAO LƯU toàn bộ giá của gói bảo dưỡng và cấp dịch vụ trước khi kiểm thử.")

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Mở màn hình lần đầu", "P0", PRE,
         "1. Vào phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → Cập nhật nhanh giá dịch vụ\n"
         "2. Quan sát toàn màn hình", "—",
         "- Màn hình là một khung nhập gọn ở giữa trang, KHÔNG có bảng danh sách, "
         "KHÔNG có bộ lọc\n"
         "- Có 2 ô: Hệ số giá bán dịch vụ (có dấu sao đỏ) và Định mức đàm phán giá (%) "
         "(không có dấu sao)\n"
         "- Cuối khung có nút Lưu"),

        ("002", "Hai ô hiện đúng giá trị đang lưu", "P0", PRE,
         "1. Mở màn hình\n2. Đọc giá trị trong hai ô", "—",
         "- Ô Hệ số giá bán dịch vụ hiện 1,2\n- Ô Định mức đàm phán giá hiện 10\n"
         "- Không ô nào để trống khi hệ thống đã có giá trị"),

        ("003", "Dòng ghi chú nêu số gói bị ảnh hưởng", "P0", PRE,
         "1. Mở màn hình\n2. Đọc dòng ghi chú dưới hai ô", "—",
         "- Dòng ghi chú nêu rõ số gói bảo dưỡng sẽ bị áp lại (khoảng 207)\n"
         "- Nêu rõ việc GHI ĐÈ giá trị đã chỉnh riêng ở từng gói\n"
         "- Con số này khớp với tổng số gói thực tế ở màn Danh mục gói bảo dưỡng"),

        ("004", "Dòng Cập nhật gần nhất", "P1", PRE,
         "1. Mở màn hình\n2. Đọc dòng \"Cập nhật gần nhất\"", "—",
         "- Hiện thời điểm lần thay đổi gần nhất\n"
         "- Sau khi lưu một lần rồi nạp lại màn, thời điểm này đổi theo"),

        ("005", "Mở màn hình khi hệ thống chưa từng đặt thông số", "P1",
         "Môi trường kiểm thử riêng, hệ thống chưa từng lưu thông số giá dịch vụ nào.",
         "1. Mở màn hình", "—",
         "- Màn hình mở bình thường, KHÔNG lỗi, không trắng trang\n"
         "- Hai ô để trống, sẵn sàng cho nhập lần đầu\n"
         "⚠️ Hệ thống cũ lỗi ở trường hợp này vì luôn giả định đã có sẵn thông số"),

        ("006", "Màn hình không treo lúc vừa mở", "P1", PRE,
         "1. Mở màn hình và quan sát trong 5 giây đầu", "—",
         "- Có dấu hiệu đang tải rồi hiện dữ liệu\n"
         "- Không lỗi, không đứng hình, không trắng trang"),

        ("007", "Số gói trong ghi chú cập nhật theo dữ liệu thực", "P1",
         PRE + " Vừa thêm 1 gói bảo dưỡng mới ở màn Danh mục gói bảo dưỡng.",
         "1. Thêm 1 gói bảo dưỡng mới\n2. Mở lại màn Cập nhật nhanh giá dịch vụ\n"
         "3. Đọc số gói trong dòng ghi chú", "—",
         "- Con số tăng thêm 1\n"
         "⚠️ Không được là con số cố định viết cứng trong màn hình"),
    ]),

    ("II", "RÀNG BUỘC NHẬP LIỆU", [
        ("001", "Bỏ trống Hệ số giá bán dịch vụ", "P0", PRE,
         "1. Xóa trắng ô Hệ số giá bán dịch vụ\n2. Bấm Lưu", "Hệ số: (để trống)",
         "- Ô Hệ số viền đỏ, hiện chữ đỏ \"Bắt buộc phải nhập\" ngay dưới ô\n"
         "- KHÔNG mở hộp xác nhận, không ghi gì cả"),

        ("002", "Bỏ trống Định mức đàm phán giá", "P0", PRE,
         "1. Xóa trắng ô Định mức đàm phán giá, giữ nguyên Hệ số\n2. Bấm Lưu và xác nhận",
         "Định mức: (để trống)",
         "- KHÔNG báo lỗi ở ô Định mức (ô này không bắt buộc)\n"
         "- Lưu thành công"),

        ("003", "Nhập Hệ số bằng 0", "P0", PRE,
         "1. Nhập Hệ số = 0\n2. Bấm Lưu", "Hệ số: 0",
         "- Ô Hệ số báo \"Phải lớn hơn 0\"\n- Không mở hộp xác nhận, không ghi gì"),

        ("004", "Nhập Hệ số âm", "P0", PRE,
         "1. Nhập Hệ số = -1\n2. Bấm Lưu", "Hệ số: -1",
         "- Ô Hệ số báo lỗi phải lớn hơn 0, không ghi gì"),

        ("005", "Nhập Hệ số bằng chữ", "P0", PRE,
         "1. Nhập Hệ số = \"abc\"\n2. Bấm Lưu", "Hệ số: abc",
         "- Ô Hệ số báo \"Phải là số\", không ghi gì"),

        ("006", "Nhập Hệ số vượt trần", "P0", PRE,
         "1. Nhập Hệ số = 1000\n2. Bấm Lưu", "Hệ số: 1000",
         "- Ô Hệ số báo \"Tối đa 999,99\", không ghi gì"),

        ("007", "Nhập Hệ số đúng sát trần", "P1", PRE,
         "1. Nhập Hệ số = 999,99\n2. Bấm Lưu và xác nhận", "Hệ số: 999,99",
         "- Lưu thành công\n"
         "- Nạp lại màn hình thì ô Hệ số hiện đúng 999,99\n"
         "⚠️ Sau kịch bản này phải khôi phục lại hệ số cũ ngay, vì giá 207 gói đã bị đổi"),

        ("008", "Nhập Hệ số có phần thập phân", "P0", PRE,
         "1. Nhập Hệ số = 1,25\n2. Bấm Lưu và xác nhận", "Hệ số: 1,25",
         "- Lưu thành công, giá trị lưu đúng 1,25 chứ không phải 125\n"
         "⚠️ Đây là bẫy thường gặp: hệ thống hiểu nhầm dấu phẩy thành dấu ngăn hàng nghìn"),

        ("009", "Nhập Định mức âm", "P0", PRE,
         "1. Nhập Định mức = -5\n2. Bấm Lưu", "Định mức: -5",
         "- Ô Định mức báo \"Không được nhỏ hơn 0\", không ghi gì"),

        ("010", "Nhập Định mức bằng 0", "P1", PRE,
         "1. Nhập Định mức = 0\n2. Bấm Lưu và xác nhận", "Định mức: 0",
         "- Lưu thành công (0 là giá trị hợp lệ)\n"
         "- Nạp lại màn hình thì ô Định mức hiện 0 chứ KHÔNG để trống\n"
         "⚠️ Bẫy: hệ thống nhầm số 0 với 'chưa nhập' rồi bỏ qua, không ghi xuống"),

        ("011", "Nhập Định mức vượt trần", "P0", PRE,
         "1. Nhập Định mức = 100\n2. Bấm Lưu", "Định mức: 100",
         "- Ô Định mức báo \"Tối đa 99\", không ghi gì"),

        ("012", "Nhập Định mức đúng sát trần", "P1", PRE,
         "1. Nhập Định mức = 99\n2. Bấm Lưu và xác nhận", "Định mức: 99",
         "- Lưu thành công, giá trị lưu đúng 99"),

        ("013", "Nhập Định mức bằng chữ", "P1", PRE,
         "1. Nhập Định mức = \"abc\"\n2. Bấm Lưu", "Định mức: abc",
         "- Ô Định mức báo \"Phải là số\", không ghi gì"),

        ("014", "Lỗi chỉ hiện sau lần bấm Lưu đầu tiên", "P1", PRE,
         "1. Mở màn hình mới\n2. Xóa trắng ô Hệ số\n3. Quan sát trước khi bấm Lưu\n4. Bấm Lưu",
         "Hệ số: (để trống)",
         "- Trước bước 4: ô KHÔNG viền đỏ, không hiện chữ lỗi\n"
         "- Sau bước 4: mới hiện viền đỏ và chữ lỗi\n"
         "⚠️ Đây là hành vi đúng theo thiết kế của hệ thống"),

        ("015", "Lỗi biến mất sau khi nhập lại đúng", "P1", PRE,
         "1. Xóa trắng ô Hệ số, bấm Lưu để hiện lỗi\n2. Nhập Hệ số = 1,3\n3. Bấm Lưu và xác nhận",
         "Hệ số: 1,3",
         "- Viền đỏ và chữ đỏ biến mất khi nhập\n- Lưu thành công"),

        ("016", "Cả hai ô cùng sai", "P1", PRE,
         "1. Nhập Hệ số = 0 và Định mức = 200\n2. Bấm Lưu", "Hệ số: 0; Định mức: 200",
         "- CẢ HAI ô cùng báo lỗi tương ứng\n- Không mở hộp xác nhận, không ghi gì"),
    ]),

    ("III", "HỘP XÁC NHẬN TRƯỚC KHI GHI", [
        ("001", "Bấm Lưu mở hộp xác nhận", "P0", PRE,
         "1. Nhập Hệ số = 1,5\n2. Bấm Lưu", "Hệ số: 1,5",
         "- Mở hộp xác nhận tiêu đề \"Xác nhận cập nhật giá dịch vụ\"\n"
         "- Có nút Hủy và nút Đồng ý\n"
         "⚠️ Bắt buộc phải có bước hỏi này. Hệ thống cũ bấm Lưu là chạy luôn — "
         "nếu bản mới cũng chạy luôn thì là lỗi nghiêm trọng"),

        ("002", "Nội dung hộp xác nhận nêu đủ mức ảnh hưởng", "P0", PRE,
         "1. Bấm Lưu\n2. Đọc kỹ toàn bộ nội dung hộp xác nhận", "Hệ số: 1,5",
         "- Nêu rõ SỐ GÓI BẢO DƯỠNG sẽ bị cập nhật (khoảng 207)\n"
         "- Nêu rõ việc GHI ĐÈ giá trị đã chỉnh riêng ở từng gói\n"
         "- Nêu rõ SỐ CẤP DỊCH VỤ sẽ được tính lại giá gốc (khoảng 242)\n"
         "- Kết bằng câu hỏi xác nhận"),

        ("003", "Bấm Hủy trong hộp xác nhận", "P0", PRE,
         "1. Nhập Hệ số = 2\n2. Bấm Lưu\n3. Bấm Hủy\n"
         "4. Sang màn Danh mục gói bảo dưỡng kiểm tra giá", "Hệ số: 2",
         "- Hộp đóng lại, KHÔNG ghi gì cả\n"
         "- Ô Hệ số vẫn hiện 2 (giá trị đang gõ dở, chưa lưu)\n"
         "- Giá của các gói bảo dưỡng KHÔNG bị đổi\n"
         "- Nạp lại màn hình thì ô Hệ số quay về 1,2"),

        ("004", "Bấm Đồng ý trong hộp xác nhận", "P0", PRE,
         "1. Nhập Hệ số = 1,5\n2. Bấm Lưu\n3. Bấm Đồng ý", "Hệ số: 1,5",
         "- Hộp đóng, hệ thống xử lý\n"
         "- Hiện thông báo kết quả nêu số gói đã cập nhật và số cấp đã tính lại giá"),

        ("005", "Số trong hộp xác nhận khớp dữ liệu thực", "P1", PRE,
         "1. Đếm số gói ở màn Danh mục gói bảo dưỡng\n"
         "2. Quay lại, bấm Lưu và đối chiếu con số trong hộp xác nhận", "—",
         "- Hai con số bằng nhau"),

        ("006", "Đóng hộp xác nhận bằng dấu X", "P1", PRE,
         "1. Bấm Lưu\n2. Bấm dấu X ở góc hộp xác nhận\n"
         "3. Kiểm tra giá của gói bảo dưỡng", "Hệ số: 2",
         "- Hành xử giống nút Hủy: không ghi gì cả"),
    ]),

    ("IV", "GHI DỮ LIỆU HÀNG LOẠT", [
        ("001", "Đổi hệ số áp cho toàn bộ gói bảo dưỡng", "P0",
         PRE + " Ghi lại trước hệ số hiện tại của 5 gói bảo dưỡng bất kỳ.",
         "1. Nhập Hệ số = 1,5\n2. Bấm Lưu và Đồng ý\n"
         "3. Sang màn Danh mục gói bảo dưỡng, mở lần lượt 5 gói đã ghi lại", "Hệ số: 1,5",
         "- Cả 5 gói đều có hệ số mới là 1,5\n"
         "- Thông báo kết quả nêu số gói đã cập nhật khớp với tổng số gói"),

        ("002", "Ghi đè cả gói đã chỉnh riêng", "P0",
         PRE + " Gói \"Gói A\" đã được chỉnh riêng hệ số thành 3,0 khác hẳn mặt bằng chung.",
         "1. Ghi lại hệ số riêng của Gói A là 3,0\n2. Về màn này, nhập Hệ số = 1,5\n"
         "3. Bấm Lưu và Đồng ý\n4. Mở lại Gói A", "Hệ số: 1,5",
         "- Gói A cũng bị đổi thành 1,5, giá trị riêng 3,0 KHÔNG được giữ lại\n"
         "⚠️ Đây là hành vi CÓ CHỦ Ý, giữ nguyên từ hệ thống cũ. Người dùng phải được cảnh báo "
         "qua hộp xác nhận trước khi bấm"),

        ("003", "Đổi định mức áp cho toàn bộ gói", "P0", PRE,
         "1. Ghi lại định mức của 5 gói bất kỳ\n2. Nhập Định mức = 15\n3. Bấm Lưu và Đồng ý\n"
         "4. Mở lại 5 gói đó", "Định mức: 15",
         "- Cả 5 gói đều có định mức mới là 15"),

        ("004", "Giá gốc cấp dịch vụ được tính lại khi hệ số đổi", "P0",
         PRE + " Ghi lại giá gốc của 5 cấp dịch vụ bất kỳ.",
         "1. Nhập Hệ số = 1,5 (khác giá trị cũ 1,2)\n2. Bấm Lưu và Đồng ý\n"
         "3. Mở lại 5 cấp dịch vụ đã ghi", "Hệ số: 1,2 → 1,5",
         "- Giá gốc của 5 cấp đều được tính lại theo hệ số mới\n"
         "- Thông báo kết quả nêu số cấp đã tính lại giá"),

        ("005", "Giá gốc KHÔNG bị tính lại khi hệ số không đổi", "P0",
         PRE + " Ghi lại giá gốc của 5 cấp dịch vụ bất kỳ.",
         "1. GIỮ NGUYÊN Hệ số = 1,2, chỉ đổi Định mức từ 10 sang 20\n2. Bấm Lưu và Đồng ý\n"
         "3. Mở lại 5 cấp dịch vụ đã ghi", "Hệ số không đổi; Định mức: 10 → 20",
         "- Giá gốc của 5 cấp GIỮ NGUYÊN, không bị tính lại\n"
         "- Định mức của các gói đã đổi thành 20\n"
         "⚠️ Quy tắc quan trọng: chỉ hệ số đổi mới kéo theo tính lại giá gốc"),

        ("006", "Gói không xác định được đơn giá công bị bỏ qua", "P0",
         "Có ít nhất 1 gói bảo dưỡng thuộc công ty chưa khai đơn giá công. "
         "Ghi lại giá gốc hiện tại của gói đó.",
         "1. Nhập Hệ số mới\n2. Bấm Lưu và Đồng ý\n3. Đọc kỹ thông báo kết quả\n"
         "4. Mở lại gói đó xem giá gốc", "Hệ số: 1,5",
         "- Thông báo kết quả nêu rõ có gói bị BỎ QUA và số lượng\n"
         "- Giá gốc của gói đó GIỮ NGUYÊN như trước, KHÔNG bị đưa về 0\n"
         "⚠️ Hệ thống cũ ghi giá gốc của gói này về 0 — tức là mất giá. "
         "Đây là trường hợp bắt buộc phải kiểm"),

        ("007", "Thông báo kết quả nêu đủ ba con số", "P0", PRE,
         "1. Nhập Hệ số mới\n2. Bấm Lưu và Đồng ý\n3. Đọc thông báo kết quả", "Hệ số: 1,6",
         "- Thông báo nêu số gói đã cập nhật, số cấp đã tính lại giá và số gói bị bỏ qua\n"
         "- Các con số này cộng lại phải hợp lý với tổng số gói hiện có"),

        ("008", "Giá trị mới còn nguyên sau khi nạp lại màn", "P0", PRE,
         "1. Nhập Hệ số = 1,5 và Định mức = 15\n2. Bấm Lưu và Đồng ý\n"
         "3. Nhấn F5 nạp lại trang", "Hệ số: 1,5; Định mức: 15",
         "- Hai ô hiện đúng 1,5 và 15\n- Dòng \"Cập nhật gần nhất\" đổi sang thời điểm vừa lưu"),

        ("009", "Lưu lại đúng giá trị đang có", "P1", PRE,
         "1. Không đổi gì\n2. Bấm Lưu và Đồng ý\n3. Kiểm tra giá của 5 gói bảo dưỡng",
         "Giữ nguyên Hệ số 1,2 và Định mức 10",
         "- Lưu thành công, không lỗi\n"
         "- Các gói bị áp lại đúng giá trị cũ nên nhìn như không đổi\n"
         "- Giá gốc cấp dịch vụ KHÔNG bị tính lại vì hệ số không đổi"),

        ("010", "Thời gian xử lý với 207 gói", "P0", PRE,
         "1. Nhập Hệ số mới\n2. Bấm Lưu và Đồng ý, bấm giờ", "Hệ số: 1,5",
         "- Hoàn tất trong vài giây, không treo trang, không báo hết thời gian chờ\n"
         "- Nút Lưu chuyển sang trạng thái \"Đang lưu...\" và không bấm lại được trong lúc xử lý"),

        ("011", "Chống bấm Lưu nhiều lần liên tiếp", "P0", PRE,
         "1. Nhập Hệ số mới\n2. Bấm Lưu và Đồng ý\n"
         "3. Trong lúc đang xử lý, thử bấm Lưu tiếp", "Hệ số: 1,5",
         "- Nút Lưu bị vô hiệu, không chạy được lượt ghi thứ hai\n"
         "- Kết quả cuối vẫn đúng, không có gói nào bị áp hai lần sai lệch"),

        ("012", "Đổi thông số ảnh hưởng tới báo giá dịch vụ mới", "P0", PRE,
         "1. Đổi Hệ số thành 1,5 và Lưu\n"
         "2. Lập một báo giá dịch vụ mới, chọn một gói bảo dưỡng", "Hệ số: 1,5",
         "- Giá dịch vụ trên báo giá mới tính theo hệ số 1,5"),

        ("013", "Báo giá cũ không bị đổi giá theo", "P0",
         PRE + " Có sẵn 1 báo giá dịch vụ đã lập trước đó với hệ số 1,2.",
         "1. Ghi lại tổng tiền của báo giá cũ\n2. Đổi Hệ số thành 1,5 và Lưu\n"
         "3. Mở lại báo giá cũ", "Hệ số: 1,2 → 1,5",
         "- Tổng tiền của báo giá CŨ giữ nguyên\n"
         "⚠️ Thông số này chỉ áp cho việc lập chứng từ MỚI, không được sửa ngược chứng từ đã lập"),

        ("014", "Khôi phục lại giá trị ban đầu sau kiểm thử", "P0",
         PRE + " Đã chạy xong các kịch bản ghi dữ liệu ở trên.",
         "1. Nhập lại Hệ số = 1,2 và Định mức = 10 (giá trị gốc)\n2. Bấm Lưu và Đồng ý\n"
         "3. Đối chiếu giá của 5 gói với bản sao lưu ban đầu", "Hệ số: 1,2; Định mức: 10",
         "- Giá của các gói trở về đúng như bản sao lưu\n"
         "⚠️ BẮT BUỘC chạy bước này sau khi kiểm thử xong, nếu không toàn bộ giá dịch vụ "
         "trên môi trường kiểm thử sẽ sai"),
    ]),

    ("V", "CẢNH BÁO CHƯA LƯU & THAO TÁC ĐỒNG THỜI", [
        ("001", "Cảnh báo khi rời màn lúc đang sửa dở", "P0", PRE,
         "1. Đổi Hệ số thành 2 nhưng KHÔNG bấm Lưu\n2. Bấm sang màn khác",
         "Hệ số: 2 (chưa lưu)",
         "- Hệ thống cảnh báo dữ liệu chưa lưu và hỏi xác nhận\n"
         "- Chọn ở lại thì màn vẫn giữ nguyên giá trị đang gõ\n"
         "- Chọn thoát thì giá trị cũ không bị đổi"),

        ("002", "Rời màn khi chưa sửa gì", "P1", PRE,
         "1. Mở màn hình\n2. Không đổi gì\n3. Bấm sang màn khác", "—",
         "- Chuyển màn ngay, KHÔNG hỏi lại"),

        ("003", "Không còn cảnh báo sau khi đã lưu", "P1", PRE,
         "1. Đổi Hệ số\n2. Bấm Lưu và Đồng ý\n3. Bấm sang màn khác ngay sau đó", "Hệ số: 1,5",
         "- Chuyển màn ngay, KHÔNG hỏi lại vì dữ liệu đã được lưu"),

        ("004", "Đóng tab trình duyệt lúc đang sửa dở", "P2", PRE,
         "1. Đổi Hệ số nhưng chưa Lưu\n2. Đóng tab trình duyệt", "Hệ số: 2 (chưa lưu)",
         "- Trình duyệt hỏi xác nhận trước khi đóng\n"
         "- Nếu vẫn đóng thì giá trị cũ không bị đổi"),

        ("005", "Hai người cùng lưu thông số", "P1",
         "Hai tài khoản đều có quyền, cùng mở màn hình.",
         "1. Người 1 nhập Hệ số = 1,5 và Lưu\n2. Người 2 (đang mở màn với giá trị cũ) "
         "nhập Hệ số = 2 và Lưu\n3. Cả hai nạp lại màn hình", "Người 1: 1,5; Người 2: 2",
         "- Cả hai lưu được\n- Giá trị cuối là 2 (của người lưu sau)\n"
         "- Các gói bảo dưỡng đều mang hệ số 2, không có gói nào còn 1,5\n"
         "⚠️ Không được xảy ra tình trạng nửa số gói mang 1,5, nửa mang 2"),

        ("006", "Lưu trong lúc người khác đang thêm gói bảo dưỡng", "P1",
         "Hai người cùng thao tác.",
         "1. Người 1 mở màn Cập nhật nhanh giá dịch vụ\n"
         "2. Người 2 thêm 1 gói bảo dưỡng mới\n3. Người 1 bấm Lưu và Đồng ý\n"
         "4. Mở gói vừa thêm", "Hệ số: 1,5",
         "- Gói mới cũng được áp hệ số 1,5\n"
         "- Số gói trong thông báo kết quả đã tính cả gói mới"),

        ("007", "Nhất quán giữa hai cổng", "P1", PRE,
         "1. Đổi Hệ số thành 1,5 ở cổng mới và Lưu\n"
         "2. Mở màn tương ứng ở cổng cũ và đọc giá trị", "Hệ số: 1,5",
         "- Cổng cũ hiện đúng 1,5\n"
         "⚠️ Hai cổng dùng chung một bộ thông số, mọi sai lệch đều là lỗi"),

        ("008", "Luồng xuyên suốt đầy đủ", "P0", PRE,
         "1. Sao lưu giá của 5 gói và 5 cấp dịch vụ\n2. Đổi Hệ số và Định mức, bấm Lưu, bấm Hủy\n"
         "3. Kiểm tra giá chưa đổi\n4. Bấm Lưu lại, bấm Đồng ý\n"
         "5. Kiểm tra giá 5 gói và 5 cấp đã đổi đúng\n"
         "6. Lập một báo giá dịch vụ mới và kiểm giá\n"
         "7. Khôi phục giá trị gốc và Lưu lại\n8. Đối chiếu với bản sao lưu",
         "Hệ số 1,2 → 1,5 → 1,2; Định mức 10 → 15 → 10",
         "- Bước 3: giá chưa đổi\n- Bước 5: giá đổi đúng theo hệ số mới\n"
         "- Bước 6: báo giá mới dùng hệ số mới\n"
         "- Bước 8: mọi giá trị trở về đúng bản sao lưu ban đầu"),
    ]),
]

build(output_file=OUTPUT_FILE, sheet_name=SHEET_NAME, feature_name=FEATURE_NAME,
      module_name=MODULE_NAME, description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS, sections=SECTIONS)
