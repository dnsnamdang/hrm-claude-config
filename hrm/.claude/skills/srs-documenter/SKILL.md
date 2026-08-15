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
(bản gốc là `SRS - Lĩnh vực.docx`, màn Danh mục lĩnh vực — đã copy vào repo để ai clone về cũng có).

Trước khi sinh SRS, **luôn đọc lại file mẫu** để bám đúng khung và cách hành văn:

```bash
python -c "
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn
d=Document(r'.claude/skills/srs-documenter/assets/SRS_MAU.docx')
def blocks(doc):
    for c in doc.element.body.iterchildren():
        if c.tag==qn('w:p'): yield Paragraph(c,doc)
        elif c.tag==qn('w:tbl'): yield Table(c,doc)
for b in blocks(d):
    if isinstance(b,Paragraph):
        if b.text.strip(): print('[%s] %s'%(b.style.name,b.text.strip()))
    else:
        print('  >>> TABLE %dx%d'%(len(b.rows),len(b.columns)))
        for r in b.rows[:3]: print('     |',' | '.join(c.text.strip()[:50] for c in r.cells))
"
```

**KHÔNG dùng template markdown/HTML tự chế.** Form của team là chuẩn duy nhất.

---

## Cấu trúc SRS chuẩn (6 chương)

```
SOFTWARE REQUIREMENTS SPECIFICATION (SRS)      [Heading 1]
  Màn hình: <Tên màn hình>                     [Heading 2]
  Phân hệ: <Tên phân hệ> – nhóm <Tên nhóm menu>[Heading 2]
  (bảng thông tin: Mã màn hình / Đường dẫn / Phiên bản / Ngày lập / Người lập /
   Trạng thái tài liệu / Nguồn đối chiếu)

1. Giới thiệu
   1.1 Mục đích              — gạch đầu dòng, nêu SRS này nhằm gì
   1.2 Phạm vi               — "Màn hình … cung cấp chức năng:" + "Ngoài phạm vi:"
   1.3 Thuật ngữ và viết tắt — BẢNG 2 cột (Thuật ngữ | Mô tả), có cả P1/P2/SRS

2. Tổng quan
   2.1 Bối cảnh nghiệp vụ    — "… dùng để:" + "Do đó cần:"
   2.2 Nhóm người dùng       — liệt kê theo P1 / P2 / không có quyền

3. Phân quyền và kiểm soát truy cập
   3.1 Danh sách quyền       — BẢNG (Ký hiệu | Tên quyền | Mã quyền | Nhóm quyền)
   3.2 Quy tắc truy cập bắt buộc
   3.3 Ma trận phân quyền    — BẢNG (Chức năng | P1 | P2 | Không có quyền), dùng ✅ / ❌

4. Danh mục chức năng (Function list)
   BẢNG (ID | Chức năng | Mô tả đặc tả thu nhỏ (Mini-Spec) | Quyền), ID dạng FR-01, FR-02…

5. Đặc tả chi tiết theo từng chức năng (FUNCTIONAL PACKAGING)
   5.1 Sơ đồ UML tổng quan   — ẢNH use case tổng quan
   5.2 Đặc tả chi tiết từng chức năng
   5.2.1 <Chức năng 1>  … 5.2.N <Chức năng N>

6. Quy tắc nghiệp vụ (Business Rules)
   BR-01, BR-02… mỗi rule 1 đoạn tiêu đề + gạch đầu dòng
   Cuối chương: dòng "Chức năng liên quan: FR-xx …"
```

### Mỗi chức năng ở 5.2.x có 6 mục con CỐ ĐỊNH

| Thứ tự | Mục con | Nội dung |
|---|---|---|
| 5.2.x.1 | Biểu đồ Usecase | **Ảnh PNG** (xem mục "Sinh ảnh biểu đồ Use Case") |
| 5.2.x.2 | Giới thiệu | Bảng 8 dòng (xem dưới) |
| 5.2.x.3 | Layout màn hình | **Đường dẫn vào màn + ẢNH CHỤP THẬT** của chức năng (đổi 2026-08-13) |
| 5.2.x.4 | Mô tả chi tiết giao diện | Bảng 8 cột (xem dưới) |
| 5.2.x.5 | Tiêu chí nghiệm thu | Gạch đầu dòng, nhóm theo vai trò/tình huống |
| 5.2.x.6 | Danh sách event và xử lý event | Bảng 4 cột (xem dưới) |

> Chức năng KHÔNG có tương tác riêng (vd Xem danh sách, Tìm kiếm, Xuất Excel) thì **bỏ mục
> "Biểu đồ Usecase"** — bản mẫu cũng làm vậy. Đánh số các mục con lùi lại 1 bậc.

---

## 3 BẢNG BẮT BUỘC — đúng số cột, đúng tên cột

### Bảng "Giới thiệu" — 2 cột × 8 dòng

| Mục | Nội dung |
|---|---|
| Tên chức năng | |
| Mô tả | |
| Tác nhân | `Admin; User được phân quyền …` |
| Điều kiện ban đầu | |
| Dòng sự kiện chính | Đánh số `1. 2. 3.` mỗi bước 1 dòng |
| Dòng sự kiện phụ | Gạch đầu dòng `•`, mỗi nhánh 1 dòng |
| Yêu cầu đặc biệt | Để trống nếu không có |

### Bảng "Mô tả chi tiết giao diện" — 8 cột

`STT | Tên đối tượng | Loại | Trạng thái | Phạm vi | Bắt buộc | Giá trị ban đầu | Mô tả`

- **Loại**: `Label`, `Text`, `Textbox`, `Textarea`, `Dropdown`, `Datepicker`, `Number`, `Badge`,
  `Button`, `Icon Button`, `Table/Grid`, `Modal`, `Pagination`, `Toast / Alert`, `Loading`
- **Trạng thái**: `Enable`, `Disable`, `Read-only`, `Enable / Ẩn`, `Hiển thị`
- **Phạm vi**: `0–255 ký tự`, `≥ 0`, `0 – 100`, `dd/mm/yyyy`, `Danh sách`, hoặc `–`
- **Bắt buộc**: `Có` / `Không` / `–`
- **Giá trị ban đầu**: `Trống`, `Ngầm định trống`, `Lấy từ hệ thống`, `Ẩn`, giá trị mặc định cụ thể
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
– Hiển thị thông báo "<thông báo thành công>"
```

---

## Layout màn hình — ĐƯỜNG DẪN **+ ẢNH CHỤP THẬT** (đổi 2026-08-13)

> ⚠️ **Quy ước ĐÃ THAY ĐỔI — đọc kỹ, đừng làm theo bản cũ.**
> - 2026-08-07: từng chốt BỎ ảnh, mục Layout chỉ ghi đường dẫn.
> - **2026-08-13: user chốt ĐƯA ẢNH QUAY LẠI** — *"nay phải bổ sung lại ảnh hướng dẫn chức năng
>   trong srs"*. Tức là quay về đúng bản mẫu `SRS_MAU.docx` (bản mẫu có 26 ảnh nhúng).

Mục **`5.2.x.3 Layout màn hình` của MỖI chức năng** gồm 2 phần, theo thứ tự:

**1. Đường dẫn** (giữ nguyên như quy ước cũ — vẫn hữu ích, không bỏ):
```
Đường dẫn màn hình:
• Menu: Phân hệ <X> → <Nhóm menu> → <Tên màn>
• Route (FE): /duong-dan-man
• URL đầy đủ: https://<host-hrm>/duong-dan-man
```
Với modal/popup, thêm 1 câu: *"Modal <Tên> được mở ngay trên màn hình danh sách theo đường dẫn ở trên."*

**2. Ảnh chụp thật của ĐÚNG chức năng đó**, canh giữa, rộng **6.2 inch**, kèm caption
`Hình N: <mô tả>` (in nghiêng, 9.5pt, canh giữa) — dùng đúng helper ở mục "Sinh ảnh biểu đồ Use Case".

| Chức năng | Ảnh phải chụp |
|---|---|
| Truy cập màn hình | Toàn màn danh sách lúc mới vào |
| Xem danh sách | Bảng danh sách (thấy rõ các cột) |
| Tìm kiếm & lọc | Panel bộ lọc nâng cao ĐANG MỞ |
| Tạo mới | Form/modal Tạo mới (trống, chưa nhập) |
| Chỉnh sửa | Form/modal Sửa có dữ liệu thật |
| Xem chi tiết | Màn/modal chi tiết ở chế độ chỉ đọc |
| Khóa / Mở khóa | Hộp thoại xác nhận |
| Xóa | Hộp thoại xác nhận xóa |
| Import / Export | Modal chọn cột / chọn file |
| Validate | Form đang hiện lỗi đỏ inline (nếu tách thành mục riêng) |

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
| `assets/srs_uml_render.py` | Module vẽ PNG bằng Pillow — `draw_overview()` và `draw_usecase()`. Tên snake_case để import được |
| `assets/srs_docx_lib.py` | Lớp `SrsDoc` dựng file .docx theo form chuẩn (`gen_srs_mau.py` import từ đây) |
| `assets/gen_srs_mau.py` | **Bản mẫu tham chiếu**: dựng trọn SRS theo form chuẩn. Copy file này rồi thay nội dung là nhanh nhất |

Generator của từng màn đã làm nằm ở `.plans/gop-db/<feature>/gen_srs.py` — xem để đối chiếu:
`customer-care-serial-catalog` (màn chỉ đọc, đơn giản nhất) · `customer-care-cost-catalog`
(có vẽ biểu đồ use case) · `finance-account-catalog` · `finance-currency-catalog`.

Ảnh UML là file **trung gian**, đã nhúng vào .docx nên `srs_docx_lib` ghi chúng vào thư mục tạm
của hệ điều hành — không rải rác vào repo. Muốn giữ lại để xem thì truyền `img_dir='...'`.

Phụ thuộc: `pip install pillow python-docx` (không cần cairosvg / playwright / trình duyệt).

> ⚠️ Tài liệu cũ trỏ 3 file này vào `hrm/scripts/`. Thư mục đó **nằm ngoài mọi git repo**
> (`d:\CompanyProject\hrm\` không phải repo — chỉ `hrm-api`, `hrm-client`, `hrm-claude-config` là
> repo), nên file để đó không đi theo repo và dev khác không có. Luôn lấy bản trong `assets/`.

### Cách gọi

```python
import sys, os
# Trỏ vào thư mục assets của skill để import được 2 module dùng chung
sys.path.insert(0, r"<đường dẫn>/.claude/skills/srs-documenter/assets")
import srs_uml_render as uml

# 5.1 Sơ đồ UML tổng quan
uml.draw_overview(
    'img/overview.png',
    'HỆ THỐNG HRM — <Tên màn hình>',
    [('Người quản lý danh mục (P1)', [0,1,2,3,4,5,6]),   # (tên actor, chỉ số use case nối tới)
     ('Người xem danh mục (P2)',     [0,1,2,6])],
    [('FR-01','Truy cập màn hình','view',   None),        # (mã, tên, nhóm màu, ghi chú)
     ('FR-04','Tạo mới',          'crud',   None),
     ('FR-06','Xoá / Khoá',       'action', '«extend» Khoá khi đã phát sinh chứng từ'),
     ('FR-07','Xuất Excel',       'io',     None)])

# 5.2.x.1 Biểu đồ use case của 1 chức năng
uml.draw_usecase('img/uc_fr06.png', 'Người quản lý danh mục (P1)',
                 'FR-06', 'Xoá / Khoá <đối tượng>', 'action',
                 [('include', 'Kiểm tra chứng từ phát sinh'),
                  ('extend',  'Khoá dịch vụ khi đã phát sinh chứng từ')])
```

**Nhóm màu ellipse:** `view` (xanh dương — xem/lọc/tra cứu) · `crud` (xanh lá — thêm/sửa) ·
`action` (cam — thao tác trạng thái) · `io` (tím — xuất/nhập/in) · `sub` (xám — use case include/extend).

### Chèn vào docx + chú thích

```python
par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
par.add_run().add_picture(png, width=Inches(6.2))
cap = doc.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap.add_run('Hình %d: %s' % (n, caption)); r.italic = True; r.font.size = Pt(9.5)
```

Ảnh tổng quan chèn ở **6.3 inch**, ảnh từng chức năng **6.2 inch**.

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

```python
sec = doc.sections[0]
sec.page_width  = Inches(8.5);  sec.page_height = Inches(11)     # Letter, bám bản mẫu
sec.left_margin = Inches(1.25); sec.right_margin = Inches(1.25)

doc.styles['Normal'].font.name = 'Calibri'
doc.styles['Normal'].font.size = Pt(11)
for name, size in [('Heading 1',20), ('Heading 2',16), ('Heading 3',14)]:
    doc.styles[name].font.size = Pt(size)
    doc.styles[name].font.color.rgb = RGBColor(0x2F,0x54,0x96)   # xanh navy như bản mẫu
```

Bảng dùng `style = 'Table Grid'`, chữ trong bảng `Pt(10)`, dòng tiêu đề in đậm.

---

## Quy trình generate SRS

### Bước 1: Thu thập thông tin từ code

**BE — đọc theo thứ tự:**
```
1. Migration        → Database schema, data types, constraints
2. Entity/Model     → Relationships, constants (STATUS, TYPE), accessors, điều kiện is_can_*
3. Routes           → API endpoints + middleware checkPermission (nguồn của chương 3)
4. Request          → Validation rules (nguồn của cột "Phạm vi"/"Bắt buộc" + thông báo lỗi)
5. Controller       → Request flow, response format
6. Service          → Business logic, điều kiện, phép tính (nguồn của chương 6)
7. Transformer      → Response data structure
8. PermissionsTableSeeder → Mã quyền + tên quyền + group (nguồn của bảng 3.1)
9. Console Command  → Scheduled jobs, cron logic
```

**FE — đọc theo thứ tự:**
```
1. Page component   → Cột bảng, nút, bộ lọc (nguồn của bảng "Mô tả chi tiết giao diện")
2. Modal component  → Trường nhập, giá trị mặc định, trạng thái enable/disable
3. API calls        → Endpoint + payload
4. Menu sidebar     → Đường dẫn menu (nguồn của mục "Layout màn hình")
```

### Bước 2: Phân tích & tổng hợp

- Xác định **actors** → quy về ký hiệu **P1 (quản lý) / P2 (xem)**, khớp đúng quyền trong seeder
- Liệt kê **chức năng FR-01…FR-0N** từ route + nút trên màn
- Trích **business rules BR-01…** từ service layer (if/else, validate, calculate, điều kiện chặn)
- Lập **ma trận phân quyền** từ middleware của từng route
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
print('tables', len(d.tables), 'paragraphs', len(d.paragraphs))
print('ảnh nhúng:', sum(1 for r in d.part.rels.values() if 'image' in r.reltype))
bad = [x.text for x in d.paragraphs if '┌' in x.text or '○' in x.text]
print('còn sơ đồ ký tự:', len(bad))    # PHẢI = 0
```

---

## Output

- **File chính:** `.plans/[feature]/SRS - <Tên màn hình>.docx`
  (nhánh `gop_db` → `.plans/gop-db/[feature]/…`)
- **Script sinh:** `.plans/[feature]/gen_srs.py` — đặt cùng thư mục tài liệu để **commit kèm được**,
  nhờ đó tái sinh lại file .docx bất cứ lúc nào.
  ⚠️ KHÔNG để ở `hrm/scripts/` — thư mục đó nằm ngoài mọi git repo nên "commit kèm" là bất khả thi.
- **Ảnh PNG: CHỈ ĐỂ LOCAL, KHÔNG commit.** Ảnh đã nhúng sẵn trong .docx nên người khác không cần
  bản rời; đẩy lên chỉ làm nặng repo. `srs_docx_lib` mặc định ghi ảnh vào thư mục tạm của hệ điều
  hành; nếu truyền `img_dir` để giữ lại thì đặt tên thư mục là `img/` hoặc `*_shots/` — `.gitignore`
  đã chặn sẵn 2 dạng này.
- Trước khi báo xong, chạy `git status`: chỉ được thấy `.docx` và `gen_srs.py`, không được thấy `.png`.

> Bản HTML (`srs.html`) là format CŨ, chỉ giữ cho các feature đã sinh trước 2026-08-07.
> Feature mới chỉ cần bản .docx theo form chuẩn.

---

## Quy tắc viết SRS

### Nguyên tắc chung
- Viết bằng **tiếng Việt**, thuật ngữ kỹ thuật giữ tiếng Anh
- Mỗi chức năng phải có **Điều kiện ban đầu + Dòng sự kiện chính + Dòng sự kiện phụ**
- Business rules phải **truy vết được** tới code
- Validation rules và **thông báo lỗi** phải khớp **100%** với Request class
- Mã quyền trong bảng 3.1 phải khớp **đúng id** trong `PermissionsTableSeeder`
- Mọi hành vi KHÁC với màn ERP gốc (nếu là màn port) phải ghi rõ là **chủ đích**

### Nguồn dữ liệu ưu tiên
1. **Code** (migration, entity, request, service, routes, seeder) — nguồn chính xác nhất
2. **design.md** trong `.plans/` — context về quyết định thiết kế
3. **plan.md** trong `.plans/` — scope đã thống nhất
4. **User mô tả** — bổ sung business context mà code không thể hiện

### Không được
- **Không vẽ sơ đồ bằng ký tự** — phải là ảnh PNG
- **Không bỏ ảnh ở mục Layout** — từ 2026-08-13 mỗi chức năng BẮT BUỘC có ảnh chụp thật kèm đường dẫn
- Không dùng template markdown/HTML tự chế thay cho form chuẩn
- Không đổi số cột / tên cột của 3 bảng bắt buộc
- Không đoán response format — đọc transformer/resource
- Không đoán validation rules — đọc Request class
- Không đoán database schema — đọc migration
- Không bỏ sót enum values — đọc constants trong Entity
- Không thêm requirement mà code không có (trừ khi SRS cho feature chưa code)

---

## Bản đã làm theo chuẩn này

| Màn hình | File |
|---|---|
| Danh mục dịch vụ sửa chữa và chi phí khác (CSKH) | `.plans/gop-db/customer-care-cost-catalog/SRS - Danh mục dịch vụ sửa chữa và chi phí khác.docx` |
