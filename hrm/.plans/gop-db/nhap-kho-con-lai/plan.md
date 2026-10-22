# Kho › Nhập kho — 4 màn còn lại — Plan

> Design: `.plans/gop-db/nhap-kho-con-lai/design.md` · Nhánh `feat/kho-nhap-kho-con-lai` (cả 2 repo, từ `develop`)

## Phase 0 — Khảo sát (xong 22/10)

- [x] 4 màn ERP + đếm dữ liệu (reimport 24, inventory import 1, exc shortage 6, hàng đợi 15) + chốt 4 câu với user

## Phase 1 — Chờ báo thừa, thiếu + Phiếu báo hàng thừa, thiếu (xong 22/10)

- [x] Quyền 4 tên y ERP (type 21, group "Xử lý thừa, thiếu nhập kho") cuối `PermissionsTableSeeder` — đã sync local
- [x] BE `Entities/ExcShortage/*`, `Services/ExcShortage/ExcShortageService` (hàng đợi, danh sách, chi tiết, nguồn từ PNK)
      + `ExcShortageWriteService` (tạo/sửa/gửi, xóa, Không duyệt, file, thông báo, lịch sử), `ExcShortageController`,
      route `finance/exc-shortage-imports` (+ `/queue*`), `CatalogHistoryService::GATED_TABLES`
- [x] FE `pages/warehouse/import-discrepancies` (hàng đợi) + `pages/warehouse/exc-shortage-imports` (danh sách, Thêm,
      Chi tiết, Sửa, popup Không duyệt), menu `warehouse.js` 2 link
- [x] PHPUnit `Modules/Finance/Tests/Feature/ExcShortageApiTest.php` 11/11
- [x] Playwright bấm thật: hàng đợi 15 phiếu → Báo hàng thừa thiếu → báo lỗi bắt buộc → Lưu và gửi → danh sách → Chi tiết
      (Xử lý ERP, Không duyệt popup lý do) → Lịch sử → Sửa → Lưu → Xóa → PNK về lại hàng đợi; Thêm mới chọn PNK qua popup.
      Dữ liệu thử đã dọn (phiếu, lịch sử, thông báo). File đính kèm KHÔNG upload thật lên S3 (gắn URL giả vào form).

### Verify lại 22/10 (user "chạy verify màn") — đối chiếu checklist skill erp-to-hrm-screen

- [x] Sửa 6 điểm lệch quy ước: nhãn "Người lập/Ngày lập" → "Người tạo/Ngày tạo" (cột, lọc, Excel BE+FE); phân trang
      mặc định 10; Diễn giải `col-12` + textarea; phiếu không tồn tại → `/pages/extras/404` (+ `X-Silent-Errors`);
      lịch sử file = bảng ảo URL qua `LogsCatalogHistory` (gỡ file cũng ghi log); toast QLDA "… thành công."
- [x] Grep tự kiểm của skill: 0 vi phạm. PHPUnit 12/12 (thêm ca lịch sử đổi file)
- [x] Thông báo "Chờ xử lý" kiểm THẬT (transaction thật rồi dọn): người duyệt quản lý phòng người lập nhận, người duyệt
      không quản lý phòng không nhận (y ERP `is_same_department`)
- [x] Playwright: tiêu đề cột 2 màn, phân trang 1–10 / 15, form textarea, 404
- Khuôn khối form: `V2BaseFormSection` theo màn Kho mới nhất (Điều chuyển vị trí, user chốt 20/10) — checklist skill
  còn ghi nhóm kho dùng `V2BaseFormCard` (cũ hơn).

## Phase 2 — Phiếu nhập kho điều chỉnh kiểm kê (xong 22/10)

- [x] Quyền 2 tên y ERP "Xem phiếu nhập kho điều chỉnh kiểm kê - theo tổng công ty / - theo công ty" (type 21, guard api)
      cuối `PermissionsTableSeeder` — đã sync local (101231-101232). Lập phiếu theo "Xử lý phiếu kiểm kê hàng hóa", bước
      Kế toán kho theo "Kế toán kho" (đã có bản api).
- [x] `PhysicalStockWriter::importLot` thêm 2 khoá TUỲ CHỌN `stock_log_object` / `detail_log_type` (+ `NHAP_DIEU_CHINH = 3`)
      — không truyền thì y cũ (user cho mở rộng, PHPUnit tồn đầu kỳ / thừa thiếu vẫn xanh).
- [x] BE `Entities/WarehouseInventoryImport/WarehouseInventoryImport`, `Services/InventoryImport/WarehouseInventoryImportService`
      (danh sách, chi tiết, nguồn từ phiếu kiểm kê, Excel, In mẫu 294 / 293 + trần 2.000 dòng) +
      `WarehouseInventoryImportWriteService` (Lưu / Gửi duyệt ghi tồn 8 bảng — lô type 3 `NHAPDIEUCHINH-…`, sửa, file, thông
      báo Kế toán kho cùng công ty người gửi, lịch sử, phiếu kiểm kê → Đang xử lý), `WarehouseInventoryImportController`,
      route `finance/warehouse-inventory-imports`, `CatalogHistoryService::GATED_TABLES`.
- [x] Sửa lỗi ERP: `stock_logs.change` nhân hệ số ĐVT; `stock_of_companies` đúng công ty phiếu (ERP null); dòng hàng lấy lại
      ở server + khoá phiếu kiểm kê khi tạo; xem phiếu kiểm phạm vi (ERP `canView = true`).
- [x] FE `pages/warehouse/inventory-imports` (danh sách + Xuất Excel + In danh sách, Thêm từ `?self_inventory_id=`, Chi tiết
      với "Tạo phiếu nhập hàng" → ERP cho Kế toán kho + In, Sửa), menu `warehouse.js`. Nút ở Chi tiết phiếu kiểm kê đổi
      từ ERP sang màn HRM (`SelfInventoryService::INVENTORY_IMPORT_CREATE_PATH`, cờ `inventory_import_create_path`).
- [x] Không có "Tạo mới" ở danh sách (nút "Thêm" ERP mở form rỗng không chọn được phiếu kiểm kê); không có Xóa (y ERP).
      Thêm hộp xác nhận trước "Gửi duyệt" (ghi tồn ngay, không sửa được nữa).
- [x] PHPUnit `WarehouseInventoryImportApiTest` 9/9 (dựng phiếu kiểm kê thử trong ca — local không có hàng thừa chưa xử lý)
- [x] Playwright bấm thật: Chi tiết phiếu kiểm kê → nút → form Thêm (2 dòng thừa) → báo lỗi bắt buộc → Lưu → danh sách →
      Chi tiết → In → Sửa → hộp xác nhận Gửi duyệt (Hủy) → Lưu → In danh sách → 404. Gửi duyệt THẬT (ghi tồn) chỉ kiểm bằng
      PHPUnit để không đổi tồn local. Dữ liệu thử đã dọn.

## Phase 3 — Phiếu nhập lại điều chỉnh sai số liệu (chưa làm)

## Checkpoint — 2026-10-22

- **Vừa hoàn thành:** Phase 1 + Phase 2 (chưa commit).
- **Bước tiếp theo:** Phase 3.
- **Ghi chú test:** thông báo "Chờ xử lý" gửi người có quyền Duyệt + quản lý phòng ban người lập (ERP `is_same_department`) —
  local chưa ai giữ quyền mới nên chưa thấy thông báo này; thông báo "Không duyệt" tới người lập đã kiểm thật.
