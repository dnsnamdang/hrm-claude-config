# Plan — Lỗi "The given data was invalid." khi Gửi duyệt YCXH (Redmine feedback)

Nguồn: ảnh Redmine (2026-09-18 16:00), màn **Tạo yêu cầu xuất hàng**
(`hrm-client/pages/finance/product-export-requests/create.vue`). Chú thích verbatim:
**"NHập các thông tin như hìn - Gửi duyệt : Báo lỗi nhưng k biết lỗi gì => Phải báo cụ thể và báo
đỏ dưới textbox"**. Ảnh: loại **"Xuất hàng gửi" (type 12)**, **Xuất thẳng (is_export_direct) TÍCH**,
đã chọn khách hàng, 1 hàng — **KHÔNG có Kho**. Bấm **Lưu và gửi duyệt** → hiện đỏ chung
"The given data was invalid." ở đáy form, không chỉ ra field nào sai.

## Chẩn đoán (systematic-debugging Phase 1 — đã xong)

Root cause là **lệch rule FE ↔ BE ở `warehouse_id` khi Xuất thẳng**, KHÔNG phải lỗi hiển thị:

- **BE** `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php::rulesForType()`
  hardcode `warehouse_id => 'required|integer'` cho type 12 (dòng 606) và cả 6/18/99/19 (600/610),
  **bỏ qua `is_export_direct`**.
- **FE** `ProductExportRequestForm.vue`: `needWarehouse` (dòng 1035) =
  `!isContractType && !isBranchTransfer && type != null && is_export_direct !== 1` → khi tích Xuất
  thẳng thì KHÔNG bắt buộc kho, và `onExportDirectChange` (1245) set `warehouse_id = null`.
- Hệ quả: FE validate qua (không đòi kho) → gửi payload `warehouse_id = null` → **BE 422 ở
  warehouse_id**. Mà khi Xuất thẳng, ô Kho + div lỗi (`showWarehouse` dòng ~1039) bị ẨN → dù
  `applyServerErrors` có map `errors.warehouse_id` cũng không có chỗ render → user chỉ thấy câu
  chung "The given data was invalid." (message mặc định của Laravel ValidationException).

### Đối chiếu ERP (chuẩn nghiệp vụ) — `warehouse/ProductExportRequestsController@store`
- Dòng 385: `if ($type != XUAT_DIEU_CHUYEN_KHO_CHI_NHANH(7) && !$is_export_direct) { warehouse_id
  => required }` — **nơi DUY NHẤT** thêm `warehouse_id`.
- Dòng 466-467: `if ($is_export_direct && !in_array($type, getTransferTypes[5,6])) { unset
  warehouse_id }` — chỉ là lưới an toàn (no-op vì 385 vốn đã không thêm khi Xuất thẳng).
- ⇒ ERP: **`warehouse_id` bắt buộc ⟺ (type != 7) VÀ (không Xuất thẳng)** cho MỌI loại. FE HRM
  (`needWarehouse`) đã đúng theo ERP; chỉ BE HRM sai.

## Task

### BE — `ProductExportRequestController.php::rulesForType()` (status=2 branch)
- [x] Type 12 (dòng 606): `warehouse_id` → `required_unless:is_export_direct,1|nullable|integer`
      (đồng bộ pattern đã dùng cho `transition_type` dòng 590).
- [x] Type 6 (dòng 600): warehouse_id → cùng rule (ĐC kho nội bộ vẫn hiện checkbox Xuất thẳng;
      `import_warehouse_id` giữ nguyên `required|integer|different:warehouse_id`).
- [x] Type 18/99/19 (dòng 610): warehouse_id → cùng rule.
- [x] Type 3 (Xuất mượn, dòng 595): **GIỮ NGUYÊN** `required|integer` — FE ẩn checkbox Xuất thẳng
      cho type 3 (`showExportDirect` loại 3 & 15) nên is_export_direct luôn 0, khớp `needWarehouse`.
- [x] `php -l` sạch, file giữ LF (0 CR).

### Verify
- [x] Playwright 127.0.0.1:3000: tái hiện đúng ca ảnh (type 12 + Xuất thẳng + KH + 1 hàng, KHÔNG
      kho) → **Lưu và gửi duyệt** phải LƯU THÀNH CÔNG (hết lỗi giả). Xoá bản ghi test sau khi kiểm.
- [x] Kiểm ca lỗi thật vẫn báo inline đỏ dưới ô: type 12 KHÔNG Xuất thẳng + bỏ trống Kho → FE
      validateForm chặn tại chỗ (viền đỏ + text dưới ô Kho), không gọi API.
- [x] KHÔNG commit/push (chờ user).

## Checkpoint
### Checkpoint — bắt đầu (2026-09-18)
Vừa hoàn thành: chẩn đoán root cause (lệch rule warehouse_id ↔ is_export_direct), đối chiếu ERP.
Đang làm: sửa `rulesForType()` cho type 6/12/18/99/19.
Bước tiếp theo: sửa BE → php -l → Playwright verify.
Blocked: không

### Checkpoint — XONG fix + verify Playwright (2026-09-18)
Vừa hoàn thành: sửa BE `rulesForType()` cho type 6/12/18/99/19 (warehouse_id →
`required_unless:is_export_direct,1|nullable|integer`), type 3 giữ nguyên `required|integer`.
`php -l` sạch, file `ProductExportRequestController.php` vẫn LF (0 CR). Đã verify THẬT trên trình
duyệt tại `http://127.0.0.1:3000/finance/product-export-requests/create`:
- **Ca ảnh Redmine (type 12 "Xuất hàng gửi" + Xuất thẳng TÍCH + KH "18 AUTO" + 1 hàng RRI32, KHÔNG
  kho):** bấm **Lưu và gửi duyệt** → xác nhận → **LƯU THÀNH CÔNG**. `POST .../assign/product-export-requests
  => 200 OK` (KHÔNG còn 422), điều hướng sang detail record **40339**. Hết lỗi giả "The given data
  was invalid.".
- **Ca lỗi thật (type 12 KHÔNG Xuất thẳng, bỏ trống Kho xuất):** bấm **Lưu và gửi duyệt** → xác
  nhận → FE `validateForm` **CHẶN TẠI CHỖ**: text đỏ **"Vui lòng chọn kho xuất."** hiện inline
  ngay dưới ô Kho xuất, KHÔNG có POST tới `/assign/product-export-requests` (kiểm `browser_network_requests`
  — chỉ toàn GET). Đúng yêu cầu Redmine "báo cụ thể và báo đỏ dưới textbox".
- **Dọn dẹp:** đã xoá bản ghi test 40339 khỏi erp_new (request + product_export_request_details +
  product_export_request_tab_products + catalog_histories log create → tất cả về 0). DB sạch.
Bước tiếp theo: chờ user chốt commit lên nhánh gop_db (CHƯA commit/push).
Blocked: không

---

## Fix — tạo xong quay về màn danh sách (2026-10-07)

- [x] `create.vue:60` sau khi tạo thành công đang `$router.push('/.../${newId}')` → vào màn CHI TIẾT.
      Sửa về luôn push `/finance/product-export-requests` (màn danh sách) theo quy ước CLAUDE.md
      "Thao tác xong thì QUAY VỀ MÀN DANH SÁCH". Gỡ biến `newId` thừa.
- [ ] Lưu ý: màn Sửa (`_id/edit.vue`) sau lưu cũng đẩy về chi tiết — chờ user chốt có đồng bộ không.
- [x] Test Playwright: tạo YCXH → kỳ vọng URL về `/finance/product-export-requests`. **ĐẠT.**

### Checkpoint — verify fix redirect (2026-10-07)
Vừa hoàn thành: verify THẬT trên `http://127.0.0.1:3000/finance/product-export-requests/create`.
Tạo YCXH type "Xuất khác" → **Lưu nháp** → điều hướng về `/finance/product-export-requests`
(màn DANH SÁCH, KHÔNG phải detail). Bản ghi mới **PYCXH-35690 / Xuất khác / DNS Admin - HN_KDTM**
hiện ở dòng #1 danh sách. Fix đạt yêu cầu "tạo thành công quay về màn list".
Bước tiếp theo: chờ user chốt (1) có commit fix này lên gop_db không; (2) có đồng bộ `_id/edit.vue`
đẩy về list không.
Blocked: không
