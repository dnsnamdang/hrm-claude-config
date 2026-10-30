# Phiếu công tác: lọc theo Hợp đồng không ra HĐ bán

Không Redmine · @junfoke · `hrm-api`, nhánh `gop_db`

## Ngày 30/10/2026 (@junfoke)
- [x] 30/10/2026 — Xử lý: tìm PCT theo HĐ `HĐ_TPE_HN_KD1_26_0857_VDCBG` ra rỗng — HĐ bán chỉ lưu ở `assign_business_tasks.contractable_code`, bộ lọc chỉ tìm cột cũ `wr_service_contract_code` (625 dòng local bị ảnh hưởng). Lọc thêm `contractable_code` ở danh sách PCT, xuất Excel (`AssignBusinessService`) và Việc của tôi (`MyJobService`); cột "Hợp đồng" lấy `contractable_code` trước, rỗng mới lấy cột cũ (2 resource + Excel). Kiểm local: 0 → 1 phiếu (PCT-13322). Commit `c2d9376dc` — đã lên origin/gop_db + develop.
