# Design (tóm tắt) — Duyệt HĐ "Không thực hiện" → Hủy hợp đồng

**Người phụ trách:** @khoipv
**Spec chi tiết:** `docs/superpowers/specs/2026-06-10-contract-cancel-not-executed-on-approve-design.md`

## Mục tiêu
TP bấm **Duyệt** HĐ có `result = 2` → HĐ chuyển **Hủy hợp đồng** + đẩy dự toán/báo giá/gói thầu sang trạng thái **Hủy hợp đồng** mới + ghi lịch sử kèm lý do.

## Quyết định lớn
- Tái dùng nút **Duyệt** (không nút/endpoint mới); `approve()` rẽ nhánh theo `result`.
- Thêm **const mới** cho cả 4 entity: Contract `HUY=5`, Quotation `HUY_HOP_DONG=19`, Project `HUY_HOP_DONG=18`, BidPackage `HUY_HOP_DONG=17`. Thêm `Contract::KHONG_THUC_HIEN=2` (result).
- Hủy HĐ thì **không** tạo snapshot version.
- FE thêm nhãn + màu (`pj-status-rose`) + filter cho trạng thái mới ở 4 màn danh sách.

## Điểm chạm
- BE: `Contract.php`, `Quotation.php`, `Project.php`, `BidPackage.php` (const); `ContractController::approve()` (rẽ nhánh); `ContractService::cancelDownstream()` (method mới).
- FE: `contract/contract` (index/approve/GeneralComponent), `bid_package/quotation/index`, `bid_package/bid_package/index`, `plan/project/index`.
