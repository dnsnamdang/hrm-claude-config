---
name: business-flow-documenter
description: Viết tài liệu MÔ TẢ NGHIỆP VỤ (.docx) cho 1 màn/1 luồng — dùng để làm gì, ai tham gia, chạy qua những bước nào, mỗi bước thông báo cho AI, phân quyền và quy tắc bắt buộc. Dùng khi user nói "mô tả nghiệp vụ", "tả nghiệp vụ", "nghiệp vụ chức năng này thế nào", "luồng hoạt động ra sao"
---

# Business Flow Documenter — HRM / ERP TPE

## Mục đích

Sinh tài liệu **Mô tả nghiệp vụ** dạng Word cho một màn hình hoặc một luồng chứng từ. Người đọc là
**người dùng cuối, cán bộ nghiệp vụ, người nghiệm thu và QA** — không phải dev.

Tài liệu phải trả lời trọn 5 câu:
1. Chức năng này **dùng để làm gì**, giải quyết nỗi đau gì?
2. **Ai tham gia**, mỗi vai trò làm gì?
3. **Chạy qua những bước nào**, mỗi bước ai bấm gì, hệ thống làm gì?
4. **Thông báo cho ai** ở từng bước, nội dung ra sao, bấm vào đi đâu?
5. **Quy tắc bắt buộc** nào chi phối (bắt buộc nhập, khóa sửa, phân quyền, sinh mã…)?

## Khi nào dùng

User nói: *"viết mô tả nghiệp vụ"* · *"tả nghiệp vụ cho tôi"* · *"nghiệp vụ phần này thế nào"* ·
*"luồng hoạt động ra sao"* · *"file mô tả nghiệp vụ chi tiết"* · *"dùng để làm gì, thông báo cho ai"*.

## Phân biệt với 3 loại tài liệu khác — ĐỌC TRƯỚC KHI CHỌN SKILL

| Loại | Trả lời câu hỏi | Người đọc | Skill |
| --- | --- | --- | --- |
| **Mô tả nghiệp vụ** | *Vì sao có chức năng này? Luồng chạy thế nào? Ai nhận thông báo?* | Nghiệp vụ, quản lý, QA | **skill này** |
| HDSD | *Tôi phải bấm vào đâu, nhập gì?* — click-by-click + ảnh thật | Người dùng cuối | `hdsd-documenter` |
| SRS | *Hệ thống phải làm được gì?* — đặc tả để nghiệm thu theo từng chức năng | Khách hàng, BA | `srs-documenter` |
| Test case | *Kiểm thử thế nào để biết đúng/sai?* | QA | `testcase-documenter` |

Cùng một màn có thể có cả 4 file. Mô tả nghiệp vụ **không** đi sâu từng nút bấm (đó là việc của
HDSD) và **không** liệt kê đặc tả từng trường (đó là việc của SRS).

---

## ⚠️ NGUYÊN TẮC SỐ 1 — NGÔN NGỮ NGHIỆP VỤ, KHÔNG PHẢI NGÔN NGỮ CODE

Áp dụng y hệt `testcase-documenter`. **Tuyệt đối không** viết vào tài liệu: tên bảng/cột dữ liệu,
id quyền, tên hàm/class/file, đường dẫn kỹ thuật, mã lỗi kỹ thuật, tên tham số.

| Thay vì | Viết là |
| --- | --- |
| "trạng thái = 2" | "trạng thái **Chờ xử lý**" |
| "hệ thống trả 423" | "hệ thống chặn, báo phiếu đã gửi đi nên không sửa được" |
| "gửi thông báo qua hàng đợi" | "hệ thống gửi thông báo qua chuông thông báo trên thanh công cụ" |
| "bảng con bị xóa cascade" | "xóa phiếu là xóa cả các dòng thiết bị của phiếu" |

**Được giữ**: tên quyền nguyên văn tiếng Việt (copy đúng `PermissionsTableSeeder`), tên nhãn/nút
đúng như hiển thị trên màn hình, tên trạng thái đúng như badge.

Gắn bộ kiểm tra tự động vào cuối generator (copy từ `tc_engine.check_terms`) và đọc kết quả trước
khi báo xong.

---

## Cấu trúc bắt buộc — 12 chương

Bám đúng thứ tự này; chương nào không áp dụng thì vẫn giữ tiêu đề + 1 dòng "Không áp dụng vì …".

| # | Chương | Nội dung bắt buộc |
| --- | --- | --- |
| 1 | TÀI LIỆU NÀY DÀNH CHO AI | 1 đoạn + gạch đầu dòng các nhóm người đọc |
| 2 | CHỨC NĂNG NÀY DÙNG ĐỂ LÀM GÌ | 2.1 Mục đích · 2.2 Vị trí trong luồng lớn · 2.3 Giá trị mang lại |
| 3 | NHỮNG AI THAM GIA | **Bảng** vai trò → làm gì. Nêu cả vai trò không thao tác (khách hàng) |
| 4 | VÒNG ĐỜI CỦA PHIẾU / BẢN GHI | **Bảng** trạng thái → ý nghĩa → **ai làm nó chuyển sang trạng thái đó**. Ghi rõ trạng thái nào do màn này tạo ra, trạng thái nào do chứng từ khác cập nhật ngược về |
| 5 | LUỒNG HOẠT ĐỘNG CHI TIẾT | Chia 5.1, 5.2… theo BƯỚC nghiệp vụ, không theo màn hình. Bước có nhiều nhánh → **bảng** hướng xử lý → diễn ra thế nào → kết quả |
| 6 | THÔNG BÁO — AI NHẬN, KHI NÀO, NỘI DUNG GÌ | **Bắt buộc có bảng 4 cột**: Sự kiện · Ai nhận · Nội dung · Bấm vào thì đi đâu. Xem mục "Chương 6" bên dưới |
| 7 | PHÂN QUYỀN | 7.1 Bảng quyền → nhìn thấy dữ liệu nào (kể cả trường hợp KHÔNG có quyền nào) · 7.2 Bảng thao tác → điều kiện được phép |
| 8 | QUY TẮC NGHIỆP VỤ BẮT BUỘC | Bắt buộc nhập (tách theo từng nút bấm) · ràng buộc dữ liệu · khóa chỉnh sửa · danh mục bị khóa · quy tắc sinh mã |
| 9 | **CÁC LỐI VÀO MÀN HÌNH** | **Bảng 3 cột**: Vào bằng · Danh sách hiện ra · Dùng khi nào. Xem mục "Chương 9" bên dưới |
| 10 | TRA CỨU, IN VÀ XUẤT DỮ LIỆU | Tìm nhanh tìm được theo gì · bộ lọc có gì · in cái gì · xuất được gì |
| 11 | LIÊN THÔNG VỚI HỆ THỐNG KHÁC | Dùng chung dữ liệu với ERP/phân hệ nào; **bảng** các điểm cố ý làm khác: Điểm khác · Bên cũ · Bên mới · Lý do |
| 12 | GIỚI HẠN HIỆN TẠI | Cái gì chưa có, workaround tạm, khi nào bỏ |

## Chương 9 — CÁC LỐI VÀO MÀN HÌNH (chốt 2026-08-26)

Rất nhiều màn của ERP có **một đường dẫn nhưng nhiều mục menu trỏ vào**, khác nhau ở query string,
và mỗi lối vào cho ra một danh sách khác hẳn. Người nghiệm thu mở đúng một link rồi kết luận "màn
này thiếu dữ liệu" là chuyện đã xảy ra — nên tài liệu PHẢI liệt kê đủ.

Bảng bắt buộc 3 cột:

| Vào bằng | Danh sách hiện ra | Dùng khi nào |
| --- | --- | --- |
| (không kèm gì) | Chỉ phiếu do chính tôi lập | Xem lại việc của mình, kể cả phiếu còn nháp |
| `?type=all` | Toàn bộ phiếu trong phạm vi quyền của tôi | Lối vào chính từ menu |
| `?type=waiting_handle` | Phiếu đang Chờ xử lý gửi về đúng phòng tôi | Danh sách việc phòng tôi phải làm |

Kèm theo bảng, luôn ghi 3 câu này (người đọc hay hiểu nhầm đúng 3 chỗ đó):

- Đường dẫn quyết định **phạm vi xem**, KHÔNG phải quyền — người không có quyền xem theo cấp mà mở
  link "xem tất cả" thì vẫn chỉ thấy phiếu của chính mình.
- Nút **Làm mới** chỉ xoá điều kiện lọc, không đưa người dùng sang phạm vi khác.
- Link kèm giá trị lạ thì hệ thống bỏ qua, giữ phạm vi mặc định.

Lấy danh sách lối vào ở đâu: các mục menu của ERP (`resources/views/layouts/topmenubar.blade.php`)
và các nhánh `if ($request->type == ...)` trong `searchByFilter()` của model tương ứng. ⚠️ Tên tham
số KHÔNG đồng nhất giữa các màn — phần lớn là `type`, riêng màn Báo giá dịch vụ là `permission`.

## Chương 6 — phần hay bị viết hời hợt nhất

User hỏi *"thông báo cho ai?"* là hỏi **danh sách người nhận cụ thể**, không phải "hệ thống có gửi
thông báo". Bảng phải trả lời được từng ô:

- **Ai nhận**: nói rõ *toàn bộ nhân viên phòng X* hay *chỉ trưởng phòng* hay *người lập phiếu*.
  Đây là chỗ sai nhiều nhất — phải đọc code gửi thông báo để biết nó lấy danh sách người nhận theo
  phòng ban, theo vai trò hay theo một người cụ thể.
- **Nội dung**: chép đúng khuôn chữ người nhận sẽ thấy, kể cả tiền tố trong ngoặc vuông.
- **Bấm vào thì đi đâu**: màn nào, có mở đúng bản ghi đó không.

Sau bảng, thêm phần "Quy ước chung" nêu: phần nào bị cắt khi nội dung quá dài · trường hợp người
lập trùng phòng nhận thì có tự nhận thông báo của chính mình không · lỗi gửi thông báo có làm hỏng
nghiệp vụ không · sự kiện nào **không** phát sinh thông báo (cũng phải nói rõ, tránh QA báo thiếu).

---

## Cách thu thập dữ liệu (đọc code, đừng đoán)

| Cần gì | Đọc ở đâu |
| --- | --- |
| Danh sách trạng thái + ý nghĩa | Hằng số trạng thái trên Entity |
| Ai chuyển trạng thái | Service + Controller của từng thao tác |
| Điều kiện hiện/ẩn nút | Các accessor `is_can_*` của Entity |
| **Người nhận thông báo** | Lớp Notifier/Helper gửi thông báo — xem nó lấy danh sách người nhận theo gì |
| Nội dung thông báo | Hàm dựng nội dung trong Notifier + `.claude/skills/notification-convention/SKILL.md` |
| Bắt buộc nhập theo trạng thái | FormRequest |
| Tên quyền | `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` |
| Nhãn/nút/chữ đúng như user thấy | Mở màn thật trên cổng dev (Playwright) — **đừng lấy tên field trong code** |
| Khác biệt với ERP | So với code ERP tương ứng; nếu feature là port màn thì lấy từ `plan.md` mục "Khác biệt có chủ đích" |

---

## Generator

Viết bằng `python-docx` thuần — **không dùng khung có mục lục tự động** như `hdsd-documenter`:
khung đó cần Word thật để cập nhật mục lục, chạy trên máy không có Word là gãy.

Mẫu đầy đủ: `.claude/skills/business-flow-documenter/assets/gen_mota_mau.py`
(bản dựng thật để đối chiếu: `.plans/gop-db/warranty-repair-request/gen_mo_ta_nghiep_vu.py`).

```python
doc = Document()
doc.styles["Normal"].font.name = "Times New Roman"
doc.styles["Normal"].font.size = Pt(12)

def h(text, level):  doc.add_paragraph(text, style="Heading %d" % level)
def para(text):      p = doc.add_paragraph(); p.alignment = JUSTIFY; p.add_run(text)
def bullet(text):    doc.add_paragraph(text, style="List Bullet")
def table(rows):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Light Grid Accent 1"; t.alignment = 1
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            t.cell(i, j).text = val
```

Quy ước:
- Bìa: tiêu đề "MÔ TẢ NGHIỆP VỤ" 20pt đậm + tên màn 16pt đậm + dòng "Phân hệ … · Cập nhật ngày
  dd/mm/yyyy", đều canh giữa, rồi `add_page_break()`.
- Chỉ dùng `Heading 1/2` và `List Bullet` của template, **không ép font/size cho thân bài**.
- Bảng luôn dùng style `Light Grid Accent 1`, dòng đầu là dòng tiêu đề.
- Lưu tại `.plans/[feature]/Mô tả nghiệp vụ - <Tên màn>.docx`; script để cùng thư mục, tên
  `gen_mo_ta_nghiep_vu.py`.
- Một feature nhiều màn → mỗi màn một file, đừng gộp.
- Kiểm lại trước khi giao: `soffice --headless --convert-to pdf` rồi đọc vài trang xem có vỡ bảng,
  lọt thuật ngữ kỹ thuật hay thiếu chương nào không.

⚠️ Đầu file luôn có:
```python
import sys
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
```

---

## Checklist trước khi báo xong

- [ ] Đủ **12 chương**, không bỏ chương nào
- [ ] Chương 4 nói rõ **ai** làm bản ghi chuyển sang từng trạng thái
- [ ] Chương 5 chia theo **bước nghiệp vụ**, nhánh rẽ có bảng "hướng xử lý → kết quả"
- [ ] Chương 6 có **bảng 4 cột** và nói rõ *toàn bộ nhân viên phòng* hay *một người*
- [ ] Chương 6 có phần quy ước chung + nêu sự kiện **không** gửi thông báo
- [ ] **Chương 9 liệt kê ĐỦ mọi lối vào** (đếm từ menu ERP + các nhánh `type`/`permission`), kèm 3 câu lưu ý
- [ ] Chương 7 có cả trường hợp **không có quyền nào**
- [ ] Chương 8 tách bắt buộc nhập **theo từng nút bấm** (lưu nháp vs gửi đi)
- [ ] Chương 10 có bảng khác biệt kèm **lý do**, không chỉ liệt kê
- [ ] Chương 11 nêu giới hạn thật, không giấu
- [ ] Bộ kiểm tra thuật ngữ in "sạch"
- [ ] Tên trạng thái / nút / nhãn **khớp màn thật** (đã mở màn kiểm chứng)
- [ ] Đã xuất PDF soát lại bố cục

## Không được

- Không mô tả nghiệp vụ bằng cách kể lại code ("gọi hàm X rồi cập nhật cột Y")
- Không viết "hệ thống gửi thông báo" mà không nói **cho ai**
- Không bỏ chương Giới hạn hiện tại để tài liệu trông đẹp
- Không tự suy diễn nghiệp vụ khi code không nói rõ — hỏi lại user rồi mới viết
- Không trộn click-by-click của HDSD vào đây
