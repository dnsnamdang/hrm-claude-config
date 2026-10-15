# -*- coding: utf-8 -*-
"""Dung HDSD man 'Phieu xuat kho' (WarehouseExport / PXK) - ERP TanPhatDev.

Nguon: khao sat controller Warehouse\\WarehouseExportsController + model
WarehouseExport (+ ExportModel + Lot/LotDetail/LotPackage + Tab) + views
warehouse/warehouse_exports + PermissionsTableSeeder. KHONG chen anh -> dung o placeholder.

Chay:  /usr/local/bin/python3 gen_hdsd_pxk_erp.py
Output: ERP/HDSD_luongchinh/HDSD_PhieuXuatKho.docx
"""
import os
import sys
import zipfile

from docx import Document
from docx.oxml.ns import qn

ERP = "/Users/nguyentrancu/DEV/code/ERP-HRM/ERP"
sys.path.insert(0, os.path.join("/Users/nguyentrancu/DEV/code/ERP-HRM/HRM",
                                ".claude", "skills", "hdsd-documenter", "assets"))
from hdsd_engine import HdsdBuilder  # noqa: E402

OUT_DIR = os.path.join(ERP, "HDSD_luongchinh")
os.makedirs(OUT_DIR, exist_ok=True)
OUTPUT = os.path.join(OUT_DIR, "HDSD_PhieuXuatKho.docx")

SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_shots_empty")
os.makedirs(SHOTS, exist_ok=True)


def img_placeholder(b, mo_ta):
    b.para(mo_ta, bold_prefix="[Vị trí chèn ảnh] ")


def clear_toc_cache(path):
    """Xoa text cache trong moi field TOC (muc luc + danh muc hinh) -> Word tu dung lai khi mo."""
    doc = Document(path)
    body = doc.element.body
    fields = []
    for el in body.iter():
        tag = el.tag
        if tag == qn('w:fldChar'):
            t = el.get(qn('w:fldCharType'))
            if t == 'begin':
                fields.append({'instr': '', 'in_result': False})
            elif t == 'separate':
                if fields:
                    fields[-1]['in_result'] = True
            elif t == 'end':
                if fields:
                    fields.pop()
        elif tag == qn('w:instrText'):
            if fields:
                fields[-1]['instr'] += (el.text or '')
        elif tag == qn('w:t'):
            if any(f['in_result'] and 'TOC' in f['instr'] for f in fields):
                el.text = ''
    doc.save(path)


def finish_macos(b):
    b.doc.save(b.output)
    clear_toc_cache(b.output)
    b._set_update_fields()
    removed = b._purge_orphan_media()
    chk = Document(b.output)
    raw = zipfile.ZipFile(b.output).read("word/document.xml").decode("utf-8")
    my_headings = {p.text.strip() for p in chk.paragraphs
                   if p.style.name in ("Heading 1", "Heading 2", "Heading 3")}
    sot = [h for h in b.template_headings if h and h in raw and h not in my_headings]
    h1 = sum(1 for p in chk.paragraphs if p.style.name == "Heading 1")
    print("File:", b.output)
    print("Heading 1:", h1, "| Bang:", len(chk.tables),
          "| Anh:", len(chk.inline_shapes), "| Media mo coi da xoa:", len(removed))
    print("Tieu de khung con sot:", sot or "khong (OK)")
    assert not sot, "Van con tieu de khung: %s" % sot


# ============================================================ NOI DUNG
b = HdsdBuilder(
    output=OUTPUT,
    shots_dir=SHOTS,
    cover_title="(Màn hình: Phiếu xuất kho)",
    doc_title="HDSD - Phiếu xuất kho",
)

# ------------------------------------------------- TONG QUAN
b.h1("TỔNG QUAN PHẦN MỀM")

b.h2("1. Thuật ngữ & viết tắt")
b.para("Bảng thuật ngữ giúp người dùng hiểu đúng các bước hướng dẫn.")
b.table([
    ["Thuật ngữ", "Ý nghĩa"],
    ["Phiếu xuất kho (PXK)", "Chứng từ bước 3 của quy trình xuất hàng: do Thủ kho lập từ Đề nghị xuất kho để thực hiện lấy hàng theo lô và xuất kho thực tế. Đây chính là màn hình tài liệu này hướng dẫn. Mã phiếu có dạng PXK-xxxxx."],
    ["Đề nghị xuất kho (ĐNXK / PDNXK)", "Chứng từ bước 2, do Kế toán kho lập. Phiếu xuất kho được lập từ một Đề nghị xuất kho đang chờ duyệt; lập phiếu xuất kho đồng thời là duyệt đề nghị đó."],
    ["Yêu cầu xuất hàng (YCXH)", "Chứng từ bước 1, do nhân viên kinh doanh lập."],
    ["Phiếu xuất hàng", "Chứng từ bước 4 (cuối), do Kế toán lập để ghi nhận & hạch toán. Lập từ nút \"Tạo phiếu xuất hàng\" trên phiếu xuất kho."],
    ["Thủ kho", "Vai trò lập và thực hiện phiếu xuất kho (đi lấy hàng, chọn lô, xuất kho) tại kho mình phụ trách."],
    ["Kế toán kho", "Vai trò tiếp nhận phiếu xuất kho đã xuất để lập Phiếu xuất hàng hoặc từ chối (không duyệt)."],
    ["Lô nhập (import_lot)", "Đợt hàng nhập kho, dùng để truy xuất nguồn gốc & xuất theo nguyên tắc FIFO. Trên phiếu xuất kho phải chỉ rõ xuất từ lô nào."],
    ["Vị trí (position)", "Vị trí lưu trữ hàng trên kệ trong kho. Mỗi dòng hàng xuất phải chỉ rõ lấy ở vị trí nào."],
    ["Tiến trình (step)", "Giai đoạn xử lý phiếu: \"Đang đi lấy hàng\" (mới lập, đang phân công đi lấy) → \"Đang xuất kho\" / \"Hoàn thành xuất kho\"."],
    ["Phiếu đi lấy hàng (phiếu lấy hàng)", "Bước chia nhóm và phân công người đi lấy hàng theo lô, in ra để đi nhặt hàng trước khi xuất kho."],
    ["Loại xuất (type)", "Phân loại mục đích xuất; kế thừa từ Đề nghị xuất kho, không tự chọn."],
    ["Phiếu nhập lại / xuất lại", "Khi phiếu bị từ chối có thể nhập lại hàng về kho; sau đó có thể lập phiếu xuất lại."],
])

b.h2("2. Lịch sử cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Nội dung", "Người thực hiện"],
    ["1.0", "11/09/2026", "Khởi tạo HDSD màn Phiếu xuất kho (ERP)", "Phòng Phát triển"],
])

b.h2("3. Giới thiệu chung & đường dẫn truy cập")
b.para("Màn hình Phiếu xuất kho dùng để Thủ kho thực hiện việc xuất hàng ra khỏi kho: chọn lô hàng và vị trí cụ thể, phân công người đi lấy, xác nhận số lượng thực xuất và trừ tồn kho. Đây là bước biến đề nghị xuất kho thành hành động lấy hàng và xuất kho thực tế.")
b.bullet("menu Khởi tạo › Hàng hóa › Nhập - xuất hàng › \"Phiếu xuất kho\" (danh sách theo phạm vi quyền).", bold_prefix="Đường dẫn danh sách: ")
b.bullet("menu \"Phiếu xuất kho chờ duyệt\" dẫn tới danh sách các phiếu đã xuất, đang chờ Kế toán kho lập phiếu xuất hàng.", bold_prefix="Chờ duyệt (Kế toán kho): ")
b.bullet("màn Phiếu xuất kho được lập từ một Đề nghị xuất kho (PDNXK) đang chờ duyệt — Thủ kho mở đề nghị và bấm \"Tạo phiếu xuất kho\". Lập phiếu xuất kho đồng thời duyệt đề nghị đó.", bold_prefix="Điểm tạo phiếu: ")
b.para("Vị trí trong quy trình xuất hàng (4 chứng từ nối tiếp):")
b.table([
    ["Bước", "Chứng từ", "Người thực hiện", "Ghi chú"],
    ["1", "Yêu cầu xuất hàng", "Nhân viên kinh doanh", "Đề nghị xuất, gửi duyệt."],
    ["2", "Đề nghị xuất kho", "Kế toán kho", "Lập từ yêu cầu, gửi Thủ kho."],
    ["3", "Phiếu xuất kho", "Thủ kho", "Màn hình này — chọn lô, đi lấy hàng, xuất kho (trừ tồn thực tế)."],
    ["4", "Phiếu xuất hàng", "Kế toán", "Ghi nhận & hạch toán, hoàn tất."],
])

b.h2("4. Quyền & phạm vi (tổng quan)")
b.para("Phạm vi dữ liệu nhìn thấy và các thao tác đều phụ thuộc quyền. Màn này hầu như KHÔNG gắn quyền qua đường dẫn (route) mà kiểm soát trong xử lý nghiệp vụ. Các nhóm quyền chính:")
b.bullet("3 quyền xem theo cấp (tổng công ty / công ty / phòng ban) quyết định thấy phiếu của phạm vi nào; ngoài ra còn quyền \"Xem tất cả phiếu xuất nhập kho\". Không có quyền nào thì chỉ thấy phiếu do chính mình lập.", bold_prefix="Xem danh sách: ")
b.bullet("vai trò theo kho — lập và thực hiện phiếu xuất kho tại kho mình phụ trách (đi lấy hàng, chọn lô, xuất kho, hủy).", bold_prefix="Thủ kho: ")
b.bullet("tiếp nhận phiếu đã xuất để lập Phiếu xuất hàng (nút \"Tạo phiếu xuất hàng\") hoặc từ chối (Không duyệt); chỉ trong công ty mình.", bold_prefix="Kế toán kho: ")
b.para("Các thao tác Sửa / Hủy / đi lấy hàng phụ thuộc quyền sở hữu + trạng thái: chỉ người lập mới sửa/hủy phiếu ở trạng thái Đang tạo. Lưu ý: khác Đề nghị xuất kho, quyền xem phiếu xuất kho CHỈ có 3 cấp (tổng công ty / công ty / phòng ban), KHÔNG có cấp bộ phận. Màn Phiếu xuất kho KHÔNG bị chặn theo hạn mức/công nợ. Chi tiết ở PHẦN 2.")

# ------------------------------------------------- PHAN 1
b.h1("PHẦN 1: TRUY CẬP & BỐ CỤC MÀN HÌNH")

b.h2("1.1. Cách truy cập & các màn danh sách")
b.table([
    ["Màn", "Dùng cho", "Nội dung"],
    ["Phiếu xuất kho (danh sách)", "Thủ kho / người xem", "Phiếu xuất kho trong phạm vi quyền của người dùng; có nút Xuất Excel và Tạo mới (điều hướng)."],
    ["Phiếu xuất kho chờ duyệt", "Kế toán kho", "Phiếu đã xuất, chờ lập Phiếu xuất hàng hoặc từ chối."],
])
img_placeholder(b, "Ảnh menu Phiếu xuất kho và Phiếu xuất kho chờ duyệt.")

b.h2("1.2. Bố cục màn hình danh sách")
b.bullet("tiêu đề \"Danh sách phiếu xuất kho\".", bold_prefix="Thanh tiêu đề: ")
b.bullet("các ô tìm theo cột (Kho hàng, Tên/mã hàng hóa, Mã phiếu, Loại, Phiếu ĐNXK, Người đề nghị, Người yêu cầu, Người lập, Trạng thái, Người duyệt) và lọc theo khoảng thời gian.", bold_prefix="Khu vực lọc: ")
b.bullet("bảng liệt kê phiếu theo phạm vi quyền, cột Hành động ở cuối mỗi dòng.", bold_prefix="Bảng danh sách: ")
b.bullet("nút Xuất Excel, chọn số dòng/trang và chuyển trang.", bold_prefix="Công cụ & phân trang: ")
img_placeholder(b, "Ảnh tổng quan màn danh sách phiếu xuất kho.")

# ------------------------------------------------- PHAN 2
b.h1("PHẦN 2: DANH SÁCH PHIẾU XUẤT KHO")
img_placeholder(b, "Ảnh màn danh sách với dữ liệu mẫu và cột Hành động.")

b.h2("2.1. Phân quyền & hướng dẫn theo quyền")
b.para("Danh sách hiển thị theo phạm vi quyền của người đăng nhập. Bảng dưới liệt kê đầy đủ các quyền liên quan tới màn. Người dùng thường chỉ có một vài quyền — hãy đối chiếu đúng phần áp dụng cho mình.")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút/màn tương ứng"],
    ["Xem phiếu xuất kho theo tổng công ty", "Thấy toàn bộ phiếu (trạng thái khác nháp) của mọi công ty.", "Danh sách"],
    ["Xem phiếu xuất kho theo công ty", "Thấy phiếu trong công ty của mình.", "Danh sách"],
    ["Xem phiếu xuất kho theo phòng ban", "Thấy phiếu do nhân viên thuộc các phòng ban mình quản lý lập.", "Danh sách"],
    ["Xem tất cả phiếu xuất nhập kho", "Thấy phiếu thuộc các kho mình là thủ kho.", "Danh sách"],
    ["Thủ kho", "Lập phiếu xuất kho từ đề nghị; đi lấy hàng; chọn lô; xuất kho; sửa/hủy phiếu nháp của mình.", "Nút \"Tạo phiếu xuất kho\" (trên màn Đề nghị xuất kho); Phiếu lấy hàng; Sửa/Xuất kho; Hủy"],
    ["Kế toán kho", "Lập Phiếu xuất hàng từ phiếu đã xuất; từ chối (Không duyệt).", "Nút \"Tạo phiếu xuất hàng\", \"Không duyệt\""],
])
b.para("Lưu ý phạm vi: hệ thống xét quyền xem theo thứ tự tổng công ty → công ty → phòng ban → thủ kho (theo kho); nếu không có quyền nào ở trên, người dùng chỉ thấy phiếu do chính mình lập. Ngoài ra, phiếu nháp (Đang tạo) của người khác luôn bị ẩn — chỉ người lập mới thấy phiếu nháp của mình.")

b.h3("Người dùng có quyền \"Xem phiếu xuất kho theo tổng công ty\"")
b.para("Thấy toàn bộ phiếu (trạng thái khác nháp) của mọi công ty, cộng phiếu do chính mình lập. Thực hiện đầy đủ thao tác xem/lọc; sửa/hủy vẫn theo quy tắc sở hữu + trạng thái.")

b.h3("Người dùng có quyền \"Xem phiếu xuất kho theo công ty / phòng ban\"")
b.para("Thấy phiếu trong phạm vi công ty / phòng ban tương ứng mà mình phụ trách, cộng thêm phiếu do chính mình lập.")

b.h3("Người dùng là Thủ kho")
b.para("Thấy phiếu thuộc các kho mình phụ trách (nếu có quyền \"Xem tất cả phiếu xuất nhập kho\") và phiếu mình lập. Đây là vai trò chính của màn: lập phiếu xuất kho từ đề nghị, đi lấy hàng, chọn lô, xuất kho.")

b.h3("Người dùng là Kế toán kho")
b.para("Với phiếu đã xuất (Chờ duyệt / Đang hạch toán) trong công ty mình, Kế toán kho có nút \"Tạo phiếu xuất hàng\" để lập phiếu xuất hàng (bước 4) và nút \"Không duyệt\" để từ chối trả phiếu về.")

b.h2("2.2. Tìm kiếm & lọc")
b.table([
    ["Tiêu chí", "Cách dùng"],
    ["Kho hàng", "Chọn kho để lọc phiếu theo kho xuất."],
    ["Tên, mã hàng hóa", "Nhập để lọc phiếu có chứa hàng theo tên hoặc mã."],
    ["Mã phiếu", "Nhập mã phiếu xuất kho (PXK-…)."],
    ["Loại", "Chọn loại xuất."],
    ["Phiếu ĐNXK", "Nhập mã phiếu đề nghị xuất kho gốc (PDNXK-…)."],
    ["Người đề nghị", "Chọn (tìm theo tên) người đề nghị."],
    ["Người yêu cầu", "Chọn (tìm theo tên) người lập yêu cầu xuất hàng."],
    ["Người lập", "Chọn (tìm theo tên) người lập phiếu xuất kho."],
    ["Trạng thái", "Chọn trạng thái phiếu (xem mục 2.4)."],
    ["Người duyệt", "Chọn (tìm theo tên) người duyệt (Kế toán kho)."],
    ["Khoảng thời gian", "Lọc theo khoảng ngày lập phiếu."],
])

b.h2("2.3. Các cột trong danh sách")
b.table([
    ["Cột", "Ý nghĩa"],
    ["STT", "Số thứ tự dòng."],
    ["Mã phiếu", "Mã phiếu xuất kho. Bấm để mở: nếu đang đi lấy hàng → mở Phiếu lấy hàng; nếu đã xuất → mở chi tiết. Nếu là phiếu xuất lại có ghi chú \"Xuất lại cho phiếu …\"."],
    ["Loại", "Loại xuất (kế thừa từ đề nghị)."],
    ["Ngày lập", "Ngày tạo phiếu."],
    ["Phiếu ĐNXK", "Mã đề nghị xuất kho gốc (bấm để mở)."],
    ["Người đề nghị", "Người đề nghị xuất kho."],
    ["Người yêu cầu", "Người lập yêu cầu xuất hàng."],
    ["Người lập", "Người lập phiếu xuất kho (Thủ kho)."],
    ["Trạng thái", "Trạng thái phiếu, hiển thị nhãn màu."],
    ["Tiến trình", "Giai đoạn: Đang đi lấy hàng / Đang xuất kho / Hoàn thành xuất kho."],
    ["Người duyệt", "Kế toán kho đã duyệt / lập phiếu xuất hàng."],
    ["Ngày nhận", "Thời điểm phiếu được gửi tới kế toán."],
    ["Ngày duyệt", "Thời điểm duyệt."],
    ["Hành động", "Các nút thao tác (xem mục 2.5)."],
])

b.h2("2.4. Bảng trạng thái phiếu")
b.table([
    ["Trạng thái", "Ý nghĩa"],
    ["Đang tạo", "Phiếu nháp — đang lập/đi lấy hàng, chưa gửi. Chỉ người lập sửa/hủy được."],
    ["Chờ duyệt", "Đã xuất kho và gửi cho Kế toán kho, chờ lập phiếu xuất hàng."],
    ["Đang hạch toán", "Đã duyệt / đã lập phiếu xuất hàng, đang chờ hạch toán."],
    ["Đã hạch toán", "Phiếu xuất hàng đã hoàn tất hạch toán."],
    ["Không duyệt", "Bị Kế toán kho từ chối (kèm lý do)."],
    ["Đã nhập lại", "Đã lập phiếu nhập lại hàng về kho."],
    ["Đã xuất lại", "Đã lập phiếu xuất lại từ phiếu này."],
    ["Đã hủy", "Phiếu đã bị hủy."],
])
b.para("Ngoài trạng thái, cột Tiến trình cho biết phiếu đang \"Đang đi lấy hàng\" (mới lập, đang phân công người đi lấy) hay đã \"Đang xuất kho\" / \"Hoàn thành xuất kho\".")

b.h2("2.5. Thao tác trên từng dòng (cột Hành động)")
b.para("Các nút nằm trong menu thao tác và hiển thị tùy trạng thái, tiến trình, loại phiếu, quyền và quyền sở hữu:")
b.table([
    ["Nút", "Điều kiện hiển thị", "Kết quả"],
    ["Phiếu lấy hàng", "Phiếu Đang tạo và đang ở bước đi lấy hàng.", "Mở màn Phiếu đi lấy hàng (phân công, in phiếu lấy hàng)."],
    ["Sửa phiếu / Xuất kho", "Phiếu Đang tạo do chính bạn lập. Khi còn ở bước đi lấy hàng nút ghi \"Xuất kho\"; sau đó ghi \"Sửa phiếu\".", "Mở màn xuất kho (chọn lô, xác nhận số lượng, gửi)."],
    ["Tạo phiếu xuất hàng", "Bạn là Kế toán kho cùng công ty; phiếu Chờ duyệt.", "Mở màn lập Phiếu xuất hàng (loại 20/21 mở màn bên HRM)."],
    ["Tạo phiếu nhập lại", "Phiếu Không duyệt, do bạn lập (hoặc Super Admin).", "Mở màn lập Phiếu nhập lại."],
    ["Tạo phiếu xuất lại", "Phiếu Đã nhập lại, do bạn lập (hoặc Super Admin).", "Mở màn lập Phiếu xuất lại."],
    ["Hủy", "Phiếu Đang tạo do chính bạn lập.", "Hủy phiếu (cần xác nhận); phiếu chuyển Đã hủy."],
    ["In biên bản giao nhận - bàn giao", "Loại có giao hàng và đã xuất kho.", "Mở hộp chọn mẫu & đại diện rồi in."],
    ["In", "Luôn có.", "In phiếu xuất kho."],
])

# ------------------------------------------------- PHAN 3
b.h1("PHẦN 3: LẬP & XUẤT KHO")
b.para("Phiếu xuất kho do Thủ kho lập. Điểm vào lập phiếu là từ màn Đề nghị xuất kho: mở đề nghị đang chờ duyệt rồi bấm \"Tạo phiếu xuất kho\". Điều kiện: bạn là Thủ kho của kho xuất và đề nghị đang ở trạng thái Chờ duyệt. Việc lập phiếu xuất kho đồng thời là duyệt đề nghị đó.")
b.para("Quy trình xuất kho gồm hai giai đoạn nối tiếp:")
b.bullet("lập phiếu, chọn lô/vị trí dự kiến → sinh Phiếu đi lấy hàng (bước phân công người đi nhặt hàng, xem PHẦN 4).", bold_prefix="Giai đoạn 1 — Đang đi lấy hàng: ")
b.bullet("sau khi đã lấy hàng, mở màn xuất kho để xác nhận số kiện, chuyến xe, đính kèm chứng từ và Gửi → hệ thống trừ tồn kho thực tế và chuyển phiếu cho Kế toán kho.", bold_prefix="Giai đoạn 2 — Xuất kho: ")
img_placeholder(b, "Ảnh màn lập phiếu xuất kho (Dự kiến lấy hàng).")

b.h2("3.1. Thông tin chung (tab Thông tin chung)")
b.table([
    ["Trường", "Bắt buộc", "Hiện khi / ghi chú"],
    ["Loại yêu cầu", "—", "Chỉ hiển thị với loại xuất sản xuất / xuất thực hiện hợp đồng; luôn khóa (kế thừa từ đề nghị)."],
    ["Chọn phiếu đề nghị xuất kho", "Có", "Hiển thị mã đề nghị gốc; khi phiếu đã có mã (đã lưu) thì bị khóa, không đổi được."],
    ["Người nhận hàng", "Có", "Chọn nhân viên nhận hàng."],
    ["Kho xuất", "—", "Chỉ đọc — lấy từ đề nghị."],
    ["Người đề nghị", "—", "Chỉ đọc — người đề nghị xuất kho."],
    ["Ghi chú", "Không", "Ghi chú cho phiếu (tối đa 255 ký tự)."],
    ["File đính kèm", "Có khi Gửi", "Chỉ có ở màn xuất kho (sửa). Bắt buộc đính kèm ít nhất 1 chứng từ khi Lưu & Xuất; chấp nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, csv."],
    ["Hợp đồng", "—", "Chỉ đọc; chỉ hiện với loại xuất bán hàng (gắn hợp đồng)."],
])
b.para("Với loại xuất bán hàng, form hiển thị thêm khối thông tin khách hàng (chỉ đọc): Mã khách hàng, Khách hàng, Số điện thoại, Địa chỉ, Người liên hệ (và Điện thoại liên hệ), Địa chỉ giao hàng, cùng ô tích \"Hàng cồng kềnh / nặng trên 50kg\".")

b.h2("3.2. Chọn lô & vị trí (bảng Chi tiết — tab Hàng hóa)")
b.para("Đây là điểm khác biệt cốt lõi so với Đề nghị xuất kho: ở phiếu xuất kho phải chỉ rõ lấy hàng từ VỊ TRÍ nào và LÔ NHẬP nào, nhập số lượng xuất theo từng lô.")
b.para("Mỗi dòng hàng có thể tách thành nhiều dòng con (mỗi dòng là một cặp Vị trí + Lô). Các cột trong nhóm \"Chi tiết\":")
b.table([
    ["Cột", "Nhập được?", "Ghi chú"],
    ["Vị trí", "Chọn (nút tìm)", "Bấm biểu tượng tìm để chọn vị trí trên kệ; nếu chỉ có 1 vị trí phù hợp, hệ thống tự điền."],
    ["Lô", "Chọn (nút tìm)", "Chọn lô nhập; chỉ bật sau khi đã chọn vị trí. Nếu vị trí chỉ có 1 lô, hệ thống tự điền. Không được chọn trùng lô trong cùng một hàng."],
    ["Tồn", "Không", "Tồn hiện có của đúng vị trí + lô đó. Bị tô đỏ khi tồn nhỏ hơn số lượng muốn xuất."],
    ["SL xuất", "Có (nhập số)", "Số lượng xuất từ lô này. Tổng các dòng lô không được vượt số lượng đề nghị và không vượt tồn."],
])
b.para("Nút \"+ Thêm\" thêm một cặp vị trí/lô cho dòng hàng; nút xóa (X) bỏ một dòng lô. Ngoài nhóm lô, bảng còn có: Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, ĐV đề nghị, SL đề nghị, ĐV xuất (chọn đổi đơn vị), SL xuất theo ĐV đề nghị, và cột Kiện (chọn kiện đóng gói, ở màn xuất kho). Cuối bảng có dòng tổng cộng (tổng SL đề nghị, tổng tồn, tổng SL xuất).")
b.para("Với loại xuất bán theo hợp đồng hãng, hàng được chia theo các tab hạng mục hợp đồng; các tab này chỉ nhập số lượng, KHÔNG chọn lô.")
img_placeholder(b, "Ảnh bảng Chi tiết với phần chọn Vị trí / Lô / Tồn / SL xuất.")

b.h2("3.3. Tab Vận chuyển & tab Bốc xếp")
b.bullet("chỉ hiện với các loại có giao hàng. Chọn hình thức vận chuyển; nếu Công ty vận chuyển thì chọn Tuyến đường, xem Số Km dự kiến / Số Km chốt, nhập Ghi chú vận chuyển (bắt buộc khi km chốt khác km dự kiến) và chọn các Chuyến xe. Khi có chuyến xe, chuyến phải được duyệt thì mới gửi phiếu được.", bold_prefix="Tab Vận chuyển: ")
b.bullet("khai chi phí bốc xếp: tính theo khối lượng hay thời gian, loại hình thuê (Công ty / Thuê ngoài), nhà cung cấp, loại bốc xếp, khối lượng/số giờ, đơn giá, VAT. Nếu thuê Công ty thì lập bảng chia tiền cho từng nhân viên nhận việc (tổng tiền chia phải bằng tổng tiền bốc xếp).", bold_prefix="Tab Bốc xếp: ")

b.h2("3.4. Các nút lưu")
b.table([
    ["Nút", "Hành động"],
    ["Lưu", "Lưu phiếu ở trạng thái Đang tạo (nháp)."],
    ["Lưu & Xuất", "Xuất kho: trừ tồn thực tế và gửi cho Kế toán kho (chuyển sang Chờ duyệt). Bắt buộc đã đính kèm chứng từ và (nếu có chuyến xe) chuyến đã được duyệt."],
    ["In dự kiến", "In phiếu xuất kho dạng dự kiến để đối chiếu trước khi xuất (trên màn xuất kho)."],
    ["Hủy", "Quay lại danh sách, không lưu."],
])
b.para("Các nút Lưu / Lưu & Xuất chỉ bật khi mọi dòng lô có tồn đủ (tồn ≥ số lượng xuất) và hàng hợp lệ. Nếu bạn xuất ít hơn số lượng đề nghị, hệ thống hỏi xác nhận \"Bạn đang xuất kho ít hơn số lượng đề nghị!\".")

b.h2("3.5. Quy tắc kiểm tra dữ liệu (validate)")
b.table([
    ["Trường / tình huống", "Yêu cầu"],
    ["Phiếu đề nghị xuất kho", "Bắt buộc; phải tồn tại."],
    ["Người nhận hàng", "Bắt buộc."],
    ["Danh sách lô", "Bắt buộc ít nhất 1 dòng; mỗi dòng lô số lượng từ 0 đến 999.999."],
    ["Vị trí / Lô", "Bắt buộc khi số lượng > 0; không được trùng cặp vị trí + lô trong cùng một hàng; không xuất quá tồn của vị trí + lô đó."],
    ["Ghi chú", "Tối đa 255 ký tự."],
    ["Đính kèm (khi Lưu & Xuất)", "Bắt buộc ít nhất 1 file đúng định dạng cho phép."],
    ["Vận chuyển (Công ty vận chuyển)", "Bắt buộc chọn chuyến xe (không trùng); nhập Số Km chốt, Tuyến đường; ghi chú khi km lệch."],
    ["Bốc xếp thuê Công ty", "Tổng tiền chia cho các nhân viên phải bằng tổng tiền bốc xếp."],
])
b.para("Hệ thống còn kiểm tra hàng/vị trí đang trong đợt kiểm kho (không cho xuất) và lô đang chờ xuất lại. Thiếu dữ liệu hoặc vượt tồn sẽ báo lỗi ngay tại dòng tương ứng (tô đỏ) và không lưu cho tới khi sửa đủ.")

# ------------------------------------------------- PHAN 4
b.h1("PHẦN 4: PHIẾU ĐI LẤY HÀNG")
b.para("Sau khi lập phiếu, phiếu ở bước \"Đang đi lấy hàng\". Bấm \"Phiếu lấy hàng\" (trên dòng danh sách) để mở màn phân công đi lấy hàng.")
b.bullet("mỗi dòng lô hiển thị tên hàng, mã, vị trí, lô, số lượng. Kéo–thả để chia hàng thành các nhóm đi lấy; bấm \"+\" để thêm nhóm.", bold_prefix="Chia nhóm: ")
b.bullet("mỗi nhóm chọn \"Chọn người đi lấy\" (nhân viên) và \"Chọn chuyến xe\" (nếu do công ty vận chuyển).", bold_prefix="Phân công: ")
b.bullet("bấm \"In\" trên từng nhóm để in phiếu lấy hàng cho người đi nhặt hàng (hiện khi nhóm đã có hàng và đã chọn người đi lấy).", bold_prefix="In phiếu lấy hàng: ")
b.para("Khi mọi dòng đã được phân công người đi lấy, phiếu sẵn sàng để chuyển sang bước Xuất kho. Bấm \"Xuất kho\" để mở màn xác nhận xuất (PHẦN 3, giai đoạn 2). Nút \"Hủy\" quay về danh sách.")
img_placeholder(b, "Ảnh màn Phiếu đi lấy hàng (chia nhóm, phân công người đi lấy).")

# ------------------------------------------------- PHAN 5
b.h1("PHẦN 5: XEM CHI TIẾT & XỬ LÝ CỦA KẾ TOÁN KHO")

b.h2("5.1. Xem chi tiết")
b.para("Bấm Mã phiếu (khi phiếu đã xuất) để xem chi tiết. Trang chi tiết chỉ đọc, hiển thị đầy đủ thông tin chung, vận chuyển, bốc xếp và bảng hàng theo lô (Vị trí / Lô / SL xuất — không hiển thị đơn giá/thành tiền cho hàng hóa). Nếu phiếu từng bị từ chối, có card \"Ghi chú duyệt\" hiển thị lý do.")

b.h2("5.2. Kế toán kho xử lý phiếu Chờ duyệt")
b.para("Với phiếu đã xuất và đang Chờ duyệt trong công ty mình, Kế toán kho chọn một trong các thao tác (trên màn chi tiết hoặc dòng danh sách):")
b.bullet("mở màn lập Phiếu xuất hàng (bước 4) để ghi nhận & hạch toán. Với loại xuất bán/sản xuất theo hợp đồng (loại 20/21), hệ thống mở màn lập phiếu xuất hàng bên HRM.", bold_prefix="Tạo phiếu xuất hàng: ")
b.bullet("bấm \"Không duyệt\", nhập lý do (bắt buộc). Phiếu chuyển sang trạng thái Không duyệt; Thủ kho có thể lập phiếu nhập lại để đưa hàng về kho.", bold_prefix="Không duyệt (từ chối): ")

b.h2("5.3. Bảng tổng hợp nút thao tác trên trang chi tiết")
b.table([
    ["Nút", "Ai thấy / điều kiện", "Kết quả"],
    ["Không duyệt", "Kế toán kho cùng công ty; phiếu Chờ duyệt (hoặc đang hạch toán).", "Nhập lý do; phiếu chuyển Không duyệt."],
    ["Tạo phiếu xuất hàng", "Kế toán kho cùng công ty; phiếu Chờ duyệt.", "Mở màn lập Phiếu xuất hàng (ERP hoặc HRM tùy loại)."],
    ["Quay lại", "Luôn có.", "Về màn danh sách."],
])

# ------------------------------------------------- PHAN 6
b.h1("PHẦN 6: NHẬP LẠI & XUẤT LẠI")
b.para("Khi phiếu bị Kế toán kho từ chối (Không duyệt), hàng đã xuất cần được xử lý trả về kho rồi mới xuất lại:")
b.bullet("với phiếu ở trạng thái Không duyệt, người lập bấm \"Tạo phiếu nhập lại\" để đưa hàng về kho. Sau khi nhập lại, phiếu chuyển sang trạng thái Đã nhập lại.", bold_prefix="Tạo phiếu nhập lại: ")
b.bullet("với phiếu ở trạng thái Đã nhập lại, bấm \"Tạo phiếu xuất lại\" để lập một phiếu xuất kho mới dựa trên phiếu cũ (giữ nguyên thông tin). Phiếu gốc chuyển sang Đã xuất lại.", bold_prefix="Tạo phiếu xuất lại: ")
b.para("Các thao tác này chỉ dành cho người lập phiếu (hoặc quản trị) và đúng trạng thái tương ứng.")

# ------------------------------------------------- PHAN 7
b.h1("PHẦN 7: HỦY PHIẾU")
b.para("Màn Phiếu xuất kho KHÔNG có chức năng xóa hẳn phiếu; thao tác thu hồi là Hủy.")
b.para("Chỉ hủy được phiếu ở trạng thái Đang tạo (nháp) do chính mình lập. Bấm \"Hủy\" trên dòng danh sách, xác nhận. Sau khi hủy, phiếu chuyển sang Đã hủy, đồng thời đề nghị xuất kho gốc cũng được hủy tương ứng. Phiếu đã xuất (đã gửi) không hủy được tại màn này — nếu cần thu hồi, dùng luồng Không duyệt → Nhập lại (PHẦN 5, 6).")

# ------------------------------------------------- PHAN 8
b.h1("PHẦN 8: IN ẤN & XUẤT EXCEL")
b.table([
    ["Chức năng", "Nội dung"],
    ["In", "In mẫu Phiếu xuất kho tiêu chuẩn (từ menu thao tác trên mỗi dòng)."],
    ["In phiếu lấy hàng", "In phiếu cho từng nhóm người đi lấy hàng (trên màn Phiếu đi lấy hàng)."],
    ["In dự kiến", "In phiếu xuất kho dạng dự kiến để đối chiếu trước khi xuất (trên màn xuất kho)."],
    ["In biên bản giao nhận - bàn giao", "Mở hộp chọn mẫu biên bản và người đại diện (đại diện bên giao, bên nhận, chức vụ, số điện thoại) rồi in. Bao gồm biên bản giao nhận, biên bản nghiệm thu thiết bị và biên bản bàn giao thiết bị/sơ bộ (tùy loại và mẫu chọn)."],
    ["Xuất Excel danh sách", "Tải file Excel danh sách phiếu theo bộ lọc & phạm vi hiện tại. Danh sách quá lớn (≥ 2000 dòng) sẽ được gửi qua email."],
])

# ------------------------------------------------- PHAN 9
b.h1("PHẦN 9: CÂU HỎI THƯỜNG GẶP & LƯU Ý")
b.table([
    ["Tình huống", "Giải thích / cách xử lý"],
    ["Lập phiếu xuất kho ở đâu?", "Không tạo trực tiếp từ menu Phiếu xuất kho mà từ màn Đề nghị xuất kho: mở đề nghị đang chờ duyệt rồi bấm \"Tạo phiếu xuất kho\". Cần là Thủ kho của kho xuất."],
    ["Không lưu/xuất được vì dòng lô bị đỏ", "Tồn của vị trí + lô đó nhỏ hơn số lượng muốn xuất, hoặc chưa chọn đủ vị trí/lô. Chọn lại lô khác hoặc giảm số lượng."],
    ["Chọn được vị trí nhưng không chọn được lô", "Nút chọn lô chỉ bật sau khi đã chọn vị trí. Chọn vị trí trước; nếu vị trí chỉ có 1 lô, hệ thống tự điền."],
    ["Bấm Lưu & Xuất báo thiếu chứng từ", "Khi gửi phiếu (xuất kho) bắt buộc đính kèm ít nhất 1 file chứng từ đúng định dạng."],
    ["Bấm Lưu & Xuất báo cần duyệt xe", "Phiếu có chuyến xe do công ty vận chuyển nhưng chuyến chưa được duyệt. Duyệt chuyến xe xuất phát rồi gửi lại; trong lúc đó phiếu vẫn ở trạng thái Đang tạo."],
    ["Không thấy nút \"Tạo phiếu xuất hàng\"", "Nút này chỉ dành cho Kế toán kho cùng công ty, với phiếu ở trạng thái Chờ duyệt. Loại xuất bán/sản xuất theo hợp đồng sẽ mở màn lập phiếu bên HRM."],
    ["Phiếu bị từ chối thì làm gì?", "Xem lý do ở card \"Ghi chú duyệt\", lập Phiếu nhập lại để đưa hàng về kho, sau đó Tạo phiếu xuất lại (PHẦN 6)."],
    ["Muốn xóa hẳn phiếu", "Màn này không có xóa. Phiếu nháp lập nhầm thì dùng Hủy; phiếu đã xuất thì dùng luồng Không duyệt → Nhập lại."],
    ["Danh sách trống dù có nhiều phiếu", "Có thể bạn chưa có quyền xem cấp phù hợp (chỉ thấy phiếu của mình). Liên hệ quản trị để cấp quyền xem theo công ty/phòng ban, hoặc cần là thủ kho của kho."],
])

# ============================================================ FINISH
finish_macos(b)
print("XONG.")
