# -*- coding: utf-8 -*-
"""Dung HDSD man 'Yeu cau nhap hang' (Phieu Yeu cau nhap hang) - ERP TanPhatDev.

Nguon: khao sat controller Warehouse\\ProductImportRequestsController + model
ProductImportRequest (+ ImportModel) + views warehouse/product_import_requests +
PermissionsTableSeeder. KHONG chen anh (user chot khong can) -> dung o placeholder.

Chay:  /usr/local/bin/python3 gen_hdsd_ycnh_erp.py
Output: ERP/HDSD_luongchinh/HDSD_YeuCauNhapHang.docx
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
OUTPUT = os.path.join(OUT_DIR, "HDSD_YeuCauNhapHang.docx")

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
    cover_title="(Màn hình: Yêu cầu nhập hàng)",
    doc_title="HDSD - Yêu cầu nhập hàng",
)

# ------------------------------------------------- TONG QUAN
b.h1("TỔNG QUAN PHẦN MỀM")

b.h2("1. Thuật ngữ & viết tắt")
b.para("Bảng thuật ngữ giúp người dùng hiểu đúng các bước hướng dẫn.")
b.table([
    ["Thuật ngữ", "Ý nghĩa"],
    ["Phiếu Yêu cầu nhập hàng (YCNH)", "Chứng từ đầu tiên của quy trình nhập hàng, đề nghị nhập hàng vào kho. Đây chính là màn hình tài liệu này hướng dẫn. Mã phiếu có dạng PYCNH-xxxxx."],
    ["Đề nghị nhập kho", "Chứng từ bước 2, do Kế toán kho lập từ YCNH đã duyệt."],
    ["Phiếu nhập kho", "Chứng từ bước 3, kho thực hiện nhập."],
    ["Phiếu nhập hàng", "Chứng từ bước 4 (cuối), ghi nhận & hạch toán nhập hàng."],
    ["Loại yêu cầu (loại nhập)", "Phân loại mục đích nhập hàng: mua ngoài, mua nước ngoài, mượn trả lại, bán trả lại, nhập gửi, nhập khác… Loại quyết định các trường phải nhập và luồng duyệt."],
    ["Nhập thẳng", "Nhập trực tiếp không qua bước đề nghị nhập kho; khi tick, không cần chọn Kho nhập và cho phép Kế toán kho lập Phiếu nhập hàng ngay."],
    ["Phiếu báo hàng về", "Chứng từ báo hàng đã về (theo hợp đồng mua) — nguồn để lập YCNH cho các loại nhập mua."],
    ["Hàng trả lại", "Hàng khách trả (bán trả lại) hoặc trả sau khi mượn — có thể phải duyệt giá nhập trước khi nhập kho."],
    ["Kế toán kho", "Vai trò tiếp nhận YCNH đã duyệt để lập Đề nghị nhập kho / Phiếu nhập hàng, hoặc từ chối phiếu."],
    ["TP duyệt", "Trưởng phòng duyệt YCNH loại bán trả lại / bán (khi mượn) trả lại."],
    ["Ban kiểm soát / BGĐ duyệt giá", "Cấp duyệt GIÁ nhập cho hàng trả lại có quyết toán: Ban kiểm soát duyệt trước, có thể chuyển tiếp lên Ban giám đốc duyệt."],
])

b.h2("2. Lịch sử cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Nội dung", "Người thực hiện"],
    ["1.0", "09/09/2026", "Khởi tạo HDSD màn Yêu cầu nhập hàng (ERP)", "Phòng Phát triển"],
])

b.h2("3. Giới thiệu chung & đường dẫn truy cập")
b.para("Màn hình Yêu cầu nhập hàng dùng để lập và quản lý các phiếu đề nghị nhập hàng vào kho cho nhiều mục đích khác nhau (mua hàng trong nước / nước ngoài, nhận lại hàng mượn, nhận lại hàng bán trả, nhập hàng gửi, nhập khác…). Đây là bước khởi đầu của quy trình nhập hàng gồm 4 chứng từ nối tiếp.")
b.bullet("menu Khởi tạo › Hàng hóa › Nhập - xuất hàng › \"Phiếu Yêu cầu nhập hàng\".", bold_prefix="Đường dẫn: ")
b.bullet("một mục menu riêng \"Phiếu yêu cầu nhập hàng chờ duyệt\" (chỉ hiển thị với người có quyền Kế toán kho) dẫn tới danh sách các phiếu đang chờ xử lý.", bold_prefix="Chờ duyệt: ")
b.para("Vị trí trong quy trình nhập hàng (4 chứng từ nối tiếp):")
b.table([
    ["Bước", "Chứng từ", "Ghi chú"],
    ["1", "Yêu cầu nhập hàng", "Màn hình này — lập, gửi duyệt."],
    ["2", "Đề nghị nhập kho", "Kế toán kho lập từ YCNH đã duyệt."],
    ["3", "Phiếu nhập kho", "Kho thực hiện nhập."],
    ["4", "Phiếu nhập hàng", "Ghi nhận & hạch toán, hoàn tất."],
])

b.h2("4. Quyền & phạm vi (tổng quan)")
b.para("Phạm vi dữ liệu nhìn thấy và các thao tác đều phụ thuộc quyền. Có các nhóm quyền chính:")
b.bullet("4 quyền xem theo cấp (tổng công ty / công ty / phòng ban / bộ phận) quyết định thấy phiếu của phạm vi nào; không có quyền nào thì chỉ thấy phiếu do chính mình tạo.", bold_prefix="Xem danh sách: ")
b.bullet("cần để lập Đề nghị nhập kho / Phiếu nhập hàng, từ chối phiếu, và xem phiếu chờ duyệt.", bold_prefix="Kế toán kho: ")
b.bullet("Trưởng phòng duyệt YCNH bán trả lại / bán (khi mượn) trả lại; Ban kiểm soát và Ban giám đốc duyệt GIÁ nhập cho hàng trả lại có quyết toán.", bold_prefix="Quyền duyệt: ")
b.para("Các thao tác Sửa / Hủy không phụ thuộc quyền mà phụ thuộc quyền sở hữu + trạng thái: chỉ người tạo mới sửa/hủy được phiếu ở trạng thái Đang tạo. Màn này KHÔNG có chức năng xóa hẳn phiếu — chỉ có Hủy. Chi tiết ở PHẦN 2 và PHẦN 5.")

# ------------------------------------------------- PHAN 1
b.h1("PHẦN 1: TRUY CẬP & BỐ CỤC MÀN HÌNH")

b.h2("1.1. Cách truy cập & các màn danh sách")
b.para("Vào menu Khởi tạo › Hàng hóa › Nhập - xuất hàng › \"Phiếu Yêu cầu nhập hàng\". Hệ thống có nhiều màn danh sách dùng chung một nguồn dữ liệu nhưng phục vụ các vai trò khác nhau:")
b.table([
    ["Màn", "Dùng cho", "Nội dung"],
    ["Danh sách (tất cả)", "Người lập / người xem", "Toàn bộ phiếu trong phạm vi quyền của người dùng; có thêm ô lọc Số hợp đồng, có nút Tạo mới và Xuất Excel."],
    ["Chờ duyệt / Kế toán", "Kế toán kho", "Phiếu đã gửi để Kế toán kho lập đề nghị nhập kho / phiếu nhập hàng hoặc từ chối."],
    ["Màn Trưởng phòng duyệt", "Trưởng phòng", "Phiếu bán trả lại / bán (khi mượn) trả lại đang Chờ TP duyệt, thuộc phòng ban mình quản lý."],
    ["Màn Ban kiểm soát / BGĐ duyệt giá", "Ban kiểm soát, Ban giám đốc", "Phiếu hàng trả lại đang chờ duyệt giá nhập (Chờ ban kiểm soát duyệt / Chờ BGĐ duyệt)."],
])
img_placeholder(b, "Ảnh menu Khởi tạo › Hàng hóa › Nhập - xuất hàng › Phiếu Yêu cầu nhập hàng.")

b.h2("1.2. Bố cục màn hình danh sách")
b.bullet("tiêu đề \"Danh sách yêu cầu nhập hàng\".", bold_prefix="Thanh tiêu đề: ")
b.bullet("các ô tìm theo cột (Kho hàng, Tên/mã hàng hóa, Mã phiếu, Số hợp đồng, Loại, Nhà cung cấp, Khách hàng, Trạng thái, Người lập, Người duyệt) và lọc theo khoảng thời gian.", bold_prefix="Khu vực lọc: ")
b.bullet("bảng liệt kê phiếu theo phạm vi quyền, cột Hành động ở cuối mỗi dòng.", bold_prefix="Bảng danh sách: ")
b.bullet("nút Tạo mới và Xuất Excel (chỉ trên màn Danh sách/tất cả), chọn số dòng/trang và chuyển trang.", bold_prefix="Công cụ & phân trang: ")
img_placeholder(b, "Ảnh tổng quan màn danh sách yêu cầu nhập hàng.")

# ------------------------------------------------- PHAN 2
b.h1("PHẦN 2: DANH SÁCH YÊU CẦU NHẬP HÀNG")
img_placeholder(b, "Ảnh màn danh sách với dữ liệu mẫu và cột Hành động.")

b.h2("2.1. Phân quyền & hướng dẫn theo quyền")
b.para("Danh sách hiển thị theo phạm vi quyền của người đăng nhập. Bảng dưới liệt kê đầy đủ các quyền liên quan tới màn. Người dùng thường chỉ có một vài quyền — hãy đối chiếu đúng phần áp dụng cho mình.")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Nút/màn tương ứng"],
    ["Xem yêu cầu nhập hàng theo tổng công ty", "Thấy toàn bộ phiếu của mọi công ty.", "Danh sách"],
    ["Xem yêu cầu nhập hàng theo công ty", "Thấy phiếu trong công ty của mình.", "Danh sách"],
    ["Xem yêu cầu nhập hàng theo phòng ban", "Thấy phiếu trong phòng ban mình quản lý (và phiếu mình tạo).", "Danh sách"],
    ["Xem yêu cầu nhập hàng theo bộ phận", "Thấy phiếu trong bộ phận mình quản lý (và phiếu mình tạo).", "Danh sách"],
    ["Kế toán kho", "Xem phiếu chờ duyệt; lập Đề nghị nhập kho / Phiếu nhập hàng từ phiếu đã gửi; từ chối phiếu.", "Nút \"Tạo đề nghị nhập kho\", \"Tạo phiếu nhập hàng\", \"Không duyệt\"; màn kế toán"],
    ["Trưởng phòng duyệt yêu cầu nhập hàng", "TP duyệt phiếu bán trả lại / bán (khi mượn) trả lại.", "Nút \"TP Duyệt\" / \"Không duyệt\""],
    ["Ban kiểm soát duyệt giá nhập hàng trả lại", "Ban kiểm soát duyệt giá nhập cho hàng trả lại có quyết toán; có thể chuyển tiếp lên BGĐ.", "Nút \"Duyệt\" / \"Chuyển duyệt\" / \"Không duyệt\""],
    ["BGĐ duyệt giá nhập hàng trả lại", "Ban giám đốc duyệt giá nhập cho hàng trả lại.", "Nút \"Duyệt\" / \"Không duyệt\" (BGĐ)"],
])
b.para("Lưu ý phạm vi: nếu không có quyền xem cấp nào, người dùng chỉ thấy phiếu do chính mình tạo. Việc lập phiếu (Tạo mới) thì ai cũng làm được. Khi có một trong các quyền xem cấp, phiếu nháp (Đang tạo) của người khác vẫn bị ẩn — chỉ người lập mới thấy phiếu nháp của mình. Nếu thiếu quyền, các nút tương ứng sẽ không hiển thị; truy cập trực tiếp bằng đường dẫn sẽ báo không có quyền.")

b.h3("Người dùng có quyền \"Xem yêu cầu nhập hàng theo tổng công ty\"")
b.para("Thấy toàn bộ phiếu của mọi công ty. Thực hiện đầy đủ thao tác xem/lọc; sửa/hủy vẫn theo quy tắc sở hữu + trạng thái (PHẦN 5).")

b.h3("Người dùng có quyền \"Xem yêu cầu nhập hàng theo công ty / phòng ban / bộ phận\"")
b.para("Thấy phiếu trong phạm vi công ty / phòng ban / bộ phận tương ứng mà mình phụ trách, cộng thêm phiếu do chính mình tạo. Phòng ban/bộ phận được xác định theo phân công quản lý của nhân viên.")

b.h3("Người dùng là Kế toán kho")
b.para("Thấy các phiếu chờ duyệt. Với phiếu đã ở trạng thái Chờ duyệt: nếu là nhập thường (không nhập thẳng) sẽ có nút \"Tạo đề nghị nhập kho\"; nếu là nhập thẳng sẽ có nút \"Tạo phiếu nhập hàng\". Có thể \"Không duyệt\" để trả phiếu về Đang tạo. Đây là vai trò xử lý bước tiếp của quy trình.")

b.h3("Người dùng là Trưởng phòng (duyệt yêu cầu nhập hàng)")
b.para("Với phiếu bán trả lại / bán (khi mượn) trả lại đang ở trạng thái Chờ TP duyệt thuộc phòng ban mình quản lý, có nút \"TP Duyệt\" và \"Không duyệt\". Xem chi tiết luồng duyệt ở PHẦN 4.")

b.h3("Người dùng là Ban kiểm soát / Ban giám đốc (duyệt giá)")
b.para("Với phiếu hàng trả lại đang chờ duyệt giá: Ban kiểm soát thấy nút \"Duyệt\", \"Chuyển duyệt\" (đẩy lên BGĐ), \"Không duyệt\"; Ban giám đốc thấy nút \"Duyệt\", \"Không duyệt\". Xem chi tiết ở PHẦN 4.")

b.h2("2.2. Tìm kiếm & lọc")
b.para("Các ô lọc theo cột (nhập/chọn ngay trên đầu bảng hoặc thanh lọc):")
b.table([
    ["Tiêu chí", "Cách dùng"],
    ["Kho hàng", "Chọn kho (theo kho người dùng được phép)."],
    ["Tên, mã hàng hóa", "Nhập để lọc phiếu có chứa hàng theo tên hoặc mã."],
    ["Mã phiếu", "Nhập mã phiếu (PYCNH-…)."],
    ["Số hợp đồng", "Nhập số hợp đồng liên quan (chỉ có trên màn Danh sách/tất cả)."],
    ["Loại", "Chọn loại yêu cầu nhập (xem mục 3.1)."],
    ["Nhà cung cấp", "Chọn nhà cung cấp."],
    ["Khách hàng", "Chọn (tìm theo tên) để lọc."],
    ["Trạng thái", "Chọn trạng thái phiếu (xem mục 2.5)."],
    ["Người lập / Người duyệt", "Chọn (tìm theo tên) để lọc."],
    ["Khoảng thời gian", "Lọc theo khoảng ngày lập phiếu."],
])

b.h2("2.3. Các cột trong danh sách")
b.table([
    ["Cột", "Ý nghĩa"],
    ["STT", "Số thứ tự dòng."],
    ["Mã phiếu", "Mã yêu cầu nhập hàng (bấm để mở chi tiết)."],
    ["Loại", "Loại yêu cầu nhập."],
    ["Nhà cung cấp", "Nhà cung cấp của phiếu (mã - tên)."],
    ["Khách hàng", "Khách hàng của phiếu (nếu có; hoặc lấy theo phiếu xuất liên quan)."],
    ["Ngày lập", "Ngày tạo phiếu."],
    ["Trạng thái", "Trạng thái phiếu, hiển thị nhãn màu."],
    ["Người lập", "Người tạo phiếu (mã phòng - tên)."],
    ["Người duyệt", "Người đã duyệt phiếu."],
    ["Ngày nhận", "Thời điểm phiếu được gửi/nhận để xử lý."],
    ["Ngày duyệt", "Thời điểm duyệt."],
    ["Hành động", "Các nút thao tác (xem mục 2.4)."],
])

b.h2("2.4. Thao tác trên từng dòng (cột Hành động)")
b.para("Các nút nằm trong menu thao tác (biểu tượng bánh răng) và hiển thị tùy trạng thái, loại phiếu, quyền và quyền sở hữu:")
b.table([
    ["Nút", "Điều kiện hiển thị", "Kết quả"],
    ["Sửa yêu cầu", "Phiếu Đang tạo do chính bạn lập (trừ loại Nhập hàng mua nước ngoài mới).", "Mở màn sửa phiếu."],
    ["Hủy yêu cầu", "Phiếu Đang tạo do chính bạn lập (trừ các loại điều chuyển và mua nước ngoài mới).", "Hủy phiếu (cần xác nhận); phiếu chuyển sang Đã hủy."],
    ["Tạo đề nghị nhập kho", "Bạn là Kế toán kho; phiếu Chờ duyệt; không nhập thẳng.", "Mở màn lập Đề nghị nhập kho (bước 2)."],
    ["Tạo phiếu nhập hàng", "Bạn là Kế toán kho; phiếu Chờ duyệt; nhập thẳng.", "Mở màn lập Phiếu nhập hàng."],
    ["TP Duyệt yêu cầu", "Bạn có quyền TP duyệt; phiếu Chờ TP duyệt thuộc phòng ban bạn quản lý.", "Mở chi tiết để duyệt."],
    ["In yêu cầu", "Luôn có.", "In phiếu yêu cầu nhập hàng."],
    ["Lịch sử phiếu", "Luôn có.", "Xem lịch sử thay đổi của phiếu."],
])
b.para("Nếu không thấy nút Sửa/Hủy: phiếu đã qua trạng thái Đang tạo, hoặc không phải phiếu của bạn, hoặc thuộc loại không cho sửa/hủy. Không thấy nút duyệt: phiếu chưa ở đúng trạng thái chờ cấp bạn, hoặc bạn chưa có quyền duyệt tương ứng. Các nút Duyệt giá của Ban kiểm soát/BGĐ nằm trong trang chi tiết phiếu (xem PHẦN 4).")

b.h2("2.5. Bảng trạng thái phiếu")
b.table([
    ["Trạng thái", "Ý nghĩa"],
    ["Đang tạo", "Phiếu nháp, chưa gửi duyệt. Chỉ người tạo sửa/hủy được."],
    ["Chờ duyệt", "Đã gửi; chờ Kế toán kho xử lý bước tiếp (hoặc từ chối)."],
    ["Chờ TP duyệt", "Phiếu bán trả lại / bán (khi mượn) trả lại chờ Trưởng phòng duyệt."],
    ["Chờ ban kiểm soát duyệt", "Hàng trả lại có quyết toán, chờ Ban kiểm soát duyệt giá nhập."],
    ["Chờ BGĐ duyệt", "Chờ Ban giám đốc duyệt giá nhập."],
    ["Đang lập đề nghị", "Kế toán kho đã duyệt, đang lập đề nghị nhập kho."],
    ["Đã đề nghị", "Đã lập đề nghị nhập kho từ phiếu."],
    ["Đang nhập kho / Đã nhập kho", "Kho đang / đã nhập xong."],
    ["Đang hạch toán / Đã hạch toán", "Đang / đã ghi nhận hạch toán."],
    ["Đã hủy", "Phiếu đã bị hủy."],
])

# ------------------------------------------------- PHAN 3
b.h1("PHẦN 3: TẠO YÊU CẦU NHẬP HÀNG")
b.para("Trên màn danh sách bấm nút \"Tạo mới\" để mở màn lập yêu cầu nhập hàng. Việc lập phiếu không đòi hỏi quyền đặc biệt; phiếu nháp thuộc về người lập. Đầu form hiển thị Người tạo - Ngày tạo (mặc định là người đăng nhập và ngày hôm nay).")
img_placeholder(b, "Ảnh màn Tạo yêu cầu nhập hàng (form).")

b.h2("3.1. Chọn loại yêu cầu")
b.para("Trường \"Loại yêu cầu\" (bắt buộc) quyết định các trường phía dưới, bảng hàng hóa và luồng duyệt. Các loại có thể chọn khi tạo tay:")
b.table([
    ["Loại yêu cầu", "Mục đích"],
    ["Nhập hàng mua ngoài", "Nhập hàng mua trong nước theo phiếu báo hàng về."],
    ["Nhập hàng mượn trả lại", "Nhận lại hàng đã cho mượn (theo phiếu yêu cầu xuất mượn)."],
    ["Nhập hàng bán trả lại", "Nhận lại hàng khách đã mua trả lại (có thể phải duyệt giá)."],
    ["Nhập hàng bán(khi mượn) trả lại", "Nhận lại hàng bán khi mượn khách trả lại (có thể phải duyệt giá)."],
    ["Nhập hàng mua nước ngoài(mới)", "Nhập hàng mua nước ngoài theo hợp đồng mua mới (có ngoại tệ/tỉ giá, chi phí quốc tế)."],
    ["Nhập hàng gửi", "Nhập hàng gửi của khách hàng."],
    ["Nhập hàng mua trong nước (TỰ DO + HÃNG)", "Nhập theo phiếu báo hàng về tự do + hãng, kèm chi phí hợp đồng."],
    ["Nhập hàng khác", "Các trường hợp còn lại (chọn nhà cung cấp / nhân viên, tự thêm hàng)."],
])
b.para("Lưu ý: các loại nhập điều chuyển (cùng thủ kho, kho nội bộ, kho chi nhánh), nhập ghép, nhập tách, nhập sản xuất theo hợp đồng do hệ thống tự sinh từ nghiệp vụ khác, không tạo tay tại màn này. Khi sửa phiếu, trường Loại yêu cầu bị khóa (không đổi loại sau khi đã tạo).")

b.h2("3.2. Các trường thông tin chung")
b.para("Tùy loại yêu cầu, các trường sau hiển thị (cột \"Hiện khi\" cho biết loại nào áp dụng):")
b.table([
    ["Trường", "Bắt buộc", "Hiện khi / ghi chú"],
    ["Loại yêu cầu", "Có", "Luôn hiện. Khóa khi đang sửa."],
    ["Nhập thẳng", "Không", "Mọi loại. Tick để nhập thẳng (ẩn Kho nhập và phần vận chuyển)."],
    ["Chọn nhà cung cấp", "Không", "Loại Nhập hàng khác."],
    ["Chọn nhân viên", "Không", "Loại Nhập hàng khác."],
    ["Chọn phiếu báo hàng về", "Có (khi hiện)", "Loại Nhập hàng mua ngoài / mua nước ngoài (mới) / mua trong nước (TỰ DO + HÃNG). Khóa khi đang sửa."],
    ["Chọn phiếu yêu cầu xuất bán hàng mượn", "Có (khi hiện)", "Loại Nhập hàng bán(khi mượn) trả lại. Khóa khi đang sửa."],
    ["Chọn phiếu yêu cầu xuất hàng", "Không", "Loại mượn trả lại / bán trả lại / nhập gửi / nhập khác. Khóa khi đang sửa."],
    ["Khách hàng", "Không", "Loại Nhập hàng gửi (mở modal chọn khách hàng)."],
    ["Chọn kho nhập", "Có (khi hiện)", "Mọi loại khi KHÔNG tick Nhập thẳng."],
    ["Vận chuyển", "Có (khi hiện)", "Các loại có giao hàng, khi không nhập thẳng: Tự vận chuyển / Công ty vận chuyển / Khách hàng vận chuyển."],
    ["Số km dự kiến", "Có (khi hiện)", "Chỉ khi chọn \"Công ty vận chuyển\"."],
    ["Ghi chú / File đính kèm", "Không", "Ghi chú tối đa 255 ký tự; đính kèm pdf, ảnh, doc, xls."],
])

b.h2("3.3. Bảng chi tiết hàng hóa & các tab")
b.para("Phần dưới form là bảng hàng hóa, nằm trong tab \"Hàng hóa\". Tùy loại nhập có thể có thêm các tab chi phí: Chi phí NCC, Chi phí quốc tế, Phân bổ chi phí tính thuế (loại mua nước ngoài); Chi phí HĐ (loại mua trong nước tự do + hãng, mua ngoài); Chi phí nội địa. Tab nào có lỗi sẽ hiện cảnh báo màu đỏ.")
b.para("Các cột trong bảng hàng hóa thay đổi theo loại nhập:")
b.table([
    ["Loại nhập", "Cột đặc trưng / cách nhập"],
    ["Nhập mua ngoài / mua nước ngoài", "Tên hàng, Mã, Model, ĐVT, SL, Đơn giá, Thành tiền, VAT %, Tiền VAT; số lượng lấy theo phiếu báo hàng về (chỉ đọc)."],
    ["Nhập mua trong nước (TỰ DO + HÃNG)", "Thêm cột SL về và SL (nhập được) để nhập số lượng thực nhận."],
    ["Nhập hàng bán trả lại / bán(khi mượn) trả lại", "SL xuất, Đã trả, SL trả (nhập), các cột giá bán/giảm giá/VAT; khi có quyết toán còn có Đơn giá mua đề xuất / Thành tiền mua đề xuất."],
    ["Nhập hàng mượn trả lại", "SL mượn, Đã trả, SL trả (nhập), Đơn vị tính (chọn)."],
    ["Nhập hàng gửi / Nhập hàng khác", "Số lượng (nhập), Đơn vị tính (chọn), Giá NCC, Thành tiền; có nút thêm/xóa dòng hàng (chọn hàng qua ô tìm kiếm)."],
])
b.para("Nhập Số lượng cho từng dòng cần nhập. Các bảng chi phí (NCC / quốc tế / nội địa / HĐ) cho phép thêm dòng chi phí kèm giá trị, VAT, nhà cung cấp và file đính kèm.")

b.h2("3.4. Các nút lưu")
b.table([
    ["Nút", "Hành động"],
    ["Lưu", "Lưu phiếu ở trạng thái Đang tạo (nháp)."],
    ["Lưu & Gửi", "Gửi duyệt. Với đa số loại: chuyển Chờ duyệt (sang Kế toán kho). Với bán trả lại / bán (khi mượn) trả lại thường: chuyển Chờ TP duyệt. Với hàng trả lại có quyết toán: chuyển Chờ ban kiểm soát duyệt (duyệt giá)."],
    ["Hủy", "Quay lại danh sách, không lưu."],
])
b.para("Nút \"Lưu & Gửi\" chỉ bật khi phiếu đã hợp lệ: có ít nhất một dòng hàng số lượng lớn hơn 0, và với hàng mượn/bán trả lại thì không còn dòng vượt số lượng được phép trả.")

b.h2("3.5. Quy tắc kiểm tra dữ liệu (validate)")
b.table([
    ["Trường / tình huống", "Yêu cầu"],
    ["Loại yêu cầu", "Bắt buộc, thuộc danh sách loại hợp lệ."],
    ["Danh sách hàng", "Bắt buộc ít nhất 1 dòng; số lượng mỗi dòng từ 0 đến 999.999 (loại Nhập gửi / Nhập khác yêu cầu tối thiểu 1 khi sửa)."],
    ["Kho nhập", "Bắt buộc khi không tick Nhập thẳng."],
    ["Ghi chú / đính kèm", "Ghi chú tối đa 255 ký tự; tệp đúng định dạng cho phép (pdf, png, jpg, doc, docx, xls, xlsx)."],
    ["Nhập mượn trả lại / bán trả lại / nhập gửi", "Bắt buộc chọn phiếu yêu cầu xuất hàng liên quan."],
    ["Nhập bán(khi mượn) trả lại", "Bắt buộc chọn phiếu yêu cầu xuất bán hàng mượn."],
    ["Nhập mua nước ngoài", "Bắt buộc phiếu báo hàng về, tỉ giá (>0), thuế nhập khẩu từng dòng và các chi phí quốc tế."],
    ["Nhập mua ngoài / mua trong nước", "Bắt buộc chọn phiếu báo hàng về tương ứng."],
    ["Nhập hàng gửi", "Bắt buộc chọn khách hàng."],
    ["Vận chuyển bằng công ty", "Bắt buộc nhập Số km dự kiến (phải có bảng giá hoặc công thức vận chuyển hiệu lực)."],
])
b.para("Ngoài ra hệ thống kiểm tra nghiệp vụ: hàng mượn/bán trả lại phải đủ điều kiện trả (chưa trả trên phiếu khác, hợp đồng chưa quyết toán…). Thiếu dữ liệu bắt buộc sẽ báo lỗi ngay tại trường tương ứng và không lưu cho tới khi bổ sung đủ.")

# ------------------------------------------------- PHAN 4
b.h1("PHẦN 4: XEM CHI TIẾT & DUYỆT PHIẾU")

b.h2("4.1. Xem chi tiết")
b.para("Bấm Mã phiếu (hoặc mở chi tiết) để xem phiếu. Trang chi tiết hiển thị đầy đủ thông tin chung, danh sách hàng, số lượng, giá trị, chi phí, trạng thái, người lập, người duyệt và ghi chú duyệt (nếu có). Cuối trang là các nút thao tác theo trạng thái và quyền (mục 4.2–4.5).")

b.h2("4.2. Luồng Kế toán kho (nhập thường & nhập thẳng)")
b.para("Đa số loại nhập sau khi gửi sẽ ở trạng thái Chờ duyệt và chuyển tới Kế toán kho:")
b.bullet("với phiếu nhập thường (không nhập thẳng), Kế toán kho bấm \"Tạo đề nghị nhập kho\" để lập đề nghị nhập kho (bước 2). Phiếu chuyển sang Đang lập đề nghị.", bold_prefix="Tạo đề nghị nhập kho: ")
b.bullet("với phiếu nhập thẳng, Kế toán kho bấm \"Tạo phiếu nhập hàng\" để lập thẳng phiếu nhập hàng.", bold_prefix="Tạo phiếu nhập hàng: ")
b.bullet("Kế toán kho bấm \"Không duyệt\", nhập ghi chú (bắt buộc). Phiếu trả về trạng thái Đang tạo để người lập chỉnh sửa.", bold_prefix="Không duyệt: ")

b.h2("4.3. Luồng Trưởng phòng duyệt (bán trả lại / bán khi mượn trả lại)")
b.para("Phiếu loại bán trả lại / bán (khi mượn) trả lại (không quyết toán) khi gửi sẽ ở trạng thái Chờ TP duyệt. Người có quyền \"Trưởng phòng duyệt yêu cầu nhập hàng\" mở chi tiết:")
b.bullet("bấm \"TP Duyệt\" để duyệt; phiếu chuyển Chờ duyệt (sang Kế toán kho).", bold_prefix="TP Duyệt: ")
b.bullet("bấm \"Không duyệt\" để trả phiếu về Đang tạo.", bold_prefix="Không duyệt: ")
b.para("Việc duyệt bị chặn nếu phòng ban do Trưởng phòng quản lý có nhân viên đang có công nợ/hàng quá hạn (theo cấu hình \"Duyệt yêu cầu nhập hàng\"). Quản trị hệ thống không bị chặn.")

b.h2("4.4. Luồng duyệt GIÁ hàng trả lại: Ban kiểm soát → Ban giám đốc")
b.para("Phiếu hàng trả lại có quyết toán khi gửi sẽ ở trạng thái Chờ ban kiểm soát duyệt (duyệt GIÁ nhập). Luồng:")
b.bullet("mở chi tiết, nhập giá nhập duyệt cho từng dòng rồi bấm \"Duyệt\" (mở hộp ghi chú, xác nhận) — phiếu chuyển Chờ duyệt (sang Kế toán kho). Hoặc bấm \"Chuyển duyệt\" để đẩy lên Ban giám đốc (phiếu chuyển Chờ BGĐ duyệt). Hoặc bấm \"Không duyệt\" (bắt buộc ghi chú) để trả về Đang tạo.", bold_prefix="Ban kiểm soát: ")
b.bullet("với phiếu Chờ BGĐ duyệt, bấm \"Duyệt\" (xác nhận giá) để chuyển Chờ duyệt sang Kế toán kho; hoặc \"Không duyệt\" (bắt buộc ghi chú) để trả về Đang tạo.", bold_prefix="Ban giám đốc: ")
b.para("Việc chuyển từ Ban kiểm soát lên Ban giám đốc là thao tác thủ công (nút \"Chuyển duyệt\"), không tự động theo ngưỡng tiền. Các thao tác duyệt cũng chịu ràng buộc chặn theo cấu hình \"Duyệt yêu cầu nhập hàng\" như mục 4.3.")

b.h2("4.5. Bảng tổng hợp nút thao tác trên trang chi tiết")
b.table([
    ["Nút", "Ai thấy / điều kiện", "Kết quả"],
    ["Tạo đề nghị nhập kho", "Kế toán kho; phiếu Chờ duyệt; không nhập thẳng.", "Mở màn lập Đề nghị nhập kho."],
    ["Tạo phiếu nhập hàng", "Kế toán kho; phiếu Chờ duyệt; nhập thẳng.", "Mở màn lập Phiếu nhập hàng."],
    ["Không duyệt (Kế toán kho)", "Kế toán kho được từ chối phiếu.", "Nhập ghi chú; phiếu về Đang tạo."],
    ["TP Duyệt / Không duyệt", "Trưởng phòng; phiếu Chờ TP duyệt.", "Duyệt sang Chờ duyệt / trả về Đang tạo."],
    ["Duyệt / Chuyển duyệt / Không duyệt", "Ban kiểm soát; phiếu Chờ ban kiểm soát duyệt.", "Duyệt giá sang Chờ duyệt / đẩy lên BGĐ / trả về Đang tạo."],
    ["Duyệt / Không duyệt (BGĐ)", "Ban giám đốc; phiếu Chờ BGĐ duyệt.", "Duyệt giá sang Chờ duyệt / trả về Đang tạo."],
    ["Sửa", "Người lập; phiếu Đang tạo.", "Mở màn sửa phiếu."],
    ["Quay lại", "Luôn có.", "Về màn danh sách."],
])

# ------------------------------------------------- PHAN 5
b.h1("PHẦN 5: HỦY PHIẾU")
b.para("Màn Yêu cầu nhập hàng KHÔNG có chức năng xóa hẳn phiếu; thao tác thu hồi duy nhất là Hủy.")
b.h2("5.1. Điều kiện hủy")
b.para("Chỉ hủy được phiếu ở trạng thái Đang tạo do chính mình lập, và loại phiếu không thuộc các loại điều chuyển (cùng thủ kho, kho nội bộ, kho chi nhánh) hay Nhập hàng mua nước ngoài (mới).")
b.h2("5.2. Cách hủy & kết quả")
b.para("Bấm \"Hủy yêu cầu\" trên dòng danh sách (hoặc trong menu thao tác), xác nhận. Sau khi hủy, phiếu chuyển sang trạng thái Đã hủy và được đánh dấu hoàn tất (không đi tiếp quy trình). Phiếu đã hủy vẫn được lưu để tra cứu, không bị xóa khỏi hệ thống.")

# ------------------------------------------------- PHAN 6
b.h1("PHẦN 6: IN ẤN, XUẤT EXCEL & LỊCH SỬ")
b.table([
    ["Chức năng", "Nội dung"],
    ["In yêu cầu", "In mẫu Phiếu yêu cầu nhập hàng (từ menu thao tác trên mỗi dòng danh sách)."],
    ["Xuất Excel danh sách", "Tải file Excel danh sách phiếu theo bộ lọc hiện tại (nút ở màn Danh sách/tất cả). Danh sách quá lớn sẽ được gửi qua email."],
    ["Lịch sử phiếu", "Xem timeline các phiên thay đổi của phiếu (thời gian gửi, duyệt, ghi chú duyệt, hoàn thành, trả lại…)."],
])

# ------------------------------------------------- PHAN 7
b.h1("PHẦN 7: MÀN DÀNH CHO NGƯỜI DUYỆT & KẾ TOÁN")
b.para("Ngoài danh sách chung, hệ thống có các màn chuyên biệt (cùng nguồn dữ liệu, khác bộ lọc theo vai trò):")
b.bullet("dành cho Kế toán kho tiếp nhận phiếu đã gửi để lập đề nghị nhập kho / phiếu nhập hàng hoặc từ chối.", bold_prefix="Màn kế toán / chờ duyệt: ")
b.bullet("dành cho Trưởng phòng duyệt phiếu bán trả lại / bán (khi mượn) trả lại đang Chờ TP duyệt thuộc phòng ban mình quản lý.", bold_prefix="Màn Trưởng phòng duyệt: ")
b.bullet("dành cho Ban kiểm soát và Ban giám đốc duyệt GIÁ nhập cho hàng trả lại (Chờ ban kiểm soát duyệt / Chờ BGĐ duyệt).", bold_prefix="Màn duyệt giá: ")
b.para("Các màn này không có nút Tạo mới và Xuất Excel; chỉ có ô lọc nhanh (khoảng thời gian, tên/mã hàng, kho) và bảng phiếu cần xử lý.")

# ------------------------------------------------- PHAN 8
b.h1("PHẦN 8: CÂU HỎI THƯỜNG GẶP & LƯU Ý")
b.table([
    ["Tình huống", "Giải thích / cách xử lý"],
    ["Danh sách trống dù có nhiều phiếu", "Có thể bạn chưa có quyền xem cấp phù hợp (chỉ thấy phiếu của mình). Liên hệ quản trị để cấp quyền xem theo công ty/phòng ban/bộ phận."],
    ["Không thấy nút Sửa / Hủy", "Hai thao tác này chỉ dành cho phiếu Đang tạo do chính bạn lập; một số loại (điều chuyển, mua nước ngoài mới) không cho hủy/sửa."],
    ["Muốn xóa hẳn phiếu", "Màn này không có chức năng xóa. Với phiếu nháp lập nhầm, hãy dùng Hủy — phiếu chuyển sang Đã hủy và không đi tiếp quy trình."],
    ["Không thấy nút Tạo đề nghị nhập kho / Tạo phiếu nhập hàng", "Cần quyền Kế toán kho và phiếu phải ở trạng thái Chờ duyệt; nhập thẳng thì dùng \"Tạo phiếu nhập hàng\", ngược lại dùng \"Tạo đề nghị nhập kho\"."],
    ["Phiếu bị chuyển sang Chờ TP duyệt / Chờ ban kiểm soát duyệt", "Do loại phiếu là bán trả lại / bán (khi mượn) trả lại: loại thường qua Trưởng phòng; loại có quyết toán qua Ban kiểm soát → BGĐ duyệt giá trước khi tới Kế toán kho."],
    ["Duyệt bị chặn", "Cấu hình \"Duyệt yêu cầu nhập hàng\" chặn cấp quản lý duyệt khi phòng/bộ phận mình quản lý có nhân viên quá hạn. Xử lý phần quá hạn trước, hoặc nhờ quản trị hệ thống."],
    ["Chọn nhầm loại nhập", "Không đổi được loại sau khi tạo. Nếu chọn nhầm, hãy Hủy phiếu nháp và lập lại với loại đúng."],
    ["Tick Nhập thẳng khác gì không tick?", "Nhập thẳng bỏ qua bước đề nghị nhập kho: không cần chọn Kho nhập và cho phép Kế toán kho tạo Phiếu nhập hàng ngay khi phiếu Chờ duyệt."],
])

# ============================================================ FINISH
finish_macos(b)
print("XONG.")
