# Đồng bộ nút Chi tiết ↔ Danh sách (10 màn luồng kho) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans để thực thi plan theo từng task. Các bước dùng checkbox (`- [ ]`) để theo dõi.

**Goal:** Màn Xem chi tiết của 10 phiếu luồng kho hiển thị đúng tập nút như danh sách cho cùng bản ghi (cả tập nút lẫn điều kiện ẩn/hiện), nút "Quay lại" luôn cuối, footer dùng `V2Footer`.

**Architecture:** Thuần FE cho 8/10 màn (di cư footer `.export-actionbar` → `V2Footer`, bổ sung nút thiếu 2 chiều, đồng bộ điều kiện). Hai màn YCXH & YCNH thêm phần BE: Resource danh sách trả thêm cờ `is_can_*_approve` (đang có ở detail) để danh sách ẩn/hiện nút Duyệt đúng; nút Duyệt ở danh sách chỉ **điều hướng** sang chi tiết (không duyệt tại chỗ).

**Tech Stack:** Nuxt 2.14 / Vue 2 / Bootstrap-Vue (hrm-client); PHP 7.4 / Laravel 8 Resource (hrm-api). Nghiệm thu bằng Playwright MCP.

**Spec:** `HRM/.plans/dong-bo-nut-chi-tiet-danh-sach/design.md`

## Global Constraints (copy từ HRM/CLAUDE.md — áp cho MỌI task)

- Nhánh đích: `develop`. **KHÔNG commit, KHÔNG push** (trừ khi user yêu cầu).
- Footer màn chi tiết/form BẮT BUỘC trong `V2Footer`; nút không có key sẵn → slot `#custom-actions`; **không tự thêm "Quay lại"** (V2Footer tự render cuối).
- Nút không dùng được → **ẩn** (`v-if`/`visible`), **KHÔNG** `interactable + disabledTitle`.
- Cờ quyền **fail-closed**: mặc định `false`, chỉ set từ `$store.state.permissions` hoặc field BE. CẤM `can... = true`.
- Element form màn mới = `V2Base*`; nút = `V2BaseButton`/`V2BaseIconButton`. Không HTML thô.
- Nút cùng cụm: `class="mr-2 mb-2"`, nút CUỐI cụm chỉ `mb-2` (cách nhau 12px).
- Chi tiết chỉ được thiếu so với danh sách: "Xem" và "Lịch sử" (nếu đã nhúng `SystemInfoSection`).
- Số định dạng quốc tế (`,` nghìn `.` thập phân) — giữ nguyên, không regress.
- BE Resource: eager-load/`withCount`, CẤM N+1; chỉ trả cờ chỉ-đọc, không đổi nghiệp vụ/validation.
- Tài liệu ghi ở `HRM/.plans/...` qua symlink.

## Review Focus (các điểm dễ gây lỗi — gắn kiểm ở task tương ứng)

1. **Nút Duyệt trên danh sách hiện SAI khi bản ghi không đủ điều kiện** (cờ BE thiếu → fail-open hoặc fail-closed-sai). → kiểm ở Task 1 (YCXH) & Task 5 (YCNH): mở ≥1 bản ghi KHÔNG được duyệt, nút Duyệt phải ẩn ở cả 2 màn.
2. **Di cư V2Footer làm đứt handler** — nút In/Xuất Excel/Tạo HĐ bấm không ra gì. → mọi task footer: bước verify phải *bấm thật* mỗi nút custom và xác nhận có hành động.
3. **"Quay lại" không ở cuối** sau khi dồn nút vào `#custom-actions`. → mọi task footer: verify thứ tự DOM, "Quay lại" là nút cuối.
4. **Bản ghi đã khóa/đã duyệt: điều kiện ẩn/hiện lệch list↔detail.** → mỗi task: kiểm thêm 1 bản ghi ở trạng thái khác (đã duyệt/đã hủy), 2 màn phải khớp.
5. **BE thêm cờ `is_can_*_approve` gây N+1** trên danh sách. → Task 1 & 5: verify số query danh sách không tăng theo số dòng (Laravel Telescope/`DB::listen` hoặc đọc log), dùng accessor eager-load.

---

## Khuôn chung di cư footer → V2Footer (các task footer tham chiếu, KHÔNG lặp lại)

Áp cho bất kỳ task nào có `[FOOTER]`. Thực hiện trong `_id/index.vue` của màn:

1. Đọc danh sách nút của **danh sách** cho bản ghi: `getRowActions(item)` / mảng `rowActions` / `components/row-actions.js`. Ghi ra tập nút + điều kiện `visible`/`v-if` của từng nút.
2. Xóa `<div class="export-actionbar">…</div>` và SCSS `.export-actionbar` liên quan.
3. Thêm `<V2Footer :url-back="urlBack" :menu="footerMenu">` + slot `#custom-actions`:
   - Nút có key sẵn trong `V2Footer.menu` (`edit/print/approve/delete/cancel/...`) → set qua `footerMenu` (giá trị = biểu thức điều kiện, fail-closed).
   - Nút KHÔNG có key (Xuất Excel, Tạo HĐ, "Lập phiếu…", biến thể In nhiều loại, nút điều hướng pick/re-export…) → đặt trong `#custom-actions` bằng `V2BaseButton` (class `mr-2 mb-2`), nối `@click` về handler đã có.
4. Chuyển mỗi điều kiện ẩn/hiện từ danh sách sang đúng nút (cùng biểu thức). KHÔNG tự thêm "Quay lại".
5. `urlBack` computed trỏ về nơi user đi vào (giữ query nếu có).

**Verify chung mỗi task footer (Playwright MCP, `http://127.0.0.1:3000`):**
- Mở danh sách, chọn 1 bản ghi, ghi tập nút hành động của dòng đó.
- Mở chi tiết cùng bản ghi: tập nút footer = tập nút danh sách (trừ Xem/Lịch sử), **"Quay lại" là phần tử cuối**.
- Bấm thật từng nút custom (In/Xuất…) → có hành động/popup đúng.
- Lặp với 1 bản ghi trạng thái khác (đã duyệt/đã hủy) → 2 màn vẫn khớp.
- Mỗi task KHÔNG commit.

---

## Task 1: YCXH — product-export-requests (BE cờ duyệt + detail In/Xuất + list điều hướng duyệt)

**Files:**
- Modify (BE): Resource danh sách YCXH trong `HRM/hrm-api/Modules/.../ProductExportRequest*` (grep `is_can_manager_approve` để tìm accessor/Resource detail đang dùng).
- Modify (FE list): `pages/finance/product-export-requests/index.vue` (rowActions ~663-688).
- Modify (FE detail): `pages/finance/product-export-requests/components/ProductExportRequestForm.vue` (V2Footer ~1591-1682; nút duyệt ~1631-1667).

**Interfaces:**
- Produces (BE→FE): list row có thêm `is_can_manager_approve`, `is_can_board_approve` (bool), tính bằng cùng accessor Entity như detail.

- [ ] **Step 1 (BE):** Thêm `is_can_manager_approve`, `is_can_board_approve` vào Resource danh sách YCXH, tái dùng accessor Entity đang dùng ở detail; eager-load quan hệ cần thiết ở query danh sách (tránh N+1).
- [ ] **Step 2 (BE verify):** Gọi API danh sách, xác nhận mỗi dòng có 2 cờ; so 1 dòng với giá trị cờ ở detail cùng bản ghi — phải trùng. Kiểm số query không tăng theo số dòng.
- [ ] **Step 3 (FE detail):** Trong `#custom-actions` của `ProductExportRequestForm.vue` thêm các nút **In (các biến thể)** + **Xuất Excel** (đọc handler/biến thể In từ `index.vue` để nối đúng), class `mr-2 mb-2`.
- [ ] **Step 4 (FE list):** Thêm vào rowActions danh sách: **Lập phiếu xuất hàng** + **Chuyển BGĐ duyệt / BGĐ duyệt / Không duyệt**. Nút duyệt `@click` = `$router.push` sang chi tiết (không duyệt tại chỗ); `visible` = cờ `is_can_*_approve` tương ứng (fail-closed). Lập phiếu xuất hàng nối handler/điều hướng như chi tiết.
- [ ] **Step 5 (COND):** Nút "Lập ĐNXK" (cả 2 màn) bổ sung điều kiện `is_export_direct !== 1` cho khớp.
- [ ] **Step 6 (verify):** Playwright — bản ghi đủ điều kiện duyệt: list hiện nút duyệt, bấm → sang đúng chi tiết; chi tiết có In/Xuất, "Quay lại" cuối. Bản ghi KHÔNG đủ điều kiện duyệt: nút duyệt **ẩn** ở cả 2 màn. Tập nút 2 màn khớp (trừ Xem/Lịch sử).
- [ ] **Step 7:** KHÔNG commit. Báo tập nút quan sát được ở 2 màn.

## Task 2: ĐNXK — warehouse-export-requests `[FOOTER]`

**Files:** Modify `pages/finance/warehouse-export-requests/_id/index.vue` (export-actionbar ~231-255), `pages/finance/warehouse-export-requests/index.vue`.

- [ ] **Step 1:** Di cư footer theo **Khuôn chung**.
- [ ] **Step 2 (D←L):** Thêm 2 nút **In** còn thiếu vào chi tiết.
- [ ] **Step 3 (L←D):** Nếu chi tiết có **Hủy** mà danh sách thiếu → thêm vào danh sách (cùng điều kiện).
- [ ] **Step 4 (verify):** theo Verify chung. KHÔNG commit.

## Task 3: PXK — warehouse-exports `[FOOTER]`

**Files:** Modify `pages/finance/warehouse-exports/_id/index.vue` (export-actionbar ~85-124).

- [ ] **Step 1:** Di cư footer theo **Khuôn chung**; giữ các nút điều hướng sang `pick`/`re-export` trong `#custom-actions`.
- [ ] **Step 2 (verify):** theo Verify chung, có bấm thật nút pick/re-export. KHÔNG commit.

## Task 4: PXH — product-exports `[FOOTER]`

**Files:** Modify `pages/finance/product-exports/_id/index.vue` (export-actionbar ~376-388).

- [ ] **Step 1:** Di cư footer theo **Khuôn chung**.
- [ ] **Step 2 (verify):** theo Verify chung. KHÔNG commit.

## Task 5: YCNH — product-import-requests (BE cờ duyệt + list điều hướng duyệt)

**Files:**
- Modify (BE): Resource danh sách YCNH (`HRM/hrm-api/Modules/.../ProductImportRequest*`).
- Modify (FE list): `pages/finance/product-import-requests/index.vue` (~657-697).
- Detail `_id/index.vue` **đã dùng V2Footer** (~408-481) — không di cư; nút "Sửa" chi tiết đã ẩn đúng (`footerMenu.edit`, ~752) — **không sửa**.

**Interfaces:**
- Produces (BE→FE): list row có `is_can_approve_by_manager`, `is_can_control_board_approve`, `is_can_board_of_manager_approve` (bool), cùng accessor như detail (~415-434).

- [ ] **Step 1 (BE):** Thêm 3 cờ trên vào Resource danh sách YCNH, tái dùng accessor Entity, eager-load tránh N+1.
- [ ] **Step 2 (BE verify):** mỗi dòng có 3 cờ; so 1 dòng với detail; số query không tăng theo số dòng.
- [ ] **Step 3 (FE list):** Thêm 5 nút duyệt/không duyệt (BKS duyệt, Chuyển BGĐ, BGĐ duyệt, Không duyệt…) vào rowActions; `@click` = `$router.push` sang chi tiết để duyệt (vì cần lưới nhập giá); `visible` = cờ tương ứng (fail-closed).
- [ ] **Step 4 (verify):** Playwright — bản ghi đủ điều kiện: list hiện nút, bấm → sang chi tiết đúng; chi tiết có lưới nhập giá để duyệt. Bản ghi không đủ điều kiện: nút ẩn ở cả 2 màn. Tập nút 2 màn khớp.
- [ ] **Step 5:** KHÔNG commit.

## Task 6: ĐNNK — warehouse/import-requests `[FOOTER]`

**Files:** Modify `pages/warehouse/import-requests/_id/index.vue` (export-actionbar ~180-210, SCSS ~493-524).

- [ ] **Step 1:** Di cư footer theo **Khuôn chung** (xóa cả SCSS `.export-actionbar`).
- [ ] **Step 2 (verify):** theo Verify chung. KHÔNG commit.

## Task 7: PNK — warehouse-imports `[FOOTER]`

**Files:** Modify `pages/finance/warehouse-imports/_id/index.vue` (export-actionbar ~174-194, computed `barActions` ~296-301). List + detail cùng dùng `components/row-actions.js`→`warehouseImportRowActions(item)` (tập nút đã đồng bộ).

- [ ] **Step 1:** Di cư footer theo **Khuôn chung**; map `barActions` sang `footerMenu`/`#custom-actions`, giữ nguyên tập nút từ `warehouseImportRowActions` (không đổi điều kiện).
- [ ] **Step 2 (verify):** theo Verify chung, đặc biệt xác nhận tập nút 2 màn khớp (cùng nguồn). KHÔNG commit.

## Task 8: PNH — product-imports (L←D: Phân bổ hàng)

**Files:** Modify `pages/finance/product-imports/index.vue`. Detail `_id/index.vue` (~574-590) đã V2Footer — giữ nguyên.

- [ ] **Step 1 (L←D):** Thêm nút **Phân bổ hàng** vào rowActions danh sách, nối handler/điều hướng + điều kiện `visible` giống nút ở chi tiết.
- [ ] **Step 2 (verify):** Playwright — bản ghi có Phân bổ hàng: hiện ở cả 2 màn, bấm ở list ra đúng hành động; bản ghi không đủ điều kiện: ẩn cả 2. KHÔNG commit.

## Task 9: YCXBHM — borrow-sell-requests `[FOOTER]` + detail Sửa

**Files:** Modify `pages/finance/borrow-sell-requests/_id/index.vue` (export-actionbar ~212-248), tham chiếu `index.vue`.

- [ ] **Step 1:** Di cư footer theo **Khuôn chung**.
- [ ] **Step 2 (D←L):** Thêm nút **Sửa** vào chi tiết (list có, detail thiếu), cùng điều kiện `visible` như list.
- [ ] **Step 3 (verify):** theo Verify chung, xác nhận Sửa hiện/ẩn khớp list. KHÔNG commit.

## Task 10: PXBHM — borrow-sells `[FOOTER]` + In bỏ gate

**Files:** Modify `pages/finance/borrow-sells/_id/index.vue` (export-actionbar ~390-402; gate In ~397), tham chiếu `index.vue` (~616-640).

- [ ] **Step 1:** Di cư footer theo **Khuôn chung**.
- [ ] **Step 2 (COND):** **Bỏ** điều kiện `is_can_view` ở nút In chi tiết → In luôn hiện (khớp danh sách luôn hiện).
- [ ] **Step 3 (verify):** theo Verify chung; xác nhận In hiện ở cả 2 màn với bản ghi bất kỳ (kể cả khi trước đây `is_can_view=false`). KHÔNG commit.

## Task 11: Dọn nút disabled-hiện trên 10 màn danh sách `[COND]`

**Files:** Modify 10 file `index.vue` của các màn ở §5 design (chỉ các dòng có `interactable` + `disabledTitle`).

- [ ] **Step 1:** Grep `disabledTitle`/`interactable` trong 10 `index.vue`; mỗi nút như vậy → chuyển điều kiện vào `v-if`/`visible` để ẩn hẳn (ví dụ "Sửa" list YCNH ~682-683). KHÔNG đổi điều kiện nghiệp vụ, chỉ đổi cách thể hiện (xám→ẩn).
- [ ] **Step 2 (verify):** Playwright — với bản ghi mà trước đây nút bị xám: nút nay **ẩn** ở danh sách, khớp chi tiết (chi tiết đã ẩn). Grep lại 10 file: không còn `disabledTitle` cho nút thao tác đổi dữ liệu.
- [ ] **Step 3:** KHÔNG commit.

---

## Prerequisite cho mọi bước verify

- Chạy HRM local (skill `run-hrm`): MySQL `erp_hrm_check` → API `:8000` → Nuxt `http://127.0.0.1:3000`.
- Playwright MCP mở `http://127.0.0.1:3000` (KHÔNG `localhost`), KHÔNG `pkill -f mcp-chrome`.
- Cần tài khoản có quyền thấy các nút (đăng nhập có sẵn trong `e2e/.auth/user.json`).

## Ghi chú thực thi

- Thứ tự gợi ý: Task 2,3,4,6,7 (footer thuần, dễ) → 8,9,10 (FE nhẹ) → 1,5 (có BE) → 11 (quét cuối, sau khi các màn đã ổn).
- Task 1 & 5 có BE: nếu không tìm thấy accessor `is_can_*_approve` ở Entity (chỉ tính inline trong controller/detail) → dừng, hỏi user trước khi tách accessor dùng chung (sửa hàm dùng chung phải hỏi).
