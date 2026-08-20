# Plan — Sắp xếp lại menu phân hệ Cung ứng

**Người phụ trách:** @khoipv
**Ngày tạo:** 2026-08-10
**Spec chi tiết:** `docs/superpowers/specs/2026-08-10-menu-supply-sap-xep-design.md`

## Phase 1 — FE

- [x] FE1: Viết lại `hrm-thanhan-client/utils/MenuSupply.js` theo cấu trúc 4 nhóm (Tổng quan / Phiếu đề xuất cung ứng / Xử lý cung ứng ▾ / Mua hàng ▾ / Báo cáo ▾)
- [x] FE2: Set `isShow` cho cả menu cha (tránh dropdown rỗng khi user thiếu quyền)
- [x] FE3: Verify headless — parse `menu` bằng node OK (5 mục: 2 link phẳng + 3 dropdown); đối chiếu 5 chuỗi `isShow` với BE (`SupplyProposal::PERM_VIEW/PERM_HANDLE`, `PurchaseContractService::PERM_VIEW`, `PurchaseOrderService::PERM_VIEW`, middleware route báo cáo) → khớp 100%; 7 link đều có page tương ứng; `active()` xử lý được cả route name (subItems) lẫn path (link phẳng)

## Phase 2 — Verify UI

- [x] V1: User mở `/supply/...` kiểm tra dropdown hiển thị đúng, highlight đúng khi vào từng màn

## Checkpoint

### Checkpoint — 2026-08-10
Vừa hoàn thành: FE1–FE3, đã viết lại `utils/MenuSupply.js` (chỉ 1 file thay đổi)
Đang làm dở: không
Bước tiếp theo: V1 — user mở `/supply/...` xác nhận dropdown + highlight
Blocked:
