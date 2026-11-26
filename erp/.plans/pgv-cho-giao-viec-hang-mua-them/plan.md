# Chờ giao việc bỏ sót HĐDV còn hàng hoá mua thêm — plan

Báo 26/11/2026: PGV TPSG.PGV.2026020421 (id 20421) giao hết công/dịch vụ của HĐDV id 9171
nhưng hàng hoá mua thêm giao SL 0 → vào "Chờ giao việc" không thấy HĐ để giao tiếp.

Nguyên nhân: `WrServiceContract::getQuantityHasRepair()` (lọc tab HĐ/PLBS màn Chờ giao việc + đếm trang chủ)
và `canAssignTask()` (nút "Tạo phiếu giao việc") chỉ xét sửa chữa / dịch vụ / dịch vụ mở rộng, không xét
`wr_service_contract_merchandises`. Màn lập PGV thì có tính hàng mua thêm còn lại =
`qty - annex_qty - getAssigningMerchandiseQty()`.

Nhánh: develop_02 (sau đó gop_db). User duyệt sửa hàm dùng chung 26/11.

## Tasks
User chốt phạm vi 26/11: chỉ tính dòng hàng mua thêm **chưa xuất kho hết** (`exported_qty < qty - annex_qty`) —
nếu tính tất cả thì thêm 155 HĐ (134 HĐ chưa từng có PGV, đa số hàng đã xuất thẳng).

- [x] `getQuantityHasRepair()`: nối thêm `getContractIdsHasMerchandiseToAssign()` (bulk query, mirror `getAssigningMerchandiseQty`, lọc HĐ/PLBS có hiệu lực, bỏ dòng đã xuất hết)
- [x] `canAssignTask()`: thêm vòng hàng hoá mua thêm (cùng công thức, bỏ dòng đã xuất hết)
- [x] Kiểm trên hrm_erp_gop (script đọc): 54 HĐ còn hàng mua thêm cần giao, **28 HĐ mới** vào danh sách, có HĐ 9171; đối chiếu từng HĐ với công thức per-row (`getAssigningMerchandiseQty`) → 0 lệch; `getQuantityHasRepair` 0,41s. `canAssignTask()` HĐ 9171: nhánh hàng mua thêm ra còn hàng (vd vít nở DK16 còn 20); user 461 thử ra false vì thiếu quyền `phieu_giao_viec.create` trong ngữ cảnh script, không do code mới.
- [ ] Kiểm trên màn thật (Chờ giao việc → tab HĐ thấy 9171 → lập PGV giao hàng mua thêm)
- [x] Commit/push develop_02 `bc0504f082` + gop_db `1aff446848` (26/11/2026)

### Checkpoint — 2026-11-26 (wrap up cuối ngày)
Vừa hoàn thành: `getContractIdsHasMerchandiseToAssign()` + `canAssignTask` xét hàng mua thêm chưa xuất hết; kiểm script 28 HĐ mới (có 9171), 0 lệch; push develop_02 `bc0504f082` + gop_db `1aff446848`.
Đang làm dở: (không)
Bước tiếp theo: kiểm màn thật (Chờ giao việc → HĐ 9171 → lập PGV hàng mua thêm).
Blocked: (không)
