# #11512 Phiếu duyệt KQ (HĐDV) — chặn hàng bán thêm / vật tư chưa đủ SL bàn giao

Nhánh: develop_02 (worktree `ERP/TanPhatDev-11512`, nhánh `fix/11512-dkq-hang-ban-them`)

## Hiện trạng
- `WrApproveResultsController::hasProductExport()` chỉ chạy cho YC lắp đặt (`assembly`, HĐ hãng).
- Phiếu DKQ của HĐDV (`wr_service_contract_id`) không kiểm SL → hàng bán thêm chưa xuất vẫn duyệt được.

## Quy tắc chặn (bám phiếu DKQ lắp đặt)
- Gom SL giao theo (product_id, unit_id) từ: `merchandises[*].qty` (Hàng bán thêm),
  `product_repairs[*].items[*].qty`, `product_warrantys[*].items[*].qty` (Danh sách vật tư đi kèm lỗi thiết bị).
- SL được bàn giao = Σ `wr_service_contract_items.exported_qty` (HĐ + PLBS; cột này đã trừ nhập trả lại)
  − SL các phiếu DKQ khác của cùng HĐ đã ghi (wr_assign_tasks.parent_id NOT NULL, trừ chính phiếu đang sửa).
- Giao > SL được bàn giao → trả `type=check_product_export` (FE đã có sẵn cách hiện) với câu
  "Số lượng sản phẩm '<mã>' không đủ số lượng để bàn giao".

## Tasks
- [x] T1 BE: thêm `hasServiceProductExport()` + gọi ở store() và update() khi có wr_service_contract_id
- [x] T2 Kiểm thử php -l + tinker gọi hàm với dữ liệu local
- [x] T3 Commit develop_02 (hỏi trước khi push), đổi Redmine → Code xong chờ test

### Checkpoint — 2026-11-11 15:35
Vừa hoàn thành: push develop_02 18290bfc68 + gop_db 5defd8d2ba; Redmine #11512 → Code xong chờ test
Đang làm dở:
Bước tiếp theo: chờ QA test
Blocked:
