# #10451 — Plan: thêm 3 cột VAT vào màn Phiếu cung cấp thông tin

**Mục tiêu:** Màn *Phiếu cung cấp thông tin* (warranty_repair_information_requests) hiển thị 3 cột **VAT · Tiền VAT · Thành tiền sau VAT** ở mục B/I (Công / Dịch vụ / Vật tư), khớp màn *Báo giá dịch vụ*.

**Phạm vi thật:** CHỈ 1 file FE — `resources/views/customercare/warranty_repair_information_requests/form.blade.php`.
Show auto-khớp (`@include form`). Bản in đã có sẵn (service `WarrantyRepairServiceQuotationPrint` dùng chung, data-row phát đủ VAT). Không migration, không BE.

**Vị trí chèn (parity báo giá DV):** 3 cột đặt **sau "Loại công việc", trước "Thời gian có vật tư (ngày)"**.
Nhãn + class y hệt reference: `<th class="space-normal">VAT</th>` · `<th class="space-normal">Tiền VAT</th>` · `<th class="space-normal">Thành tiền sau VAT</th>`.
Bind getter sẵn có (xác nhận đồng nhất cả 3 nhóm): `vat_percent` · `vat_cost | number` · `total_cost_after_vat | number`.

Header 14 cột → 17 cột. MỌI dòng `<tr>` trong tbody phải +3 ô để không lệch cột.

## Tasks

- [x] **T1 — Header:** chèn 3 `<th class="space-normal">` (VAT / Tiền VAT / Thành tiền sau VAT) sau th "Loại công việc" (`:375`), trước th "Thời gian có vật tư" (`:376`).

- [x] **T2 — Dòng thiết bị cha** (`:383-412`): chèn 3 `<td></td>` rỗng sau ô "Loại công việc" = ô select type_do (`:401`), trước ô `:408`. (Dòng header thiết bị, VAT để trống.)

- [x] **T3 — Nhóm Công** (`:413-441`): chèn 3 `<td>` sau ô "Loại công việc" rỗng (`:431`), trước ô "Thời gian" (`:432`):
  - `<td class="text-right v-align-middle"><% product_repair.vat_percent %></td>`
  - `<td class="text-right v-align-middle"><% product_repair.vat_cost | number %></td>`
  - `<td class="text-right v-align-middle"><% product_repair.total_cost_after_vat | number %></td>`

- [x] **T4 — Dòng header "Danh sách dịch vụ"** (`:443-460`): chèn 3 `<td class="text-center v-align-middle text-bold"></td>` rỗng sau ô `:455`, trước ô `:456`. (Hàng tiêu đề nhóm, VAT subtotal để trống như Thời gian/Ghi chú.)

- [x] **T5 — Dòng dịch vụ** (`ng-repeat service`, `:461-504`): chèn 3 `<td>` sau ô "Loại công việc" rỗng (`:489`), trước ô "Thời gian" (`:490`):
  - `<td class="text-right v-align-middle"><% service.vat_percent %></td>`
  - `<td class="text-right v-align-middle"><% service.vat_cost | number %></td>`
  - `<td class="text-right v-align-middle"><% service.total_cost_after_vat | number %></td>`

- [x] **T6 — Dòng header "Danh sách vật tư"** (`:506-524`): chèn 3 `<td class="text-center v-align-middle text-bold"></td>` rỗng sau ô `:519`, trước ô `:520`.

- [x] **T7 — Dòng vật tư** (`ng-repeat product_item`, `:525-566`): chèn 3 `<td>` sau ô "Loại công việc" rỗng (`:551`), trước ô "Thời gian" (`:552`):
  - `<td class="text-right v-align-middle"><% product_item.vat_percent %></td>`
  - `<td class="text-right v-align-middle"><% product_item.vat_cost | number %></td>`
  - `<td class="text-right v-align-middle"><% product_item.total_cost_after_vat | number %></td>`

- [x] **T8 — Verify Playwright** (ERP :8001 local, DB test): phiếu #8162 — màn **Xem** B/I = 16 cột (show ẩn Giá vốn), 3 cột VAT đúng vị trí sau "Loại công việc"; dòng Công hiển thị VAT=0/Tiền VAT=0/TT sau VAT=3,213,000 (vat%=0 → TT sau VAT = TT sau CK ✓). Màn **Sửa** B/I = 17 cột (có Giá vốn), VAT ở cột 11-13, mọi dòng colTotal=17 không lệch. Section A (bảo hành) giữ 13 cột KHÔNG VAT; Section II (bảo dưỡng) giữ nguyên không VAT. Console chỉ 404 ảnh (có sẵn), không lỗi Angular/JS. Công thức VAT dùng getter đồng nhất màn báo giá DV (đã chạy prod) → non-zero phủ bởi parity. Bản in dùng chung service, không đụng.

### Checkpoint — 2026-11-26
Vừa hoàn thành: T1-T8 — 5 edit vào `form.blade.php`, verify Playwright show+edit đầy đủ.
Đang làm dở: (không)
Bước tiếp theo: chờ user duyệt để commit/push (CHƯA commit).
Blocked: (không)

## Rủi ro / lưu ý
- `php -l` không áp (file .blade thuần HTML+Angular, không PHP logic mới) — chỉ cần kiểm cột không lệch.
- VAT% chỉ đọc (auto từ master), đúng nghiệp vụ reference — KHÔNG thêm input.
- Không đụng show.blade.php, không đụng service in, không đụng BE/migration.

### Checkpoint — 2026-11-26 (wrap up cuối ngày)
Vừa hoàn thành: commit + push ERP develop_02 `ea138fda86` (1 file `form.blade.php` +21); Redmine #10451 user tự đổi trạng thái (Code xong chờ test).
Đang làm dở: (không)
Bước tiếp theo: gop_db khi user yêu cầu; chờ tester.
Blocked: (không) — CHƯA gop_db.
