# -*- coding: utf-8 -*-
"""
Sinh tài liệu MÔ TẢ NGHIỆP VỤ cho TRỌN LUỒNG DỊCH VỤ (5 chứng từ) — bản 28/08/2026.

Khác các file mô tả nghiệp vụ đã có (mỗi file 1 màn), file này mô tả CẢ DÂY CHUYỀN:
Yêu cầu KT SC-BH -> Phiếu xử lý -> Phiếu cung cấp thông tin -> Báo giá dịch vụ,
kèm nhánh tự động Phiếu bảo hành.

Nguồn dữ liệu (đọc trực tiếp, không suy đoán):
  · Hằng trạng thái + accessor điều kiện: Modules/CustomerCare/Entities/**
  · Việc phát sinh theo trạng thái      : *Service::applyStatusSideEffects()
  · Người nhận thông báo                : *Notifier
  · Lối vào + số liệu thật              : gen_loi_vao.py (đo 28/08/2026, DB gộp)
  · Khác biệt cố ý với ERP              : design.md mục 9 + plan.md
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

JUSTIFY = WD_ALIGN_PARAGRAPH.JUSTIFY
CENTER = WD_ALIGN_PARAGRAPH.CENTER

doc = Document()
doc.styles["Normal"].font.name = "Times New Roman"
doc.styles["Normal"].font.size = Pt(12)


def h(text, level):
    doc.add_paragraph(text, style="Heading %d" % level)


def para(text):
    p = doc.add_paragraph()
    p.alignment = JUSTIFY
    p.add_run(text)


def bullet(text):
    doc.add_paragraph(text, style="List Bullet")


def table(rows):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Light Grid Accent 1"
    t.alignment = 1
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            t.cell(i, j).text = val
    doc.add_paragraph()


# ══════════════════════════════ BÌA ══════════════════════════════
p = doc.add_paragraph()
p.alignment = CENTER
r = p.add_run("MÔ TẢ NGHIỆP VỤ")
r.bold = True
r.font.size = Pt(20)

p = doc.add_paragraph()
p.alignment = CENTER
r = p.add_run("LUỒNG DỊCH VỤ SỬA CHỮA – BẢO HÀNH\n(trọn 5 chứng từ)")
r.bold = True
r.font.size = Pt(16)

p = doc.add_paragraph()
p.alignment = CENTER
p.add_run("Phân hệ Chăm sóc khách hàng · Bán dịch vụ — Cập nhật ngày 28/08/2026")

doc.add_page_break()

# ══════════════════════ 1. TÀI LIỆU NÀY DÀNH CHO AI ══════════════════════
h("1. TÀI LIỆU NÀY DÀNH CHO AI", 1)
para(
    "Tài liệu mô tả trọn dây chuyền chứng từ của mảng dịch vụ sửa chữa – bảo hành: từ lúc khách "
    "hàng báo hỏng thiết bị cho tới lúc gửi được báo giá cho khách, kèm nhánh xử lý phần thiết bị "
    "còn trong bảo hành. Tài liệu không hướng dẫn bấm từng nút (việc đó ở tài liệu Hướng dẫn sử "
    "dụng), mà trả lời: mỗi chứng từ dùng để làm gì, ai lập, khi nào chuyển trạng thái, ai nhận "
    "thông báo và quy tắc nào chi phối."
)
bullet("Cán bộ kinh doanh tiếp nhận yêu cầu của khách hàng")
bullet("Cán bộ phòng dịch vụ / kỹ thuật đi khảo sát và cung cấp thông tin")
bullet("Người làm báo giá và người phụ trách theo dõi tiến độ dịch vụ")
bullet("Quản lý phòng ban, người nghiệm thu chức năng")
bullet("Nhân viên kiểm thử cần hiểu luồng trước khi viết và chạy kịch bản kiểm thử")

# ══════════════════════ 2. DÙNG ĐỂ LÀM GÌ ══════════════════════
h("2. LUỒNG NÀY DÙNG ĐỂ LÀM GÌ", 1)

h("2.1. Mục đích", 2)
para(
    "Khi khách hàng báo thiết bị hỏng, công ty phải trả lời được ba câu trước khi nhận việc: hỏng "
    "cái gì, sửa được hay không, và khách phải trả bao nhiêu. Trước đây chuỗi việc này chạy bằng "
    "điện thoại và bảng tính rời rạc: người nhận yêu cầu ghi một nơi, kỹ thuật khảo sát ghi một "
    "nơi, người làm báo giá lại gõ lại từ đầu. Hậu quả thường gặp là sót thiết bị, tính thiếu tiền "
    "dịch vụ, không biết việc đang nằm ở ai, và không phân định được phần nào khách phải trả tiền "
    "còn phần nào công ty làm miễn phí theo cam kết bảo hành."
)
para(
    "Luồng dịch vụ nối các bước đó thành một dây chuyền chứng từ: chứng từ sau lập từ chứng từ "
    "trước, dữ liệu chép sang chứ không gõ lại, và mỗi lần một bên hoàn thành phần việc của mình "
    "thì trạng thái của các chứng từ liên quan tự đổi theo để bên kia biết đến lượt mình."
)

h("2.2. Vị trí trong luồng lớn", 2)
para(
    "Luồng gồm bốn chứng từ nối tiếp và một nhánh tự động:"
)
table([
    ["Bước", "Chứng từ", "Ai lập", "Việc chính"],
    ["1", "Yêu cầu kiểm tra sửa chữa – bảo hành",
     "Người tiếp nhận yêu cầu của khách", "Ghi nhận khách hàng, địa chỉ, danh sách thiết bị hỏng"],
    ["2", "Phiếu xử lý yêu cầu",
     "Phòng tiếp nhận", "Quyết hướng xử lý cho TỪNG thiết bị: tư vấn điện thoại hay đi khảo sát"],
    ["3", "Phiếu cung cấp thông tin làm báo giá",
     "Cán bộ kỹ thuật", "Khảo sát thực tế, khai công – dịch vụ – vật tư và các khoản chi phí"],
    ["4", "Báo giá dịch vụ",
     "Người lập Phiếu yêu cầu (bên kinh doanh)", "Nạp thuế suất, thêm hàng hoá, chốt giá gửi khách"],
    ["Nhánh", "Phiếu bảo hành",
     "Hệ thống tự sinh", "Tách riêng phần thiết bị công ty làm miễn phí theo cam kết bảo hành"],
    ["5", "Hợp đồng dịch vụ", "—", "CHƯA CÓ trên hệ thống mới, xem chương 12"],
])
para(
    "Ba bước đầu bắt buộc nối tiếp: không bước nào lập được nếu bước trước chưa gửi đi. Bước 4 là "
    "bước đầu tiên phá thế nối tiếp — báo giá dịch vụ lập được cả khi không có chứng từ nào ở "
    "trước (xem mục 5.5)."
)

h("2.3. Giá trị mang lại", 2)
bullet("Không gõ lại dữ liệu: nội dung chép từ chứng từ trước sang, giảm sai sót và rút ngắn thời gian.")
bullet("Luôn biết việc đang nằm ở ai: mỗi lần gửi đi là trạng thái của cả chuỗi chứng từ đổi theo.")
bullet("Tách bạch tiền: phần bảo hành khách trả 0 đồng được tách hẳn sang một phiếu riêng, phần sửa chữa – bảo dưỡng mới đi tiếp sang báo giá.")
bullet("Có hộp việc riêng cho từng vai: mỗi người vào đúng lối vào của mình là thấy đúng phần việc đến lượt mình.")
bullet("Truy được vết: mọi thay đổi trạng thái và mọi lần sửa đều ghi vào Lịch sử thay đổi của chứng từ.")

# ══════════════════════ 3. NHỮNG AI THAM GIA ══════════════════════
h("3. NHỮNG AI THAM GIA", 1)
table([
    ["Vai trò", "Làm gì trong luồng"],
    ["Khách hàng",
     "Không thao tác trên hệ thống. Báo hỏng thiết bị, cung cấp thông tin thiết bị và nhận báo giá."],
    ["Người tiếp nhận yêu cầu (kinh doanh)",
     "Lập Phiếu yêu cầu ở bước 1. Về sau chính người này là người LÀM BÁO GIÁ ở bước 4, và cũng "
     "chính người này có quyền Từ chối tiếp nhận Phiếu cung cấp thông tin nếu thấy thông tin chưa đạt."],
    ["Phòng tiếp nhận",
     "Nhận thông báo khi phiếu yêu cầu được gửi. Lập Phiếu xử lý yêu cầu, quyết hướng xử lý từng "
     "thiết bị. Có thể Từ chối phiếu yêu cầu kèm lý do."],
    ["Cán bộ kỹ thuật (người có quyền Tạo phiếu cung cấp thông tin)",
     "Đi khảo sát, lập Phiếu cung cấp thông tin làm báo giá: khai lỗi, công, dịch vụ, vật tư, chi "
     "phí, và quyết định từng thiết bị thuộc diện Bảo hành hay Sửa chữa."],
    ["Người làm báo giá",
     "Chính là người đã lập Phiếu yêu cầu. Lập Báo giá dịch vụ, nạp thuế suất, thêm hàng hoá, đặt "
     "số ngày hiệu lực rồi tự duyệt."],
    ["Quản lý phòng ban / công ty",
     "Không thao tác bắt buộc. Theo dõi theo phạm vi quyền được cấp (chương 7)."],
    ["Hệ thống",
     "Tự sinh Phiếu bảo hành khi Phiếu cung cấp thông tin được gửi đi; tự chuyển báo giá quá hạn "
     "sang Hết hiệu lực vào 00:30 hằng ngày."],
])

# ══════════════════════ 4. VÒNG ĐỜI ══════════════════════
h("4. VÒNG ĐỜI CỦA TỪNG CHỨNG TỪ", 1)
para(
    "Bảng dưới ghi rõ trạng thái nào do chính màn đó tạo ra, trạng thái nào do chứng từ khác đẩy "
    "ngược về. Trạng thái do chứng từ khác đẩy về thì người dùng của màn đó KHÔNG tự đặt được."
)

h("4.1. Yêu cầu kiểm tra sửa chữa – bảo hành", 2)
table([
    ["Trạng thái", "Ý nghĩa", "Ai làm nó chuyển sang trạng thái này"],
    ["Đang tạo", "Phiếu nháp, chỉ người lập nhìn thấy, còn sửa và xoá được", "Người lập bấm Lưu"],
    ["Chờ xử lý", "Đã gửi cho phòng tiếp nhận, phiếu khoá", "Người lập bấm Lưu và gửi"],
    ["Đang xử lý", "Phòng tiếp nhận đã lập Phiếu xử lý yêu cầu", "Phiếu xử lý (bước 2) đẩy về"],
    ["Đã xử lý", "Phiếu xử lý đã gửi đi và có phần cần khảo sát", "Phiếu xử lý (bước 2) đẩy về"],
    ["Đã tư vấn điện thoại", "Mọi thiết bị xử lý xong qua điện thoại — LUỒNG ĐÓNG tại đây",
     "Phiếu xử lý (bước 2) đẩy về"],
    ["Đang CCTT", "Kỹ thuật đang làm dở Phiếu cung cấp thông tin (mới lưu nháp)",
     "Phiếu cung cấp thông tin (bước 3) đẩy về"],
    ["Đã CCTT báo giá", "Phiếu cung cấp thông tin đã gửi đi",
     "Phiếu cung cấp thông tin (bước 3) đẩy về"],
    ["Đã báo giá", "Báo giá dịch vụ đã được duyệt", "Báo giá dịch vụ (bước 4) đẩy về"],
    ["Đã lập hợp đồng", "Hợp đồng dịch vụ đã lập",
     "Hợp đồng (bước 5) đẩy về — bước 5 chưa có trên hệ thống mới, hiện chỉ là dữ liệu cũ"],
])

h("4.2. Phiếu xử lý yêu cầu", 2)
table([
    ["Trạng thái", "Ý nghĩa", "Ai làm nó chuyển sang trạng thái này"],
    ["Đang tạo", "Phiếu nháp, còn sửa và xoá được", "Người lập bấm Lưu"],
    ["Chờ CCTT", "Đã gửi đi, có ít nhất một thiết bị chọn hướng Cung cấp thông tin làm báo giá",
     "Người lập bấm Lưu và gửi"],
    ["Đã tư vấn điện thoại", "MỌI thiết bị đều chọn hướng Tư vấn điện thoại — phiếu này và phiếu "
     "yêu cầu gốc cùng đóng", "Người lập bấm Lưu và gửi"],
    ["Đang CCTT", "Kỹ thuật đã lưu nháp Phiếu cung cấp thông tin",
     "Phiếu cung cấp thông tin (bước 3) đẩy về"],
    ["Đã CCTT", "Phiếu cung cấp thông tin đã gửi đi; phiếu được đóng dấu người và ngày xử lý",
     "Phiếu cung cấp thông tin (bước 3) đẩy về"],
    ["Chờ CCTT bổ sung", "Cần bổ sung thông tin cho phần đã cung cấp", "Người xử lý đặt lại"],
])

h("4.3. Phiếu cung cấp thông tin làm báo giá", 2)
table([
    ["Trạng thái", "Ý nghĩa", "Ai làm nó chuyển sang trạng thái này"],
    ["Đang tạo", "Phiếu nháp. Phiếu nháp của người khác thì KHÔNG ai xem được, kể cả quản trị",
     "Người lập bấm Lưu"],
    ["Chờ làm báo giá", "Đã gửi đi, phiếu khoá không sửa được nữa", "Người lập bấm Lưu và gửi"],
    ["Không duyệt", "Bị trả lại kèm lý do; người lập sửa rồi gửi lại được",
     "Người lập Phiếu yêu cầu bấm Từ chối tiếp nhận"],
    ["Đang báo giá", "Báo giá dịch vụ mới lưu nháp", "Báo giá dịch vụ (bước 4) đẩy về"],
    ["Báo giá đã duyệt", "Báo giá dịch vụ đã duyệt", "Báo giá dịch vụ (bước 4) đẩy về"],
    ["Đã lập hợp đồng / Đã hoàn thành / Kết thúc", "Các chứng từ phía sau đẩy ngược về",
     "Không tự đặt được từ màn này"],
])
para(
    "Màn này còn một cột riêng là Trạng thái bảo hành, chạy song song và độc lập với cột Trạng "
    "thái: để trống nếu phiếu không có thiết bị bảo hành; nhận giá trị Đã tạo phiếu bảo hành ngay "
    "khi phiếu được gửi đi và có thiết bị bảo hành. Giá trị Chờ tạo phiếu bảo hành trên thực tế "
    "không xuất hiện ở màn này, vì phiếu bảo hành sinh ngay trong lúc bấm Lưu và gửi, không có "
    "quãng chờ nào ở giữa."
)

h("4.4. Báo giá dịch vụ", 2)
table([
    ["Trạng thái", "Ý nghĩa", "Ai làm nó chuyển sang trạng thái này"],
    ["Đang tạo", "Báo giá nháp, chỉ người lập sửa và xoá được", "Người lập bấm Lưu nháp"],
    ["Duyệt", "Đã chốt giá, phiếu khoá; hệ thống đóng dấu người duyệt và ngày duyệt",
     "Người lập bấm Lưu và duyệt — KHÔNG có người duyệt riêng, người lập tự duyệt"],
    ["Đã tạo hợp đồng", "Hợp đồng dịch vụ đã lập từ báo giá này",
     "Hợp đồng (bước 5) đẩy về — chưa phát sinh trên hệ thống mới"],
    ["Hết hiệu lực", "Quá số ngày hiệu lực ghi trên báo giá",
     "Hệ thống tự chuyển vào 00:30 hằng ngày"],
])

h("4.5. Phiếu bảo hành", 2)
table([
    ["Trạng thái", "Ý nghĩa", "Ai làm nó chuyển sang trạng thái này"],
    ["Đang tạo", "Không phát sinh trong thực tế — phiếu sinh tự động nên bỏ qua bước nháp", "—"],
    ["Đã duyệt", "Trạng thái ngay khi phiếu được sinh ra, vì không cần ai duyệt",
     "Hệ thống đặt lúc sinh phiếu"],
    ["Đang thực hiện / Đã hoàn thành", "Do bước giao việc và nghiệm thu đặt",
     "Hai bước đó chưa đưa vào sử dụng"],
])

# ══════════════════════ 5. LUỒNG HOẠT ĐỘNG ══════════════════════
h("5. LUỒNG HOẠT ĐỘNG CHI TIẾT", 1)

h("5.1. Bước 1 — Tiếp nhận yêu cầu của khách hàng", 2)
para(
    "Khách hàng báo thiết bị hỏng. Người tiếp nhận lập Phiếu yêu cầu kiểm tra sửa chữa – bảo hành, "
    "khai khách hàng, người liên hệ, địa chỉ sửa chữa, phòng tiếp nhận và danh sách thiết bị liên "
    "quan. Thiết bị chọn từ danh sách thiết bị của chính khách hàng đó (thiết bị đã mua của công "
    "ty, thiết bị cũ khách tự khai, hoặc thiết bị của nhà cung cấp khác), không phải chọn tự do "
    "trong danh mục hàng hoá."
)
table([
    ["Bấm nút gì", "Diễn ra thế nào", "Kết quả"],
    ["Lưu", "Phiếu ghi nhận ở dạng nháp", "Trạng thái Đang tạo — chỉ người lập nhìn thấy, còn sửa và xoá được"],
    ["Lưu và gửi", "Phiếu gửi cho phòng tiếp nhận và khoá lại",
     "Trạng thái Chờ xử lý. Toàn bộ nhân viên phòng tiếp nhận nhận thông báo"],
])
para(
    "Phòng tiếp nhận có thể Từ chối phiếu kèm lý do; khi đó người lập phiếu nhận thông báo kèm lý "
    "do để sửa lại."
)

h("5.2. Bước 2 — Quyết hướng xử lý cho từng thiết bị", 2)
para(
    "Từ một phiếu yêu cầu đang ở trạng thái Chờ xử lý, phòng tiếp nhận bấm Tạo phiếu xử lý yêu "
    "cầu. Với TỪNG thiết bị trên phiếu, người xử lý chọn một trong hai hướng."
)
table([
    ["Hướng xử lý", "Diễn ra thế nào", "Kết quả sau khi bấm Lưu và gửi"],
    ["Tư vấn điện thoại",
     "Lỗi đơn giản, hướng dẫn khách tự xử lý qua điện thoại, không phát sinh chi phí",
     "Nếu MỌI thiết bị đều chọn hướng này: phiếu xử lý và phiếu yêu cầu gốc cùng chuyển Đã tư vấn "
     "điện thoại. Luồng ĐÓNG tại đây, không đi tiếp"],
    ["Cung cấp thông tin làm báo giá",
     "Phải cử người đi khảo sát thực tế mới biết sửa thế nào và hết bao nhiêu",
     "Phiếu xử lý chuyển Chờ CCTT, phiếu yêu cầu gốc chuyển Đã xử lý. Mọi người có quyền Tạo phiếu "
     "cung cấp thông tin trong cùng công ty nhận thông báo"],
])
para(
    "Chỉ cần một thiết bị chọn hướng khảo sát là phiếu đi tiếp; các thiết bị tư vấn qua điện thoại "
    "trên cùng phiếu coi như đã xong."
)

h("5.3. Bước 3 — Khảo sát và cung cấp thông tin làm báo giá", 2)
para(
    "Từ một phiếu xử lý đang Chờ CCTT, cán bộ kỹ thuật bấm Tạo phiếu cung cấp thông tin. Đây là "
    "chứng từ ĐẦU TIÊN có tiền. Phiếu chia thành các khối:"
)
bullet("A – Bảo hành thiết bị: những thiết bị công ty làm miễn phí theo cam kết bảo hành, khách trả 0 đồng.")
bullet("B – Dịch vụ kiểm tra, sửa chữa, bảo dưỡng: gồm phần I thiết bị sửa chữa và phần II thiết bị cần bảo dưỡng.")
bullet("C – Chi phí khác: các khoản chi phí liên quan và chi phí vận chuyển.")
bullet("D – Tổng hợp: bảng tiền của phần bảo hành, phần sửa chữa – bảo dưỡng và bảng tổng hợp chung.")
para(
    "Mỗi dòng thiết bị có ô Loại công việc. Chọn Bảo hành thì cả dòng chuyển sang khối A và hệ "
    "thống tự đặt chi phí được bảo hành bằng đúng thành tiền của công, dịch vụ và vật tư của dòng "
    "đó — khách trả 0. Chuyển ngược lại sang Sửa chữa thì các cột Cho bảo hành và Miễn phí ở khối "
    "chi phí bị đặt lại về 0 và phải nhập lại."
)
table([
    ["Bấm nút gì", "Diễn ra thế nào", "Kết quả"],
    ["Lưu", "Ghi nhận phiếu nháp",
     "Phiếu Đang tạo. Phiếu xử lý và phiếu yêu cầu gốc cùng chuyển Đang CCTT, để người khác biết "
     "việc đang có người làm"],
    ["Lưu và gửi", "Phiếu gửi đi và khoá",
     "Phiếu chuyển Chờ làm báo giá, đóng dấu người và thời điểm gửi. Phiếu xử lý chuyển Đã CCTT "
     "kèm đóng dấu người xử lý; phiếu yêu cầu gốc chuyển Đã CCTT báo giá. Nếu có thiết bị ở khối A "
     "thì Phiếu bảo hành sinh ra ngay. Nếu phiếu có phần cần báo giá thì người lập Phiếu yêu cầu "
     "nhận thông báo"],
])

h("5.4. Nhánh tự động — Phiếu bảo hành", 2)
para(
    "Không ai lập Phiếu bảo hành bằng tay. Khi Phiếu cung cấp thông tin được gửi đi và có ít nhất "
    "một thiết bị ở khối A, hệ thống lập tức sinh một phiếu bảo hành: chép sang toàn bộ thiết bị, "
    "dịch vụ, vật tư của khối A cùng các khoản chi phí, và tính lại phần tiền bảo hành từ chính dữ "
    "liệu đã lưu chứ không lấy số từ màn hình. Phiếu ra đời đã ở trạng thái Đã duyệt."
)
bullet("Bấm Lưu (nháp) thì KHÔNG sinh phiếu bảo hành.")
bullet("Mỗi phiếu cung cấp thông tin chỉ sinh ĐÚNG MỘT phiếu bảo hành — bị từ chối rồi gửi lại cũng không sinh thêm.")
bullet("Bước sinh phiếu bảo hành KHÔNG gửi thông báo cho ai.")
para(
    "Trên dữ liệu thật, phần lớn phiếu cung cấp thông tin là phiếu CHỈ CÓ bảo hành: khách không "
    "phải trả gì nên không có gì để báo giá, và luồng của những phiếu này DỪNG LẠI ở phiếu bảo "
    "hành — không bắn thông báo, không vào hộp việc chờ làm báo giá, không có thao tác Tạo báo giá "
    "dịch vụ lẫn Từ chối tiếp nhận."
)

h("5.5. Bước 4 — Lập báo giá dịch vụ", 2)
para("Báo giá dịch vụ có BA đường vào, cùng dùng một form:")
table([
    ["Đường vào", "Khi nào dùng", "Điều kiện"],
    ["Từ Phiếu cung cấp thông tin (thao tác Tạo báo giá dịch vụ)",
     "Đường đi chuẩn của dây chuyền", "Đủ 4 điều kiện ở mục 5.6"],
    ["Lập độc lập (bấm Tạo mới trên màn danh sách báo giá)",
     "Khách hỏi giá dịch vụ mà chưa qua bước tiếp nhận – khảo sát nào",
     "Không có điều kiện. Người lập tự chọn khách hàng, người liên hệ, địa chỉ sửa chữa và tự thêm "
     "thiết bị từ danh sách thiết bị của khách"],
    ["Nhân bản một báo giá cũ",
     "Khách cũ hỏi lại một bộ dịch vụ tương tự", "Hiện với mọi báo giá trong tầm nhìn của mình"],
])
para(
    "Việc cốt lõi của bước này là NẠP THUẾ SUẤT: phiếu cung cấp thông tin không có thuế suất, nên "
    "khi chép sang báo giá, thuế suất của công, vật tư, dịch vụ và gói bảo dưỡng được nạp mới từ "
    "danh mục. Báo giá còn có thêm khối Loại hàng hoá mà phiếu trước không có, và hai cột tồn kho "
    "hiện lên khi người lập chọn kho để xem tồn."
)
table([
    ["Bấm nút gì", "Diễn ra thế nào", "Kết quả"],
    ["Lưu nháp", "Ghi nhận báo giá nháp", "Báo giá Đang tạo. Phiếu cung cấp thông tin gốc chuyển Đang báo giá"],
    ["Lưu và duyệt", "Báo giá TỰ DUYỆT, không chờ ai phê duyệt",
     "Báo giá chuyển Duyệt, đóng dấu người và ngày duyệt rồi khoá. Phiếu cung cấp thông tin chuyển "
     "Báo giá đã duyệt, phiếu yêu cầu gốc chuyển Đã báo giá. KHÔNG gửi thông báo cho ai"],
])
para(
    "Lưu ý về nhân bản: bản sao là một báo giá ĐỘC LẬP — cắt sạch liên kết với phiếu yêu cầu, "
    "phiếu xử lý và phiếu cung cấp thông tin của bản gốc, không mang mã cũ và không chép tệp đính "
    "kèm. Địa chỉ khách hàng và thuế suất được nạp lại theo danh mục hiện tại, nên bản sao CÓ THỂ "
    "ra số tiền khác bản gốc nếu danh mục đã thay đổi. Đây là chủ ý: báo giá mới phải dùng địa chỉ "
    "và thuế suất đang có hiệu lực."
)

h("5.6. Bốn điều kiện để lập được báo giá từ phiếu cung cấp thông tin", 2)
para(
    "Thao tác Tạo báo giá dịch vụ và thao tác Từ chối tiếp nhận trên phiếu cung cấp thông tin dùng "
    "chung một bộ điều kiện. Thiếu một điều kiện là cả hai nút cùng biến mất."
)
table([
    ["#", "Điều kiện", "Ghi chú"],
    ["1", "Phiếu đang ở trạng thái Chờ làm báo giá", ""],
    ["2", "Phiếu CÓ phần cần báo giá: ít nhất một thiết bị sửa chữa, hoặc một thiết bị bảo dưỡng, "
          "hoặc chi phí sửa chữa lớn hơn 0",
     "Đây là điều kiện lọc mạnh nhất — phiếu thuần bảo hành bị loại ở đây"],
    ["3", "Người bấm CHÍNH LÀ người đã lập Phiếu yêu cầu ở bước 1",
     "Không phải người lập phiếu cung cấp thông tin, và cũng không phải người có quyền cao. Quản "
     "trị viên toàn quyền vẫn không thấy nút nếu không phải người lập"],
    ["4", "Mỗi dòng thiết bị chỉ mang đúng một lỗi",
     "Khi lập phiếu, thiết bị nhiều lỗi đã được tách sẵn thành nhiều dòng nên điều kiện này trên "
     "thực tế chưa từng chặn phiếu nào"],
])

h("5.7. Bước tự động — Báo giá hết hiệu lực", 2)
para(
    "Mỗi báo giá có ô Hiệu lực báo giá tính bằng số ngày kể từ ngày lập. Hằng đêm lúc 00:30, hệ "
    "thống rà các báo giá đang ở trạng thái Duyệt mà đã quá hạn và chuyển sang Hết hiệu lực. Lần "
    "chuyển này ĐƯỢC GHI vào Lịch sử thay đổi kèm ghi chú “Hệ thống tự chuyển khi báo giá quá hạn "
    "hiệu lực”, người thực hiện hiển thị là Hệ thống. Báo giá không đặt số ngày hiệu lực thì được "
    "bỏ qua, không bị coi là hết hạn."
)

h("5.8. Khi cần sửa lại một chứng từ đã gửi", 2)
para(
    "Gửi đi là khoá. Muốn sửa thì phải nhờ trả lại: người lập Phiếu yêu cầu bấm Từ chối tiếp nhận "
    "trên phiếu cung cấp thông tin kèm lý do, phiếu về trạng thái Không duyệt, hai chứng từ phía "
    "trước cùng quay lại Đang CCTT; người lập sửa xong gửi lại. Trường hợp muốn làm lại từ đầu thì "
    "xoá chứng từ: xoá phiếu cung cấp thông tin thì phiếu xử lý quay lại Chờ CCTT và phiếu yêu cầu "
    "quay lại Đã xử lý; xoá báo giá nháp thì phiếu cung cấp thông tin quay lại Chờ làm báo giá. "
    "Xoá chứng từ là xoá cả các dòng thiết bị, dịch vụ, vật tư và chi phí của nó."
)

# ══════════════════════ 6. THÔNG BÁO ══════════════════════
h("6. THÔNG BÁO — AI NHẬN, KHI NÀO, NỘI DUNG GÌ", 1)
table([
    ["Sự kiện", "Ai nhận", "Nội dung", "Bấm vào thì đi đâu"],
    ["Gửi Phiếu yêu cầu đi",
     "TOÀN BỘ nhân viên của phòng tiếp nhận ghi trên phiếu",
     "[YCSCBH] Chờ duyệt: <số phiếu>. Khách hàng: <tên khách hàng>.",
     "Màn chi tiết đúng phiếu yêu cầu đó"],
    ["Phòng tiếp nhận Từ chối phiếu yêu cầu",
     "MỘT người: người lập phiếu yêu cầu",
     "[YCSCBH] Từ chối: <số phiếu>. Lý do: <lý do>",
     "Màn chi tiết đúng phiếu yêu cầu đó"],
    ["Gửi Phiếu xử lý đi (phiếu có phần cần khảo sát)",
     "MỌI người có quyền Tạo phiếu cung cấp thông tin, giới hạn trong CÙNG CÔNG TY với phiếu",
     "[PXL] Chờ duyệt: <số phiếu>. Khách hàng: <tên khách hàng>.",
     "Màn chi tiết đúng phiếu xử lý đó"],
    ["Không duyệt phiếu xử lý",
     "MỘT người: người lập phiếu xử lý",
     "[PXL] Từ chối: <số phiếu>. Lý do: <lý do>",
     "Màn chi tiết đúng phiếu xử lý đó"],
    ["Gửi Phiếu cung cấp thông tin đi (phiếu có phần cần báo giá)",
     "MỘT người: người đã lập PHIẾU YÊU CẦU ở bước 1 — không phải người lập phiếu này",
     "[PCCTT] Chờ duyệt: <số phiếu>. Khách hàng: <tên khách hàng>.",
     "Màn chi tiết đúng phiếu cung cấp thông tin đó"],
    ["Từ chối tiếp nhận phiếu cung cấp thông tin",
     "MỘT người: người lập phiếu cung cấp thông tin",
     "[PCCTT] Từ chối: <số phiếu>. Lý do: <lý do>",
     "Màn chi tiết đúng phiếu cung cấp thông tin đó"],
])

h("6.1. Quy ước chung", 2)
bullet("Thông báo hiện ở chuông trên thanh công cụ; bấm vào mở thẳng đúng chứng từ đó, không về danh sách chung.")
bullet("Nội dung tối đa 120 ký tự. Quá dài thì phần ghi chú (tên khách hàng hoặc lý do) bị cắt bớt, số phiếu luôn được giữ nguyên.")
bullet("Người lập nếu cũng thuộc phòng nhận thông báo thì vẫn nhận thông báo của chính mình — hệ thống gửi theo danh sách phòng, không loại người gửi.")
bullet("Gửi thông báo lỗi KHÔNG làm hỏng nghiệp vụ: chứng từ vẫn lưu và vẫn chuyển trạng thái bình thường.")

h("6.2. Những sự kiện KHÔNG phát sinh thông báo", 2)
bullet("Lưu nháp, sửa chứng từ nháp, xoá chứng từ.")
bullet("Gửi phiếu cung cấp thông tin mà phiếu CHỈ có phần bảo hành (không có dịch vụ sửa chữa và không có thiết bị bảo dưỡng).")
bullet("Gửi lại lần hai một phiếu cung cấp thông tin đã sinh phiếu bảo hành.")
bullet("Sinh Phiếu bảo hành.")
bullet("Toàn bộ màn Báo giá dịch vụ: lưu nháp, duyệt, nhân bản, tự chuyển hết hiệu lực đều KHÔNG gửi thông báo — vì người lập báo giá tự duyệt, không phải chờ ai.")

# ══════════════════════ 7. PHÂN QUYỀN ══════════════════════
h("7. PHÂN QUYỀN", 1)

h("7.1. Nhìn thấy dữ liệu nào", 2)
para(
    "Năm màn dùng chung một cách gác cổng, theo ba mức quyền xem RIÊNG của từng loại chứng từ "
    "(mỗi loại một bộ ba quyền)."
)
table([
    ["Quyền được cấp", "Nhìn thấy"],
    ["Xem … theo tổng công ty", "Toàn bộ chứng từ của mọi công ty"],
    ["Xem … theo công ty", "Chứng từ của công ty mình, cộng chứng từ do chính mình lập"],
    ["Xem … theo phòng ban", "Chứng từ của phòng ban mình quản lý, cộng chứng từ do chính mình lập"],
    ["KHÔNG có quyền nào", "Chỉ chứng từ do chính mình lập"],
])
para("Ba bộ quyền đang dùng, ghi đúng tên như trong hệ thống:")
bullet("Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng công ty / theo công ty / theo phòng ban")
bullet("Xem phiếu cung cấp thông tin theo tổng công ty / theo công ty / theo phòng ban")
bullet("Xem báo giá dịch vụ SC - BH theo tổng công ty / theo công ty / theo phòng ban")
bullet("Xem phiếu bảo hành theo tổng công ty / theo công ty / theo phòng ban")
para(
    "Ngoài ra còn hai quyền thao tác: Xử lý yêu cầu sửa chữa (người có quyền này luôn nhìn thấy "
    "thêm những phiếu yêu cầu gửi về phòng mình, dù không đủ quyền xem theo cấp) và Tạo phiếu cung "
    "cấp thông tin (điều kiện để lập chứng từ bước 3, và là danh sách người nhận thông báo ở bước 2)."
)
para(
    "Hai quy tắc áp cho mọi mức quyền: chứng từ NHÁP của người khác thì không ai xem được, kể cả "
    "quản trị và kể cả khi mở thẳng bằng đường dẫn hay đường in; và cột Giá vốn chỉ hiện với người "
    "có quyền Xem giá vốn hàng hoá — người không có quyền vẫn mở, vẫn sửa, vẫn lưu chứng từ bình "
    "thường mà không làm mất giá vốn đã nhập trước đó."
)

h("7.2. Thao tác nào được phép khi nào", 2)
table([
    ["Thao tác", "Ai được làm", "Điều kiện"],
    ["Sửa / Xoá Phiếu yêu cầu, Phiếu xử lý",
     "Chỉ người lập", "Chứng từ đang ở Đang tạo"],
    ["Sửa / Xoá Phiếu cung cấp thông tin",
     "Chỉ người lập", "Chứng từ đang ở Đang tạo hoặc Không duyệt"],
    ["Sửa / Xoá Báo giá dịch vụ",
     "Chỉ người lập", "Báo giá đang ở Đang tạo. Bấm Lưu và duyệt là khoá"],
    ["Tạo phiếu xử lý yêu cầu", "Phòng tiếp nhận", "Phiếu yêu cầu đang Chờ xử lý"],
    ["Tạo phiếu cung cấp thông tin", "Người có quyền Tạo phiếu cung cấp thông tin",
     "Phiếu xử lý đang Chờ CCTT"],
    ["Tạo báo giá dịch vụ · Từ chối tiếp nhận",
     "Người đã lập Phiếu yêu cầu", "Đủ 4 điều kiện ở mục 5.6"],
    ["Nhân bản báo giá", "Mọi người xem được báo giá đó", "Không có điều kiện trạng thái"],
    ["Sửa / Xoá Phiếu bảo hành", "Không ai", "Phiếu sinh tự động, chỉ để xem, in và xuất dữ liệu"],
])
para(
    "Nút không dùng được thì ẨN HẲN, không hiện dạng chữ mờ. Danh sách nút ở màn chi tiết luôn "
    "khớp với danh sách nút ở màn danh sách của cùng chứng từ đó. Mọi điều kiện trên đều được chặn "
    "ở máy chủ, không chỉ ẩn nút trên màn hình."
)

# ══════════════════════ 8. QUY TẮC BẮT BUỘC ══════════════════════
h("8. QUY TẮC NGHIỆP VỤ BẮT BUỘC", 1)

h("8.1. Bắt buộc nhập — tách theo từng nút bấm", 2)
table([
    ["Nút", "Bắt buộc nhập gì"],
    ["Lưu (nháp)",
     "Rất ít: chứng từ gốc và khách hàng. Cố ý cho lưu nửa chừng để người dùng không mất công đã "
     "nhập khi phải dừng giữa chừng"],
    ["Lưu và gửi / Lưu và duyệt",
     "Đầy đủ theo nghiệp vụ của từng chứng từ. Riêng báo giá bắt buộc có Hiệu lực báo giá (số "
     "ngày). Thiếu thì hệ thống chặn và hiện lỗi ngay dưới ô nhập, không rời trang"],
])
para(
    "Các ô nhập số ngày và số lượng chỉ nhận số nguyên dương; gõ chữ vào bị chặn ngay trên màn và "
    "chặn thêm một lần nữa ở máy chủ, kể cả khi chỉ lưu nháp."
)

h("8.2. Ràng buộc số tiền", 2)
bullet("Chi phí cho SC - BD = Giá trị trừ Cho bảo hành — là ô TỰ TÍNH, không nhập tay.")
bullet("Trả phí = Cho bảo hành trừ Miễn phí; Khách hàng phải trả = Trả phí cộng Chi phí cho SC - BD — đều là ô tự tính.")
bullet("Không cho nhập Cho bảo hành lớn hơn Giá trị, cũng không cho Miễn phí lớn hơn Cho bảo hành.")
bullet("Ba cột Cho bảo hành, Miễn phí, Trả phí CHỈ hiện khi chứng từ có thiết bị bảo hành. Chứng từ thuần sửa chữa thấy bảng gọn hơn, chỉ còn hai ô nhập.")
bullet("Bảng tổng hợp của báo giá KHÔNG cộng phần bảo hành — phần đó khách không trả tiền, đã tách sang phiếu bảo hành.")

h("8.3. Khoá chỉnh sửa", 2)
para(
    "Gửi đi là khoá. Sau khi gửi, chứng từ không sửa và không xoá được nữa; muốn sửa phải nhờ trả "
    "lại (mục 5.8). Không có ngoại lệ cho quản trị viên. Ràng buộc này chặn ở máy chủ: vào thẳng "
    "màn Sửa bằng đường dẫn cũng bị đưa về màn Chi tiết."
)

h("8.4. Danh mục bị khoá", 2)
para(
    "Danh mục đã khoá hoặc ngừng hoạt động không còn xuất hiện trong danh sách chọn của chứng từ "
    "mới, NHƯNG chứng từ cũ đang dùng giá trị đó vẫn hiển thị đúng tên và không mất dữ liệu khi "
    "lưu lại. Giá trị đã khoá được đánh dấu bằng biểu tượng ổ khoá."
)

h("8.5. Sinh mã chứng từ", 2)
para(
    "Mã chứng từ do hệ thống sinh, người dùng không nhập và không sửa. Dạng mã ghép từ mã công ty, "
    "loại chứng từ và số thứ tự theo năm — ví dụ phiếu bảo hành có dạng <MÃ CÔNG TY>.PBH.<năm><số "
    "thứ tự>, báo giá dịch vụ có dạng <MÃ CÔNG TY>.BGDV.<năm><số thứ tự>."
)

h("8.6. Lịch sử thay đổi", 2)
para(
    "Bốn chứng từ (trừ Phiếu bảo hành) đều ghi Lịch sử thay đổi: ai tạo, ai sửa, trường nào đổi từ "
    "giá trị nào sang giá trị nào, và mọi lần chuyển trạng thái. Xem lịch sử ở ngay màn chi tiết "
    "hoặc mở nhanh từ dòng ở màn danh sách. Lần hệ thống tự chuyển báo giá sang Hết hiệu lực cũng "
    "được ghi, với người thực hiện là Hệ thống."
)

# ══════════════════════ 9. LỐI VÀO ══════════════════════
h("9. CÁC LỐI VÀO MÀN HÌNH", 1)
para(
    "Mỗi màn của luồng đều là MỘT màn nhưng có NHIỀU lối vào, khác nhau ở đoạn tham số phía sau "
    "đường dẫn, và mỗi lối vào cho ra một danh sách khác hẳn. Cột cuối là số bản ghi tài khoản "
    "quản trị nhìn thấy, đo ngày 28/08/2026 trên dữ liệu gộp."
)
table([
    ["Bấm vào đâu (phân hệ → nhóm → mục)", "Đường dẫn", "Danh sách hiện ra", "Quản trị thấy"],
    ["Bán hàng → Bán dịch vụ → Yêu cầu sửa chữa - bảo hành",
     "/customer-care/warranty-repair-requests",
     "CHỈ phiếu do chính tôi lập, kể cả phiếu còn nháp", "6"],
    ["CSKH → Kiểm tra bảo hành sửa chữa → Yêu cầu kiểm tra sửa chữa - bảo hành",
     "/customer-care/warranty-repair-requests?type=all",
     "Toàn bộ phiếu trong phạm vi quyền, cộng phiếu gửi về phòng tôi tiếp nhận", "5.371"],
    ["(không có mục menu — link từ màn khác)",
     "/customer-care/warranty-repair-requests?type=waiting_handle",
     "Phiếu Chờ xử lý gửi về đúng phòng tôi — hộp việc của phòng", "0"],
    ["(không có mục menu — đường dẫn trần)",
     "/customer-care/warranty-repair-handle-requests",
     "CHỈ phiếu xử lý do chính tôi lập", "5"],
    ["CSKH → Kiểm tra bảo hành sửa chữa → Phiếu xử lý yêu cầu",
     "/customer-care/warranty-repair-handle-requests?type=all",
     "Toàn bộ phiếu xử lý trong phạm vi quyền", "5.258"],
    ["(không có mục menu)",
     "/customer-care/warranty-repair-handle-requests?type=waiting_information",
     "Phiếu Chờ CCTT — hộp việc của người đi khảo sát", "22"],
    ["(không có mục menu — đường dẫn trần)",
     "/customer-care/wr-information-requests",
     "CHỈ phiếu cung cấp thông tin do chính tôi lập", "1"],
    ["CSKH → Kiểm tra bảo hành sửa chữa → Phiếu cung cấp thông tin làm báo giá",
     "/customer-care/wr-information-requests?permission=all",
     "Toàn bộ phiếu trong phạm vi quyền", "4.980"],
    ["Bán hàng → Bán dịch vụ → Phiếu cung cấp thông tin làm báo giá",
     "/customer-care/wr-information-requests?type=waiting_create_quotation",
     "Phiếu chờ CHÍNH TÔI làm báo giá — đủ 4 điều kiện ở mục 5.6", "0"],
    ["(không có mục menu — đường dẫn trần)",
     "/customer-care/wr-quotations", "CHỈ báo giá do chính tôi lập", "0"],
    ["Bán hàng → Bán dịch vụ → Danh sách báo giá",
     "/customer-care/wr-quotations?type=all",
     "Toàn bộ báo giá trong phạm vi quyền", "3.585"],
    ["(không có mục menu — đường dẫn trần)",
     "/customer-care/wr-warranties", "CHỈ phiếu bảo hành do chính tôi lập", "0"],
    ["CSKH → Kiểm tra bảo hành sửa chữa → Phiếu bảo hành",
     "/customer-care/wr-warranties?type=all",
     "Toàn bộ phiếu bảo hành trong phạm vi quyền", "3.631"],
])
para("Ba điều hay hiểu nhầm nhất về lối vào:")
bullet("Đường dẫn quyết định PHẠM VI XEM, không cấp quyền. Người không có quyền xem theo cấp nào mà mở link “xem tất cả” thì vẫn chỉ thấy chứng từ của chính mình.")
bullet("Nút Làm mới chỉ xoá các điều kiện lọc đang áp dụng, KHÔNG đưa người dùng sang phạm vi khác. Muốn đổi phạm vi thì bấm lại mục menu tương ứng.")
bullet("Link kèm giá trị lạ thì hệ thống bỏ qua và giữ phạm vi mặc định — không lỗi, cũng không lộ thêm dữ liệu.")
para(
    "Lưu ý thêm: tên tham số không đồng nhất giữa các màn. Phần lớn dùng type, riêng Phiếu cung "
    "cấp thông tin và Báo giá dịch vụ bên hệ thống cũ dùng permission; hệ thống mới nhận cả hai "
    "tên. Và hộp việc rỗng thường chỉ có nghĩa hiện không có việc nào đến lượt bạn, không phải "
    "chức năng hỏng."
)

# ══════════════════════ 10. TRA CỨU, IN, XUẤT ══════════════════════
h("10. TRA CỨU, IN VÀ XUẤT DỮ LIỆU", 1)

h("10.1. Tìm kiếm và bộ lọc", 2)
para(
    "Mỗi màn có một ô tìm nhanh và một bộ lọc mở rộng. Ô tìm nhanh tìm theo số chứng từ, tên và mã "
    "khách hàng, địa chỉ sửa chữa, người tạo. Bộ lọc mở rộng có: trạng thái, khách hàng, người "
    "tạo, công ty – phòng ban, tên hoặc mã hàng hoá, model, serial, khoảng ngày tạo; màn Báo giá "
    "có thêm ô Người duyệt và ô Số phiếu cung cấp thông tin; màn Phiếu cung cấp thông tin và Phiếu "
    "bảo hành có ô Số phiếu cung cấp thông tin. Chọn xong ô lọc là danh sách tự tìm lại, không "
    "phải bấm nút."
)
para(
    "Người dùng tự chọn cột hiển thị và tự sắp xếp theo các cột số chứng từ, khách hàng, ngày tạo, "
    "ngày duyệt, số tiền."
)

h("10.2. In", 2)
table([
    ["Chứng từ", "In được gì"],
    ["Yêu cầu kiểm tra sửa chữa – bảo hành", "In một phiếu · In danh sách theo bộ lọc đang áp dụng"],
    ["Phiếu xử lý yêu cầu", "In một phiếu · In danh sách"],
    ["Phiếu cung cấp thông tin làm báo giá", "In một phiếu · In danh sách"],
    ["Báo giá dịch vụ",
     "In một báo giá theo 3 MẪU khác nhau, chọn trong hộp thoại trước khi in; có tuỳ chọn in kèm "
     "danh mục kiểm tra bảo dưỡng (chỉ hiện khi báo giá có dịch vụ bảo dưỡng) · In danh sách"],
    ["Phiếu bảo hành", "In một phiếu · In danh sách"],
])
para(
    "Bản in luôn hiện trước ở cửa sổ xem trước để người dùng soát rồi mới in. Đầu bản in là "
    "letterhead của ĐÚNG công ty ghi trên chứng từ, không phải công ty của người đang in. Ô Thời "
    "gian trên bản in danh sách ghi “Tất cả” khi không lọc theo ngày."
)

h("10.3. Xuất Excel", 2)
para(
    "Cả năm màn xuất được danh sách ra Excel theo đúng bộ lọc đang áp dụng, và file tích sẵn đúng "
    "những cột đang hiện trên màn. Với danh sách lớn, hệ thống lấy dữ liệu theo từng đợt và hiện "
    "dòng tiến độ để người dùng biết còn bao lâu. Ô số tiền trong file giữ KIỂU SỐ để cộng, lọc và "
    "tạo bảng tổng hợp được ngay; dấu ngăn cách hàng nghìn hiển thị theo thiết lập vùng của máy mở "
    "file. Ô số điện thoại giữ kiểu chuỗi để không mất số 0 ở đầu."
)

# ══════════════════════ 11. LIÊN THÔNG ══════════════════════
h("11. LIÊN THÔNG VỚI HỆ THỐNG KHÁC", 1)
para(
    "Luồng dịch vụ trên hệ thống mới dùng CHUNG cơ sở dữ liệu với hệ thống cũ: chứng từ lập ở bên "
    "nào cũng hiện ở bên kia, và số liệu của hai bên là một. Danh mục dùng chung gồm khách hàng, "
    "hàng hoá, lỗi thiết bị, dịch vụ, đơn vị tính, kho và tồn kho, công ty – phòng ban, nhân viên."
)
para("Những chỗ CỐ Ý làm khác hệ thống cũ:")
table([
    ["Điểm khác", "Hệ thống cũ", "Hệ thống mới", "Lý do"],
    ["Thiết bị nhiều lỗi tách thành nhiều dòng",
     "Các dòng tách ra MẤT SẠCH dịch vụ do đọc nhầm dữ liệu, dẫn tới thiếu tiền dịch vụ trong báo "
     "giá gửi khách",
     "Dòng tách ra giữ đúng dịch vụ của lỗi đó", "Là lỗi kỹ thuật, không phải nghiệp vụ"],
    ["Cột Giá vốn", "Hiện cho mọi người mở được chứng từ",
     "Ẩn hẳn nếu không có quyền Xem giá vốn hàng hoá, và máy chủ không trả về số",
     "Chặn từ máy chủ, không dựa vào việc ẩn trên màn hình"],
    ["Chứng từ nháp của người khác",
     "Danh sách ẩn, nhưng mở thẳng bằng đường dẫn thì quản trị vẫn đọc được",
     "Không ai đọc được, kể cả quản trị và kể cả đường in", "Nháp là việc riêng của người lập"],
    ["Bắt buộc nhập khi Lưu nháp", "Bắt buộc mọi trường ở cả hai nút",
     "Lưu nháp chỉ cần chứng từ gốc và khách hàng", "Nháp phải lưu được nửa chừng"],
    ["Báo giá quá hạn hiệu lực",
     "Đổi hàng loạt, KHÔNG ghi lịch sử — người dùng thấy trạng thái tự nhảy mà không có dòng nào "
     "giải thích",
     "Đi từng chứng từ để ghi lịch sử kèm ghi chú, không đụng tới người cập nhật cuối",
     "Mọi thay đổi trạng thái đều phải truy được vết"],
    ["Tổng tiền khi sửa dòng chi tiết sau lúc lập",
     "Không tính lại tổng, tổng lưu bị sai", "Tính lại tổng mỗi lần lưu",
     "Đã tìm thấy chứng từ lệch thật vì lỗi này"],
    ["Chữ trên nút nhân bản", "Menu ghi “Sao chép”", "“Nhân bản”",
     "Bảng chữ chuẩn dùng chung toàn hệ thống: cùng một hành động mà mỗi phân hệ một chữ thì người "
     "dùng phải học lại ở từng màn"],
])
para(
    "Một ràng buộc vận hành cần nhớ: việc tự chuyển báo giá sang Hết hiệu lực CHỈ được bật ở MỘT "
    "bên. Bật cả hai thì bên nào chạy trước sẽ đổi trạng thái, và nếu bên cũ chạy trước thì bên "
    "mới không kịp ghi lịch sử."
)

# ══════════════════════ 12. GIỚI HẠN ══════════════════════
h("12. GIỚI HẠN HIỆN TẠI", 1)
table([
    ["Hạng mục", "Hiện trạng", "Cách làm tạm"],
    ["Hợp đồng dịch vụ (bước 5)",
     "Chưa có trên hệ thống mới. Đã khảo sát xong và chốt cách làm ngày 28/08/2026, chưa viết mã. "
     "Nút Lập hợp đồng dịch vụ ở màn Báo giá đang ẩn",
     "Lập hợp đồng trên hệ thống cũ; dữ liệu vẫn dùng chung nên hệ thống mới đọc được ngay"],
    ["Lịch sử thay đổi của Phiếu bảo hành",
     "Chưa có (bốn chứng từ còn lại đã có đủ). Bản in và xuất Excel thì đã có",
     "Tra ngược qua lịch sử của phiếu cung cấp thông tin đã sinh ra nó"],
    ["Tạo phiếu giao việc từ Phiếu bảo hành",
     "Chưa có, chờ bước giao việc", "Giao việc trên hệ thống cũ"],
    ["Sáu quyền xem của Báo giá dịch vụ và Phiếu bảo hành",
     "Đã khai nhưng CHƯA nạp vào dữ liệu. Hệ quả đo được: cùng một tài khoản, hệ thống cũ thấy "
     "4.218 báo giá còn hệ thống mới chỉ thấy 3.586 — chênh lệch do quyền, không do cách lọc",
     "Chờ chạy phần nạp quyền, hoặc chốt cho hệ thống mới đọc luôn phân quyền của hệ thống cũ"],
    ["Việc tự chuyển báo giá hết hiệu lực",
     "Chưa chạy thật lần nào. Chạy lần đầu sẽ đổi 116 trong số 121 báo giá đang ở trạng thái Duyệt "
     "— là tồn đọng vì hệ thống mới chưa từng chạy",
     "Chờ chốt thời điểm chạy và tắt việc tương ứng bên hệ thống cũ"],
    ["Một điểm còn chờ chốt về công thức chi phí",
     "Nhập Cho bảo hành vượt Giá trị trong khi Miễn phí đang có số: hệ thống cũ để Trả phí ra số "
     "ÂM, hệ thống mới dọn Miễn phí về 0 nên Trả phí bằng 0",
     "Chờ quyết định giữ cách nào"],
])

# ══════════════════════ BỘ KIỂM THUẬT NGỮ ══════════════════════
OUT = "Mô tả nghiệp vụ - Luồng dịch vụ (5 chứng từ).docx"
doc.save(OUT)

CAM = [
    "controller", "service.php", "entity", "resource", "migration", "endpoint", "api ",
    "json", "null", "boolean", "query", "sql", "select ", "where ", "join ",
    "wr_service", "warranty_repair_", "customer_care", "->", "()", "class ", "function ",
    "http 4", "http 5", "status = ", "type = ", "$this", "laravel", "vue", "component",
]
noi_dung = []
for p_ in doc.paragraphs:
    noi_dung.append(p_.text)
for t_ in doc.tables:
    for row in t_.rows:
        for cell in row.cells:
            noi_dung.append(cell.text)
full = "\n".join(noi_dung).lower()

loi = [tu for tu in CAM if tu in full]
print("Da tao:", OUT)
print("So chuong:", sum(1 for p_ in doc.paragraphs if p_.style.name == "Heading 1"))
print("So bang:", len(doc.tables))
print("Bo kiem thuat ngu:", "SACH" if not loi else "CON LOT: %s" % loi)
