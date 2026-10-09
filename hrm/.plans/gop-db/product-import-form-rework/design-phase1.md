# Design Cụm 1 — Khung động + loại 4 (Bán trả lại)

Mục tiêu Cụm 1: **dựng lại form Tạo/Sửa Phiếu nhập hàng theo chuẩn HRM** và **đưa toàn bộ phần
"thay đổi theo loại nhập hàng" vào một KHUNG CẤU HÌNH động**, nhưng trước mắt chỉ khai + chạy
được **loại 4 (Bán trả lại)** — loại HRM đang hỗ trợ. Các loại khác để khung sẵn, bật dần ở Cụm 2–3.

Không đụng BE nghiệp vụ loại 4 (đã chạy). Cụm 1 chủ yếu là **FE rework** + 1 chỉnh nhỏ BE (trả
`import_type` + cấu hình form xuống FE nếu cần). KHÔNG mở `buildDetailsByType` cho loại mới ở cụm này.

---

## 1. Khung cấu hình động — `typeConfig` (trọng tâm Cụm 1)

Thay vì rải `v-if type===x` khắp template, gom về **1 object cấu hình theo `import_type`**. Đặt ở
FE: `pages/finance/product-imports/constants/importTypeConfig.js`.

```js
// Mỗi loại nhập hàng khai 1 entry. Cụm 1 CHỈ khai đủ cho loại 4; loại khác để placeholder.
export const IMPORT_TYPE_CONFIG = {
  4: {
    name: 'Bán trả lại',
    productTableVariant: 'default',   // 'default' (C) | 'vat' (B) | 'foreign' (A)
    tabs: ['products', 'inlandCost', 'pickupCost'], // tab nào hiện
    columns: {                         // cột nào hiện trong tab hàng hoá
      listedPrice: true,               // Giá niêm yết (showListedPrice: type∈{4,9,13})
      sellingPrice: true, discount: true, vat: true,
      consignmentDeadline: false,      // cột "hạn gửi" — chỉ type 14
    },
    flags: {
      isForeign: false,                // type∈{1,11}
      hasInlandCost: true,             // type≠3
      allocationAll: false,            // type∈{11,15,2,16}
    },
    accountingHint: 'DT 5212 · kho 1561/157 · GV 632 · CK 5211 · GG 5213 · thuế 33311',
  },
  // 2,15,99 → Cụm 2 · 11,3,9,14 → Cụm 3 (khai dần)
}

export function getTypeConfig(importType) {
  return IMPORT_TYPE_CONFIG[importType] || null
}
```

Template `ProductImportForm.vue` đọc `cfg = getTypeConfig(header.import_type)` rồi:
- Render tab theo `cfg.tabs` (v-for, không còn 3 tab cứng).
- Render cột bảng hàng hoá theo `cfg.columns` (+ vẫn gate `canViewCostPrice` cho nhóm cột giá vốn).
- Tiêu đề tab hàng hoá lấy theo `cfg.name` thay vì chuỗi cứng "Hàng hoá nhập trả lại".
- Dòng gợi ý hạch toán (nếu hiện) lấy `cfg.accountingHint`.

**Nguồn chân lý của các cờ dẫn xuất = ERP `ProductImport.blade.php`** (đã chép trong design.md):
`is_foreign type∈{1,11}` · `has_inland_cost type≠3` · `showListedPrice type∈{4,9,13}` ·
`allocation_all type∈{11,15,2,16}`. Cụm 1 chỉ cần đúng cho loại 4; khai sẵn chỗ cho loại khác.

> Loại chưa khai config (`getTypeConfig` trả null) → form hiện thông báo "Loại nhập hàng chưa được
> hỗ trợ" + ẩn nút Lưu/Duyệt, KHÔNG để vỡ layout. Khớp với BE đang ném 422 cho loại ≠ 4.

---

## 2. Ô chọn PNK đổi được (yêu cầu cốt lõi của user)

Hiện trạng: PNK hiển thị read-only `{{ header.warehouse_import_code || '—' }}`, pick xong không đổi.

Cụm 1:
- Ở khối **Thông tin chung**, cạnh dòng "Phiếu nhập kho" thêm nút **V2BaseIconButton**
  (`ri-edit-line`, title "Đổi phiếu nhập kho") — chỉ hiện ở **mode create** và khi phiếu **chưa
  khóa/chưa duyệt** (`header.status === STATUS_DANG_TAO`). Bấm → mở lại `WarehouseImportSearchModal`.
- Chọn phiếu mới → gọi lại `loadFromWarehouseImport(newId)` → nạp lại header + dòng hàng + **gọi
  lại `loadAccountingWarehouses()`** theo nguồn mới. Cảnh báo `$confirm()` trước khi đổi vì sẽ
  **mất dữ liệu hàng hoá đang nhập dở** ("Đổi phiếu nhập kho sẽ nạp lại toàn bộ danh sách hàng
  hoá. Tiếp tục?").
- Nhánh nguồn là ĐNNK (`product_import_request_id`) giữ nguyên cơ chế tương tự (nút đổi phiếu YC).
- Ở **mode edit**: KHÔNG cho đổi phiếu nguồn (ERP cũng chốt nguồn sau khi tạo) → không hiện nút.

---

## 3. Chuyển sang component HRM (Hướng A)

Bảng tra thay thế (grep tự kiểm `<input|<select|<button|<label|class="btn|form-control` phải rỗng):

| Hiện tại (thô) | Thay bằng |
|---|---|
| `<select>` kho kế toán trong bảng | `V2BaseSelectInModal`? → KHÔNG (không trong modal) → `V2BaseSelect` (options = accWarehouses) |
| `<input type="number">` số lượng hạch toán | `V2BaseInput` (rule `number_only`/`positive_number`) hoặc `V2BaseCurrencyInput` nếu là tiền |
| Thanh nút tự chế `.export-actionbar` | `V2Footer` (Quay lại tự có) + slot `#custom-actions` cho "Lưu nháp"/"Lưu và tiếp tục"/"Duyệt" |
| Ô đọc (import_type_name, mã phiếu…) | `V2Base* :disabled` hoặc `dl.kv-grid` giữ nguyên (chỉ đọc, không phải input) |
| Badge trạng thái (nếu có) | `V2BaseBadge` + `utils/statusBadgeVariant.js` |
| Checkbox `not_paying_bill`, "Nhập thẳng" | giữ `V2BaseCheckbox` (đã dùng) |

- Nhóm "Thông tin chung" và "Hàng hoá & chi phí" bọc `V2BaseFormSection` (card + tiêu đề chuẩn).
- Số/tiền hiển thị `1,234,567.89` (`toLocaleString('en-US')`); ô nhập tiền dùng `V2BaseCurrencyInput`.
- Nút gọi API ghi (Lưu/Duyệt): `$safeLoadingStart/Finish` + `:interactable`; nút Duyệt + confirm popup.
- Thao tác xong (Lưu/Lưu nháp/Duyệt) → `markFormSaved()` → `$router.push('/finance/product-imports')`.
- Bảng hàng hoá tràn ngang → bọc `V2BaseTableScroll` (thanh cuộn trên+dưới).

---

## 4. Danh mục kho kế toán "không cần quyền"

Endpoint `ProductImportController::accountingWarehouses` **đã ungated** trên gop_db. Cụm 1:
- Giữ nguyên endpoint. FE gọi sau khi header có id nguồn (create: sau loadFromWarehouseImport/Request;
  edit: sau loadForEdit). Đổi phiếu nguồn → gọi lại.
- Nếu danh mục rỗng → KHÔNG kết luận "lỗi quyền". Hiện dòng xám "Không có kho kế toán phù hợp với
  phiếu nguồn" và điều tra data (warehouse_id/company_id null, lọc ký gửi). Giữ `accWarehouseCatalogOk`
  để phân biệt lỗi gọi API (callout đỏ) vs danh mục rỗng hợp lệ.

---

## 5. Giữ loại 4 chạy đúng — KHÔNG regression

- BE loại 4 không đổi. FE sau rework phải: tạo mới từ PNK loại 4 → nạp dòng hàng → chọn kho kế toán
  → Lưu nháp (status 3) / Duyệt (status 1) → thành công; sửa lại phiếu status 3 → đúng dữ liệu cũ.
- Các method tính giá (`rowPriceAfterExtra`, `rowDiscountPrice`, `rowTotalAmountAllocated`,
  `rowVatCostAllocated`, allocation nội địa/bốc xếp) **giữ nguyên**, chỉ di chuyển chỗ gọi theo cột
  động. `buildFormData`, `validateBeforeApprove`, `save`, `handleSaveError` giữ nguyên hợp đồng API.

---

## 6. Phạm vi KHÔNG làm ở Cụm 1

- KHÔNG mở `buildDetailsByType`/`accumulateReturnedQtyByType`/`store()` cho loại ≠ 4.
- KHÔNG làm biến thể bảng VAT (B) / nước ngoài (A) — chỉ để `productTableVariant` trong config.
- KHÔNG làm cột "hạn gửi" (type 14) — chỉ để cờ `consignmentDeadline: false`.
- KHÔNG đụng ngoại tệ/currency (type 11).

---

## 7. Verify Cụm 1 (Playwright 127.0.0.1:3000)

1. Tạo mới loại 4 từ 1 PNK → form hiện đúng tab/cột theo config; chọn kho kế toán; Lưu nháp OK.
2. **Bấm nút đổi PNK** → chọn phiếu khác → confirm → dòng hàng + danh mục kho kế toán nạp lại đúng.
3. Grep thô rỗng (`<input|<select|<button|<label|class="btn|form-control` trừ V2Base).
4. Số hiển thị `1,234,567.89`; nút trong V2Footer; Duyệt có popup xác nhận.
5. Mở lại phiếu status 3 (edit) → không có nút đổi nguồn, dữ liệu đúng, Lưu OK.
6. Console không có 500/403/404 ở endpoint product-imports & accounting-warehouses.
