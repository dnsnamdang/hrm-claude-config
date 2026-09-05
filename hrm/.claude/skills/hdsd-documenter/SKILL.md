---
name: hdsd-documenter
description: Generate tài liệu Hướng dẫn sử dụng (HDSD) Word cho màn hình/luồng nghiệp vụ — CỰC KỲ CHI TIẾT, click-by-click, đủ từng trường + giá trị mặc định, ảnh chụp thật
---

# HDSD Documenter — ERP TPE

## Mục đích
Tạo tài liệu **Hướng dẫn sử dụng (HDSD)** dạng **Word (.docx)** cho người dùng cuối, cho một màn hình hoặc một luồng nghiệp vụ. Output phải giống **đúng file mẫu đã được duyệt: `assets/HDSD_MAU.docx`** (đóng gói ngay trong skill này — xem Bước 4), ảnh **chụp thật** từ hệ thống.

## Khi nào dùng
- User yêu cầu "viết tài liệu hướng dẫn", "viết HDSD", "hướng dẫn sử dụng màn …".
- Cần tài liệu bàn giao cho người dùng/đào tạo.

## ⚠️ NGUYÊN TẮC SỐ 1 — ĐẦY ĐỦ & CHI TIẾT TỐI ĐA
User đã chốt: HDSD phải **chi tiết tới từng hành động nhỏ nhất**. Liệt kê nút thôi là **CHƯA ĐỦ**. Với **mỗi nút điều hướng/mở popup** (Tạo mới, Sửa, Xem, Duyệt, Từ chối, Nhập kết quả, Xử lý, Xóa, In…) phải mô tả:
1. Bấm nút đó **mở ra màn/popup nào** (chụp ảnh thật màn đó).
2. **LIỆT KÊ TỪNG TRƯỜNG** nhập liệu: nhãn, loại control, **có bắt buộc không**, **giá trị điền sẵn/mặc định khi tạo mới**, điều kiện ẩn/hiện/khóa, dữ liệu cascading.
3. **Các nút lưu** và hành động (lưu gì, thông báo thành công, điều hướng đi đâu).
4. Trạng thái/kết quả sau thao tác.

→ Mỗi tab/màn có riêng các mục: **Tạo mới / Sửa / Xem / Duyệt / Nhập kết quả / Lịch sử / Xóa** (tuỳ màn có gì). Mục Tạo mới luôn có **bảng từng trường** + **box "Giá trị điền sẵn khi tạo mới"**.

## ⚠️ NGUYÊN TẮC SỐ 2 — VIẾT THEO TỪNG QUYỀN
Mỗi màn hình đều gắn với **một tập quyền cụ thể** (khai báo trong `PermissionsTableSeeder`, gắn vào route qua `checkPermission`, và ẩn/hiện nút ở FE). HDSD **BẮT BUỘC**:
1. **Liệt kê đủ mọi quyền liên quan tới màn** (tên quyền nguyên văn tiếng Việt như trong seeder).
2. **Mỗi quyền có một mục hướng dẫn riêng**: người có quyền đó **nhìn thấy gì** (tab/cột/nút/menu) và **làm được thao tác nào**, kèm hướng dẫn click-by-click cho đúng phạm vi quyền đó.
3. **Mỗi thao tác** trong tài liệu ghi rõ **quyền yêu cầu**; nếu không có quyền → nút bị ẩn (hoặc gọi API trả 403 "Bạn không có quyền…").
4. Nếu màn có **phân quyền theo cấp** (công ty/phòng ban/bộ phận/cá nhân) → mô tả rõ mỗi cấp thấy được dữ liệu của ai.

→ Không gộp chung "người dùng có thể tạo/sửa/xóa". Người đọc HDSD thường **chỉ có 1–2 quyền**, tài liệu phải cho họ biết chính xác phần nào áp dụng cho mình.

## ⚠️ NGUYÊN TẮC SỐ 3 — NGÔN NGỮ NGƯỜI DÙNG CUỐI, KHÔNG PHẢI NGÔN NGỮ CODE
Người đọc HDSD là **người dùng nghiệp vụ**, không phải dev. (User chốt 2026-08-12 khi review tài liệu: *"tài liệu này dev có dùng đâu mà toàn id như code thế này"*.)

**TUYỆT ĐỐI KHÔNG viết** vào tài liệu: tên bảng / tên cột DB · id permission, group, type, guard · tên hàm / class / file · đường dẫn API (`/api/v1/...`, `GET /{id}/lock`) · mã HTTP (400/403/404/422) · tên tham số kỹ thuật (`sort_by`, `per_page`, `meta.total`, `localStorage`, `filterCollapsed`).

Thay bằng **đúng nhãn hiển thị trên màn hình** và câu chữ người dùng hiểu:
- `status = 0` → "trạng thái Khóa" · `revenue_calculation = 1` → "Có tính doanh thu"
- "BE trả 422, lỗi inline" → "hệ thống báo lỗi đỏ ngay dưới ô …, cửa sổ không đóng"
- "BE trả 403" → "hệ thống từ chối, báo không có quyền"
- tên bảng chứng từ → tên nghiệp vụ ("Báo giá hãng", "Hợp đồng hãng")

**Vẫn giữ**: tên quyền nguyên văn tiếng Việt, và **đường dẫn màn hình** dạng `/customer-care/costs` (người dùng cần để gõ thẳng vào trình duyệt). Nếu cần nêu mã lỗi/endpoint cho tester, để trong tài liệu test case chứ không phải HDSD.

⚠️ Bám form TRÌNH BÀY của file mẫu nhưng **không bắt chước cách viết kỹ thuật** nếu file mẫu có.

Liên quan: `.claude/skills/testcase-documenter/SKILL.md` (cùng nguyên tắc ngôn ngữ) · `.claude/skills/srs-documenter/SKILL.md` (SRS thì NGƯỢC LẠI — được phép dùng thuật ngữ kỹ thuật).

## Quy trình (4 bước)

### Bước 1 — Khảo sát màn (đọc code — BẮT BUỘC đọc ĐỦ SOURCE MỌI LUỒNG LIÊN QUAN)
User đã chốt: **không chỉ đọc FE của màn** — phải đọc source code **tất cả các luồng liên quan** để tài liệu mô tả đúng nghiệp vụ, không đoán từ UI:
- **FE màn chính**: `index.vue` / page chính → tab, modal, nút, API gọi; quét toàn bộ component con (agent Explore/Opus).
- **BE đầy đủ**: Routes (middleware/permission) → Controller → Service → Entity/Model → FormRequest (rule + message) → Resource → **Migration/Seeder** (cột, giá trị mặc định thật). Đọc cả bảng Log/History nếu có.
- **LUỒNG XUÔI + NGƯỢC (downstream/upstream)**: grep tên Entity/Service/config xem **nơi nào KHÁC sử dụng** — vd màn cấu hình thì phải đọc service tiêu thụ cấu hình (cấu hình duyệt giá → `QuotationService::calculateApprovalLevel` + luồng gửi duyệt/TP/BGĐ + badge realtime trên form làm giá); màn tổng hợp thì đọc query gom từng loại dữ liệu (điều kiện lấy, loại trừ trạng thái nào). Trả lời được: **cấu hình/dữ liệu này sinh ra từ đâu, ảnh hưởng tới màn nào, chốt tại thời điểm nào, đổi rồi có tính lại không**.
- **Modal/form tái dùng từ module khác**: đọc tận file gốc (mode view/edit/approve khác nhau thế nào), không suy diễn.
- **QUÉT QUYỀN CỦA MÀN (bắt buộc)** — gom từ 4 nguồn, đối chiếu cho khớp:
  1. `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` → grep nhóm quyền của màn, lấy **tên quyền nguyên văn**.
  2. **Routes**: `->middleware('checkPermission:Tên quyền')` trên từng endpoint (index/store/update/destroy/approve/export…) → biết thao tác nào cần quyền nào.
     ⚠️ Tên quyền **có dấu phẩy** KHÔNG gắn qua middleware được (Laravel dùng dấu phẩy để tách tham số middleware, tên quyền sẽ bị cắt làm đôi) → những quyền đó được gate thẳng trong Controller/Service bằng `isCurrentEmployeeHasPermission('<Tên quyền>')`. Vì vậy **phải grep cả trong Controller/Service**, chỉ đọc file routes là bỏ sót quyền.
  3. **FE**: grep `hasPermission` / `can(` / `v-if` quanh nút & tab trong page và component con → biết nút nào bị ẩn khi thiếu quyền.
  4. **Phân quyền theo cấp** (nếu có): scope lọc dữ liệu theo `company_id`/`department_id`/`part_id`/người tạo trong Service → mỗi cấp thấy dữ liệu của ai.
  → Kết quả: **bảng quyền** (Tên quyền · Cho phép làm gì · Nút/tab tương ứng trên UI · Endpoint). Hỏi user nếu tên quyền trong seeder không khớp thực tế hoặc màn chưa gắn quyền.
- Kết quả khảo sát phải đủ để viết mục "Ý nghĩa nghiệp vụ / tác động" kèm **ví dụ số cụ thể** và các **edge case** (ranh giới ≥/<, giá trị rơi ngoài khoảng, quyền, thời điểm chốt dữ liệu).
- Hỏi user nếu cần: bỏ tab nào không, format (mặc định Word), ảnh chụp thật hay placeholder.

### Bước 2 — Chụp ảnh thật (Playwright MCP)
- Dùng **Playwright MCP (Node)** — KHÔNG dùng Playwright Python (bản Python chỉ dành cho pytest harness, xem `.claude/skills/playwright-setup/SKILL.md`).
- Login site (vd dev-hrm.eteksofts.com) bằng tài khoản user cung cấp → form `#emailaddress` (hoặc textbox "Địa chỉ email") + "Mật khẩu" + nút "Đăng nhập".
- **Ưu tiên tài khoản có dữ liệu thật ở mọi tab** để ảnh sát thực tế.
- Resize 1440x900. Mở từng tab, cuộn container nội dung lên đầu (`document.querySelector('.overflow-auto').scrollTop=0`) rồi chụp viewport; với form dài dùng `fullPage:true`.
- Chụp đủ: mỗi tab danh sách, bộ lọc nâng cao mở, các popup/modal (lọc, cấu hình cột, xác nhận xóa, xuất Excel chọn cột), **và đặc biệt các FORM Tạo mới/Sửa** mà nút mở ra.
- **Ảnh theo quyền**: nếu user cung cấp nhiều tài khoản khác quyền → chụp màn theo từng vai trò (vd tài khoản chỉ có quyền Xem: thanh công cụ không có nút Tạo mới/Duyệt) để minh hoạ mục "Hướng dẫn theo quyền". Chỉ có 1 tài khoản full quyền → vẫn chụp bằng tài khoản đó, nhưng **ghi chú rõ nút nào sẽ không hiển thị nếu thiếu quyền nào** (đừng bịa ảnh).
- Mở form Tạo mới KHÔNG lưu là an toàn. Với Duyệt/Xóa: chụp hộp xác nhận rồi **bấm Hủy** (không thực thi trên dữ liệu thật).
- Lưu ảnh vào `hdsd_<feature>_shots/` (đặt tên có số thứ tự + mô tả). Đọc lại ảnh để kiểm tra chất lượng trước khi dùng.

### Bước 3 — Đi sâu form (đọc field + mặc định)
- Mỗi nút "Tạo mới" thường mở **màn/popup riêng của phân hệ** (vd `/assign/solutions/add`, `/assign/meeting/create`, `/assign/assign_business/add`) hoặc popup trong trang (Task, Issue dùng `CreateXxxModal.vue`).
- **Cử nhiều agent Opus đọc song song** (mỗi agent 1 form/nhóm form). Yêu cầu mỗi agent trả về cho từng mode (create/edit/view/approve/handle):
  - Tiêu đề; các tab/section.
  - **Từng trường**: nhãn (nguyên văn tiếng Việt), control, bắt buộc + message lỗi, **giá trị mặc định/điền sẵn** (lấy từ `data()` init, `created/mounted`, prefill query, vd `created_by`=người dùng, ngày=hôm nay, phòng=phòng user, trạng thái mặc định), điều kiện ẩn/hiện/readonly, cascading, nguồn options (API).
  - Nút + hành động (API, toast, điều hướng); khác biệt giữa các mode.
- Chỉ định **model Opus** cho subagent đọc form (model nhỏ hơn hay bỏ sót trường và giá trị mặc định).

### Bước 4 — Dựng file Word (python-docx)

> ⚠️ **STYLE CHUẨN — FILE KHUNG ĐÓNG GÓI TRONG SKILL (không phụ thuộc máy cá nhân):**
> **`.claude/skills/hdsd-documenter/assets/HDSD_MAU.docx`**
> Mọi HDSD mới phải nhìn **giống hệt** file này — mở ra xem trước khi dựng nếu chưa rõ.
>
> **Dùng engine chung, KHÔNG nhân bản khung dựng cho mỗi màn:**
> **`.claude/skills/hdsd-documenter/assets/hdsd_engine.py`** (Windows, `python` + `python-docx`).
> Nó lo đủ: đổi dòng bìa → lưu proto Caption → strip body → helper style → purge media mồ côi →
> cập nhật mục lục bằng Word → assert sạch. Bắt dòng bìa và điểm strip **theo VỊ TRÍ** chứ không
> theo nội dung, nên dùng được với mọi file khung mà không phải sửa gì.
>
> Generator của từng màn chỉ còn phần nội dung:
> ```python
> import os, sys
> sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
>                                 "..", "..", "..", ".claude", "skills",
>                                 "hdsd-documenter", "assets"))
> from hdsd_engine import HdsdBuilder
>
> b = HdsdBuilder(output=..., shots_dir=..., cover_title="(Màn hình: …)", doc_title="HDSD - …")
> b.h1("TỔNG QUAN"); b.h2("1. Mục tiêu"); b.para("…")
> b.table([["Cột A", "Cột B"], ["1", "2"]])
> b.image("01-danh-sach.png", "Màn hình danh sách")
> b.finish()          # lưu + purge + cập nhật mục lục bằng Word + assert + in thống kê
> ```
> `b.image()` assert ảnh tồn tại nên thiếu ảnh là gãy ngay, không lặng lẽ bỏ qua.
> **Một feature nhiều màn** → mỗi màn một file `HDSD_<Tên màn>.docx`; một script có thể tạo nhiều
> `HdsdBuilder` liên tiếp (xem `.plans/gop-db/customer-care-maintenance-catalogs/gen_hdsd.py`).
>
> *(`assets/gen_hdsd_mau.py` là bản đầy đủ một file, giữ lại để tham chiếu cách dựng.
> Bản `hdsd_p5_work/hdsd_clean.py` / `HDSDClean` nêu ở tài liệu cũ KHÔNG còn tồn tại trong repo.)*
>
> **QUY ĐỊNH TRÌNH BÀY — chốt 05/09/2026, áp cho CẢ SRS lẫn HDSD.**
> Đã nằm sẵn trong **style của `assets/HDSD_MAU.docx`** → generator **không phải làm gì thêm**,
> và **tuyệt đối không được ép lại bằng direct formatting**:
>
> | Thành phần | Quy định | Nằm ở đâu |
> |---|---|---|
> | Toàn bộ tài liệu | Font **Times New Roman** | style `Normal` + `word/theme/theme1.xml` |
> | Heading 1 | **18pt**, **căn giữa**, **bắt đầu từ đầu trang mới** | style `Heading 1` (`jc=center` + `pageBreakBefore`) |
> | Trang bìa | giữ nguyên cỡ chữ lớn của mẫu — **miễn trừ** quy tắc 13pt | style `Title` |
> | Văn xuôi, bullet, Heading 2/3 | **13pt** | `Normal` 13pt, Heading 2/3 không khai size → kế thừa |
> | Chú thích tên hình ảnh | **căn giữa**, **13pt** | style `Caption` (`jc=center`, kế thừa cỡ chữ của `Normal`) |
> | Chữ trong bảng | kế thừa `Normal` | style bảng |
>
> ⚠️ **Bẫy: Heading của file mẫu trỏ sang FONT THEME** (`w:asciiTheme="majorHAnsi"`). Còn thuộc
> tính `*Theme` thì Word ưu tiên nó và **xoá `w:ascii`** khi lưu lại ở bước cập nhật mục lục →
> heading không ra Times New Roman. Đã xử lý một lần trong `HDSD_MAU.docx`: bỏ hết `*Theme` trong
> `styles.xml` + đổi `majorFont`/`minorFont` của `theme1.xml` sang Times New Roman.
> **Đổi file mẫu sau này phải làm lại đúng 2 việc đó.**
>
> **Luật vàng: KHÔNG áp direct formatting — để style của template quyết định tất cả.**
> | Thành phần | Đúng (như file mẫu) | Sai (đừng làm) |
> |---|---|---|
> | Heading 1/2/3 | `add_paragraph(text, style='Heading N')`, không set gì thêm → tự ra đúng quy định trên | Ép canh giữa / ép font / ép size / ép line-spacing / tự chèn page break |
> | Body | chỉ set `alignment = JUSTIFY` | Ép 12pt / giãn dòng 1.5 / space_before/after |
> | List Bullet | `style='List Bullet'`, không set gì thêm | Ép font, ép alignment, ép spacing |
> | Ô bảng | chỉ gán `cell.text`; đậm dòng tiêu đề do table style tự làm | Ép bold/font/size từng run |
> | Bảng | style `Light Grid Accent 1` + `alignment = CENTER` | Style khác, autofit tay |
> | Ảnh | paragraph canh giữa, `width=Inches(6.0)` cho MỌI ảnh | 5.4"/5.6"/kích thước lẻ mỗi ảnh một khác |
> | In đậm | chỉ `run.bold = True` khi cần nhấn ý | Đậm kèm ép font/size |
>
> **Cách kiểm chứng đã giống mẫu** (chạy trước khi giao):
> so 3 số dưới đây với chính `assets/HDSD_MAU.docx`; đếm paragraph Heading có `alignment`/`line_spacing`/`space_*`/`first_line_indent`/run có `font.name|size`
> → phải = **2**; đếm tương tự cho Normal + List Bullet → phải = **10**; đếm run trong ô bảng có
> `font.name|font.size|bold` → phải = **0**. (2 và 10 là phần bìa + mục lục kế thừa từ template.)
> Lệch số nghĩa là còn direct formatting sót → sửa rồi build lại.
> **Kiểm định dạng theo quy định 05/09/2026** (chạy trên file ĐÃ finish, tức đã qua Word):
> ```python
> import re, zipfile
> from docx import Document
> d = Document(OUT); h1 = d.styles['Heading 1']
> assert h1.font.size.pt == 18 and str(h1.paragraph_format.alignment).startswith('CENTER') >        and h1.paragraph_format.page_break_before is True, 'Heading 1 sai quy định'
> assert d.styles['Normal'].font.size.pt == 13, 'Chữ thân bài phải 13pt'
> assert str(d.styles['Caption'].paragraph_format.alignment).startswith('CENTER'), >        'Chú thích hình phải căn giữa'
> with zipfile.ZipFile(OUT) as z:
>     theme = z.read('word/theme/theme1.xml').decode('utf-8')
> assert set(re.findall(r'<a:latin typeface="([^"]*)"', theme)[:2]) == {'Times New Roman'}
> ```
> Muốn soi mắt thường: `soffice --headless --convert-to pdf` rồi render trang thân bài bằng PyMuPDF,
> so cạnh trang tương ứng của `assets/HDSD_MAU.docx`.

Generator chạy bằng `python` trên Windows, lib `python-docx` + `Pillow`. Các bước:

1. **Copy file mẫu làm khung**: giữ Bìa (kèm logo) + MỤC LỤC (TOC field) + DANH MỤC HÌNH ẢNH (TOF field) + toàn bộ styles.
2. **Sửa dòng tiêu đề trên bìa** `(Luồng nghiệp vụ: …)` → `(Màn hình: …)`.
   > 🐛 **BẪY 1 — dòng bìa bị cắt thành nhiều run.** `for run in p.runs: run.text.replace(...)` sẽ
   > **không khớp run nào và im lặng bỏ qua** (chuỗi nằm rải ở "Luồng nghiệp vụ", ": Tổng hợp",
   > " Bomlist)"). Phải dọn hết text về run đầu:
   > ```python
   > for run in p.runs[1:]: run.text = ""
   > p.runs[0].text = TIEU_DE_MOI
   > ```
   > Dùng `for…else: raise` để script gãy ngay nếu không tìm thấy dòng bìa.
3. Lưu **proto Caption** (clone paragraph style `Caption`, có SEQ field nên Word tự đánh số):
   run0 "Hình " + SEQ + run cuối ": <text>".
4. **Strip body** từ **Heading 1 thứ 3 trở đi** tới hết, GIỮ `sectPr` (luôn là child cuối của body).
   Heading 1 #1 = "MỤC LỤC", #2 = "DANH MỤC HÌNH ẢNH" → giữ; #3 trở đi là thân bài của tài liệu mẫu.
   > 🐛 Bắt theo **VỊ TRÍ**, đừng bắt theo text: mỗi file khung đặt tên khác nhau
   > ("TỔNG QUAN" ở `HDSD_Bomlist`, "TỔNG QUAN PHẦN MỀM" ở `HDSD_MAU`).
   > Nếu vẫn cần đọc text heading thì dùng `Paragraph(child, doc).text`, **KHÔNG dùng
   > `child.itertext()`** — hàm này gom cả text trong field/bookmark nên trả về
   > "TỔNG QUANTỔNG QUANTỔNG QUAN". Style name trong XML là `Heading1` (không có dấu cách).
   >
   > 💡 Lưu lại danh sách tiêu đề thân bài của file khung ở bước này — bước 8 dùng để assert.
5. Rebuild bằng helper tự viết: `h1/h2/h3`, `para` (Normal justify), `bullet`, `table`, `image`,
   `caption` — mọi phần tử chèn qua `sectPr.addprevious(...)`. Xem bảng luật style ở trên.
6. **Purge media mồ côi** (python-docx không xoá file ảnh khi xoá paragraph → file phình; thực đo
   4.4 MB → 3.3 MB): quét `r:embed`/`r:link` trong document/header/footer → map qua `.rels` → bỏ
   media + Relationship không còn ai tham chiếu.
7. **CẬP NHẬT MỤC LỤC & DANH MỤC HÌNH ẢNH BẰNG WORD — BẮT BUỘC.**
   > 🐛 **BẪY 2 — lỗi nghiêm trọng nhất, từng lọt ra file bàn giao.** `updateFields=true` CHỈ là
   > *lời mời* Word cập nhật khi mở file; bản thân `document.xml` **vẫn giữ nguyên text cũ của
   > template**. Ai mở bằng WPS / trình xem khác (hoặc bấm "No" khi Word hỏi) sẽ thấy nguyên mục lục
   > của tài liệu mẫu — "PHẦN 2: TẠO BOM LIST" nằm trong HDSD màn danh mục chi phí.
   >
   > Máy team có Word (`C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE`) → gọi qua
   > PowerShell COM từ generator (`subprocess.run(["powershell", "-NonInteractive", "-Command", …])`):
   > ```powershell
   > $doc = $word.Documents.Open($p, $false, $false)
   > $doc.Fields.Update() | Out-Null
   > foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
   > foreach ($tof in $doc.TablesOfFigures) { $tof.Update() }
   > $doc.Repaginate(); $doc.Save(); $doc.Close(0); $word.Quit()
   > ```
   > (`$word.Visible = $false`, `$word.DisplayAlerts = 0`.) Sau bước này số trang trong mục lục mới
   > là số trang thật. Tiện thể set `BuiltInDocumentProperties("Title")`.
8. **Verify — assert trong generator, không kiểm bằng mắt:**
   - **`assert` không còn tiêu đề thân bài nào của file khung trong `document.xml`** (dùng danh sách
     đã lưu ở bước 4) — một dòng này chốt cả mục lục, danh mục hình ảnh lẫn bìa
   - Số `inline_shapes` / `tables` / `Caption` / `Heading 1` đúng như dự kiến
     (lưu ý `inline_shapes` = số ảnh nội dung **+ 1 logo bìa**)
   - Mọi `r:embed` resolve được trong `.rels` (broken = 0)
   - Dump lại toàn bộ paragraph style `toc 1`/`toc 2`/`table of figures` ra file UTF-8 và **đọc**
     — đây là bước duy nhất phát hiện được mục lục sai nội dung

## Cấu trúc tài liệu (bắt buộc)
Bìa → MỤC LỤC → DANH MỤC HÌNH ẢNH → **TỔNG QUAN PHẦN MỀM** (1. Thuật ngữ, 2. Cập nhật tài liệu, 3. Giới thiệu chung + đường dẫn, 4. Quyền & phạm vi) → **PHẦN 1: Truy cập & bố cục** → **mỗi tab/màn = 1 PHẦN**, trong đó:
- Ảnh tổng quan tab.
- Tìm kiếm & lọc (ô nhanh + bộ lọc nâng cao liệt kê từng tiêu chí).
- Các cột danh sách.
- Nút thanh công cụ (Tạo mới / Xuất Excel / Cấu hình cột…).
- Thao tác từng dòng (theo quyền & trạng thái).
- **Tạo mới** (ảnh form + bảng từng trường + box mặc định + nút lưu).
- **Sửa / Duyệt / Nhập kết quả / Xử lý / Lịch sử / Xóa** (mô tả khác biệt, ảnh nếu cần).
- **Mục "Phân quyền & hướng dẫn theo quyền"** (bắt buộc, đặt ngay sau ảnh tổng quan tab):
  - **Bảng quyền của màn**: `Tên quyền | Cho phép làm gì | Nút/tab tương ứng | Ghi chú (điều kiện trạng thái, cấp dữ liệu)`.
  - **Mỗi quyền một tiểu mục** "Người dùng có quyền *<Tên quyền>*": thấy gì (tab/cột/nút), làm được thao tác nào, hướng dẫn từng bước cho đúng phạm vi quyền, và **thấy dữ liệu của ai** nếu có phân quyền theo cấp.
  - Câu cảnh báo chuẩn: *"Nếu không có quyền này, nút … sẽ không hiển thị; trường hợp truy cập trực tiếp bằng đường dẫn, hệ thống báo lỗi không có quyền."*
- Trong mọi mục thao tác ở trên, mỗi thao tác **ghi kèm quyền yêu cầu** (vd: *Duyệt — yêu cầu quyền "Duyệt báo giá"*).

## Checklist độ đầy đủ (tự kiểm trước khi giao)
- [ ] Đã đọc source ĐỦ các luồng liên quan (FE màn + BE route→service→entity→migration + nơi khác tiêu thụ dữ liệu/cấu hình) — tài liệu có mục giải thích nghiệp vụ/tác động kèm ví dụ, không viết mò từ UI.
- [ ] Mỗi nút "Tạo mới" có ảnh form thật + bảng từng trường + cột "Bắt buộc" + cột "Giá trị mặc định".
- [ ] Đã ghi rõ giá trị điền sẵn (người tạo/người duyệt/người theo dõi/ngày/giờ/trạng thái/phòng ban…).
- [ ] Mỗi thao tác thay đổi dữ liệu (Sửa/Duyệt/Từ chối/Nhập kết quả/Xóa) đều được mô tả: mở ra gì, nhập gì, lưu thế nào, kết quả.
- [ ] **Đã liệt kê ĐỦ quyền của màn** (đối chiếu seeder + middleware `checkPermission` + gate trong controller + `hasPermission` ở FE), tên quyền nguyên văn.
- [ ] **Mỗi quyền có tiểu mục hướng dẫn riêng**: thấy gì, làm được gì, các bước thao tác, phạm vi dữ liệu theo cấp (nếu có).
- [ ] Mỗi thao tác thay đổi dữ liệu đều ghi rõ **quyền yêu cầu** + điều gì xảy ra khi thiếu quyền.
- [ ] Bộ lọc nâng cao liệt kê đủ từng tiêu chí.
- [ ] Ảnh chụp thật, rõ, đúng nội dung; caption đánh số tự động.
- [ ] **KHÔNG còn thuật ngữ code** (tên bảng/cột, id quyền, endpoint, mã HTTP) — xem NGUYÊN TẮC SỐ 3.
- [ ] **Đã ĐỌC LẠI mục lục và danh mục hình ảnh trong file xuất ra** — đúng heading của màn này,
      số trang thật, KHÔNG còn dòng nào của tài liệu mẫu. (Đừng tin `updateFields`; phải cho Word
      cập nhật thật rồi dump ra kiểm.)
- [ ] **Dòng tiêu đề trên bìa** đã đổi đúng tên màn hình (dễ sót vì lệnh replace không báo lỗi).
- [ ] File mở được, không lỗi ảnh (broken=0), đã purge media mồ côi.
- [ ] **Thư mục ảnh nguồn KHÔNG bị commit** — chạy `git status`, chỉ được thấy file `.docx` và
      `gen_hdsd.py`, tuyệt đối không thấy file `.png` nào.
- [ ] **Style giống file mẫu**: đếm paragraph có direct formatting → Heading = 2 (phần bìa/mục lục kế thừa template), run trong ô bảng = 0, mọi ảnh rộng 6.0" canh giữa (xem bảng luật style ở Bước 4). Đối chiếu bằng cách chạy cùng phép đếm trên chính file mẫu:
      ```python
      def over(p):
          pf = p.paragraph_format
          if p.alignment is not None or pf.line_spacing or pf.space_before or pf.space_after or pf.first_line_indent: return True
          return any(r.font.name or r.font.size for r in p.runs)
      ```
      (Paragraph body đặt `alignment = JUSTIFY` nên nhóm Normal + List Bullet đếm cao là bình thường — file mẫu cũng vậy.)

## Output & lưu trữ
- File Word: `.plans/[feature]/HDSD_<TênMàn>.docx` (cùng chỗ design.md / plan.md / testcase.xlsx) — hoặc theo vị trí user chỉ định.
- Ảnh nguồn: `.plans/[feature]/hdsd_<feature>_shots/` — **CHỈ ĐỂ LOCAL, KHÔNG commit**.
  Ảnh đã nhúng sẵn trong .docx nên người khác không cần bản rời; đẩy lên chỉ làm nặng repo
  (9 ảnh của 1 màn đã là ~3 MB). Giữ lại trên máy để còn sửa / xóa / chụp lại khi cập nhật tài liệu.
  `.gitignore` của `hrm-claude-config` đã chặn sẵn `**/.plans/**/*_shots/` và `**/.plans/**/img/`
  — kiểm tra bằng `git status` trước khi báo xong, nếu thấy ảnh hiện ra là rule chưa ăn.
- Generator: lưu vào `.plans/[feature]/gen_hdsd.py` — cùng thư mục tài liệu nên **được version control**. KHÔNG để trong scratchpad (mất khi hết session), cũng KHÔNG để ở `hrm/scripts/` (thư mục đó nằm NGOÀI mọi git repo, người khác clone về sẽ không có).
- Cập nhật `.plans/[feature]/plan.md` + `STATUS.md` theo convention.

## Lưu ý
- Tài liệu + ngôn ngữ: **tiếng Việt**, văn phong cho người dùng cuối (xem NGUYÊN TẮC SỐ 3).
- 🐛 **Console Windows là cp1252** — `print()` chuỗi tiếng Việt trong script kiểm tra sẽ ném
  `UnicodeEncodeError`. Ghi kết quả ra file bằng `io.open(..., encoding="utf-8")` rồi đọc file đó,
  đừng in thẳng.
- KHÔNG thực thi thao tác phá huỷ trên dữ liệu thật khi chụp (Duyệt/Xóa → bấm Hủy).
- Nếu màn tái sử dụng form của phân hệ khác (vd "Tạo mới" mở màn module khác) → vẫn mô tả đầy đủ trong HDSD này (đừng chỉ trỏ "xem màn khác").
