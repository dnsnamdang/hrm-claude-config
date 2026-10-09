# Hiển thị thông tin đồng bộ ERP trong box "Lập hợp đồng ERP từ báo giá"

> Module Assign (HRM). Branch: `sync_quotation` (cả hrm-api, hrm-client, ERP TanPhatDev).
> Màn: Dự án tiềm năng → tab Báo giá → box "Lập hợp đồng ERP từ báo giá".

## Yêu cầu (theo ảnh spec)
Thêm 3 thông tin: **Mã hợp đồng ERP**, **Trạng thái đồng bộ** (mặc định "Chưa đồng bộ"), **Thời gian đồng bộ**.
Chốt với user: (B) Mã HĐ ERP = **mã code dạng chữ** (cần ERP gửi sang); hiển thị **trong BOX** (không thêm vào bảng 11 cột).

## Mapping dữ liệu
- Mã hợp đồng ERP = `quotations.erp_firm_contract_code` (MỚI) — ERP gửi khi lập HĐ. Link mở HĐ ERP theo `erp_firm_contract_id`.
- Trạng thái đồng bộ = `quotations.erp_sync_status` (null→"Chưa đồng bộ", success→"Đã đồng bộ", failed→"Đồng bộ lỗi") — set bởi `QuotationErpSyncService` (đẩy báo giá sang ERP firm-quotation).
- Thời gian đồng bộ = `quotations.erp_synced_at`.

## Thay đổi
### ERP (TanPhatDev)
- [x] `HrmApiService::markContractCreated($id, $erpContractId, $erpContractCode=null)` — gửi thêm `erp_firm_contract_code`.
- [x] `FirmContractService.php:567` — truyền `$contract->code`.

### HRM API
- [x] Migration `2026_07_23_000001_add_erp_firm_contract_code_to_quotations_table` — thêm cột `erp_firm_contract_code` (nullable, after erp_firm_contract_id).
- [x] `QuotationController::erpMarkContract` — lưu `erp_firm_contract_code` từ request.
- [x] `QuotationController::buildContractSummary` — trả `erp_firm_contract_code`, `erp_firm_contract_url`, `erp_sync_status`, `erp_sync_status_name`, `erp_synced_at`.

### HRM Client
- [x] `ProspectiveProjectQuotationsTab.vue` — box "Lập hợp đồng ERP" thêm block 3 mục (Mã HĐ ERP link + badge trạng thái + thời gian). Mặc định "—"/"Chưa đồng bộ".

## Verify
- [x] php -l sạch (4 file). Migration valid. Template .vue parse errors: NONE.
- [ ] **User chạy migration HRM**: `php artisan migrate` (hrm-api) — thêm cột erp_firm_contract_code.
- [ ] E2E: đồng bộ báo giá → box hiện "Đã đồng bộ" + thời gian; lập HĐ ERP → callback lưu code → box hiện Mã HĐ ERP (link).
- [ ] Commit (chờ user) — cả 3 repo trên branch sync_quotation.

### Checkpoint — 2026-07-23
Vừa hoàn thành: BE HRM+ERP + FE box. Chờ user chạy migration + test + commit.

---

## Đính chính (2026-07-23) — HĐ từ báo giá HRM là HĐ DỰ ÁN
"Hợp đồng dự án" KHÔNG phải bảng riêng — vẫn là `firm_contracts` nhưng `contract_type = 4` (ERP `FirmContract::HOP_DONG_DU_AN`). Vì vậy:
- Code `markContractCreated`/`erp_firm_contract_id` ở `FirmContractService` là ĐÚNG chỗ (xử lý mọi firm_contracts gồm type 4) — không revert.
- Deep-link cũ mở `firm-contracts/create?hrm_quotation_id=` KHÔNG truyền contract_type → ERP mặc định `HOP_DONG=1` (hãng). SAI.
- [x] Fix: thêm `&contract_type=4` vào `erp_contract_url` (buildContractSummary) → mở đúng màn tạo HĐ DỰ ÁN. Commit hrm-api eaa06fe2e.

---

## Bổ sung (2026-07-23) — Ẩn nút "Lập hợp đồng ERP" với báo giá có cấp con
Báo giá có dòng cấp con (`quotation_product_prices.parent_id != null`) CHƯA hỗ trợ lập HĐ ERP → ẩn nút.
- [x] BE `buildContractSummary`: thêm `$hasChildren` (whereNotNull parent_id exists); `$canCreate = ... && !$hasChildren`; trả thêm `has_children`.
- [x] FE box: thêm badge "Báo giá có cấp con — chưa hỗ trợ lập HĐ" (v-else-if has_children) → nút ẩn (v-if can_create_contract=false).
- [x] Verify tinker: BG-41/44 (có con, đồng bộ hết) → nút ẨN (trước HIỆN). php -l + template OK.
- [ ] Commit (chờ user).

---

## Bổ sung (2026-07-23) — Badge box khác nhau giữa các tài khoản (misleading)
Người KHÔNG phải người lập báo giá thấy badge "Chờ đồng bộ hết hàng sang ERP" dù báo giá ĐÃ đồng bộ hết — do nhánh else gộp chung "chưa đồng bộ" và "không phải người lập" (can_create_contract phụ thuộc isCreator).
- [x] BE: trả thêm `is_synced` (= remaining===0, độc lập người xem).
- [x] FE: tách badge — thứ tự: Đã lập → ngoại tệ → cấp con → `!is_synced` "Chờ đồng bộ" → can_create "Sẵn sàng"+nút → else "Đã đồng bộ — chỉ người lập báo giá mới lập được HĐ".
- Kết quả: người lập thấy "Sẵn sàng lập hợp đồng" + nút; người khác (đã đồng bộ) thấy "Đã đồng bộ — chỉ người lập mới lập HĐ" (không còn hiểu nhầm "chờ đồng bộ").
- [x] php -l + template OK. [ ] Commit (chờ user).
