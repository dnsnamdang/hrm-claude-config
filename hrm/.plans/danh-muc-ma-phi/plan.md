# Danh mục mã phí (port ERP → HRM) — plan

Port `cost_debts` (ERP CostDebt) sang HRM Modules/Finance, nhân khuôn "vụ việc" (Work).
Quyết định: DB gộp (bảng `cost_debts` sẵn có), toàn cục (không phân cấp), 1 quyền
"Quản lý danh mục mã phí", xóa/khóa chặn khi đã dùng ở `account_details.cost_debt_id`.

## Tasks
- [x] BE Entity `CostDebt` (table cost_debts, canDelete qua account_details.cost_debt_id)
- [x] BE Service `CostDebtService`
- [x] BE Controller `V1/CostDebtController`
- [x] BE Request `CostDebtRequest` (unique cost_debts.code)
- [x] BE Resource List + Detail
- [x] BE Routes: group `cost-debts` gate `Quản lý danh mục mã phí`
- [x] BE Seeder: permission "Quản lý danh mục mã phí" (type=8)
- [x] FE pages/finance/cost-debts/{index.vue, CostDebtModal.vue}
- [x] FE finance.js: mục "Danh mục mã phí" → link /finance/cost-debts
- [x] DB erp_hrm_check: gán quyền "Quản lý danh mục mã phí" cho role 18
- [x] php -l + verify

### Checkpoint — 2026-08-04
Vừa hoàn thành: BE+FE mã phí + quyền, push gop_db. Bước tiếp: user verify + yarn dev.
Blocked:

---

## Bugfix — 405 khi bấm Sửa (cùng pattern works)
**Root cause:** route group `cost-debts` thiếu `GET /{id}` (show); FE `CostDebtModal` gọi `GET finance/cost-debts/{id}` → 405.
**Fix (BE):** `CostDebtService::getCostDebt` + `CostDebtController::show` (CostDebtDetailResource, 404 nếu không thấy) + route `GET /{id}` (checkPermission:Quản lý danh mục mã phí). Verified show trả id/code/name/note/status/is_can_delete.
## Bugfix — bộ lọc Trạng thái lỗi (mặc định rỗng = không hiện gì, không chọn được Tất cả)
**Root cause:** option `{ id: undefined, name: 'Tất cả' }` — V2BaseSelect map thành `{id: undefined}`; khi mount select tự chọn "Tất cả" và emit `status="undefined"` → BE `filled('status')`=true → `where status='undefined'` → 0 dòng. Đồng thời không click chọn lại "Tất cả" được.
**Fix (FE):** bỏ option "Tất cả"; `V2BaseSelect` thêm `:allowClear="true" placeholder="Tất cả"`. Trạng thái rỗng = tất cả (BE dùng filled). Áp cho `pages/finance/cost-debts/index.vue` + `pages/finance/works/index.vue` (dính y hệt). Compile OK.
**Đã sửa luôn (cùng lần):** `pages/master-data/{provinces,areas,wards,nations}/index.vue` — cùng fix. Toàn repo hết pattern `{id:undefined,name:'Tất cả'}` (6/6 chỗ). Compile OK.
