# Báo cáo fix nhãn "Từ chối lập gói thầu" (label-only)

Ngày: 2026-06-23 — @khoipv

Mục tiêu: thêm nhãn hiển thị trạng thái mới ở các màn còn thiếu (chỉ label/màu/option,
KHÔNG thêm nút/hành động).

- Báo giá (quotation): status = 20 → "Từ chối lập gói thầu", màu đỏ.
- Dự toán (project): status = 19 → "Từ chối lập gói thầu", màu đỏ.

---

## Nhóm BÁO GIÁ (status 20)

### 1. pages/plan/quotation/index.vue
- `getStatusText()`: thêm nhánh `status == 20` → return 'Từ chối lập gói thầu' (sau nhánh 19).
- `statusColorMap`: thêm `20: 'status-pill pj-status-red'` (sau key 19).
- Ghi chú: file có dropdown `statuses` nhưng yêu cầu chỉ làm getStatusText + statusColorMap → KHÔNG thêm option vào `statuses`.

### 2. pages/plan/quotation/waiting-approve.vue
- `getStatusText()`: thêm nhánh `status == 20` → 'Từ chối lập gói thầu'.
- `statusColorMap`: thêm `20: 'status-pill pj-status-red'`.

### 3. pages/contractor/quotation/index.vue
- File này dùng `getStatusClass()` (không có statusColorMap).
- `getStatusClass()`: thêm nhánh `status == 20` → return 'status-pill pj-status-red' (theo pattern nhánh 19 dùng pj-status-rose).
- `getStatusText()`: thêm nhánh `status == 20` → 'Từ chối lập gói thầu'.

### 4. pages/contract/quotation_render/index.vue
- `getStatusText()`: thêm nhánh `status == 20` → 'Từ chối lập gói thầu'.
- `statusColorMap`: thêm `20: 'status-pill pj-status-red'`.

---

## Nhóm DỰ TOÁN (status 19)

Lưu ý: bên dự toán status 18 = 'Hủy hợp đồng' (KHÔNG phải 19 như báo giá),
status MỚI của dự toán là 19 = 'Từ chối lập gói thầu'.

### 5. pages/plan/project/index.vue
- `statusOptions`: thêm `{ id: 19, text: 'Từ chối lập gói thầu' }` (sau option id 18).
- `statusColorMap`: thêm `19: 'status-pill pj-status-red'`.
- `getStatusText()`: thêm nhánh `status == 19` → 'Từ chối lập gói thầu' (sau nhánh 18).

### 6. pages/bid_package/project/index.vue
- `statusOptions`: thêm `{ id: 19, text: 'Từ chối lập gói thầu' }`.
- `statusColorMap`: thêm `19: 'status-pill pj-status-red'`.
- `getStatusClass()`: thêm nhánh `status == 19` → 'status-pill pj-status-red'.
- `getStatusText()`: thêm nhánh `status == 19` → 'Từ chối lập gói thầu'.

---

## Filter báo cáo (chỉ thêm option 19)

### 7. pages/sale/detail-report/index.vue
- `statusOptions`: thêm `{ id: 19, text: 'Từ chối lập gói thầu' }` (sau id 18 'Hủy hợp đồng'). Không sửa gì khác.

### 8. pages/sale/report-project-contract/index.vue
- `statusOptions`: thêm `{ id: 19, text: 'Từ chối lập gói thầu' }` (sau id 18 'Hủy hợp đồng'). Không sửa gì khác.

---

## Dashboard BE (status 20)

### 9. Modules/Category/Services/CategoryDashboardService.php
- Hàm `getAllQuotationStatusMapping()`.
- Đã thêm `Quotation::TU_CHOI_LAP_GOI_THAU` vào nhóm "Không thực hiện"
  (nhóm có id = Quotation::KHONG_DUYET), cùng nhóm với KHONG_DUYET, HUY,
  TP_KHONG_DUYET, BGĐ_KHONG_DUYET, HUY_HOP_DONG — đây là nhóm gom các trạng thái hủy/không thực hiện.
- Hằng số `Quotation::TU_CHOI_LAP_GOI_THAU = 20` đã tồn tại sẵn
  (Modules/Category/Entities/Quotation/Quotation.php:110).
- Kết quả `php -l`: No syntax errors detected.

---

## Ghi chú chung
- Tất cả màu đỏ dùng class `status-pill pj-status-red` để bám theo class các file đang dùng
  (status 19/18 'Hủy hợp đồng' dùng pj-status-rose; status mới dùng pj-status-red giống các trạng thái hủy khác trong cùng file).
- Không thêm nút/hành động, không đổi logic nghiệp vụ.
- Không có file nào đã có sẵn nhãn 20/19 từ trước → tất cả 9 file đều cần và đã được sửa.
