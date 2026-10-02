# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho Redmine #10900 - Xoa du lieu giam gia hang loat o Bao gia."""
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

MODULE = "Báo giá - Xóa giảm giá"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Bổ sung 1 nút trên thanh công cụ phía trên bảng \"Chi tiết sản phẩm\" ở màn Tạo mới / Cập nhật "
     "báo giá, cho phép xóa toàn bộ dữ liệu giảm giá đang nhập chỉ bằng một thao tác thay vì phải sửa "
     "tay từng dòng. Chữ trên nút đổi theo phương thức giảm giá đang chọn: \"Xóa giảm giá\" (khi chọn "
     "Giảm giá mặt hàng) hoặc \"Xóa phân bổ\" (khi chọn Giảm giá tổng)."),

    ("2. Đối tượng được tính / hiển thị",
     "Nút chỉ hiện khi ĐỒNG THỜI: (a) tài khoản có quyền \"Cho phép thêm giảm giá trong báo giá\"; "
     "(b) báo giá đã chọn một phương thức giảm giá (Giảm giá mặt hàng hoặc Giảm giá tổng); "
     "(c) đang ở màn Tạo mới hoặc màn Cập nhật báo giá.\n"
     "Phạm vi bị xóa:\n"
     "- Giảm giá mặt hàng: cột GG(%) và GG(đ) của TẤT CẢ dòng thuộc nhóm Hàng hóa VÀ nhóm Dịch vụ "
     "được đưa về 0.\n"
     "- Giảm giá tổng: cột \"Phân bổ GG\" của TẤT CẢ dòng hàng hóa, dòng dịch vụ VÀ dòng Chi phí vận "
     "chuyển được đưa về 0."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Tài khoản KHÔNG có quyền \"Cho phép thêm giảm giá trong báo giá\": nút ẩn hẳn, không hiện nút "
     "xám.\n"
     "- Chưa chọn phương thức giảm giá: nút không hiện.\n"
     "- Màn Chi tiết (chỉ xem) báo giá: không có nút.\n"
     "- Bảng \"Khoản giảm giá tổng\" (danh sách các khoản giảm giá người dùng đã nhập) KHÔNG bị xóa khi "
     "bấm \"Xóa phân bổ\" - chỉ cột Phân bổ GG về 0, các khoản giảm giá giữ nguyên để phân bổ lại được.\n"
     "- Đơn giá, Số lượng, VAT(%) của từng dòng không bị đụng tới."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng. Đây là thao tác trên form nhập liệu của một báo giá, không phải màn danh sách nên "
     "không có bộ lọc thời gian."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng \"Chi tiết sản phẩm\" của báo giá gồm 3 phần: nhóm Hàng hóa (nhiều dòng, có thể chia nhóm "
     "nhiều cấp), nhóm Dịch vụ (nhiều dòng) và dòng \"Chi phí vận chuyển\" nằm riêng ở cuối. "
     "Dòng vận chuyển không nằm trong nhóm hàng hóa hay dịch vụ nhưng vẫn nhận phân bổ giảm giá tổng, "
     "nên phải kiểm riêng dòng này ở mọi trường hợp test liên quan Giảm giá tổng."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Sau khi xóa, các ô \"Đơn giá sau GG\", \"Thành tiền bán\", tiền VAT, \"Tổng giá trị báo giá\" và "
     "\"Tỷ suất lợi nhuận\" tự tính lại theo dữ liệu mới, người dùng không phải bấm thêm nút nào. "
     "Với Giảm giá tổng, sau khi xóa phân bổ thì dòng cảnh báo lệch hiện lại dạng \"Đã phân bổ 0 / Tổng "
     "giảm giá X\" và nút \"Phân bổ tự động\" xuất hiện trở lại."),

    ("7. Phân quyền cấp",
     "Tính năng KHÔNG thêm quyền mới. Dùng lại đúng quyền đã có:\n"
     "- \"Cho phép thêm giảm giá trong báo giá\" (nhóm Báo giá): quyết định nút có hiện hay không. "
     "Không có quyền này thì ô chọn phương thức giảm giá cũng bị khóa.\n"
     "- Các quyền xem / thao tác báo giá theo cấp tổ chức đang có sẵn: \"Xem tất cả danh sách Báo giá\", "
     "\"Xem danh sách Báo giá theo công ty\", \"Xem danh sách Báo giá theo phòng ban\", "
     "\"Xem danh sách Báo giá theo bộ phận\".\n"
     "Lưu ý triển khai: quyền \"Cho phép thêm giảm giá trong báo giá\" phải được cấp cho nhóm người dùng "
     "cần test, nếu không toàn bộ khối giảm giá bị khóa và không test được gì."),

    ("8. Cách tính các ô thống kê",
     "- \"Tổng giảm giá\" = tổng số tiền giảm giá của mọi dòng (theo phương thức đang chọn).\n"
     "- \"Tổng giá trị báo giá\" = tổng Thành tiền bán sau giảm giá, cộng thuế theo quy tắc sẵn có.\n"
     "- Dòng cảnh báo lệch của Giảm giá tổng = \"Đã phân bổ <tổng cột Phân bổ GG của mọi dòng, gồm cả "
     "dòng Chi phí vận chuyển> / Tổng giảm giá <tổng các khoản giảm giá đã nhập>\". Hai số bằng nhau "
     "thì cảnh báo biến mất và nút \"Phân bổ tự động\" ẩn đi.\n"
     "- \"Tỷ suất lợi nhuận\" tính lại theo giá bán sau giảm giá mới."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này:\n"
     "1) Nút này CỐ TÌNH hiện-mờ (không bấm được) khi mọi giá trị giảm giá đang bằng 0, khác với quy "
     "ước chung của hệ thống là ẩn hẳn nút không dùng được. Đây là yêu cầu của khách, KHÔNG phải lỗi. "
     "Riêng trường hợp thiếu quyền giảm giá thì vẫn ẩn hẳn.\n"
     "2) \"Xóa phân bổ\" KHÔNG xóa bảng khoản giảm giá tổng. Thấy bảng khoản giảm giá còn nguyên là "
     "ĐÚNG, đừng báo lỗi.\n"
     "3) Luôn kiểm thêm dòng \"Chi phí vận chuyển\" - đây là chỗ dễ sót nhất, trước đây đổi phương thức "
     "giảm giá xong dòng này vẫn còn số dư làm lệch tổng tiền.\n"
     "4) Thao tác chỉ tác động lên dữ liệu đang nhập trên màn hình. Chưa bấm Lưu thì dữ liệu cũ vẫn còn "
     "nguyên; thoát ra không lưu rồi vào lại phải thấy số liệu giảm giá như cũ.\n"
     "5) Số tiền hiển thị theo chuẩn quốc tế: dấu phẩy ngăn cách hàng nghìn, dấu chấm cho phần thập "
     "phân (ví dụ 14,920,000)."),
]

ROLE_TCS = [
    ("00", "Tài khoản có quyền giảm giá thấy nút xóa", "P0",
     "Nhóm người dùng của tài khoản A đã được cấp quyền \"Cho phép thêm giảm giá trong báo giá\". "
     "Báo giá BG-TEST-001 đang soạn, phương thức Giảm giá mặt hàng, 2 dòng hàng hóa có giảm giá 10%.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào phân hệ Giao việc → nhóm Báo giá → bấm \"Báo giá\"\n"
     "3. Mở báo giá BG-TEST-001, bấm nút Sửa\n"
     "4. Quan sát thanh công cụ phía trên bảng Chi tiết sản phẩm",
     "Tài khoản: A (có quyền giảm giá)",
     "- Nút \"Xóa giảm giá\" hiện trên thanh công cụ, có biểu tượng cục tẩy\n"
     "- Nút bấm được (không bị mờ) vì đang có dữ liệu giảm giá\n"
     "- Ô chọn phương thức giảm giá không bị khóa"),

    ("01", "Tài khoản KHÔNG có quyền giảm giá thì không thấy nút", "P0",
     "Nhóm người dùng của tài khoản B KHÔNG được cấp quyền \"Cho phép thêm giảm giá trong báo giá\". "
     "Cùng báo giá BG-TEST-001 ở trên.",
     "1. Đăng nhập bằng tài khoản B\n"
     "2. Vào phân hệ Giao việc → nhóm Báo giá → bấm \"Báo giá\"\n"
     "3. Mở báo giá BG-TEST-001, bấm nút Sửa\n"
     "4. Quan sát thanh công cụ phía trên bảng Chi tiết sản phẩm",
     "Tài khoản: B (không có quyền giảm giá)",
     "- ⚠️ Nút \"Xóa giảm giá\" / \"Xóa phân bổ\" KHÔNG xuất hiện (ẩn hẳn, không phải nút xám)\n"
     "- Ô chọn phương thức giảm giá bị khóa, không chọn được\n"
     "- Các phần còn lại của màn báo giá hoạt động bình thường"),

    ("02", "Rút quyền giảm giá khi đang mở màn báo giá", "P1",
     "Tài khoản A đang mở màn Cập nhật báo giá BG-TEST-001 với nút \"Xóa giảm giá\" đang hiện. "
     "Quản trị viên rút quyền \"Cho phép thêm giảm giá trong báo giá\" khỏi nhóm người dùng của A.",
     "1. Giữ nguyên màn đang mở của tài khoản A\n"
     "2. Quản trị viên rút quyền ở màn Thiết lập → Phân quyền\n"
     "3. Tài khoản A tải lại trang báo giá",
     "—",
     "- Sau khi tải lại trang, nút xóa giảm giá biến mất\n"
     "- Không có lỗi trắng trang, dữ liệu báo giá vẫn hiển thị đủ"),
]

SEC_I = [
    ("001", "Nút hiện đúng ở màn Cập nhật báo giá", "P0",
     "Tài khoản A có quyền giảm giá. Báo giá BG-TEST-001 ở trạng thái cho phép sửa, phương thức "
     "Giảm giá mặt hàng.",
     "1. Vào phân hệ Giao việc → nhóm Báo giá → bấm \"Báo giá\"\n"
     "2. Mở báo giá BG-TEST-001 → bấm nút Sửa\n"
     "3. Cuộn tới bảng \"Chi tiết sản phẩm\"",
     "—",
     "- Nút xóa nằm trên cùng thanh công cụ với các nút thao tác của bảng Chi tiết sản phẩm, "
     "cách nhóm nút bên trái bằng một vạch ngăn\n"
     "- Nút có nền đỏ, biểu tượng cục tẩy, chữ \"Xóa giảm giá\""),

    ("002", "Nút hiện đúng ở màn Tạo mới báo giá", "P0",
     "Tài khoản A có quyền giảm giá. Chưa có báo giá nào được tạo.",
     "1. Vào phân hệ Giao việc → nhóm Báo giá → bấm \"Báo giá\"\n"
     "2. Bấm nút \"Thêm mới\"\n"
     "3. Chọn phương thức giảm giá \"Giảm giá mặt hàng\"\n"
     "4. Quan sát thanh công cụ của bảng Chi tiết sản phẩm",
     "Phương thức giảm giá: Giảm giá mặt hàng",
     "- ⚠️ Màn Tạo mới hành xử y hệt màn Cập nhật: nút hiện với chữ \"Xóa giảm giá\"\n"
     "- Chưa nhập giảm giá nên nút đang mờ, không bấm được"),

    ("003", "Chưa chọn phương thức giảm giá thì không có nút", "P0",
     "Tài khoản A có quyền giảm giá. Báo giá mới tạo, ô phương thức giảm giá đang để trống.",
     "1. Vào màn Tạo mới báo giá\n"
     "2. Không chọn phương thức giảm giá\n"
     "3. Quan sát thanh công cụ của bảng Chi tiết sản phẩm",
     "Phương thức giảm giá: (để trống)",
     "- Nút xóa KHÔNG hiện\n"
     "- Vạch ngăn trước nút cũng không hiện (không để lại khoảng trống thừa)"),

    ("004", "Chữ trên nút đổi theo phương thức Giảm giá mặt hàng", "P0",
     "Màn Cập nhật báo giá BG-TEST-001, tài khoản A có quyền giảm giá.",
     "1. Chọn phương thức giảm giá \"Giảm giá mặt hàng\"\n"
     "2. Đọc chữ trên nút",
     "Phương thức giảm giá: Giảm giá mặt hàng",
     "- Chữ trên nút là \"Xóa giảm giá\""),

    ("005", "Chữ trên nút đổi theo phương thức Giảm giá tổng", "P0",
     "Màn Cập nhật báo giá BG-TEST-001, tài khoản A có quyền giảm giá.",
     "1. Chọn phương thức giảm giá \"Giảm giá tổng\"\n"
     "2. Đọc chữ trên nút",
     "Phương thức giảm giá: Giảm giá tổng",
     "- ⚠️ Chữ trên nút đổi ngay thành \"Xóa phân bổ\", không phải tải lại trang"),

    ("006", "Nút mờ khi mọi giá trị giảm giá đang bằng 0", "P0",
     "Báo giá BG-TEST-002 có 5 dòng hàng hóa, tất cả đều để GG(%) = 0 và GG(đ) = 0. "
     "Phương thức Giảm giá mặt hàng.",
     "1. Mở BG-TEST-002 → bấm Sửa\n"
     "2. Quan sát nút \"Xóa giảm giá\"\n"
     "3. Thử bấm vào nút",
     "Mọi dòng: GG(%) = 0, GG(đ) = 0",
     "- ⚠️ Nút VẪN HIỆN nhưng ở trạng thái mờ, bấm không có phản ứng (đúng yêu cầu khách, không phải "
     "lỗi)\n"
     "- Không mở cửa sổ xác nhận, không hiện thông báo"),

    ("007", "Nút tự bật khi vừa nhập giảm giá cho một dòng", "P0",
     "Báo giá BG-TEST-002, mọi dòng đang không có giảm giá, nút đang mờ.",
     "1. Nhập GG(%) = 5 cho dòng hàng hóa đầu tiên\n"
     "2. Bấm ra ngoài ô\n"
     "3. Quan sát nút \"Xóa giảm giá\"",
     "Dòng 1 - GG(%): 5",
     "- Nút chuyển sang bấm được ngay, không phải tải lại trang"),

    ("008", "Nút tự mờ lại sau khi người dùng tự sửa giảm giá về 0", "P1",
     "Báo giá BG-TEST-002 chỉ có duy nhất dòng 1 đang để GG(%) = 5.",
     "1. Sửa GG(%) của dòng 1 về 0\n"
     "2. Bấm ra ngoài ô\n"
     "3. Quan sát nút",
     "Dòng 1 - GG(%): 0",
     "- Nút tự chuyển về trạng thái mờ vì không còn dữ liệu giảm giá để xóa"),

    ("009", "Nút bật khi chỉ có dòng DỊCH VỤ có giảm giá", "P1",
     "Báo giá BG-TEST-003: mọi dòng hàng hóa GG = 0, riêng 1 dòng thuộc nhóm Dịch vụ có GG(đ) = "
     "500,000. Phương thức Giảm giá mặt hàng.",
     "1. Mở BG-TEST-003 → bấm Sửa\n"
     "2. Quan sát nút \"Xóa giảm giá\"",
     "Dòng dịch vụ - GG(đ): 500,000",
     "- ⚠️ Nút bấm được - điều kiện bật nút tính cả nhóm Dịch vụ chứ không chỉ nhóm Hàng hóa"),

    ("010", "Nút mờ khi Giảm giá tổng đã nhập khoản nhưng chưa phân bổ", "P0",
     "Báo giá BG-TEST-004, phương thức Giảm giá tổng, đã nhập 1 khoản giảm giá 20,000,000 nhưng "
     "chưa bấm \"Phân bổ tự động\" nên cột Phân bổ GG mọi dòng đều là 0.",
     "1. Mở BG-TEST-004 → bấm Sửa\n"
     "2. Quan sát nút \"Xóa phân bổ\"",
     "Khoản giảm giá tổng: 20,000,000; Đã phân bổ: 0",
     "- ⚠️ Nút mờ, vì chưa có giá trị phân bổ nào để xóa (nút này xóa PHÂN BỔ chứ không xóa khoản "
     "giảm giá)"),

    ("011", "Nút mờ khi phân bổ chỉ nằm ở dòng Chi phí vận chuyển", "P1",
     "Báo giá BG-TEST-004, phương thức Giảm giá tổng, mọi dòng hàng hóa và dịch vụ có Phân bổ GG = 0, "
     "riêng dòng Chi phí vận chuyển có Phân bổ GG = 500,000.",
     "1. Mở BG-TEST-004 → bấm Sửa\n"
     "2. Quan sát nút \"Xóa phân bổ\"",
     "Dòng Chi phí vận chuyển - Phân bổ GG: 500,000",
     "- ⚠️ Nút bấm được - phân bổ của dòng vận chuyển cũng được tính là dữ liệu cần xóa"),
]

SEC_II = [
    ("001", "Xóa giảm giá cho toàn bộ dòng hàng hóa", "P0",
     "Báo giá BG-TEST-001, phương thức Giảm giá mặt hàng, 10 dòng hàng hóa trong đó 2 dòng đang "
     "để GG(%) = 10. Tổng giảm giá trước khi xóa: 14,920,000. Tổng giá trị báo giá: 770,481,005.",
     "1. Mở BG-TEST-001 → bấm Sửa\n"
     "2. Bấm nút \"Xóa giảm giá\"\n"
     "3. Trên cửa sổ xác nhận bấm \"Xóa giảm giá\"\n"
     "4. Kiểm cột GG(%) và GG(đ) của cả 10 dòng",
     "2 dòng đang GG(%) = 10",
     "- Cột GG(%) và GG(đ) của TẤT CẢ 10 dòng đều về 0\n"
     "- Thông báo xanh \"Đã xóa toàn bộ dữ liệu giảm giá\"\n"
     "- Tổng giảm giá về 0, Tổng giá trị báo giá thành 785,401,005 (tăng đúng 14,920,000)\n"
     "- Nút \"Xóa giảm giá\" tự chuyển sang mờ"),

    ("002", "Xóa giảm giá cho cả dòng hàng hóa lẫn dòng dịch vụ", "P0",
     "Báo giá BG-TEST-003: 3 dòng hàng hóa có GG(%) = 8 và 2 dòng dịch vụ có GG(đ) = 500,000 mỗi dòng. "
     "Phương thức Giảm giá mặt hàng.",
     "1. Mở BG-TEST-003 → bấm Sửa\n"
     "2. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "3. Kiểm lần lượt nhóm Hàng hóa rồi nhóm Dịch vụ",
     "3 dòng hàng hóa GG(%) = 8; 2 dòng dịch vụ GG(đ) = 500,000",
     "- ⚠️ Cả nhóm Hàng hóa VÀ nhóm Dịch vụ đều về 0 - dễ sót nhóm Dịch vụ\n"
     "- Không dòng nào bị xóa khỏi bảng, chỉ giá trị giảm giá về 0"),

    ("003", "Xóa giảm giá khi nhập bằng số tiền thay vì phần trăm", "P0",
     "Báo giá BG-TEST-005: 2 dòng nhập GG bằng cột GG(đ) (lần lượt 1,200,000 và 3,660,000), "
     "không nhập GG(%).",
     "1. Mở BG-TEST-005 → bấm Sửa\n"
     "2. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "3. Kiểm cả 2 cột GG(%) và GG(đ)",
     "Dòng 1 - GG(đ): 1,200,000; Dòng 2 - GG(đ): 3,660,000",
     "- Cả GG(%) và GG(đ) của 2 dòng về 0\n"
     "- Ô \"Đơn giá sau GG\" quay về bằng đúng Đơn giá gốc"),

    ("004", "Xóa giảm giá trên báo giá có nhiều nhóm hàng nhiều cấp", "P1",
     "Báo giá BG-TEST-006 có 3 nhóm hàng hóa lồng nhau (nhóm cha - nhóm con), mỗi nhóm 2 dòng, "
     "tất cả đang có GG(%) = 5.",
     "1. Mở BG-TEST-006 → bấm Sửa\n"
     "2. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "3. Mở hết các nhóm và kiểm từng dòng",
     "Mọi dòng: GG(%) = 5",
     "- ⚠️ Mọi dòng ở MỌI cấp nhóm đều về 0, kể cả dòng đang nằm trong nhóm bị thu gọn\n"
     "- Cấu trúc nhóm không bị thay đổi"),

    ("005", "Xóa giảm giá hai lần liên tiếp", "P2",
     "Báo giá BG-TEST-001 vừa bấm \"Xóa giảm giá\" xong, mọi giảm giá đã về 0.",
     "1. Thử bấm lại nút \"Xóa giảm giá\"",
     "—",
     "- Nút đang mờ nên không bấm được, không mở cửa sổ xác nhận\n"
     "- Không có thông báo lỗi, số liệu giữ nguyên"),

    ("006", "Hủy ở cửa sổ xác nhận thì không xóa gì", "P0",
     "Báo giá BG-TEST-001, 2 dòng đang GG(%) = 10, tổng giảm giá 14,920,000.",
     "1. Bấm nút \"Xóa giảm giá\"\n"
     "2. Trên cửa sổ xác nhận bấm \"Hủy\"\n"
     "3. Kiểm lại bảng Chi tiết sản phẩm",
     "—",
     "- Cửa sổ đóng lại, KHÔNG có thông báo nào\n"
     "- 2 dòng vẫn giữ nguyên GG(%) = 10, tổng giảm giá vẫn 14,920,000"),

    ("007", "Đóng cửa sổ xác nhận bằng dấu X thì không xóa gì", "P1",
     "Báo giá BG-TEST-001, 2 dòng đang GG(%) = 10.",
     "1. Bấm nút \"Xóa giảm giá\"\n"
     "2. Bấm dấu X ở góc phải cửa sổ xác nhận\n"
     "3. Kiểm lại bảng",
     "—",
     "- Dữ liệu giảm giá giữ nguyên như trước khi bấm"),
]

SEC_III = [
    ("001", "Xóa phân bổ đưa cột Phân bổ GG của mọi dòng về 0", "P0",
     "Báo giá BG-TEST-004, phương thức Giảm giá tổng, 1 khoản giảm giá 20,000,000 đã phân bổ tự động "
     "cho 6 dòng, thêm 500,000 phân bổ cho dòng Chi phí vận chuyển. Đã phân bổ: 20,500,000. "
     "Tổng giá trị báo giá: 765,401,005.",
     "1. Mở BG-TEST-004 → bấm Sửa\n"
     "2. Bấm nút \"Xóa phân bổ\"\n"
     "3. Trên cửa sổ xác nhận bấm \"Xóa phân bổ\"\n"
     "4. Kiểm cột Phân bổ GG của cả 6 dòng và dòng Chi phí vận chuyển",
     "Đã phân bổ: 20,500,000 (6 dòng + vận chuyển 500,000)",
     "- Cột Phân bổ GG của cả 6 dòng về 0\n"
     "- ⚠️ Dòng \"Chi phí vận chuyển\" cũng về 0 - đây là chỗ dễ bị sót nhất\n"
     "- Dòng tổng hiện \"Đã phân bổ 0\"\n"
     "- Tổng giá trị báo giá thành 785,401,005\n"
     "- Thông báo xanh \"Đã xóa toàn bộ phân bổ giảm giá\""),

    ("002", "Bảng khoản giảm giá tổng KHÔNG bị xóa", "P0",
     "Báo giá BG-TEST-004 có 1 khoản giảm giá tổng 20,000,000 (có loại giảm giá và ghi chú kèm theo), "
     "đã phân bổ hết.",
     "1. Bấm \"Xóa phân bổ\" → xác nhận\n"
     "2. Kiểm bảng khoản giảm giá tổng",
     "1 khoản: 20,000,000",
     "- ⚠️ Bảng khoản giảm giá tổng GIỮ NGUYÊN đủ 1 dòng 20,000,000, kèm loại giảm giá và ghi chú\n"
     "- Ô \"Tổng giảm giá\" vẫn là 20,000,000\n"
     "- Đây là hành vi ĐÚNG theo yêu cầu, không phải lỗi thiếu xóa"),

    ("003", "Nút Phân bổ tự động hiện lại sau khi xóa phân bổ", "P0",
     "Báo giá BG-TEST-004 đang phân bổ khớp hoàn toàn nên nút \"Phân bổ tự động\" đang ẩn.",
     "1. Bấm \"Xóa phân bổ\" → xác nhận\n"
     "2. Quan sát khu vực khoản giảm giá tổng",
     "—",
     "- Nút \"Phân bổ tự động\" hiện trở lại\n"
     "- Dòng cảnh báo lệch hiện dạng \"Đã phân bổ 0 / Tổng giảm giá 20,000,000\""),

    ("004", "Phân bổ lại sau khi xóa", "P0",
     "Báo giá BG-TEST-004 vừa bấm \"Xóa phân bổ\", các khoản giảm giá còn nguyên.",
     "1. Bấm \"Phân bổ tự động\"\n"
     "2. Kiểm cột Phân bổ GG và dòng cảnh báo lệch",
     "Khoản giảm giá: 20,000,000",
     "- Phân bổ chia lại đủ 20,000,000 cho các dòng\n"
     "- Dòng cảnh báo lệch biến mất, nút \"Phân bổ tự động\" ẩn đi\n"
     "- Nút \"Xóa phân bổ\" bấm được trở lại"),

    ("005", "Xóa phân bổ khi người dùng tự sửa tay từng dòng", "P1",
     "Báo giá BG-TEST-007: người dùng không dùng phân bổ tự động mà gõ tay cột Phân bổ GG cho 3 dòng "
     "(lần lượt 1,000,000 / 2,000,000 / 3,500,000).",
     "1. Bấm \"Xóa phân bổ\" → xác nhận\n"
     "2. Kiểm cả 3 dòng",
     "3 dòng gõ tay: 1,000,000 / 2,000,000 / 3,500,000",
     "- Cả 3 dòng về 0 bất kể phân bổ do gõ tay hay do phân bổ tự động"),

    ("006", "Hủy ở cửa sổ xác nhận Xóa phân bổ", "P0",
     "Báo giá BG-TEST-004, Đã phân bổ 20,500,000.",
     "1. Bấm nút \"Xóa phân bổ\"\n"
     "2. Bấm \"Hủy\"\n"
     "3. Kiểm lại cột Phân bổ GG",
     "—",
     "- Toàn bộ giá trị phân bổ giữ nguyên, kể cả dòng Chi phí vận chuyển"),

    ("007", "Xóa phân bổ không đụng tới cột GG(%) / GG(đ) của dòng", "P1",
     "Báo giá BG-TEST-008 từng dùng Giảm giá mặt hàng (còn số liệu ở cột GG) rồi chuyển sang "
     "Giảm giá tổng.",
     "1. Kiểm cột GG(%) / GG(đ) trước khi bấm\n"
     "2. Bấm \"Xóa phân bổ\" → xác nhận\n"
     "3. Kiểm lại cột GG(%) / GG(đ)",
     "—",
     "- Chỉ cột Phân bổ GG bị đưa về 0\n"
     "- Cột GG(%) / GG(đ) giữ nguyên trạng thái trước khi bấm"),
]

SEC_IV = [
    ("001", "Nội dung cửa sổ xác nhận khi xóa Giảm giá mặt hàng", "P0",
     "Báo giá BG-TEST-001, phương thức Giảm giá mặt hàng, đang có dữ liệu giảm giá.",
     "1. Bấm nút \"Xóa giảm giá\"\n"
     "2. Đọc kỹ tiêu đề, nội dung và hai nút trên cửa sổ",
     "—",
     "- Tiêu đề: \"Xóa dữ liệu giảm giá\"\n"
     "- Nội dung: \"Bạn có chắc chắn muốn xóa toàn bộ dữ liệu giảm giá?\"\n"
     "- Hai nút: \"Hủy\" và \"Xóa giảm giá\" (nút Xóa màu đỏ, có biểu tượng cục tẩy)"),

    ("002", "Nội dung cửa sổ xác nhận khi xóa phân bổ Giảm giá tổng", "P0",
     "Báo giá BG-TEST-004, phương thức Giảm giá tổng, đang có phân bổ.",
     "1. Bấm nút \"Xóa phân bổ\"\n"
     "2. Đọc kỹ tiêu đề, nội dung và hai nút",
     "—",
     "- Tiêu đề: \"Xóa phân bổ giảm giá\"\n"
     "- Nội dung: \"Bạn có chắc chắn muốn xóa toàn bộ giá trị phân bổ giảm giá? Tất cả giá trị tại cột "
     "Phân bổ GG sẽ được đặt về 0\"\n"
     "- Hai nút: \"Hủy\" và \"Xóa phân bổ\" (nút Xóa màu đỏ)"),

    ("003", "Cửa sổ xác nhận dùng đúng khuôn chung của hệ thống", "P2",
     "Bất kỳ báo giá nào đang có dữ liệu giảm giá.",
     "1. Bấm nút xóa\n"
     "2. So khuôn cửa sổ với cửa sổ xác nhận xóa ở màn danh sách báo giá",
     "—",
     "- Cùng khuôn: biểu tượng tròn ở đầu tiêu đề, nút nằm góc dưới bên phải, bấm ra ngoài hoặc "
     "bấm phím Esc thì cửa sổ đóng mà không xóa gì"),
]

SEC_V = [
    ("001", "Đơn giá sau GG tính lại sau khi xóa giảm giá", "P0",
     "Báo giá BG-TEST-001: dòng 1 Đơn giá 10,000,000, GG(%) = 10 nên Đơn giá sau GG đang là 9,000,000.",
     "1. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "2. Đọc ô \"Đơn giá sau GG\" của dòng 1",
     "Dòng 1 - Đơn giá: 10,000,000; GG(%): 10",
     "- Đơn giá sau GG quay về đúng 10,000,000\n"
     "- Không phải bấm thêm nút nào để số liệu tự cập nhật"),

    ("002", "Thành tiền bán và tiền thuế tính lại", "P0",
     "Cùng dữ liệu trên, dòng 1 Số lượng 5, thuế 10%.",
     "1. Ghi lại Thành tiền bán và tiền thuế của dòng 1 trước khi xóa\n"
     "2. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "3. Đọc lại 2 ô đó",
     "Số lượng: 5; Thuế: 10%",
     "- Thành tiền bán = 50,000,000\n"
     "- Tiền thuế = 5,000,000\n"
     "- Hai số khớp với đơn giá gốc, không còn dấu vết giảm giá"),

    ("003", "Tổng giá trị báo giá tính lại", "P0",
     "Báo giá BG-TEST-001, tổng giảm giá 14,920,000, Tổng giá trị báo giá 770,481,005.",
     "1. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "2. Đọc ô \"Tổng giá trị báo giá\"",
     "—",
     "- Tổng giá trị báo giá tăng đúng bằng phần giảm giá bị xóa, thành 785,401,005"),

    ("004", "Tỷ suất lợi nhuận tính lại", "P1",
     "Báo giá BG-TEST-001, tài khoản có quyền \"Xem giá vốn hàng hoá\" để nhìn được tỷ suất.",
     "1. Ghi lại Tỷ suất lợi nhuận trước khi xóa\n"
     "2. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "3. Đọc lại Tỷ suất lợi nhuận",
     "—",
     "- Tỷ suất lợi nhuận tăng lên tương ứng với giá bán mới\n"
     "- Không hiện dấu gạch ngang hay ô trống"),

    ("005", "Số liệu hiển thị đúng định dạng sau khi tính lại", "P1",
     "Báo giá BG-TEST-001 vừa xóa giảm giá xong.",
     "1. Đọc các ô số tiền trên bảng và ở khối tổng",
     "—",
     "- ⚠️ Số tiền dùng dấu phẩy ngăn cách hàng nghìn và dấu chấm cho phần thập phân "
     "(ví dụ 785,401,005)\n"
     "- Ô về 0 hiển thị \"0\", không để trống, không hiện chữ lạ"),

    ("006", "Báo giá dùng ngoại tệ tính lại đúng", "P1",
     "Báo giá BG-TEST-009 dùng loại tiền tệ khác đồng Việt Nam, có tỷ giá quy đổi, 3 dòng đang "
     "có GG(%) = 7.",
     "1. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "2. Kiểm các ô số tiền theo cả 2 loại tiền",
     "Loại tiền tệ: khác đồng Việt Nam",
     "- Giá trị theo ngoại tệ và giá trị quy đổi đều tính lại đúng\n"
     "- Ô Tỷ giá giữ nguyên, không bị đặt lại"),
]

SEC_VI = [
    ("001", "Lưu sau khi xóa giảm giá rồi mở lại", "P0",
     "Báo giá BG-TEST-001 vừa bấm \"Xóa giảm giá\", chưa bấm Lưu.",
     "1. Bấm nút Lưu\n"
     "2. Quay lại màn danh sách, mở lại BG-TEST-001\n"
     "3. Kiểm cột GG(%), GG(đ) và Tổng giá trị báo giá",
     "—",
     "- Mọi dòng vẫn ở 0, Tổng giá trị báo giá đúng bằng số đã thấy trước khi Lưu\n"
     "- Không có dòng nào bị mất khỏi bảng Chi tiết sản phẩm"),

    ("002", "Lưu sau khi xóa phân bổ rồi mở lại", "P0",
     "Báo giá BG-TEST-004 vừa bấm \"Xóa phân bổ\", chưa bấm Lưu.",
     "1. Bấm nút Lưu\n"
     "2. Mở lại BG-TEST-004\n"
     "3. Kiểm cột Phân bổ GG, dòng Chi phí vận chuyển và bảng khoản giảm giá tổng",
     "—",
     "- Phân bổ mọi dòng và dòng Chi phí vận chuyển vẫn là 0\n"
     "- ⚠️ Bảng khoản giảm giá tổng vẫn còn đủ khoản 20,000,000\n"
     "- Dòng cảnh báo lệch \"Đã phân bổ 0 / Tổng giảm giá 20,000,000\" hiện lại"),

    ("003", "Thoát KHÔNG lưu sau khi xóa thì dữ liệu cũ còn nguyên", "P0",
     "Báo giá BG-TEST-001 có 2 dòng GG(%) = 10, đã bấm \"Xóa giảm giá\" nhưng chưa Lưu.",
     "1. Bấm nút \"Quay lại\"\n"
     "2. Trên cảnh báo chưa lưu chọn thoát\n"
     "3. Mở lại BG-TEST-001",
     "—",
     "- ⚠️ Dữ liệu giảm giá cũ còn nguyên (2 dòng GG(%) = 10) vì thao tác xóa chỉ tác động lên màn "
     "đang nhập"),

    ("004", "Cảnh báo chưa lưu xuất hiện sau khi xóa", "P1",
     "Báo giá BG-TEST-001 vừa mở màn Sửa, chưa sửa gì.",
     "1. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "2. Bấm \"Quay lại\"",
     "—",
     "- Hệ thống cảnh báo dữ liệu chưa được lưu, hỏi có chắc muốn thoát không\n"
     "- Chọn ở lại thì vẫn thấy kết quả vừa xóa"),

    ("005", "Tạo mới: xóa giảm giá rồi lưu báo giá mới", "P1",
     "Đang ở màn Tạo mới, đã nhập đủ thông tin bắt buộc, thêm 3 dòng hàng hóa có GG(%) = 5.",
     "1. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "2. Bấm Lưu\n"
     "3. Mở lại báo giá vừa tạo",
     "3 dòng GG(%) = 5",
     "- Báo giá được tạo với giảm giá bằng 0 ở mọi dòng\n"
     "- Tổng giá trị báo giá đúng bằng tổng chưa giảm giá"),
]

SEC_VII = [
    ("001", "Đổi phương thức từ Giảm giá tổng sang Giảm giá mặt hàng", "P0",
     "Báo giá BG-TEST-004 đang ở Giảm giá tổng, đã phân bổ 20,000,000 cho các dòng và 500,000 cho "
     "dòng Chi phí vận chuyển.",
     "1. Đổi ô phương thức giảm giá sang \"Giảm giá mặt hàng\"\n"
     "2. Kiểm cột Phân bổ GG của mọi dòng\n"
     "3. Kiểm riêng dòng \"Chi phí vận chuyển\"\n"
     "4. Kiểm Tổng giá trị báo giá",
     "Phân bổ: 20,000,000 + vận chuyển 500,000",
     "- Mọi giá trị phân bổ về 0\n"
     "- ⚠️ Dòng Chi phí vận chuyển cũng về 0 (trước đây bị sót, để lại số dư làm lệch tổng tiền)\n"
     "- Tổng giá trị báo giá tính lại đúng, không còn trừ phần vận chuyển"),

    ("002", "Đổi phương thức từ Giảm giá mặt hàng sang Giảm giá tổng", "P0",
     "Báo giá BG-TEST-001 đang ở Giảm giá mặt hàng, 2 dòng GG(%) = 10.",
     "1. Đổi phương thức sang \"Giảm giá tổng\"\n"
     "2. Kiểm cột GG(%) / GG(đ) và bảng khoản giảm giá tổng",
     "—",
     "- Cột GG(%) và GG(đ) của mọi dòng về 0\n"
     "- Bảng khoản giảm giá tổng trống, chờ nhập mới\n"
     "- Chữ trên nút đổi thành \"Xóa phân bổ\" và đang ở trạng thái mờ"),

    ("003", "Đổi phương thức rồi đổi ngược lại", "P1",
     "Báo giá BG-TEST-004 đang ở Giảm giá tổng có phân bổ.",
     "1. Đổi sang \"Giảm giá mặt hàng\"\n"
     "2. Đổi ngược về \"Giảm giá tổng\"\n"
     "3. Kiểm toàn bộ số liệu giảm giá và Tổng giá trị báo giá",
     "—",
     "- Không còn số dư giảm giá nào sót lại ở bất kỳ cột nào\n"
     "- Tổng giá trị báo giá bằng đúng tổng khi không có giảm giá"),

    ("004", "Bỏ trống phương thức giảm giá", "P2",
     "Báo giá BG-TEST-001 đang ở Giảm giá mặt hàng có dữ liệu giảm giá.",
     "1. Xóa lựa chọn ở ô phương thức giảm giá\n"
     "2. Quan sát thanh công cụ và số liệu",
     "—",
     "- Nút xóa biến mất\n"
     "- Không còn giá trị giảm giá nào trên bảng, Tổng giá trị báo giá tính lại đúng"),
]

SEC_VIII = [
    ("001", "Báo giá không có dòng hàng hóa nào", "P1",
     "Báo giá mới tạo, chưa thêm dòng nào vào bảng Chi tiết sản phẩm, đã chọn Giảm giá mặt hàng.",
     "1. Quan sát nút xóa",
     "—",
     "- Nút hiện nhưng mờ, bấm không phản ứng\n"
     "- Không có lỗi trắng trang"),

    ("002", "Báo giá chỉ có dòng Chi phí vận chuyển", "P2",
     "Báo giá chỉ nhập Chi phí vận chuyển 5,000,000, không có dòng hàng hóa hay dịch vụ, "
     "phương thức Giảm giá tổng, đã phân bổ 1,000,000 cho dòng vận chuyển.",
     "1. Bấm \"Xóa phân bổ\" → xác nhận\n"
     "2. Kiểm dòng Chi phí vận chuyển",
     "Chi phí vận chuyển - Phân bổ GG: 1,000,000",
     "- Phân bổ của dòng vận chuyển về 0\n"
     "- Chi phí vận chuyển 5,000,000 giữ nguyên (chỉ phân bổ bị xóa)"),

    ("003", "Báo giá nhiều dòng", "P1",
     "Báo giá BG-TEST-010 có 120 dòng hàng hóa, tất cả đang có GG(%) = 3.",
     "1. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "2. Cuộn hết bảng và kiểm ngẫu nhiên 10 dòng ở đầu, giữa, cuối\n"
     "3. Đo thời gian từ lúc xác nhận tới lúc số liệu cập nhật",
     "120 dòng GG(%) = 3",
     "- Mọi dòng đều về 0, không sót dòng nào\n"
     "- Màn hình không đứng quá 2 giây, không hiện cảnh báo trình duyệt"),

    ("004", "Xóa giảm giá trên báo giá đang ở trạng thái không cho sửa", "P0",
     "Báo giá BG-TEST-011 đang ở trạng thái đã duyệt / đã khóa, không cho chỉnh sửa.",
     "1. Mở BG-TEST-011 ở màn Chi tiết\n"
     "2. Tìm nút xóa giảm giá trên thanh công cụ",
     "—",
     "- ⚠️ Không có nút xóa giảm giá vì màn chỉ xem không cho sửa\n"
     "- Nút Sửa cũng không hiện"),

    ("005", "Bấm liên tiếp nhiều lần vào nút xóa", "P2",
     "Báo giá BG-TEST-001 đang có dữ liệu giảm giá.",
     "1. Bấm nhanh 3 lần liên tiếp vào nút \"Xóa giảm giá\"\n"
     "2. Quan sát số cửa sổ xác nhận mở ra",
     "—",
     "- Chỉ 1 cửa sổ xác nhận mở ra, không chồng nhiều lớp\n"
     "- Sau khi xác nhận chỉ hiện 1 thông báo thành công"),

    ("006", "Xóa giảm giá trên báo giá có bản sao từ báo giá khác", "P2",
     "Báo giá BG-TEST-012 được tạo bằng chức năng sao chép từ BG-TEST-001, mang theo đầy đủ "
     "dữ liệu giảm giá.",
     "1. Mở BG-TEST-012 → bấm Sửa\n"
     "2. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "3. Mở lại BG-TEST-001 để đối chiếu",
     "—",
     "- BG-TEST-012 về 0 toàn bộ\n"
     "- ⚠️ BG-TEST-001 (bản gốc) KHÔNG bị ảnh hưởng"),
]

SEC_IX = [
    ("001", "Luồng đầy đủ với Giảm giá mặt hàng", "P0",
     "Tài khoản A có quyền giảm giá và có dự án được phân công để tạo báo giá.",
     "1. Vào phân hệ Giao việc → nhóm Báo giá → bấm \"Báo giá\" → \"Thêm mới\"\n"
     "2. Nhập thông tin chung, chọn phương thức \"Giảm giá mặt hàng\"\n"
     "3. Thêm 5 dòng hàng hóa và 2 dòng dịch vụ, nhập GG(%) = 10 cho tất cả\n"
     "4. Ghi lại Tổng giá trị báo giá\n"
     "5. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "6. Bấm Lưu\n"
     "7. Mở lại báo giá vừa tạo",
     "7 dòng, GG(%) = 10",
     "- Sau khi xóa: mọi giảm giá về 0, Tổng giá trị báo giá tăng đúng bằng phần giảm giá\n"
     "- Sau khi Lưu và mở lại: số liệu giữ đúng như lúc Lưu\n"
     "- Không có lỗi ở bất kỳ bước nào"),

    ("002", "Luồng đầy đủ với Giảm giá tổng", "P0",
     "Tài khoản A có quyền giảm giá, đang ở màn Tạo mới báo giá.",
     "1. Chọn phương thức \"Giảm giá tổng\"\n"
     "2. Thêm 5 dòng hàng hóa, nhập Chi phí vận chuyển 5,000,000\n"
     "3. Thêm 1 khoản giảm giá tổng 10,000,000, bấm \"Phân bổ tự động\"\n"
     "4. Gõ tay 500,000 vào cột Phân bổ GG của dòng Chi phí vận chuyển\n"
     "5. Bấm \"Xóa phân bổ\" → xác nhận\n"
     "6. Bấm \"Phân bổ tự động\" lần nữa\n"
     "7. Bấm Lưu và mở lại",
     "Khoản giảm giá: 10,000,000; vận chuyển: 5,000,000",
     "- Bước 5: mọi phân bổ kể cả dòng vận chuyển về 0, khoản giảm giá 10,000,000 còn nguyên\n"
     "- Bước 6: phân bổ lại đủ 10,000,000, cảnh báo lệch biến mất\n"
     "- Bước 7: mở lại thấy đúng số liệu đã phân bổ lại"),

    ("003", "Luồng người dùng đổi ý nhiều lần", "P1",
     "Tài khoản A đang sửa báo giá BG-TEST-001.",
     "1. Nhập giảm giá cho 3 dòng\n"
     "2. Bấm \"Xóa giảm giá\" → Hủy\n"
     "3. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "4. Nhập lại giảm giá cho 1 dòng\n"
     "5. Bấm \"Xóa giảm giá\" → xác nhận\n"
     "6. Bấm Lưu",
     "—",
     "- Bước 2: dữ liệu còn nguyên\n"
     "- Bước 3 và 5: về 0 đúng như mong đợi, nút tự mờ lại sau mỗi lần xóa\n"
     "- Bước 6: lưu thành công, mở lại thấy giảm giá bằng 0"),
]

SECTIONS = [
    ("I", "HIỂN THỊ NÚT & ĐIỀU KIỆN BẬT / TẮT", SEC_I),
    ("II", "XÓA GIẢM GIÁ - PHƯƠNG THỨC GIẢM GIÁ MẶT HÀNG", SEC_II),
    ("III", "XÓA PHÂN BỔ - PHƯƠNG THỨC GIẢM GIÁ TỔNG", SEC_III),
    ("IV", "CỬA SỔ XÁC NHẬN", SEC_IV),
    ("V", "TÍNH LẠI SỐ LIỆU SAU KHI XÓA", SEC_V),
    ("VI", "LƯU & MỞ LẠI BÁO GIÁ", SEC_VI),
    ("VII", "ĐỔI PHƯƠNG THỨC GIẢM GIÁ", SEC_VII),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU & TRƯỜNG HỢP BIÊN", SEC_VIII),
    ("IX", "LUỒNG ĐẦU CUỐI", SEC_IX),
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testcase.xlsx")
    build(
        output_file=out,
        sheet_name="Trang tính1",
        feature_name="Xóa dữ liệu giảm giá hàng loạt ở Báo giá",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
