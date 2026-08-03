"""Sinh CSV testcase issue #10565 (Tab Báo giá - Đồng bộ hàng tạm sang ERP).

Output: .plans/sync-hang-tam/testcase-issue-10565.csv
Cột theo đúng tab 'Testcase - Tạo mới dự án tiền khả thi (TKT)' (gid=739303646):
A Module | B Nhóm chức năng | C TC ID | D Chức năng | E Priority | F Tiền điều kiện
| G Bước thực hiện | H Test Data | I Expected Result (chi tiết)
"""
import csv

OUT = ".plans/sync-hang-tam/testcase-issue-10565.csv"
NCOL = 19
GROUP = "Tab Báo giá - Đồng bộ hàng tạm"
MODULE = "Dự án tiền KT"

HEADER_BLOCK = ("UPDATE NỘI DUNG 31/07/2026", "", "", "Task http://quanly.dnsmedia.vn/issues/10565")

# (tc_id, chức năng, priority, tiền điều kiện, bước thực hiện, test data, expected)
TCS = [
    ("TC-ROLE-241", "Không hiển thị banner đồng bộ hàng tạm khi dự án chưa có báo giá trúng thầu", "P0",
     "Dự án TKT A có 2 báo giá trạng thái Đã duyệt / Chờ duyệt, chưa có báo giá Trúng thầu",
     "1. Mở chi tiết dự án A.\n2. Chọn tab Báo giá.\n3. Quan sát khu vực phía trên bảng danh sách.",
     "Dự án A: 0 báo giá Trúng thầu",
     "Không hiển thị banner \"Đồng bộ hàng tạm sang ERP\"; không có nút Gửi duyệt hàng tạm."),

    ("TC-ROLE-242", "AC1 - Báo giá Trúng thầu chỉ có hàng hóa chuẩn ERP thì không hiển thị nút Gửi duyệt hàng tạm", "P0",
     "Dự án B có 1 báo giá Trúng thầu gồm 5 dòng hàng, tất cả đều chọn từ Core ERP (có mã hàng ERP)",
     "1. Mở chi tiết dự án B → tab Báo giá.\n2. Quan sát banner và khu vực nút.",
     "Báo giá BG-B: 5/5 dòng là hàng ERP, 0 hàng tạm",
     "Không hiển thị banner đồng bộ hàng tạm và không hiển thị nút \"Gửi duyệt hàng tạm\"."),

    ("TC-ROLE-243", "AC2 - Báo giá Trúng thầu có hàng tạm thì hiển thị nút Gửi duyệt hàng tạm", "P0",
     "Dự án C có 1 báo giá Trúng thầu gồm 5 dòng: 3 hàng ERP + 2 hàng tạm nhập tay; user đăng nhập là Sale phụ trách dự án C",
     "1. Mở chi tiết dự án C → tab Báo giá.\n2. Quan sát banner phía trên bảng.",
     "Báo giá BG-C: 2 hàng tạm chưa gửi",
     "- Hiển thị banner \"Báo giá trúng thầu BG-C — Đồng bộ hàng tạm sang ERP\".\n- Hiển thị nút \"Gửi duyệt hàng tạm\"."),

    ("TC-ROLE-244", "Kiểm tra badge trạng thái và tiến độ khi chưa gửi duyệt", "P0",
     "Như TC-ROLE-243 (báo giá BG-C có 2 hàng tạm chưa gửi)",
     "1. Mở tab Báo giá của dự án C.\n2. Quan sát badge trạng thái và dòng tiến độ trên banner.",
     "2 hàng tạm chưa gửi",
     "- Badge hiển thị \"Chưa đồng bộ\" (màu xám).\n- Dòng tiến độ hiển thị \"2 hàng tạm chờ gửi\".\n- Chưa hiển thị dòng Mã phiếu."),

    ("TC-ROLE-245", "Kiểm tra quyền - chỉ Sale phụ trách dự án nhìn thấy nút Gửi duyệt hàng tạm", "P0",
     "Dự án C có báo giá Trúng thầu chứa hàng tạm; đăng nhập bằng user KHÔNG phải Sale chính của dự án C (VD: user P3 hoặc sale dự án khác)",
     "1. Mở chi tiết dự án C → tab Báo giá.\n2. Quan sát banner.",
     "User: không phải Sale phụ trách",
     "- Banner vẫn hiển thị trạng thái đồng bộ (chỉ đọc).\n- KHÔNG hiển thị nút \"Gửi duyệt hàng tạm\" và \"Cập nhật kết quả duyệt\"."),

    ("TC-ROLE-246", "Kiểm tra backend chặn khi user không phải Sale phụ trách gọi API gửi duyệt", "P0",
     "Dự án C có báo giá Trúng thầu chứa hàng tạm; đăng nhập user không phải Sale phụ trách",
     "1. Gọi trực tiếp API POST assign/prospective-projects/{id}/send-tmp-approval.\n2. Quan sát phản hồi.",
     "projectId = dự án C",
     "Trả về HTTP 403 với thông báo \"Bạn không phải Sale phụ trách dự án này\"; trạng thái đồng bộ không thay đổi."),

    ("TC-ROLE-247", "Kiểm tra popup xác nhận khi bấm Gửi duyệt hàng tạm", "P1",
     "Đăng nhập bằng Sale phụ trách dự án C; báo giá BG-C có 2 hàng tạm chưa gửi",
     "1. Mở tab Báo giá.\n2. Bấm nút \"Gửi duyệt hàng tạm\".\n3. Quan sát popup.",
     "-",
     "Hiển thị popup tiêu đề \"Xác nhận\", nội dung \"Gửi duyệt hàng tạm của báo giá trúng thầu sang ERP?\", 2 nút \"Gửi duyệt\" và \"Huỷ\"."),

    ("TC-ROLE-248", "Bấm Huỷ trên popup xác nhận", "P1",
     "Đang mở popup xác nhận gửi duyệt hàng tạm",
     "1. Bấm nút \"Huỷ\".\n2. Quan sát banner.",
     "-",
     "- Popup đóng, không gọi API.\n- Badge vẫn là \"Chưa đồng bộ\", nút \"Gửi duyệt hàng tạm\" vẫn hiển thị."),

    ("TC-ROLE-249", "AC3 - Gửi duyệt thành công thì trạng thái chuyển Đang đồng bộ sang ERP", "P0",
     "Sale phụ trách dự án C; báo giá BG-C có 2 hàng tạm chưa gửi; kết nối ERP hoạt động",
     "1. Bấm \"Gửi duyệt hàng tạm\".\n2. Bấm \"Gửi duyệt\" trên popup.\n3. Quan sát thông báo và banner.",
     "BG-C: 2 hàng tạm",
     "- Toast thành công \"Đã gửi duyệt hàng tạm sang ERP\".\n- Badge chuyển thành \"Đang đồng bộ sang ERP\" (màu vàng).\n- Tiến độ hiển thị \"0/2 hàng tạm đã duyệt\"."),

    ("TC-ROLE-250", "Ẩn nút Gửi duyệt và hiện nút Cập nhật kết quả duyệt sau khi gửi", "P0",
     "Báo giá BG-C vừa gửi duyệt thành công (trạng thái Đang đồng bộ sang ERP)",
     "1. Quan sát khu vực nút trên banner.",
     "-",
     "- Không còn nút \"Gửi duyệt hàng tạm\".\n- Hiển thị nút \"Cập nhật kết quả duyệt\"."),

    ("TC-ROLE-251", "Kiểm tra hiển thị mã phiếu yêu cầu duyệt hàng tạm trên banner", "P1",
     "Báo giá BG-C đã gửi duyệt thành công, ERP trả về mã phiếu (VD PYCDHT-2026-00012)",
     "1. Quan sát dòng \"Mã phiếu\" trên banner.\n2. Bấm vào mã phiếu.",
     "Mã phiếu: PYCDHT-2026-00012",
     "- Hiển thị \"Mã phiếu: PYCDHT-2026-00012\" dạng liên kết.\n- Bấm vào mở tab mới sang màn chi tiết phiếu yêu cầu duyệt hàng tạm trên ERP."),

    ("TC-ROLE-252", "AC4 - ERP sinh phiếu Yêu cầu duyệt hàng tạm ở trạng thái Đang tạo", "P0",
     "Báo giá BG-C vừa gửi duyệt thành công",
     "1. Đăng nhập ERP.\n2. Mở danh sách Yêu cầu duyệt hàng tạm.\n3. Tìm phiếu vừa sinh theo mã hiển thị trên HRM.",
     "Mã phiếu: PYCDHT-2026-00012",
     "- Có 1 phiếu \"Yêu cầu duyệt hàng tạm\" mới.\n- Trạng thái phiếu = \"Đang tạo\".\n- Số dòng hàng tạm trên phiếu = 2 (đúng số hàng tạm của báo giá)."),

    ("TC-ROLE-253", "AC4 - Kiểm tra ánh xạ dữ liệu từng dòng hàng tạm sang ERP", "P0",
     "Phiếu PYCDHT-2026-00012 trên ERP; đã biết dữ liệu 2 dòng hàng tạm trên báo giá BG-C (mã, tên, model, hãng, xuất xứ, ĐVT, thuộc tính, %VAT, giá dự kiến, giá báo)",
     "1. Mở chi tiết phiếu trên ERP.\n2. Đối chiếu từng trường của mỗi dòng với dữ liệu trên báo giá HRM (theo bảng QUY TẮC ÁNH XẠ HÀNG TẠM).",
     "2 dòng hàng tạm",
     "Các trường Mã hàng, Tên hàng, Model, Hãng sản xuất, Xuất xứ, Đơn vị tính, Thuộc tính hàng hoá, %VAT, Giá dự kiến (giá vốn), Giá báo khớp 100% với dữ liệu trên HRM."),

    ("TC-ROLE-254", "Kiểm tra quy đổi giá về VND khi báo giá là ngoại tệ", "P0",
     "Báo giá Trúng thầu BG-D loại tiền USD, tỷ giá 25.000, có 1 hàng tạm giá vốn 100 USD, giá báo 120 USD",
     "1. Bấm Gửi duyệt hàng tạm.\n2. Mở phiếu tương ứng trên ERP.\n3. Đối chiếu giá.",
     "Tỷ giá 25.000; 100 USD; 120 USD",
     "Trên ERP: giá dự kiến = 2.500.000 VND, giá báo = 3.000.000 VND (đã nhân tỷ giá, không giữ nguyên số ngoại tệ)."),

    ("TC-ROLE-255", "Kiểm tra báo giá VND không bị nhân sai tỷ giá", "P0",
     "Báo giá Trúng thầu BG-E loại tiền VND (tỷ giá để trống/bằng 0), có 1 hàng tạm giá vốn 1.000.000, giá báo 1.200.000",
     "1. Bấm Gửi duyệt hàng tạm.\n2. Mở phiếu trên ERP và đối chiếu giá.",
     "Tỷ giá trống; 1.000.000 / 1.200.000",
     "Trên ERP: giá dự kiến = 1.000.000, giá báo = 1.200.000 (giữ nguyên, không về 0 và không nhân sai)."),

    ("TC-ROLE-256", "AC4 - Kiểm tra thông tin nguồn (dự án, báo giá, ghi chú) trên phiếu ERP", "P1",
     "Báo giá BG-C của dự án \"Dự án C\" có ghi chú; đã gửi duyệt thành công",
     "1. Mở chi tiết phiếu trên ERP.\n2. Quan sát khu vực thông tin chung.",
     "Mã báo giá BG-C; tên dự án \"Dự án C\"",
     "Phiếu hiển thị đúng mã báo giá nguồn, tên dự án nguồn và ghi chú lấy từ báo giá HRM."),

    ("TC-ROLE-257", "AC5 - User thuộc bộ phận có thẩm quyền được sửa/duyệt phiếu", "P0",
     "Phiếu Yêu cầu duyệt hàng tạm ở trạng thái Đang tạo; đăng nhập ERP bằng user thuộc bộ phận có thẩm quyền duyệt hàng tạm",
     "1. Mở chi tiết phiếu.\n2. Quan sát các nút thao tác.",
     "User: có thẩm quyền duyệt",
     "Hiển thị và cho phép dùng chức năng Sửa / Duyệt phiếu."),

    ("TC-ROLE-258", "AC5 - User không thuộc bộ phận có thẩm quyền không được sửa/duyệt phiếu", "P0",
     "Phiếu Yêu cầu duyệt hàng tạm ở trạng thái Đang tạo; đăng nhập ERP bằng user KHÔNG thuộc bộ phận có thẩm quyền",
     "1. Mở chi tiết phiếu.\n2. Thử thao tác Sửa / Duyệt.",
     "User: không có thẩm quyền",
     "Không hiển thị (hoặc chặn) chức năng Sửa / Duyệt; hệ thống báo không có quyền, dữ liệu phiếu không đổi."),

    ("TC-ROLE-259", "AC6 - Thông báo tới người có thẩm quyền khi có yêu cầu duyệt hàng tạm mới", "P0",
     "User X thuộc bộ phận có thẩm quyền duyệt; Sale vừa bấm Gửi duyệt hàng tạm cho \"Dự án C\"",
     "1. Đăng nhập ERP bằng user X.\n2. Mở danh sách thông báo.",
     "Tên dự án: Dự án C",
     "Nhận được thông báo nội dung \"Có yêu cầu duyệt hàng tạm mới từ Dự án C\"; bấm vào mở đúng phiếu vừa tạo."),

    ("TC-ROLE-260", "Chặn gửi duyệt lần 2 khi báo giá đang ở trạng thái Đang đồng bộ", "P0",
     "Báo giá BG-C đang ở trạng thái Đang đồng bộ sang ERP",
     "1. Gọi API POST assign/quotations/{id}/send-tmp-approval cho BG-C.\n2. Quan sát phản hồi và banner trên UI.",
     "BG-C: tmp_sync_status = Đang đồng bộ",
     "- API trả lỗi \"Báo giá đã gửi duyệt hàng tạm rồi.\"\n- Không sinh thêm phiếu mới trên ERP.\n- Trạng thái, mã phiếu trên banner giữ nguyên."),

    ("TC-ROLE-261", "Chỉ gửi dòng hàng tạm, không gửi hàng hóa chuẩn ERP", "P0",
     "Báo giá Trúng thầu có 5 dòng: 3 hàng ERP + 2 hàng tạm",
     "1. Bấm Gửi duyệt hàng tạm.\n2. Mở phiếu trên ERP và đếm số dòng.",
     "3 hàng ERP + 2 hàng tạm",
     "Phiếu ERP chỉ có đúng 2 dòng (2 hàng tạm); 3 dòng hàng ERP không được đẩy sang."),

    ("TC-ROLE-262", "Chặn gửi duyệt khi báo giá chưa ở trạng thái Trúng thầu", "P0",
     "Báo giá BG-F có hàng tạm nhưng trạng thái là Đã duyệt (chưa Trúng thầu)",
     "1. Quan sát tab Báo giá.\n2. Gọi API send-tmp-approval cho BG-F.",
     "BG-F: trạng thái Đã duyệt",
     "- UI không hiển thị nút gửi duyệt cho báo giá này.\n- API trả lỗi \"Chỉ gửi duyệt hàng tạm cho báo giá Trúng thầu.\""),

    ("TC-ROLE-263", "ERP không trả kết quả tạo hàng tạm thì không đánh dấu Đang đồng bộ", "P0",
     "Báo giá BG-C có 2 hàng tạm; ERP trả về danh sách map rỗng (không tạo được hàng tạm)",
     "1. Bấm Gửi duyệt hàng tạm → xác nhận.\n2. Quan sát thông báo và banner.\n3. Bấm gửi lại lần nữa.",
     "ERP trả map rỗng",
     "- Toast lỗi \"ERP không trả về kết quả tạo hàng tạm. Vui lòng thử lại.\"\n- Badge vẫn là \"Chưa đồng bộ\", nút \"Gửi duyệt hàng tạm\" vẫn còn.\n- Vẫn gửi lại được (không bị kẹt trạng thái)."),

    ("TC-ROLE-264", "Lỗi kết nối ERP khi gửi duyệt", "P1",
     "Báo giá BG-C có hàng tạm; ERP tạm ngưng/timeout",
     "1. Bấm Gửi duyệt hàng tạm → xác nhận.\n2. Quan sát thông báo và trạng thái.",
     "ERP ngắt kết nối",
     "- Hiển thị toast lỗi (thông báo lỗi từ hệ thống, không trắng màn).\n- Trạng thái đồng bộ giữ nguyên \"Chưa đồng bộ\"."),

    ("TC-ROLE-265", "Cập nhật kết quả duyệt khi ERP mới duyệt một phần", "P0",
     "Báo giá BG-C đang đồng bộ với 2 hàng tạm; trên ERP đã duyệt 1 hàng, 1 hàng còn Đang tạo",
     "1. Bấm nút \"Cập nhật kết quả duyệt\".\n2. Quan sát thông báo và tiến độ trên banner.",
     "1/2 hàng tạm đã duyệt",
     "- Toast \"Đã cập nhật kết quả duyệt\".\n- Tiến độ hiển thị \"1/2 hàng tạm đã duyệt\".\n- Badge vẫn là \"Đang đồng bộ sang ERP\"."),

    ("TC-ROLE-266", "Cập nhật kết quả duyệt khi ERP đã duyệt hết hàng tạm", "P0",
     "Báo giá BG-C đang đồng bộ với 2 hàng tạm; ERP đã duyệt cả 2 và sinh mã hàng chính thức",
     "1. Bấm \"Cập nhật kết quả duyệt\".\n2. Quan sát banner.",
     "2/2 hàng tạm đã duyệt",
     "- Badge chuyển thành \"Đã đồng bộ\" (màu xanh).\n- Tiến độ hiển thị \"2/2 hàng tạm đã tạo trên ERP\".\n- Ẩn nút \"Cập nhật kết quả duyệt\"."),

    ("TC-ROLE-267", "Cảnh báo khi ERP từ chối hàng tạm", "P0",
     "Báo giá BG-C đang đồng bộ với 2 hàng tạm; ERP từ chối 1 hàng",
     "1. Bấm \"Cập nhật kết quả duyệt\".\n2. Quan sát thông báo và trạng thái.",
     "1 hàng bị từ chối",
     "- Hiển thị cảnh báo \"Có 1 hàng tạm bị từ chối\".\n- Badge vẫn là \"Đang đồng bộ sang ERP\" (chưa chuyển Đã đồng bộ)."),

    ("TC-ROLE-268", "Tự động kéo kết quả duyệt khi mở tab Báo giá", "P1",
     "Báo giá BG-C đang ở trạng thái Đang đồng bộ; trên ERP vừa duyệt thêm 1 hàng tạm (chưa bấm cập nhật trên HRM)",
     "1. Rời khỏi tab Báo giá và mở lại (hoặc tải lại màn chi tiết dự án → tab Báo giá).\n2. Quan sát tiến độ.",
     "ERP vừa duyệt thêm 1 hàng",
     "Tiến độ trên banner tự cập nhật theo kết quả mới nhất mà không cần bấm \"Cập nhật kết quả duyệt\"."),

    ("TC-ROLE-269", "Dòng hàng tạm được gắn mã hàng chính thức sau khi duyệt", "P0",
     "Báo giá BG-C đã đồng bộ xong (badge Đã đồng bộ)",
     "1. Mở chi tiết báo giá BG-C.\n2. Quan sát 2 dòng hàng vốn là hàng tạm.",
     "2 hàng tạm đã duyệt",
     "2 dòng này đã gắn mã hàng hóa chính thức của ERP, không còn được coi là hàng tạm."),

    ("TC-ROLE-270", "Gửi duyệt khi dự án có nhiều báo giá trúng thầu chứa hàng tạm", "P1",
     "Dự án G có 2 báo giá Trúng thầu, mỗi báo giá có hàng tạm chưa gửi",
     "1. Bấm \"Gửi duyệt hàng tạm\" trên banner.\n2. Quan sát thông báo.\n3. Kiểm tra trên ERP.",
     "2 báo giá trúng thầu",
     "- Thông báo \"Đã gửi duyệt hàng tạm 2 báo giá.\"\n- ERP sinh phiếu tương ứng cho cả 2 báo giá."),

    ("TC-ROLE-271", "Gọi API gửi duyệt khi không còn báo giá nào cần gửi", "P2",
     "Dự án C đã gửi duyệt hết hàng tạm (không còn báo giá trúng thầu chưa gửi)",
     "1. Gọi API POST assign/prospective-projects/{id}/send-tmp-approval.\n2. Quan sát phản hồi.",
     "-",
     "Trả về thông báo \"Không có báo giá trúng thầu cần gửi duyệt hàng tạm.\"; không sinh phiếu ERP."),

    ("TC-ROLE-272", "Gọi API cập nhật kết quả khi không có báo giá đang đồng bộ", "P2",
     "Dự án C không có báo giá nào ở trạng thái Đang đồng bộ",
     "1. Gọi API POST assign/prospective-projects/{id}/pull-tmp-approval.\n2. Quan sát phản hồi.",
     "-",
     "Trả về thông báo \"Không có báo giá đang đồng bộ.\"; dữ liệu không thay đổi."),

    ("TC-ROLE-273", "Trạng thái đồng bộ được giữ đúng sau khi tải lại trang", "P1",
     "Báo giá BG-C đang ở trạng thái Đang đồng bộ sang ERP, đã có mã phiếu",
     "1. Tải lại trang (F5).\n2. Mở lại tab Báo giá.\n3. Quan sát banner.",
     "-",
     "Badge, tiến độ và mã phiếu hiển thị đúng như trước khi tải lại (dữ liệu lấy từ CSDL, không mất trạng thái)."),

    ("TC-ROLE-274", "Sau khi đồng bộ xong thì banner lập hợp đồng ERP sẵn sàng", "P1",
     "Báo giá BG-C loại tiền VND, đã đồng bộ hết hàng tạm, chưa lập hợp đồng ERP",
     "1. Quan sát banner \"Lập hợp đồng ERP từ báo giá\".",
     "BG-C: VND, đã đồng bộ",
     "Banner không còn trạng thái \"Chờ đồng bộ hết hàng sang ERP\" mà chuyển sang \"Sẵn sàng lập hợp đồng\"."),
]


def pad(vals):
    return list(vals) + [""] * (NCOL - len(vals))


with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(pad(HEADER_BLOCK))
    for i, (tc_id, func, prio, pre, steps, data, exp) in enumerate(TCS):
        module = MODULE if i == 0 else ""
        group = GROUP if i == 0 else ""
        w.writerow(pad([module, group, tc_id, func, prio, pre, steps, data, exp]))

print(f"OK: {OUT} — {len(TCS)} testcase")
