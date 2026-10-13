# RESUME — Bàn giao để tiếp tục ở hội thoại mới

> File này là **điểm vào duy nhất** khi mở lại task. Đọc file này trước, rồi mới đọc
> `design.md` · `design-phase1.md` · `be-spec-per-type.md` · `plan.md` cùng thư mục.
> Cập nhật lần cuối: **08/10/2026**.

---

## 0. CÁCH GỌI LẠI Ở HỘI THOẠI MỚI (copy nguyên câu dưới cho Claude)

> Tiếp tục task **rework form Phiếu nhập hàng HRM** (ERP→HRM port). Đọc trước
> `HRM/.plans/gop-db/product-import-form-rework/RESUME.md` rồi làm tiếp **Cụm 1** đúng
> như mục "VIỆC ĐANG LÀM DỞ" trong đó. Quyền hạn: tôi đã giao toàn quyền tự đánh giá/
> quyết định/tự kiểm (Playwright), tôi chỉ nghiệm thu — KHÔNG dừng giữa chừng hỏi duyệt
> từng cụm. KHÔNG commit/push khi tôi chưa yêu cầu.

Working dir: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client`. Dev server: http://127.0.0.1:3000.

---

## 1. YÊU CẦU GỐC (nguyên văn user)

> "phiếu nhập hàng form tạo mới có ô cho phép chọn phiếu nhập kho và thay đổi được phiếu,
> thông tin các trường thay đổi tuỳ theo loại nhập hàng, box chi tiết chứa thông tin hàng
> hoá cũng vậy, các tab cũng vậy, các cột trong tab hàng hoá cũng vậy sẽ thay đổi theo loại
> nhập hàng. Rà soát lại phiếu nhập hàng đã port từ ERP sang HRM hiện có và sửa lại logic cho
> đúng, tôi muốn giống hết kể cả về bố cục form… chỗ danh mục kho kế toán ở đây lấy không cần quyền."

**Grant toàn quyền (nguyên văn):** "tôi giao toàn bộ cho bạn tự đánh giá và quyết đinh + tự
kiểm tra tôi chỉ nghiệm thu thôi vì đây chỉ là task port erp sang logic đã có sẵn bạn hãy tự
tìm hiểu và làm cho đúng, đầy đủ" → tự làm + tự verify, KHÔNG gate duyệt từng cụm.

---

## 2. QUYẾT ĐỊNH ĐÃ CHỐT (không bàn lại)

- **UI = Hướng A**: khớp ERP về **nghiệp vụ/cấu trúc thông tin** (đủ trường/tab/cột/hạch toán,
  động theo loại) nhưng **dựng bằng component HRM** (V2Base*, V2Footer, badge HRM, số kiểu
  `1,234,567.89`). KHÔNG bê layout AngularJS của ERP.
- **Phạm vi = 8 loại tạo tay**: `2` Mua trong nước · `3` Mượn trả lại · `4` Bán trả lại ·
  `9` Nhập bán mượn trả lại · `11` Mua nước ngoài mới · `14` Nhập gửi · `15` Mua trong nước tự do ·
  `99` Khác. (10 loại tự sinh 1,5,6,7,8,10,12,13,16,17,20 KHÔNG đưa vào form tạo tay.)
- **Chia 3 cụm, KHÔNG gate duyệt từng cụm**:
  - **Cụm 1** = khung động + loại `4` (loại duy nhất `supported:true`, BE đang chạy).
  - **Cụm 2** = `2`, `15`, `99` (biến thể VAT B).
  - **Cụm 3** = `11` (nước ngoài A/currency), `3`, `9`, `14` (cột hạn gửi + chỉ kho ký gửi).
- **Danh mục kho kế toán KHÔNG cần quyền**: endpoint đã ungated sẵn trên `gop_db`. Danh mục rỗng =
  lỗi DATA (thiếu warehouse_id/company_id), KHÔNG phải lỗi quyền → giữ cờ `accWarehouseCatalogOk`.

---

## 3. TIẾN ĐỘ

### ĐÃ XONG
- [x] Điều tra ERP + brainstorming (HARD-GATE đã qua, user duyệt design Cụm 1 + trao toàn quyền).
- [x] Viết đủ 4 design docs cùng thư mục (`design.md`, `design-phase1.md`, `be-spec-per-type.md`, `plan.md`).
- [x] **Tạo `pages/finance/product-imports/constants/importTypeConfig.js`** (201 dòng) — HOÀN CHỈNH,
      khai đủ 8 loại, chỉ loại 4 `supported:true`. Export `TABLE_VARIANT`, `IMPORT_TYPE_CONFIG`, `getTypeConfig`.

### VIỆC ĐANG LÀM DỞ (Cụm 1 — bước tiếp theo NGAY)
Chưa sửa dòng nào trong `ProductImportForm.vue`. Cần làm, theo thứ tự:

**A. Script (`ProductImportForm.vue`):**
1. `import { getTypeConfig } from '../constants/importTypeConfig'`; import + register
   V2BaseSelect, V2BaseCurrencyInput, V2BaseIconButton, V2BaseFormSection, V2Footer, V2BaseTableScroll.
2. Thêm computed: `cfg()` = `getTypeConfig(this.header.import_type)`; `isTypeSupported()` =
   `!!(this.cfg && this.cfg.supported)`; `cols()` = các cờ nhóm cột (gate `canViewCostPrice && cfg.columns[group]`);
   đổi `prodColCount` sang tính động từ `cols`. Thêm method `hasTab(key)`.
3. Thêm `canChangeSource()` = `mode==='create' && header.status === STATUS_DANG_TAO` +
   method `changeWarehouseImportSource()` / `changeRequestSource()`: `await this.$confirm({message:
   'Đổi phiếu nhập kho sẽ nạp lại toàn bộ danh sách hàng hoá và danh mục kho kế toán. Tiếp tục?'})`
   → `$refs.warehouseImportModal.show()` / `$refs.requestModal.show()`.
4. `save()`: thêm `$safeLoadingStart()/Finish()` (finally); nhánh Duyệt thêm `$confirm()` **gọi tên phiếu**
   (vì auto-confirm của V2Footer chung chung → dùng `#custom-actions` + `$confirm()`).

**B. Template:**
5. Thêm nút đổi nguồn (V2BaseIconButton `ri-edit-line`) cạnh dòng PNK (dòng 67) / ĐNNK (dòng 68),
   chỉ hiện khi `canChangeSource`.
6. Render cả 2 source modal LUÔN (ngoài chuỗi v-if/v-else) để ref tồn tại ở view form.
7. Tab `<b-tab>` theo `hasTab('inlandCost')`/`hasTab('pickupCost')` (vẫn `&& canViewCostPrice`);
   tiêu đề tab hàng hoá = `cfg.goodsTabTitle`.
8. Bọc mỗi nhóm cột giá trong `v-if="cols.X"`.
9. Convert HTML thô → V2Base:
   - `<select>` kho kế toán (dòng **170-177**) → **V2BaseSelect** (inline, `:value`/`@change`).
   - `<input type="number">` SL (dòng **181-186**) → **V2BaseCurrencyInput** (clamp `max` TRONG component).
   - `.btn-acc-add`/`.btn-acc-remove` (dòng **189-194**) → **V2BaseIconButton**.
   - 2 thanh `.export-actionbar` (dòng **39-47** và **248-288**) → **V2Footer** + slot `#custom-actions`.
10. `!isTypeSupported` → callout "Loại nhập hàng chưa được hỗ trợ" + ẩn nút Lưu/Duyệt.
11. Fix dòng **199** `text-muted` (ĐỎ) → `#6b7280`.

**C. Fix 3 GAP map `import_type` (quan trọng — nếu không, cfg luôn null):**
12. `loadForEdit()` (dòng 642-720): thêm `this.header.import_type = d.type ?? null`.
13. `loadFromRequest()` (dòng 591-614): thêm `this.header.import_type = src.type ?? null`.
14. `applyHeaderDisplayFromSource()` nhánh ĐNNK else (dòng ~751): thêm `this.header.import_type = src.type ?? this.header.import_type`.
    (`loadFromWarehouseImport` dòng 568 và nhánh direct dòng 734 ĐÃ set đúng — không đụng.)

**D. Tự kiểm:**
15. Grep HTML thô phải RỖNG:
    `grep -rn '<input \|<textarea\|<select \|<button \|class="btn \|class="form-control' pages/finance/product-imports/ | grep -v V2Base`
16. Playwright verify tại http://127.0.0.1:3000 theo `design-phase1.md §7` (6 bước — KHÔNG báo xong
    khi chưa bấm thật). Luôn mở `127.0.0.1:3000` (KHÔNG `localhost` — token auth ở origin 127.0.0.1).

### CHƯA LÀM
- [ ] Cụm 2 (BE `buildDetailsByType`/`store()` loại 2,15,99 + FE bật `supported`).
- [ ] Cụm 3 (BE loại 11/3/9/14 + FE biến thể A/currency, cột hạn gửi, lọc kho ký gửi).

---

## 4. FILE & ANCHOR QUAN TRỌNG (đã verify còn đúng)

- **FE target chính:** `pages/finance/product-imports/components/ProductImportForm.vue` (1318 dòng, CHƯA sửa).
  - `.export-actionbar` 2 chỗ: 39-47 (picker) và 248-288 (form). Bar 248-288: Lưu nháp (255-264,
    `save(STATUS_DANG_TAO)`), Lưu và tiếp tục (266-276, create-only), Duyệt (277-286, `save(STATUS_DA_HOAN_THANH)`).
  - Hằng (305-307): `API_BASE='finance/product-imports'`, `STATUS_DA_HOAN_THANH=1`, `STATUS_DANG_TAO=3`.
  - `header.import_type` (dòng 355), `import_type_name` (356); `canViewCostPrice` (341, từ perm 'Xem giá vốn hàng hoá').
  - Method tính giá (round2/rowSupplierAmount/rowPriceAfterExtra/rowDiscountPrice/rowTotalAmountAllocated/
    rowVatCostAllocated… dòng 827-857), allocation (860-876), buildFormData (931-963), save (981-1009) — GIỮ NGUYÊN hợp đồng, chỉ di chuyển chỗ gọi theo cột động.
  - Source modal: `WarehouseImportSearchModal.show()`, `ProductImportRequestSearchModal.show()`,
    emit `@choose` item có `.id`. Handler sẵn: `onChooseWarehouseImport` (624), `onChooseProductImportRequest` (633) — tái dùng cho nút đổi nguồn.
- **Config:** `pages/finance/product-imports/constants/importTypeConfig.js` (XONG).
- **Component contract đã verify:**
  - `V2BaseSelect`: `:value`/`@change`/`options` ([{id/value, name/label/text}]); `allowClear` default true; inline (KHÔNG phải trong modal nên KHÔNG dùng V2BaseSelectInModal).
  - `V2BaseCurrencyInput`: `:value`/`@input`/`@blur`, emit số thường, hiển thị `1,234,567.89`; clamp `max` PHẢI trong component.
  - `V2BaseIconButton`: slot icon `<i class="ri-...">`, prop `interactable` (KHÔNG `disabled`), `danger` bool, emit `click`.
  - `V2Footer`: props `urlBack`/`decisionId`/`menu`; auto-confirm CHUNG CHUNG (không gọi tên phiếu) → Duyệt-có-tên-phiếu dùng `#custom-actions` + `$confirm()`.
- **BE trả `type` số:** `ProductImportDetailResource.php:85`, `ProductImportRequestDetailResource.php:26`.

---

## 5. NỀN TẢNG gop_db + RULE BẮT BUỘC (đừng vi phạm)

- DB gộp, KHÔNG `mysql2`/`DB_CONNECTION_SECOND`. `auth()->id()` = 1 employee id. Trùng bảng → ưu tiên bảng ERP.
- Route `/product-imports` KHÔNG middleware spatie → gate store/update trong Service. BE loại ≠4 ném 422 (cố ý).
- **Cờ quyền fail-closed**: KHÔNG hard-code `= true`; chỉ set từ `$store.state.permissions` / field BE.
- Màn mới chỉ dùng V2Base*; nút form trong V2Footer; số `1,234,567.89` (`en-US`, KHÔNG `vi-VN`); ngày `dd/mm/yyyy`;
  ô rỗng `{{ x || '' }}`; `.text-muted` ĐỎ → dùng `#6b7280`; confirm qua `$confirm()`/`base-confirm-modal`;
  nút ghi API cần `$safeLoadingStart/Finish` + `:interactable`; nút đổi trạng thái (Duyệt) cần confirm nêu tên phiếu.
- **KHÔNG**: commit/push khi chưa yêu cầu · đọc `vendor/`,`node_modules/` · tự sửa hàm dùng chung chưa xác nhận ·
  tự quyết `is_can_delete` · tự thêm phân quyền theo cấp (phải hỏi).
- Doc gop_db: plans → `.plans/gop-db/[feature]/`; specs → `docs/superpowers/specs/gop-db/`. KHÔNG tạo file ở root `ERP-HRM/`.
- Attribution khi commit/PR (chỉ khi user yêu cầu): commit kết `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`; PR kết `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
