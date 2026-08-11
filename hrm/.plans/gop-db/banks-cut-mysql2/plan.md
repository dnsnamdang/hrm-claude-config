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
