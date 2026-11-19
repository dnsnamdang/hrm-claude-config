# YCXH — Lịch sử chỉ ghi ô người dùng tự đổi (không ghi thông tin đi kèm)

> Phân hệ: Giao việc / Kho — Yêu cầu xuất hàng (YCXH, `product_export_requests`).
> Nhánh: `develop` (hậu duệ `gop_db`) → tài liệu đặt ở `.plans/gop-db/`.
> Khác với `ycxh-history-missing-logs` (Redmine #11388 — log BỊ THIẾU của xuất thẳng/đính kèm).
> Đây là yêu cầu NGƯỢC LẠI: log đang DƯ — ghi cả thông tin suy ra từ lựa chọn.

## 1. Mục tiêu

Trên màn "Lịch sử thay đổi" của YCXH, **chỉ ghi lại những ô người dùng trực tiếp chọn/đổi**
(ví dụ: đổi Hợp đồng), **KHÔNG ghi các thông tin hiển thị đi kèm theo lựa chọn đó**
(Khách hàng, SĐT, địa chỉ, MST…). Áp dụng cho **tất cả các loại** YCXH.

## 2. Hiện trạng (nguyên nhân — đã xác minh trong code)

Khi đổi nguồn (Hợp đồng) trên phiếu nháp, `applySourceChange()` gọi `fillCustomerSnapshot()`
tự điền lại `customer_id`, `customer_name`, `customer_address`, `customer_contact_name`,
`customer_mobile`, `customer_contact_phone`, `identity_card_number` theo hợp đồng mới.

- Whitelist log cũ (`catalogColumns()`) có `emplement_contract_code` + `customer_name`
  nhưng **thiếu `firm_contract_id`**. Địa chỉ/SĐT/MST vốn đã không nằm whitelist nên không log.
- **Loại 14** (XUAT_BAN_HD_HANG) dùng cột riêng `firm_contract_id` → đổi HĐ **không ghi "Hợp đồng"**,
  chỉ còn ghi "Khách hàng" (đúng ảnh user chụp: "đổi số HĐ nhưng lịch sử lại ghi mỗi đổi khách hàng").
- **Loại 19/20/21** dùng `emplement_contract_code` → ghi CẢ "Hợp đồng" LẪN "Khách hàng" (dư "Khách hàng").

## 3. Quyết định đã chốt (user duyệt trong chat)

- **Ghi thêm Hợp đồng cho loại 14**: đưa `firm_contract_id` vào whitelist, hiển thị bằng **MÃ HĐ**
  (không phải id), nhãn **"Hợp đồng"**.
- **KHÔNG ghi các ô suy ra theo nguồn** (`customer_name`…) khi việc thay đổi là do đổi nguồn.
- **Hướng B — GIỮ log "Bảng chi tiết hàng hóa"** (`details_rows`) khi nó đổi theo HĐ.
  (Bảng hàng hóa là dữ liệu nghiệp vụ thực, không phải nhãn hiển thị đi kèm → vẫn log.)
- User đã **OK** toàn bộ thiết kế ngắn (gồm cả việc sửa nhãn ở file dùng chung `CatalogHistoryService`).

## 4. Giải pháp

Cột "suy ra theo nguồn" (`SOURCE_DERIVED_LOG_COLUMNS = ['customer_name']`) sẽ được **bỏ qua khi
và chỉ khi** phiếu vừa đổi nguồn (`$sourceChanged = true`): ngay trước khi so sánh `before/after`
để ghi log, ta ghi đè `before[col]` = giá trị MỚI → before == after → cột đó không vào log.

- Khi user **tự sửa tay** Khách hàng ở loại cho phép (3/99) mà KHÔNG đổi nguồn → `$sourceChanged=false`
  → "Khách hàng" **vẫn được log** (đúng — đây là thay đổi trực tiếp của user).
- Không tạo log nhiễu, không cần backfill: before/after đều tính "live" tại thời điểm sửa.

### Hành vi sau fix khi đổi Hợp đồng

| Loại | Trước fix | Sau fix |
|---|---|---|
| 14 | Khách hàng (+ Bảng hàng) | **Hợp đồng** (+ Bảng hàng nếu đổi) |
| 19/20/21 | Hợp đồng + Khách hàng (+ Bảng hàng) | **Hợp đồng** (+ Bảng hàng nếu đổi) |

## 5. File chạm

- `Modules/Assign/Services/ProductExportRequestService.php`
  - `catalogColumns()`: + `firm_contract_id`.
  - `catalogDisplay()`: `firm_contract_id` → hiển thị MÃ (`FirmContract::value('code')`).
  - hằng `SOURCE_DERIVED_LOG_COLUMNS = ['customer_name']`.
  - `updateFromRequest()`: hoist `$sourceChanged` (by-ref vào closure); trước `logCatalogUpdate` ghi đè
    `before[col]` cho các cột suy-ra khi `$sourceChanged`.
- `app/Services/CatalogHistoryService.php` (DÙNG CHUNG — chỉ sửa nhánh `product_export_requests`)
  - thêm `'firm_contract_id' => 'Hợp đồng'` (mỗi phiếu chỉ dùng 1 trong 2 cột HĐ nên không trùng dòng).

## 6. Kiểm thử

Dry-run tinker (bọc transaction + rollBack, không ghi DB), chạy trên `erp_hrm_check`:

- **Loại 14** — phiếu nháp PYCXH-39254 (id 39254), đổi `firm_contract_id` 10627→24935 (KH khác nhau):
  log đúng **1 dòng** `{"Hợp đồng": "…25_1000…" → "…26_1242…"}`, **không có "Khách hàng"**. ✅
- **Loại 19** — phiếu nháp id 38510, đổi `emplement_contract_id` 24933→24935 (KH khác nhau):
  log đúng **1 dòng** `{"Hợp đồng": "…26_1241…" → "…26_1242…"}`, **không có "Khách hàng"**. ✅

(Loại 20/21 không có phiếu nháp trong DB dev; dùng chung đúng một đường `updateFromRequest` +
`SOURCE_DERIVED_LOG_COLUMNS` với 14/19 nên hành vi đồng nhất.)

## 7. Trạng thái

Code đã sửa xong (php -l sạch), đã dry-run xác minh. **CHƯA commit** — chờ user yêu cầu.
