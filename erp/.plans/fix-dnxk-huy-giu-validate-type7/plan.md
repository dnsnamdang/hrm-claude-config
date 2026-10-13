# Fix: ĐNXK điều chuyển kho chi nhánh (qua kho) — nút Lưu bị chặn câm khi chưa huỷ giữ

**Nhánh:** `gop_db` (ERP TanPhatDev)
**Màn:** Đề nghị xuất kho — `warehouse.warehouse_export_requests` (route `warehouseExportRequest.create/edit`)
**Loại phiếu:** YCXH điều chuyển kho chi nhánh `type = 7`, nhánh **qua kho** (`is_export_direct = false`)

## Vấn đề

Khi số lượng xuất được ở màn ĐNXK không đủ (vì hàng đang bị người yêu cầu điều chuyển GIỮ), FE
khoá luôn nút **Lưu** và **Lưu và gửi** mà không hiện thông báo gì → người lập phiếu không biết
phải **huỷ giữ** trước mới làm tiếp được.

Nguyên nhân: getter `can_export` của dòng chi tiết (`WarehouseExportRequestDetail`) trả `false`
khi `qty > min(in_stock + prepick_qty, in_warehouse) - in_promotion_stock`, nút bị `ng-disabled`
nên POST không bao giờ tới BE — mà BE (`TransferHoldValidator`) mới là nơi có thông báo đúng
"Còn hàng đang giữ tại công ty nguồn. Cần hủy giữ trước khi lập đề nghị xuất kho."

## Hướng xử lý (user chốt: Hướng A)

Với **type 7 qua kho** (`!is_export_direct`): bỏ khoá nút theo số lượng ở FE — để **BE làm cổng
chốt**. Getter `can_export` của dòng trả `true` cho nhánh này, nút luôn bấm được, POST tới BE,
BE validate huỷ-giữ và trả message rõ ràng để FE hiện (markup sẵn ở `form.blade.php:11-14`).

## Tasks

- [x] Xác minh `is_export_direct` có mặt trong payload `parent` ở CẢ 2 đường:
  - Tạo mới: `ProductExportRequest::getDataForWarehouseExportRequest()` trả `$req->toArray()` (gồm `is_export_direct`)
  - Sửa: `WarehouseExportRequest::getDataForEdit()` eager-load `parent` không giới hạn cột → `parent.is_export_direct` có mặt
- [x] Sửa `resources/views/partials/classes/warehouse/WarehouseExportRequestDetail.blade.php`
  getter `can_export`: thêm early-return `true` cho `type == 7 && !parent.parent.is_export_direct`
  (ngay sau `if (!this.need_export) return true;`)
- [x] Xác nhận `invalidQty` chỉ kiểm tra khớp SL theo tab (không liên quan tồn/giữ) → giữ nguyên
- [ ] Verify trình duyệt: mở ĐNXK type 7 qua kho với hàng đang bị giữ → nút Lưu/Lưu và gửi bấm
  được → BE trả message huỷ-giữ → FE hiện khối `errors.transfer_hold`

## Ghi chú

- Đây là sửa getter Angular dùng chung của màn ĐNXK — user đã duyệt riêng thay đổi này ("A").
- Không đụng BE: `TransferHoldValidator` + block trong `WarehouseExportRequestsController::store/update`
  đã đúng và đã có message.
