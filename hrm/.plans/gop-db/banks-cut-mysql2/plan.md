# Plan — banks-cut-mysql2

Người phụ trách: @khoipv · Nhánh: `gop_db` · Spec: `docs/superpowers/specs/gop-db/2026-08-03-banks-cut-mysql2-design.md`

## Phase 1 — BE: cắt sync db_second khỏi BankService

- [x] `BankService.php`: bỏ inject `TpBank`/`TpBankBranch` khỏi constructor + 2 property
- [x] `BankService.php`: bỏ 8 khối sync `use_erp` trong `createBank`, `addBankBranches`, `deleteBank`, `deleteBankBranches`, `lock`, `unlock`
- [x] `BankService.php`: dọn import thừa (`TpBank`, `TpBankBranch`, `MasterSetting`, `DB`)
- [x] `BankBranch.php`: xoá comment `// protected $connection = 'mysql2';` + xoá constructor override hỏng (dòng 145-148)

## Phase 2 — Verify

- [x] `php -l` 2 file sửa — sạch
- [x] Grep xác nhận `BankService` sạch `TpBank|TpBankBranch|use_erp` — 0 match
- [x] Smoke test tinker (transaction + rollback): tạo/sửa bank (1 dòng duy nhất), tạo/sửa branch, lock/unlock, xoá — tất cả PASS, DB nguyên trạng (0 dòng test sót)
- [x] Check `storage/logs/laravel.log` — smoke test không sinh lỗi mới (chỉ có lỗi cũ `Unknown database 'forge'` 14:13-14:18, do config chưa load .env, không liên quan)

### Checkpoint — 2026-08-03
Vừa hoàn thành: toàn bộ Phase 1 + Phase 2 (cắt sync db_second màn banks + fix constructor BankBranch, verify xong).
Đang làm dở: không.
Bước tiếp theo: user test lại màn /human/banks trên browser nếu muốn; feature sẵn sàng.
Blocked: không.

## Phase 3 — FE: thêm loading `$nuxt.$loading` cho thao tác ghi màn /human/banks (yêu cầu user 2026-08-03)

- [x] `BankModel.vue` `submitSave`: thêm `$nuxt.$loading.start()` (đã có sẵn `finish()` trong finally)
- [x] `BankBranchesAddModel.vue` `submitSave`: thêm `$nuxt.$loading.start()` (đã có sẵn `finish()` trong finally)
- [x] `BankBranchesModel.vue` `deleteBankBranch`: thêm start + `.finally(finish)`
- [x] `index.vue` `deleteBank` + `unlockItem`: thêm start + `.finally(finish)`; `lockItem`: bọc try/catch/finally + thêm toast lỗi (trước đó lock fail là rejection câm, không toast — nay đồng bộ với unlockItem)
- [x] Verify: parse template + script 4 file bằng vue-template-compiler + @babel/parser — OK cả 4

### Checkpoint — 2026-08-03 (Phase 3)
Vừa hoàn thành: loading cho toàn bộ 6 thao tác ghi màn /human/banks (lưu bank, lưu chi nhánh, xoá chi nhánh, xoá/khoá/mở khoá bank).
Đang làm dở: không.
Bước tiếp theo: user test browser màn /human/banks (loading bar chạy khi bấm Lưu/Xoá/Khoá).
Blocked: không.

## Phase 4 — FE: làm lại UI màn /human/banks theo V2Base (yêu cầu user 2026-08-03, tham khảo assign/industry-groups)

- [x] `index.vue`: V2BaseFilterPanel (keyword + tên viết tắt + tên GDQT + trạng thái) + V2BaseDataTable (STT, Logo, Mã-Tên NH + actions, Tên GDQT, Địa chỉ, Chi nhánh, Cập nhật sortable, Trạng thái pill + toggle lock) + BaseConfirmModal xoá/khoá + auto-search deep watcher theo skill list-page
- [x] `BankModel.vue`: modal V2 (hide-footer, header icon, V2BaseInput/Label, lỗi inline text-small-error, footer Lưu/Lưu & Tiếp tục/Đóng theo skill button-convention), giữ tra cứu VietQR + upload logo, validate client chặn submit khi thiếu required
- [x] `BankBranchesModel.vue`: modal V2 chứa bảng chi nhánh (toolbar Thêm chi nhánh + lọc tỉnh/tên, bảng sticky header, action Sửa/Xoá) — xoá chi nhánh nay có BaseConfirmModal xác nhận (trước đây xoá thẳng không hỏi)
- [x] `BankBranchesAddModel.vue`: modal V2 form (tên + tỉnh V2BaseSelectInModal, lỗi inline, footer chuẩn)
- [x] `BankSearch.vue`: restyle header/footer V2, giữ logic tra cứu VietQR
- [x] Icon đã đối chiếu font local `_remixicon.scss` (17/17 OK)
- [x] Verify: parse 5 file OK + Playwright browser: danh sách 10 dòng render đúng, lọc nâng cao mở đúng, modal tạo mới + validate inline 3 lỗi, modal chi nhánh + modal thêm chi nhánh lồng, E2E tạo bank "Ngân hàng Test V2" → hiện đầu danh sách → xoá qua confirm modal → DB sạch (SELECT count=0)

## Phase 5 — FE: thêm chức năng Xem chi tiết ngân hàng (yêu cầu user 2026-08-03)

- [x] `index.vue`: thêm nút Xem (ri-eye-line, đứng đầu theo thứ tự Xem → Sửa → Xoá của skill button-convention, bấm được cả khi khoá) + state `isShow` + reset qua `@closeModal` (modal emit khi `@hidden`)
- [x] `BankModel.vue`: prop `isShow` — title "Xem chi tiết ngân hàng", ẩn khối Gợi ý/Tra cứu + nút upload/xoá ảnh, disable toàn bộ input, thêm ô Trạng thái (chỉ view), footer chỉ còn Đóng (skill modal-popup: modal chỉ xem)
- [x] Verify: parse 2 file OK + Playwright: modal Xem đủ 6 input disabled + đúng dữ liệu SHB, footer chỉ Đóng, không Tra cứu/Tải ảnh; đóng rồi mở Sửa cùng dòng → input enable lại, footer Lưu/Đóng, có Tra cứu (isShow reset đúng)

### Checkpoint — 2026-08-03 (Phase 5)
Vừa hoàn thành: chức năng Xem chi tiết ngân hàng (read-only modal).
Đang làm dở: không.
Bước tiếp theo: user test lại toàn màn /human/banks trên browser.
Blocked: không.

## Phase 6 — Tài liệu test case màn Danh mục ngân hàng (yêu cầu user 2026-08-07)

- [x] Rà lại BE: `BankController`, `BankService`, `Bank`, `BankBranch`, `CreateBankRequest`, `CreateBankBranchesRequest`, `Routes/api.php`, 3 Resource
- [x] Rà lại FE: `pages/master-data/banks/index.vue` + 4 component (BankModel, BankBranchesModel, BankBranchesAddModel, BankSearch)
- [x] Xác định phân quyền: route chỉ có `auth:api`, KHÔNG gắn `checkPermission`, menu `master-data.js` không có permission key → không sinh section TC-ROLE
- [x] Viết `generate-testcase.py` theo skill `testcase-documenter`
- [x] Sinh `testcase.xlsx` — 106 TC / 8 section La mã, P0 = 61 (58%)

### Checkpoint — 2026-08-07 (Phase 6)
Vừa hoàn thành: `testcase.xlsx` (106 TC) + `generate-testcase.py` cho màn Danh mục ngân hàng.
Đang làm dở: không.
Bước tiếp theo: QA review file; cần chỉnh thì sửa `generate-testcase.py` rồi chạy lại (`python .plans/gop-db/banks-cut-mysql2/generate-testcase.py`).
Blocked: không.

### Điểm nghi vấn ghi nhận khi viết test case (chưa fix, chỉ để QA kiểm chứng)
- `BankService::getBanks` dòng 32-34: `where(name like)->orWhere(code like)` không bọc nhóm → kết hợp keyword + status/short_name có thể lọt bản ghi sai (TC_02.009, TC_02.010).
- `getBankBranches` dùng INNER JOIN `provinces` còn cột đếm chi nhánh dùng `with('branches')` → chi nhánh `province_id` null bị đếm nhưng không hiện trong modal (TC_06.019).

### Bug phát hiện & fix trong Phase 4
- **Race `editItem` → `$bvModal.show`**: set prop rồi show modal cùng tick khiến `@show` đọc `id` cũ (modal chi nhánh mở ra rỗng dù count > 0) → bọc `$nextTick` quanh mọi chỗ show modal có prop id (index.vue 3 chỗ + BankBranchesModel 2 chỗ)

### Ghi chú verify
- `use_erp = 1` trên DB local → các khối sync vừa bỏ TRƯỚC ĐÓ đang chạy thật (ghi trùng cùng bảng).
- Constructor override cũ của `BankBranch` nuốt mất `parent::__construct()` → trước fix, tạo chi nhánh qua
  `BankBranch::create()` không fill attribute (insert thiếu `name` NOT NULL sẽ lỗi SQL). Sau fix tạo OK.
- `TpBank.php` / `TpBankBranch.php` giữ nguyên file theo yêu cầu user — hiện 0 nơi tham chiếu.

## Phase 7 — Bộ tài liệu bàn giao theo skill mới (yêu cầu user 2026-08-17)

Xuất lại **testcase** theo form mẫu chuẩn (17 cột, 2 khối summary DNS/TP — bản cũ 15 cột)
và bổ sung **HDSD** + **SRS** cho màn `/human/banks`.

- [x] Rà lại code hiện tại trên `gop_db` (màn đã đổi sang V2Base: `pages/human/banks`, `Modules/Human`)
- [x] Chụp 17 ảnh thật trên cổng dev `hrm-crm.eteksofts.com` (1440x900) → `banks_shots/` (chỉ để local, `.gitignore` đã chặn)
- [x] `gen_testcase.py` (engine chung `tc_engine.py`) → `testcase.xlsx` — **164 TC / 1 nhóm quyền + 10 section La Mã, P0 = 95 (58%)**
- [x] `gen_srs.py` (`srs_docx_lib.py`) → `SRS - Danh mục ngân hàng.docx` — 12 chức năng FR-01…FR-12, 40 bảng, 22 ảnh (7 sơ đồ use case + 15 ảnh chụp thật)
- [x] `gen_hdsd.py` (`hdsd_engine.py`) → `HDSD_Danh muc ngan hang.docx` — 34 trang, 15 phần, 12 bảng, 17 ảnh thật
- [x] Kiểm: bộ kiểm tra thuật ngữ in "OK - khong con thuat ngu ky thuat"; mục lục + danh mục hình ảnh đã cho Word cập nhật thật rồi đọc lại (đúng heading của màn này); đếm direct formatting = đúng như file mẫu (heading 2, run trong ô bảng 0); `git status` không thấy `.png`
- [x] Xoá `generate-testcase.py` (bản 15 cột cũ) — giữ lại sẽ ghi đè `testcase.xlsx` bản mới khi chạy nhầm

### 3 lỗi phát hiện khi soát code để viết tài liệu (CHƯA FIX)

1. **Sắp xếp theo cột không có tác dụng** — `index.vue` gửi `sortBy`/`sortDesc`, `BankService::getBanks`
   chỉ đọc `sort_by`/`sort_desc` → luôn rơi về `banks.id desc`. Kiểm chứng trên cổng dev:
   `?sortBy=name&sortDesc=asc` trả về y hệt mặc định, `?sort_by=name&sort_desc=false` mới đổi thứ tự.
   Mũi tên trên tiêu đề cột vẫn đổi chiều nên nhìn như đang chạy.
2. **Cảnh báo "Thông tin chưa lưu" không hiện** — `BankModel.vue` đã gắn `unsavedModalMixin`
   (`@shown`/`@hide`) nhưng trên cổng dev đóng cửa sổ đang nhập dở vẫn đóng thẳng, mất dữ liệu.
   Cần kiểm tra lại mixin (hoặc bản deploy cũ hơn nhánh `gop_db`).
3. **Cột "Chi nhánh" lệch với popup Chi nhánh** — cột đếm qua `with('branches')` (đếm cả chi nhánh
   `province_id` null), popup dùng INNER JOIN `provinces` nên bỏ các chi nhánh đó. (Đã ghi nhận từ
   Phase 6, vẫn còn.)

Cả 3 đều đã được viết vào tài liệu: testcase ghi Expected Result theo hành vi ĐÚNG + gắn ⚠️ ở mục 9,
SRS ghi ở BR-09, HDSD ghi ở PHẦN 3 mục 7 / PHẦN 5 mục 8 / PHẦN 10 mục 8.

### Ghi nhận thêm về phân quyền

Màn `/human/banks` **không gắn quyền nào**: seeder không khai quyền cho danh mục ngân hàng, 10 route
`/human/banks` chỉ có `auth:api`, `master-data.js` để `isShow: true`. Mọi tài khoản đã đăng nhập đều
tạo/sửa/khóa/xóa được danh mục dùng chung này. Đã ghi rõ trong cả 3 tài liệu (testcase mục 7 + nhóm
TC-ROLE, SRS chương 3 + BR-07, HDSD PHẦN 2) — chờ nghiệp vụ quyết có siết lại không.

### Đợt chỉnh bố cục theo bộ tài liệu mẫu màn Danh mục khách hàng (2026-08-17)

Đối chiếu với `.plans/gop-db/customer-docs/` (SRS + HDSD + testcase của màn `/assign/customers`)
rồi sửa cho khớp. Font, khổ giấy, lề, màu heading vốn đã giống nhau (cùng engine trong skill);
khác nhau ở bố cục:

| Tài liệu | Đã sửa |
| --- | --- |
| testcase.xlsx | Tên sheet `DanhMucNganHang` → **`Trang tính1`**; tiêu đề khối A11 thêm hậu tố **“- Cập nhật ngày 17/08/2026”** |
| SRS | Thêm mục **“Mục lục” + trường TOC** ngay sau bảng thông tin bìa · bỏ đuôi “(FUNCTIONAL PACKAGING)” ở tên chương 5 · mỗi chức năng chuyển từ Heading 2 sang **Heading 3 dạng `5.2.N FR-0N — Tên`** · 65 mục con `5.2.x.y` chuyển từ Heading 3 sang **đoạn thường** · chương 6 thêm dòng **“Chức năng liên quan: …” cho TỪNG quy tắc** thay vì một dòng tổng ở cuối |
| HDSD | Gom bảng quyền vào **TỔNG QUAN mục 4** (4.1 Bảng quyền · 4.2 Phạm vi dữ liệu) · gộp đường dẫn truy cập vào mục 3 · bảng “Cập nhật tài liệu” đổi thành **4 cột** (thêm Người cập nhật) · phần phân quyền chuyển xuống **PHẦN 11 “HƯỚNG DẪN THEO TỪNG QUYỀN”** kèm mục “Câu hỏi thường gặp” · đánh số lại PHẦN 1…11 và sửa toàn bộ tham chiếu chéo |

Kết quả build lại: testcase 164 TC (không đổi) · SRS 40 bảng / 22 ảnh / 405 đoạn ·
HDSD 32 trang, 14 Heading 1, 11 bảng, 17 ảnh, mục lục + danh mục hình ảnh đã cho Word cập nhật thật.

⏸ **Đang chờ user**: user gửi thêm link form SRS
`https://docs.google.com/document/d/1jJRNSH0yR7nt3aQhkWOlCtYgJXC6HlxH/edit` nhưng tài khoản
`namdangit@gmail.com` không mở được (Drive báo không tìm thấy, WebFetch trả 401). User chốt
**để sau, khi nào bảo thì sửa tiếp**. Khi làm tiếp cần xin quyền xem doc đó, hoặc dùng bản form
đọc được trong Drive: **“SRS _Mẫu phiếu thu thập thông tin.docx”** (thư mục “Tài liệu SRS_QLDA_DANH MỤC”,
id `13WprLC0itjfdp0O8hmcqCEBnvGNOd3si`) — form đó khác bản hiện tại ở 3 điểm: chương 6 Business Rules
là **bảng 3 cột** (STT | Quy tắc | Mô tả chi tiết), mục 3.1 Danh sách quyền là **gạch đầu dòng**
(không phải bảng), và tiêu đề 5.2.x **không gắn mã FR**.

### Sinh lại SRS theo skill mới — form 4 chương (2026-08-17, sau khi kéo skill)

`srs-documenter` đã đổi bản mẫu sang **`SRS - Danh mục khách hàng.docx`** (user chỉnh tay rồi chốt)
và rút form từ 6 chương xuống **4 chương**. Đã viết lại `gen_srs.py` theo form mới:

| Nội dung | Thay đổi |
| --- | --- |
| Trang đầu | Bỏ dòng “Phân hệ: …” và **bỏ hẳn bảng thông tin trang bìa**; dùng `title_block()` — 2 dòng căn giữa 24pt, không phải Heading |
| Chương mục | Gộp còn 4: **Phần 1. Giới thiệu · Phần 2. Phân quyền · Phần 3. Đặc tả chi tiết · Phần 4. Quy tắc nghiệp vụ** |
| Đã bỏ | Mục “Phạm vi”, cả chương “Tổng quan”, mục “Quy tắc truy cập bắt buộc”, cả chương “Danh mục chức năng (Function list)”, mục **“Tiêu chí nghiệm thu”** của 12 chức năng, dòng “Chức năng liên quan: FR-xx”, 2 dòng “Menu:”/“Route (FE):” ở mục Layout |
| Đánh số | Chức năng chuyển sang `2.1 … 2.12` (**bỏ mã FR ở tiêu đề**, mã FR chỉ còn ở ma trận phân quyền); mục con chạy liên tục `2.x.1 → 2.x.5`, chức năng chỉ đọc bỏ “Biểu đồ Usecase” và lùi 1 bậc |
| Bảng giao diện | Rút cột theo loại chức năng: **8 cột** khi có nhập liệu · **7 cột** (bỏ “Bắt buộc”) cho Xem danh sách / Xem chi tiết / Lịch sử · **6 cột** (bỏ thêm “Phạm vi”) cho hộp thoại Khóa-Mở khóa và Xóa |
| Bảng Giới thiệu | Chức năng chỉ đọc truyền `dacbiet=None` → bỏ hẳn dòng “Yêu cầu đặc biệt” (7 dòng thay vì 8) |
| Phần 2 | Bảng “Nhóm quyền thao tác” (Ký hiệu / Tên quyền / Tác dụng) — màn không có quyền riêng nên 1 dòng “—” + 4 gạch đầu dòng nêu hiện trạng; KHÔNG có bảng “Nhóm quyền quyết định phạm vi dữ liệu” vì màn không phân quyền theo cấp; ma trận `Chức năng | Đã đăng nhập | Chưa đăng nhập` |

Kết quả build: **38 bảng · 251 đoạn · 23 ảnh** (8 sơ đồ use case + 15 ảnh chụp thật), sơ đồ ký tự = 0.
Generator có sẵn assert của skill Bước 4: sinh xong tự kiểm “không còn mục nào của form cũ” — đã in
`OK`. Đánh số 2.1 → 2.12 và 2.x.1 → 2.x.5 đã rà lại, liên tục, không nhảy số.

ℹ️ Đợt kéo skill này **chỉ đổi `srs-documenter`** (SKILL.md + SRS_MAU.docx + gen_srs_mau.py +
srs_docx_lib.py). `hdsd-documenter` và `testcase-documenter` không đổi → `HDSD_Danh muc ngan hang.docx`
và `testcase.xlsx` giữ nguyên bản đã căn theo bộ mẫu customer-docs.

### Đối chiếu trực tiếp file mẫu khách hàng — sửa 6 điểm lệch (2026-08-17)

User báo bản sinh theo SKILL.md vẫn chưa khớp `customer-docs/SRS - Danh mục khách hàng.docx`.
Đọc thẳng file mẫu bằng script của skill (duyệt `w:t` vì chữ trong ô bảng bị bọc `w:sdt` do đi qua
Google Docs) rồi so từng khối:

| Điểm lệch | Bản mẫu | Đã sửa |
| --- | --- | --- |
| Dòng “Menu: …” ở mục Layout | **VẪN CÒN** (11–12 lần, nằm cùng gạch đầu dòng với “URL đầy đủ”) | Viết helper `lay()` trong generator in đủ 2 gạch đầu dòng, không dùng `d.layout()` của lib (hàm đó chỉ in URL) |
| Nhãn mục con `2.x.y` | **IN ĐẬM**, là đoạn thường | Thêm helper `sub()` → `add_run(...).bold = True` |
| Tiêu đề `BR-0N — …` | **IN ĐẬM** | Dùng `sub()` cho cả 9 quy tắc |
| 2 dòng tiêu đề trang đầu | 24pt, căn giữa, **KHÔNG in đậm** | Bỏ `bold` mà `title_block()` của lib áp |
| Trường Mục lục | Để **RỖNG**, không có dòng “Nhấn chuột phải…” | `d.toc(note='')` |
| Chức năng đầu tiên | Gộp **“Truy cập và xem danh sách”** làm 1 mục (FR-01) | Gộp 2.1 + 2.2 cũ → còn **11 chức năng**, đánh số lại 2.1–2.11 và FR-01–FR-11 (ma trận + sơ đồ tổng quan + 7 biểu đồ use case) |

⚠️ **SKILL.md đang sai một chỗ** so với chính bản mẫu nó trỏ tới: mục “ĐÃ BỎ” ghi *bỏ cả 2 dòng
`Menu:` và `Route (FE):`*, nhưng file mẫu chỉ bỏ `Route (FE):`, **vẫn giữ `Menu:`**. Generator của
màn này bám FILE MẪU (giữ Menu). Nếu ai sửa skill thì sửa lại dòng đó — thuộc tài sản chung, phải
qua PR.

Kết quả build cuối: **36 bảng · 254 đoạn · 23 ảnh** (8 sơ đồ use case + 15 ảnh chụp thật).
Chuỗi khối (Heading / bảng / ảnh) của phần đầu và của từng chức năng đã trùng khớp bản mẫu.

### Mục lục SRS: cho Word cập nhật thật (2026-08-17)

`SrsDoc.toc()` chỉ **chèn trường TOC** — mở file lên thấy TRỐNG cho tới khi người đọc bấm
Update Field (bản mẫu `customer-docs` cũng đang trống y hệt). Đã bổ sung bước hậu xử lý trong
`gen_srs.py`: gọi Word qua PowerShell COM (`$doc.Fields.Update()` + `$toc.Update()` + `Repaginate`)
đúng cách `hdsd_engine` đang làm, nên file xuất ra đã có sẵn mục lục.

Kiểm chứng sau khi build: **22 dòng mục lục** (`toc 1`/`toc 2`/`toc 3`) kèm số trang thật —
Phần 1 tr.2 · Phần 2 tr.2 · Phần 3 tr.4 · 2.1→2.11 tr.4–30 · Phần 4 tr.32; tổng 34 trang.

### Checkpoint — 2026-08-17 (Phase 7)
Vừa hoàn thành: 3 tài liệu bàn giao cho màn Danh mục ngân hàng (testcase.xlsx 164 TC, SRS .docx, HDSD .docx) + 17 ảnh thật.
Đang làm dở: không.
Bước tiếp theo: user đọc 3 file; cần sửa nội dung thì sửa `gen_*.py` rồi chạy lại (`python .plans/gop-db/banks-cut-mysql2/gen_testcase.py|gen_srs.py|gen_hdsd.py`). Quyết định có fix 3 lỗi ở trên và có bổ sung quyền cho màn không.
Blocked: không.
