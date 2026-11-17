import sys
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
doc.styles["Normal"].font.name = "Times New Roman"
doc.styles["Normal"].font.size = Pt(12)

def h(t, l=1): doc.add_paragraph(t, style="Heading %d" % l)
def para(t):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; p.add_run(t)
def bullet(t): doc.add_paragraph(t, style="List Bullet")
from docx.shared import Cm
def table(rows, widths=None):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Light Grid Accent 1"; t.alignment = 1
    if widths:
        t.autofit = False
        for col, w in zip(t.columns, widths): col.width = Cm(w)
        for r in t.rows:
            for c, w in zip(r.cells, widths): c.width = Cm(w)
    for i, r in enumerate(rows):
        for j, v in enumerate(r): t.cell(i, j).text = v
    doc.add_paragraph()
def center(t, size, bold=True):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(t); r.bold = bold; r.font.size = Pt(size)

for _ in range(6): doc.add_paragraph()
center("MÔ TẢ TIẾN TRÌNH DỰ ÁN TKT", 20)
center("Tiến trình nội bộ — 12 bước theo 2 luồng", 16)
center("Phân hệ Giao việc · Dự án TKT · Cập nhật ngày 17/11/2026", 12, False)
doc.add_page_break()

h("1. Tiến trình nội bộ là gì?")
para("Tiến trình nội bộ cho biết dự án TKT đang ở bước nào trong quy trình làm việc của công ty, từ lúc mới tạo cho tới khi kết thúc. Tiến trình gồm 12 bước, hiện thành nhãn \"Tiến trình nội bộ\" ở màn danh sách và màn chi tiết dự án. Quy định này áp dụng cho dự án con và dự án độc lập; dự án cha giữ cách hiển thị riêng như hiện tại.")
bullet("Người dùng không chọn tay bước này.")
bullet("Hệ thống tự chuyển bước khi người dùng làm một thao tác nghiệp vụ (gửi yêu cầu làm giải pháp, tạo báo giá, chốt báo giá…).")
bullet("Mỗi lần chuyển bước hệ thống đều ghi lại lịch sử: từ bước nào sang bước nào, lúc nào, do ai.")
bullet("Tên bước và màu nhãn do hệ thống quyết định, hiển thị thống nhất ở danh sách, chi tiết, bộ lọc, báo cáo và file Excel.")

h("2. Hai luồng")
para("Luồng của dự án được quyết định ngay khi tạo dự án, bằng ô chọn \"Có giải pháp\".")
table([
 ["Luồng", "Ý nghĩa", "Đường đi"],
 ["Không có giải pháp", "Sale bán hàng hóa trực tiếp, không cần phòng kỹ thuật làm giải pháp", "1 → 2 → 6 → 7 → 8 → 9 → 10 → 12 (bỏ qua bước 3, 4, 5)"],
 ["Có giải pháp", "Có bước gửi yêu cầu làm giải pháp cho phòng giải pháp, hoặc phòng kinh doanh tự làm", "1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 12"],
])
para("Bước 11 (Đóng / Không thực hiện dự án) có thể xảy ra từ bất kỳ bước nào.")

h("3. Bảng 12 bước")
table([
 ["Bước", "Tên bước", "Dự án vào bước này khi…", "Ai thao tác", "Hiện trạng"],
 ["1", "Đang tạo", "Bấm Lưu nháp khi tạo dự án", "Sale", "Đã có"],
 ["2", "Thu thập thông tin dự án", "Bấm Lưu chính thức (hệ thống cấp mã dự án); hoặc tạo meeting cho dự án nháp", "Sale", "Đã có"],
 ["3", "Chờ tiếp nhận làm giải pháp", "Bấm Gửi yêu cầu làm giải pháp", "Sale", "Đã có"],
 ["4", "Đang làm giải pháp", "Phòng giải pháp Tiếp nhận yêu cầu và bắt đầu làm", "Phòng giải pháp / Sale tự làm", "Đã có"],
 ["5", "Trao đổi giải pháp với khách hàng", "Hồ sơ giải pháp được Duyệt nội bộ", "Trưởng phòng giải pháp", "Đã có (đã đổi tên)"],
 ["6", "Lập dự toán", "Một trong 3 việc: bấm Chốt giải pháp (bắt buộc đính kèm file) · tạo Yêu cầu xây dựng giá · tạo Báo giá", "Sale", "Đã có (đã đổi tên, đã bắt buộc file)"],
 ["7", "Thương thảo giá và giải pháp", "Báo giá được Duyệt nội bộ", "Người duyệt báo giá", "Đã có (đã đổi tên)"],
 ["8", "Thương thảo hợp đồng", "Bấm Chốt báo giá cuối cùng (Trúng thầu), kèm file xác nhận của khách hàng", "Sale", "Đã có (đã bắt buộc file)"],
 ["9", "Thực hiện hợp đồng", "Hợp đồng chuyển sang Có hiệu lực", "Hệ thống theo hợp đồng", "Chưa làm"],
 ["10", "Nghiệm thu và thanh lý hợp đồng", "Hợp đồng bước vào nghiệm thu / thanh lý", "Hệ thống theo hợp đồng", "Chưa làm"],
 ["11", "Đóng / Không thực hiện dự án", "(a) Sale bấm Đóng dự án, chọn nguyên nhân và ghi chú. (b) Hợp đồng bị Hủy / Đóng thì hệ thống tự đóng dự án", "Sale / Hệ thống", "(a) Đã có · (b) Chưa làm"],
 ["12", "Kết thúc và lưu trữ", "Dự án hoàn tất, chỉ để tra cứu", "Chưa xác định ai thực hiện", "Chưa làm"],
], [1.2, 3.4, 6.2, 2.8, 2.6])

h("4. Các trường hợp lùi bước")
table([
 ["Đang ở bước", "Lùi về bước", "Khi nào", "Hiện trạng"],
 ["3", "2", "Yêu cầu làm giải pháp bị Từ chối hoặc Hủy", "Đã có"],
 ["3", "2", "Phòng giải pháp bấm Yêu cầu bổ sung thông tin. Chỉ lùi khi dự án đang ở bước 3; nếu giải pháp đã làm dở (bước 4, 5) thì giữ nguyên. Sale gửi lại yêu cầu thì dự án tự lên lại bước 3", "Đã có"],
 ["8", "7", "Hủy chốt báo giá (file xác nhận đã đính kèm lúc chốt cũng bị xóa)", "Đã có"],
], [2.4, 2.4, 9.4, 2.0])

h("5. Sơ đồ tóm tắt")
bullet("Luồng chung đầu: 1 Đang tạo → (Lưu chính thức) → 2 Thu thập thông tin dự án.")
bullet("Nhánh có giải pháp: 2 → (Gửi yêu cầu làm giải pháp) → 3 Chờ tiếp nhận → (Tiếp nhận) → 4 Đang làm giải pháp → (Duyệt hồ sơ giải pháp) → 5 Trao đổi giải pháp với khách hàng. Từ bước 3 có thể lùi về bước 2 nếu yêu cầu bị từ chối, hủy hoặc cần bổ sung thông tin.")
bullet("Nhánh không có giải pháp: từ bước 2 đi thẳng sang bước 6.")
bullet("Hai nhánh gặp nhau ở 6 Lập dự toán (chốt giải pháp có file / tạo yêu cầu xây dựng giá / tạo báo giá) → (Duyệt báo giá) → 7 Thương thảo giá và giải pháp → (Chốt báo giá cuối cùng có file) → 8 Thương thảo hợp đồng. Hủy chốt thì từ 8 về 7.")
bullet("Sau đó: 9 Thực hiện hợp đồng → 10 Nghiệm thu và thanh lý hợp đồng → 12 Kết thúc và lưu trữ.")
bullet("Từ bất kỳ bước nào: Đóng dự án (chọn nguyên nhân) hoặc hợp đồng bị hủy → 11 Đóng / Không thực hiện dự án.")

h("6. Quy tắc bắt buộc")
bullet("Chốt giải pháp: bắt buộc đính kèm ít nhất 1 file. Thiếu file, hệ thống báo \"Vui lòng đính kèm file xác nhận của khách hàng\" và không cho chốt.")
bullet("Chốt báo giá cuối cùng: bắt buộc đính kèm ít nhất 1 file xác nhận của khách hàng, quy tắc tương tự.")
bullet("File đã chốt hiển thị lại ở màn chi tiết dự án: file chốt giải pháp nằm ở khối Giải pháp, file chốt báo giá nằm ở tab Báo giá; có nút xem trước và tải xuống.")
bullet("Không chọn tay được bước: muốn đổi bước phải làm thao tác nghiệp vụ tương ứng.")
bullet("Tên bước 5, 6, 7 theo bảng mới; các tên cũ (Đã duyệt giải pháp, Dự toán, Thương thảo giá) không còn xuất hiện ở danh sách, bộ lọc, báo cáo và file Excel.")

h("7. Lịch sử tiến trình")
para("Mỗi lần dự án chuyển bước, hệ thống ghi lại bước cũ, bước mới, thời điểm và người thực hiện. Các thao tác từ báo giá (duyệt báo giá, chốt, hủy chốt) và từ yêu cầu xây dựng giá cũng được ghi đầy đủ vào lịch sử.")

h("8. Giới hạn hiện tại")
bullet("Bước 9, 10, 12 chưa có thao tác nào đưa dự án vào, vì phụ thuộc trạng thái hợp đồng; dự kiến làm ở task sau.")
bullet("Trường hợp hợp đồng bị Hủy / Đóng thì tự đóng dự án (bước 11b) chưa làm.")
bullet("Bước 12: tài liệu yêu cầu chưa nói rõ ai thực hiện, cần khách hàng chốt.")
bullet("Ở màn chi tiết Giải pháp, nhãn \"Tiến trình nội bộ\" đang hiện trạng thái của giải pháp chứ không phải bước của dự án; chưa quyết định có sửa hay không.")
bullet("Màn Dự án con của dự án cha chưa kiểm thử được bằng dữ liệu thật vì môi trường dev chưa có dự án cha nào có con.")

out = "/Users/manhcuong/Desktop/dns/HRM/.plans/prospective-project-status-12-steps/Mô tả tiến trình dự án TKT.docx"
doc.save(out); print(out)
