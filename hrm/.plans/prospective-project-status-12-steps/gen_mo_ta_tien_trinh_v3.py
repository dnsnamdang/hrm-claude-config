import sys
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
doc.styles["Normal"].font.name = "Times New Roman"
doc.styles["Normal"].font.size = Pt(12)

def h(t, l=1): doc.add_paragraph(t, style="Heading %d" % l)
def para(t):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; p.add_run(t)
def bullet(t): doc.add_paragraph(t, style="List Bullet")
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
center("MÔ TẢ NGHIỆP VỤ", 20)
center("TIẾN TRÌNH DỰ ÁN TKT", 16)
center("Dự án con / dự án độc lập (12 bước) và Dự án cha (8 bước)", 13, False)
center("Phân hệ CSKH trước bán · Đã chạy thử trên hệ thống ngày 17/11/2026", 12, False)
doc.add_page_break()

# 1
h("1. TÀI LIỆU NÀY DÀNH CHO AI")
para("Tài liệu mô tả vì sao dự án tiền khả thi (gọi tắt là dự án TKT) có \"Tiến trình\", dự án đi qua những bước nào, ai làm dự án chuyển bước, khi nào được lùi, ai nhận thông báo và những quy tắc bắt buộc. Nội dung bám theo cách hệ thống đang chạy thực tế, không phải theo dự kiến.")
bullet("Nhân viên kinh doanh (NV KD) phụ trách dự án: biết mình phải làm gì để dự án sang bước kế tiếp.")
bullet("Trưởng phòng, Ban giám đốc: biết mình duyệt những gì và duyệt xong thì dự án đi đâu.")
bullet("Người nghiệm thu, QA: có bảng đối chiếu bước nào do thao tác nào tạo ra để kiểm thử.")
bullet("Quản lý: biết phần nào đã có, phần nào chưa làm (chương 12).")

# 2
h("2. CHỨC NĂNG NÀY DÙNG ĐỂ LÀM GÌ")
h("2.1 Mục đích", 2)
para("Tiến trình nội bộ cho biết dự án TKT đang ở đâu trong quy trình làm việc của công ty, từ lúc mới tạo cho đến khi kết thúc. Người dùng không chọn tay bước này. Hệ thống tự chuyển bước khi người dùng làm một việc nghiệp vụ như gửi yêu cầu làm giải pháp, duyệt giải pháp, tạo báo giá, duyệt báo giá, chốt báo giá hoặc đóng dự án.")
h("2.2 Có hai bộ tiến trình", 2)
table([
 ["Loại dự án", "Số bước", "Đặc điểm"],
 ["Dự án con và dự án độc lập", "12 bước", "Có làm giải pháp kỹ thuật, báo giá, thương thảo, hợp đồng. Nội dung chính của tài liệu."],
 ["Dự án cha", "8 bước (1, 2, 7, 8, 9, 10, 11, 12)", "Là gói thầu tổng gom nhiều dự án con. Không làm giải pháp kỹ thuật nên bỏ các bước 3 đến 6. Có tên bước riêng, xem chương 4.2."],
], [4.0, 3.6, 8.4])
para("Lưu ý quan trọng: một số số thứ tự bước trùng nhau giữa hai bộ nhưng khác tên. Ví dụ bước 7 của dự án con là \"Thương thảo giá và giải pháp\", còn bước 7 của dự án cha là \"Trình duyệt hợp đồng\". Mọi nơi hiển thị (danh sách, chi tiết, bộ lọc, báo cáo, file Excel) đã đọc theo đúng loại dự án.")
h("2.3 Giá trị mang lại", 2)
bullet("Mọi người nhìn một nhãn là biết dự án đang ở khâu nào, không cần hỏi NV KD.")
bullet("Lịch sử chuyển bước giúp truy lại dự án nằm ở khâu nào bao lâu, do ai thao tác.")
bullet("Hệ thống dựa vào bước và giai đoạn dự án để nhắc hạn và tự đóng dự án bị bỏ quên (chương 5.9).")

# 3
h("3. NHỮNG AI THAM GIA")
table([
 ["Vai trò", "Làm gì với tiến trình"],
 ["NV KD phụ trách dự án", "Người chính. Tạo dự án, gửi yêu cầu làm giải pháp, chốt giải pháp, lập báo giá, chốt báo giá cuối cùng, đóng dự án, đề xuất gia hạn. Chỉ NV KD phụ trách mới được đóng dự án, chốt giải pháp và gửi đề xuất gia hạn."],
 ["Người lập dự án", "Người duy nhất được sửa thông tin dự án. Dự án còn ở bước Đang tạo thì chỉ người lập mới nhìn thấy."],
 ["Phòng giải pháp (người tiếp nhận, PM, Trưởng phòng giải pháp)", "Tiếp nhận yêu cầu làm giải pháp, làm giải pháp, duyệt hồ sơ giải pháp."],
 ["Người lập báo giá", "Lập báo giá và gửi duyệt."],
 ["Trưởng phòng", "Duyệt báo giá cấp 2 và cấp 3 (quyền \"Trưởng phòng duyệt giá Bom giải pháp\"); duyệt đề xuất gia hạn ngắn ngày (quyền \"Trưởng phòng duyệt gia hạn dự án TKT\")."],
 ["Ban giám đốc", "Duyệt báo giá cấp 3 sau Trưởng phòng (quyền \"Ban giám đốc duyệt giá Bom giải pháp\"); duyệt đề xuất gia hạn vượt ngưỡng (quyền \"Ban giám đốc duyệt gia hạn dự án TKT\")."],
 ["NV KD hỗ trợ", "Chỉ xem dự án mình được gán hỗ trợ, không sửa, không đóng."],
 ["Hệ thống (chạy tự động hằng ngày)", "Nhắc hạn và tự đóng dự án quá thời gian thực hiện."],
 ["Khách hàng", "Không thao tác trên hệ thống. Chỉ có file xác nhận của khách hàng được đính kèm khi chốt giải pháp và chốt báo giá."],
], [5.0, 11.0])

# 4
h("4. VÒNG ĐỜI CỦA DỰ ÁN (CÁC BƯỚC TIẾN TRÌNH)")
h("4.1 Dự án con và dự án độc lập — 12 bước", 2)
table([
 ["Bước", "Tên bước", "Dự án vào bước này khi", "Ai làm dự án chuyển sang bước"],
 ["1", "Đang tạo", "Bấm Lưu nháp lúc tạo dự án", "NV KD lập dự án"],
 ["2", "Thu thập thông tin dự án", "Bấm Lưu chính thức (hệ thống cấp mã dự án); hoặc lưu phiếu thu thập thông tin của dự án nháp qua màn Meeting; hoặc quay về từ bước 3 trở lên khi yêu cầu làm giải pháp bị từ chối hoặc hủy (từ bước 3 còn khi cần bổ sung) — chương 5.3", "NV KD; hoặc hệ thống khi yêu cầu bị từ chối / hủy / bổ sung"],
 ["3", "Chờ tiếp nhận làm giải pháp", "Gửi yêu cầu làm giải pháp (trạng thái Chờ tiếp nhận). Việc phòng giải pháp bấm Tiếp nhận KHÔNG đổi bước, dự án vẫn ở bước 3", "NV KD"],
 ["4", "Đang làm giải pháp", "Giải pháp được tạo và gửi đi: ở trạng thái Chờ PM duyệt, Chờ Leader duyệt, Đang triển khai hoặc Chờ duyệt giải pháp. Dự án Tự triển khai chỉ vào bước này khi giải pháp Đang triển khai", "Phòng giải pháp (hoặc NV KD với dự án tự triển khai) khi tạo và gửi giải pháp"],
 ["5", "Trao đổi giải pháp với khách hàng", "Giải pháp chuyển sang trạng thái Đã duyệt giải pháp", "Người duyệt giải pháp"],
 ["6", "Lập dự toán", "Một trong 3 việc, việc nào làm trước thì vào bước này: chốt giải pháp (có file); tạo yêu cầu xây dựng giá; tạo báo giá", "NV KD"],
 ["7", "Thương thảo giá và giải pháp", "Báo giá được duyệt nội bộ (tự duyệt, hoặc Trưởng phòng duyệt, hoặc Trưởng phòng và Ban giám đốc duyệt)", "NV KD (tự duyệt) / Trưởng phòng / Ban giám đốc"],
 ["8", "Thương thảo hợp đồng", "Chốt báo giá cuối cùng (Trúng thầu), kèm file xác nhận của khách hàng", "NV KD"],
 ["9", "Thực hiện hợp đồng", "Hợp đồng có hiệu lực", "Chưa có thao tác nào đưa dự án vào bước này (chương 12)"],
 ["10", "Nghiệm thu và thanh lý hợp đồng", "Hợp đồng vào nghiệm thu, thanh lý", "Chưa có thao tác nào đưa dự án vào bước này (chương 12)"],
 ["11", "Đóng/Không thực hiện dự án", "NV KD bấm Đóng dự án (chọn nguyên nhân); hoặc hệ thống tự đóng khi quá hạn; hoặc đóng theo dự án cha", "NV KD / Hệ thống / đóng dự án cha"],
 ["12", "Kết thúc và lưu trữ", "Dự án hoàn tất, chỉ để tra cứu", "Chưa có thao tác nào đưa dự án vào bước này (chương 12)"],
], [1.1, 3.6, 7.3, 4.0])

h("4.2 Dự án cha — 8 bước", 2)
table([
 ["Bước", "Tên bước", "Dự án cha vào bước này khi", "Ai làm dự án chuyển sang bước"],
 ["1", "Đang tạo", "Bấm Lưu nháp lúc tạo dự án cha", "NV KD lập dự án"],
 ["2", "Đang thực hiện", "Bấm Lưu chính thức dự án cha (hệ thống cấp mã dự án cha dạng \"phòng.năm.DAC…\")", "NV KD"],
 ["7", "Trình duyệt hợp đồng", "Hợp đồng được lập từ báo giá tổng của dự án cha (báo giá tổng chuyển sang \"Đã tạo hợp đồng\")", "Hệ thống, khi hợp đồng được lập"],
 ["8", "Thương thảo hợp đồng", "Dự kiến theo bảng bước", "Chưa có thao tác nào đưa dự án vào bước này"],
 ["9", "HĐ đủ điều kiện thực hiện", "Dự kiến theo bảng bước", "Chưa có thao tác nào đưa dự án vào bước này"],
 ["10", "Nghiệm thu & Thanh lý", "Dự kiến theo bảng bước", "Chưa có thao tác nào đưa dự án vào bước này"],
 ["11", "Đóng/Không thực hiện dự án", "NV KD bấm Đóng dự án (chọn nguyên nhân); các dự án con chưa đóng bị đóng theo", "NV KD phụ trách dự án cha"],
 ["12", "Kết thúc & lưu trữ", "Dự án hoàn tất, chỉ để tra cứu", "Chưa có thao tác nào đưa dự án vào bước này"],
], [1.1, 3.6, 7.3, 4.0])
para("Dự án cha còn ở bước Đang tạo (mới lưu nháp) thì không gán thêm được dự án con, vì con kế thừa khách hàng của cha mà cha nháp có thể chưa khai đủ. Dự án cha đã Đóng hoặc đã Kết thúc & lưu trữ cũng không được chọn làm cha nữa.")

# 5
h("5. LUỒNG HOẠT ĐỘNG CHI TIẾT")
h("5.1 Tạo dự án (bước 1 và 2)", 2)
para("NV KD tạo dự án. Bấm Lưu nháp thì dự án ở bước 1, chỉ người lập thấy. Bấm Lưu chính thức thì dự án sang bước 2 và được cấp mã. Dự án con hoặc dự án độc lập chọn \"Cách triển khai dự án\" và \"Có cần làm giải pháp\". Hai lựa chọn này quyết định dự án đi theo nhánh nào ở bước kế tiếp, và bị khóa không đổi được từ khi dự án rời bước 1 và 2.")
para("Quy tắc quan trọng: màn Sửa dự án không bao giờ làm dự án lùi bước. Từ bước 2 trở đi, bước chỉ thay đổi do các thao tác nghiệp vụ nêu dưới đây, nên sửa một ô ghi chú không kéo dự án về bước cũ.")
h("5.2 Rẽ nhánh sau bước 2", 2)
table([
 ["Tình huống của dự án", "Diễn ra thế nào", "Kết quả"],
 ["Không cần làm giải pháp", "NV KD lập yêu cầu xây dựng giá hoặc báo giá ngay, không qua phòng giải pháp", "Từ bước 2 sang thẳng bước 6, bỏ qua bước 3, 4, 5"],
 ["Cần làm giải pháp, cách triển khai là Triển khai theo phòng hoặc Liên phòng ban", "NV KD gửi Yêu cầu làm giải pháp cho phòng giải pháp", "Bước 3 Chờ tiếp nhận. Phòng giải pháp bấm Tiếp nhận: dự án vẫn ở bước 3. Khi giải pháp được tạo và gửi đi thì sang bước 4; giải pháp được duyệt thì sang bước 5"],
 ["Cần làm giải pháp, cách triển khai là Tự triển khai", "Không gửi yêu cầu. NV KD tạo giải pháp ngay khi dự án đang ở bước 2 và phiếu thu thập thông tin đã nhập đủ các trường bắt buộc", "Chỉ khi giải pháp ở trạng thái Đang triển khai mới sang bước 4 (các trạng thái chờ duyệt không đổi bước); giải pháp Đã duyệt thì bước 5"],
], [4.6, 6.4, 5.0])
para("Dự án Tự triển khai và không cần làm giải pháp không có các tab Yêu cầu, Giải pháp, Vấn đề giải pháp, Files, Hồ sơ; vẫn có tab Nhiệm vụ. Mỗi dự án chỉ có một giải pháp.")
h("5.3 Yêu cầu làm giải pháp bị từ chối, hủy hoặc cần bổ sung (lùi về bước 2)", 2)
table([
 ["Sự việc", "Dự án lùi khi nào", "Sau đó"],
 ["Yêu cầu làm giải pháp bị Từ chối", "Dự án đang ở bất kỳ bước nào trên bước 2", "Về bước 2"],
 ["Yêu cầu làm giải pháp bị Hủy", "Dự án đang ở bất kỳ bước nào trên bước 2", "Về bước 2; đồng thời mở lại quyền sửa dự án"],
 ["Phòng giải pháp bấm Yêu cầu bổ sung thông tin", "Chỉ khi dự án đang ở bước 3. Nếu giải pháp đã làm dở (bước 4, 5) thì giữ nguyên", "Về bước 2; NV KD bổ sung rồi gửi lại thì dự án tự lên lại bước 3"],
], [5.0, 6.0, 5.0])
h("5.4 Chốt giải pháp (sang bước 6)", 2)
para("Khi hồ sơ giải pháp đã được duyệt (hoặc đã hết hiệu lực), NV KD phụ trách bấm Chốt giải pháp, chọn hồ sơ cần chốt, ghi chú và bắt buộc đính kèm ít nhất một file xác nhận của khách hàng. Hệ thống chốt hồ sơ, đánh dấu yêu cầu làm giải pháp là \"Đã làm GP\", đưa giải pháp sang \"Chốt giải pháp\" và đưa dự án sang bước 6 Lập dự toán. Chỉ tiến, không lùi: dự án đã ở bước 6 trở lên thì giữ nguyên. Chốt giải pháp không đưa dự án thẳng sang bước 8.")
h("5.5 Lập dự toán và duyệt báo giá (bước 6 và 7)", 2)
para("Dự án sang bước 6 khi có bất kỳ việc nào trong ba việc: chốt giải pháp, tạo yêu cầu xây dựng giá, tạo báo giá. Chỉ tiến lên, dự án đã ở bước cao hơn thì không bị kéo xuống. Báo giá gửi duyệt thì cấp duyệt do hệ thống tính theo quy chế giá trị đơn hàng và tỷ suất lợi nhuận:")
table([
 ["Cấp duyệt", "Ai duyệt", "Kết quả"],
 ["Cấp 1 (tự duyệt)", "NV KD tự bấm duyệt. Chỉ áp dụng cho báo giá \"sạch\": chỉ hàng hóa và dịch vụ có trong danh mục, mọi đơn giá bán lớn hơn 1.000 đồng, không có giảm giá", "Báo giá Đã duyệt; dự án sang bước 7"],
 ["Cấp 2", "Trưởng phòng của phòng ban lập báo giá", "Báo giá Đã duyệt; dự án sang bước 7"],
 ["Cấp 3", "Trưởng phòng duyệt trước, sau đó Ban giám đốc của công ty duyệt", "Trưởng phòng duyệt thì báo giá chuyển chờ Ban giám đốc, dự án chưa đổi bước; Ban giám đốc duyệt xong dự án sang bước 7"],
 ["Từ chối ở bất kỳ cấp nào", "Người duyệt bắt buộc nhập lý do", "Báo giá quay về Đang tạo để sửa; bước của dự án không đổi"],
], [3.2, 7.6, 5.2])
para("Dự án sang bước 7 thì hệ thống tính lại ngay hạn đóng tự động của dự án, vì mốc hạn tính từ ngày duyệt báo giá gần nhất (chương 5.9).")
h("5.6 Chốt và hủy chốt báo giá (bước 8 và lùi về 7)", 2)
table([
 ["Hướng xử lý", "Diễn ra thế nào", "Kết quả"],
 ["Chốt báo giá cuối cùng", "NV KD phụ trách bấm Chốt trên báo giá đã duyệt, bắt buộc đính kèm ít nhất một file xác nhận của khách hàng. Mỗi dự án chỉ được một báo giá Trúng thầu; đã có thì phải hủy chốt trước", "Báo giá thành Trúng thầu; dự án sang bước 8 (chỉ tiến, không lùi)"],
 ["Hủy chốt báo giá", "NV KD nhập lý do hủy chốt", "Báo giá về Đã duyệt; file xác nhận đã đính kèm lúc chốt bị xóa; dự án lùi về bước 7 nhưng CHỈ khi dự án đang đúng ở bước 8"],
], [3.6, 7.2, 5.2])
h("5.7 Đóng dự án (bước 11)", 2)
para("NV KD phụ trách bấm Đóng dự án, chọn nguyên nhân thất bại từ danh mục và có thể ghi chú. Dự án đã đóng thì không đóng lại được. Khi đóng, hệ thống đóng theo luôn mọi việc đang dở của dự án:")
bullet("Các giải pháp và mô-đun giải pháp chưa đóng chuyển sang Đóng.")
bullet("Các yêu cầu làm giải pháp chưa kết thúc chuyển sang Đóng (không đụng yêu cầu đã Từ chối hoặc Đã làm GP).")
bullet("Các yêu cầu xây dựng giá đang tạo, chờ hoặc đang xây dựng giá chuyển sang Đóng (yêu cầu đã có báo giá giữ nguyên).")
bullet("Mọi báo giá chưa đóng chuyển sang Đóng và ghi vào lịch sử báo giá kèm lý do.")
para("Dự án đã đóng thì mọi nút thao tác đổi dữ liệu (Sửa, Xóa) bị ẩn; chỉ còn xem.")
h("5.8 Dự án cha", 2)
bullet("Lưu chính thức dự án cha: sang bước 2 Đang thực hiện, được cấp mã riêng.")
bullet("Dự án cha chỉ có các tab Thông tin chung, Dự án con, Báo giá (báo giá gom từ dự án con và báo giá tổng), Meetings. Không có tab giải pháp.")
bullet("Báo giá tổng gom các báo giá đã duyệt của các dự án con, chỉ qua một cấp duyệt. Duyệt báo giá tổng KHÔNG làm dự án cha đổi bước.")
bullet("Khi hợp đồng được lập từ báo giá tổng: báo giá tổng chuyển \"Đã tạo hợp đồng\", các báo giá con nguồn bị khóa không lập hợp đồng nhánh nữa, dự án cha sang bước 7 Trình duyệt hợp đồng.")
bullet("Từ bước 7 trở đi khóa cứng tổng ngân sách dự kiến của dự án cha, vì hợp đồng đã lập theo con số này.")
bullet("Dự án cha đã có con thì khóa Khách hàng, vì các con kế thừa khách hàng từ cha.")
bullet("Đóng dự án cha: chỉ NV KD phụ trách. Trên giao diện nút Đóng dự án chỉ hiện khi dự án cha đang ở bước Đang thực hiện. Khi đóng, các báo giá tổng chuyển Đóng và TỪNG dự án con chưa đóng được đóng theo đúng như bấm Đóng dự án trên con (kể cả giải pháp, yêu cầu, báo giá của con). Một con lỗi không chặn các con còn lại.")
h("5.9 Hạn đóng tự động, nhắc hạn và gia hạn", 2)
para("Mỗi dự án chưa đóng có một \"hạn đóng tự động\" do hệ thống tính. Dự án có hạn đóng thì hiện ở màn danh sách và chi tiết.")
table([
 ["Tình huống", "Hạn đóng tính thế nào"],
 ["Dự án chưa có báo giá nào được duyệt", "Ngày tạo dự án cộng số tháng cấu hình chung (mặc định 3 tháng); số tháng này cấu hình theo công ty"],
 ["Dự án đã có báo giá được duyệt", "Ngày duyệt của báo giá duyệt gần nhất cộng số tháng cấu hình theo Giai đoạn dự án đang đứng"],
 ["Giai đoạn dự án không cấu hình số tháng", "Dự án KHÔNG bao giờ bị tự đóng"],
 ["Có đề xuất gia hạn đã duyệt", "Cộng thêm tổng số ngày đã được duyệt gia hạn"],
], [6.0, 10.0])
para("Hệ thống chạy tự động lúc 01:30 mỗi ngày: tính lại hạn đóng cho mọi dự án chưa đóng, nhắc NV KD trước hạn một lần theo mỗi mốc (mặc định còn từ 7 ngày trở xuống), và tự đóng dự án khi quá hạn cộng thêm số ngày ân hạn cấu hình (mặc định 0 ngày). Dự án tự đóng được đóng đúng như người dùng bấm Đóng dự án (đóng theo giải pháp, yêu cầu, báo giá), lý do ghi nguyên văn \"Hệ thống tự đóng do quá thời gian thực hiện\".")
para("Gia hạn: NV KD phụ trách gửi đề xuất gia hạn kèm số ngày và lý do. Nút Gia hạn chỉ hiện khi dự án chưa đóng, không ở bước 9, 10 hoặc 11, chưa quá hạn đóng và chưa có đề xuất nào đang chờ duyệt.")
table([
 ["Số ngày xin gia hạn", "Ai duyệt", "Kết quả"],
 ["Không vượt ngưỡng (mặc định 30 ngày)", "Trưởng phòng của phòng ban NV KD", "Duyệt xong hạn đóng lùi ra đúng số ngày, hệ thống nhắc lại theo mốc mới"],
 ["Vượt ngưỡng", "Trưởng phòng duyệt trước, rồi Ban giám đốc của công ty", "Trưởng phòng duyệt thì chuyển sang chờ Ban giám đốc, chưa cộng ngày; Ban giám đốc duyệt thì cộng ngày"],
 ["Từ chối ở bất kỳ cấp nào", "Người duyệt nhập lý do", "Đề xuất bị từ chối, hạn đóng giữ nguyên"],
], [4.6, 5.6, 5.8])
para("Gia hạn chỉ có nghĩa là lùi thời điểm hệ thống tự đóng dự án, không sửa ngày kết thúc dự án do sale tự nhập.")
h("5.10 Lịch sử tiến trình", 2)
para("Mỗi lần dự án chuyển bước, hệ thống ghi lại bước cũ, bước mới, thời điểm và người thực hiện. Mọi đường chuyển bước (chuyển từ báo giá, từ yêu cầu xây dựng giá, từ giải pháp, từ đóng dự án) đều đi qua cùng một cơ chế nên đều có ghi lịch sử.")

# 6
h("6. THÔNG BÁO — AI NHẬN, KHI NÀO, NỘI DUNG GÌ")
table([
 ["Sự kiện", "Ai nhận", "Nội dung", "Bấm vào thì đi đâu"],
 ["NV KD bấm Đóng dự án", "Người lập và PM của các giải pháp chưa đóng; người lập các báo giá đang Đang tạo, Chờ Trưởng phòng hoặc Chờ Ban giám đốc duyệt; Trưởng phòng có quyền duyệt giá của đúng phòng ban các báo giá đang chờ Trưởng phòng; toàn bộ người có quyền duyệt giá Ban giám đốc nếu có báo giá chờ Ban giám đốc. Không gửi cho chính người bấm", "[DATKT] Cập nhật: <tên dự án>. Đã đóng dự án. Người đóng: …. Lý do: …. Ghi chú: …", "Màn quản lý dự án đó"],
 ["Đóng dự án cha", "Không gửi thông báo riêng cho dự án cha. Từng dự án con bị đóng theo gửi thông báo như dòng trên", "Như trên, theo từng dự án con", "Màn quản lý dự án con"],
 ["Hệ thống nhắc sắp đến hạn đóng", "NV KD phụ trách", "[DATKT] Sắp đến hạn: <tên dự án>. Hạn đóng: dd/mm/yyyy, còn N ngày. Mã: …. Còn theo dõi dự án này không?", "Màn quản lý dự án"],
 ["Hệ thống tự đóng dự án", "NV KD phụ trách", "[DATKT] Quá hạn: <tên dự án>. Hệ thống tự đóng do quá thời gian thực hiện. Mã: …", "Màn quản lý dự án"],
 ["NV KD chốt giải pháp", "PM và người tạo giải pháp, trừ người chốt", "[GP] Cập nhật: <tên dự án>. Đã chốt giải pháp. Hồ sơ: …. Người chốt: …", "Màn quản lý dự án"],
 ["NV KD gửi đề xuất gia hạn", "TOÀN BỘ người có quyền \"Trưởng phòng duyệt gia hạn dự án TKT\" (hệ thống gửi theo quyền, không lọc theo phòng ban)", "[DATKT] Chờ duyệt: <tên dự án>. Người đề xuất …. Xin gia hạn N ngày. Hạn đóng hiện tại …. Lý do …", "Màn Gia hạn dự án TKT, mở đúng đề xuất"],
 ["Trưởng phòng duyệt đề xuất vượt ngưỡng", "TOÀN BỘ người có quyền \"Ban giám đốc duyệt gia hạn dự án TKT\"", "Như trên, thêm dòng \"Trưởng phòng đã duyệt\"", "Màn Gia hạn dự án TKT, mở đúng đề xuất"],
 ["Đề xuất gia hạn được duyệt hoặc bị từ chối", "Người gửi đề xuất", "[DATKT] Đã duyệt: …. Đã duyệt gia hạn N ngày. Người duyệt …. Hạn đóng mới …  /  Từ chối: …. Không duyệt gia hạn N ngày. Người từ chối …. Lý do …", "Màn quản lý dự án"],
 ["Báo giá được duyệt", "Người lập báo giá, NV KD phụ trách dự án, Trưởng phòng duyệt giá của phòng ban báo giá", "Thông báo báo giá \"Đã duyệt\", kèm người duyệt", "Màn báo giá"],
], [3.2, 5.6, 4.6, 2.6])
h("Quy ước chung", 2)
bullet("Tên dự án in đậm, dài quá bị cắt; ghi chú dài quá bị cắt ở cuối và có nút Xem thêm.")
bullet("Việc chuyển bước tự nó KHÔNG gửi thông báo. Thông báo chỉ phát sinh từ các thao tác nghiệp vụ ở bảng trên (đóng, chốt giải pháp, gia hạn, duyệt báo giá, nhắc hạn).")
bullet("Dự án đóng mà không có giải pháp, báo giá đang dở nào thì không có người nhận, nên không có thông báo nào được gửi.")
bullet("Lỗi gửi thông báo không làm hỏng nghiệp vụ: dự án vẫn đóng, đề xuất vẫn được duyệt.")
bullet("Việc tiếp nhận yêu cầu làm giải pháp và duyệt hồ sơ giải pháp có thông báo riêng của phân hệ giải pháp, nằm ngoài phạm vi tài liệu này.")

# 7
h("7. PHÂN QUYỀN")
h("7.1 Ai nhìn thấy dự án nào", 2)
bullet("Dự án đang ở bước Đang tạo: chỉ người lập thấy.")
bullet("Các bước còn lại: người có quyền xem ở phạm vi Tổng công ty thấy tất cả; còn lại thấy theo phạm vi quyền xem được cấp (công ty, phòng ban, bộ phận, hoặc chỉ dự án mình lập) và thêm các dự án mình được gán là NV KD hỗ trợ.")
bullet("Người không có quyền xem danh sách dự án nào và cũng không được gán hỗ trợ thì chỉ thấy dự án do chính mình lập.")
h("7.2 Ai được làm gì", 2)
table([
 ["Thao tác", "Điều kiện được phép"],
 ["Sửa thông tin dự án", "Chỉ người lập dự án. Quyền xem theo phạm vi và NV KD hỗ trợ chỉ được xem."],
 ["Đóng dự án (con, độc lập, cha)", "Chỉ NV KD phụ trách; dự án chưa đóng. Với dự án cha, giao diện chỉ hiện nút khi dự án đang Đang thực hiện."],
 ["Chốt giải pháp", "Chỉ NV KD phụ trách; dự án có hồ sơ giải pháp Đã duyệt hoặc Hết hiệu lực; bắt buộc có file."],
 ["Chốt / hủy chốt báo giá", "Chỉ NV KD phụ trách dự án của báo giá (báo giá không gắn dự án thì chỉ người lập)."],
 ["Gửi đề xuất gia hạn", "Chỉ NV KD phụ trách, theo điều kiện ở chương 5.9."],
 ["Duyệt gia hạn", "Trưởng phòng: có quyền duyệt gia hạn cấp Trưởng phòng VÀ quản lý phòng ban của đề xuất. Ban giám đốc: có quyền duyệt gia hạn cấp Ban giám đốc VÀ thuộc đúng công ty của đề xuất."],
 ["Duyệt báo giá", "Trưởng phòng duyệt giá của phòng ban báo giá; Ban giám đốc duyệt giá của đúng công ty."],
 ["Tạo giải pháp (dự án Tự triển khai)", "Dự án đang ở bước 2, có cần làm giải pháp, phiếu thu thập thông tin đã nhập đủ trường bắt buộc, và chưa có giải pháp nào."],
], [5.0, 11.0])

# 8
h("8. QUY TẮC NGHIỆP VỤ BẮT BUỘC")
h("8.1 Bắt buộc nhập theo từng nút", 2)
table([
 ["Nút", "Bắt buộc"],
 ["Lưu nháp dự án", "Chỉ bắt buộc Tên dự án; các ô khác để trống được, nhưng ô đã nhập thì vẫn phải đúng định dạng. Chưa cấp mã dự án."],
 ["Lưu dự án (chính thức)", "Nhập đủ các trường bắt buộc; hệ thống cấp mã dự án."],
 ["Chốt giải pháp", "Chọn hồ sơ giải pháp và đính kèm ít nhất một file. Thiếu file hệ thống báo \"Vui lòng đính kèm file xác nhận của khách hàng\"."],
 ["Chốt báo giá cuối cùng", "Đính kèm ít nhất một file xác nhận của khách hàng, quy tắc như trên."],
 ["Hủy chốt báo giá", "Nhập lý do hủy chốt."],
 ["Đóng dự án", "Chọn nguyên nhân thất bại; ghi chú không quá 500 ký tự."],
 ["Gửi đề xuất gia hạn", "Nhập số ngày và lý do."],
 ["Từ chối đề xuất gia hạn, từ chối báo giá", "Nhập lý do."],
], [5.0, 11.0])
h("8.2 Ràng buộc dữ liệu và khóa chỉnh sửa", 2)
bullet("Bước không bao giờ do người dùng chọn hoặc sửa tay. Màn Sửa gửi lại bước cũ thì hệ thống bỏ qua.")
bullet("Từ khi dự án rời bước 1 và 2, \"Cách triển khai dự án\" và \"Có cần làm giải pháp\" bị khóa. Dự án đã có giải pháp hoặc yêu cầu làm giải pháp thì không đổi được cách triển khai.")
bullet("Loại dự án (cha, con, độc lập) chỉ đổi được khi dự án còn ở bước Đang tạo và chưa có dự án con trực thuộc.")
bullet("Dự án con phải nằm trong khung thời gian của dự án cha; khách hàng, giảm giá, tiền tệ, bảng giá của dự án con kế thừa từ dự án cha.")
bullet("Mỗi dự án chỉ có một giải pháp và tối đa một báo giá Trúng thầu.")
bullet("Cùng một khách hàng và cùng một nhóm ngành chỉ được có một dự án ở các bước 1 đến 7; từ bước 8 trở đi coi như đã sang làm hợp đồng và nhả nhóm ngành cho dự án mới.")
bullet("Dự án đã đóng: ẩn mọi nút thao tác đổi dữ liệu; không tạo được meeting mới.")
bullet("Dự án cha từ bước 7: không đổi được tổng ngân sách dự kiến.")
h("8.3 Quy tắc sinh mã", 2)
bullet("Dự án con và độc lập: mã sinh theo Ứng dụng của dự án khi bấm Lưu chính thức.")
bullet("Dự án cha: mã dạng \"phòng.năm.DAC…\" cấp khi bấm Lưu chính thức.")

# 9
h("9. CÁC LỐI VÀO MÀN HÌNH")
table([
 ["Bấm vào đâu", "Danh sách hiện ra", "Dùng khi nào"],
 ["CSKH trước bán → Dự án TKT", "Danh sách dự án TKT theo phạm vi quyền xem của người đăng nhập (dự án cha và con cùng một danh sách)", "Lối vào chính; cột Tiến trình dự án và bộ lọc Tiến trình nội bộ ở đây"],
 ["Từ danh sách chọn một dự án", "Màn quản lý dự án: tiêu đề có nhãn Tiến trình; các tab, nút Chốt giải pháp, Gia hạn, Đóng dự án", "Thao tác làm dự án chuyển bước"],
 ["Báo giá chờ duyệt, Gia hạn dự án TKT (menu duyệt của Trưởng phòng và Ban giám đốc)", "Hàng đợi báo giá và đề xuất gia hạn chờ đúng cấp, đúng phạm vi của người duyệt", "Người duyệt xử lý việc chờ"],
 ["CSKH trước bán → Báo cáo → Báo cáo vòng đời dự án TKT", "Báo cáo theo tiến trình dự án, có cơ cấu giai đoạn dự án", "Quản lý theo dõi số lượng dự án ở từng bước"],
 ["Bấm vào thông báo (chuông)", "Mở thẳng màn quản lý dự án hoặc màn Gia hạn dự án TKT đúng đề xuất", "Khi nhận thông báo ở chương 6"],
], [5.0, 6.6, 4.4])
bullet("Lối vào chỉ quyết định nơi người dùng đứng, không cấp thêm quyền: người không có quyền xem vẫn không thấy dự án.")
bullet("Nút Làm mới chỉ xóa điều kiện lọc.")

# 10
h("10. TRA CỨU, IN VÀ XUẤT DỮ LIỆU")
bullet("Bộ lọc nâng cao của danh sách dự án có ô Tiến trình nội bộ: liệt kê đúng tên các bước, dự án cha và con dùng chung danh sách chọn theo tên.")
bullet("File Excel xuất danh sách và báo cáo vòng đời dự án TKT hiển thị đúng tên bước theo loại dự án (cha hay con), không còn tên bước cũ.")
bullet("Báo cáo vòng đời dự án TKT có cột \"Cơ cấu giai đoạn dự án\" và nhãn \"Tiến trình dự án\".")

# 11
h("11. LIÊN THÔNG VỚI HỆ THỐNG KHÁC")
table([
 ["Điểm", "Bên cũ", "Bên mới", "Lý do"],
 ["Tên bước 5, 6, 7 của dự án con", "Đã duyệt giải pháp · Dự toán · Thương thảo giá", "Trao đổi giải pháp với khách hàng · Lập dự toán · Thương thảo giá và giải pháp", "Khớp bảng Tiến trình dự án con / độc lập nội bộ của quy trình QTTT ngày 10/09"],
 ["Chốt giải pháp", "Đưa dự án thẳng sang bước 8", "Chỉ sang bước 6; bước 8 do nút Chốt báo giá cuối cùng đặt", "Chốt giải pháp mới là xong việc kỹ thuật, chưa thống nhất giá với khách"],
 ["Chốt giải pháp và chốt báo giá", "Không bắt buộc file", "Bắt buộc đính kèm file xác nhận của khách", "Có bằng chứng khách đã đồng ý trước khi sang bước sau"],
 ["Tên bước hiển thị", "Mỗi màn tự ghi tên bước", "Tên bước và màu do hệ thống quyết định, mọi màn dùng chung", "Hết tình trạng mỗi nơi một tên, dự án cha không còn hiện sai tên"],
 ["Báo giá tổng của dự án cha", "—", "Không làm dự án cha đổi bước khi duyệt, không đồng bộ lại sang ERP", "Các báo giá con đã đồng bộ; đồng bộ thêm sẽ trùng dữ liệu"],
 ["Hợp đồng bên ERP", "—", "Hợp đồng lập từ báo giá tổng làm dự án cha sang bước 7", "Hợp đồng được lập và quản lý trên ERP, HRM chỉ nhận kết quả"],
], [3.4, 3.8, 5.0, 3.8])

# 12
h("12. GIỚI HẠN HIỆN TẠI")
bullet("Bước 9, 10, 12 của dự án con và bước 8, 9, 10, 12 của dự án cha chưa có thao tác nào đưa dự án vào, vì phụ thuộc trạng thái hợp đồng; dự kiến làm ở giai đoạn sau. Hợp đồng bị Hủy hoặc Đóng thì tự đóng dự án cũng chưa làm.")
bullet("Bước 12: tài liệu yêu cầu chưa nói rõ ai thực hiện việc chuyển sang Kết thúc và lưu trữ, cần khách hàng chốt.")
bullet("ĐÃ CHẠY THỬ: duyệt thêm một báo giá khi dự án đang ở bước 8 hoặc bước 9 đưa dự án VỀ BƯỚC 7. Chỉ không đổi khi dự án đã ở bước 7. Cần khách hàng xác nhận đây có phải hành vi mong muốn không.")
bullet("ĐÃ CHẠY THỬ: hệ thống tự đóng hằng ngày quét cả dự án cha như dự án thường. Dự án cha không có báo giá được duyệt riêng nên tính hạn theo ngày tạo cộng số tháng cấu hình chung (ví dụ dự án cha tạo 05/10/2026 có hạn đóng 05/01/2027). Thử giả lập quá hạn thì lịch chạy báo [ĐÓNG] dự án cha; khi đóng theo đường tự động thì chỉ dự án cha chuyển Đóng, các dự án con vẫn giữ nguyên bước cũ. Khi NV KD bấm nút Đóng dự án cha thì các con bị đóng theo. Cần khách hàng xác nhận cách xử lý.")
bullet("Nút Đóng dự án của dự án cha chỉ bị giới hạn ở bước Đang thực hiện trên giao diện; phía hệ thống chỉ chặn khi dự án cha đã đóng.")
bullet("ĐÃ CHẠY THỬ: với dự án cha, điều kiện cho phép gửi đề xuất gia hạn ở hệ thống trả \"được phép\", trong khi giao diện dự án cha không có tab Gia hạn.")
bullet("Ở màn chi tiết Giải pháp, nhãn \"Tiến trình nội bộ\" đang hiện trạng thái của giải pháp, không phải bước của dự án; chưa quyết định có sửa hay không.")
bullet("Tab Dự án con chưa kiểm thử được bằng dữ liệu thật trên môi trường dev vì chưa có dự án cha nào có con.")

h("13. KẾT QUẢ KIỂM CHỨNG TRÊN HỆ THỐNG")
para("Ngày 17/11/2026 đã gọi trực tiếp các chức năng thật của hệ thống trên dữ liệu thử nghiệm (cơ sở dữ liệu nội bộ của máy phát triển), sau mỗi lần thử đều hoàn tác nên dữ liệu không đổi. Bảng dưới là kết quả.")
table([
 ["Nội dung kiểm", "Kết quả quan sát được", "Khớp tài liệu"],
 ["Yêu cầu làm giải pháp: Gửi", "Dự án sang bước 3", "Khớp"],
 ["Phòng giải pháp bấm Tiếp nhận", "Không gọi đồng bộ bước, dự án giữ bước 3", "Đã sửa tài liệu (trước ghi nhầm là sang bước 4)"],
 ["Giải pháp Chờ PM / Chờ Leader / Đang triển khai / Chờ duyệt giải pháp (dự án Theo phòng, Liên phòng)", "Cả 4 trạng thái đều đưa dự án sang bước 4", "Khớp"],
 ["Giải pháp Đã duyệt giải pháp", "Dự án sang bước 5", "Khớp"],
 ["Dự án Tự triển khai: giải pháp Đang triển khai", "Sang bước 4", "Khớp"],
 ["Dự án Tự triển khai: giải pháp Chờ PM, Chờ Leader, Chờ duyệt giải pháp", "Dự án KHÔNG đổi bước (giữ bước 2)", "Đã sửa tài liệu"],
 ["Dự án Tự triển khai: tạo giải pháp khi đang bước 6, hoặc bước 2 mà không cần làm giải pháp", "Bị chặn: \"Dự án không đủ điều kiện để tạo giải pháp\"", "Khớp"],
 ["Yêu cầu làm giải pháp bị Từ chối hoặc Hủy", "Dự án về bước 2 từ bước 3, 4, 6, 7", "Khớp"],
 ["Yêu cầu bổ sung thông tin", "Chỉ về bước 2 khi dự án đang ở bước 3; ở bước 4 và 6 giữ nguyên", "Khớp"],
 ["Yêu cầu xây dựng giá", "Từ bước 2 lên 6; đang ở bước 7 giữ nguyên", "Khớp"],
 ["Chốt báo giá cuối cùng", "Từ bước 7 lên 8; đang ở bước 9 giữ nguyên", "Khớp"],
 ["Hủy chốt báo giá", "Chỉ lùi về 7 khi dự án đang đúng ở bước 8; đang ở 9 hoặc 6 giữ nguyên", "Khớp"],
 ["Mọi lần đổi bước qua các đường trên", "Có ghi lịch sử chuyển bước", "Khớp"],
 ["Duyệt báo giá khi dự án đang ở bước 8 hoặc 9", "Dự án bị đưa về bước 7", "Phát hiện mới, ghi ở chương 12"],
 ["Màn Sửa gửi lại trạng thái \"Thu thập thông tin\" cho dự án đang ở bước 6", "Dự án vẫn ở bước 6", "Khớp"],
 ["Đóng dự án có việc dở (1 giải pháp, 2 yêu cầu làm giải pháp, 4 yêu cầu xây dựng giá, 2 báo giá)", "Tất cả chuyển Đóng, dự án sang bước 11. Người nhận thông báo: người lập giải pháp và người lập báo giá đang dở", "Khớp"],
 ["Đóng lại dự án đã đóng", "Bị chặn: \"Dự án đã đóng\"", "Khớp"],
 ["Đóng dự án cha bằng nút", "Cha và cả 2 dự án con sang bước 11", "Khớp"],
 ["Đóng dự án cha theo đường tự động (lịch hằng ngày)", "Chỉ dự án cha sang bước 11, 2 dự án con giữ nguyên", "Phát hiện mới, ghi ở chương 12"],
 ["Lịch tự đóng có quét dự án cha không", "Có. Giả lập quá hạn thì báo [ĐÓNG] dự án cha", "Phát hiện mới, ghi ở chương 12"],
 ["Hợp đồng lập từ báo giá tổng", "Dự án cha sang bước 7, báo giá tổng sang \"Đã tạo hợp đồng\"", "Khớp"],
 ["Đề xuất gia hạn 20 ngày và đúng 30 ngày", "Cấp Trưởng phòng; Trưởng phòng duyệt xong, hạn đóng lùi đúng số ngày, ngày kết thúc dự án không đổi", "Khớp"],
 ["Đề xuất gia hạn 31 ngày", "Cấp Ban giám đốc; Trưởng phòng duyệt chuyển sang chờ Ban giám đốc, chưa cộng ngày; Ban giám đốc duyệt mới cộng ngày", "Khớp"],
 ["Gửi đề xuất thứ hai khi đang có đề xuất chờ", "Bị chặn: \"Dự án đang có đề xuất gia hạn chờ duyệt\"", "Khớp"],
 ["Gửi đề xuất gia hạn cho dự án cha", "Hệ thống cho phép", "Phát hiện mới, ghi ở chương 12"],
], [5.6, 6.8, 3.6])
h("Những phần CHƯA chạy thử", 2)
bullet("Bấm Lưu nháp và Lưu chính thức trên màn tạo dự án (kể cả dự án cha): chỉ đọc code và đọc màn hình, giao diện gửi trạng thái 2 khi Lưu.")
bullet("Duyệt báo giá tổng của dự án cha không đổi bước cha: chỉ đọc code (chú thích trong hệ thống nêu rõ cố ý không đổi).")
bullet("Nội dung chữ và người nhận của thông báo duyệt báo giá, thông báo nhắc hạn và tự đóng khi gửi thật: chưa gửi thử để tránh tạo thông báo.")
bullet("Chốt giải pháp thiếu file bị chặn: đã kiểm trước đó ở lần làm tính năng, không chạy lại hôm nay.")
bullet("Chương 9 chưa lần hết phạm vi danh sách của từng lối vào.")

out = "/Users/manhcuong/Desktop/dns/HRM/.plans/prospective-project-status-12-steps/Mô tả tiến trình dự án TKT_v3.docx"
doc.save(out); print(out)
