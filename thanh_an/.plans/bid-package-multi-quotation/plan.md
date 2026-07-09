# Plan — Gói thầu gộp nhiều báo giá

> Phụ trách: @khoipv · 2026-07-07 · Đánh giá lại: 2026-07-08 · Code: 2026-07-08
> Design: `.plans/bid-package-multi-quotation/design.md`
> Spec: `docs/superpowers/specs/2026-07-07-bid-package-multi-quotation-design.md`
> Trạng thái: **ĐÃ CODE XONG BE + FE (Phase 0-5)** — còn Phase 6 verify UI.

---

## Phase 0 — Chốt quyết định treo ✅ (chốt đủ 8/8 — 2026-07-08)
- [x] Mặt hàng trùng giữa báo giá → **APPEND tách nhóm** nguyên trạng theo từng báo giá, badge mã BG trên header nhóm, cảnh báo mềm khi trùng, KHÔNG cộng dồn SL (spec mục 5b)
- [x] `price_type_min/max_id` khác nhau giữa các BG → **để TRỐNG + cảnh báo**, KHÔNG chặn gộp (spec mục 5b)
- [x] Bỏ bớt báo giá đã chọn → chỉ cho phép khi TẠO MỚI (`!isShow && !isEdit`, giống icon "+" cũ) → gỡ trọn nhóm theo `group.quotation_id`, KHÔNG cần revert BE (status chỉ đổi khi lưu). Xóa gói thầu mới revert (đã vá).
- [x] Chặn khác KH → chặn cứng ngay trong modal (row khác KH bị disable + toast) + validate BE `withValidator`
- [x] Backfill bảng nối cho dữ liệu cũ → **CÓ** (81/81 dòng khớp; mọi query chỉ join bảng nối 1 kiểu)
- [x] Phạm vi gộp chỉ `bid_type == 1`; nhảy thầu giữ nguyên đơn (fallback cột đơn khi bảng nối trống)
- [x] `ContractAssignEmployee.quotation_id` khi gộp → **NULL** (lịch sử phân công gói thầu query theo `bid_package_id` — `ContractService:773`; `quotation-history` yêu cầu `whereNull(bid_package_id)` nên không mất gì)
- [x] Phạm vi nhóm 🟠 → **sửa hết 1 đợt** (đã sửa toàn bộ)

## Phase 1 — DB & Entity (BE) ✅
- [x] Migration `2026_07_08_100000_create_bid_package_quotations_table` — tạo bảng nối + backfill (ĐÃ CHẠY, 81/81)
- [x] Migration `2026_07_08_110000_add_quotation_id_to_bid_package_groups_and_products` — cột truy nguồn mức nhóm + dòng hàng + backfill (ĐÃ CHẠY; lưu ý: cột `bid_package_products.quotation_id` trước đây KHÔNG tồn tại dù entity có relation — dead code)
- [x] Entity `BidPackageQuotation` (bid_package/quotation/project) + `BidPackage::quotations()` + fillable `quotation_id` cho `BidPackageGroup`/`BidPackageProduct`

## Phase 2 — Vòng đời gói thầu (BE) ✅ — 6 điểm trạng thái
- [x] `StoreBidPackageRequest`: `prepareForValidation` gói `quotation_id` đơn → `quotation_ids[]`; rule required theo bid_type; `project_id` nullable khi gộp >1; `withValidator` chặn khác KH (chỉ enforce khi >1 để không ảnh hưởng luồng cũ)
- [x] `BidPackageService::syncQuotations()` (MỚI): ghi bảng nối cho mọi gói có báo giá; >1 → cột đơn NULL, =1 → giữ cột đơn; gọi trong `store()` + `update()`
- [x] `BidPackageService::sourceQuotations()` (MỚI): helper lấy N báo giá qua bảng nối, fallback cột đơn
- [x] `updateStatus()`: lặp N báo giá (7→11 tạo, 7/11→8 giao NV) + N dự toán (→11); nhánh nhảy thầu giữ nguyên
- [x] `assignEmployeeCreateContract()`: `ContractAssignEmployee.quotation_id` tự NULL khi gộp (copy cột đơn); set contract_manager/received_time/group cho N báo giá
- [x] `BidPackageController::render()` kết xuất: lặp N dự toán → `DA_CHUYEN_HOP_DONG`, N báo giá → `GOI_THAU_DA_KET_XUAT` (fallback cột đơn khi bảng nối trống)
- [x] `render()` hủy/trượt (`result==2`): lặp N → `GOI_THAU_DA_BI_HUY`
- [x] `delete()`: revert N báo giá 11/8→7 + dự toán 11→10 (`BAO_GIA_DA_GUI_THAU`), chỉ revert đúng trạng thái do gói gây ra; xóa bản ghi bảng nối (vá lỗ hổng cũ)
- [x] Confirm `StoreContractRequest` KHÔNG có rule `quotation_id` → HĐ nhận null OK, không sửa

## Phase 3 — Resource / related-data (BE) ✅
- [x] `BidPackageResource`: thêm `quotations[]` (id/code/project) + `quotation_codes` (chuỗi); giữ field cũ
- [x] `DetailBidPackageResource`: `quotation_products` = UNION N báo giá; thêm `quotation_ids` + `quotations[]` (prefill edit); nhóm trả `quotation_id`/`quotation_code` (badge)
- [x] Related-data gói thầu (`BidPackageController:1102`): liệt kê N dự toán + N báo giá qua bảng nối, fallback cột đơn
- [x] Related-data báo giá (`QuotationController`) + dự toán (`ProjectController`): thấy gói thầu gộp qua bảng nối (orWhereIn)

## Phase 4 — Báo cáo & hiển thị phụ (BE) ✅
- [x] `saleProductReport` theo HĐ: fallback resolve báo giá theo DÒNG HÀNG (`bid_package_products.quotation_id`) → thiếu thì báo giá duy nhất trong bảng nối
- [x] `saleProductReport` theo dự toán: `bidPackageIds` union bảng nối + lọc dòng hàng theo báo giá của dự toán (null = hành vi cũ)
- [x] `saleProductBidPackages` (popup): union bảng nối cho cả `quotation_id`/`project_id`
- [x] `detailReport`: `first_bp` join qua `bid_package_quotations`
- [x] `lifecycleReport`: `gt_agg` = link (bảng nối UNION cột đơn) + phân bổ giá trị theo dòng hàng (không double-count gói gộp nhiều dự toán); SQL đã smoke test
- [x] `report-project-contract` + `summaryReportStats` + `bidContractProductMap` (QuotationController): resolve qua bảng nối; HĐ từ gói gộp tính cho TẤT CẢ báo giá nguồn
- [x] Dashboard `CategoryDashboardService`: 3 chỗ nhóm BidPackage `whereHas('project')` → thêm `orWhereHas('quotations.project')` (nhóm Quotation/Contract không ảnh hưởng — dùng project_id của chính nó)
- [x] Filter `BidPackageService` (index/canCreateContract/getDataForModal): lọc quotation_id/project_id qua cột đơn HOẶC bảng nối
- [x] Reverse resource `QuotationResource` + `ProjectResource`: tên NV lập thầu qua bảng nối

## Phase 5 — FE form gói thầu ✅
- [x] `QuotationModal.vue`: multi-select (checkbox + click row), chặn cứng khác KH (disable + toast), props `exclude-ids`/`locked-customer-id`, nút "Xong (n)" emit `choose-quotations` (mảng detail)
- [x] `GeneralComponent.vue`: ô Báo giá → chips N mã (link chi tiết + nút x khi tạo mới); ô Dự toán hiển thị N mã qua `projectCodeDisplay`; icon "+" KH theo `hasSourceQuotations`
- [x] `addQuotations`/`appendQuotation`: APPEND groups theo từng báo giá (gắn `quotation_id/code` vào nhóm + dòng hàng); rule field header (KH = BG đầu, project null khi >1, union array_product_id + productIds, concat supplier_auths, price_type khác → trống + cảnh báo); clone mảng tránh mutate defaultForm
- [x] `warnDuplicateProducts`: cảnh báo mềm mặt hàng trùng giữa các BG
- [x] `removeQuotation`: gỡ trọn nhóm theo BG; còn 1 BG → quay về dạng đơn
- [x] `updatePrice` guard + `hasErrorInGeneralTab` thêm `quotation_ids`
- [x] `add.vue`/`edit.vue`/`_id/index.vue`: validate union (`hasSourceQuotation`); payload spread tự gửi `quotation_ids[]`
- [x] `ProductComponent.vue`: badge mã BG trên header nhóm
- [x] Danh sách `index.vue`: cột mã báo giá + mã dự toán hiển thị N dòng (từ `item.quotations`)

## Phase 6 — Kiểm thử
**Đã PASS (verify UI Playwright + DB 2026-07-08, dùng BG-36 + BG-37 cùng KH 1803, khác dự toán DT-31/DT-30):**
- [x] Modal multi-select: tích 2 BG, "Xong (n)", chặn cứng khác KH (BG-39 bị disable + toast "Chỉ được gộp các báo giá cùng một khách hàng") — *fix kèm: `QuotationResource` thiếu `customer_id` → đã thêm*
- [x] Form gộp: chips 2 mã link chi tiết; KH auto-fill từ BG đầu; "Mã dự toán" hiện "DT-003/2026, DT-002/2026"; 4 nhóm append đúng nguồn + badge mã BG; 70 dòng hàng; union productIds = 69 (1 mặt hàng trùng 2 BG → giữ 2 dòng riêng); price_type giống nhau → giữ nguyên
- [x] Lưu (status 1 — GT-354): `quotation_id/project_id` NULL, bảng nối 2 dòng đúng, **cả 2 BG 7→11**, DT giữ 10; nhóm/dòng hàng lưu đủ `quotation_id` truy nguồn (5 dòng bg36 + 65 dòng bg37)
- [x] Danh sách: cột Mã báo giá + Mã dự toán hiện 2 mã × link đúng; chi tiết: chips + badge + mã dự toán ghép
- [x] Related-data 3 chiều: BG-36 thấy GT-354; DT-31 thấy GT-354; GT-354 thấy đủ 2 DT + 2 BG
- [x] Xóa gói (status 1): **revert cả 2 BG 11→7**, bảng nối dọn sạch (vá lỗ hổng cũ OK)
- [x] Lưu và gửi (status 2 — GT-355): **cả 2 BG →8, cả 2 DT →11**; xóa → **BG 8→7, DT 11→10** — trọn nhánh giao NV + revert
- [x] Không hồi quy: danh sách gói cũ 1 báo giá hiển thị bình thường (mã BG qua backfill), gói nhảy thầu cột trống như cũ
- [x] Dọn test data: GT-354/GT-355 đã xóa, BG-36/37 + DT-30/31 về nguyên trạng

**Bổ sung khi user tự test (2026-07-08 chiều, GT-356 gộp BG-332+BG-333):**
- [x] **Kết xuất thầu gói gộp PASS**: cả 2 BG → 18 (GOI_THAU_DA_KET_XUAT), cả 2 DT → 12 (DA_CHUYEN_HOP_DONG)
- [x] Fix màn `contract/bid_package_render` + `bid_package/waiting-approve-result`: cột "Dự toán" trống với gói gộp → hiển thị N mã từ `item.quotations` (mỗi mã 1 dòng, link đúng) — verify UI PASS trên GT-356

**Bổ sung nhánh HĐ từ gói gộp (2026-07-08 tối, user tạo HD-187/2026 từ GT-356 — project_id/quotation_id NULL đúng thiết kế):**
- [x] `ContractResource`: thêm `projects[]` + `quotations[]` resolve qua bảng nối khi `project_id` null && có `bid_package_id` (chỉ query khi cần — HĐ thường không tốn thêm query)
- [x] Màn `contract/contract` (danh sách HĐ): cột "Mã dự toán" hiện N mã × link — verify UI PASS (HD-187 → DT-242/2026 + DT-241/2026)
- [x] `saleProductReport` nhánh HĐ: INNER JOIN projects → **leftJoin** + KH `COALESCE(p.customer_id, c.customer_id)` (cả filter) + guard `(c.project_id NOT NULL OR c.bid_package_id NOT NULL)` để HĐ không dự toán/không gói thầu vẫn bị loại như hành vi cũ; mở rộng bước 1b: resolve **dự toán theo dòng hàng** (BG→DT qua bảng nối). Verify API PASS: 5 dòng HD-187 hiện đúng, hàng BG-332→DT-241, hàng BG-333→DT-242, khớp bg_qty/gt_qty từng dòng

**UX modal chọn báo giá (2026-07-08 tối, theo yêu cầu user):**
- [x] Tích BG đầu tiên → modal **tự lọc server-side** theo KH đó (thay vì hiện hết + disable); bỏ tích hết → trả lại danh sách đầy đủ. FE: watch `effectiveCustomerId` + gửi `customer_id` trong `getData` (QuotationModal.vue). BE: bật lại filter `customer_id` trong `QuotationService` (đang bị comment — 4 màn danh sách BG có ô lọc KH gửi field này nhưng BE bỏ qua, coi như fix kèm ô lọc chết). Giữ disable/toast làm safety net. Verify UI PASS: 73 BG → tích BG-334 → còn 1 BG đúng KH → bỏ tích → về 73

**Merge nhánh (2026-07-09):**
- [x] Resolve conflict `GeneralComponent.vue` khi merge `thanhan-dev` vào `tao-goi-thau`: giữ cấu trúc multi-báo-giá (`addQuotations`/`appendQuotation`) của HEAD + tích hợp logic multi-KH-sử-dụng-cuối của thanhan-dev → helper mới `mergeCustomerLastUsed(data)` gọi ở cả nhánh isFirst (reset rồi nạp) lẫn nhánh append (hợp nhất không trùng, dedupe theo id). Đã `git add`, **chưa commit** (user tự commit)

**Còn lại (chưa E2E / chưa sửa):**
- [ ] Màn `contract/negotiation_minutes` (index + approve): hiển thị `project_code_name` → trống với HĐ/BBTT từ gói gộp (kiểm resource màn này rồi xử lý tương tự ContractResource)
- [ ] Chi tiết HĐ (DetailContractResource) — kiểm hiển thị mã dự toán/báo giá với HĐ gộp
- [ ] Phân công lập HĐ cho gói gộp (`assignEmployeeCreateContract`) — user có thể đã chạy khi tạo HD-187, chưa verify contract_manager trên 2 BG
- [ ] Hủy/trượt thầu gói gộp (render result=2 — N báo giá/dự toán → GOI_THAU_DA_BI_HUY)
- [ ] Các report còn lại với gói gộp: detailReport, lifecycleReport, report-project-contract, dashboard, filter danh sách
- [ ] Sửa (edit) gói gộp đang tạo: prefill chips từ `quotation_ids`, lưu lại không drift bảng nối

---

### Checkpoint — 2026-07-08 (tối)
Vừa hoàn thành: Nhánh HĐ từ gói gộp — HD-187/2026 (từ GT-356): fix danh sách HĐ hiện N mã dự toán (ContractResource + contract/contract); fix saleProductReport không rớt HĐ gộp (leftJoin + guard giữ hành vi cũ + resolve dự toán theo dòng hàng) — verify UI + API PASS. Trước đó cùng ngày: fix 2 màn bid_package_render/waiting-approve-result; verify kết xuất gộp PASS.
Đang làm dở: Phase 6 phần còn lại (negotiation_minutes, chi tiết HĐ, hủy/trượt, report còn lại, edit gói gộp).
Bước tiếp theo: Kiểm màn BB thương thảo + chi tiết HĐ với HD-187; verify contract_manager 2 BG nguồn của GT-356; sau đó report còn lại.
Blocked:
