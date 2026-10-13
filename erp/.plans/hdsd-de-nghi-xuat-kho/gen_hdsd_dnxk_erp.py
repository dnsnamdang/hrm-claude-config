# -*- coding: utf-8 -*-
"""Dung HDSD man 'De nghi xuat kho' (Phieu de nghi xuat kho / PDNXK) - ERP TanPhatDev.

Nguon: khao sat controller Warehouse\\WarehouseExportRequestsController + model
WarehouseExportRequest (+ ExportModel) + views warehouse/warehouse_export_requests +
PermissionsTableSeeder. KHONG chen anh (user chot khong can) -> dung o placeholder.

Chay:  /usr/local/bin/python3 gen_hdsd_dnxk_erp.py
Output: ERP/HDSD_luongchinh/HDSD_DeNghiXuatKho.docx
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
OUTPUT = os.path.join(OUT_DIR, "HDSD_DeNghiXuatKho.docx")

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
    cover_title="(Màn hình: Đề nghị xuất kho)",
    doc_title="HDSD - Đề nghị xuất kho",
)

# ------------------------------------------------- TONG QUAN
b.h1("TỔNG QUAN PHẦN MỀM")

b.h2("1. Thuật ngữ & viết tắt")
b.para("Bảng thuật ngữ giúp người dùng hiểu đúng các bước hướng dẫn.")
b.table([
    ["Thuật ngữ", "Ý nghĩa"],
    ["Đề nghị xuất kho (ĐNXK / PDNXK)", "Chứng từ bước 2 của quy trình xuất hàng: do Kế toán kho lập từ Yêu cầu xuất hàng, gửi cho Thủ kho xử lý. Đây chính là màn hình tài liệu này hướng dẫn. Mã phiếu có dạng PDNXK-xxxxx."],
    ["Yêu cầu xuất hàng (YCXH)", "Chứng từ bước 1, do nhân viên kinh doanh lập. Đề nghị xuất kho được sinh ra từ Yêu cầu xuất hàng (hoặc Yêu cầu xuất ghép / xuất tách)."],
    ["Phiếu xuất kho", "Chứng từ bước 3, do Thủ kho lập từ Đề nghị xuất kho để thực hiện xuất."],
    ["Phiếu xuất hàng", "Chứng từ bước 4 (cuối), ghi nhận & hạch toán xuất hàng."],
    ["Phiếu điều chuyển kho", "Với đề nghị loại xuất điều chuyển cùng thủ kho, bước tiếp là lập Phiếu điều chuyển kho thay cho Phiếu xuất kho."],
    ["Loại xuất (type)", "Phân loại mục đích xuất. Đề nghị xuất kho KHÔNG tự chọn loại mà kế thừa loại từ Yêu cầu xuất hàng gốc."],
    ["Kế toán kho", "Vai trò lập Đề nghị xuất kho từ Yêu cầu xuất hàng đã duyệt."],
    ["Thủ kho", "Vai trò tiếp nhận Đề nghị xuất kho tại kho mình phụ trách để lập Phiếu xuất kho / Phiếu điều chuyển, hoặc từ chối trả lại."],
    ["Trưởng phòng kế toán", "Vai trò được xem chi tiết mọi đề nghị (trạng thái khác nháp)."],
    ["SL được xuất", "Số lượng tối đa được phép xuất của mỗi dòng hàng, tính theo tồn kho / số đang giữ tùy loại."],
    ["SL đang giữ", "Số lượng hàng đã được giữ trước (prepick) cho phiếu, hiển thị với loại xuất bán hàng / xuất bán SC-BD."],
    ["SL đề nghị", "Số lượng người lập đề nghị xuất cho từng dòng hàng (trường nhập chính trên form)."],
])

b.h2("2. Lịch sử cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Nội dung", "Người thực hiện"],
    ["1.0", "09/09/2026", "Khởi tạo HDSD màn Đề nghị xuất kho (ERP)", "Phòng Phát triển"],
])

b.h2("3. Giới thiệu chung & đường dẫn truy cập")
b.para("Màn hình Đề nghị xuất kho dùng để lập và quản lý các phiếu đề nghị xuất kho — bước trung gian giữa Yêu cầu xuất hàng và Phiếu xuất kho. Kế toán kho gom hàng hóa và kho xuất từ Yêu cầu xuất hàng đã duyệt để lập đề nghị, gửi cho Thủ kho thực hiện.")
b.bullet("menu Khởi tạo › Hàng hóa › Nhập - xuất hàng › \"Đề nghị xuất kho\" (danh sách theo phạm vi quyền).", bold_prefix="Đường dẫn danh sách: ")
b.bullet("menu \"Phiếu đề nghị xuất kho chờ duyệt\" dẫn tới danh sách các phiếu đang chờ Thủ kho xử lý tại kho mình phụ trách.", bold_prefix="Chờ duyệt (Thủ kho): ")
b.bullet("màn Đề nghị xuất kho KHÔNG có nút \"Tạo mới\". Việc lập đề nghị được khởi phát từ màn Yêu cầu xuất hàng (hoặc Yêu cầu xuất ghép / xuất tách): Kế toán kho mở phiếu yêu cầu đã duyệt rồi bấm lập đề nghị xuất kho.", bold_prefix="Điểm tạo phiếu: ")
b.para("Vị trí trong quy trình xuất hàng (4 chứng từ nối tiếp):")
b.table([
    ["Bước", "Chứng từ", "Người thực hiện", "Ghi chú"],
    ["1", "Yêu cầu xuất hàng", "Nhân viên kinh doanh", "Đề nghị xuất, gửi duyệt."],
    ["2", "Đề nghị xuất kho", "Kế toán kho", "Màn hình này — lập từ Yêu cầu xuất hàng, gửi Thủ kho."],
    ["3", "Phiếu xuất kho", "Thủ kho", "Thực hiện xuất (hoặc Phiếu điều chuyển kho)."],
    ["4", "Phiếu xuất hàng", "Kế toán", "Ghi nhận & hạch toán, hoàn tất."],
])

b.h2("4. Quyền & phạm vi (tổng quan)")
b.para("Phạm vi dữ liệu nhìn thấy và các thao tác đều phụ thuộc quyền. Màn này KHÔNG gắn quyền qua đường dẫn (route) mà kiểm soát trong xử lý nghiệp vụ. Các nhóm quyền chính:")
b.bullet("3 quyền xem theo cấp (tổng công ty / công ty / phòng ban) quyết định thấy đề nghị của phạm vi nào; không có quyền nào thì chỉ thấy phiếu do chính mình lập.", bold_prefix="Xem danh sách: ")
b.bullet("cần để lập Đề nghị xuất kho từ Yêu cầu xuất hàng (điều kiện bắt buộc khi tạo phiếu).", bold_prefix="Kế toán kho: ")
b.bullet("vai trò theo kho — tiếp nhận đề nghị tại kho mình phụ trách để tạo Phiếu xuất kho / Phiếu điều chuyển hoặc từ chối.", bold_prefix="Thủ kho: ")
b.bullet("được xem chi tiết mọi đề nghị (trạng thái khác nháp).", bold_prefix="Trưởng phòng kế toán: ")
b.para("Các thao tác Sửa / Hủy không phụ thuộc quyền mà phụ thuộc quyền sở hữu + trạng thái: chỉ người lập mới sửa/hủy được phiếu ở trạng thái Đang tạo (nháp). Màn này KHÔNG có chức năng xóa hẳn phiếu — chỉ có Hủy. Màn Đề nghị xuất kho KHÔNG bị chặn duyệt theo hạn mức/công nợ. Chi tiết ở PHẦN 2 và PHẦN 5.")

# ------------------------------------------------- PHAN 1
b.h1("PHẦN 1: TRUY CẬP & BỐ CỤC MÀN HÌNH")

b.h2("1.1. Cách truy cập & các màn danh sách")
b.para("Hệ thống có các màn danh sách dùng chung một nguồn dữ liệu nhưng phục vụ các vai trò khác nhau:")
b.table([
    ["Màn", "Dùng cho", "Nội dung"],
    ["Đề nghị xuất kho (danh sách)", "Người lập / người xem", "Đề nghị trong phạm vi quyền của người dùng; có nút Xuất Excel."],
    ["Phiếu đề nghị xuất kho chờ duyệt", "Thủ kho", "Đề nghị đang Chờ duyệt tại kho mình phụ trách, để tạo phiếu xuất kho / điều chuyển hoặc từ chối."],
    ["Màn Thủ kho (forWarehouse)", "Thủ kho", "Danh sách đề nghị gửi tới kho mình phụ trách (ẩn phiếu nháp). Không có nút Xuất Excel."],
])
b.para("Lưu ý: các màn danh sách này KHÔNG có nút \"Tạo mới\" — đề nghị được lập từ màn Yêu cầu xuất hàng.")
img_placeholder(b, "Ảnh menu Đề nghị xuất kho và Phiếu đề nghị xuất kho chờ duyệt.")

b.h2("1.2. Bố cục màn hình danh sách")
b.bullet("tiêu đề \"Danh sách đề nghị xuất kho\".", bold_prefix="Thanh tiêu đề: ")
b.bullet("các ô tìm theo cột (Tên/mã hàng hóa, Mã phiếu, Loại, Phiếu YCXH, Người yêu cầu, Người lập, Khách hàng, Trạng thái, Người duyệt) và lọc theo khoảng thời gian, theo phạm vi.", bold_prefix="Khu vực lọc: ")
b.bullet("bảng liệt kê đề nghị theo phạm vi quyền, cột Hành động ở cuối mỗi dòng.", bold_prefix="Bảng danh sách: ")
b.bullet("nút Xuất Excel (trên màn danh sách chính), chọn số dòng/trang và chuyển trang.", bold_prefix="Công cụ & phân trang: ")
img_placeholder(b, "Ảnh tổng quan màn danh sách đề nghị xuất kho.")

# ------------------------------------------------- PHAN 2
b.h1("PHẦN 2: DANH SÁCH ĐỀ NGHỊ XUẤT KHO")
img_placeholder(b, "Ảnh màn danh sách với dữ liệu mẫu và cột Hành động.")

b.h2("2.1. Phân quyền & hướng dẫn theo quyền")
b.para("Danh sách hiển thị theo phạm vi quyền của người đăng nhập. Bảng dưới liệt kê đầy đủ các quyền liên quan tới màn. Người dùng thường chỉ có một vài quyền — hãy đối chiếu đúng phần áp dụng cho mình.")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút/màn tương ứng"],
    ["Xem đề nghị xuất kho theo tổng công ty", "Thấy toàn bộ đề nghị của mọi công ty.", "Danh sách"],
    ["Xem đề nghị xuất kho theo công ty", "Thấy đề nghị trong công ty của mình.", "Danh sách"],
    ["Xem đề nghị xuất kho theo phòng ban", "Thấy đề nghị thuộc các phòng ban mình quản lý (và phiếu mình lập).", "Danh sách"],
    ["Kế toán kho", "Lập Đề nghị xuất kho từ Yêu cầu xuất hàng đã duyệt (cùng công ty với phiếu yêu cầu).", "Nút lập đề nghị trên màn Yêu cầu xuất hàng"],
    ["Thủ kho", "Tiếp nhận đề nghị tại kho mình phụ trách; tạo Phiếu xuất kho / Phiếu điều chuyển; từ chối đề nghị.", "Nút \"Tạo phiếu xuất kho\", \"Tạo phiếu điều chuyển kho\", \"Không duyệt\"; màn chờ duyệt"],
    ["Trưởng phòng kế toán", "Xem chi tiết mọi đề nghị (trạng thái khác nháp).", "Màn chi tiết"],
])
b.para("Lưu ý phạm vi: hệ thống xét quyền xem theo thứ tự tổng công ty → công ty → phòng ban → Thủ kho (theo kho); nếu không có quyền nào ở trên, người dùng chỉ thấy đề nghị do chính mình lập. Ngoài ra, phiếu nháp (Đang tạo) của người khác luôn bị ẩn — chỉ người lập mới thấy phiếu nháp của mình. (Quyền \"Xem đề nghị xuất kho theo bộ phận\" có trong hệ thống nhưng hiện chưa được dùng để lọc dữ liệu.)")

b.h3("Người dùng có quyền \"Xem đề nghị xuất kho theo tổng công ty\"")
b.para("Thấy toàn bộ đề nghị của mọi công ty. Thực hiện đầy đủ thao tác xem/lọc; sửa/hủy vẫn theo quy tắc sở hữu + trạng thái (PHẦN 5).")

b.h3("Người dùng có quyền \"Xem đề nghị xuất kho theo công ty / phòng ban\"")
b.para("Thấy đề nghị trong phạm vi công ty / phòng ban tương ứng mà mình phụ trách, cộng thêm phiếu do chính mình lập. Phòng ban được xác định theo phân công quản lý của nhân viên.")

b.h3("Người dùng là Thủ kho")
b.para("Thấy các đề nghị gửi tới kho mình phụ trách. Với đề nghị đang Chờ duyệt, có các nút xử lý: \"Tạo phiếu xuất kho\" (đề nghị thường), \"Tạo phiếu điều chuyển kho\" (đề nghị điều chuyển cùng thủ kho), hoặc \"Không duyệt\" để trả đề nghị về nháp. Đây là vai trò thực hiện bước tiếp của quy trình.")

b.h3("Người dùng là Kế toán kho")
b.para("Là vai trò lập đề nghị (từ màn Yêu cầu xuất hàng). Trên danh sách đề nghị, xem được các phiếu trong phạm vi quyền xem của mình; sửa/hủy phiếu nháp do chính mình lập.")

b.h3("Người dùng là Trưởng phòng kế toán")
b.para("Được xem chi tiết mọi đề nghị đã gửi (trạng thái khác nháp), phục vụ giám sát; không có nút thao tác xử lý kho.")

b.h2("2.2. Tìm kiếm & lọc")
b.para("Các ô lọc theo cột trên danh sách:")
b.table([
    ["Tiêu chí", "Cách dùng"],
    ["Tên, mã hàng hóa", "Nhập để lọc đề nghị có chứa hàng theo tên hoặc mã."],
    ["Mã phiếu", "Nhập mã đề nghị (PDNXK-…)."],
    ["Loại", "Chọn loại xuất (xem mục 2.5)."],
    ["Phiếu YCXH", "Nhập mã phiếu yêu cầu xuất hàng gốc."],
    ["Người yêu cầu", "Chọn (tìm theo tên) người lập phiếu yêu cầu xuất hàng."],
    ["Người lập", "Chọn (tìm theo tên) người lập đề nghị."],
    ["Khách hàng", "Chọn (tìm theo tên) để lọc."],
    ["Trạng thái", "Chọn trạng thái đề nghị (xem mục 2.4)."],
    ["Người duyệt", "Chọn (tìm theo tên) Thủ kho đã duyệt."],
    ["Khoảng thời gian", "Lọc theo khoảng ngày lập đề nghị."],
])

b.h2("2.3. Các cột trong danh sách")
b.table([
    ["Cột", "Ý nghĩa"],
    ["STT", "Số thứ tự dòng."],
    ["Mã phiếu", "Mã đề nghị xuất kho (bấm để mở chi tiết)."],
    ["Loại", "Loại xuất (kế thừa từ Yêu cầu xuất hàng)."],
    ["Phiếu YCXH", "Mã phiếu yêu cầu xuất hàng / xuất ghép gốc (bấm để mở)."],
    ["Khách hàng", "Khách hàng của phiếu."],
    ["Người yêu cầu", "Người lập phiếu yêu cầu xuất hàng (mã phòng - họ tên)."],
    ["Người lập", "Người lập đề nghị (Kế toán kho)."],
    ["Ngày lập", "Ngày tạo đề nghị."],
    ["Trạng thái", "Trạng thái đề nghị, hiển thị nhãn màu."],
    ["Người duyệt", "Thủ kho đã duyệt."],
    ["Ngày nhận", "Thời điểm đề nghị được gửi tới kho."],
    ["Ngày duyệt", "Thời điểm Thủ kho duyệt."],
    ["Hành động", "Các nút thao tác (xem mục 2.4 dưới bảng trạng thái)."],
])

b.h2("2.4. Bảng trạng thái phiếu")
b.table([
    ["Trạng thái", "Ý nghĩa"],
    ["Đang tạo", "Phiếu nháp — chưa gửi, hoặc bị Thủ kho từ chối. Chỉ người lập sửa/hủy được."],
    ["Chờ duyệt", "Đã gửi tới Thủ kho, chờ xử lý (tạo phiếu xuất / điều chuyển hoặc từ chối)."],
    ["Đang xuất kho", "Thủ kho đã duyệt, đang lập / thực hiện phiếu xuất kho."],
    ["Đã xuất kho", "Đã xuất kho xong."],
    ["Đang hạch toán / Đã hạch toán", "Đang / đã ghi nhận hạch toán."],
    ["Đã hủy", "Phiếu đã bị hủy."],
])

b.h2("2.5. Thao tác trên từng dòng (cột Hành động)")
b.para("Các nút nằm trong menu thao tác (biểu tượng bánh răng) và hiển thị tùy trạng thái, loại phiếu, quyền và quyền sở hữu:")
b.table([
    ["Nút", "Điều kiện hiển thị", "Kết quả"],
    ["Sửa đề nghị", "Phiếu Đang tạo do chính bạn lập.", "Mở màn sửa đề nghị."],
    ["Hủy đề nghị", "Phiếu Đang tạo do chính bạn lập.", "Hủy phiếu (cần xác nhận); phiếu chuyển sang Đã hủy."],
    ["Tạo phiếu xuất kho", "Bạn là Thủ kho của kho xuất; phiếu Chờ duyệt; không phải loại điều chuyển cùng thủ kho.", "Mở màn lập Phiếu xuất kho (bước 3)."],
    ["Tạo phiếu điều chuyển kho", "Bạn là Thủ kho của kho xuất; phiếu Chờ duyệt; là loại xuất điều chuyển cùng thủ kho.", "Mở màn lập Phiếu điều chuyển kho."],
    ["In đề nghị", "Luôn có.", "In phiếu đề nghị xuất kho."],
    ["In bộ giấy tờ đi đường", "Luôn có.", "In lệnh điều động + phiếu xuất kho đi đường (giấy tờ vận chuyển)."],
])
b.para("Nếu không thấy nút Sửa/Hủy: phiếu đã qua trạng thái Đang tạo, hoặc không phải phiếu của bạn. Không thấy nút Tạo phiếu xuất kho / điều chuyển: bạn không phải Thủ kho của kho xuất, hoặc phiếu chưa ở trạng thái Chờ duyệt. Chức năng từ chối (Không duyệt) nằm trong trang chi tiết phiếu (xem PHẦN 4), không đặt trên dòng danh sách.")

# ------------------------------------------------- PHAN 3
b.h1("PHẦN 3: LẬP & SỬA ĐỀ NGHỊ XUẤT KHO")
b.para("Đề nghị xuất kho do Kế toán kho lập. Điểm vào lập phiếu là từ màn Yêu cầu xuất hàng (hoặc Yêu cầu xuất ghép / xuất tách): mở phiếu yêu cầu đã duyệt rồi bấm lập đề nghị xuất kho — hệ thống mở form lập đề nghị với dữ liệu lấy sẵn từ phiếu yêu cầu. Điều kiện: bạn có quyền Kế toán kho và cùng công ty với phiếu yêu cầu.")
img_placeholder(b, "Ảnh màn lập Đề nghị xuất kho (form).")

b.h2("3.1. Thông tin đầu phiếu")
b.para("Đầu form hiển thị tên loại xuất và ở góc phải là Người lập - Ngày lập (mặc định là người đăng nhập và ngày hôm nay). Loại xuất kế thừa từ phiếu yêu cầu, không tự chọn.")
b.table([
    ["Trường", "Bắt buộc", "Hiện khi / ghi chú"],
    ["Loại xuất", "—", "Chỉ hiển thị với loại xuất sản xuất / xuất thực hiện hợp đồng; luôn bị khóa (không đổi được)."],
    ["Chọn phiếu yêu cầu xuất hàng", "Có", "Hiển thị mã phiếu yêu cầu gốc. Khi đang sửa, không đổi được phiếu yêu cầu."],
    ["Hợp đồng / đơn hàng", "Có (khi hiện)", "Hiển thị (chỉ đọc) với các loại gắn hợp đồng (xuất thực hiện hợp đồng, xuất bán hàng…)."],
    ["Người yêu cầu", "—", "Chỉ đọc — người lập phiếu yêu cầu xuất hàng."],
    ["Kho xuất", "Có", "Chọn kho xuất. Bị khóa và lấy tự động theo phiếu yêu cầu, TRỪ loại xuất điều chuyển kho chi nhánh (được chọn kho)."],
    ["Kho nhập", "Có (khi hiện)", "Chỉ hiện với loại điều chuyển (cùng thủ kho / nội bộ); chỉ đọc."],
    ["Khách hàng", "—", "Chỉ hiện với loại xuất hàng gửi; chỉ đọc."],
    ["KD chịu vận chuyển", "Không", "Ô tích, với các loại có giao hàng."],
    ["Ghi chú", "Không", "Mặc định kế thừa ghi chú từ phiếu yêu cầu; tối đa 255 ký tự."],
    ["File đính kèm", "Không", "Chỉ hiện với loại xuất sản xuất / xuất thực hiện hợp đồng; chấp nhận pdf, png, jpg, doc, docx, xls, xlsx."],
])
b.para("Với các loại gắn khách hàng, form còn hiển thị khối thông tin khách hàng (chỉ đọc): Mã khách hàng, Khách hàng, Số điện thoại, Địa chỉ, Người liên hệ, Địa chỉ giao hàng.")

b.h2("3.2. Bảng hàng hóa & các tab")
b.para("Bảng hàng hóa chỉ hiển thị sau khi đã có phiếu yêu cầu. Có các tab:")
b.bullet("danh sách sản phẩm chính của đề nghị.", bold_prefix="Tab \"Hàng hóa\": ")
b.bullet("với loại xuất bán theo hợp đồng hãng, hàng được chia theo từng hạng mục (tab) của hợp đồng hãng. Tab có lỗi số lượng sẽ hiện cảnh báo màu đỏ.", bold_prefix="Tab theo hợp đồng: ")
b.bullet("bảng gộp sản phẩm (với các loại phù hợp).", bold_prefix="Tab \"Danh sách tổng hợp\": ")
b.para("Các cột bảng hàng hóa:")
b.table([
    ["Cột", "Nhập được?", "Ghi chú"],
    ["STT", "Không", ""],
    ["Cần xuất", "Có (ô tích)", "Bỏ tích → dòng mờ, không tính vào tổng và không nhập số lượng."],
    ["Tên hàng hóa / Model / Mã hàng hóa / Thương hiệu", "Không", "Thông tin hàng, lấy theo phiếu yêu cầu."],
    ["SL được xuất", "Không", "Số lượng tối đa được xuất, tính theo tồn / số giữ tùy loại."],
    ["SL đang giữ", "Không", "Chỉ hiện với loại xuất bán hàng / xuất bán SC-BD."],
    ["SL đề nghị", "Có (nhập số)", "Bắt buộc; là số lượng đề nghị xuất. Không được vượt SL được xuất."],
    ["Đơn vị tính", "Không", "ĐVT của dòng hàng."],
    ["Hình ảnh tham khảo", "Không", "Ảnh minh họa."],
])
b.para("Cuối bảng có dòng tổng cộng: Tổng SL được xuất / Tổng SL đang giữ (nếu có) / Tổng SL đề nghị. Lưu ý: ở màn Đề nghị xuất kho chỉ chọn KHO, KHÔNG chọn lô — việc chọn lô thực hiện ở bước Phiếu xuất kho phía sau. Khi đổi kho xuất, hệ thống cập nhật lại tồn/giữ cho từng dòng.")

b.h2("3.3. Các nút lưu")
b.table([
    ["Nút", "Hành động"],
    ["Lưu", "Lưu đề nghị ở trạng thái Đang tạo (nháp)."],
    ["Lưu & Gửi", "Gửi đề nghị cho Thủ kho — chuyển trạng thái Chờ duyệt; hệ thống giữ hàng và gửi thông báo tới Thủ kho của kho."],
    ["Hủy", "Quay lại danh sách, không lưu."],
])
b.para("Hai nút Lưu / Lưu & Gửi chỉ bật khi đề nghị hợp lệ: có ít nhất một dòng được tích \"Cần xuất\" với số lượng lớn hơn 0, và không dòng nào vượt SL được xuất.")

b.h2("3.4. Quy tắc kiểm tra dữ liệu (validate)")
b.table([
    ["Trường / tình huống", "Yêu cầu"],
    ["Kho xuất", "Bắt buộc; kho hợp lệ (không phải kho cấm xuất thường)."],
    ["Danh sách hàng", "Bắt buộc ít nhất 1 dòng; mỗi dòng số lượng từ 0 đến 999.999."],
    ["SL đề nghị", "Không được vượt số lượng trên Yêu cầu xuất hàng; không được vượt SL được xuất (đủ tồn / đủ số giữ theo cơ chế của loại)."],
    ["Ghi chú", "Tối đa 255 ký tự."],
    ["Xuất bán theo hợp đồng hãng", "Bắt buộc chia tab theo hạng mục hợp đồng; tổng số lượng các nhóm phải khớp tổng số lượng sản phẩm."],
    ["Quyền", "Người lập phải có quyền Kế toán kho và cùng công ty với phiếu yêu cầu."],
])
b.para("Thiếu dữ liệu bắt buộc hoặc số lượng vượt tồn sẽ báo lỗi ngay tại dòng tương ứng (dòng vượt tồn bị tô đỏ) và không lưu cho tới khi sửa đủ.")

b.h2("3.5. Sửa đề nghị")
b.para("Chỉ sửa được đề nghị ở trạng thái Đang tạo do chính mình lập (nút \"Sửa đề nghị\" trên dòng danh sách hoặc trong chi tiết). Khi sửa, không đổi được phiếu yêu cầu xuất hàng gốc. Lưu lại có thể chọn giữ nháp (Lưu) hoặc gửi lại cho Thủ kho (Lưu & Gửi). Nếu lưu về nháp, phiếu yêu cầu gốc quay về trạng thái đang lập đề nghị.")

# ------------------------------------------------- PHAN 4
b.h1("PHẦN 4: XEM CHI TIẾT & XỬ LÝ (THỦ KHO)")

b.h2("4.1. Xem chi tiết")
b.para("Bấm Mã phiếu (hoặc mở chi tiết) để xem đề nghị. Trang chi tiết là chế độ chỉ đọc, hiển thị đầy đủ thông tin chung, danh sách hàng kèm cột Đơn giá / Thành tiền và tổng tiền, trạng thái, người lập, người duyệt. Nếu đề nghị từng bị từ chối, có card \"Ghi chú duyệt\" hiển thị lý do. Quyền xem: Trưởng phòng kế toán / Thủ kho của kho (khi phiếu đã gửi), hoặc người lập đề nghị / người lập phiếu yêu cầu.")

b.h2("4.2. Thủ kho xử lý đề nghị Chờ duyệt")
b.para("Với đề nghị đang Chờ duyệt tại kho mình phụ trách, Thủ kho mở chi tiết và chọn một trong các thao tác:")
b.bullet("với đề nghị thường, bấm để mở màn lập Phiếu xuất kho (bước 3). Sau khi Thủ kho hoàn tất, đề nghị chuyển sang Đang xuất kho.", bold_prefix="Tạo phiếu xuất kho: ")
b.bullet("với đề nghị loại xuất điều chuyển cùng thủ kho, bấm để mở màn lập Phiếu điều chuyển kho thay cho phiếu xuất kho.", bold_prefix="Tạo phiếu điều chuyển kho: ")
b.bullet("bấm \"Không duyệt\", nhập lý do (bắt buộc). Đề nghị trả về trạng thái Đang tạo để Kế toán kho chỉnh sửa; phiếu yêu cầu gốc quay về trạng thái đang lập đề nghị.", bold_prefix="Không duyệt (từ chối): ")

b.h2("4.3. Bảng tổng hợp nút thao tác trên trang chi tiết")
b.table([
    ["Nút", "Ai thấy / điều kiện", "Kết quả"],
    ["Không duyệt", "Thủ kho của kho xuất; phiếu Chờ duyệt.", "Nhập lý do; đề nghị về Đang tạo."],
    ["Tạo phiếu xuất kho", "Thủ kho; phiếu Chờ duyệt; không phải loại điều chuyển cùng thủ kho.", "Mở màn lập Phiếu xuất kho."],
    ["Tạo phiếu điều chuyển kho", "Thủ kho; phiếu Chờ duyệt; loại điều chuyển cùng thủ kho.", "Mở màn lập Phiếu điều chuyển kho."],
    ["Quay lại", "Luôn có.", "Về màn danh sách."],
])

# ------------------------------------------------- PHAN 5
b.h1("PHẦN 5: HỦY PHIẾU")
b.para("Màn Đề nghị xuất kho KHÔNG có chức năng xóa hẳn phiếu; thao tác thu hồi duy nhất là Hủy.")
b.h2("5.1. Điều kiện hủy")
b.para("Chỉ hủy được đề nghị ở trạng thái Đang tạo (nháp — chưa gửi hoặc bị từ chối) do chính mình lập. Khi đã gửi (Chờ duyệt), người lập không hủy được nữa; quyền xử lý chuyển sang Thủ kho (duyệt / từ chối).")
b.h2("5.2. Cách hủy & kết quả")
b.para("Bấm \"Hủy đề nghị\" trên dòng danh sách (hoặc trong menu thao tác), xác nhận. Sau khi hủy, đề nghị chuyển sang trạng thái Đã hủy và được đánh dấu hoàn tất; phiếu yêu cầu xuất hàng gốc cũng được đưa về trạng thái hủy tương ứng. Phiếu đã hủy vẫn được lưu để tra cứu, không bị xóa khỏi hệ thống.")

# ------------------------------------------------- PHAN 6
b.h1("PHẦN 6: IN ẤN & XUẤT EXCEL")
b.table([
    ["Chức năng", "Nội dung"],
    ["In đề nghị", "In mẫu Phiếu đề nghị xuất kho tiêu chuẩn (từ menu thao tác trên mỗi dòng danh sách)."],
    ["In bộ giấy tờ đi đường", "In bộ nhiều mẫu phục vụ vận chuyển: Lệnh điều động và (nếu có kho) Phiếu xuất kho đi đường."],
    ["Xuất Excel danh sách", "Tải file Excel danh sách đề nghị theo bộ lọc hiện tại (nút trên màn danh sách chính). Danh sách quá lớn (≥ 2000 dòng) sẽ được gửi qua email."],
])

# ------------------------------------------------- PHAN 7
b.h1("PHẦN 7: MÀN DÀNH CHO THỦ KHO")
b.para("Ngoài danh sách chung, Thủ kho có màn chuyên biệt (cùng nguồn dữ liệu, khác bộ lọc theo vai trò):")
b.bullet("liệt kê các đề nghị đang Chờ duyệt tại kho mình phụ trách, để Thủ kho tạo phiếu xuất kho / điều chuyển hoặc từ chối.", bold_prefix="Phiếu đề nghị xuất kho chờ duyệt: ")
b.bullet("danh sách các đề nghị gửi tới kho mình phụ trách (ẩn phiếu nháp của người khác).", bold_prefix="Màn Thủ kho: ")
b.para("Màn chờ duyệt của Thủ kho không có nút Xuất Excel; thao tác xử lý (tạo phiếu xuất kho / điều chuyển / từ chối) thực hiện qua chi tiết phiếu như PHẦN 4.")

# ------------------------------------------------- PHAN 8
b.h1("PHẦN 8: CÂU HỎI THƯỜNG GẶP & LƯU Ý")
b.table([
    ["Tình huống", "Giải thích / cách xử lý"],
    ["Không thấy nút Tạo mới trên màn Đề nghị xuất kho", "Đúng thiết kế — đề nghị được lập từ màn Yêu cầu xuất hàng. Mở phiếu yêu cầu đã duyệt rồi bấm lập đề nghị xuất kho."],
    ["Không lập được đề nghị (báo không đủ quyền)", "Cần quyền Kế toán kho và phải cùng công ty với phiếu yêu cầu xuất hàng."],
    ["Danh sách trống dù có nhiều phiếu", "Có thể bạn chưa có quyền xem cấp phù hợp (chỉ thấy phiếu của mình). Liên hệ quản trị để cấp quyền xem theo công ty/phòng ban, hoặc bạn cần là Thủ kho của kho."],
    ["Không thấy nút Sửa / Hủy", "Hai thao tác này chỉ dành cho phiếu Đang tạo (nháp) do chính bạn lập. Khi đã gửi (Chờ duyệt) thì không sửa/hủy được nữa."],
    ["Muốn xóa hẳn phiếu", "Màn này không có chức năng xóa. Với phiếu nháp lập nhầm, hãy dùng Hủy — phiếu chuyển sang Đã hủy."],
    ["Không thấy nút Tạo phiếu xuất kho / điều chuyển", "Cần là Thủ kho của kho xuất và phiếu phải ở trạng thái Chờ duyệt. Loại điều chuyển cùng thủ kho thì dùng \"Tạo phiếu điều chuyển kho\", còn lại dùng \"Tạo phiếu xuất kho\"."],
    ["Không chọn được kho xuất", "Kho xuất bị khóa và lấy tự động theo phiếu yêu cầu; chỉ loại xuất điều chuyển kho chi nhánh mới được chọn kho."],
    ["Không thấy chỗ chọn lô", "Đúng thiết kế — ở đề nghị xuất kho chỉ chọn kho. Việc chọn lô thực hiện ở bước Phiếu xuất kho."],
    ["Bị từ chối (Không duyệt)", "Thủ kho đã trả đề nghị về nháp kèm lý do (xem card Ghi chú duyệt). Kế toán kho sửa lại rồi gửi lại."],
])

# ============================================================ FINISH
finish_macos(b)
print("XONG.")
