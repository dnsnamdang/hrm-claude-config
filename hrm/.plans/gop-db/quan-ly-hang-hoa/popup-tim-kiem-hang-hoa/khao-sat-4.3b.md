# Bước 4.3b (HRM) — popup chọn hàng CSKH còn lại — khảo sát 14/10/2026 (chỉ đọc)

> hrm-client / hrm-api worktree `wt-chuyen-doi-hang-hoa` (nhánh chung `feat/chuyen-doi-hang-hoa`). Chưa đụng source.

## 1. Popup cũ còn lại
`pages/customer-care/services/components/ProductSearchModal.vue` ("Chọn hàng hóa áp dụng") — gọi `GET customer-care/services/search-products` (`ServiceService.php:997`) với bộ lọc phân loại CŨ (T/chất enum, Loại hàng hoá JSON, Lĩnh vực/Chương/Nhóm CV/Cụm CV cũ, Nhóm hàng…); chỉ lọc `status≠0` + loại hàng tạm; KHÔNG có máy, KHÔNG có `is_service_quotation` ⇒ HRM đang lỏng hơn ERP (ERP đã khoá ở 4.4/4.5).

## 2. 8 chỗ dùng (đều đang sống)
| # | Màn / component | Chọn gì | Hiện | Popup mới |
|---|---|---|---|---|
| A | YC thông tin BH-SC (`wr-information-requests`) | Vật tư cho từng thiết bị (bảo hành / sửa chữa) · Vật tư gói bảo dưỡng | nhiều | thiết bị: **chế độ máy** (`machineId` = máy của dòng); gói bảo dưỡng: `service_quotation_only` — như ERP |
| B | Báo giá DV SC-BD-BT (`wr-quotations`, kế thừa A) | như A + **C – Loại hàng hoá** (merchandise) | nhiều | như A; merchandise: mặc định (ERP chặn chọn "Thiết bị" ở client theo enum cũ) |
| C | Lỗi thiết bị (`device-errors`) | Áp dụng cho thiết bị · Vật tư thay thế | nhiều | thiết bị: mặc định; vật tư: `service_quotation_only` — như ERP E-T6 |
| D | Xử lý YC BH (`warranty-repair-handle-requests`) | Hàng hoá tương đương (thiết bị KH nhập tay) | 1 | mặc định, chọn 1 |
| E | Gói bảo dưỡng (`services`) | Áp dụng cho hàng hoá (máy áp dụng gói) | nhiều | mặc định — nhưng form **gom theo Nhóm hàng CŨ** (`group_id`), popup mới không trả nhóm |
| F | Thêm thiết bị ngoài (`AddExternalEquipmentModal`) — từ YC BH-SC, popup thiết bị KH | Trang thiết bị / Hàng công ty tương đương | 1 | mặc định, chọn 1, popup lồng |
| G | Thêm thiết bị cũ (`AddOldEquipmentModal`) | Trang thiết bị | 1 | như F |
| H | Tab Trang thiết bị KH (`EquipmentTab`) | Hàng công ty tương đương | 1 | như F |
Hợp đồng DV (`wr-service-contracts`) kế thừa B nhưng không mở popup (chết).
Ngoài popup: ô chọn có tìm ở Tra cứu tồn (`lookup/stock-companies`) cũng gọi `services/search-products`; Tab thiết bị KH có ô chọn gọi `assign/customers/manager/search-products`.

## 3. Thiếu ở `ProductPickerPanel`
- Chưa có vỏ popup dùng chung `V2ProductPickerModal` (plan C1 hẹn làm ở 4.3b).
- Chưa có prop `serviceQuotationOnly` / `scope` (hiện chỉ đi lén qua `lockedFilters`).
- Dòng trả về không có nhóm hàng (màn E cần).
- Màn B merchandise: chưa có quy tắc "không chọn Thiết bị" theo phân loại mới.
- Dòng thiết bị KH nhập tay (không có `product_id`) ⇒ chế độ máy không có máy.

## 4. Chốt của user 14/10
| # | Câu | Chốt |
|---|---|---|
| Q1 | Phạm vi | **Cả 8 chỗ + gỡ popup cũ** (và endpoint cũ hết người gọi) |
| Q2 | Gói bảo dưỡng gom theo gì | **Loại sản phẩm mới**; hàng chưa quy đổi vào nhóm "Chưa phân loại"; bỏ nút "Chọn nhóm hàng" (chọn nhiều trong popup mới thay thế); dữ liệu gói đã lưu không đổi |
| Q3 | Báo giá DV — Loại hàng hoá chặn "Thiết bị"? | **Không chặn** (giữ như HRM hiện tại) |

## 5. Tự chốt
- Vỏ popup dùng chung `V2ProductPickerModal` (khung `V2BaseModal` theo mockup) bọc `ProductPickerPanel`; dùng cho cả 8 chỗ.
- `ProductPickerPanel` thêm prop thật `serviceQuotationOnly`, `scope` (thay vì đi lén qua `lockedFilters`).
- Vật tư theo thiết bị: dòng có máy (`product_id`) ⇒ chế độ máy; dòng thiết bị KH nhập tay (không có `product_id`) ⇒ danh sách thường — như ERP khi không có máy.
- Vật tư gói bảo dưỡng + Vật tư thay thế (lỗi thiết bị) ⇒ `serviceQuotationOnly` — như ERP. (Dev chưa có dữ liệu cờ Tính chất ⇒ 0 hàng, việc quy đổi chặn go-live.)
- Giữ các lời gọi lấy thông tin dòng hiện có (`line-info`, `products-info`) — chỉ đổi nguồn id.
- Ô chọn có tìm ở Tra cứu tồn công ty (`lookup/stock-companies`) chuyển sang API picker (`scope=trading` + gồm hàng chưa xếp catalog) để gỡ được endpoint cũ. Ô chọn ở Tab thiết bị KH (`assign/customers/manager/search-products`) không phải popup — giữ.
| Q4 (14/10, giữa lúc làm) | Chỗ chọn MÁY / THIẾT BỊ tìm trong phạm vi nào? | **Toàn bộ hàng** (kể cả ngừng KD, chưa xếp catalog; vẫn ẩn hàng tạm) cho: Gói bảo dưỡng (máy áp dụng), Lỗi thiết bị ("Áp dụng cho thiết bị"), Hàng tương đương (Xử lý YC BH, thêm thiết bị KH, tab thiết bị KH), Trang thiết bị KH. Chỗ chọn VẬT TƯ / hàng bán giữ hàng Đang KD. **Sửa ERP theo cho đồng bộ** (popup tương đương / thiết bị CSKH, lỗi thiết bị "Thiết bị", dịch vụ `sale/services`). BE `items` phải nhận phạm vi toàn bộ. |
