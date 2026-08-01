"""Generate testcase Excel TỔNG THỂ cho màn BOM Giải pháp (/assign/bom-list)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import _tc_builder
from _tc_builder import build

ROMAN_FULL = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
              "XI", "XII", "XIII", "XIV"]
_tc_builder.ROMAN = ROMAN_FULL


def load_eic_sections():
    """Nạp lại các section Export / Import / Sao chép đã viết ở
    `.plans/baogia-copy-export-import/testcase-export-import-copy-generate.py`
    để file này chứa TRỌN VẸN phần thuộc BOM (không phải trỏ sang file khác)."""
    import importlib.util
    real_build = _tc_builder.build
    _tc_builder.build = lambda *a, **k: None
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                            'baogia-copy-export-import', 'testcase-export-import-copy-generate.py')
        spec = importlib.util.spec_from_file_location('eic_src_bom', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        _tc_builder.build = real_build
        _tc_builder.ROMAN = ROMAN_FULL   # module nguồn cũng gán lại ROMAN


EIC = load_eic_sections()


def pick(section, idx_1based):
    return [section[2][i - 1] for i in idx_1based]

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testcase-bom-list.xlsx")
SHEET_NAME = "BomList"
FEATURE_NAME = "BOM Giải pháp (QLDA TKT) — toàn bộ chức năng"
MODULE_NAME = "BOM Giải pháp"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Kiểm thử TOÀN BỘ chức năng màn BOM Giải pháp `/assign/bom-list`: danh sách + bộ lọc + xuất Excel danh sách, tạo/sửa BOM "
     "(thông tin chung, lưới hàng hoá nhóm 2 cấp, hàng ERP / hàng tạm / công thức ERP, cha-con, nhân bản, kéo-thả), "
     "dịch vụ & chi phí khác, BOM Tổng hợp gộp BOM thành phần (sub-BOM), trạng thái & luồng duyệt qua hồ sơ trình duyệt, "
     "lịch sử, xoá, liên thông sang Báo giá, nhóm hàng 2 cấp + kéo-thả, và TRỌN BỘ Export / Import / Sao chép BOM (section VIII–XII).\n"
     "► File này là bộ testcase ĐẦY ĐỦ của màn BOM Giải pháp — không cần tham chiếu file nào khác. Phần Báo giá nằm ở `testcase-bao-gia.xlsx`."),

    ("2. Đối tượng được tính / hiển thị",
     "► 6 trạng thái BOM: 1 Đang tạo · 2 Hoàn thành · 3 Chờ duyệt · 4 Đã duyệt · 5 Đã được tổng hợp · 6 Không duyệt.\n"
     "► 2 loại BOM: Thành phần (type = 1) và Tổng hợp (type = 2 — mới được chọn BOM con và mới tạo được báo giá).\n"
     "► Bộ lọc danh sách: Dự án TKT, Giải pháp, Hạng mục, Khách hàng, Người tạo, Trạng thái, Loại BOM, khoảng Ngày tạo.\n"
     "► Lưới hàng hoá gồm: dòng Hàng hoá (ERP hoặc hàng tạm, 2 cấp cha-con) và khối riêng 'Dịch vụ & Chi phí khác'.\n"
     "► Màn Hàng hoá dự án chỉ lấy dòng CHA của BOM Tổng hợp ĐÃ DUYỆT (hợp với báo giá tự lập đã duyệt/trúng thầu)."),

    ("3. Đối tượng bị ẩn / không tính",
     "► Nút Sửa chỉ hiện khi trạng thái ∈ {Đang tạo, Hoàn thành, Không duyệt} VÀ người đăng nhập là người tạo BOM.\n"
     "► Nút Xoá chỉ hiện khi trạng thái = Đang tạo VÀ là người tạo VÀ có quyền 'Tạo BOM List'.\n"
     "► Import chỉ chạy được khi BOM ở trạng thái cho phép sửa VÀ là người tạo.\n"
     "► Nút chọn BOM con chỉ bật khi Loại BOM = Tổng hợp.\n"
     "► Ô 'Mã BOM' ẩn ở màn Tạo mới (mã do hệ thống sinh khi Lưu).\n"
     "► Cột giá vốn: người không có quyền 'Xem giá vốn hàng hoá' không xem được giá vốn hàng ERP và không được chọn hàng ERP làm hàng con."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "► Danh sách: 'Ngày tạo từ' / 'đến' áp lên created_at của BOM (bao gồm 2 đầu mút).\n"
     "► Cột 'Cập nhật' hiển thị thời điểm sửa gần nhất (updated_at) — không phải điều kiện lọc.\n"
     "► Giá ERP nạp vào BOM là giá tại thời điểm thêm hàng/lưu; đổi giá bên ERP sau đó không tự cập nhật ngược vào BOM đã lưu."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "► NHÓM HÀNG 2 CẤP: Cấp 1 số La Mã (I, II); Cấp 2 nhãn I.1/I.2, thụt lề, nền nhạt hơn. Nhóm Cấp 2 KHÔNG tạo được nhóm cấp 3.\n"
     "► HÀNG HOÁ 2 CẤP: dòng cha (cụm) và dòng con (vật tư). Dòng 'Dịch vụ & Chi phí khác' KHÔNG có cấp con.\n"
     "► Kéo-thả nhóm chỉ đổi thứ tự trong CÙNG CẤP + CÙNG CHA; handle kéo nhóm tách khỏi handle kéo hàng hoá.\n"
     "► BOM Tổng hợp gộp nhiều BOM Thành phần: hàng hoá của BOM con được gộp vào lưới; BOM con bị chuyển trạng thái 'Đã được tổng hợp'.\n"
     "► Mã hàng tạm tự sinh HHB + id (mã user nhập chỉ là nhãn gom nhóm)."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "► Mã hàng KHÔNG duy nhất trong 1 BOM → quan hệ cha-con khi import nối theo cột 'Mã hàng cha' + dòng gần nhất phía trên CÙNG NHÓM LÁ.\n"
     "► Mã hàng tạm: mã đã tồn tại trong 'Hàng hoá dự án' của CHÍNH DỰ ÁN đó → GIỮ; khác dự án → sinh mã HHB mới.\n"
     "► Gộp BOM con: hàng tạm trùng mã được khử trùng lặp khi gộp; hàng ERP đối chiếu theo erp_product_id.\n"
     "► Thêm BOM con vào BOM tổng hợp → BOM con chuyển 'Đã được tổng hợp'; bỏ ra khỏi danh sách → trả về 'Hoàn thành'.\n"
     "► Ràng buộc dòng con: không được trùng mã với chính dòng CHA trực tiếp (so theo erp_product_id)."),

    ("7. Phân quyền cấp",
     "• 'Tạo BOM List' (id 1034) — hiện nút Tạo mới, nút Sao chép ở danh sách, và là điều kiện để Xoá.\n"
     "• 'Xem giá vốn hàng hoá' — xem giá vốn hàng ERP; bắt buộc khi chọn hàng ERP làm hàng con.\n"
     "• Vai trò dữ liệu (không phải permission): người TẠO BOM — điều kiện bắt buộc để Sửa / Import / Xoá.\n"
     "• Duyệt BOM Tổng hợp đi theo HỒ SƠ TRÌNH DUYỆT của Giải pháp / Hạng mục (không có nút duyệt riêng trên màn BOM).\n"
     "⚠️ Quyền kiểm tra qua ROLE (role_has_permissions), không qua quyền gán trực tiếp cho nhân viên."),

    ("8. Cách tính các ô thống kê",
     "► Ô 'Thành tiền' 1 dòng = Đơn giá (giá vốn ERP/nhập tay) × Số lượng.\n"
     "► Dòng CHA có CON: giá trị cha roll-up từ các con, không cộng trùng cả cha lẫn con.\n"
     "► Ô tổng BOM = Σ hàng hoá (theo quy tắc roll-up) + Σ dịch vụ & chi phí khác.\n"
     "► Modal Import BOM: Tổng = Hợp lệ + Lỗi + Chờ xác nhận (chi tiết ở testcase Import/Export/Sao chép).\n"
     "► Màn danh sách không có ô thống kê tổng — chỉ đếm số bản ghi ở phân trang."),

    ("9. Ghi chú đọc bảng",
     "► Mọi thao tác trên lưới chỉ ghi DB khi bấm 'Lưu nháp' / 'Lưu BOM'. TC nào sửa lưới đều phải kiểm tra lại sau khi Lưu + tải lại trang.\n"
     "► 'Lưu nháp' giữ trạng thái Đang tạo; 'Lưu BOM' (lưu chính thức) đưa BOM sang Hoàn thành.\n"
     "► BOM Không duyệt sửa lại và lưu chính thức → quay lại luồng bình thường.\n"
     "► Testcase viết theo LOGIC CODE MỚI NHẤT; chỗ nào code lệch tài liệu đã ghi rõ ở cột 'Giải thích nghiệp vụ'.\n"
     "► Section VIII–XII (nhóm 2 cấp, export, import, sao chép, round-trip) là phần ĐÃ GỘP vào file này — không cần mở file testcase nào khác."),
]

S1 = ("I", "PHÂN QUYỀN & TRUY CẬP", [
 ("", "Truy cập màn danh sách BOM", "P0",
  "User đã đăng nhập, hệ thống có sẵn BOM của nhiều người tạo",
  "1. Vào menu QLDA TKT → BOM Giải pháp\n2. Quan sát danh sách + bộ lọc",
  "—",
  "- Vào được màn hình, hiện bộ lọc và bảng danh sách BOM\n- Không lỗi console, không bảng trắng",
  "Màn danh sách BOM"),
 ("", "Quyền 'Tạo BOM List' quyết định nút Tạo mới và Sao chép", "P0",
  "User A có quyền 'Tạo BOM List'; user B không có",
  "1. Đăng nhập A → xem toolbar danh sách + menu thao tác 1 dòng\n2. Đăng nhập B → xem tương tự",
  "—",
  "- A: có nút Tạo mới + action 'Sao chép' ở dòng\n- B: KHÔNG có nút Tạo mới, KHÔNG có action Sao chép",
  "Gate quyền 1034"),
 ("", "Chỉ người tạo mới sửa được BOM", "P0",
  "BM-01 trạng thái Đang tạo, người tạo = X",
  "1. Đăng nhập Y → xem action của dòng BM-01\n2. Mở thẳng URL màn Cập nhật của BM-01 → thử Lưu",
  "—",
  "- Không có action Sửa\n- Nếu vào được URL thì bị chặn khi lưu: 'Chỉ người tạo BOM mới được phép sửa.'",
  "Gate người tạo"),
 ("", "BOM ở trạng thái không cho sửa", "P0",
  "BM-02 Chờ duyệt; BM-03 Đã duyệt; BM-04 Đã được tổng hợp — cùng người tạo đăng nhập",
  "1. Xem action Sửa của 3 dòng\n2. Gọi thẳng API cập nhật 1 trong 3",
  "—",
  "- Cả 3 KHÔNG có action Sửa\n- API bị chặn: 'BOM ở trạng thái này không được phép sửa. Chỉ BOM \"Đang tạo\", \"Hoàn thành\" hoặc \"Không duyệt\" mới được sửa.'",
  "Chỉ 3 trạng thái được sửa"),
 ("", "Chỉ người tạo mới import được", "P1",
  "BM-05 Đang tạo, người tạo = X",
  "1. Đăng nhập Y (nếu vào được màn Cập nhật) → thực hiện Import",
  "—",
  "- Bị chặn 'Chỉ người tạo BOM mới được phép import.'",
  "Gate import"),
 ("", "Điều kiện xoá BOM", "P0",
  "BM-06 Đang tạo do user đăng nhập tạo (có quyền 1034); BM-07 Hoàn thành cùng người tạo; BM-08 Đang tạo do người khác tạo",
  "1. Xem action Xoá của 3 dòng\n2. Gọi API xoá BM-07 và BM-08",
  "—",
  "- Chỉ BM-06 có action Xoá\n- BM-07: 'Chỉ được xoá BOM List ở trạng thái Đang tạo'\n- BM-08: 'Chỉ người tạo mới được xoá BOM List này'",
  "3 điều kiện xoá đồng thời"),
 ("", "Không có quyền giá vốn — ẩn giá vốn hàng ERP", "P0",
  "BM-09 có 1 hàng ERP (giá 500.000) và 1 hàng tạm (300.000). User không có quyền 'Xem giá vốn hàng hoá'",
  "1. Mở BM-09 màn Xem → xem cột đơn giá của 2 dòng",
  "—",
  "- Giá của hàng ERP bị ẩn/'—'; hàng tạm vẫn xem được (nếu là người tạo)\n- Tổng giá vốn ẩn tương ứng",
  "Gate giá vốn theo dòng"),
 ("", "Không có quyền giá vốn — không chọn được hàng ERP làm hàng con", "P1",
  "BM-09 màn Cập nhật, user không có quyền giá vốn",
  "1. Bấm 'Thêm con' trên 1 dòng → chọn hàng ERP",
  "—",
  "- Bị chặn 'Bạn không có quyền \"Xem giá vốn hàng hoá\" nên không thể chọn hàng ERP làm hàng con.'",
  "Chặn rò giá vốn ERP"),
])

S2 = ("II", "DANH SÁCH — LỌC, TÌM KIẾM, CỘT, XUẤT EXCEL DANH SÁCH", [
 ("", "Hiển thị đủ cột mặc định", "P0",
  "Có ≥ 3 BOM",
  "1. Mở danh sách → đọc header bảng",
  "—",
  "- Có các cột: STT, Mã • Tên BOM, Dự án TKT, Giải pháp, Hạng mục, Version GP, Version HM, Khách hàng, Loại BOM, Trạng thái, Người tạo, Ngày tạo, Cập nhật, Thao tác",
  "Bộ cột danh sách BOM"),
 ("", "Badge trạng thái đúng 6 giá trị", "P0",
  "Có BOM ở đủ 6 trạng thái",
  "1. Bỏ lọc trạng thái → đối chiếu badge",
  "—",
  "- Hiển thị đúng: Đang tạo / Hoàn thành / Chờ duyệt / Đã duyệt / Đã được tổng hợp / Không duyệt, mỗi trạng thái 1 màu",
  "6 trạng thái BOM"),
 ("", "Lọc theo Dự án → Giải pháp → Hạng mục (bậc thang)", "P0",
  "Dự án DA-01 có 2 giải pháp; giải pháp S1 có 2 hạng mục",
  "1. Chọn Dự án DA-01 → mở dropdown Giải pháp\n2. Chọn S1 → mở dropdown Hạng mục\n3. Đổi dự án",
  "—",
  "- Giải pháp chỉ liệt kê của DA-01 (placeholder nhắc chọn dự án trước)\n- Hạng mục chỉ của S1\n- Đổi dự án → 2 cấp dưới tự reset",
  "Lọc bậc thang"),
 ("", "Lọc theo Trạng thái / Loại BOM / Người tạo / Khách hàng", "P0",
  "Dữ liệu đa dạng ≥ 6 BOM",
  "1. Lọc Trạng thái = Đã duyệt\n2. Đổi sang Loại BOM = Tổng hợp\n3. Lọc Người tạo = X\n4. Lọc Khách hàng = Công ty A",
  "—",
  "- Mỗi lần lọc danh sách chỉ còn bản ghi thoả điều kiện\n- Bỏ lọc thì danh sách trở lại đầy đủ",
  "4 filter độc lập"),
 ("", "Lọc theo khoảng Ngày tạo", "P0",
  "BM-A 01/07/2026, BM-B 15/07/2026, BM-C 31/07/2026",
  "1. Lọc từ 01/07/2026 đến 15/07/2026\n2. Đổi 16/07 → 31/07",
  "—",
  "- Lần 1: BM-A, BM-B (gồm 2 đầu mút)\n- Lần 2: chỉ BM-C",
  "Lọc created_at"),
 ("", "Tìm kiếm nhanh theo mã/tên BOM", "P0",
  "Có BOM mã BOM-2026-00037 tên 'BOM dây chuyền A'",
  "1. Gõ 'BOM-2026-00037'\n2. Gõ 'dây chuyền'\n3. Gõ chuỗi không tồn tại",
  "—",
  "- Tìm được theo cả mã và tên\n- Chuỗi không tồn tại → trạng thái rỗng, không lỗi",
  "Quick search"),
 ("", "Sắp xếp + phân trang", "P1",
  "Có ≥ 25 BOM",
  "1. Sắp xếp theo Ngày tạo tăng/giảm\n2. Sang trang 2 → đổi số dòng/trang",
  "—",
  "- Thứ tự đổi đúng chiều sắp xếp\n- Trang 2 không lặp dữ liệu trang 1; đổi page size quay về trang 1",
  "Sort + pagination"),
 ("", "Cấu hình cột hiển thị", "P1",
  "Danh sách BOM",
  "1. Bấm 'Cấu hình cột hiển thị' → bỏ tích Version GP, Version HM → áp dụng\n2. Tải lại trang",
  "—",
  "- 2 cột ẩn đi, bảng không vỡ\n- Cấu hình được ghi nhớ sau khi tải lại",
  "Column customization"),
 ("", "Xuất Excel DANH SÁCH theo bộ lọc đang chọn", "P0",
  "Đang lọc: Trạng thái = Đã duyệt (5 bản ghi)",
  "1. Bấm 'Xuất Excel' trên toolbar\n2. Mở file",
  "5 bản ghi",
  "- Nút chuyển 'Đang xuất...' rồi trở lại; có toast 'Xuất Excel thành công'\n"
  "- File chứa ĐÚNG 5 dòng theo bộ lọc (không phải toàn bộ BOM), cột khớp bảng danh sách\n"
  "- Đây là xuất DANH SÁCH, khác nút Xuất Excel trong màn chi tiết (xuất 1 BOM)",
  "exportList theo filter hiện tại"),
 ("", "Bộ nút thao tác trên từng dòng", "P0",
  "BM-06 Đang tạo (của mình), BM-03 Đã duyệt (người khác tạo)",
  "1. So sánh action 2 dòng",
  "—",
  "- BM-06: Xem chi tiết, Sửa, Sao chép (nếu có quyền), Xem lịch sử, Xoá\n- BM-03: Xem chi tiết, Sao chép, Xem lịch sử (không Sửa, không Xoá)",
  "Row action theo trạng thái + người tạo"),
 ("", "Xem lịch sử BOM từ danh sách", "P1",
  "BM-10 đã qua nhiều lần sửa/duyệt",
  "1. Bấm action 'Xem lịch sử'",
  "—",
  "- Popup lịch sử mở đúng BOM đó: các mốc tạo/sửa/gửi duyệt/duyệt/không duyệt kèm người thực hiện + thời điểm",
  "BomListLog"),
 ("", "Danh sách rỗng khi lọc không có kết quả", "P2",
  "Lọc điều kiện không khớp bản ghi nào",
  "1. Chọn bộ lọc vô nghiệm",
  "—",
  "- Hiện trạng thái rỗng rõ ràng, không lỗi",
  "Empty state"),
])

S3 = ("III", "TẠO / SỬA BOM — THÔNG TIN CHUNG & VALIDATE", [
 ("", "Tạo BOM Thành phần đầy đủ thông tin", "P0",
  "User có quyền 'Tạo BOM List'; dự án DA-01 có giải pháp S1",
  "1. Bấm Tạo mới → nhập Tên BOM 'BOM điều khiển line 01'\n2. Chọn Dự án DA-01 → Giải pháp S1 → Hạng mục (nếu có) → Khách hàng tự nạp\n"
  "3. Chọn Loại BOM = Thành phần, Loại tiền tệ, Ghi chú\n4. Thêm ≥ 1 dòng hàng hoá → bấm 'Lưu BOM'",
  "—",
  "- Khách hàng tự điền theo dự án\n- Lưu thành công, sinh mã BOM-2026-NNNNN, trạng thái = Hoàn thành\n- Điều hướng về danh sách/chi tiết đúng BOM vừa tạo",
  "Lưu chính thức → Hoàn thành"),
 ("", "Ô Mã BOM ẩn ở màn Tạo mới", "P1",
  "Màn Tạo BOM",
  "1. Quan sát khối thông tin chung trước khi Lưu\n2. Sau khi Lưu, mở lại màn Cập nhật",
  "—",
  "- Trước khi Lưu: KHÔNG hiển thị ô 'Mã BOM' (mã do hệ thống sinh)\n- Sau khi Lưu: ô Mã BOM hiển thị mã thật",
  "Ẩn mã khi chưa có"),
 ("", "Lưu nháp — trạng thái Đang tạo, cho phép thiếu thông tin", "P0",
  "Màn Tạo BOM, mới nhập Tên BOM",
  "1. Bấm 'Lưu nháp'\n2. Mở lại BOM vừa lưu",
  "—",
  "- Lưu được dù chưa chọn Dự án/Giải pháp/Khách hàng\n- Trạng thái = Đang tạo\n- Dữ liệu đã nhập được giữ",
  "Draft nới lỏng validate"),
 ("", "Lưu chính thức thiếu trường bắt buộc → chặn", "P0",
  "Màn Tạo BOM, để trống Tên BOM / Dự án / Giải pháp / Khách hàng / Loại BOM",
  "1. Bấm 'Lưu BOM'\n2. Quan sát từng ô",
  "—",
  "- Báo lỗi tương ứng: 'Vui lòng nhập tên BOM.', 'Vui lòng chọn Dự án.', 'Vui lòng chọn Giải pháp.', "
  "'Vui lòng chọn Khách hàng.', 'Vui lòng chọn Loại BOM.'\n- Ô lỗi viền đỏ, không tạo bản ghi",
  "Validate lưu chính thức"),
 ("", "Tên BOM vượt 255 ký tự", "P1",
  "Màn Tạo BOM",
  "1. Nhập tên 300 ký tự → Lưu",
  "300 ký tự",
  "- Báo 'Tên BOM không được vượt quá 255 ký tự.'\n- Không lưu bản bị cắt cụt",
  "DB không strict mode → phải chặn ở ứng dụng"),
 ("", "Giải pháp có hạng mục con → chỉ tạo được BOM Tổng hợp ở cấp giải pháp", "P0",
  "Giải pháp S2 có 3 hạng mục con",
  "1. Tạo BOM chọn Giải pháp S2, KHÔNG chọn Hạng mục, Loại BOM = Thành phần → Lưu",
  "—",
  "- Bị chặn 'Giải pháp có hạng mục con — BOM cấp giải pháp chỉ được tạo loại Tổng hợp.'",
  "Ràng buộc cấp giải pháp/hạng mục"),
 ("", "Một version giải pháp chỉ có 1 BOM tổng hợp", "P0",
  "Giải pháp S1 version hiện tại đã có 1 BOM Tổng hợp",
  "1. Tạo BOM Tổng hợp thứ 2 cho cùng giải pháp + version → Lưu",
  "—",
  "- Bị chặn với thông báo đã có BOM tổng hợp trên version này (kèm mã BOM đang tồn tại)",
  "Chống trùng BOM tổng hợp/version"),
 ("", "Sửa BOM ở trạng thái Hoàn thành", "P0",
  "BM-20 trạng thái Hoàn thành, người tạo đăng nhập",
  "1. Mở Cập nhật → đổi tên, thêm 1 dòng hàng hoá → 'Lưu BOM'\n2. Mở lại",
  "—",
  "- Sửa và lưu thành công, dữ liệu mới được ghi nhận\n- Trạng thái vẫn Hoàn thành",
  "Hoàn thành vẫn sửa được"),
 ("", "Sửa BOM 'Không duyệt' rồi lưu lại", "P0",
  "BM-21 trạng thái Không duyệt",
  "1. Mở Cập nhật → sửa theo góp ý → 'Lưu BOM'\n2. Xem trạng thái",
  "—",
  "- Lưu được; trạng thái chuyển về luồng bình thường (Hoàn thành) để trình duyệt lại\n- Lịch sử ghi nhận lần sửa",
  "resetFromRejected"),
 ("", "Chọn Loại tiền tệ", "P1",
  "Màn Cập nhật BM-20",
  "1. Đổi Loại tiền tệ → Lưu → mở lại",
  "—",
  "- Tiền tệ được lưu; các ô tiền hiển thị theo tiền tệ đã chọn",
  "getCurrencies"),
 ("", "Ghi chú BOM lưu và chảy sang báo giá", "P1",
  "BM-22 có dòng hàng hoá nhập Ghi chú 'Hàng đặt trước 30 ngày'",
  "1. Lưu BOM → tạo báo giá từ BOM (nếu đủ điều kiện) → xem cột Ghi chú\n2. In báo giá",
  "—",
  "- Ghi chú của dòng được lưu và hiển thị lại ở BOM\n- Báo giá tạo từ BOM kế thừa đúng ghi chú; bản in hiện cột Ghi chú",
  "note chảy BOM → báo giá → bản in"),
])

S4 = ("IV", "LƯỚI HÀNG HOÁ — NHÓM 2 CẤP, THÊM/SỬA/XOÁ, CHA-CON", [
 ("", "Thêm hàng hoá ERP", "P0",
  "BM-30 màn Cập nhật, đã có 1 nhóm",
  "1. Bấm 'Thêm mới' → tab Hàng hoá ERP → tìm và chọn 1 sản phẩm → Thêm",
  "Mã ERP thật",
  "- Dòng mới có Tên/Mã/Model/Thương hiệu/Xuất xứ/ĐVT/TSKT lấy từ ERP và bị khoá\n- Đơn giá lấy theo ERP; Số lượng mặc định sửa được",
  "Popup 2 tab dùng chung với báo giá"),
 ("", "Thêm hàng tạm nhập tay", "P0",
  "BM-30",
  "1. Tab 'Thêm mới thủ công' → nhập Tên, ĐVT, Thương hiệu, Xuất xứ, TSKT, Số lượng, Đơn giá → Thêm\n2. Lưu BOM → mở lại",
  "—",
  "- Dòng hàng tạm thêm được, các ô sửa được\n- Sau Lưu: mã tự sinh HHB + số (mã user nhập chỉ là nhãn gom nhóm)",
  "Mã hàng tạm HHB+id"),
 ("", "Dùng lại hàng tạm của dự án", "P1",
  "Dự án 38 đã có hàng tạm HHB001756",
  "1. Chọn nguồn 'Hàng hoá dự án' → chọn HHB001756 → Thêm → Lưu BOM",
  "Cùng dự án",
  "- Dòng mang đủ thông tin của hàng cũ\n- Sau Lưu GIỮ nguyên mã HHB001756 (cùng dự án)",
  "Rule mã hàng tạm cùng dự án"),
 ("", "Thêm hàng hoá theo công thức ERP (recipe) — tự sinh dòng con", "P1",
  "ERP có sản phẩm dạng công thức với 3 vật tư con",
  "1. Thêm sản phẩm công thức đó vào BOM\n2. Quan sát các dòng sinh ra",
  "—",
  "- Dòng cha kèm 3 dòng con vật tư theo công thức ERP\n- Số lượng con nhân theo số lượng cha",
  "getErpRecipeChildren"),
 ("", "Thêm dòng CON thủ công cho 1 dòng cha", "P0",
  "BM-30 có dòng cha 'Cụm bơm'",
  "1. Bấm 'Thêm con' → thêm 2 dòng con\n2. Xem tiền dòng cha\n3. Lưu → mở lại",
  "—",
  "- 2 dòng con thụt vào dưới cha\n- Tiền cha roll-up từ con, không cộng trùng\n- Sau Lưu quan hệ giữ đúng",
  "Cây hàng hoá 2 cấp"),
 ("", "Dòng con không được trùng mã với dòng CHA trực tiếp", "P0",
  "BM-30 dòng cha là hàng ERP mã X",
  "1. Thêm con cho dòng đó và chọn đúng sản phẩm ERP mã X → Lưu",
  "—",
  "- Bị chặn với thông báo con không được trùng mã cha trực tiếp\n- Hàng tạm trùng mã KHÔNG bị chặn theo luật này",
  "So theo erp_product_id (P17-P18)"),
 ("", "Nhân bản dòng hàng hoá (kèm dòng con)", "P1",
  "BM-30 có dòng X kèm 2 con",
  "1. Bấm 'Nhân bản' trên dòng X → Lưu → mở lại",
  "—",
  "- Sinh bản sao của X kèm 2 con, đặt ngay dưới X\n- Sửa bản sao không ảnh hưởng dòng gốc",
  "Nút Nhân bản"),
 ("", "Sửa inline các ô trên lưới", "P0",
  "BM-30 có 5 dòng",
  "1. Sửa Số lượng, Đơn giá (hàng tạm), Ghi chú, TSKT ngay trên lưới\n2. Lưu BOM → mở lại",
  "—",
  "- Sửa được trực tiếp; ô master của hàng ERP vẫn khoá\n- Sau Lưu, dữ liệu đúng như đã sửa",
  "Cột Ghi chú inline (E4b)"),
 ("", "Xoá dòng hàng hoá (cha có con)", "P0",
  "BM-30 có cha + 2 con",
  "1. Xoá dòng cha → xác nhận → Lưu → mở lại",
  "—",
  "- Có xác nhận; xoá cha thì con bị xoá theo, không để con mồ côi\n- Sau Lưu, DB không còn 3 dòng",
  "Xoá cascade"),
 ("", "Thêm nhóm Cấp 1 và nhóm con Cấp 2", "P0",
  "BM-30 màn Cập nhật",
  "1. 'Thêm nhóm' → 'Dây chuyền sơn'\n2. Trên nhóm đó bấm 'Thêm nhóm con' → 'Vật tư điện'\n3. Quan sát nhãn và thụt lề",
  "—",
  "- Nhóm Cấp 1 nhãn 'I.', nhóm con nhãn 'I.1' thụt lề nền nhạt hơn\n- Nhóm Cấp 2 không có nút 'Thêm nhóm con'",
  "Nhóm 2 cấp (chi tiết ở testcase riêng)"),
 ("", "Xoá nhóm Cấp 1 → cascade nhóm con, hàng hoá không mất", "P0",
  "Nhóm I có 2 nhóm con, tổng 4 dòng hàng hoá",
  "1. Xoá nhóm I → xác nhận → Lưu → mở lại",
  "—",
  "- Nhóm I và 2 nhóm con biến mất; 4 dòng hàng hoá vẫn còn (không nhóm)\n- Không sinh nhóm rỗng",
  "Cascade xoá nhóm"),
 ("", "Kéo-thả đổi thứ tự nhóm và hàng hoá", "P0",
  "BM-30 có 3 nhóm, 4 dòng trong 1 nhóm",
  "1. Kéo nhóm 3 lên vị trí 1 → Lưu → tải lại\n2. Kéo 1 dòng hàng hoá lên đầu nhóm → Lưu → tải lại",
  "—",
  "- Thứ tự đổi ngay và giữ sau khi Lưu + tải lại\n- Kéo nhóm không xáo thứ tự hàng hoá và ngược lại\n- Kéo nhóm sang khác cấp/khác cha bị chặn (con trỏ no-drop)",
  "2 handle kéo độc lập"),
 ("", "Cấu hình cột hiển thị trên lưới BOM", "P2",
  "BM-30 màn Cập nhật",
  "1. Mở cấu hình cột → bật/tắt Model, Xuất xứ, Ghi chú",
  "—",
  "- Cột ẩn/hiện đúng, bảng không vỡ, tổng tiền không đổi",
  "BomBuilderColumnModal"),
 ("", "Số lượng phải > 0", "P0",
  "BM-30",
  "1. Đặt Số lượng = 0 cho 1 dòng → Lưu BOM",
  "SL = 0",
  "- Bị chặn 'Số lượng phải lớn hơn 0'",
  "Validate số lượng"),
 ("", "Tìm hàng hoá trong chính BOM (thanh tìm kiếm lưới)", "P2",
  "BM-31 có 50 dòng",
  "1. Gõ mã/tên vào ô tìm trong lưới",
  "—",
  "- Lưới lọc đúng dòng khớp, xoá từ khoá thì hiện lại đủ dòng",
  "searchBomProducts"),
])

S5 = ("V", "DỊCH VỤ & CHI PHÍ KHÁC", [
 ("", "Thêm dịch vụ từ danh mục chi phí ERP", "P0",
  "BM-40 màn Cập nhật; danh mục ERP có 'Phí lắp đặt' VAT 8%",
  "1. Ở khối 'Dịch vụ & Chi phí khác' → Thêm mới → chọn 'Phí lắp đặt' → nhập đơn giá → Thêm\n2. Lưu BOM → mở lại",
  "VAT 8%",
  "- Dòng dịch vụ nằm ở KHỐI RIÊNG (không lẫn vào lưới hàng hoá)\n- VAT lấy đúng 8% từ ERP (không mặc định 0)\n- Sau Lưu dữ liệu đúng",
  "bom_list_service_items + VAT từ ERP"),
 ("", "Tạo nhanh chi phí tự do", "P1",
  "BM-40",
  "1. Tạo nhanh chi phí 'Phí cẩu hàng' → nhập giá → Thêm → Lưu",
  "—",
  "- Dòng được thêm với chi phí tự do (không cần khớp danh mục)\n- Lưu thành công",
  "Chi phí tự do cost_id = null"),
 ("", "Sửa / xoá dòng dịch vụ", "P0",
  "BM-40 có 2 dòng dịch vụ",
  "1. Sửa tên + đơn giá 1 dòng → Lưu\n2. Xoá 1 dòng → Lưu → mở lại",
  "—",
  "- Sửa/xoá phản ánh đúng sau khi Lưu\n- Tổng BOM cập nhật theo",
  "CRUD service items"),
 ("", "Tên dịch vụ bắt buộc + giới hạn độ dài", "P1",
  "BM-40",
  "1. Thêm dịch vụ để trống tên → Lưu\n2. Nhập tên 300 ký tự → Lưu",
  "—",
  "- Trống tên: báo lỗi bắt buộc\n- 300 ký tự: báo vượt 255 ký tự, không lưu bản cắt cụt",
  "service_items.*.name required_with|max:255"),
 ("", "Dòng dịch vụ không có cấp con", "P1",
  "BM-40 có dòng dịch vụ",
  "1. Thử thêm dòng con cho dòng dịch vụ",
  "—",
  "- Không có nút Thêm con cho dịch vụ; nếu import file có con dưới dịch vụ thì báo 'Dịch vụ & Chi phí khác không hỗ trợ hàng cấp con.'",
  "Dịch vụ là dòng phẳng"),
 ("", "Dịch vụ của BOM chảy sang báo giá tạo từ BOM", "P0",
  "BM-41 (Tổng hợp, Đã duyệt) có 2 dòng dịch vụ",
  "1. Tạo báo giá từ BM-41\n2. Xem khối Dịch vụ & Chi phí khác của báo giá",
  "2 dịch vụ",
  "- Báo giá nhận đủ 2 dòng dịch vụ với tên/giá/VAT đúng",
  "createFromRequest/FromBom copy service items"),
])

S6 = ("VI", "BOM TỔNG HỢP & BOM THÀNH PHẦN (SUB-BOM)", [
 ("", "Chọn BOM con chỉ bật khi Loại BOM = Tổng hợp", "P0",
  "Màn Tạo BOM",
  "1. Chọn Loại BOM = Thành phần → xem nút chọn BOM con\n2. Đổi sang Tổng hợp → xem lại",
  "—",
  "- Thành phần: nút chọn BOM con bị khoá\n- Tổng hợp: nút bật, mở được popup chọn BOM con",
  "canSelectSubBom"),
 ("", "Chọn nhiều BOM con và gộp hàng hoá", "P0",
  "BOM con BM-C1 (5 dòng), BM-C2 (4 dòng), cùng dự án/giải pháp, trạng thái Hoàn thành",
  "1. Tạo BOM Tổng hợp → chọn 2 BOM con → xác nhận\n2. Quan sát lưới + chip hiển thị BOM con đã chọn\n3. Lưu BOM",
  "5 + 4 dòng",
  "- Hiện 'Đã chọn: 2 BL con' và chip tên từng BOM con\n- Lưới gộp đủ hàng hoá 2 BOM con\n- Lưu thành công",
  "Gộp sub-BOM"),
 ("", "BOM con chuyển trạng thái 'Đã được tổng hợp'", "P0",
  "BM-C1, BM-C2 đang Hoàn thành",
  "1. Lưu BOM Tổng hợp có chứa 2 BOM con đó\n2. Về danh sách xem trạng thái BM-C1, BM-C2",
  "—",
  "- Cả 2 chuyển trạng thái 'Đã được tổng hợp'\n- Không sửa/xoá được nữa (không có action Sửa/Xoá)",
  "syncChildStatus khi thêm"),
 ("", "Bỏ BOM con ra khỏi BOM tổng hợp → trả trạng thái Hoàn thành", "P0",
  "BOM Tổng hợp đang chứa BM-C1, BM-C2",
  "1. Mở Cập nhật → bỏ chọn BM-C2 → Lưu\n2. Xem trạng thái BM-C2",
  "—",
  "- BM-C2 quay lại trạng thái Hoàn thành, sửa lại được\n- BM-C1 vẫn 'Đã được tổng hợp'",
  "syncChildStatus khi gỡ"),
 ("", "Dedupe hàng tạm trùng mã khi gộp BOM con", "P1",
  "BM-C1 và BM-C2 cùng có hàng tạm mã HHB001756",
  "1. Gộp 2 BOM con vào BOM Tổng hợp → xem lưới",
  "—",
  "- Hàng tạm trùng mã được gộp (không hiện 2 dòng trùng lặp vô nghĩa)\n- Số lượng phản ánh đúng theo quy tắc gộp",
  "Dedupe mã hàng tạm khi gộp (P18)"),
 ("", "Nhóm hàng sau khi gộp sub-BOM", "P2",
  "BM-C1 và BM-C2 mỗi BOM có nhóm 2 cấp",
  "1. Gộp vào BOM Tổng hợp → xem cây nhóm",
  "—",
  "- Ghi nhận thực tế: nhóm sau gộp hiện PHẲNG về Cấp 1 (không giữ 2 cấp của từng BOM con)\n- Không mất hàng hoá, không lỗi",
  "Giới hạn đã biết: mergedBomGroups phẳng — xác nhận BA nếu cần giữ 2 cấp"),
 ("", "BOM tổng hợp là nguồn tạo báo giá", "P0",
  "BOM Tổng hợp BM-50 đã duyệt, dự án Tự triển khai",
  "1. Tạo báo giá từ BM-50 → kiểm tra dữ liệu kế thừa",
  "—",
  "- Báo giá nhận đủ hàng hoá + nhóm + dịch vụ từ BOM\n- Báo giá loại 'kế thừa BOM' và bị khoá cấu trúc",
  "Liên thông BOM → báo giá"),
 ("", "Không tự tham chiếu vòng khi chọn BOM con", "P2",
  "BOM A đang là BOM con của BOM B",
  "1. Mở BOM A (nếu là Tổng hợp) → thử chọn BOM B làm con",
  "—",
  "- Ghi nhận thực tế hành vi hệ thống (hiện chưa chặn vòng lặp A→B→A theo ghi chú kỹ thuật)\n- Nếu tạo được vòng lặp thì báo cáo là RỦI RO cần xử lý",
  "syncSubBomRelations chưa chặn vòng — ngoài scope trước đây"),
])

S7 = ("VII", "TRẠNG THÁI & LUỒNG DUYỆT BOM", [
 ("", "Lưu nháp → Đang tạo; Lưu BOM → Hoàn thành", "P0",
  "Màn Tạo BOM đầy đủ thông tin",
  "1. Bấm 'Lưu nháp' → xem trạng thái\n2. Mở lại, bấm 'Lưu BOM' → xem trạng thái",
  "—",
  "- Sau Lưu nháp: Đang tạo\n- Sau Lưu BOM: Hoàn thành",
  "2 nút lưu, 2 trạng thái"),
 ("", "BOM tổng hợp chuyển 'Chờ duyệt' khi hồ sơ trình duyệt được gửi", "P0",
  "BOM Tổng hợp BM-60 (Hoàn thành) gắn với hồ sơ trình duyệt của Giải pháp S1",
  "1. Gửi hồ sơ trình duyệt của S1\n2. Xem trạng thái BM-60 + lịch sử",
  "—",
  "- BM-60 chuyển 'Chờ duyệt'\n- Lịch sử BOM ghi nhận mốc gửi duyệt\n- Không sửa/xoá được ở trạng thái này",
  "syncStatusFromSubmission: pending"),
 ("", "Hồ sơ được duyệt → BOM 'Đã duyệt'", "P0",
  "BM-60 đang Chờ duyệt",
  "1. Người duyệt hồ sơ trình duyệt bấm Duyệt\n2. Xem trạng thái BM-60",
  "—",
  "- BM-60 chuyển 'Đã duyệt'\n- Từ đây mới tạo được báo giá từ BOM và mới vào 'Hàng hoá dự án'",
  "syncStatusFromSubmission: approved"),
 ("", "Hồ sơ bị từ chối → BOM 'Không duyệt'", "P0",
  "BM-61 đang Chờ duyệt",
  "1. Người duyệt từ chối hồ sơ\n2. Xem trạng thái BM-61 + khả năng sửa",
  "—",
  "- BM-61 chuyển 'Không duyệt'\n- Người tạo sửa lại được (1 trong 3 trạng thái cho sửa)",
  "syncStatusFromSubmission: rejected"),
 ("", "Chỉ BOM TỔNG HỢP đổi trạng thái theo hồ sơ trình duyệt", "P1",
  "Hồ sơ trình duyệt gắn cả BOM Tổng hợp và BOM Thành phần",
  "1. Gửi/duyệt hồ sơ\n2. Xem trạng thái từng BOM",
  "—",
  "- Chỉ BOM loại Tổng hợp đổi trạng thái\n- BOM Thành phần giữ nguyên trạng thái cũ",
  "Điều kiện bom_list_type = TỔNG HỢP"),
 ("", "BOM 'Đã duyệt' xuất hiện ở Hàng hoá dự án", "P0",
  "BM-62 vừa được duyệt, có 3 dòng cha (2 hàng tạm, 1 hàng ERP gốc)",
  "1. Mở màn Hàng hoá dự án lọc theo dự án tương ứng",
  "—",
  "- Các dòng CHA hàng tạm của BM-62 xuất hiện\n- Hàng ERP GỐC không xuất hiện\n- Không lặp dòng cho cùng (mã + dự án)",
  "Union BOM đã duyệt + báo giá; lọc ERP gốc + dedup"),
 ("", "Lịch sử BOM ghi đủ mốc", "P0",
  "BM-60 đã qua tạo → sửa → gửi duyệt → duyệt",
  "1. Mở popup Lịch sử của BM-60",
  "—",
  "- Đủ các mốc theo thời gian, mỗi mốc có người thực hiện + thời điểm + nội dung thay đổi",
  "BomListLog"),
])

S8 = ("VIII", "EXPORT / IMPORT / SAO CHÉP — MỨC LIÊN THÔNG", [
 ("", "Xuất Excel 1 BOM từ màn Chi tiết và màn Cập nhật", "P0",
  "BM-70 có 12 dòng (8 cha, 4 con) + 2 dịch vụ",
  "1. Màn Chi tiết → 'Xuất Excel' → modal → Xuất\n2. Màn Cập nhật → 'Xuất Excel' → Xuất\n3. So sánh 2 file",
  "—",
  "- Cả 2 nơi cho ra cùng định dạng round-trip; tên file theo mã BOM (BOM-2026-000xx.xlsx)\n- Có tuỳ chọn 'Xuất hàng hoá cấp con'",
  "Chi tiết ở testcase Export/Import/Sao chép"),
 ("", "Import file BOM rồi Lưu — dữ liệu vào đúng lưới", "P0",
  "BM-71 Đang tạo; file Excel 8 dòng có nhóm 2 cấp + cha-con",
  "1. Import → Validate → Import (chọn phương thức) → 'Lưu BOM'\n2. Mở lại BOM",
  "8 dòng",
  "- Lưới nhận đúng dữ liệu, nhóm và cha-con đúng\n- Sau Lưu, DB khớp; hàng tạm sinh/giữ mã theo quy tắc dự án",
  "Import áp lưới → Lưu mới ghi DB"),
 ("", "Sao chép BOM từ danh sách", "P0",
  "BM-70 có 12 dòng, 2 nhóm cấp 1 + 3 nhóm cấp 2, 2 BOM con",
  "1. Action 'Sao chép' → xem form → Lưu",
  "—",
  "- Mở form Tạo mới prefill, tiêu đề 'Sao chép BOM List', tên có hậu tố ' - Sao chép', mã trống\n"
  "- Cấu trúc nhóm + hàng hoá + dịch vụ được nhân bản; BOM con bị NGẮT (không kế thừa)\n- BOM gốc không đổi",
  "getCopyData"),
 ("", "Nút Import không dùng được khi BOM không cho sửa", "P0",
  "BM-72 Đã duyệt",
  "1. Mở BM-72 → tìm chức năng Import",
  "—",
  "- Không vào được màn Cập nhật nên không import được; nếu gọi API thì bị chặn 'BOM ở trạng thái này không được phép import.'",
  "Gate trạng thái import"),
])

S9 = ("IX", "XOÁ & EDGE CASES", [
 ("", "Xoá BOM ở trạng thái Đang tạo", "P0",
  "BM-80 Đang tạo, do user đăng nhập tạo, có 6 dòng + 1 dịch vụ + 2 nhóm",
  "1. Action Xoá → xác nhận\n2. Quay lại danh sách và mở link cũ",
  "—",
  "- Có hộp xác nhận\n- BOM biến mất khỏi danh sách; mở link cũ báo không tồn tại\n- Hàng hoá/nhóm/dịch vụ liên quan cũng bị xoá",
  "destroy"),
 ("", "Không xoá được BOM đang được BOM tổng hợp sử dụng", "P0",
  "BM-C1 đang là BOM con của 1 BOM Tổng hợp (trạng thái Đã được tổng hợp)",
  "1. Thử xoá BM-C1",
  "—",
  "- Không có action Xoá (trạng thái ≠ Đang tạo)\n- Gọi API bị chặn, dữ liệu BOM tổng hợp không bị vỡ",
  "Bảo vệ quan hệ sub-BOM"),
 ("", "Mở BOM không tồn tại", "P1",
  "id BOM không tồn tại",
  "1. Mở /assign/bom-list/999999",
  "—",
  "- Thông báo không tìm thấy, không vỡ trang",
  "Route model binding 404"),
 ("", "BOM 300+ dòng — hiệu năng lưới", "P2",
  "BM-81 có 300 dòng",
  "1. Mở màn Cập nhật → cuộn → sửa 1 ô số lượng → Lưu BOM",
  "300 dòng",
  "- Không treo trình duyệt; tính lại tổng đúng; Lưu thành công đủ 300 dòng",
  "Ngưỡng dữ liệu lớn"),
 ("", "Ký tự đặc biệt trong tên hàng / ghi chú", "P1",
  "BM-82 có dòng tên '=Bơm <2HP> & \"Vòng bi\"'",
  "1. Lưu → mở lại → Xuất Excel",
  "—",
  "- Hiển thị nguyên văn, xuất Excel không lỗi HTTP 500, ô hiện đúng chuỗi",
  "Chuỗi bắt đầu '=' từng gây sập export"),
 ("", "Vượt độ dài bị chặn ở tầng ứng dụng", "P0",
  "BM-83",
  "1. Nhập Tên hàng 300 ký tự, Ghi chú 600 ký tự, Nhóm hàng 300 ký tự → Lưu",
  "—",
  "- Báo lỗi vượt giới hạn tương ứng (255 / 500 / 250 ký tự)\n- KHÔNG lưu bản bị cắt cụt",
  "DB không strict mode"),
 ("", "Hai người cùng sửa 1 BOM", "P2",
  "BM-84 mở trên 2 phiên",
  "1. Phiên 1 sửa + Lưu\n2. Phiên 2 (dữ liệu cũ) bấm Lưu\n3. Mở lại BOM",
  "—",
  "- Không mất dữ liệu âm thầm: hoặc báo cần tải lại, hoặc kết quả cuối cùng nhất quán và kiểm chứng được",
  "Ghi nhận hành vi thực tế"),
 ("", "Mất kết nối khi Lưu BOM", "P2",
  "BM-85 màn Cập nhật đã sửa nhiều dòng",
  "1. Ngắt mạng → Lưu BOM\n2. Bật mạng → Lưu lại",
  "—",
  "- Lần 1: báo lỗi rõ ràng, dữ liệu đang nhập trên lưới KHÔNG bị mất\n- Lần 2: lưu thành công đủ dữ liệu",
  "Chống mất dữ liệu khi lỗi mạng"),
])

# ===== Gộp nội dung Export / Import / Sao chép (phần thuộc BOM) =====
# Phân quyền: TC 10 (quyền Sao chép BOM) và 11 (trạng thái import BOM) của section nguồn.
S1 = (S1[0], S1[1], S1[2] + pick(EIC.S1, [10, 11]))

S8_OLD = S8  # 'Liên thông' — thay bằng các section đầy đủ bên dưới
S8 = ("VIII", "NHÓM HÀNG 2 CẤP & KÉO-THẢ SẮP XẾP NHÓM", EIC.S11[2])
S10 = ("IX", "EXPORT FILE CHI TIẾT BOM", EIC.S6[2])
S11 = ("X", "IMPORT BOM LIST", EIC.S7[2])
S12 = ("XI", "SAO CHÉP BOM LIST", EIC.S8[2])
# Round-trip & E2E: lấy 2 TC thuần BOM (2, 4) + 2 TC robustness file import dùng chung (9, 10)
S13 = ("XII", "ROUND-TRIP & E2E", pick(EIC.S9, [2, 4, 9, 10]))
S14 = ("XIII", S9[1], S9[2])   # Xoá & edge cases đưa xuống cuối

SECTIONS = [S1, S2, S3, S4, S5, S6, S7, S8, S10, S11, S12, S13, S14]
SECTIONS = [
    (roman, title, [(f"{i:03d}",) + tuple(tc[1:]) for i, tc in enumerate(tcs, start=1)])
    for roman, title, tcs in SECTIONS
]

build(OUTPUT_FILE, SHEET_NAME, FEATURE_NAME, MODULE_NAME, DESCRIPTION_BLOCK, SECTIONS)
total = sum(len(s[2]) for s in SECTIONS)
p0 = sum(1 for s in SECTIONS for tc in s[2] if tc[2] == 'P0')
print(f"Tổng TC: {total} | P0: {p0} ({round(p0*100/total)}%)")
