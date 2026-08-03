# Plan — Fix validate vượt SL HĐ giữa phiếu mượn & YCXH

## Bug
HĐ DHNT_TPE_HN_KDTM_26_0280_23.6.26, item TATE-TBTE-01 SL HĐ=1. Tạo được CẢ:
- YCXH PYCXH-32357 (`XUAT_BAN_HD_HANG`=type 14) SL1 — tạo 09:00, nay completed
- Phiếu mượn PYCXBHM-04002 SL1 — tạo 09:02, đã duyệt

→ đã xuất=1 + đang xuất=1 = 2 > 1 → còn lại=-1 → kẹt, không tạo được YCXH mới.

## Root cause (đã xác minh DB + code)
Hai luồng validate không dùng chung quỹ cam kết theo HĐ:
- YCXH: `ProductExportRequest::validateProducts` (model:1968) → `quantity - exported_qty - getExportingQty < qty`. `FirmContractTabProduct::getExportingQty` (model:144) đếm YCXH (XUAT_BAN_HD_HANG) + warehouse in-flight, **KHÔNG đếm BorrowSellRequest**.
- Phiếu mượn: `BorrowSellRequestsController@store:403` → `contract_qty - exported_qty < qty`. **KHÔNG trừ getExportingQty (YCXH in-flight) lẫn phiếu mượn in-flight**.

Lỗ hổng 2 chiều. Constant: XUAT_BAN_HD_HANG=14, XUAT_KM_HD_HANG=15.

## Quy tắc đã chốt (user)
- Quỹ: `Σ SL YC xuất bán hàng mượn (in-flight) + Σ SL YC xuất hàng (in-flight) + đã xuất ≤ SL HĐ`, tính theo từng item.
- KHÔNG liên quan logic trả hàng mượn / hoàn quỹ.
- Đối xứng 2 chiều: validate YC xuất hàng phải tính thêm YC xuất bán hàng mượn, và ngược lại.
- Chỉ chặn tại validate lúc **tạo phiếu** (store). Không cần chặn ở approve.

## Tasks
- [x] Điều tra root cause + xác minh DB (số liệu HĐ 22685, 2 phiếu)
- [x] Chốt nghiệp vụ với user
- [x] Verify `exported_qty` tăng từ CẢ 2 loại (BorrowSell.php:481 khi duyệt mượn; ProductExport.php:1613/1643/1726 khi xuất YCXH) → bucket "đã hoàn tất". In-flight đếm riêng (YCXH status∈[2,7,10,11], borrow status=2) → KHÔNG double-count. Tham chiếu công thức chuẩn: FirmContractProductExportService:137-139.
- [x] Thêm `FirmContractTabProduct::getBorrowingQty($except)` (mirror getExportingQty; bsrtp join borrow_sell_requests status=2, lọc firm_contract_id+parent_id+product_id)
- [x] Sửa `ProductExportRequest::validateProducts` (nhánh XUAT_BAN_HD_HANG, model:1968) trừ thêm `getBorrowingQty()`
- [x] Sửa `BorrowSellRequestsController@store` (~409) trừ thêm `getExportingQty(0)` + `getBorrowingQty($object->id)` (guard chỉ khi FirmContractTabProduct)
- [x] php -l sạch 3 file; verify tinker: getBorrowingQty=1 cho phiếu mượn status=2 (PYCXBHM-04004); item bug available=0
- [x] Xác nhận controller validateProducts chỉ check tồn kho (không trùng quota) + borrow controller chỉ 1 site validate
- [ ] User test browser 4 ca: xuất→mượn, mượn→xuất, đúng hạn mức, vượt hạn mức (FE đã hiện toastr "Số lượng không hợp lệ" từ BE — user chỉ yêu cầu chặn ở validate)

### Checkpoint — 2026-06-23
Vừa hoàn thành: Fix đối xứng 2 chiều validate quỹ HĐ (mượn↔xuất) tại store, thêm getBorrowingQty, php -l sạch, verify tinker.
Đang làm dở: không.
Bước tiếp theo: User test browser 4 ca + (nếu OK) commit.
Blocked:

### Checkpoint — 2026-06-23 (FIX #2 — root cause guard need_check_exported)
User test trên dev_128 (HĐ 1120, item 11153, YCXH 1025 status=11 + borrow 151): borrow KHÔNG bị chặn.
Root cause: `BorrowSellRequestsController@store` guard `$object->contractable->need_check_exported` = **NULL với FirmContract** (accessor này chỉ có ở ServiceContract/BorrowSell, KHÔNG có ở FirmContract) → toàn bộ check SL (cả phần fix #1) bị bỏ qua cho mọi phiếu mượn gắn HĐ hãng.
Fix: với `contractable_type == FirmContract` → luôn `$need_check_exported = true`; HĐ dịch vụ giữ theo cờ cũ.
Verify tinker: getExportingQty(0)=1, getBorrowingQty(except 151)=0 → còn lại = 1−0−1 = 0 < 1 → CHẶN đúng. php -l sạch.
LƯU Ý: dev_128 (dev-erp.dnsmedia.vn) cần PULL code mới mới có hiệu lực (fix #1 + #2 chưa chắc đã deploy lên dev server đó).
Cân nhắc thêm: getExportingQty chỉ đếm YCXH status [2,7,10,11]; nếu nghiệp vụ cần chặn cả khi YCXH ở status 1 (đã đề nghị)/3 (đang tạo) thì phải mở rộng tập status (đồng bộ cả validate YCXH-vs-YCXH) — chờ user xác nhận.

## Lưu ý
- `getExportingQty` là HÀM DÙNG CHUNG → cần xác nhận trước khi sửa (CLAUDE.md).
