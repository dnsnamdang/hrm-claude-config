# Kết xuất hợp đồng sang cung ứng — Plan

- Phụ trách: @khoipv · Bắt đầu 2026-08-26
- **Design tóm tắt:** `.plans/contract-render-supply/design.md`
- **Spec đầy đủ:** `docs/superpowers/specs/2026-08-26-contract-render-supply-design.md`
- **Plan chi tiết (code từng bước):** `docs/superpowers/plans/2026-08-26-contract-render-supply.md`

---

## Phase 1 — CSDL

- [x] Migration `contracts`: `supply_rendered_at`, `supply_rendered_by` (+ index, không FK)
- [x] Migration `supply_proposals`: `contract_id` (+ index, không FK)
- [x] `Contract::$fillable` + `Contract::canRenderSupply()`
- [x] Chạy `php artisan migrate` + kiểm chứng schema bằng tinker

## Phase 2 — BE Modules/Category (endpoint kết xuất)

- [x] `Http/Requests/RenderSupplyContractRequest.php` — validate `result = 1` + điều khoản TT khối main (+ kpi nếu `has_kpi`)
- [x] `ContractService::renderSupply()` — guard → lưu kết quả → `updatePaymentTermsAfterApprove()` → đóng dấu kết xuất
- [x] `ContractController::renderSupply()` — `DB::transaction` + catch → 400
- [x] Route `PUT /category/contracts/{contract}/render-supply`
- [x] `ContractResource`: `can_render_supply`, `supply_rendered_at`
- [x] Kiểm chứng: `php -l`, `route:list --path=render-supply`, tinker guard

## Phase 3 — BE Modules/Supply (danh sách + prefill)

- [x] Tách `SupplyProposalService::importTypeFallbackMap()` + `contractProductRows()` từ `goodsPool()`
- [x] `goodsPool()` dùng lại 2 hàm vừa tách — so sánh output before/after phải giống hệt
- [x] `SupplyProposalService::assertContractAvailable()` — 1 HĐ ↔ 1 phiếu còn sống
- [x] `RenderedContractService` (`getList`, `prefill`)
- [x] `RenderedContractResource`
- [x] `RenderedContractController` (`index`, `prefill`)
- [x] Routes `/supply/rendered-contracts` (chưa gắn quyền)
- [x] Kiểm chứng: `php -l`, `route:list --path=rendered-contracts`, tinker `getList()`

## Phase 4 — BE Supply (phiếu đề xuất nhận nguồn HĐ)

- [x] `StoreSupplyProposalRequest`: rule `contract_id`
- [x] `SupplyProposalService::store()` / `update()`: lưu `contract_id` + gọi guard
- [x] `DetailSupplyProposalResource`: trả `contract_id`, `contract_code`
- [x] Kiểm chứng: `php -l` + tinker guard

## Phase 5 — FE (điểm vào)

- [x] `utils/MenuSupply.js`: mục "Hợp đồng đã kết xuất" trước "Phiếu đề xuất cung ứng"
- [x] `pages/contract/contract/index.vue`: nút "Kết xuất sang cung ứng" (`v-if="item.can_render_supply"`)

## Phase 6 — FE màn kết xuất

- [x] `GeneralComponent.vue` (HĐ): **THÊM** prop `isRender` (default `false`) + computed `canEditPayment` — ⚠️ component dùng chung, chỉ thêm, không đổi hành vi cũ
- [x] Mở sửa Kết quả / Lý do / Điều khoản TT khi `isRender`
- [x] `pages/contract/contract/_id/render.vue` mới
- [x] Kiểm chứng UI bằng Playwright: validate 422 (result + payment_terms), kết xuất thành công, hồi quy add/edit/xem

## Phase 7 — FE màn "Hợp đồng đã kết xuất"

- [x] `pages/supply/contract_render/constants.js`
- [x] `pages/supply/contract_render/index.vue` (bộ lọc + bảng + 2 nút thao tác)
- [x] Kiểm chứng UI bằng Playwright: lọc theo từ khóa, đặt lại bộ lọc, 2 nút điều hướng

## Phase 8 — FE prefill phiếu đề xuất

- [x] `supply_proposals/add.vue`: đọc `?contract_id=`, gọi API prefill, khóa Loại + Khách hàng, hiện HĐ nguồn
- [x] `buildPayload()` + `loadDetail()` mang theo `contract_id`
- [x] Kiểm chứng UI bằng Playwright: prefill đủ hàng, lưu → HĐ ẩn, xóa phiếu → HĐ hiện lại, lập phiếu tay không đổi

## Phase 9 — Kiểm chứng đầu-cuối

- [x] Chạy trọn kịch bản kết xuất → lập phiếu → xóa phiếu → hiện lại
- [x] Kiểm tra `storage/logs/laravel-<ngày>.log` sạch
- [x] Hồi quy các màn dùng chung (compile `vue-template-compiler` OK cho 5 file .vue)
- [x] Kiểm chứng UI đầu-cuối bằng Playwright trên trình duyệt thật (xem Checkpoint 2)

---

## Checkpoint

### Checkpoint — 2026-08-26
Vừa hoàn thành: Toàn bộ Phase 1–9 (BE Category + BE Supply + FE menu/nút/màn kết xuất/màn "HĐ đã kết xuất"/prefill phiếu đề xuất).
Kiểm chứng đã chạy:
- Kịch bản đầu-cuối bằng script bootstrap Laravel, bọc `DB::beginTransaction()` / `rollBack()` — 11/11 bước đúng kỳ vọng: kết xuất → HĐ vào danh sách → prefill 4 dòng hàng → tạo phiếu → HĐ biến mất + prefill bị chặn → xóa phiếu → HĐ hiện lại → kết xuất lại bị chặn → rollback sạch DB.
- `RenderedContractResource` + `ContractResource` render đúng trường (`can_render_supply`, `supply_rendered_at`, `total_amount`, `sum_product_qty`).
- `storage/logs/laravel.log` không có lỗi ứng dụng (chỉ lỗi của script test trong scratchpad).
- FE: 5 file .vue compile sạch bằng `vue-template-compiler`.
  *(Đính chính: câu "3 route mới trả 200 trên dev server" ghi ở lần wrap up trước là SAI — lệnh curl khi đó trỏ nhầm cổng 3000 của project khác. Kiểm chứng UI thật nằm ở Checkpoint 2 bên dưới.)*
Đang làm dở: không.
Bước tiếp theo: @khoipv đăng nhập kiểm chứng UI thủ công 3 màn (kết xuất → danh sách → lập phiếu), sau đó bổ sung phân quyền cho `/supply/rendered-contracts` khi có yêu cầu.
Blocked: 
Lưu ý: đã **thêm** (không sửa hành vi cũ) vào component dùng chung `pages/contract/contract/components/GeneralComponent.vue` — prop `isRender` (default `false`), computed `canEditPayment`, và 3 khối `base-helper-error` cho lỗi điều khoản thanh toán. Cần @khoipv xác nhận.

### Checkpoint 2 — 2026-08-26 (kiểm thử Playwright trên trình duyệt thật)
Vừa hoàn thành: chạy trọn bộ kiểm thử UI đầu-cuối bằng Playwright (chế độ có hiển thị trình duyệt, Chromium, Node 24 riêng), đăng nhập tài khoản thật trên `localhost:3001`.

**Kết quả: 43 pass / 0 fail** (sau khi sửa 1 lỗi BE và 3 lỗi của chính script test)

| Bộ | Phạm vi | Kết quả |
|---|---|---|
| A+B+C (HĐ 216, `don`) | mở màn kết xuất, các field mở khóa, validate 422 | 13/13 |
| B+C (HĐ 214, `dot`) | màn kết xuất với hình thức "theo đợt" | 13/13 |
| B+C (HĐ 206, `don`, chưa tick điều khoản) | 422 trả **cả 2** lỗi `result` + `payment_terms` | 15/15 |
| D–F (HĐ 216) | kết xuất thành công → danh sách "HĐ đã kết xuất" → bộ lọc → prefill phiếu | 17/17 |
| G–I | tạo phiếu → HĐ ẩn → xóa phiếu → HĐ hiện lại → hồi quy | 13/13 |
| Guard (curl, không ghi dữ liệu) | tick hết = tắt → 422; `dot` không có đợt → 422; `result=2` → 422; kết xuất lại → 400; prefill HĐ chưa kết xuất → 400 | 5/5 |

**Lỗi thật đã phát hiện & sửa:** `Modules/Category/Http/Requests/RenderSupplyContractRequest.php` — `assertBlockHasTerms()` đếm số dòng theo `block`, trong khi FE **luôn** gửi đủ 4 loại điều khoản kèm cờ `enabled`, nên rule "bắt buộc có điều khoản thanh toán" **không bao giờ kích hoạt**. Đã sửa: hình thức `don` đếm theo `enabled`, hình thức `dot` đếm số đợt trong `payment_installments`.

**Không phải lỗi sản phẩm (đã xác minh):**
- API treo khi chạy song song → do `php artisan serve` đơn luồng, không phải lỗi tính năng.
- `POST /supply/supply-proposals` trả 403 với tk `nguyenthuhang92.tb@gmail.com` → tài khoản thiếu quyền "Lập phiếu đề xuất cung ứng" (quyền id 513 gắn role 3 và 18); đã kiểm bằng token của nhân viên có quyền.
- `Cannot read properties of undefined (reading 'setReadOnly')` (CKEditor) — lỗi có sẵn của màn HĐ, không do tính năng này.

**Dữ liệu:** đã snapshot trước khi test và **khôi phục nguyên trạng** sau khi test (contracts / payment_terms / installments / supply_proposals đều khớp snapshot).

Đang làm dở: không.
Bước tiếp theo: @khoipv xác nhận 2 điểm còn treo (mục "Cần xác nhận" bên dưới), sau đó bổ sung phân quyền cho `/supply/rendered-contracts` khi có yêu cầu.
Blocked: 

## Cần @khoipv xác nhận
1. **Sửa component dùng chung** `pages/contract/contract/components/GeneralComponent.vue` — chỉ **thêm** prop `isRender` (default `false`), computed `canEditPayment` và 3 khối `base-helper-error`; không đổi hành vi màn cũ (đã kiểm chứng: màn chi tiết HĐ thường vẫn khóa "Kết quả").
2. **Nút "Tạo phiếu đề xuất cung ứng"** ở màn "HĐ đã kết xuất" hiện ra với **mọi** user (do đang tạm không gắn quyền), nhưng API `POST /supply/supply-proposals` vẫn chặn 403 nếu thiếu quyền → user thiếu quyền bấm vào sẽ gặp lỗi 403 ở bước lưu. Có cần ẩn nút theo quyền "Lập phiếu đề xuất cung ứng" ngay bây giờ không?
3. Có cần thêm `<Required />` (sao đỏ) vào label "Kết quả" và "Điều khoản thanh toán" khi ở màn kết xuất không?

## Phase 10 — Ràng buộc "chỉ người lập HĐ mới được kết xuất" (@khoipv chốt 2026-08-26)

Trước đó `canRenderSupply()` chỉ kiểm `status=3` + `record_type=2` + chưa kết xuất → **bất kỳ ai cũng kết xuất được HĐ của người khác** (test đã chứng minh: employee 36 kết xuất HĐ 216 do employee 13 lập).

- [x] `Contract::canRenderSupply()` — thêm `created_by == optional(auth()->user())->id`
- [x] `ContractService::renderSupply()` — guard server: throw "Chỉ người lập hợp đồng mới được kết xuất sang cung ứng."
- [x] `ContractDetailResource` — bổ sung `can_render_supply` + `supply_rendered_at`
      *(phát hiện kèm: resource này KHÔNG trả `supply_rendered_at`, nên guard `if (data.supply_rendered_at)` trong `render.vue` là **code chết** — chưa bao giờ chạy)*
- [x] `pages/contract/contract/_id/render.vue` — chặn vào thẳng URL bằng `can_render_supply`, toast + `replace('/contract/contract')`
- [x] `php -l` 3 file BE + compile `vue-template-compiler` cho `render.vue`: sạch
- [x] Playwright (TK employee 36 — KHÔNG phải người lập): J1 danh sách **0** nút Kết xuất · J2 vào thẳng URL bị đẩy về · J3 đúng toast · J4 gọi thẳng API → **HTTP 400** · J5 đúng thông báo — **5/5 PASS**
- [ ] Kiểm chứng phía người lập (employee 13 vẫn thấy nút + vào được màn) — đã PASS ở lần chạy trước (K1: 4 nút, K2: vào được màn), lần chạy lại script lỗi exception chưa truy nguyên; **@khoipv tự test tiếp**

### Checkpoint 3 — 2026-08-26
Vừa hoàn thành: Phase 10 (ràng buộc người lập) + sửa code chết `supply_rendered_at` ở màn kết xuất.
Đang làm dở: không. Test tự động dừng theo yêu cầu @khoipv (anh tự test tiếp).
Dữ liệu: DB vẫn nguyên trạng theo snapshot (các thao tác Phase 10 đều bị chặn nên không ghi gì).
Bước tiếp theo: @khoipv test tay; sau đó chốt 3 điểm ở mục "Cần @khoipv xác nhận".
Blocked: 

## Phase 11 — Đồng bộ nút thao tác màn "HĐ đã kết xuất" (@khoipv yêu cầu 2026-08-26)

Nút "Tạo phiếu đề xuất cung ứng" phải giống nút "Lập hợp đồng" ở màn `contract/quotation_render` (Báo giá đã chuyển hợp đồng).

- [x] `pages/supply/contract_render/index.vue` — đổi thứ tự: **Xem** trước (không variant), **Tạo phiếu** sau (`variant="secondary"`)
- [x] Icon `plus.svg` → `contract.svg` (đúng icon nút Lập hợp đồng)
- [x] Điều hướng bằng `:to` thay cho `@click` + `$router.push` (khuôn của `quotation_render`)
- [x] Bỏ method `onCreateProposal()` không còn dùng (`onViewContract()` giữ lại cho link mã HĐ ở cột Mã)
- [x] Compile `vue-template-compiler`: sạch
- [ ] @khoipv tự kiểm chứng trên UI

## Phase 12 — Trạng thái HĐ "Đã kết xuất" (status = 9) (@khoipv chốt 2026-08-26)

**Bối cảnh:** HD-159/2026 đã kết xuất nhưng danh sách HĐ vẫn hiện "Đã duyệt". Dữ liệu đúng (`supply_rendered_at` đã ghi), nhưng thiết kế cũ **không có** trạng thái "Đã kết xuất". @khoipv chọn phương án **đổi hẳn `contracts.status`** (giống báo giá: `Quotation::CHUYEN_HOP_DONG = 9`).

**Nguyên tắc xuyên suốt:** HĐ status 9 **vẫn là HĐ đã duyệt** cho mọi nghiệp vụ downstream (nghiệm thu, thanh lý, phụ lục, đơn mua hàng, phiếu đề xuất cung ứng, giao việc) — chỉ khác nhãn hiển thị. Dùng helper mới `Contract::approvedStatuses()` thay vì hard-code `3` ở mọi nơi.

### BE
- [x] `Entities/Contract/Contract.php` — thêm `const DA_KET_XUAT = 9`; thêm `public static function approvedStatuses(): array { return [DA_DUYET, DA_KET_XUAT]; }`; `canAssign()` chấp nhận thêm `DA_KET_XUAT`
- [x] `Services/ContractService.php::renderSupply()` — set `status = DA_KET_XUAT` **sau** `updatePaymentTermsAfterApprove()` (đặt trước sẽ làm hàm này bỏ qua, mất điều khoản thanh toán)
- [x] `Services/ContractService.php::updatePaymentTermsAfterApprove()` — cho phép cả status 3 và 9 (`in_array(..., Contract::approvedStatuses(), true)`)
- [x] `Services/ContractService.php` (bộ lọc danh sách, ~dòng 117) — nhận `status=3,9` (nhiều trạng thái, phân tách bằng dấu phẩy)
- [x] `Services/AcceptanceReportService.php:295` — dropdown chọn HĐ dùng `whereIn(...approvedStatuses())`
- [x] `Services/ContractLiquidationService.php:351` — như trên
- [x] `Services/CategoryDashboardService.php` — thêm option "Đã kết xuất" vào mapping trạng thái (1444) + `whereIn` cho thống kê HĐ đã duyệt (1683)
- [x] `Http/Controllers/Api/V1/ContractController.php` — 2 `$statusMap` báo cáo: thêm `9 => 'Đã kết xuất'`
- [x] `Modules/Supply/Http/Controllers/Api/V1/PurchaseOrderController.php:340` — thêm nhãn `Contract::DA_KET_XUAT => 'Đã kết xuất'`
- [x] `Modules/Supply/Services/RenderedContractService.php:20` — danh sách "HĐ đã kết xuất" lọc theo `DA_KET_XUAT` (không còn là `3`)
- [x] `Modules/Supply/Services/SupplyProposalService.php` (2 chỗ) — `whereIn(...approvedStatuses())`
- [x] **Cố ý KHÔNG đổi:** `ContractController.php:567,602` + `NegotiationMinutesController.php:103` (duyệt HĐ set 3 — đúng); `ContractService.php:751` + `NegotiationMinuteService.php:152` (thông báo theo `$request->status` — đúng); guard trong `renderSupply()` vẫn chỉ cho `DA_DUYET` (không cho kết xuất lại)
- [x] Migration dữ liệu `Modules/Category/Database/Migrations/2026_08_26_000003_set_rendered_contracts_status.php` — chuyển HĐ đã có `supply_rendered_at` từ 3 → 9 (có `down()` để rollback). **Đã chạy** (271.71ms), cập nhật 1 dòng: HD-159/2026 (id 179)
- [x] `php -l` 11 file BE: sạch

### FE
- [x] `pages/contract/contract/index.vue` — option bộ lọc `{ id: 9, text: 'Đã kết xuất' }`; pill `pj-status-gold`; `getStatusText()` + `getStatusClass()` xử lý 9
- [x] `pages/contract/contract/approve.vue` — `getStatusText()` xử lý 9
- [x] `pages/contract/contract/_id/index.vue:18` — `canEditAfterApprove` nhận cả 3 và 9 (`[3, 9].includes(...)`), nếu không HĐ đã kết xuất sẽ mất quyền sửa sau duyệt
- [x] 8 dropdown chọn HĐ ở phụ lục / phụ lục giảm giá — `&status=3` → `&status=3,9`: `contract_annex_information`, `contract_annex_payment_terms`, `contract_annex_price`, `contract_annex_product_name`, `contract_annex_quantity`, `contract_annex_time`, `contract_annex_vat`, `discount_appendix`
- [x] `pages/contract/detail-report/index.vue` — thêm option lọc "Đã kết xuất"
- [x] `pages/contract/reports/sale-product/index.vue` — `contractStatusText()` thêm `9: 'Đã kết xuất'`
- [x] Quét lại toàn bộ FE: các map trạng thái còn lại là của **phụ lục / nghiệm thu / thanh lý / giao NV / báo giá / gói thầu** (status riêng), không phải trạng thái HĐ → không đổi
- [x] Compile `vue-template-compiler` + `@babel/parser` cho 15 file FE đã sửa: sạch

### Đã kiểm chứng dữ liệu
```
HD-159/2026 (id 179): status=9, supply_rendered_at=2026-08-26 14:14:05, by=36, created_by=36
Phân bố: status 1: 7 | 2: 6 | 3: 192 | 5: 1 | 9: 1
```

### Checkpoint 4 — 2026-08-26
Vừa hoàn thành: Phase 12 — trạng thái "Đã kết xuất" (status 9) toàn tuyến BE + FE + migration dữ liệu.
Đang làm dở: không.
Bước tiếp theo: @khoipv test tay (hard refresh trình duyệt để nạp lại bundle FE). Sau đó chốt 3 điểm ở mục "Cần @khoipv xác nhận".
Blocked: 

**Lưu ý còn tồn (không thuộc phạm vi phase này):** 2 `$statusMap` báo cáo trong `ContractController.php` vẫn thiếu `5 => 'Hủy hợp đồng'` (lỗi có sẵn — HĐ hủy hiện trạng thái rỗng ở báo cáo). Cần @khoipv quyết có bổ sung không.

### Phase 12b — Rà soát toàn hệ thống "HĐ đã duyệt" (@khoipv yêu cầu 2026-08-26)

Quét lại **toàn bộ** BE + FE tìm mọi chỗ đang hiểu "HĐ đã duyệt = status 3" để bổ sung status 9.

**Phát hiện thêm & đã sửa:**
- [x] `ContractController::summaryReportStats()` (~dòng 1136) — KPI "% Đã duyệt" của Báo cáo tổng hợp HĐ đếm `$contracts->where('status', 3)` → HĐ đã kết xuất bị loại khỏi số lượng **và** giá trị đã duyệt. Đổi sang `whereIn('status', Contract::approvedStatuses())`
- [x] `pages/contract/detail-report/index.vue` — thêm option lọc "Đã kết xuất"
- [x] `pages/contract/reports/sale-product/index.vue` — `contractStatusText()` thêm `9: 'Đã kết xuất'`

**Đã rà và xác nhận KHÔNG cần sửa (nêu rõ lý do):**

| Nơi | Lý do |
|---|---|
| `ContractController.php:567,602`, `NegotiationMinutesController.php:103` | Hành động **duyệt** HĐ → phải set 3 |
| `ContractService.php:756`, `NegotiationMinuteService.php:152` | So `$request->status` (trạng thái gửi lên khi duyệt), không phải trạng thái hiện tại |
| `ContractService.php:1102` (guard `renderSupply`) | Cố ý chỉ cho `DA_DUYET` → chặn kết xuất lại |
| `Contract::canEdit/canDelete/canApprove` | Điều kiện là `DANG_TAO` / `KHONG_DUYET` / `CHO_DUYET` — không liên quan |
| `Contract::canCreateContract()` (dòng 334) | Áp cho **BB thương thảo** (`record_type = 1`) — loại này không kết xuất được nên không bao giờ có status 9 |
| `ContractService::cancelDownstream/updateStatus` | Chỉ xử lý `CHO_DUYET` / `DANG_TAO`, hành vi với status 9 giống hệt status 3 |
| `ProjectController.php:1117` | Dùng `where('c.status', '<>', Contract::HUY)` → đã bao gồm 9 |
| `CategoryDashboardService` pie/column chart (704, 1302) | Lặp theo `getAllContractStatusMapping()` — đã có mục "Đã kết xuất" nên tự hiện thêm lát cắt |
| `render.vue:90` (`data.status != 3`) | Cố ý: HĐ status 9 **không** được vào lại màn kết xuất |
| `discount_appendix`, `negotiation_minutes`, `contract_annex_*` (status riêng) | Là trạng thái của **phụ lục / BB thương thảo** (`record_type` 1 và 3) — không kết xuất được nên không có status 9 |
| `EmploymentContract`, `LaborContract`, `PurchaseContract`, `TpContract` | Hợp đồng lao động / HĐ mua / HĐ cũ — bảng khác |
| `AcceptanceReport` / `ContractLiquidation` / annex `status in:1,2,3,4` | Trạng thái của chính chứng từ con, không phải của HĐ |

**Kiểm chứng chạy thật trên HĐ 179 (HD-159/2026, status 9):**
```
approvedStatuses() = [3,9]
1. Dropdown chọn HĐ - Nghiệm thu            : CÓ
2. Dropdown chọn HĐ - Thanh lý              : CÓ
3. Dropdown chọn HĐ - Phiếu đề xuất cung ứng: CÓ
4. Dropdown chọn HĐ - Phụ lục (status=3,9)  : CÓ
5. Giao việc (canAssign)                    : CÓ
6. Màn "HĐ đã kết xuất" (status=9)          : CÓ
7. Kết xuất lại bị chặn                     : CÓ
```
- [x] `php -l` sạch; compile FE sạch

---

## Phase 13 — Siết validate khi kết xuất theo loại hợp đồng (@khoipv)

**Yêu cầu:** HĐ **trong thầu / nhảy thầu** (`type` = 1, 2) khi kết xuất bắt buộc điền đủ 4 mục:
Kết quả (tab Tiến độ thực hiện) · tab Kết quả hợp đồng · Điều khoản thanh toán · tab Bảo lãnh thực hiện hợp đồng.
Các loại HĐ khác (Cho/Tặng, Đặt/Mượn, Nguyên tắc) bắt buộc 3 mục đầu, **bảo lãnh không bắt buộc**.

- [x] BE: thêm `Contract::bidTypes()` = `[TRONG_THAU, NGOAI_THAU]` (Contract.php)
- [x] BE: `RenderSupplyContractRequest::assertTabHasData()` — check `results()->count()` (mọi loại) và `guarantees()->count()` (chỉ `bidTypes()`)
- [x] FE: tab "Kết quả hợp đồng" đổi sang `<template #title>` + computed `hasErrorInResultTab`
- [x] FE: `hasErrorInGuaranteeTab` nhận thêm key `guarantees` (không chỉ `guarantees.*`)
- [x] FE: `base-helper-error` cho `formError['results']` và `formError['guarantees']` dưới bảng của 2 tab
- [x] `php -l` sạch, compile FE sạch

### Checkpoint — 2026-08-26
Vừa hoàn thành: Phase 13 — validate kết xuất theo loại HĐ.
Đang làm dở: không.
Bước tiếp theo: user test tay trên `localhost:3001`.
Blocked:

---

## Phase 14 — Phân công người lập phiếu đề xuất cung ứng (@khoipv)

**Yêu cầu:** Giống luồng "phân công lập hợp đồng" của báo giá, nhưng dò người phụ trách theo
**nhóm nghiệp vụ Cung ứng (`group_permissions.id = 2`)** thay vì Hợp đồng (6).
Bổ sung quyền mới **"Phân công đề xuất cung ứng"**.

**Quyết định:**
- Nút "Tạo phiếu đề xuất cung ứng" chỉ hiện với **người được phân công** + có quyền `Lập phiếu đề xuất cung ứng`
- Lịch sử phân công lưu ở **bảng riêng** `contract_supply_assign_employees` (không đụng `contract_assign_employees` đang dùng cho bàn giao HĐ)
- HĐ đã kết xuất trước đó → chạy backfill auto-gán

### DB
- [x] Migration `2026_08_26_000004_add_supply_manager_to_contracts` — thêm `supply_manager_id`, `supply_received_time`, `supply_received_group_id` + index (đã chạy)
- [x] Migration `2026_08_26_000005_create_contract_supply_assign_employees_table` — bảng lịch sử, chỉ index, không khóa ngoại (đã chạy)

### BE
- [x] Entity `ContractSupplyAssignEmployee` (`TU_DONG = 1`, `THU_CONG = 2`)
- [x] `Contract`: `$fillable` +3 cột; hằng `NHOM_HOP_DONG = 6` / `NHOM_CUNG_UNG = 2`; quan hệ `supplyAssignEmployees()`, `supplyManager()`
- [x] `Contract::canCreateSupplyProposal()` — status 9 + đúng người được phân công + quyền `Lập phiếu đề xuất cung ứng`
- [x] `Contract::canAssignSupplyEmployee()` — status 9 + quyền `Phân công đề xuất cung ứng`
- [x] `ContractService::findSupplyManagerId()` — dò `category_customer_person_charge_business` theo `customer_id` + `group_permission_id = 2`, khớp `array_product_id` với `contract_array_product_ids`; chỉ trả về khi **đúng 1** nhân viên duy nhất
- [x] `ContractService::assignSupplyEmployee()` — ghi lịch sử + set 3 cột + `EmployeeInfoService::sendNotification`
- [x] `ContractService::autoAssignSupplyManager()` gọi cuối `renderSupply()`
- [x] `RenderedContractService::assignEmployee()` — phân công tay, chặn nếu không có quyền
- [x] `RenderedContractController::assignEmployee()` + route `PUT /supply/rendered-contracts/{contract}/assign-employee`
- [x] `RenderedContractResource` +`supply_manager_id`, `supply_manager_name`, `can_create_supply_proposal`, `can_assign_supply_employee`
- [x] Seeder quyền: id **524** `Phân công đề xuất cung ứng` (group `Cung ứng`, type 7) — đã insert thẳng vào DB
- [x] `EmployeeService` + `EmployeeController`: filter `create_supply_proposal` (lọc theo quyền `Lập phiếu đề xuất cung ứng`)
- [x] Backfill HĐ status 9 chưa có `supply_manager_id` — chạy xong (HD-159/2026 không dò ra ai → chờ phân công tay)

### FE
- [x] `components/modals/AddEmployeeCreateSupplyProposalModal.vue` (id `add-employee-create-supply-proposal`) — **chỉ liệt kê nhân viên nhóm nghiệp vụ Cung ứng** (`group_permission_id = 2`) theo yêu cầu @khoipv. Filter `create_supply_proposal` đã làm sẵn ở BE nhưng **không bật** vì dữ liệu hiện tại 2 tập rời nhau (8 NV nhóm Cung ứng / 13 NV có quyền `Lập phiếu đề xuất cung ứng`, giao = 0) → bật cả hai sẽ ra popup rỗng
- [x] `pages/supply/contract_render/constants.js` — thêm cột "NV phụ trách cung ứng"
- [x] `pages/supply/contract_render/index.vue` — cột NV phụ trách (rỗng → "Chưa phân công"), nút "Phân công lập phiếu đề xuất cung ứng" (`can_assign_supply_employee`), nút "Tạo phiếu đề xuất" gate theo `can_create_supply_proposal`
- [x] `php -l` sạch, compile FE sạch

### Checkpoint — 2026-08-26
Vừa hoàn thành: Phase 14 — phân công người lập phiếu đề xuất cung ứng (BE + FE).
Đang làm dở: không.
Bước tiếp theo: gán quyền **"Phân công đề xuất cung ứng"** cho vai trò ở màn Phân quyền, khai báo người phụ trách nhóm **Cung ứng** cho khách hàng ở màn Khách hàng → test tay trên `localhost:3001`.
Blocked:
