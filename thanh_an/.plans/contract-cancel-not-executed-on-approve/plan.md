# Plan — Duyệt HĐ "Không thực hiện" → Hủy hợp đồng

**Người phụ trách:** @khoipv
**Spec:** `docs/superpowers/specs/2026-06-10-contract-cancel-not-executed-on-approve-design.md`

## Phase 1 — Backend: hằng số

- [x] BE: `Contract.php` thêm `const HUY = 5;` + `const KHONG_THUC_HIEN = 2;`
- [x] BE: `Quotation.php` thêm `const HUY_HOP_DONG = 19;`
- [x] BE: `Project.php` thêm `const HUY_HOP_DONG = 18;`
- [x] BE: `BidPackage.php` thêm `const HUY_HOP_DONG = 17;`

## Phase 2 — Backend: logic

- [x] BE: `ContractService::cancelDownstream($contract)` — set quotation/project/bid_package (cái nào có) sang `HUY_HOP_DONG`
- [x] BE: `ContractController::approve()` — nhánh `result == KHONG_THUC_HIEN` → HĐ=HUY, gọi `cancelDownstream`, history "Hủy hợp đồng" + reason, notify; bỏ snapshot. Luồng cũ giữ nguyên
- [x] BE: `php -l` 6 file pass

## Phase 3 — Frontend: nhãn/màu/filter

- [x] FE Hợp đồng: `contract/contract/index.vue` (statuses + colorMap + getStatusText → id 5)
- [x] FE Hợp đồng: `contract/contract/approve.vue` + `components/GeneralComponent.vue` (badge id 5)
- [x] FE Báo giá: `bid_package/quotation/index.vue` (id 19)
- [x] FE Gói thầu: `bid_package/bid_package/index.vue` (id 17)
- [x] FE Dự toán: `plan/project/index.vue` (id 18)

## Phase 3b — Frontend: BỔ SUNG các màn danh sách khác (phát sinh khi test — mỗi module có map status riêng)

- [x] Báo giá (id 19): `plan/quotation/index.vue`, `plan/quotation/waiting-approve.vue`, `contractor/quotation/index.vue` (getStatusClass), `contract/quotation_render/index.vue`
- [x] Dự toán (id 18): `bid_package/project/index.vue`, `sale/project/index.vue`
- [x] Gói thầu (id 17): `bid_package/bid_package/waiting-approve-result.vue`, `contract/bid_package_render/index.vue`
## Phase 3c — Frontend: Báo cáo & Dashboard (user yêu cầu thêm)

- [x] FE `sale/report-project-contract/index.vue` (statusOptions+badgeClass DỰ TOÁN id18; getContractStatusName HĐ id5; getBidPackageStatusName GÓI THẦU id17)
- [x] FE `bid_package/detail-report/index.vue` (statusOptions GÓI THẦU id17 — text render từ server)
- [x] FE `sale/detail-report/index.vue` (statusOptions DỰ TOÁN id18 — text render từ server)
- [x] FE `components/dashboad/PlanDashboard.vue` (BÁO GIÁ id19 + colorMap)
- [x] FE `components/dashboad/BidPackageDashboard.vue` (GÓI THẦU id17 + colorMap)

## Phase 2b — Backend: $statusMap cho status_name báo cáo (phát sinh — detail-report lấy text từ server)

- [x] BE `QuotationController.php` — 3 chỗ `$statusMap` thêm `19 => 'Hủy hợp đồng'`
- [x] BE `ProjectController.php` — 3 chỗ thêm `18 => 'Hủy hợp đồng'`
- [x] BE `BidPackageController.php` — 2 chỗ thêm `17 => 'Hủy hợp đồng'`
- [x] BE `php -l` 3 file pass
- [x] `CategoryDashboardService` — gom trạng thái Hủy hợp đồng vào nhóm "Không thực hiện": Quotation::HUY_HOP_DONG + BidPackage::HUY_HOP_DONG; thêm Contract::HUY vào getAllContractStatusMapping. `php -l` pass. (Project không có hàm group trong service này)

## Phase 4 — Kiểm thử thủ công

- [ ] Tạo HĐ từ báo giá, result=2, gửi duyệt → TP bấm Duyệt → HĐ = "Hủy hợp đồng", báo giá = "Hủy hợp đồng"
- [ ] Tạo HĐ từ gói thầu, result=2, duyệt → gói thầu (+ dự toán nếu có) = "Hủy hợp đồng"
- [ ] Lịch sử duyệt HĐ hiển thị action "Hủy hợp đồng" + lý do
- [ ] HĐ result=1 duyệt bình thường → DA_DUYET + snapshot như cũ (không hồi quy)
- [ ] Badge/nhãn trạng thái mới hiển thị đúng màu trên 4 danh sách; filter lọc được

## Checkpoint

### Checkpoint — 2026-06-10
Vừa hoàn thành: brainstorming + spec + plan
Đang làm dở: chưa code
Bước tiếp theo: implement Phase 1 (const) → Phase 2 (logic) → Phase 3 (FE)
Blocked:

### Checkpoint — 2026-06-10 (code xong BE+FE)
Vừa hoàn thành: Phase 1-3. BE: 4 entity thêm const (Contract HUY=5/KHONG_THUC_HIEN=2, Quotation/Project/BidPackage HUY_HOP_DONG=19/18/17), `ContractService::cancelDownstream`, `approve()` rẽ nhánh result=2 → hủy + history + reason. FE: 7 file thêm nhãn/màu(rose)/filter trạng thái "Hủy hợp đồng". php -l pass 6 file BE
Đang làm dở: không
Bước tiếp theo: user kiểm thử thủ công Phase 4 (duyệt HĐ result=2 từ báo giá/gói thầu → kiểm trạng thái HĐ + nguồn + lịch sử; HĐ result=1 không hồi quy)
Blocked: không
