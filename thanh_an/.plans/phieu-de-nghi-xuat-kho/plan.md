# Plan — Phiếu đề nghị xuất kho (bản thật theo demo)

> @khoipv · Bắt đầu 25/11/2026
> Demo: `demos/demo-phieu-de-nghi-xuat-kho.html` · Design: [design.md](design.md) · Spec: [2026-11-25-phieu-de-nghi-xuat-kho-design.md](../../docs/superpowers/specs/2026-11-25-phieu-de-nghi-xuat-kho-design.md)

## Phase 1 — Tìm hiểu & chốt hướng
- [x] 1. Đọc demo ĐNXK + spec demo + spec demo PXK, module Warehouse (PNK) BE/FE, ma trận PXL (`alloc_<nguồn>_<pa>`, tab Đề nghị xuất kho trên PXL)
- [x] 2. Hỏi user: phạm vi bước Xuất kho (popup vs PXK riêng), ai lập phiếu, phân quyền theo cấp màn danh sách, điều kiện `is_can_delete`
- [x] 3. Viết spec + design, user duyệt ("đồng ý, viết spec rồi làm luôn")
- [x] 3b. (25/11) User bổ sung: chọn HĐ phải **Đã duyệt (3) / Đã kết xuất (9)** và **còn thời gian thực hiện** (`contract_end_time` ≥ hôm nay) → ghi vào spec C5, áp ở API `/contracts` + khi lưu / gửi
- [x] 4. Lên plan chi tiết BE / FE

## Phase 2 — BE (`hrm-thanhan-api/Modules/Warehouse`)
- [x] 5. Migration 3 bảng (`warehouse_export_requests`, `_products`, `_logs`) — chỉ index, không khóa ngoại
- [x] 6. Migration seed 4 quyền (nhóm Kho, type 7) + xóa cache spatie
- [x] 7. Entity `WarehouseExportRequest` (STATUSES + màu, quan hệ, accessor `is_can_edit/send/delete/recall/return`), `WarehouseExportRequestProduct`, `WarehouseExportRequestLog`
- [x] 8. `WarehouseExportRequestService`: list (3 cấp + thủ kho, lọc, sort whitelist, keyword), filter-options, contracts (C5), prepare (SL còn lại HĐ + tồn xuất được), store/update (validate, tách theo dòng PXL, lockForUpdate, sinh mã), recall, return, delete, show
- [x] 9. `SaveWarehouseExportRequestRequest`, `WarehouseExportRequestResource`, Controller, routes `/export-requests`
- [x] 10. Chạy migration + test API bằng script (rollback) — 49/49 case pass (quyền tạo, C5 popup + khi lưu, validate FormRequest, vượt SL còn lại HĐ, vượt tồn khi gửi, gửi kho → thông báo thủ kho, phạm vi danh sách 13/14/thủ kho 15, trả lại + lý do, sửa gửi lại, thu hồi, xóa, export)
  - Sửa: `down()` migration xóa quyền ở `employee_has_permissions` (dự án đổi tên bảng spatie), không phải `model_has_permissions`
  - Entity cache quyền Quản lý + kho thủ kho theo request (danh sách tính `is_can_*` từng dòng)
  - Lỗi nghiệp vụ trả `{message, data: {errors: {key: msg}}}` như PNK; lỗi FormRequest trả `errors` top-level → FE đọc cả 2

## Phase 3 — FE (`hrm-thanhan-client/pages/warehouse/export_requests`)
- [x] 11. `constants.js` + `exportRequestRules.js` (tồn xuất được dùng chung giữa các dòng cùng hàng, lỗi đỏ/cam, payload, banner)
  - Sửa: `normalizeRow` biến `''` thành `'0'` → SL gốc trống báo "phải > 0" thay vì "bắt buộc" → thêm `qtyText`
- [x] 12. Màn danh sách V2 (`index.vue`): 11 ô lọc (không lọc cột tiền), cấu hình cột, xuất Excel, hành động Thu hồi → Sửa → Xóa
  - Khác plan: **Trả lại không đặt ở danh sách** (cần nhập lý do → theo button-convention chỉ ở màn chi tiết)
- [x] 13. Form Tạo / Sửa (`components/ExportRequestForm.vue` + `ContractPickerModal.vue` + `er-goods.scss`): thông tin chung, popup chọn HĐ, bảng hàng (tick, SL còn lại HĐ, tồn xuất được, dòng đổi hàng có SL gốc), lỗi realtime, Lưu nháp / Gửi kho (xác nhận), chặn rời trang khi chưa lưu
- [x] 14. Màn chi tiết (`components/ExportRequestDetail.vue`, `_id/index.vue`): banner lý do (Bị trả lại / Đã hủy), tab Hàng hóa (Đã xuất, Còn phải xuất) / Lịch sử, footer Sửa → Thu hồi → Trả lại (lý do bắt buộc) → Xóa
  - Khác demo: không có banner trạng thái chung (user đã bỏ ở màn PNK 20/11); không có nút "Gửi kho" ở chi tiết → Sửa rồi Gửi kho trong form
- [x] 15. Menu `utils/MenuWarehouse.js` → nhóm Xuất kho → Phiếu đề nghị xuất kho
- [x] 16. Tự kiểm: compile template + script toàn bộ file .vue OK, compile SCSS OK, test logic rules bằng node (ALL PASS)
- [x] 16b. (25/11) Thêm 4 quyền vào `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (id 529–532, khớp id DB local)
- [x] 16c. (25/11) Màn phân quyền không thấy quyền Kho (type 7 nằm lẫn trong Phân hệ cung ứng) → user chọn tách **Phân hệ kho** riêng:
  - Type 16 cho nhóm "Kho": seeder (527–532), migration ĐNXK, migration mới `2026_11_25_000002_move_warehouse_permissions_to_own_module` (đổi type cả quyền PNK đã chạy), đã migrate local
  - `components/setting/Permission.vue` (component dùng chung, user đã đồng ý) thêm mục "Phân hệ kho" → `filterPermission(16)`
  - Sự cố: chạy seeder làm mất 527/528 (PNK chưa có trong seeder) → đã thêm vào seeder + insert lại DB local
- [x] 16d. (25/11) Chia Phân hệ kho thành 3 nhóm: **Nhập kho** (527) / **Xuất kho** (529–532) / **Báo cáo kho** (528) — seeder + migration ĐNXK + migration 000002 (rollback, sửa, migrate lại local). Không dùng tên "Báo cáo" vì type 3 đã có nhóm trùng tên (FE gộp nhóm theo tên)
- [x] 16e. (25/11) Form: bỏ chú thích "Mỗi phiếu chỉ xuất từ 1 kho" dưới ô Kho xuất
- [x] 16f. (25/11) Seeder dữ liệu giả để test ĐNXK (`Modules/Warehouse/Database/Seeders/ExportRequestFakeDataSeeder.php` + `ExportRequestFakeDataCleanSeeder.php`)
  - Dùng HĐ thật (Đã duyệt/Đã kết xuất, còn hạn, chưa có PXL, hàng có hệ số ĐVT) → dựng đề xuất `FAKE-DXCU-*` + PXL đã duyệt `FAKE-PXL-*` (Xuất bán = lấy tồn + mua)
  - 2 kho giả `FAKE-KHO-HN` (thủ kho 15, 17) / `FAKE-KHO-HCM` (thủ kho 13 DNS Admin); tồn nhập qua PNK (xem 16j)
  - Kịch bản: đủ tồn + lô giữ cho HĐ + lô hết hạn · thiếu tồn kho HN (đủ ở HCM) · dòng đổi hàng · 2 PXL cùng hàng (gộp dòng) · HĐ đã có ĐNXK Nháp / Chờ xuất kho / Bị trả lại · HĐ đã đề nghị hết (không hiện popup)
  - Chạy lại được (dọn dữ liệu FAKE trước khi tạo), không sửa HĐ thật
  - Chỉ lấy dòng HĐ giá > 0, SL giới hạn 300 (HĐ thật có SL mL rất lớn); chặn chạy trên production
  - Đã chạy local + kiểm qua service `contracts()` / `prepare()`: popup thêm HD-168/167/166/162/161, HD-160 (đề nghị hết) không hiện; tồn / lô giữ / lô hết hạn / chờ xuất trừ đúng
- [x] 16g. (25/11) Popup chọn HĐ (`ContractPickerModal.vue`): bỏ cột "Số dòng phù hợp" (BE vẫn trả `lines_left`, không ảnh hưởng)
- [x] 16h. (25/11) Popup chọn HĐ: cột "Hạn thực hiện" → "Thời gian thực hiện" = ngày ký - ngày kết thúc (BE `contracts()` trả thêm `execution_time`; `contract_time` ở DB toàn 0000 nên dùng `contract_sign_time`)
- [x] 16i. (25/11) Form: bỏ khung "Ghi chú" (3 dòng giải thích SL còn lại / tồn xuất được / dòng ĐỔI) dưới bảng hàng; ô tổng dồn sang phải
- [x] 16j. (25/11) Seeder: tồn giả đi đúng **luồng nhập kho** thay vì ghi thẳng `stock_balances` (doc_type FAKE)
  - Mỗi kho 1 đơn mua `FAKE-DMH-HN/HCM` (Hoàn thành, NCC lấy từ đơn mua thật mới nhất) → phiếu giao hàng `FAKE-PGH-HN/HCM` (Hoàn thành, 1 điểm giao về kho) → PNK Đã nhập kho (mã `PNK-2026-####` sinh bằng `generateCode()`)
  - Ghi tồn + thẻ kho bằng chính `WarehouseReceiptService::writeStock` (protected → gọi qua closure) → thẻ kho `doc_type PNK`; `rebuildStockFromReceipts()` không còn bị chặn bởi dòng FAKE
  - Lô giữ cho HĐ = mục đích `h0` kind hold (KH + HĐ), lô hết hạn = lô có HSD quá khứ; số lô `LO<ymd>-NNN`, HSD mặc định +18 tháng
  - Dọn: thêm serial / lô / dòng / PNK theo kho giả + PGH / đơn mua mã `FAKE-%`
  - Đã chạy 2 lần local: PNK-2026-0003 (HN, 29 dòng) / PNK-2026-0004 (HCM, 20 dòng); `prepare()` ra số tồn như bản cũ (lô giữ 100, lô hết hạn không tính); `detail()` PNK đọc được
- [ ] 18. (25/11) Yêu cầu mới: chọn HĐ → ưu tiên hàng đã có phiếu đề xuất, **chọn thêm được hàng HĐ chưa có phiếu đề xuất** — đang chốt yêu cầu (xem Q-E, Q-F)
- [ ] 17. User test trên trình duyệt (tạo → gửi kho → thủ kho trả lại → sửa gửi lại → thu hồi → xóa)

### Checkpoint — 25/11/2026
Vừa hoàn thành: FE task 11–16 (danh sách, form tạo/sửa, chi tiết, menu); thêm Thu hồi vào cột hành động danh sách
Đang làm dở: không
Bước tiếp theo: user test trên trình duyệt theo task 17, báo lỗi nếu có
Blocked:

## Câu hỏi mở
- [x] Q-A. Bước Xuất kho → **dừng ở Chờ xuất kho** (thủ kho chỉ Trả lại); Xuất kho / Đóng phần còn lại / trừ tồn làm cùng màn PXK riêng đợt sau
- [x] Q-B. Ai lập ĐNXK → **thêm quyền "Quản lý phiếu đề nghị xuất kho"**
- [x] Q-C. Phân quyền theo cấp → **3 cấp tổng cty / cty / nhóm nghiệp vụ**
- [x] Q-D. `is_can_delete` → **người lập + Nháp hoặc Bị trả lại**
- [ ] Q-E. "Hàng đã có phiếu đề xuất" = dòng PXL đã duyệt có ô Xuất bán (như hiện tại) hay có phiếu đề xuất cung ứng (DXCU) bất kỳ, kể cả chưa lên PXL?
- [ ] Q-F. Hàng có đề xuất 1 phần (HĐ 100, đề xuất 60) → 40 còn lại có thêm được như hàng ngoài đề xuất không? (đề xuất: có)
