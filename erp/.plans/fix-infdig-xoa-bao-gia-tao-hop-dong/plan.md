# Fix: infdig ($digest 10 iterations) khi xoá báo giá ở màn tạo hợp đồng nguyên tắc

> File: `resources/views/partials/classes/sale/firm/contract/FirmContract.blade.php`
> Màn: `admin/sale/firm-contracts/create?firm-quotation=...&contract_type=1`

## Triệu chứng
Bấm "Xác nhận" popup "Nếu bạn hủy báo giá này..." (xoá báo giá đã chọn) → Angular lỗi
`[$rootScope:infdig] 10 $digest() iterations reached` (stack qua `app.directive.js:197` ckEditor updateModel) → popup không đóng.

## Nguyên nhân gốc
`removeQuotation()` → `reset()` (dòng 612) chạy `for (let key in this) { if (!no_clear.includes(key)) delete this[key]; }` → xoá luôn các backing field `_tabs`, `_groups`, `_all_combos`, `_combo_categories`, `_revenue_costs`, `_costs`, `_market_costs`.

Các getter tương ứng viết kiểu `get tabs(){ return this._tabs || []; }`. Khi `_tabs` = undefined, getter trả về **một mảng `[]` MỚI mỗi lần gọi**. Template Angular bind (ng-model/ng-repeat) so sánh tham chiếu → luôn "thay đổi" → digest không hội tụ → infdig. CKEditor `updateModel` ($apply khi change) chỉ là ngòi nổ khởi động digest.

## Fix
Đổi 7 getter mảng từ `return this._x || []` sang lazy-init trả **ref ổn định**:
```js
get tabs() { if (!this._tabs) this._tabs = []; return this._tabs; }
```
Áp dụng cho: tabs (151), groups (159), all_combos (652), combo_categories (751), revenue_costs (867), costs (943), market_costs (1118).
→ Sau digest đầu tiên `_x` = [] (truthy, ref cố định) → getter trả cùng ref → digest hội tụ, hết infdig. Không đổi hành vi (rỗng vẫn rỗng), an toàn cho mọi template dùng class này.

## Việc đã làm
- [x] Sửa 7 getter (lazy-init). Cú pháp getter/setter kiểm tra OK.
- [ ] E2E browser: mở create?firm-quotation=... → xoá báo giá → popup đóng, không lỗi console; các bảng tab/nhóm/combo/chi phí trống bình thường.
- [ ] Commit (chờ user).

## Ghi chú
- `removeFirmContract()` cũng gọi `reset()` → cùng được fix.
- Method gom sản phẩm theo VAT (dòng ~453) trả mảng mới mỗi lần nhưng không bind ng-repeat trực tiếp (trang chạy bình thường trước reset) → không đụng.
- Không cần sửa directive ckEditor (updateModel chỉ là ngòi nổ).

### Checkpoint — 2026-07-23
Vừa hoàn thành: fix 7 getter mảng lazy-init để hết infdig sau reset.
Bước tiếp theo: user test browser + commit.
Blocked:

---

## Fix bổ sung (2026-07-23) — lỗi `$digest already in progress` ($inprog)

Sau khi hết infdig, lộ lỗi `[$rootScope:inprog] $digest already in progress` (stack `app.directive.js:197` ckEditorPrint updateModel) — xuất hiện ngay khi vào màn (CKEditor `dataReady` fire trong lúc digest đang chạy) và sau khi bấm Xác nhận.

**Nguyên nhân:** directive CKEditor (`ckEditor` + `ckEditorPrint` trong `public/js/angular/app.directive.js`) gọi `scope.$apply()` trong `updateModel`/`pasteState`. CKEditor có thể fire change/dataReady KHI Angular digest đang chạy → `$apply` ném inprog (re-entrancy kinh điển CKEditor+Angular).

**Fix:** đổi `scope.$apply(fn)` → `scope.$evalAsync(fn)` (4 chỗ: updateModel + pasteState của cả 2 directive). `$evalAsync` chạy fn trong digest hiện tại nếu đang có, hoặc lên lịch digest mới — KHÔNG bao giờ ném inprog. Không đổi hành vi (model vẫn cập nhật + digest vẫn chạy).
- [x] Sửa `public/js/angular/app.directive.js` (dòng 122/133/197/208). `node --check` sạch.
- [ ] E2E: vào màn create không còn lỗi console; gõ CKEditor + xoá báo giá đều OK.

**Lưu ý:** `app.directive.js` là file dùng chung toàn app → ảnh hưởng mọi chỗ dùng ckEditor/ckEditorPrint, nhưng `$evalAsync` an toàn hơn `$apply` (chỉ tránh double-digest), không hồi quy.
