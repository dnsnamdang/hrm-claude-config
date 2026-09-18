# -*- coding: utf-8 -*-
"""Sinh file testcase BO SUNG cho Redmine #11286 — popup chon hang hoa theo cong ty.

Chay: python .plans/popup-hang-hoa-theo-cong-ty/gen_testcase.py
Output: .plans/popup-hang-hoa-theo-cong-ty/testcase-11286.xlsx
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- 9 muc mo ta
DESCRIPTION_BLOCK = [
    ("1 Mục đích tính năng",
     "Kiểm thử phần BỔ SUNG của yêu cầu #11286 cho cửa sổ \"Chọn hàng hoá\" ở 3 nơi: "
     "Quản lý dự án TKT → Quản lý Báo giá → Tạo/Sửa → nút Thêm hàng hoá; "
     "Quản lý dự án TKT → Quản lý Bomlist → Tạo/Sửa → nút Thêm hàng hoá; "
     "và hệ thống ERP → Kinh doanh → Báo giá → Tạo/Sửa → cửa sổ Chọn hàng hoá.\n"
     "4 nội dung được bổ sung: (1) cột \"Nguồn hàng\" cho biết hàng thuộc công ty/chi nhánh nào; "
     "(2) hai cột \"Lĩnh vực\" và \"Chương\" đứng cạnh cột \"Loại hàng hóa\" sẵn có; "
     "(3) ô lọc \"Công ty\" để thu hẹp danh sách theo công ty sở hữu hàng; "
     "(4) giá bán hiển thị và giá được chốt khi lưu đều là giá riêng của công ty ghi trên báo giá / bom "
     "(mỗi mặt hàng chỉ một mức giá duy nhất, không hiện giá của công ty khác)."),

    ("2. Đối tượng được tính / hiển thị",
     "► Cửa sổ Chọn hàng hoá liệt kê hàng hoá đang ở trạng thái Đang kinh doanh của hệ thống ERP.\n"
     "► Cột \"Nguồn hàng\" hiện MÃ NGẮN công ty sở hữu hàng (TPE, TPSG, TPHP, TPV…); rê chuột lên ô "
     "hiện tên công ty đầy đủ.\n"
     "► Cột \"Lĩnh vực\", \"Chương\" lấy theo nhóm hàng của mặt hàng; một nhóm có nhiều phân loại thì "
     "hiện ĐỦ, mỗi giá trị một dòng trong cùng ô.\n"
     "► Ô lọc \"Công ty\" liệt kê TOÀN BỘ công ty trong hệ thống (hiện có 7: TPE, TPHP, TPV, TPSG, TPA, "
     "UPS, ETEK GREEN), kể cả công ty chưa có mặt hàng nào.\n"
     "► Giá bán hiển thị ở cột \"Giá niêm yết\" = giá của bảng giá đang chọn trên báo giá × hệ số riêng "
     "của công ty ghi trên báo giá, làm tròn tới hàng nghìn."),

    ("3. Đối tượng bị ẩn / không tính",
     "► Không hiện giá bán của các công ty khác — mỗi mặt hàng chỉ một dòng, một mức giá.\n"
     "► Hàng hoá thuộc nhóm chưa được phân loại (hiện có 496 mặt hàng): hai ô Lĩnh vực / Chương ĐỂ TRỐNG, "
     "không hiện chữ thay thế, không hiện dấu gạch.\n"
     "► Hàng hoá không ghi công ty sở hữu: ô Nguồn hàng để trống và không xuất hiện khi lọc theo bất kỳ "
     "công ty nào.\n"
     "► Ba thông tin mới (Nguồn hàng, Lĩnh vực, Chương) CHỈ hiển thị trong cửa sổ chọn hàng — không được "
     "ghi vào dòng hàng của báo giá / bom, không lên bản in, không có trong file Excel xuất ra.\n"
     "► Giá vốn (Đơn giá nhập) KHÔNG nhân hệ số công ty và chỉ hiện với người có quyền \"Xem giá vốn hàng hoá\"."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng. Yêu cầu này không có bộ lọc theo thời gian; các ô lọc mới là lọc theo công ty nguồn hàng."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "► Thứ tự cột trong cửa sổ Chọn hàng hoá của Báo giá: Chọn · Ảnh · Loại hàng hóa · Tên hàng hoá · "
     "Lĩnh vực · Chương · Model · Mã hàng · Nguồn hàng · Giá niêm yết · Bảo hành · VAT(%) · Định mức đàm phán giá (%) · "
     "SL tồn có thể bán · SL KM có thể xuất · SL có thể LR · Ghi chú · Tính chất hàng hóa · Nguồn.\n"
     "► Thứ tự cột trong cửa sổ Chọn hàng hoá của Bomlist: Chọn · Mã · Tên hàng hoá · Loại hàng hóa · "
     "Lĩnh vực · Chương · Model · Thương hiệu · Xuất xứ · ĐVT · Nguồn hàng · Số lượng · Nguồn.\n"
     "► Hai cột Lĩnh vực và Chương LUÔN đứng liền nhau và đứng ngay trước cột Model ở cả ba cửa sổ.\n"
     "► Một mặt hàng thuộc nhóm có nhiều phân loại → trong một ô có nhiều dòng, dòng Lĩnh vực thứ n "
     "tương ứng dòng Chương thứ n."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "► Nhiều phân loại của cùng một nhóm hàng được gộp vào một ô, bỏ giá trị trùng, mỗi giá trị một dòng "
     "— KHÔNG nhân bản mặt hàng thành nhiều dòng trong danh sách.\n"
     "► Số dòng hiển thị và tổng số bản ghi ở chân cửa sổ phải bằng nhau trước và sau khi bổ sung 3 cột mới "
     "(cùng điều kiện lọc)."),

    ("7. Phân quyền cấp",
     "• \"Xây dựng giá bán theo công ty\" — tạo/sửa báo giá khi dự án không triển khai theo phòng.\n"
     "• \"Xây dựng giá bán theo phòng\" — tạo/sửa báo giá của dự án triển khai theo phòng.\n"
     "• \"Xem giá vốn hàng hoá\" — nhìn thấy Đơn giá nhập trong cửa sổ chọn hàng và trên lưới hàng hoá.\n"
     "• \"Tạo BOM List\" — tạo/sửa bom, mở cửa sổ chọn hàng hoá của bom.\n"
     "• Các quyền xem danh sách theo cấp (\"Xem tất cả danh sách Báo giá\", \"… theo công ty\", \"… theo phòng ban\", "
     "\"… theo bộ phận\", \"Xem danh sách BOM List theo công ty/phòng ban/bộ phận/tổng công ty\") không đổi trong "
     "yêu cầu này nhưng phải kiểm tra lại là không bị ảnh hưởng."),

    ("8. Cách tính các ô thống kê",
     "► Ô \"Giá niêm yết\" trong cửa sổ chọn hàng = giá của mặt hàng theo Bảng giá đang chọn trên báo giá, "
     "nhân hệ số riêng của công ty ghi trên báo giá, rồi làm tròn tới hàng nghìn.\n"
     "  Ví dụ đã đo trên dữ liệu thật: mặt hàng ENEO.700-V5029 giá theo bảng Bán lẻ là 1.265.000; công ty có "
     "hệ số 1,04 → hiển thị 1.316.000 (1.265.000 × 1,04 = 1.315.600, làm tròn nghìn).\n"
     "► Mặt hàng KHÔNG được cấu hình hệ số cho công ty đó → giữ nguyên giá gốc của bảng giá (không để trống, "
     "không bằng 0).\n"
     "► \"Đơn giá bán\" của dòng hàng sau khi thêm vào lưới, và số được lưu lại sau khi bấm Lưu, phải BẰNG ĐÚNG "
     "số đã hiện ở cột Giá niêm yết lúc chọn.\n"
     "► \"Đơn giá nhập\" (giá vốn) KHÔNG nhân hệ số — luôn là giá vốn gốc của mặt hàng."),

    ("9. Ghi chú đọc bảng",
     "► BẪY 1 — lọc công ty KHÔNG được đổi giá: ô lọc \"Công ty\" chỉ thu hẹp danh sách theo công ty SỞ HỮU hàng. "
     "Chọn hàng nguồn Sài Gòn khi đang lập báo giá cho công ty TPE thì giá vẫn là giá của TPE.\n"
     "► BẪY 2 — căn cứ tính giá là công ty GHI TRÊN BÁO GIÁ / BOM, không phải công ty của người đang đăng nhập. "
     "Người công ty khác mở báo giá cũ ra sửa rồi lưu thì đơn giá các dòng hàng phải GIỮ NGUYÊN.\n"
     "► BẪY 3 — ô đơn giá của hàng lấy từ hệ thống ERP bị khoá, người dùng không sửa tay được; nên sai giá sẽ "
     "âm thầm, phải đối chiếu số trước–sau khi lưu bằng mắt ở từng dòng.\n"
     "► BẪY 4 — cùng một mặt hàng phải ra CÙNG một số ở cả 3 nơi: cửa sổ chọn hàng của Báo giá, cửa sổ chọn hàng "
     "của Bom, và số được lưu xuống sau khi bấm Lưu.\n"
     "► BẪY 5 — dữ liệu báo giá cũ trên môi trường kiểm thử bị lệch mã hàng (867/1.074 dòng trỏ sang mặt hàng khác). "
     "Khi test yêu cầu này phải TẠO BÁO GIÁ MỚI, không mở báo giá cũ ra lưu lại.\n"
     "► Giá hiển thị luôn có dấu ngăn cách hàng nghìn; làm tròn tới nghìn nên 3 chữ số cuối luôn là 000."),
]

# ---------------------------------------------------------------- phan quyen
ROLE_TCS = [
    ("01", "Người có quyền \"Xây dựng giá bán theo công ty\" mở cửa sổ chọn hàng của Báo giá", "P0",
     "Tài khoản A có quyền \"Xây dựng giá bán theo công ty\", thuộc công ty TPE; dự án D1 không triển khai theo phòng",
     "1. Đăng nhập tài khoản A\n2. Vào Quản lý dự án TKT → Quản lý Báo giá → Tạo báo giá cho dự án D1\n"
     "3. Bấm nút Thêm hàng hoá để mở cửa sổ Chọn hàng hoá\n4. Quan sát các cột và ô lọc",
     "Tài khoản A / dự án D1",
     "- Cửa sổ Chọn hàng hoá mở được\n- Có đủ 3 cột mới: Nguồn hàng, Lĩnh vực, Chương\n"
     "- Trong khối Tìm kiếm nâng cao có ô lọc \"Công ty (nguồn hàng)\"\n- Cột Giá niêm yết có số, không ô nào để trống"),

    ("02", "Người có quyền \"Xây dựng giá bán theo phòng\" mở cửa sổ chọn hàng", "P1",
     "Tài khoản B chỉ có quyền \"Xây dựng giá bán theo phòng\", thuộc phòng Kỹ thuật; dự án D2 triển khai theo phòng Kỹ thuật",
     "1. Đăng nhập tài khoản B\n2. Tạo báo giá cho dự án D2\n3. Mở cửa sổ Chọn hàng hoá\n4. Chọn 1 mặt hàng",
     "Tài khoản B / dự án D2",
     "- Mở được cửa sổ, đủ 3 cột mới và ô lọc Công ty\n- Thêm được hàng vào lưới; đơn giá bằng đúng Giá niêm yết đã hiện"),

    ("03", "Người KHÔNG có quyền xây dựng giá không mở được cửa sổ chọn hàng", "P0",
     "Tài khoản C không có quyền \"Xây dựng giá bán theo công ty\" lẫn \"Xây dựng giá bán theo phòng\"",
     "1. Đăng nhập tài khoản C\n2. Vào Quản lý Báo giá\n3. Thử mở màn Tạo báo giá",
     "Tài khoản C",
     "- Hệ thống từ chối vào màn tạo báo giá, báo không có quyền\n- Không có đường nào mở được cửa sổ Chọn hàng hoá\n"
     "- ⚠️ Không được để lộ giá bán riêng của công ty qua màn này"),

    ("04", "Người không có quyền \"Xem giá vốn hàng hoá\" không thấy Đơn giá nhập", "P0",
     "Tài khoản D có quyền tạo báo giá nhưng KHÔNG có quyền \"Xem giá vốn hàng hoá\"",
     "1. Đăng nhập tài khoản D\n2. Tạo báo giá mới, mở cửa sổ Chọn hàng hoá\n3. Chọn 1 mặt hàng, thêm vào lưới\n"
     "4. Quan sát các cột giá trong cửa sổ và trên lưới hàng hoá",
     "Tài khoản D / mặt hàng ENEO.700-V5029",
     "- Cửa sổ chọn hàng vẫn hiện Giá niêm yết (giá bán) bình thường\n"
     "- Không hiện Đơn giá nhập / Thành tiền nhập / Tỷ suất lợi nhuận ở dòng vừa thêm\n"
     "- ⚠️ Kể cả khi lọc theo công ty khác cũng không có chỗ nào lộ giá vốn"),

    ("05", "Người có quyền \"Tạo BOM List\" mở cửa sổ chọn hàng của Bom", "P0",
     "Tài khoản E có quyền \"Tạo BOM List\", thuộc công ty TPSG",
     "1. Đăng nhập tài khoản E\n2. Vào Quản lý dự án TKT → Quản lý Bomlist → Tạo bom\n"
     "3. Bấm Thêm hàng hoá\n4. Quan sát cột và ô lọc",
     "Tài khoản E",
     "- Cửa sổ mở được, có cột Loại hàng hóa, Lĩnh vực, Chương, Nguồn hàng và ô \"Lọc công ty\""),

    ("06", "Gọi thẳng chức năng tìm hàng, bỏ qua giao diện, bằng tài khoản không có quyền", "P1",
     "Tài khoản C (không có quyền xây dựng giá) đã đăng nhập; dùng công cụ kiểm thử gọi thẳng chức năng "
     "Tìm hàng hoá của cửa sổ chọn hàng",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Tìm hàng hoá của cửa sổ Chọn hàng hoá\n"
     "2. Gửi kèm điều kiện lọc theo công ty Sài Gòn\n3. Xem dữ liệu trả về",
     "Tài khoản C / lọc công ty Sài Gòn",
     "- Hệ thống từ chối hoặc không trả giá vốn\n- ⚠️ Không bao giờ được trả nhiều mức giá của nhiều công ty cho cùng một mặt hàng\n"
     "- Dành cho tester kỹ thuật"),
]

# ---------------------------------------------------------------- sections
S1 = [
    (1, "Cửa sổ chọn hàng của Báo giá có đủ 3 cột mới", "P0",
     "Tài khoản A (công ty TPE) có quyền tạo báo giá; dữ liệu ERP có 23.435 mặt hàng nguồn TPE và 495 mặt hàng nguồn Sài Gòn",
     "1. Tạo báo giá mới cho dự án D1\n2. Bấm Thêm hàng hoá\n3. Kéo ngang bảng kết quả xem hết các cột",
     "—",
     "- Có cột \"Nguồn hàng\", \"Lĩnh vực\", \"Chương\"\n- Cột \"Loại hàng hóa\" cũ vẫn còn, nội dung không đổi\n"
     "- Tiêu đề cột hiện đủ chữ, không bị cắt mất chữ"),

    (2, "Thứ tự cột đúng yêu cầu", "P0",
     "Như trên",
     "1. Mở cửa sổ Chọn hàng hoá\n2. Đọc lần lượt tiêu đề các cột từ trái sang phải",
     "—",
     "- Thứ tự: Chọn · Ảnh · Loại hàng hóa · Tên hàng hoá · Lĩnh vực · Chương · Model · Mã hàng · Nguồn hàng · Giá niêm yết · …\n"
     "- ⚠️ Lĩnh vực và Chương phải đứng liền nhau và ngay TRƯỚC cột Model"),

    (3, "Cột Nguồn hàng hiện mã công ty đúng với mặt hàng", "P0",
     "Mặt hàng H1 thuộc công ty TPE; mặt hàng H2 thuộc công ty Sài Gòn (mã TPSG)",
     "1. Mở cửa sổ Chọn hàng hoá\n2. Gõ mã H1 vào ô \"Nhập tên, mã hoặc model hàng hoá...\", bấm Tìm kiếm\n"
     "3. Đọc ô Nguồn hàng\n4. Làm lại với H2",
     "H1 (nguồn TPE) / H2 (nguồn TPSG)",
     "- Dòng H1 hiện TPE, dòng H2 hiện TPSG\n- Mã hiện là mã ngắn, không hiện tên công ty dài làm vỡ cột"),

    (4, "Rê chuột lên ô Nguồn hàng hiện tên công ty đầy đủ", "P1",
     "Mặt hàng H1 nguồn TPE",
     "1. Tìm mặt hàng H1\n2. Rê chuột và giữ trên ô Nguồn hàng khoảng 2 giây",
     "H1",
     "- Hiện chú thích với tên công ty đầy đủ (ví dụ CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT)"),

    (5, "Cột Lĩnh vực và Chương có dữ liệu đúng theo mặt hàng", "P0",
     "Mặt hàng H3 thuộc nhóm hàng đã được phân loại 1 Lĩnh vực và 1 Chương",
     "1. Tìm mặt hàng H3\n2. Đọc ô Lĩnh vực và ô Chương\n3. Đối chiếu với phân loại của nhóm hàng H3 trong hệ thống ERP",
     "H3",
     "- Lĩnh vực và Chương hiện đúng tên như phân loại nhóm hàng của mặt hàng đó\n- Chữ xuống dòng đầy đủ, không bị cắt cụt"),

    (6, "Mặt hàng có nhiều phân loại — gộp nhiều dòng trong một ô", "P0",
     "Mặt hàng H4 thuộc nhóm hàng có 2 dòng phân loại trở lên (hiện có 68 nhóm như vậy)",
     "1. Tìm mặt hàng H4\n2. Đếm số dòng trong ô Lĩnh vực và ô Chương\n3. Đếm số dòng của mặt hàng H4 trong danh sách",
     "H4",
     "- Ô Lĩnh vực hiện đủ các giá trị, mỗi giá trị một dòng; ô Chương cũng vậy\n"
     "- ⚠️ Mặt hàng H4 vẫn chỉ xuất hiện MỘT dòng trong danh sách, không bị nhân thành nhiều dòng"),

    (7, "Giá trị phân loại trùng nhau chỉ hiện một lần", "P1",
     "Mặt hàng H5 thuộc nhóm có 2 dòng phân loại cùng Lĩnh vực nhưng khác Chương",
     "1. Tìm mặt hàng H5\n2. Đọc ô Lĩnh vực",
     "H5",
     "- Lĩnh vực chỉ hiện một lần, không lặp lại hai dòng giống hệt nhau\n- Ô Chương vẫn hiện đủ 2 giá trị khác nhau"),

    (8, "Mặt hàng thuộc nhóm chưa phân loại — hai ô để trống", "P0",
     "Mặt hàng H6 thuộc nhóm hàng chưa được phân loại (hiện có 496 mặt hàng như vậy)",
     "1. Tìm mặt hàng H6\n2. Đọc ô Lĩnh vực và ô Chương",
     "H6",
     "- Hai ô ĐỂ TRỐNG hoàn toàn\n- ⚠️ Không hiện dấu gạch ngang, không hiện chữ \"không xác định\", không hiện ô viền lạ\n"
     "- Các cột còn lại của dòng vẫn đầy đủ"),

    (9, "Mặt hàng không ghi công ty sở hữu", "P1",
     "Chuẩn bị 1 mặt hàng H7 chưa gán công ty trong hệ thống ERP (nếu dữ liệu không có thì ghi Không kiểm được vào Kết quả thực tế)",
     "1. Tìm mặt hàng H7\n2. Đọc ô Nguồn hàng",
     "H7",
     "- Ô Nguồn hàng để trống, không hiện dấu lạ\n- Dòng vẫn hiện bình thường, giá vẫn có"),

    (10, "Ba cột mới hiển thị đúng khi mở lại cửa sổ nhiều lần", "P1",
     "Tài khoản A đang ở màn tạo báo giá",
     "1. Mở cửa sổ Chọn hàng hoá\n2. Đóng cửa sổ bằng nút X\n3. Mở lại cửa sổ\n4. Quan sát 3 cột mới và ô lọc Công ty",
     "—",
     "- Lần mở thứ hai vẫn đủ 3 cột và ô lọc\n- Ô lọc Công ty trở về \"Tất cả\", không giữ lựa chọn cũ"),

    (11, "Ba cột mới hiển thị ở màn Sửa báo giá", "P0",
     "Báo giá BG-01 ở trạng thái Đang tạo, do tài khoản A lập",
     "1. Mở BG-01 ở chế độ Sửa\n2. Bấm Thêm hàng hoá\n3. Quan sát 3 cột mới",
     "BG-01",
     "- Đủ 3 cột mới và ô lọc Công ty như ở màn Tạo mới"),

    (12, "Chuyển trang danh sách vẫn giữ đúng 3 cột", "P1",
     "Kết quả tìm kiếm có nhiều hơn 20 dòng",
     "1. Mở cửa sổ Chọn hàng hoá, để trống ô tìm kiếm\n2. Sang trang 2, trang 3\n3. Quan sát các cột mới",
     "—",
     "- Mỗi trang đều hiện đủ Nguồn hàng / Lĩnh vực / Chương, dữ liệu khớp từng dòng\n"
     "- Tổng số bản ghi ở chân cửa sổ không đổi so với trước khi bổ sung cột"),

    (13, "Cột Lĩnh vực / Chương có tên rất dài", "P1",
     "Chọn mặt hàng H8 có tên Lĩnh vực dài khoảng 60 ký tự",
     "1. Tìm mặt hàng H8\n2. Quan sát ô Lĩnh vực",
     "H8",
     "- Chữ tự xuống dòng trong ô, đọc được hết\n- Không đẩy vỡ bảng, không che mất cột Model bên cạnh"),
]

S2 = [
    (1, "Ô lọc Công ty nằm đúng chỗ và liệt kê đủ công ty", "P0",
     "Hệ thống có 7 công ty: TPE, TPHP, TPV, TPSG, TPA, UPS, ETEK GREEN",
     "1. Mở cửa sổ Chọn hàng hoá\n2. Bấm \"Tìm kiếm nâng cao\" để mở khối lọc\n"
     "3. Bấm vào ô \"Công ty (nguồn hàng)\"\n4. Đếm và đọc các dòng trong danh sách",
     "—",
     "- Ô lọc nằm trong khối Tìm kiếm nâng cao\n- Danh sách có đủ 7 công ty, mỗi dòng dạng \"mã - tên công ty\"\n"
     "- ⚠️ Có cả công ty chưa có mặt hàng nào (yêu cầu của người dùng là hiện toàn bộ công ty)"),

    (2, "Lọc theo công ty Sài Gòn", "P0",
     "Dữ liệu: 495 mặt hàng nguồn Sài Gòn, 23.435 mặt hàng nguồn TPE",
     "1. Mở cửa sổ Chọn hàng hoá\n2. Mở Tìm kiếm nâng cao, chọn Công ty = Sài Gòn\n3. Bấm Tìm kiếm\n"
     "4. Đọc tổng số bản ghi ở chân cửa sổ\n5. Kiểm tra cột Nguồn hàng của các dòng đang hiện",
     "Công ty: Sài Gòn",
     "- Tổng số bản ghi đúng bằng số mặt hàng nguồn Sài Gòn (495 với dữ liệu hiện tại)\n"
     "- MỌI dòng đều có Nguồn hàng là TPSG, không lẫn dòng TPE"),

    (3, "Lọc theo công ty TPE", "P0",
     "Như trên",
     "1. Chọn Công ty = TPE\n2. Bấm Tìm kiếm\n3. Kiểm tra cột Nguồn hàng vài trang đầu",
     "Công ty: TPE",
     "- Chỉ còn dòng có Nguồn hàng TPE\n- Tổng số bản ghi cộng với kết quả lọc Sài Gòn bằng tổng khi không lọc"),

    (4, "⚠️ Lọc công ty KHÔNG làm đổi giá", "P0",
     "Tài khoản A thuộc công ty TPE, đang tạo báo giá cho công ty TPE. Mặt hàng ENEO.700-V5029 nguồn TPE, "
     "giá theo bảng Bán lẻ là 1.265.000",
     "1. Tìm mặt hàng ENEO.700-V5029 khi chưa lọc công ty, ghi lại Giá niêm yết\n"
     "2. Chọn Công ty = TPE, tìm lại mặt hàng đó, ghi lại Giá niêm yết\n"
     "3. Chọn Công ty = Sài Gòn rồi bỏ lọc, tìm lại lần nữa",
     "ENEO.700-V5029",
     "- Giá niêm yết của mặt hàng KHÔNG đổi qua cả 3 lần\n"
     "- ⚠️ Đây là bẫy chính của yêu cầu: ô lọc công ty chỉ thu hẹp danh sách, tuyệt đối không đổi giá"),

    (5, "Chọn công ty chưa có mặt hàng nào", "P1",
     "Công ty ETEK GREEN chưa có mặt hàng nào trong hệ thống ERP",
     "1. Chọn Công ty = ETEK GREEN\n2. Bấm Tìm kiếm",
     "Công ty: ETEK GREEN",
     "- Danh sách rỗng, hiện dòng thông báo không có dữ liệu\n- Không báo lỗi, không quay vòng tải mãi\n"
     "- Bỏ lọc thì danh sách trở lại bình thường"),

    (6, "Lọc công ty kết hợp với ô tìm theo tên / mã", "P0",
     "Mặt hàng H1 nguồn TPE, mặt hàng H2 nguồn Sài Gòn, hai mặt hàng có tên gần giống nhau",
     "1. Gõ từ khoá chung của H1 và H2 vào ô tìm nhanh, bấm Tìm kiếm — ghi lại số dòng\n"
     "2. Thêm điều kiện Công ty = Sài Gòn, bấm Tìm kiếm",
     "Từ khoá chung / Công ty: Sài Gòn",
     "- Bước 1 ra cả H1 và H2\n- Bước 2 chỉ còn H2\n- Hai điều kiện được áp đồng thời, không điều kiện nào bị bỏ"),

    (7, "Lọc công ty kết hợp với lọc Lĩnh vực và Chương", "P1",
     "Có ít nhất 3 mặt hàng nguồn Sài Gòn thuộc cùng một Lĩnh vực",
     "1. Chọn Lĩnh vực L1, bấm Tìm kiếm, ghi số dòng\n2. Chọn thêm Công ty = Sài Gòn, bấm Tìm kiếm",
     "Lĩnh vực L1 / Công ty Sài Gòn",
     "- Kết quả bước 2 là tập con của bước 1\n- Mọi dòng đều thoả cả hai điều kiện"),

    (8, "Nút Làm mới xoá luôn ô lọc Công ty", "P0",
     "Đang lọc Công ty = Sài Gòn và có thêm từ khoá tìm kiếm",
     "1. Bấm nút Làm mới trong khối lọc\n2. Quan sát ô Công ty và danh sách",
     "—",
     "- Ô Công ty trở về trạng thái \"Tất cả\"\n- Danh sách tải lại đầy đủ, tổng số bản ghi bằng lúc chưa lọc"),

    (9, "Lọc công ty rồi chuyển trang", "P1",
     "Lọc Công ty = TPE, kết quả nhiều hơn 20 dòng",
     "1. Lọc Công ty = TPE\n2. Sang trang 2, trang 3\n3. Kiểm tra cột Nguồn hàng",
     "Công ty: TPE",
     "- Mọi trang đều chỉ có dòng TPE — điều kiện lọc không bị mất khi chuyển trang"),

    (10, "Lọc công ty rồi đổi số dòng trên trang", "P2",
     "Đang lọc Công ty = Sài Gòn",
     "1. Đổi số dòng hiển thị từ 20 sang 50\n2. Quan sát danh sách và tổng số bản ghi",
     "Công ty: Sài Gòn",
     "- Điều kiện lọc giữ nguyên, tổng số bản ghi không đổi, chỉ số dòng mỗi trang thay đổi"),

    (11, "Đóng cửa sổ khi đang lọc rồi mở lại", "P1",
     "Đang lọc Công ty = Sài Gòn",
     "1. Đóng cửa sổ Chọn hàng hoá\n2. Bấm Thêm hàng hoá mở lại\n3. Quan sát ô lọc Công ty và danh sách",
     "—",
     "- Cửa sổ mở lại ở trạng thái sạch: ô Công ty là \"Tất cả\", danh sách đầy đủ"),

    (12, "Chọn hàng khi đang lọc công ty khác công ty của báo giá", "P0",
     "Báo giá đang lập cho công ty TPE; mặt hàng H2 nguồn Sài Gòn, có hệ số giá của TPE",
     "1. Lọc Công ty = Sài Gòn\n2. Bấm vào dòng H2 để thêm vào lưới\n3. Đọc Đơn giá bán của dòng vừa thêm\n"
     "4. So với Giá niêm yết đã hiện trong cửa sổ",
     "H2 / Công ty lọc: Sài Gòn",
     "- Thêm được bình thường\n- Đơn giá bán bằng đúng Giá niêm yết đã hiện\n"
     "- ⚠️ Giá là giá theo công ty TPE (công ty của báo giá), không phải giá theo công ty Sài Gòn"),

    (13, "Sửa tay đường dẫn với giá trị công ty lạ", "P1",
     "Tester kỹ thuật; đang mở màn tạo báo giá",
     "1. Dùng công cụ kiểm thử gọi chức năng Tìm hàng hoá với điều kiện công ty là một giá trị không tồn tại\n"
     "2. Xem kết quả trả về",
     "Công ty: giá trị không tồn tại",
     "- Danh sách rỗng hoặc bỏ qua điều kiện lạ, KHÔNG treo trang và không báo lỗi kỹ thuật ra màn hình\n"
     "- Không lộ thêm dữ liệu nào ngoài phạm vi bình thường"),
]

S3 = [
    (1, "Giá hiển thị đã nhân hệ số của công ty trên báo giá", "P0",
     "Mặt hàng ENEO.700-V5029: giá bảng Bán lẻ 1.265.000; công ty của báo giá có hệ số 1,04",
     "1. Tạo báo giá mới cho công ty có hệ số 1,04, Bảng giá = Bán lẻ\n2. Mở cửa sổ Chọn hàng hoá\n"
     "3. Tìm mặt hàng ENEO.700-V5029\n4. Đọc cột Giá niêm yết",
     "ENEO.700-V5029 / hệ số 1,04",
     "- Giá niêm yết hiện 1.316.000 (1.265.000 × 1,04 = 1.315.600, làm tròn tới nghìn)\n"
     "- ⚠️ Không hiện 1.265.000 (giá gốc chưa nhân hệ số)"),

    (2, "Mặt hàng không có hệ số riêng thì giữ giá gốc", "P0",
     "Mặt hàng H9 không được cấu hình hệ số cho công ty của báo giá; giá bảng Bán lẻ là 1.200.000",
     "1. Mở cửa sổ Chọn hàng hoá\n2. Tìm mặt hàng H9\n3. Đọc Giá niêm yết",
     "H9",
     "- Hiện đúng 1.200.000\n- ⚠️ Không để trống, không bằng 0"),

    (3, "Giá luôn làm tròn tới hàng nghìn", "P0",
     "Mặt hàng có giá gốc và hệ số cho ra số lẻ (ví dụ 1.315.600)",
     "1. Tìm mặt hàng đó trong cửa sổ Chọn hàng hoá\n2. Đọc Giá niêm yết",
     "Giá gốc 1.265.000 × 1,04",
     "- Số hiển thị kết thúc bằng 000 (1.316.000)\n- Có dấu ngăn cách hàng nghìn, không có phần thập phân"),

    (4, "Đơn giá bán khi thêm vào lưới bằng đúng giá đã hiện", "P0",
     "Như trường hợp 1",
     "1. Trong cửa sổ, ghi lại Giá niêm yết của mặt hàng\n2. Bấm vào dòng để thêm vào lưới hàng hoá\n"
     "3. Đọc cột Đơn giá bán của dòng vừa thêm",
     "ENEO.700-V5029",
     "- Đơn giá bán = 1.316.000, đúng bằng số đã hiện trong cửa sổ\n- Ô đơn giá bị khoá, không sửa tay được"),

    (5, "Lưu báo giá — đơn giá không đổi sau khi lưu", "P0",
     "Báo giá mới có 1 dòng ENEO.700-V5029 với đơn giá 1.316.000",
     "1. Bấm Lưu nháp\n2. Thoát khỏi báo giá\n3. Mở lại báo giá vừa lưu\n4. Đọc Đơn giá bán của dòng hàng",
     "ENEO.700-V5029",
     "- Sau khi lưu và mở lại, đơn giá vẫn là 1.316.000\n"
     "- ⚠️ Đây là lỗi lệch giá cũ của yêu cầu này (trước đây lưu xong tụt về 1.265.000) — phải kiểm kỹ"),

    (6, "Thành tiền tính trên giá đã nhân hệ số", "P0",
     "Dòng hàng ENEO.700-V5029, số lượng 3",
     "1. Thêm mặt hàng vào lưới\n2. Sửa Số lượng thành 3\n3. Đọc Thành tiền bán của dòng",
     "Số lượng: 3",
     "- Thành tiền bán = 3.948.000 (1.316.000 × 3)\n- Tổng cộng của báo giá thay đổi tương ứng"),

    (7, "Thêm nhiều hàng cùng lúc bằng tích chọn", "P1",
     "Chọn 3 mặt hàng: một có hệ số, một không có hệ số, một thuộc nguồn hàng khác công ty",
     "1. Tích chọn 3 dòng\n2. Bấm nút \"Thêm N hàng hoá\"\n3. Đối chiếu đơn giá từng dòng trên lưới với Giá niêm yết đã hiện",
     "3 mặt hàng",
     "- Cả 3 dòng có đơn giá bằng đúng số đã hiện trong cửa sổ, không dòng nào bị lấy nhầm giá gốc"),

    (8, "Đổi Bảng giá trên báo giá rồi chọn hàng", "P0",
     "Báo giá đang ở Bảng giá Bán lẻ; đổi sang một bảng giá khác",
     "1. Đổi Bảng giá của báo giá\n2. Mở cửa sổ Chọn hàng hoá, tìm mặt hàng ENEO.700-V5029\n"
     "3. Đọc Giá niêm yết\n4. Thêm vào lưới và đối chiếu",
     "ENEO.700-V5029",
     "- Giá lấy theo bảng giá mới rồi mới nhân hệ số công ty\n- Đơn giá trên lưới khớp với số vừa hiện"),

    (9, "Đổi đơn vị tính của dòng hàng", "P0",
     "Dòng hàng ENEO.700-V5029 đang ở đơn vị cơ bản, có đơn vị tính thứ hai",
     "1. Đổi ĐVT của dòng hàng sang đơn vị khác\n2. Đọc Đơn giá bán mới",
     "Đổi ĐVT",
     "- Đơn giá mới vẫn là giá của công ty ghi trên báo giá (đã nhân hệ số), không rơi về giá gốc"),

    (10, "⚠️ Người công ty khác mở báo giá cũ ra sửa rồi lưu", "P0",
     "Báo giá BG-02 của công ty TPE có 2 dòng hàng, đơn giá 1.316.000 và 1.200.000. Tài khoản F thuộc công ty Sài Gòn "
     "và có quyền sửa báo giá này",
     "1. Đăng nhập tài khoản F\n2. Mở BG-02 ở chế độ Sửa, ghi lại đơn giá 2 dòng\n"
     "3. Sửa một thông tin không liên quan tới giá (ví dụ ghi chú)\n4. Bấm Lưu\n5. Mở lại BG-02, đọc đơn giá 2 dòng",
     "BG-02 / tài khoản F công ty Sài Gòn",
     "- Đơn giá 2 dòng GIỮ NGUYÊN 1.316.000 và 1.200.000\n"
     "- ⚠️ Giá phải theo công ty ghi trên báo giá, KHÔNG theo công ty người đang đăng nhập; lệch ở đây là lỗi nặng vì "
     "ô giá bị khoá nên người dùng không phát hiện được"),

    (11, "Cửa sổ chọn hàng mở từ báo giá của công ty khác", "P0",
     "Tài khoản F (công ty Sài Gòn) mở sửa báo giá BG-02 của công ty TPE; mặt hàng ENEO.700-V5029 có hệ số khác nhau "
     "giữa hai công ty",
     "1. Trong màn Sửa BG-02, bấm Thêm hàng hoá\n2. Tìm ENEO.700-V5029, đọc Giá niêm yết\n"
     "3. Thêm vào lưới, bấm Lưu, mở lại và đọc đơn giá dòng đó",
     "BG-02 / ENEO.700-V5029",
     "- Giá trong cửa sổ và giá sau khi lưu đều là giá theo công ty TPE (công ty của báo giá)\n"
     "- ⚠️ Nếu số trong cửa sổ khác số sau khi lưu thì FAIL — ghi rõ cả hai số vào Kết quả thực tế"),

    (12, "Tạo báo giá từ Bom — giá chuyển sang đúng hệ số", "P0",
     "Bom B1 có mặt hàng ENEO.700-V5029; tạo báo giá từ B1 cho công ty có hệ số 1,04",
     "1. Vào Quản lý Bomlist, chọn B1, tạo báo giá từ bom\n2. Mở báo giá vừa tạo\n3. Đọc Đơn giá bán của dòng ENEO.700-V5029",
     "B1 / ENEO.700-V5029",
     "- Đơn giá = 1.316.000, đúng hệ số của công ty trên báo giá"),

    (13, "Sao chép báo giá", "P1",
     "Báo giá BG-03 có dòng ENEO.700-V5029 đơn giá 1.316.000",
     "1. Sao chép BG-03\n2. Mở báo giá bản sao\n3. Đọc đơn giá dòng hàng",
     "BG-03",
     "- Đơn giá của bản sao tính theo công ty ghi trên bản sao, không bị rơi về giá gốc chưa nhân hệ số"),

    (14, "Nhập báo giá từ file Excel", "P1",
     "File Excel nhập có mặt hàng ENEO.700-V5029; báo giá thuộc công ty có hệ số 1,04",
     "1. Vào màn Sửa báo giá, chọn Nhập từ Excel\n2. Chọn file, chạy nhập\n3. Đọc đơn giá dòng ENEO.700-V5029 sau khi nhập",
     "File Excel mẫu",
     "- Đơn giá sau khi nhập là 1.316.000 — cùng công thức với cửa sổ chọn hàng"),

    (15, "Báo giá chưa lưu (màn Tạo mới) lấy giá theo công ty người lập", "P1",
     "Tài khoản A thuộc công ty TPE, đang ở màn Tạo báo giá và chưa bấm Lưu lần nào",
     "1. Mở cửa sổ Chọn hàng hoá, tìm một mặt hàng có hệ số riêng của TPE\n2. Đọc Giá niêm yết\n3. Thêm vào lưới và Lưu\n"
     "4. Mở lại báo giá, đọc đơn giá",
     "Tài khoản A / mặt hàng có hệ số TPE",
     "- Giá lúc chọn và giá sau khi lưu bằng nhau\n"
     "- Vì báo giá chưa tồn tại nên công ty áp giá là công ty của người lập — cũng chính là công ty được ghi lên báo giá khi lưu"),
]

S4 = [
    (1, "Cửa sổ chọn hàng của Bom có đủ cột mới", "P0",
     "Tài khoản E có quyền \"Tạo BOM List\"",
     "1. Vào Quản lý Bomlist → Tạo bom\n2. Bấm Thêm hàng hoá\n3. Đọc tiêu đề các cột",
     "—",
     "- Có cột \"Loại hàng hóa\", \"Lĩnh vực\", \"Chương\", \"Nguồn hàng\"\n"
     "- Thứ tự: Chọn · Mã · Tên hàng hoá · Loại hàng hóa · Lĩnh vực · Chương · Model · Thương hiệu · Xuất xứ · ĐVT · Nguồn hàng · Số lượng · Nguồn"),

    (2, "Cột Loại hàng hóa của cửa sổ Bom có dữ liệu", "P0",
     "Mặt hàng H1 có Loại hàng hóa là \"Hàng bán nốt tồn kho\"",
     "1. Trong cửa sổ chọn hàng của bom, tìm H1\n2. Đọc ô Loại hàng hóa",
     "H1",
     "- Hiện đúng tên loại hàng hóa như trong cửa sổ chọn hàng của Báo giá\n"
     "- ⚠️ Không hiện mã viết liền không dấu"),

    (3, "Cột Nguồn hàng của cửa sổ Bom", "P0",
     "H1 nguồn TPE, H2 nguồn Sài Gòn",
     "1. Tìm H1 rồi H2\n2. Đọc ô Nguồn hàng, rê chuột lên ô",
     "H1 / H2",
     "- H1 hiện TPE, H2 hiện TPSG; rê chuột hiện tên công ty đầy đủ"),

    (4, "Lĩnh vực / Chương trong cửa sổ Bom", "P0",
     "Mặt hàng H4 thuộc nhóm có nhiều phân loại; H6 thuộc nhóm chưa phân loại",
     "1. Tìm H4, đếm số dòng trong ô Lĩnh vực và Chương\n2. Tìm H6, đọc hai ô đó",
     "H4 / H6",
     "- H4: nhiều dòng trong một ô, mặt hàng vẫn chỉ một dòng\n- H6: hai ô để trống"),

    (5, "Ô lọc công ty trong cửa sổ Bom", "P0",
     "Dữ liệu: 495 mặt hàng nguồn Sài Gòn",
     "1. Bấm ô \"Lọc công ty\" ở hàng bộ lọc trên cùng\n2. Chọn Sài Gòn\n3. Quan sát danh sách",
     "Công ty: Sài Gòn",
     "- Danh sách tự tải lại ngay sau khi chọn\n- Mọi dòng có Nguồn hàng TPSG"),

    (6, "Lọc công ty kết hợp ô tìm theo mã/tên trong cửa sổ Bom", "P1",
     "H1 nguồn TPE và H2 nguồn Sài Gòn có tên gần giống nhau",
     "1. Gõ từ khoá chung vào ô \"Tìm theo mã hoặc tên...\"\n2. Chọn Lọc công ty = Sài Gòn",
     "Từ khoá chung / Sài Gòn",
     "- Chỉ còn H2; hai điều kiện áp đồng thời"),

    (7, "Bỏ lọc công ty trong cửa sổ Bom", "P1",
     "Đang lọc Sài Gòn",
     "1. Xoá lựa chọn ở ô Lọc công ty\n2. Quan sát danh sách",
     "—",
     "- Danh sách trở lại đầy đủ, có cả hàng TPE"),

    (8, "⚠️ Giá trong cửa sổ Bom khớp với cửa sổ Báo giá", "P0",
     "Mặt hàng ENEO.700-V5029; bom và báo giá cùng thuộc công ty có hệ số 1,04",
     "1. Mở cửa sổ chọn hàng của Báo giá, ghi lại giá của mặt hàng\n2. Mở cửa sổ chọn hàng của Bom, tìm cùng mặt hàng\n"
     "3. So hai con số",
     "ENEO.700-V5029",
     "- Hai nơi ra CÙNG một số (1.316.000)\n"
     "- ⚠️ Trước khi sửa, cửa sổ Bom trả giá gốc chưa nhân hệ số — đây là trọng tâm cần kiểm"),

    (9, "Giá hàng trong bom sau khi lưu", "P0",
     "Bom mới, thêm mặt hàng ENEO.700-V5029",
     "1. Thêm mặt hàng vào bom\n2. Lưu bom\n3. Mở lại bom, đọc đơn giá dòng hàng",
     "ENEO.700-V5029",
     "- Đơn giá sau khi lưu bằng số đã hiện lúc chọn"),

    (10, "Bom của công ty khác công ty người đăng nhập", "P0",
     "Bom B2 thuộc công ty TPE; tài khoản E thuộc công ty Sài Gòn có quyền sửa B2",
     "1. Đăng nhập E, mở B2 ở chế độ Sửa\n2. Ghi lại đơn giá các dòng\n3. Lưu lại bom\n4. Mở lại và đối chiếu",
     "B2 / tài khoản E",
     "- Đơn giá các dòng giữ nguyên, tính theo công ty ghi trên bom"),

    (11, "Thêm hàng con (bộ hàng) trong bom", "P1",
     "Mặt hàng H10 có danh sách hàng con trong hệ thống ERP",
     "1. Thêm H10 vào bom\n2. Mở phần hàng con\n3. Đọc đơn giá các hàng con",
     "H10",
     "- Hàng con cũng lấy giá theo công ty ghi trên bom, cùng công thức với hàng cha"),

    (12, "Số dòng của cửa sổ Bom không đổi sau khi thêm cột", "P1",
     "Tìm với từ khoá cho ra nhiều kết quả",
     "1. Gõ từ khoá, đếm số dòng trả về\n2. Đối chiếu với số dòng cùng từ khoá trước khi có 4 cột mới (nếu có bản ghi lại)",
     "Từ khoá bất kỳ",
     "- Số dòng không đổi; việc bổ sung cột không làm mất hay nhân bản mặt hàng"),
]

S5 = [
    (1, "Cửa sổ chọn hàng trên ERP có đủ 3 cột mới", "P0",
     "Tài khoản có quyền lập báo giá trên hệ thống ERP",
     "1. Vào ERP → Kinh doanh → Báo giá → Tạo mới\n2. Mở cửa sổ Chọn hàng hoá\n3. Đọc tiêu đề các cột",
     "—",
     "- Có cột Lĩnh vực, Chương (liền nhau, ngay trước Model) và cột Nguồn hàng\n- Các cột cũ vẫn còn đủ"),

    (2, "Ô lọc Công ty trên cửa sổ ERP", "P0",
     "Hệ thống có 7 công ty",
     "1. Mở cửa sổ Chọn hàng hoá trên ERP\n2. Bấm ô lọc Công ty, đọc danh sách\n3. Chọn Sài Gòn",
     "Công ty: Sài Gòn",
     "- Danh sách công ty đủ 7 dòng\n- Sau khi chọn, danh sách hàng chỉ còn hàng nguồn TPSG"),

    (3, "Hai cột Lĩnh vực / Chương trên ERP đủ rộng", "P0",
     "Mặt hàng H8 có tên Lĩnh vực dài khoảng 60 ký tự",
     "1. Tìm H8 trên cửa sổ ERP\n2. Quan sát hai cột Lĩnh vực và Chương",
     "H8",
     "- Cột đủ rộng, chữ xuống dòng, đọc được hết\n"
     "- ⚠️ Lỗi đã từng gặp: hai cột bị bóp hẹp thành một sợi dọc — kiểm kỹ trên màn hình nhỏ"),

    (4, "Nguồn hàng trên ERP đúng mặt hàng", "P0",
     "H1 nguồn TPE, H2 nguồn Sài Gòn",
     "1. Tìm H1 rồi H2 trên cửa sổ ERP\n2. Đọc cột Nguồn hàng",
     "H1 / H2",
     "- Hiện đúng TPE và TPSG"),

    (5, "Mặt hàng chưa phân loại trên ERP", "P1",
     "Mặt hàng H6 thuộc nhóm chưa phân loại",
     "1. Tìm H6 trên cửa sổ ERP\n2. Đọc ô Lĩnh vực, Chương",
     "H6",
     "- Hai ô để trống, dòng vẫn hiện bình thường"),

    (6, "Lọc công ty trên ERP kết hợp các ô lọc sẵn có", "P1",
     "Cửa sổ ERP có sẵn các ô lọc Lĩnh vực, Chương, Nhóm hàng",
     "1. Chọn Lĩnh vực L1\n2. Chọn thêm Công ty = Sài Gòn\n3. Quan sát kết quả",
     "L1 / Sài Gòn",
     "- Kết quả thoả cả hai điều kiện, không mất điều kiện nào"),

    (7, "Giá trên cửa sổ ERP không đổi khi lọc công ty", "P0",
     "Mặt hàng ENEO.700-V5029",
     "1. Ghi lại giá của mặt hàng khi chưa lọc\n2. Lọc theo từng công ty rồi tìm lại mặt hàng đó",
     "ENEO.700-V5029",
     "- Giá không đổi qua các lần lọc"),

    (8, "Chuyển trang trên cửa sổ ERP", "P1",
     "Kết quả nhiều hơn một trang",
     "1. Sang trang 2, trang 3\n2. Quan sát 3 cột mới và điều kiện lọc công ty đang chọn",
     "—",
     "- Ba cột mới có dữ liệu ở mọi trang; điều kiện lọc công ty không bị mất"),
]

S6 = [
    (1, "Giá vốn KHÔNG bị nhân hệ số công ty", "P0",
     "Tài khoản có quyền \"Xem giá vốn hàng hoá\"; mặt hàng ENEO.700-V5029 có giá vốn gốc 951.456 và hệ số công ty 1,04",
     "1. Thêm mặt hàng vào lưới báo giá\n2. Đọc cột Đơn giá nhập của dòng",
     "ENEO.700-V5029",
     "- Đơn giá nhập giữ nguyên giá vốn gốc 951.456\n"
     "- ⚠️ Không được nhân 1,04 — hệ số chỉ áp cho giá bán"),

    (2, "Tỷ suất lợi nhuận tính trên giá bán đã nhân hệ số", "P1",
     "Dòng hàng có Đơn giá bán 1.316.000 và Đơn giá nhập 951.456",
     "1. Đọc cột Tỷ suất lợi nhuận của dòng",
     "—",
     "- Tỷ suất tính từ đơn giá bán đã nhân hệ số và giá vốn gốc, khớp với công thức đang dùng trên lưới"),

    (3, "Người không có quyền xem giá vốn — cửa sổ chọn hàng", "P0",
     "Tài khoản D không có quyền \"Xem giá vốn hàng hoá\"",
     "1. Đăng nhập D, mở cửa sổ Chọn hàng hoá\n2. Quan sát toàn bộ các cột, kể cả khi kéo ngang hết bảng",
     "Tài khoản D",
     "- Không có cột nào chứa giá vốn\n- Giá niêm yết (giá bán) vẫn hiện bình thường"),

    (4, "Người không có quyền xem giá vốn — lưới hàng hoá", "P0",
     "Tài khoản D vừa thêm 2 mặt hàng vào báo giá",
     "1. Quan sát lưới hàng hoá\n2. Kiểm tra từng dòng",
     "Tài khoản D",
     "- Không hiện Đơn giá nhập / Thành tiền nhập / Tỷ suất lợi nhuận ở mọi dòng"),

    (5, "Gọi thẳng chức năng tìm hàng bằng tài khoản không có quyền xem giá vốn", "P1",
     "Tài khoản D; dùng công cụ kiểm thử",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Tìm hàng hoá bằng tài khoản D\n2. Xem dữ liệu trả về",
     "Tài khoản D",
     "- Dữ liệu trả về không chứa giá vốn ở bất kỳ dòng nào\n- ⚠️ Dành cho tester kỹ thuật; đây là kiểm tra chặn từ máy chủ, không phải chỉ ẩn trên màn hình"),
]

S7 = [
    (1, "Tìm với từ khoá không có kết quả", "P1",
     "Đang mở cửa sổ Chọn hàng hoá",
     "1. Gõ chuỗi vô nghĩa vào ô tìm nhanh\n2. Bấm Tìm kiếm",
     "Từ khoá: zzzqq",
     "- Hiện dòng thông báo không có dữ liệu, chiều rộng dòng thông báo phủ đúng số cột của bảng\n"
     "- ⚠️ Kiểm tra dòng thông báo không bị lệch cột sau khi thêm 3 cột mới"),

    (2, "Tìm bằng ký tự đặc biệt", "P1",
     "Đang mở cửa sổ Chọn hàng hoá",
     "1. Gõ lần lượt các ký tự %, _, ', \" vào ô tìm nhanh và bấm Tìm kiếm",
     "%, _, ', \"",
     "- Không báo lỗi kỹ thuật, không treo\n- Kết quả rỗng hoặc đúng mặt hàng có ký tự đó trong tên"),

    (3, "Mặt hàng có hệ số bằng 0 hoặc âm trong dữ liệu", "P1",
     "Chuẩn bị mặt hàng H11 có hệ số cấu hình sai (0 hoặc âm) cho công ty của báo giá",
     "1. Tìm H11 trong cửa sổ Chọn hàng hoá\n2. Đọc Giá niêm yết",
     "H11",
     "- Giữ nguyên giá gốc của bảng giá\n- ⚠️ Không được ra 0 hoặc số âm; không được để trống"),

    (4, "Mặt hàng chưa có giá trong bảng giá đang chọn", "P1",
     "Mặt hàng H12 không có giá ở bảng giá đang chọn trên báo giá",
     "1. Tìm H12\n2. Đọc Giá niêm yết\n3. Thử thêm vào lưới và bấm Lưu",
     "H12",
     "- Ô giá hiện dấu — hoặc 0 theo đúng hành vi cũ của màn\n- Khi lưu, hệ thống báo không cho lưu dòng có đơn giá bằng 0 (giữ nguyên quy tắc cũ)"),

    (5, "Hệ thống ERP không phản hồi", "P1",
     "Tạm ngắt kết nối tới hệ thống ERP (tester kỹ thuật phối hợp)",
     "1. Mở cửa sổ Chọn hàng hoá\n2. Quan sát thông báo",
     "—",
     "- Hiện thông báo tiếng Việt dễ hiểu về việc không tải được danh sách hàng hoá\n"
     "- Không treo trang trắng, không hiện chuỗi lỗi kỹ thuật"),

    (6, "Danh sách công ty trong ô lọc không tải được", "P2",
     "Tạm ngắt kết nối tới hệ thống ERP khi mở cửa sổ",
     "1. Mở cửa sổ Chọn hàng hoá\n2. Bấm ô lọc Công ty",
     "—",
     "- Ô lọc rỗng nhưng cửa sổ vẫn dùng được các ô lọc khác\n- Có thông báo không tải được danh mục"),

    (7, "Tìm nhanh liên tiếp nhiều lần", "P1",
     "Đang mở cửa sổ Chọn hàng hoá",
     "1. Gõ liên tiếp 3 từ khoá khác nhau, mỗi lần cách nhau dưới 1 giây\n2. Chờ kết quả cuối cùng",
     "3 từ khoá liên tiếp",
     "- Kết quả hiện ra là của từ khoá cuối cùng\n- ⚠️ Không có chuyện kết quả của lần tìm trước về muộn rồi đè lên"),

    (8, "Đổi công ty lọc liên tiếp nhiều lần", "P2",
     "Đang mở cửa sổ Chọn hàng hoá",
     "1. Chọn lần lượt TPE → Sài Gòn → TPE, mỗi lần cách nhau dưới 1 giây\n2. Quan sát danh sách cuối cùng",
     "—",
     "- Danh sách khớp với lựa chọn cuối cùng; cột Nguồn hàng đồng nhất"),

    (9, "Mặt hàng đã có trong lưới, chọn lại lần nữa", "P1",
     "Dòng ENEO.700-V5029 đã có trên lưới báo giá",
     "1. Mở cửa sổ Chọn hàng hoá, chọn lại đúng mặt hàng đó\n2. Quan sát cảnh báo trùng của màn",
     "ENEO.700-V5029",
     "- Giữ nguyên hành vi cảnh báo trùng như trước đây\n- Nếu người dùng vẫn thêm, dòng mới có đơn giá bằng dòng cũ"),

    (10, "Cửa sổ chọn hàng mở từ nút Thêm nhanh ở cuối nhóm", "P1",
     "Báo giá có nhóm hàng A",
     "1. Cuộn tới cuối nhóm A, bấm Thêm mới\n2. Quan sát cửa sổ mở ra",
     "Nhóm A",
     "- Cùng cửa sổ, cùng 3 cột mới và ô lọc công ty\n- Hàng chọn xong nằm đúng trong nhóm A, đơn giá đúng"),
]

S8 = [
    (1, "Bản in báo giá không có 3 thông tin mới", "P0",
     "Báo giá BG-04 có 3 dòng hàng lấy từ hệ thống ERP",
     "1. Mở BG-04\n2. Bấm In, xem bản xem trước",
     "BG-04",
     "- Bản in không có cột Nguồn hàng, Lĩnh vực, Chương\n- Các cột cũ và bố cục bản in không đổi"),

    (2, "File Excel xuất từ báo giá không có 3 thông tin mới", "P0",
     "Báo giá BG-04",
     "1. Bấm Xuất Excel\n2. Mở file, xem các cột",
     "BG-04",
     "- Không có cột Nguồn hàng / Lĩnh vực / Chương\n- Đơn giá trong file bằng đơn giá trên màn hình"),

    (3, "Bản in bom không có 3 thông tin mới", "P1",
     "Bom B1 có hàng lấy từ hệ thống ERP",
     "1. Mở B1, bấm In\n2. Xem bản xem trước",
     "B1",
     "- Không có 3 cột mới; bố cục bản in giữ nguyên"),

    (4, "Danh sách báo giá không đổi", "P1",
     "Màn Quản lý Báo giá có dữ liệu sẵn",
     "1. Mở màn danh sách báo giá\n2. Lọc, tìm kiếm như thường ngày",
     "—",
     "- Cột, bộ lọc, tổng số bản ghi không đổi so với trước"),

    (5, "Màn chi tiết bom và danh sách đơn vị tính không đổi", "P1",
     "Bom B1 có nhiều dòng hàng",
     "1. Mở chi tiết B1\n2. Mở ô chọn ĐVT của một dòng hàng",
     "B1",
     "- Danh sách đơn vị tính hiện đủ như trước\n- ⚠️ Đây là chỗ dùng chung hàm lấy giá — kiểm tra không bị mất dòng ĐVT nào"),

    (6, "Hàng tạm (hàng tự nhập) không bị ảnh hưởng", "P0",
     "Báo giá có 1 dòng hàng tạm do người dùng tự khai",
     "1. Thêm một hàng tạm qua nút Thêm hàng tạm\n2. Nhập đơn giá tự gõ, lưu báo giá\n3. Mở lại và đọc đơn giá",
     "Hàng tạm HT-01",
     "- Đơn giá hàng tạm giữ đúng số người dùng gõ, không bị nhân hệ số\n- Hàng tạm không có Nguồn hàng / Lĩnh vực / Chương"),

    (7, "Các dòng hàng cũ trong báo giá đã duyệt", "P1",
     "Báo giá BG-05 đã duyệt, có dòng hàng lấy từ hệ thống ERP",
     "1. Mở BG-05 ở chế độ Xem\n2. Đọc đơn giá các dòng",
     "BG-05",
     "- Đơn giá đã duyệt giữ nguyên, không bị tính lại theo hệ số"),

    (8, "Cảnh báo đổi giá khi mở lại báo giá đang tạo", "P1",
     "Báo giá BG-06 ở trạng thái Đang tạo, có hàng lấy từ hệ thống ERP; hệ số hoặc giá gốc vừa được cấu hình lại",
     "1. Mở BG-06 ở chế độ Sửa\n2. Quan sát cửa sổ cảnh báo đổi giá\n3. Chọn Không đồng ý rồi mở lại, lần sau chọn Đồng ý",
     "BG-06",
     "- Cửa sổ cảnh báo liệt kê đúng dòng lệch giá, cột giá mới là giá đã nhân hệ số của công ty trên báo giá\n"
     "- Chọn Không đồng ý thì giá giữ nguyên; chọn Đồng ý thì cập nhật đúng số đã hiện"),
]

S9 = [
    (1, "Luồng đầy đủ trên Báo giá: chọn hàng → lưu → in → xuất Excel", "P0",
     "Tài khoản A công ty TPE, dự án D1; mặt hàng ENEO.700-V5029 (hệ số 1,04) và một mặt hàng không có hệ số",
     "1. Tạo báo giá mới\n2. Mở cửa sổ Chọn hàng hoá, lọc Công ty = TPE\n3. Ghi lại Giá niêm yết 2 mặt hàng, thêm cả 2 vào lưới\n"
     "4. Lưu nháp, thoát, mở lại\n5. Đối chiếu đơn giá 2 dòng với số đã ghi\n6. In và Xuất Excel",
     "2 mặt hàng như mô tả",
     "- Giá ở 4 điểm trùng nhau: trong cửa sổ, trên lưới, sau khi lưu mở lại, trong file Excel\n"
     "- Bản in và file Excel không có 3 thông tin mới"),

    (2, "Luồng đầy đủ trên Bom → tạo báo giá từ bom", "P0",
     "Tài khoản có quyền tạo bom và tạo báo giá; công ty có hệ số 1,04",
     "1. Tạo bom mới, mở cửa sổ chọn hàng, lọc Công ty = Sài Gòn, thêm 2 mặt hàng\n2. Ghi lại đơn giá, lưu bom\n"
     "3. Tạo báo giá từ bom đó\n4. Đối chiếu đơn giá các dòng trên báo giá",
     "2 mặt hàng nguồn Sài Gòn",
     "- Đơn giá trên bom và trên báo giá sinh ra từ bom bằng nhau và bằng số đã hiện lúc chọn"),

    (3, "Luồng chéo hai hệ thống: chọn cùng mặt hàng ở ERP và ở Báo giá", "P1",
     "Cùng một tài khoản nghiệp vụ, cùng mặt hàng ENEO.700-V5029, cùng công ty",
     "1. Trên ERP, mở cửa sổ chọn hàng, ghi lại giá mặt hàng\n2. Trên Quản lý Báo giá, mở cửa sổ chọn hàng, ghi lại giá\n"
     "3. So sánh hai số",
     "ENEO.700-V5029",
     "- Hai hệ thống ra cùng một số"),

    (4, "Luồng người dùng đổi ý nhiều lần", "P1",
     "Đang tạo báo giá mới",
     "1. Lọc Công ty = Sài Gòn, thêm 1 mặt hàng\n2. Xoá dòng vừa thêm\n3. Bỏ lọc, lọc lại TPE, thêm mặt hàng khác\n"
     "4. Bấm Làm mới trong khối lọc, thêm mặt hàng thứ ba\n5. Lưu và mở lại",
     "3 lần thao tác như mô tả",
     "- Lưới còn đúng 2 dòng, đơn giá cả hai đúng theo công ty của báo giá\n- Không dòng nào giữ giá của lần lọc trước"),
]

SECTIONS = [
    ("I", "CỬA SỔ CHỌN HÀNG HOÁ Ở MÀN BÁO GIÁ — CỘT NGUỒN HÀNG, LĨNH VỰC, CHƯƠNG", S1),
    ("II", "BỘ LỌC CÔNG TY (NGUỒN HÀNG) TRÊN CỬA SỔ BÁO GIÁ", S2),
    ("III", "GIÁ BÁN THEO CÔNG TY — MÀN BÁO GIÁ", S3),
    ("IV", "CỬA SỔ CHỌN HÀNG HOÁ Ở MÀN BOMLIST", S4),
    ("V", "CỬA SỔ CHỌN HÀNG HOÁ TRÊN ERP (KINH DOANH → BÁO GIÁ)", S5),
    ("VI", "GIÁ VỐN & DỮ LIỆU NHẠY CẢM", S6),
    ("VII", "RÀNG BUỘC NHẬP LIỆU & TRƯỜNG HỢP BIÊN", S7),
    ("VIII", "KHÔNG ẢNH HƯỞNG CHỨC NĂNG CŨ", S8),
    ("IX", "LUỒNG ĐẦU CUỐI", S9),
]

if __name__ == "__main__":
    build(
        output_file=os.path.join(HERE, "testcase-11286.xlsx"),
        sheet_name="Trang tính1",
        feature_name="Popup chọn hàng hoá theo công ty (Nguồn hàng, Lĩnh vực, Chương, lọc Công ty, giá theo công ty) "
                     "— bổ sung cho yêu cầu 11286, ngày 15/09/2026",
        module_name="Báo giá / Bomlist — Chọn hàng hoá",
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
