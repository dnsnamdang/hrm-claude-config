---
name: srs-documenter
description: Generate tài liệu SRS cho feature/màn hình đã triển khai hoặc sắp triển khai, theo FORM CHUẨN của team (file .docx)
---

# SRS Documenter — HRM / ERP TPE

## Mục đích

Generate tài liệu SRS (Software Requirements Specification) cho **một màn hình** đã triển khai
hoặc sắp triển khai, dựa trên code thực tế + design document + business rules.

## Khi nào dùng

- Màn hình đã code xong, cần tài liệu SRS để bàn giao / nghiệm thu / lưu trữ
- Cần SRS trước khi code để align với stakeholder
- BA / PM yêu cầu tài liệu đặc tả cho màn hình

---

## ⚠️ FORM CHUẨN — ĐỌC TRƯỚC KHI VIẾT

**File mẫu bắt buộc — đóng gói trong skill:** `.claude/skills/srs-documenter/assets/SRS_MAU.docx`

> **Bản mẫu ĐÃ ĐỔI lần 2 ngày 2026-08-28.** Bản mẫu hiện hành là **"SRS - Phiếu đề nghị thu tiền"**
> (user chốt) — chính là file đã đóng gói ở `assets/SRS_MAU.docx`. Bản mẫu cũ là
> "SRS - Danh mục khách hàng" (form 2026-08-17) — **không dùng nữa**, cần thì lấy lại bằng
> `git show 4be4678:hrm/.claude/skills/srs-documenter/assets/SRS_MAU.docx`.
> So với form 2026-08-17 có **4 điểm khác**, xem mục "4 điểm của form 2026-08-28" bên dưới.

**Generator sinh ra bản mẫu này** (copy về sửa là nhanh nhất, đủ 12 chức năng đủ kiểu — danh sách,
lọc, form thêm/sửa, popup chọn dữ liệu, chi tiết, hộp xác nhận, in, lịch sử):
`.plans/gop-db/finance-bill-income-request/gen_srs.py`

Form này bám theo bản QA gửi ("SRS - Danh mục quốc gia":
https://docs.google.com/document/d/1tKvOQqJyK0bJC6BrZGM92974irpDAsFn/edit — đọc bằng MCP Google
Drive `read_file_content`, **đừng** tải base64 về vì file 5MB), khác một điểm có chủ đích:
bản QA để trống phân quyền vì màn đó chưa chốt quyền, còn form của team **giữ quyền thật**
(Q1…Qn + V1…Vn + ma trận ✅/❌ theo `PermissionsTableSeeder`).

Trước khi sinh SRS, **luôn đọc lại file mẫu** để bám đúng khung và cách hành văn:

```bash
python -c "
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def txt(el): return ''.join(t.text or '' for t in el.iter(W+'t')).strip()
d=Document(r'.claude/skills/srs-documenter/assets/SRS_MAU.docx')
def blocks(doc):
    for c in doc.element.body.iterchildren():
        if c.tag==qn('w:p'): yield Paragraph(c,doc)
        elif c.tag==qn('w:tbl'): yield Table(c,doc)
for b in blocks(d):
    if isinstance(b,Paragraph):
        if txt(b._p): print('[%s] %s'%(b.style.name,txt(b._p)))
    else:
        print('  >>> TABLE %dx%d'%(len(b.rows),len(b.columns)))
        for r in b.rows[:3]: print('     |',' | '.join(txt(c._tc)[:50] for c in r.cells))
"
```

⚠️ Script trên duyệt `w:t` chứ không dùng `cell.text`, vì **file .docx tải từ Google Docs**
(như bản QA gửi) bọc chữ trong ô bảng vào `<w:sdt>` — `cell.text` sẽ đọc ra **rỗng**, mất hết
✅/❌ của ma trận phân quyền. `assets/SRS_MAU.docx` hiện tại do python-docx sinh nên không dính
lỗi này, nhưng cứ dùng script trên cho an toàn với mọi file mẫu.

**KHÔNG dùng template markdown/HTML tự chế.** Form của team là chuẩn duy nhất.

---

## 4 điểm của form 2026-08-28 — thiếu 1 trong 4 là bị trả về

| # | Điểm | Làm thế nào |
|---|---|---|
| 1 | Mục Layout ghi **đường dẫn MENU**, KHÔNG ghi URL | `d.layout(menu=MENU + ' => Tạo mới', shot=…)` |
| 2 | Đầu **mỗi** mục "Giới thiệu" có đoạn trỏ sang SRS quy tắc chung | `d.rule_ref('- Màn Danh sách, …', anchor='list')` |
| 3 | **Phần 4** là BẢNG 5 cột, chỉ ghi quy tắc đặc thù | `d.rule_table([...])` |
| 4 | Sơ đồ tổng quan **có phân cấp** «include»/«extend» | `d.overview_figure2(actors, mains, subs, caption)` |

Điểm 4 là lỗi user đã trả tài liệu về ngày 2026-08-28: sơ đồ cũ vẽ **mọi** chức năng thành
ellipse ngang hàng rồi nối thẳng tới actor, trong khi "Tìm kiếm và lọc", "Tuỳ chỉnh cột", "Xóa"
là thao tác **ngay trên màn danh sách**, "In / Lịch sử / Duyệt" là thao tác **trên màn chi tiết**,
popup chọn dữ liệu là **«include» của form thêm/sửa**. Xem mục "Sơ đồ tổng quan" bên dưới.

---

## Cấu trúc SRS chuẩn — 4 CHƯƠNG

```
SOFTWARE REQUIREMENTS SPECIFICATION (SRS)   ← đoạn thường, CĂN GIỮA, 24pt (KHÔNG phải Heading)
Màn hình: <Tên màn hình>                    ← đoạn thường, CĂN GIỮA, 24pt

Mục lục                                     [Heading 2] + trường TOC của Word

Phần 1. Giới thiệu                          [Heading 1]
   1 Mục đích                — 1 câu dẫn + gạch đầu dòng
   2 Thuật ngữ và viết tắt   — BẢNG 2 cột (Thuật ngữ | Mô tả)

Phần 2. Phân quyền                          [Heading 1]
   1 Danh sách quyền
       "Nhóm quyền thao tác:"                 BẢNG (Ký hiệu | Tên quyền | Tác dụng trên màn hình)
       "Nhóm quyền quyết định phạm vi dữ liệu:" BẢNG (Ký hiệu | Tên quyền | Phạm vi dữ liệu)
                                              ← chỉ thêm bảng 2 khi màn CÓ phân quyền theo cấp
   2 Ma trận phân quyền      — BẢNG (Chức năng | Q1..Qn | Không có quyền nào), dùng ✅ / ❌

Phần 3. Đặc tả chi tiết theo từng chức năng  [Heading 1]
   1 Sơ đồ UML tổng quan     — ẢNH use case tổng quan (6.3 inch)
   2 Đặc tả chi tiết từng chức năng
   2.1 <Chức năng 1>  …  2.N <Chức năng N>    [Heading 3]

Phần 4. Quy tắc nghiệp vụ                    [Heading 1]
   "Quy tắc áp dụng: …" + BẢNG 5 cột
   (STT | Mã quy tắc | Tên quy tắc | Mô tả | Phạm vi áp dụng)
```

> Mỗi mục "2.x Giới thiệu" mở đầu bằng 1 đoạn:
> *"Quy tắc chung: Áp dụng SRS Các quy tắc chung [SRS_Các quy tắc chung_VN_1.0] – Màn Danh sách,
> Phân trang… Chỉ bổ sung các quy tắc riêng của <màn> tại phần mô tả chi tiết."*
> → dùng `d.rule_ref()`; anchor lấy **nguyên** từ `ANCHOR` trong `srs_docx_lib.py`,
> **không tự bịa** anchor mới.

### ĐÃ BỎ so với form cũ — đừng viết lại

| Mục cũ | Trạng thái |
|---|---|
| Dòng `Phân hệ: <X> – nhóm <Y>` ở trang đầu | **Bỏ** |
| Bảng thông tin trang bìa (Mã màn hình / Phiên bản / Ngày lập / Người lập / Trạng thái tài liệu / Nguồn đối chiếu) | **Bỏ** |
| `1.2 Phạm vi` (+ "Ngoài phạm vi") | **Bỏ** |
| Cả chương `2. Tổng quan` (Bối cảnh nghiệp vụ, Nhóm người dùng) | **Bỏ** |
| `3.2 Quy tắc truy cập bắt buộc` | **Bỏ** |
| Cả chương `4. Danh mục chức năng (Function list)` — bảng ID / Mini-Spec | **Bỏ** |
| Mục con `Tiêu chí nghiệm thu` của từng chức năng | **Bỏ** |
| Dòng `Chức năng liên quan: FR-xx …` cuối mỗi BR | **Bỏ** |
| Dòng `Route (FE): …` ở mục Layout | **Bỏ** |
| Dòng `URL đầy đủ: …` ở mục Layout | **Bỏ từ 2026-08-28** — thay bằng `Menu: <đường dẫn menu>` |
| Phần 4 dạng `BR-0N — <tên>` + gạch đầu dòng | **Bỏ từ 2026-08-28** — thay bằng bảng 5 cột |

> **Đánh số phải liên tục** — chương chạy `Phần 1 → Phần 4`, mục con của mỗi chức năng chạy
> `2.x.1 → 2.x.5` (hoặc `2.x.1 → 2.x.4` khi bỏ Biểu đồ Usecase). Bản mẫu từng sót lỗi đánh số
> sau lần cắt gọt (chương cuối ghi "Phần 6", mục 2.1 nhảy `2.1.3 → 2.1.5`, mục 2.5 ghi `2.3/2.4/2.5`,
> mục 2.10 và 2.12 ghi `.6` thay vì `.5`) — **đã sửa hết ngày 2026-08-17**. Sinh xong nhớ tự rà lại.

### Mỗi chức năng ở 2.x có 5 mục con CỐ ĐỊNH

| Thứ tự | Mục con | Nội dung |
|---|---|---|
| 2.x.1 | Biểu đồ Usecase | **Ảnh PNG** (xem mục "Sinh ảnh biểu đồ Use Case") |
| 2.x.2 | Giới thiệu | Bảng 2 cột × 7–8 dòng (xem dưới) |
| 2.x.3 | Layout màn hình | **Đường dẫn MENU + ẢNH CHỤP THẬT** của chức năng |
| 2.x.4 | Mô tả chi tiết giao diện | Bảng 6/7/8 cột (xem dưới) |
| 2.x.5 | Danh sách event và xử lý event | Bảng 4 cột (xem dưới) |

> Chức năng KHÔNG có tương tác riêng (Xem danh sách, Tìm kiếm & lọc, Xem chi tiết, Lịch sử)
> thì **bỏ mục "Biểu đồ Usecase"** và **lùi số các mục con lại 1 bậc** — bản mẫu làm vậy.
>
> Tiêu đề mục 2.x là **tên chức năng thuần**, KHÔNG gắn mã: `2.5 Tạo mới khách hàng`
> (form cũ ghi `5.2.5 FR-05 — Tạo mới khách hàng`). Mã `FR-xx` chỉ còn dùng ở ma trận phân quyền.

---

## 3 BẢNG BẮT BUỘC — đúng số cột, đúng tên cột

### Bảng "Giới thiệu" — 2 cột × 7–8 dòng

| Mục | Nội dung |
|---|---|
| Tên chức năng | |
| Mô tả | |
| Tác nhân | `<Vai trò nghiệp vụ>; Người dùng đã đăng nhập` |
| Điều kiện ban đầu | |
| Dòng sự kiện chính | Đánh số `1. 2. 3.` mỗi bước 1 dòng |
| Dòng sự kiện phụ | Gạch đầu dòng `•`, mỗi nhánh 1 dòng |
| Yêu cầu đặc biệt | **Bỏ hẳn dòng này** với chức năng chỉ đọc; có nội dung thì mới thêm |

### Bảng "Mô tả chi tiết giao diện" — 8 cột, rút bớt theo loại chức năng

`STT | Tên đối tượng | Loại | Trạng thái | Phạm vi | Bắt buộc | Giá trị ban đầu | Mô tả`

| Loại chức năng | Số cột | Cột bỏ đi |
|---|---|---|
| Có nhập liệu (Tạo mới, Sửa, Import, Xuất, bộ lọc, modal cấu hình) | **8** | — |
| Chỉ đọc (Xem danh sách, Xem chi tiết, Lịch sử) | **7** | `Bắt buộc` |
| Hộp thoại xác nhận (Khóa / Mở khóa, Xóa) | **6** | `Bắt buộc`, `Phạm vi` |

- **Loại**: `Label`, `Text`, `Textbox`, `Textarea`, `Dropdown`, `Datepicker`, `Number`, `Badge`,
  `Button`, `Icon Button`, `Table/Grid`, `Modal`, `Pagination`, `Toast / Alert`, `Loading`
- **Trạng thái**: `Enable`, `Disable`, `Read-only`, `Enable / Ẩn`, `Enable / Disable`, `Hiển thị`
- **Phạm vi**: `0–255 ký tự`, `≥ 0`, `0 – 100`, `dd/mm/yyyy`, `Danh sách`, `Danh sách 5 giá trị`, `–`
- **Bắt buộc**: `Có` / `Không` / `–`, hoặc điều kiện: `Có khi tích “Là khách hãng”`,
  `Có với khách hàng tổ chức`, `Có khi KHÔNG chọn Công ty mẹ`
- **Giá trị ban đầu**: `Trống`, `Ẩn`, `Ẩn khi thiếu quyền`, `Hiển thị`, `Theo dữ liệu`,
  `Theo cấu hình đã lưu`, giá trị mặc định cụ thể
- Liệt kê **đủ mọi phần tử** trên màn: cả nút, cột bảng, phân trang, thông báo lỗi, trạng thái rỗng

### Bảng "Danh sách event và xử lý event" — 4 cột

`STT | Event | Loại event | Xử lý event`

- **Loại event**: `Click`, `Change`, `Keypress`, `Hover`, `System`, `Change / Blur`
- **Xử lý event** của các thao tác ghi phải viết theo **3 cụm**:

```
Before:
– Kiểm tra quyền …
– Nếu không có quyền → hiển thị "Bạn không có quyền thực hiện chức năng này." và dừng xử lý.
During:
– <trường> trống → hiển thị "<thông báo lỗi>"
– <trường> trùng → hiển thị "<thông báo lỗi>"
– Nếu có lỗi validate → không thực hiện bước After.
After:
– <hành động ghi dữ liệu>
– Ghi một dòng lịch sử …
– Hiển thị thông báo "<thông báo thành công>"
```

---

## Layout màn hình — ĐƯỜNG DẪN MENU **+ ẢNH CHỤP THẬT**

Mục **`2.x.3 Layout màn hình` của MỖI chức năng** gồm 2 phần, theo thứ tự:

**1. Đường dẫn — 2 dòng:**
```
Đường dẫn màn hình:
Menu: Phân hệ Tài chính => Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi => Đề nghị thu tiền
```
Chức năng con thì nối thêm vào cuối: `… => Thêm mới`, `… => Sửa`, `… => Xóa`, `… => Lịch sử`,
`… => Xem chi tiết => In phiếu`. Nhãn menu phải **lấy đúng chữ trên giao diện** — tra trong
`components/subsystem-menu/*.js` của hrm-client, đừng tự đặt tên.
Với modal/popup, giữ đường dẫn màn danh sách rồi thêm 1 câu:
*"Modal <Tên> được mở ngay trên màn hình danh sách theo đường dẫn ở trên."*

> Form cũ ghi `Menu:` + `Route (FE):` (trước 2026-08-17) rồi chuyển sang chỉ `URL đầy đủ:`
> (2026-08-17). Từ 2026-08-28 **quay lại ghi menu và bỏ hẳn URL** — `d.layout()` vẫn nuốt
> tham số `route=` / `url=` của generator cũ nên không cần sửa các generator đã có.

**2. Ảnh chụp thật của ĐÚNG chức năng đó**, canh giữa, rộng **6.2 inch**, kèm caption
`Hình N: <mô tả>` (in nghiêng, 9.5pt, canh giữa).

| Chức năng | Ảnh phải chụp |
|---|---|
| Xem danh sách | Toàn màn danh sách lúc mới vào (thấy rõ các cột) |
| Tìm kiếm & lọc | Panel bộ lọc nâng cao ĐANG MỞ |
| Cấu hình (cài đặt bộ lọc, tuỳ chỉnh cột) | Cửa sổ cấu hình đang mở |
| Tạo mới | Form Tạo mới; form rẽ nhánh theo loại → chụp **mỗi nhánh 1 ảnh** |
| Chỉnh sửa | Form Sửa có dữ liệu thật |
| Xem chi tiết | Màn/modal chi tiết ở chế độ chỉ đọc |
| Khóa / Mở khóa, Xóa | Hộp thoại xác nhận |
| Import / Export | Modal chọn file / chọn trường xuất |

**Cách chụp:** Playwright MCP, resize 1440×900, ảnh thật từ hệ thống — **giống hệt quy trình của
`hdsd-documenter` Bước 2**. Làm SRS + HDSD cho cùng một màn thì **chụp 1 lần, dùng chung**
thư mục ảnh `.plans/[feature]/<feature>_shots/`, đừng chụp 2 lần.

**Không được**: vẽ mô phỏng bằng ký tự/bảng, dùng ảnh của màn khác, hay để trống mục Layout.

---

## Sinh ảnh biểu đồ Use Case — BẮT BUỘC LÀ ẢNH THẬT

**TUYỆT ĐỐI KHÔNG vẽ sơ đồ bằng ký tự box-drawing (ASCII art)** — user đã phản hồi "xấu quá".

### Script dùng chung — ĐÓNG GÓI TRONG SKILL

Cả 3 file nằm ở `.claude/skills/srs-documenter/assets/` nên ai clone repo về cũng có:

| File | Vai trò |
|---|---|
| `assets/srs_uml_render.py` | Module vẽ PNG bằng Pillow — `draw_overview2()` (dùng cho tài liệu mới), `draw_usecase()`, `draw_overview()` (bản phẳng cũ, chỉ để chạy lại generator cũ) |
| `assets/srs_docx_lib.py` | Lớp `SrsDoc` dựng file .docx theo form chuẩn |
| `assets/gen_srs_mau.py` | **Khung mẫu form mới**: đủ 4 chương + 1 chức năng chỉ đọc + 1 chức năng ghi. Copy file này rồi thay nội dung là nhanh nhất |

Generator của từng màn đã làm nằm ở `.plans/gop-db/<feature>/gen_srs.py`.
⚠️ Các generator sinh **trước 2026-08-17** đều theo form CŨ (6 chương) — tham khảo cách dùng
API thì được, **đừng chép cấu trúc chương mục**.

Ảnh UML là file **trung gian**, đã nhúng vào .docx nên `srs_docx_lib` ghi chúng vào thư mục tạm
của hệ điều hành — không rải rác vào repo. Muốn giữ lại để xem thì truyền `img_dir='...'`.

Phụ thuộc: `pip install pillow python-docx` (không cần cairosvg / playwright / trình duyệt).

### Cách gọi

```python
import sys, os
sys.path.insert(0, r"<đường dẫn>/.claude/skills/srs-documenter/assets")
from srs_docx_lib import SrsDoc, ACTOR_P1, ACTOR_BOTH

d = SrsDoc(out=OUT, menu='…', route='/duong-dan-man',
           full_url='https://<host-hrm>/duong-dan-man')

d.title_block('<Tên màn hình>')          # 2 dòng căn giữa 24pt — KHÔNG dùng Heading
d.h2('Mục lục'); d.toc()

d.h1('Phần 1. Giới thiệu')

# 1 Sơ đồ UML tổng quan — CÓ PHÂN CẤP (bắt buộc từ 2026-08-28)
d.overview_figure2(
    [('<Actor 1>', [0, 1]), ('<Actor 2>', [0])],       # (actor, chỉ số trong `mains`)
    [('FR-01', 'Xem danh sách', 'view'),               # mains = MÀN HÌNH thật, nối tới actor
     ('FR-05', 'Tạo mới',      'crud')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),   # subs = thao tác trên màn đó
     ('FR-09', 'Chọn dữ liệu từ popup', 'crud', 'include', [1], 'ghi chú (hiện KHÔNG vẽ)')],
    'Sơ đồ Use Case tổng quan màn <Tên màn hình>')

# 2.x.1 Biểu đồ use case của 1 chức năng
d.uc_figure('FR-05', 'Tạo mới <đối tượng>', 'crud',
            [('include', 'Kiểm tra quyền Thêm <đối tượng>'),
             ('extend',  'Sinh mã tự động')],
            caption='Biểu đồ Use Case — FR-05 Tạo mới <đối tượng>')

# Bảng Giới thiệu — chức năng chỉ đọc thì dacbiet=None để BỎ HẲN dòng "Yêu cầu đặc biệt"
d.intro_table(ten=…, mota=…, tacnhan=…, dieukien=…, chinh=…, phu=…, dacbiet=None)

# Đoạn "Quy tắc chung" — đặt NGAY ĐẦU mục Giới thiệu của MỖI chức năng
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')

# Layout — in dòng "Menu: …" + ảnh chụp thật
d.layout(menu=MENU + ' => Tạo mới', shot=shot('02-tao-moi.png'),
         shot_caption='Form Tạo mới <đối tượng>')

# Bảng giao diện — mặc định 8 cột; chức năng chỉ đọc dùng required=False (7 cột);
# hộp thoại xác nhận dùng required=False, scope=False (6 cột)
d.ui_table(rows)
d.ui_table(rows, required=False)
d.ui_table(rows, required=False, scope=False)

d.event_table(rows)

# Phần 4 — bảng 5 cột; mô tả / phạm vi truyền list thì tự nối xuống dòng
d.rule_table([
    ('BR-01', '<Tên quy tắc>', ['– <phát biểu>', '– <ngoại lệ>'], ['Tạo mới', 'Chỉnh sửa']),
])
d.save()
```

### Sơ đồ tổng quan — cái gì vào `mains`, cái gì vào `subs`

| Vào `mains` (nối thẳng tới actor) | Vào `subs` (nối «include»/«extend» vào màn cha) |
|---|---|
| Màn danh sách · màn danh sách chờ duyệt | Tìm kiếm và lọc · Cài đặt bộ lọc · Tuỳ chỉnh cột · Xóa (nút trên dòng) → «extend» màn danh sách |
| Màn thêm mới · màn chỉnh sửa | Popup chọn khách hàng / hợp đồng / sản phẩm → «include» màn thêm mới **và** màn sửa |
| Màn chi tiết | In · Lịch sử · Duyệt / Không duyệt → «extend» màn chi tiết |

Chiều mũi tên (module đã tự xử lý, nhưng phải hiểu để đặt đúng `kind`):
**«include»** cha → con (cha luôn gọi con) · **«extend»** con → cha (con chỉ chạy trong vài tình huống).

**Nhóm màu ellipse:** `view` (xanh dương — xem/lọc/tra cứu) · `crud` (xanh lá — thêm/sửa) ·
`action` (cam — thao tác trạng thái) · `io` (tím — xuất/nhập/in) · `sub` (xám — include/extend).

Ảnh tổng quan chèn ở **6.3 inch**, ảnh từng chức năng và ảnh chụp màn **6.2 inch**.

### 4 bẫy khi render ảnh (đã trả giá)

1. **Xuất ảnh ≥ 1700px** (tổng quan 2000px). Xuất 1350px thì dấu `ụ ị ọ` tiếng Việt **bị mất**
   khi Word thu nhỏ. 1700px @6.2in ≈ 274 DPI là đủ.
2. **Vẽ ở tỷ lệ 3x rồi `resize(..., Image.LANCZOS)`** — không thì viền ellipse răng cưa.
3. **Nhãn «include»/«extend» đặt PHÍA TRÊN đường nối** (offset y ≈ `-24*S`). Đặt giữa đường sẽ
   cắt nét đứt, trông như mũi tên lỗi.
4. **Chừa `top_pad` đủ lớn** cho tiêu đề khung hệ thống, nếu không tiêu đề đè lên ellipse đầu tiên.

Font dùng `C:\Windows\Fonts\segoeui.ttf` / `segoeuib.ttf` / `segoeuii.ttf` — đủ dấu tiếng Việt.

---

## Thiết lập file .docx

**QUY ĐỊNH TRÌNH BÀY — chốt 05/09/2026, áp cho CẢ SRS lẫn HDSD.** `SrsDoc` đã làm sẵn hết,
generator **không được** ép lại font/size/căn lề — cứ dùng `d.h1() / d.h2() / d.p() / d.table()`.

| Thành phần | Quy định |
|---|---|
| Toàn bộ tài liệu | Font **Times New Roman** |
| Heading 1 | **18pt**, **căn giữa**, **bắt đầu từ đầu trang mới** |
| Trang bìa (2 dòng `title_block`) | 24pt đậm căn giữa — **miễn trừ** quy tắc 13pt |
| Văn xuôi, bullet, Heading 2/3 | **13pt** |
| Chữ trong bảng | 10pt (`TABLE_PT`) — giữ nhỏ để bảng 8 cột không vỡ trang |
| Chú thích tên hình ảnh | **căn giữa**, **13pt** nghiêng (`CAPTION_PT`) |

```python
sec = doc.sections[0]
sec.page_width  = Inches(8.5);  sec.page_height = Inches(11)     # Letter, bám bản mẫu
sec.left_margin = Inches(1.25); sec.right_margin = Inches(1.25)

set_font_name(doc.styles['Normal'])                    # Times New Roman, đủ 4 slot rFonts
doc.styles['Normal'].font.size = Pt(BODY_PT)           # 13
for name, size in [('Heading 1', H1_PT), ('Heading 2', BODY_PT), ('Heading 3', BODY_PT)]:
    set_font_name(doc.styles[name])
    doc.styles[name].font.size = Pt(size)
    doc.styles[name].font.color.rgb = RGBColor(0x2F,0x54,0x96)   # xanh navy như bản mẫu
h1 = doc.styles['Heading 1'].paragraph_format
h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
h1.page_break_before = True
```

Bảng dùng `style = 'Table Grid'`, chữ trong bảng `Pt(TABLE_PT)`, dòng tiêu đề in đậm.

### 2 bẫy khi ép Times New Roman (đã trả giá)

1. **Heading trỏ sang FONT THEME.** Style Heading của khung mặc định dùng
   `w:asciiTheme="majorHAnsi"` (= Calibri Light). Còn thuộc tính `*Theme` thì Word **ưu tiên nó
   và xoá `w:ascii`** khi lưu lại ở bước cập nhật mục lục → heading không ra Times New Roman.
   → `set_font_name()` **xoá hết `*Theme`** rồi mới set `w:ascii/hAnsi/eastAsia/cs`.
2. **Style không khai báo font (TOC, Caption, style bảng) rơi về theme.** Sửa style thôi chưa đủ.
   → `save()` gọi `_force_times_new_roman()` ghi thẳng `word/theme/theme1.xml`
   (`majorFont`/`minorFont` → Times New Roman) **sau khi lưu, trước khi cho Word cập nhật field**.

---

## Quy trình generate SRS

### Bước 1: Thu thập thông tin từ code

**BE — đọc theo thứ tự:**
```
1. Migration        → Database schema, data types, constraints
2. Entity/Model     → Relationships, constants (STATUS, TYPE), accessors, điều kiện is_can_*
3. Routes           → API endpoints + middleware checkPermission (nguồn của Phần 2)
4. Request          → Validation rules (nguồn của cột "Phạm vi"/"Bắt buộc" + thông báo lỗi)
5. Controller       → Request flow, response format
6. Service          → Business logic, điều kiện, phép tính (nguồn của Phần 4)
7. Transformer      → Response data structure
8. PermissionsTableSeeder → Tên quyền + group (nguồn của bảng Danh sách quyền)
9. Console Command  → Scheduled jobs, cron logic
```

**FE — đọc theo thứ tự:**
```
1. Page component   → Cột bảng, nút, bộ lọc (nguồn của bảng "Mô tả chi tiết giao diện")
2. Modal component  → Trường nhập, giá trị mặc định, trạng thái enable/disable
3. API calls        → Endpoint + payload
4. Menu (components/subsystem-menu/*.js) → đường dẫn MENU (nguồn của mục "Layout màn hình")
```

### Bước 2: Phân tích & tổng hợp

- Liệt kê **chức năng FR-01…FR-0N** từ route + nút trên màn → đưa vào **ma trận phân quyền**
- Ký hiệu quyền dùng **Q1…Qn** cho nhóm thao tác, **V1…Vn** cho nhóm phạm vi dữ liệu
- Trích **business rules BR-01…** từ service layer (if/else, validate, calculate, điều kiện chặn)
- Lấy **thông báo lỗi** đúng nguyên văn từ Request `messages()` để điền vào cột "Xử lý event"

### Bước 3: Viết script sinh docx

Copy `.claude/skills/srs-documenter/assets/gen_srs_mau.py` sang `.plans/[feature]/gen_srs.py`,
đổi phần nội dung, chạy:

```bash
python .plans/[feature]/gen_srs.py
```

⚠️ Đầu file thêm đoạn sau, nếu không `print()` chuỗi tiếng Việt sẽ ném `UnicodeEncodeError`
(console Windows mặc định cp1252):

```python
import sys
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
```

### Bước 4: Tự kiểm tra trước khi báo xong

```python
from docx import Document
d = Document(OUT)
paras = [x.text for x in d.paragraphs]
print('tables', len(d.tables), 'paragraphs', len(paras))
print('ảnh nhúng:', sum(1 for r in d.part.rels.values() if 'image' in r.reltype))
bad = [t for t in paras if '┌' in t or '○' in t]
print('còn sơ đồ ký tự:', len(bad))    # PHẢI = 0

# form 2026-08-28: 4 điểm bắt buộc
n_fn = sum(1 for t in paras if t.startswith('Menu: '))
print('mục Layout ghi menu:', n_fn)                     # = số chức năng
print('đoạn Quy tắc chung:', sum(1 for t in paras if t.startswith('Quy tắc chung: ')))
print('câu dẫn Phần 4:', sum(1 for t in paras if t.startswith('Quy tắc áp dụng: ')))   # = 1
print('hyperlink:', len([r for r in d.part.rels.values() if r.reltype.endswith('/hyperlink')]))
last = d.tables[-1]                                     # bảng Quy tắc nghiệp vụ
assert [c.text for c in last.rows[0].cells] ==     ['STT', 'Mã quy tắc', 'Tên quy tắc', 'Mô tả', 'Phạm vi áp dụng'], 'Phần 4 chưa là bảng 5 cột'
assert not any('URL đầy đủ' in t for t in paras), 'Còn dòng URL đầy đủ (form cũ)'

# KHÔNG được còn các mục đã bỏ
for s in ['Tổng quan','Mini-Spec','Tiêu chí nghiệm thu','Ngoài phạm vi','Chức năng liên quan',
          'Route (FE)']:
    assert not any(s in t for t in paras), 'Còn mục đã bỏ: %s' % s

# ĐỊNH DẠNG (quy định 05/09/2026) — chạy trên file ĐÃ qua Word cập nhật mục lục
import re, zipfile
h1 = d.styles['Heading 1'].paragraph_format
assert d.styles['Heading 1'].font.size.pt == 18,  'Heading 1 phải 18pt'
assert str(h1.alignment).startswith('CENTER'),    'Heading 1 phải căn giữa'
assert h1.page_break_before is True,              'Heading 1 phải sang trang mới'
assert d.styles['Normal'].font.size.pt == 13,     'Chữ thân bài phải 13pt'
with zipfile.ZipFile(OUT) as z:
    theme = z.read('word/theme/theme1.xml').decode('utf-8')
assert set(re.findall(r'<a:latin typeface="([^"]*)"', theme)[:2]) == {'Times New Roman'},     'Font theme chưa phải Times New Roman'
```

---

## Output

- **File chính:** `.plans/[feature]/SRS - <Tên màn hình>.docx`
  (nhánh `gop_db` → `.plans/gop-db/[feature]/…`)
- **Script sinh:** `.plans/[feature]/gen_srs.py` — đặt cùng thư mục tài liệu để **commit kèm được**,
  nhờ đó tái sinh lại file .docx bất cứ lúc nào.
  ⚠️ KHÔNG để ở `hrm/scripts/` — thư mục đó nằm ngoài mọi git repo nên "commit kèm" là bất khả thi.
- **Ảnh PNG: CHỈ ĐỂ LOCAL, KHÔNG commit.** Ảnh đã nhúng sẵn trong .docx nên người khác không cần
  bản rời; đẩy lên chỉ làm nặng repo. Thư mục ảnh đặt tên `img/` hoặc `*_shots/` — `.gitignore`
  đã chặn sẵn 2 dạng này.
- Trước khi báo xong, chạy `git status`: chỉ được thấy `.docx` và `gen_srs.py`, không được thấy `.png`.

> Bản HTML (`srs.html`) là format CŨ, chỉ giữ cho các feature đã sinh trước 2026-08-07.
> Feature mới chỉ cần bản .docx theo form chuẩn.

---

## Quy tắc viết SRS

### Nguyên tắc chung
- Viết bằng **tiếng Việt**, thuật ngữ kỹ thuật giữ tiếng Anh
- **Viết bằng ngôn ngữ người dùng, không dùng thuật ngữ code** — không nêu tên bảng, tên cột DB,
  tên hàm, mã HTTP. Ví dụ: viết "hệ thống báo dữ liệu đã thay đổi" chứ không viết "trả về 409"
- Mỗi chức năng phải có **Điều kiện ban đầu + Dòng sự kiện chính + Dòng sự kiện phụ**
- Business rules phải **truy vết được** tới code
- Validation rules và **thông báo lỗi** phải khớp **100%** với Request class
- Mọi hành vi KHÁC với màn ERP gốc (nếu là màn port) phải ghi rõ là **chủ đích**

### Nguồn dữ liệu ưu tiên
1. **Code** (migration, entity, request, service, routes, seeder) — nguồn chính xác nhất
2. **design.md** trong `.plans/` — context về quyết định thiết kế
3. **plan.md** trong `.plans/` — scope đã thống nhất
4. **User mô tả** — bổ sung business context mà code không thể hiện

### Không được
- **Không vẽ sơ đồ bằng ký tự** — phải là ảnh PNG
- **Không bỏ ảnh ở mục Layout** — mỗi chức năng BẮT BUỘC có ảnh chụp thật kèm đường dẫn menu
- **Không thêm lại các mục đã bỏ** ở bảng "ĐÃ BỎ" phía trên
- Không dùng template markdown/HTML tự chế thay cho form chuẩn
- Không đổi tên cột của 3 bảng bắt buộc (số cột chỉ được rút theo đúng bảng đã quy định)
- Không đoán response format — đọc transformer/resource
- Không đoán validation rules — đọc Request class
- Không đoán database schema — đọc migration
- Không bỏ sót enum values — đọc constants trong Entity
- Không thêm requirement mà code không có (trừ khi SRS cho feature chưa code)

---

## Bản đã làm theo chuẩn này

| Màn hình | File |
|---|---|
| **Phiếu đề nghị thu tiền (Tài chính)** — BẢN MẪU CHUẨN, = `assets/SRS_MAU.docx` | `.plans/gop-db/finance-bill-income-request/SRS - Phiếu đề nghị thu tiền.docx` |
| Danh mục khách hàng (Giao việc) — form CŨ 2026-08-17 | `.plans/gop-db/customer-docs/SRS - Danh mục khách hàng.docx` |
| Danh mục dịch vụ sửa chữa và chi phí khác (CSKH) — form CŨ | `.plans/gop-db/customer-care-cost-catalog/SRS - Danh mục dịch vụ sửa chữa và chi phí khác.docx` |
