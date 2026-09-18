# Plan — Lập nhiều phiếu đề xuất cung ứng cho 1 hợp đồng

- **Người phụ trách**: @khoipv
- **Design**: [design.md](design.md) · **Spec**: [../../docs/superpowers/specs/2026-09-15-nhieu-phieu-de-xuat-mot-hop-dong-design.md](../../docs/superpowers/specs/2026-09-15-nhieu-phieu-de-xuat-mot-hop-dong-design.md)

---

## Phase 1 — Backend: tính SL đã đề xuất

- [x] `SupplyProposalService::proposedQtyMap($contractIds, $ignoreProposalId = null)` — gom
      `[contract_id][product_id][unit_id] => Σ quantity`, chỉ phiếu `deleted_at IS NULL` và
      `status NOT IN (7, 8)`, lọc theo `supply_proposal_products.contract_id`
- [x] `SupplyProposalService::withProposedQty($rows, $proposed, $unitMap)` — thêm 2 key
      `sl_da_de_xuat`, `sl_con_de_xuat`; quy đổi ĐVT + phân bổ waterfall; thiếu hệ số → bỏ qua
      `product_id` đó (coi như chưa đề xuất)
- [x] `SupplyProposalService::contractProductRows()` — thêm tham số `$proposedMap = null`,
      mặc định gán `sl_da_de_xuat = 0`, `sl_con_de_xuat = sl_con_lai_hd` (không đổi key cũ)
- [x] `SupplyProposalService::contractRow()` — thêm 2 key mới vào khuôn dòng

## Phase 2 — Backend: gỡ ràng buộc 1 HĐ ↔ 1 phiếu

- [x] `assertContractAvailable()` → comment lại, viết `assertContractHasRemaining($contractId, $ignoreProposalId)`
      với lỗi mới *"Hợp đồng này đã được đề xuất đủ số lượng."*
- [x] `store()` — đổi lời gọi sang `assertContractHasRemaining()`
- [x] `update()` — đổi lời gọi, truyền `$model->id` làm `$ignoreProposalId`
- [x] `SupplyProposalService::fullyProposedContractIds()` — trả ID các HĐ đã đề xuất đủ mọi dòng

## Phase 3 — Backend: danh sách HĐ đã kết xuất

- [x] `RenderedContractService::getList()` — comment `whereNotExists` cũ, thay bằng
      `whereNotIn('id', fullyProposedContractIds())`
- [x] `getList()` — thêm subquery `proposed_qty`, `remaining_qty`, `proposal_list` (GROUP_CONCAT)
- [x] `RenderedContractService::prefill()` — đổi sang `assertContractHasRemaining()`,
      `quantity = sl_con_de_xuat`, loại dòng `<= 0.0005`
- [x] `RenderedContractResource` — trả `proposed_qty`, `remaining_qty`, `proposal_items[]`
      (parse `proposal_list`, kèm `is_dead` cho status 7/8)

## Phase 4 — Frontend

- [x] `pages/supply/contract_render/constants.js` — thêm cột `proposal_progress`, `proposal_items`
- [x] `index.vue` — slot `cell(proposal_progress)`: `x/y (z%)`, chưa có phiếu → *"Chưa đề xuất"*;
      tooltip cảnh báo tổng gộp nhiều ĐVT
- [x] `index.vue` — slot `cell(proposal_items)`: liệt kê mã phiếu, link `/supply/supply_proposals/{id}`,
      phiếu chết gạch ngang + chữ nhạt; rỗng → `—`
- [x] **Fix**: cột Tiến độ đề xuất hiện *"Chưa đề xuất"* dù HĐ đã có phiếu — điều kiện
      `v-if` đang dựa vào `proposedQty(item) > 0`, đổi sang `hasProposals(item)` (căn cứ theo
      **có phiếu hay không**, không phải theo SL) — HD-191/2026 / DXCU-2026-0003 SL=0
- [x] Màn lập phiếu (`supply_proposals/add.vue`) — **không sửa gì** (xác nhận lại là không cần đụng)
- [x] **Chỉnh**: đổi label cột `proposal_progress` từ *Tiến độ đề xuất* → **Tiến độ**
      (`contract_render/constants.js`) — 16/09/2026
- [x] **Chỉnh**: cột Khách hàng rộng ra (`min-w-200` → `min-w-300`), bật **cuộn ngang**
      (`overflow-x` cho `div.b-table-sticky-header`) và **cố định 3 cột đầu** STT / Mã HĐ / Số HĐ
      (`sticky-col-1/2/3`, bề rộng khóa cứng 60/130/160px để tính `left`) — 16/09/2026
      ⚠️ Các class `min-w-*` không nằm trong scss dùng chung → page phải tự khai báo (trước đó
      `min-w-200/140/160` trong `constants.js` đang **vô tác dụng**)

## Phase 6 — Đổi cột Tiến độ sang trạng thái chữ (16/09/2026)

> ⚠️ **Đổi luật nghiệp vụ so với 15/09/2026**: HĐ đề xuất đủ **không còn bị ẩn** khỏi danh sách.

- [x] `RenderedContractService::getList()` — comment lại `whereNotIn(fullyProposedContractIds())`,
      thêm `selectRaw` cờ `is_fully_proposed` (CASE WHEN id IN (...)); docblock cập nhật theo luật mới
- [x] `RenderedContractResource` — trả `is_fully_proposed`; `can_create_supply_proposal`
      = `canCreateSupplyProposal() && !is_fully_proposed` → **HĐ đủ SL mất nút lập phiếu**
      (BE vốn đã chặn ở `assertContractHasRemaining()` nên 2 lớp khớp nhau)
- [x] FE `index.vue` — cột Tiến độ bỏ `x/y (z%)`, đổi sang badge 3 trạng thái:
      **Chưa đề xuất** (xám #9e9e9e) · **Đang lập đề xuất** (cam #f0ad4e) · **Hoàn thành** (xanh #28a745).
      Số liệu chi tiết + cảnh báo gộp ĐVT chuyển vào tooltip (`progressTooltip`)
- [x] Verify tinker (transaction rollback trên `HD-185/2026`): đề xuất đủ 2 dòng hàng →
      HĐ **vẫn trong danh sách**, `is_fully_proposed=true`, `can_create_supply_proposal=false`;
      bớt 1 SL → quay về `false` (Đang lập đề xuất). `php -l` sạch, SFC + SCSS compile sạch
- [x] Verify lại **prefill trừ SL phiếu trước** (user nhắc 16/09): tinker rollback trên `HD-185/2026`
      — lần 1 prefill 10/20 → đề xuất 1/3 → lần 2 còn 6,667/13,333 → đề xuất nốt dòng 1 → lần 3
      dòng 1 **biến mất**, dòng 2 giữ 13,333 → chuyển phiếu sang status 7 (phiếu chết) → SL **trả lại
      nguyên 10/20**. Ca ĐVT khác: phiếu trước ghi 5 × unit 10 trong khi HĐ ghi unit 1 → vẫn trừ đúng
      còn 15 (khớp theo `product_id` + quy đổi, không khớp cứng `unit_id`)
- [x] Test Playwright trên `http://localhost:3001/supply/contract_render` (đăng nhập bằng JWT phát hành
      trong tinker cho employee id 13 — không dùng mật khẩu):
      - Header đúng 14 cột, cột 12 là **Tiến độ**; không còn chuỗi `x/y (z%)` ở bất kỳ dòng nào
      - Badge: HD-150/2026, HD-185/2026, HD-159/2026 = "Chưa lập đề xuất"; HD-191/2026 = "Đang lập đề xuất"
        (phiếu DXCU-2026-0003). Trạng thái "Hoàn thành" **chưa quan sát được trên UI** vì DB hiện
        không có HĐ nào đề xuất đủ — đã verify ở tầng BE bằng transaction rollback (xem mục trên)
      - Cuộn ngang: wrapper `div.b-table-sticky-header` có `overflow-x: auto`, `scrollWidth` 1873 >
        `clientWidth` 1481; cột Khách hàng rộng đúng 300px
      - Sticky: sau khi cuộn `scrollLeft = 391`, Mã HĐ giữ nguyên x ≈ 79,8 và Số HĐ x ≈ 209,8 trong khi
        Tên HĐ trôi từ 370 → -21. Hit-test từng 0,25px quanh mép (76 → 83) luôn trúng ô sticky ⇒
        **không có khe hở**; vệt mờ 1px thấy trong ảnh chụp chỉ là artifact vẽ subpixel
      - Prefill trên UI: bấm nút lập phiếu ở dòng HD-191/2026 → `/supply/supply_proposals/add?contract_id=216`
        điền sẵn HĐ nguồn HD-191/2026, khách hàng, 3 dòng hàng, SL đề xuất 100/100/100 (tổng 300) —
        khớp API `/prefill`. Lưu ý: phiếu DXCU-2026-0003 có SL cả 3 dòng = **0.000** (dữ liệu test) nên
        không có gì để trừ; phần trừ SL đã verify ở tầng BE (HĐ 206, transaction rollback)
- [x] Đổi nhãn badge "Chưa đề xuất" → **"Chưa lập đề xuất"** (yêu cầu 16/09/2026) — `index.vue` `progressBadge()`
- [x] **Yêu cầu bổ sung 16/09/2026** — phiếu không còn hiệu lực (status 7/8) **không hiển thị**, HĐ chỉ
      còn phiếu chết thì badge quay về *Chưa lập đề xuất*: `getList()` subquery `proposal_list` thêm
      `whereNotIn('sp.status', $dead)`. FE không phải sửa logic (bám `proposal_items`), chỉ thêm ghi chú;
      nhánh `p.is_dead` giữ làm phòng vệ. Verify tinker rollback trên HĐ 216 / DXCU-2026-0003:
      status 9 → `["DXCU-2026-0003:9"]`; status 7 và 8 → `[]`; rollback → về như cũ. `php -l` sạch,
      template compile sạch
- [ ] User build lại client + hard refresh, test lại 15 ca ở §10 spec (luật ẩn/hiện HĐ đã đổi, §10 đã cập nhật)
- [x] Cập nhật spec `docs/superpowers/specs/2026-09-15-*-design.md` theo luật mới — sửa §3.3, §5.7,
      §5.8, §6.1, §8, §9, §10 và thêm **§11 — Cập nhật 16/09/2026** (bảng so sánh luật cũ/mới,
      3 trạng thái badge, layout sticky, file đã sửa, kết quả verify)
- [x] Cập nhật tóm tắt `.plans/nhieu-phieu-de-xuat-mot-hop-dong/design.md` + `.plans/STATUS.md`

## Phase 5 — Verify

- [x] `php -l` sạch toàn bộ file BE đã sửa
- [x] Compile SFC `contract_render/index.vue` bằng `vue-template-compiler` — không lỗi
- [x] Kiểm tra bằng `php artisan tinker`: HĐ đề xuất một phần vẫn nằm trong `getList()`,
      HĐ đề xuất đủ thì không
- [ ] User build lại client + hard refresh, test 15 ca ở §10 của spec

---

## Checkpoint
### Checkpoint — 15/09/2026
Vừa hoàn thành: code xong toàn bộ BE + FE, verify tự động **23/23 PASS** (8 ca nghiệp vụ chạy trong
transaction rollback trên DB `thanhan_stag_07052026`) + 2 ca ĐVT (quy đổi hệ số, thiếu hệ số) đều đúng.
SFC `contract_render/index.vue` compile sạch bằng `vue-template-compiler`.

File đã sửa:
- `Modules/Supply/Services/SupplyProposalService.php` — thêm `QTY_EPSILON`, `deadStatuses()`,
  `proposedQtyMap()`, `withProposedQty()`, `fullyProposedContractIds()`, `assertContractHasRemaining()`;
  `contractProductRows()` thêm tham số `$proposedMap`; `contractRow()` thêm 2 key;
  `assertContractAvailable()` **comment lại không xóa**
- `Modules/Supply/Services/RenderedContractService.php` — `getList()` bỏ `whereNotExists` (comment lại),
  thêm `whereNotIn` + 3 subquery `proposed_qty` / `remaining_qty` / `proposal_list`;
  `prefill()` dùng `sl_con_de_xuat`
- `Modules/Supply/Transformers/RenderedContract/RenderedContractResource.php` — trả `proposed_qty`,
  `remaining_qty`, `proposal_items[]`
- `pages/supply/contract_render/constants.js` + `index.vue` — 2 cột mới

Bẫy đã gặp và xử lý:
- `GROUP_CONCAT ... SEPARATOR CHAR(30)` → MySQL báo lỗi cú pháp, SEPARATOR bắt buộc là **hằng chuỗi**
  → nhúng thẳng `chr(30)` từ PHP
- `GROUP_CONCAT(DISTINCT ...) ORDER BY cột khác` không hợp lệ → đổi sang subquery từ `supply_proposals`
  + `whereExists` (không join, không cần DISTINCT)
- `SUM(cp.qty - cp.exported_qty)` bỏ sót dòng có `exported_qty` NULL → bọc `COALESCE` từng cột

Đang làm dở: không có.
Bước tiếp theo: user build lại client + hard refresh, test 15 ca ở §10 của spec.
Blocked: không có.

### Checkpoint — 16/09/2026
Vừa hoàn thành: đợt chỉnh màn "Hợp đồng đã kết xuất" (Phase 6) + test Playwright + đồng bộ tài liệu.

Việc đã làm trong ngày:
- Đổi label cột `Tiến độ đề xuất` → **Tiến độ**
- Cột Khách hàng nới 300px, bật cuộn ngang, cố định 3 cột STT / Mã HĐ / Số HĐ (width khóa cứng
  60/130/160px). Phát hiện các class `min-w-*` không có trong scss dùng chung → page tự khai báo
- **Đổi luật**: HĐ đề xuất đủ không còn bị ẩn, vẫn ở lại danh sách và chỉ mất nút lập phiếu
  (`getList()` comment lại `whereNotIn`, thay bằng cờ `is_fully_proposed`; Resource siết
  `can_create_supply_proposal`)
- Cột Tiến độ bỏ `x/y (z%)`, ra badge 3 trạng thái; số liệu + cảnh báo đa ĐVT chuyển vào tooltip
- Đổi nhãn badge xám thành **"Chưa lập đề xuất"** (yêu cầu cuối ngày)
- Verify: `php -l` sạch, SFC + SCSS compile sạch, tinker transaction rollback (cờ đủ/không đủ,
  prefill trừ SL phiếu trước, ca ĐVT khác), Playwright trên `localhost:3001`
- Tài liệu: spec thêm **§11**, `design.md` + `STATUS.md` cập nhật theo luật mới

Đang làm dở: không có.
Bước tiếp theo: user hard refresh và test lại 15 ca ở §10 spec (đã cập nhật theo luật mới).
Blocked: không có. Còn 2 điểm chỉ mới verify ở tầng BE, chưa nhìn thấy trên UI vì DB stag không có
dữ liệu phù hợp: badge **Hoàn thành** và **prefill trừ SL phiếu trước** (phiếu DXCU-2026-0003 có
SL = 0). Muốn xem tận mắt thì cần một HĐ có phiếu SL > 0 trên stag.

### Checkpoint — 16/09/2026 (bổ sung cuối ngày)
Vừa hoàn thành: ẩn phiếu không còn hiệu lực khỏi cột "Phiếu đề xuất" và cho HĐ chỉ-còn-phiếu-chết quay
về badge *Chưa lập đề xuất* — sửa 1 dòng ở `RenderedContractService::getList()`
(`proposal_list` + `whereNotIn('sp.status', $dead)`), cập nhật comment ở Resource + `index.vue`,
spec thêm **§11.6**.

Đang làm dở: không có.
Bước tiếp theo: deploy lên `dev-thanhan.dnsmedia.vn` rồi user test lại màn `supply/contract_render`.
Blocked: không có.
