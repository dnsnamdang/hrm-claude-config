# Plan — Danh mục Nhóm ngành: bổ sung Lĩnh vực kinh doanh nội bộ

**Design**: `.plans/danh-muc-nhom-nganh/design.md` · **Nhánh**: `linh-vuc-noi-bo`

## Ràng buộc toàn cục

- PHP 7.4 / Laravel 8 · Nuxt 2 (Node 14) · KHÔNG commit git.
- Màn `industry-groups` là màn CŨ → giữ nguyên cơ chế hiển thị lỗi (`formError` + viền đỏ), không
  đổi sang vee-validate cho cả form (chỉ thêm trường mới theo đúng kiểu đang có).
- File `.vue`/`.js` của hrm-client là **CRLF** → script sửa file phải mở `newline=''`.
- Nút không dùng được thì ẩn hẳn; cờ quyền fail-closed.

## Phase 1 — Backend

### Task 1: Migration + backfill
- [x] **B1.** Migration `2026_08_22_000002_add_internal_business_scope_id_to_scopes_table.php`: thêm cột nullable + index (KHÔNG bọc `DB::transaction`).
- [x] **B2.** Backfill trong cùng migration: `firstOrCreate` LVKDNB `LVKDNB.KHAC` / "Khác" (`created_by`/`updated_by` = nhân viên có email `namdangit@gmail.com`, tra theo email, không viết cứng id) → update mọi `scopes` chưa có giá trị.
- [x] **B3.** `down()`: chỉ drop cột (không xoá bản ghi danh mục).
- [x] **B4.** Chạy migrate, kiểm `select count(*) from scopes where internal_business_scope_id is null` = 0.

### Task 2: Entity + ràng buộc
- [x] **B1.** `Scope`: thêm `internal_business_scope_id` vào `$fillable` + quan hệ `internalBusinessScope()`.
- [x] **B2.** `InternalBusinessScope`: quan hệ `scopes()` (hasMany) + sửa `isCanDelete()` (không còn scope tham chiếu) + thêm `isCanLockUpdate()` (không còn scope ACTIVE).
- [x] **B3.** `InternalBusinessScopeController`: guard `delete` (400 nếu đang dùng) + guard `lock` (400 nếu còn scope hoạt động); Resource trả thêm `is_can_lock_update` + `scopes_count`.
- [x] **B4.** `getAll` của LVKDNB nhận `include_ids` → trả kèm bản ghi đang chọn dù đã khoá, kèm cờ `is_locked`.

### Task 3: Validate + Service + Resource + Export
- [x] **B1.** `ScopeRequest`: `internal_business_scope_id` required|integer + closure kiểm tồn tại & đang Hoạt động; ngoại lệ giữ nguyên giá trị cũ khi Sửa.
- [x] **B2.** `ScopeService::index`: filter `internal_business_scope_id` + eager load quan hệ; `updateOrCreate`/`update` lưu field.
- [x] **B3.** `ScopeResource` + `DetailScopeResource`: trả `internal_business_scope_id`, `internal_business_scope_name`, object `{id,name,is_locked}`.
- [x] **B4.** Blade `exports/scopes.blade.php`: thêm cột "Lĩnh vực kinh doanh nội bộ" sau Tên nhóm ngành (đổi `colspan` cho khớp).
- [x] **B5.** Import BE: validate + map cột mã LVKDNB (bắt buộc, phải tồn tại & đang hoạt động).
- [x] **B6.** Smoke test API bằng curl: tạo/sửa thiếu lĩnh vực → 422; lọc theo lĩnh vực; xoá LVKDNB đang dùng → 400.

## Phase 2 — Frontend

### Task 4: Modal Thêm/Sửa Nhóm ngành
- [x] **B1.** Thêm `V2BaseSelectInModal` "Lĩnh vực kinh doanh nội bộ" + `<Required />`, chọn 1.
- [x] **B2.** Nạp options từ `assign/internal-business-scopes/getAll` (kèm `include_ids` khi sửa) — chỉ gọi khi mở modal (lazy).
- [x] **B3.** Gửi `internal_business_scope_id` khi lưu; map lỗi 422 vào `formError` hiển thị inline.
- [x] **B4.** Chế độ Xem: disabled, vẫn hiện đúng tên kể cả khi lĩnh vực đã khoá.

### Task 5: Danh sách + bộ lọc + import
- [x] **B1.** Thêm cột "Lĩnh vực kinh doanh nội bộ" sau cột Mã - Tên, ô trống `—`.
- [x] **B2.** Thêm ô lọc select trong Tìm kiếm nâng cao (`Chọn lĩnh vực kinh doanh nội bộ`), chạy auto-search như các ô khác của màn.
- [x] **B3.** Import: thêm cột "Mã lĩnh vực kinh doanh nội bộ" vào `importColumns` + rule FE + map payload.
- [x] **B4.** Cập nhật `static/Mau_import_NhomNganh.xlsx` (sinh lại bằng PhpSpreadsheet, thêm cột + dòng mẫu dùng mã có thật).

## Phase 3 — Kiểm thử

### Task 6: Verify + E2E
- [x] **B1.** Playwright MCP: form bắt buộc chọn lĩnh vực · cột hiển thị · lọc đúng · nút Xoá của LVKDNB đang dùng bị ẩn.
- [x] **B2.** E2E spec: bổ sung ca cho màn Nhóm ngành + ca ràng buộc chặn xoá/khoá LVKDNB (API).
- [x] **B3.** Chạy toàn bộ e2e liên quan, dọn dữ liệu test.
- [x] **B4.** Cập nhật plan/STATUS + báo kết quả.

## Phase 4 — Chỉnh UI theo phản hồi (2026-08-23)

### Task 7: Bố trí lại form Thêm/Sửa Nhóm ngành
- [x] **B1.** Hàng 1: Mã (col-md-4) + Tên (col-md-8) — trước là 3/6/3.
- [x] **B2.** Hàng 2: Lĩnh vực kinh doanh nội bộ (col-md-8) + Trạng thái (col-md-4) — bỏ dòng riêng col-md-9 bị cụt.
- [x] **B3.** Hàng 3: Mô tả giữ col-md-12.
- [x] **B4.** Verify bằng Playwright MCP (đúng 3 hàng 4/8 · 8/4 · 12) + chạy lại e2e 6/6 PASS.

---

### Task 8: Tài liệu test case cho QA
- [x] **B1.** Viết generator `.plans/danh-muc-nhom-nganh/gen_testcase.py` dùng engine chung `tc_engine.py` (3 khối CONFIG, không nhân bản code dựng Excel).
- [x] **B2.** 9 mục mô tả tính năng (mục 9 liệt kê 7 bẫy dễ sai của lần thay đổi này).
- [x] **B3.** 6 TC phân quyền (đủ 4 tên quyền + không quyền nào + 2 ca bỏ qua giao diện) + 10 section nghiệp vụ đánh số La Mã.
- [x] **B4.** Sinh `testcase.xlsx`: **56 TC, P0 = 31 (55%)**, bộ kiểm tra thuật ngữ in "OK - sạch", không trùng TC ID, có header 17 cột, dropdown DNS/TP, không dùng freeze panes.

---

## Checkpoint

### Checkpoint — 2026-08-23 (wrap up)
Vừa hoàn thành: 8/8 task — BE + FE + E2E + bố trí lại form theo phản hồi + tài liệu test case cho QA.
Bằng chứng: **E2E 24/24 PASS** (6 ca API của liên kết Nhóm ngành ↔ Lĩnh vực KD nội bộ + 18 ca danh mục
LVKDNB); verify UI thật bằng Playwright MCP; `testcase.xlsx` 56 TC (P0 55%), bộ kiểm tra thuật ngữ sạch.
Trạng thái DB local sau khi dọn: 22 nhóm ngành (0 bản ghi thiếu lĩnh vực), 3 lĩnh vực
(AUTO / ELEC là dữ liệu demo lúc dựng màn, KHAC do migration tạo), không còn bản ghi rác E2E.
Đang làm dở: không.
Bước tiếp theo: user rà giao diện + QA chạy `testcase.xlsx`. Khi đưa lên môi trường khác: chạy
migration thêm cột lĩnh vực cho Nhóm ngành (tự tạo LVKDNB.KHAC + backfill toàn bộ nhóm ngành cũ).
Blocked: không.

## Việc chưa làm (chờ user quyết)

- Test case riêng cho **màn Danh mục Lĩnh vực kinh doanh nội bộ** (màn mới, hiện chỉ có e2e tự động,
  chưa có file .xlsx cho QA) — theo skill thì mỗi màn 1 file riêng.
- SRS `.docx` cho cả 2 màn: chưa tạo (chỉ tạo khi được yêu cầu).
- Warning có sẵn của màn Nhóm ngành: ô Mô tả nhận số dòng ở dạng chữ nên console cảnh báo mỗi lần
  mở cửa sổ — không thuộc phạm vi thay đổi này, chờ user quyết có sửa kèm không.
