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

Xem thêm memory: `feedback_hdsd_detail_level`, `reference_hdsd_format`, `reference_hdsd_luongchinh`, `reference_playwright_ui_test`.

## Quy trình (4 bước)

### Bước 1 — Khảo sát màn (đọc code — BẮT BUỘC đọc ĐỦ SOURCE MỌI LUỒNG LIÊN QUAN)
User đã chốt: **không chỉ đọc FE của màn** — phải đọc source code **tất cả các luồng liên quan** để tài liệu mô tả đúng nghiệp vụ, không đoán từ UI:
- **FE màn chính**: `index.vue` / page chính → tab, modal, nút, API gọi; quét toàn bộ component con (agent Explore/Opus).
- **BE đầy đủ**: Routes (middleware/permission) → Controller → Service → Entity/Model → FormRequest (rule + message) → Resource → **Migration/Seeder** (cột, giá trị mặc định thật). Đọc cả bảng Log/History nếu có.
- **LUỒNG XUÔI + NGƯỢC (downstream/upstream)**: grep tên Entity/Service/config xem **nơi nào KHÁC sử dụng** — vd màn cấu hình thì phải đọc service tiêu thụ cấu hình (cấu hình duyệt giá → `QuotationService::calculateApprovalLevel` + luồng gửi duyệt/TP/BGĐ + badge realtime trên form làm giá); màn tổng hợp thì đọc query gom từng loại dữ liệu (điều kiện lấy, loại trừ trạng thái nào). Trả lời được: **cấu hình/dữ liệu này sinh ra từ đâu, ảnh hưởng tới màn nào, chốt tại thời điểm nào, đổi rồi có tính lại không**.
- **Modal/form tái dùng từ module khác**: đọc tận file gốc (mode view/edit/approve khác nhau thế nào), không suy diễn.
- **QUÉT QUYỀN CỦA MÀN (bắt buộc)** — gom từ 4 nguồn, đối chiếu cho khớp:
  1. `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` → grep nhóm quyền của màn, lấy **tên quyền nguyên văn**.
  2. **Routes**: `->middleware('checkPermission:Tên quyền')` trên từng endpoint (index/store/update/destroy/approve/export…) → biết thao tác nào cần quyền nào. Lưu ý quyền có **dấu phẩy** không gắn qua middleware được → gate trong controller bằng `isCurrentEmployeeHasPermission` (memory `reference_checkpermission_comma`) — nhớ grep cả trong Controller/Service.
  3. **FE**: grep `hasPermission` / `can(` / `v-if` quanh nút & tab trong page và component con → biết nút nào bị ẩn khi thiếu quyền.
  4. **Phân quyền theo cấp** (nếu có): scope lọc dữ liệu theo `company_id`/`department_id`/`part_id`/người tạo trong Service → mỗi cấp thấy dữ liệu của ai.
  → Kết quả: **bảng quyền** (Tên quyền · Cho phép làm gì · Nút/tab tương ứng trên UI · Endpoint). Hỏi user nếu tên quyền trong seeder không khớp thực tế hoặc màn chưa gắn quyền.
- Kết quả khảo sát phải đủ để viết mục "Ý nghĩa nghiệp vụ / tác động" kèm **ví dụ số cụ thể** và các **edge case** (ranh giới ≥/<, giá trị rơi ngoài khoảng, quyền, thời điểm chốt dữ liệu).
- Hỏi user nếu cần: bỏ tab nào không, format (mặc định Word), ảnh chụp thật hay placeholder.

### Bước 2 — Chụp ảnh thật (Playwright MCP)
- Dùng **Playwright MCP (Node)** — KHÔNG dùng Playwright Python (đó là cho pytest harness). Tham khảo `reference_playwright_ui_test`.
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
- Dùng Opus cho subagent (memory `feedback_subagent_model_opus`).

### Bước 4 — Dựng file Word (python-docx)

> ⚠️ **STYLE CHUẨN — FILE MẪU NẰM NGAY TRONG SKILL:**
> **`.claude/skills/hdsd-documenter/assets/HDSD_MAU.docx`** (bản gốc là `HDSD_KhachHang.docx` user đã duyệt).
> Mọi HDSD mới phải nhìn **giống hệt** file này — mở nó ra xem trước khi dựng nếu chưa rõ.
> Dùng sẵn `hdsd_p5_work/hdsd_clean.py` → `from hdsd_clean import HDSDClean` (subclass của
> `hdsd_lib.HDSD`; tự lấy `assets/HDSD_MAU.docx` làm khung, fallback `HDSD_KhachHang.docx` ở gốc HRM/).
> **KHÔNG dùng thẳng `hdsd_lib.HDSD`** — bản gốc ép direct formatting nên ra file trông khác hẳn mẫu.
>
> **Luật vàng: KHÔNG áp direct formatting — để style của template quyết định tất cả.**
> | Thành phần | Đúng (như file mẫu) | Sai (đừng làm) |
> |---|---|---|
> | Heading 1/2/3 | `add_paragraph(text, style='Heading N')`, không set gì thêm → tự ra trái, xanh, font heading | Canh giữa, ép Times New Roman, ép size, ép line-spacing |
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
> Muốn soi mắt thường: `soffice --headless --convert-to pdf` rồi render trang thân bài bằng PyMuPDF,
> so cạnh trang tương ứng của `assets/HDSD_MAU.docx`.

Theo `reference_hdsd_format` + `reference_hdsd_luongchinh`. Generator (python `/opt/homebrew/opt/python@3.14/bin/python3.14`, lib `python-docx` + `Pillow`):
1. **Copy `assets/HDSD_MAU.docx` làm khung**: giữ Bìa (kèm logo) + MỤC LỤC (TOC field cả Heading 1–3) + DANH MỤC HÌNH ẢNH (TOF field) + styles + `updateFields=true`.
2. Sửa bìa `(Danh mục X)` → `(Màn hình: …)` / `(Luồng nghiệp vụ: …)`.
3. Lưu **proto Caption** (clone, có SEQ field auto-số): run0 "Hình " + SEQ + run2 ": <text>".
4. **Strip body** từ heading "TỔNG QUAN PHẦN MỀM" tới hết, GIỮ `sectPr` (luôn là child cuối của body).
5. Rebuild bằng helper của `HDSDClean`: `h1/h2/h3`, `para` (Normal justify), `bullet`, `table`, `image`, `caption` (ghép qua `sectPr.addprevious(clone)`) — xem bảng luật style ở trên.
6. **Purge media mồ côi** sau khi strip (python-docx không xoá media khi xoá paragraph → file phình): quét `r:embed`/`r:link` trong document/header/footer → map qua `.rels` → bỏ media + Relationship không tham chiếu. (Bìa các file mẫu là text, purge an toàn.)
7. Bật `updateFields=true` để Word tự cập nhật mục lục/danh mục hình khi mở.
8. **Verify**: mở lại bằng python-docx, kiểm `inline_shapes`/`tables`/`captions`/`Heading 1` đúng số; quét mọi `r:embed` resolve được (broken=0).

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
- [ ] File mở được, mục lục/danh mục hình tự cập nhật, không lỗi ảnh (broken=0).
- [ ] **Style giống hệt file mẫu `assets/HDSD_MAU.docx`**: dựng bằng `HDSDClean`, đếm override = 2 (Heading) / 10 (Normal+List Bullet) / 0 (run trong ô bảng), mọi ảnh 6.0" canh giữa (xem bảng luật style ở Bước 4).

## Output & lưu trữ
- File Word: `HDSD_luongchinh/HDSD_<TênMàn>.docx` (luồng/màn lớn) — hoặc theo vị trí user chỉ định.
- Ảnh nguồn: `hdsd_<feature>_shots/`.
- Generator: lưu trong scratchpad (ephemeral) — ghi lại cách chạy vào `.plans/[feature]/design.md` để tái dựng.
- Cập nhật `.plans/[feature]/plan.md` + `STATUS.md` theo convention.

## Lưu ý
- Tài liệu + ngôn ngữ: **tiếng Việt**, văn phong cho người dùng cuối.
- KHÔNG thực thi thao tác phá huỷ trên dữ liệu thật khi chụp (Duyệt/Xóa → bấm Hủy).
- Nếu màn tái sử dụng form của phân hệ khác (vd "Tạo mới" mở màn module khác) → vẫn mô tả đầy đủ trong HDSD này (đừng chỉ trỏ "xem màn khác").
