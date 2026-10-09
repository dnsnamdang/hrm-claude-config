# Tinh chỉnh UI cha-con Báo giá & HĐ hãng — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 4 tinh chỉnh hiển thị cụm hàng 2 cấp cha-con trên form Báo giá hãng & Hợp đồng hãng.

**Architecture:** Thuần FE (Blade + AngularJS class). STT tính qua getter mới trên Tab class; tỉ lệ cha & nút "+ con" sửa blade báo giá; thành tiền con hiện thật + loại con khỏi VAT summary bằng cách skip `is_child` trong `groupByVatAndMerge`.

**Tech Stack:** AngularJS 1.3.9 (interpolation `<% %>`), Blade.

## Global Constraints

- KHÔNG commit/push khi user chưa yêu cầu.
- Branch: `sync_quotation`.
- KHÔNG có test tự động (Blade/Angular) → verify bằng `php -l` (không áp cho blade) + **test browser trên dev**.
- Phạm vi đã chốt: Req1 (2 form), Req2 & Req3 (chỉ báo giá), Req4 (2 form).
- **Đã xác minh:** tổng báo giá/HĐ + tổng tab **đã parent-only** (`FirmQuotationTab.total_cost:188` và các reducer `FirmContractTab` đều `filter(!is_child)`). → KHÔNG sửa các tổng này. Req4 chỉ còn: VAT summary + hiển thị thành tiền con trên HĐ.

---

## File Structure
- `resources/views/sale/firm/quotations/form.blade.php` — STT, tỉ lệ cha, nút +con.
- `resources/views/sale/firm/contracts/form.blade.php` — STT, thành tiền con.
- `resources/views/partials/classes/sale/firm/quotation/FirmQuotationTab.blade.php` — getter `getDisplayIndex`.
- `resources/views/partials/classes/sale/firm/contract/FirmContractTab.blade.php` — getter `getDisplayIndex`.
- `resources/views/partials/classes/sale/firm/quotation/FirmQuotation.blade.php` — `groupByVatAndMerge` skip con.
- `resources/views/partials/classes/sale/firm/contract/FirmContract.blade.php` — `groupByVatAndMerge` skip con.

---

### Task 1: STT dạng "1.1" (cả 2 form)

**Files:**
- Modify: `FirmQuotationTab.blade.php`, `FirmContractTab.blade.php` (thêm getter)
- Modify: `firm/quotations/form.blade.php:428`, `firm/contracts/form.blade.php:548`

**Interfaces:**
- Produces: `tab.getDisplayIndex(product)` → chuỗi STT ("1", "2", "1.1", "1.2"...). Danh sách `this.products` đã sắp cha rồi con ngay dưới (addChild chèn con sau cha).

- [ ] **Step 1: Thêm getDisplayIndex vào FirmQuotationTab**

Trong `FirmQuotationTab.blade.php`, thêm method (trong class, ví dụ sau getter `total_cost`):

```js
        getDisplayIndex(product) {
            let parentNo = 0;
            let childNo = 0;
            for (let p of this.products) {
                if (!p.is_child) {
                    parentNo++;
                    childNo = 0;
                    if (p === product) return String(parentNo);
                } else {
                    childNo++;
                    if (p === product) return parentNo + '.' + childNo;
                }
            }
            return '';
        }
```

- [ ] **Step 2: Thêm getDisplayIndex vào FirmContractTab** (y hệt Step 1, vào `FirmContractTab.blade.php`)

```js
        getDisplayIndex(product) {
            let parentNo = 0;
            let childNo = 0;
            for (let p of this.products) {
                if (!p.is_child) {
                    parentNo++;
                    childNo = 0;
                    if (p === product) return String(parentNo);
                } else {
                    childNo++;
                    if (p === product) return parentNo + '.' + childNo;
                }
            }
            return '';
        }
```

- [ ] **Step 3: Dùng getter ở cột STT — báo giá** (`firm/quotations/form.blade.php:428`)

Thay:
```html
                                                    <td class="text-center"><% $index + 1 %></td>
```
bằng:
```html
                                                    <td class="text-center"><% tab.getDisplayIndex(product) %></td>
```

- [ ] **Step 4: Dùng getter ở cột STT — HĐ** (`firm/contracts/form.blade.php:548`, dòng `<td class="text-center"><% $index + 1 %></td>` ngay sau `<tr ng-repeat="product in tab.products"...>` dòng 547)

Thay `<% $index + 1 %>` (td STT đó) bằng `<% tab.getDisplayIndex(product) %>`.

- [ ] **Step 5: Test browser** — mở báo giá & HĐ hãng có cụm cha-con: cha 1,2,3; con 1.1,1.2; cụm 2 → 2.1...

---

### Task 2: Tỉ lệ cha = 1 (chỉ Báo giá)

**Files:**
- Modify: `firm/quotations/form.blade.php:469`

- [ ] **Step 1: Đổi "-" thành "1"**

Thay (dòng 469):
```html
                                                        <span ng-if="!product.is_child" class="text-muted">-</span>
```
bằng:
```html
                                                        <span ng-if="!product.is_child">1</span>
```

- [ ] **Step 2: Test browser** — cột tỉ lệ: dòng cha hiện "1", con hiện input tỉ lệ.

---

### Task 3: Nút "+ con" về cột Tên hàng (chỉ Báo giá)

**Files:**
- Modify: `firm/quotations/form.blade.php` (bỏ nút ở 494-496, thêm vào cột Tên hàng sau 444)

- [ ] **Step 1: Bỏ nút "+ con" khỏi cột Thành tiền**

Xóa đoạn (dòng 494-496):
```html
                                                        <button type="button" class="btn btn-xs btn-info d-block mt-1"
                                                                ng-if="!product.is_child && !form.isShow && !tab.combo_campaign_id"
                                                                ng-click="openChildPicker(tab, product)">+ con</button>
```

- [ ] **Step 2: Thêm nút vào cột Tên hàng (sau khối Mã/Model/thuộc tính)**

Trong cột Tên hàng, ngay sau dòng `<div ng-bind-html="trustAsHtml(product.getAttribute())"></div>` (dòng 444), thêm:
```html
                                                        <button type="button" class="btn btn-xs btn-info d-block mt-1"
                                                                ng-if="!product.is_child && !form.isShow && !tab.combo_campaign_id"
                                                                ng-click="openChildPicker(tab, product)">+ con</button>
```

- [ ] **Step 3: Test browser** — nút "+ con" nằm dưới thông tin hàng trong cột Tên hàng (chỉ dòng cha, không show/combo); bấm mở picker chọn con OK.

---

### Task 4: Thành tiền con hiện thật + loại khỏi VAT summary (cả 2 form)

**Files:**
- Modify: `firm/contracts/form.blade.php:562` (thành tiền con 0 → thật)
- Modify: `FirmQuotation.blade.php` (`groupByVatAndMerge` ~101 skip con)
- Modify: `FirmContract.blade.php` (`groupByVatAndMerge` ~423 skip con)

**Interfaces:**
- Báo giá đã hiện thành tiền con thật (`product.total_cost`, form 492) → KHÔNG đổi.
- Tổng báo giá/HĐ + tab đã parent-only → KHÔNG đổi.

- [ ] **Step 1: HĐ — thành tiền con hiện thật**

Trong `firm/contracts/form.blade.php`, cột Thành tiền (dòng 561-562):
```html
                                                        <span ng-if="!product.is_child"><% product.total_cost | numberOrHyphenNotCommas %></span>
                                                        <span ng-if="product.is_child">0</span>
```
Thay dòng con thành:
```html
                                                        <span ng-if="product.is_child"><% product.total_cost | numberOrHyphenNotCommas %></span>
```
(GIỮ nút xoá/khác nếu có. Cột khác của con vẫn "0" — KHÔNG đổi ở task này; chỉ cột Thành tiền.)

- [ ] **Step 2: Báo giá — loại con khỏi VAT summary**

Trong `FirmQuotation.blade.php`, hàm `groupByVatAndMerge`, đầu callback `(tab.products || []).forEach(prod => {` (dòng ~101) thêm dòng đầu:
```js
                    if (prod.is_child) return; // Con không vào tab Tổng hợp theo VAT
```
(đặt ngay trước `const vat = prod.vat_percent ?? '';`). Đồng thời XÓA/không cần comment cũ "con VẪN vào summary" (dòng 102-103) — thay bằng ý mới.

- [ ] **Step 3: HĐ — loại con khỏi VAT summary**

Trong `FirmContract.blade.php`, hàm `groupByVatAndMerge`, đầu callback `(tab.products || []).forEach(prod => {` (dòng ~423) thêm:
```js
                    if (prod.is_child) return; // Con không vào tab Tổng hợp theo VAT
```
(ngay trước `const vat = prod.vat_percent ?? '';`).

- [ ] **Step 4: Test browser**
  - Báo giá & HĐ: dòng con có thành tiền (SL con × giá con) hiển thị; **tổng chung + tổng tab KHÔNG đổi** (chỉ cha).
  - Tab "Tổng hợp theo VAT": KHÔNG còn dòng con; group total = chỉ cha.
  - Bản in: vẫn chỉ cha (không đổi).

---

## Self-Review

1. **Spec coverage:**
   - Req1 STT "1.1" (2 form) → Task 1. ✅
   - Req2 tỉ lệ cha=1 (báo giá) → Task 2. ✅
   - Req3 +con → tên hàng (báo giá) → Task 3. ✅
   - Req4 thành tiền con hiện thật + không cộng tổng → Task 4 (HĐ hiện thật + skip con khỏi VAT summary; tổng chính đã parent-only sẵn — ghi rõ). ✅
2. **Placeholder scan:** không TBD; mọi step có code + anchor + expected. ✅
3. **Type consistency:** `getDisplayIndex(product)` định nghĩa (Task 1 Step 1-2) & dùng (Step 3-4) khớp. `is_child` dùng nhất quán. ✅

## Ghi chú kiểm tra khi thực thi
- Xác nhận HĐ có cột "Thành tiền sau VAT"/VAT của con đang "0" (dòng ~569): nếu user muốn hiện thật luôn thì mở rộng Task 4 Step 1 (hiện chỉ đổi cột Thành tiền theo yêu cầu "thành tiền").
- form_show.blade.php (báo giá xem) nếu render STT/thành tiền con giống form → đồng bộ getter STT tương tự (kiểm tra khi test).
