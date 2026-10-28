# Plan — Trả lại / thu hồi HĐ đã kết xuất sang cung ứng

> @khoipv — Bắt đầu 26/10/2026 · Spec: [docs/superpowers/specs/2026-10-26-tra-lai-thu-hoi-hd-da-ket-xuat-design.md](../../docs/superpowers/specs/2026-10-26-tra-lai-thu-hoi-hd-da-ket-xuat-design.md) · Design: [design.md](design.md)

**Ràng buộc chung:** migration chỉ index, không FK · không commit/push khi chưa được bảo · màn V2 (`supply/contract_render`) theo skill button-convention A + modal-popup + form-validate; màn cũ (`contract/contract`) theo button-convention B · label bắt buộc dùng `<Required />` · không tự chạy Playwright.

**Review focus (dễ vỡ nhất):** (1) trả lại đúng lúc lưu phiếu → không được cả hai cùng thành công · (2) ~~lưu phiếu chỉ có `products[].contract_id` sau khi trả lại → phải lỗi~~ (bỏ, xem Phase 3) · (3) hồi quy lưu/sửa phiếu nội bộ, KH lẻ, phiếu HĐ còn SL · (4) HĐ chỉ còn phiếu chết 7/8 → trả lại được · (5) banner lý do trả lại không lẫn `reason_deny` từ chối kết xuất và biến mất khi gửi lại.

## Phase 1 — BE: dữ liệu + điều kiện
- [x] Migration `Modules/Category/Database/Migrations/2026_10_26_000001_add_supply_return_columns_to_contracts.php`: `supply_returned_at` dateTime null · `supply_returned_by` ubigint null index · `supply_return_reason` text null (after `supply_render_requested_by`) + chạy `php artisan migrate`
- [x] `Contract`: thêm 3 cột vào `$fillable`; `hasLiveSupplyProposal(): bool`; `canReturnRenderSupply(): bool`; `canWithdrawRenderedSupply(): bool` (status 9 + rendered_at + HOP_DONG + !live; withdraw thêm `created_by == auth`)
- [x] Tách subquery phiếu sống: `SupplyProposalService::liveProposalExistsFor(string $contractIdColumn, ?callable $extra = null): \Closure` (public static) — `RenderedContractService::liveProposalSubquery()` gọi lại, kết quả không đổi
- [x] `HistoryApprovedContract`: 6 hằng `ACTION_RENDER_*` (chuỗi giữ nguyên DB) + `renderSupplyActions(): array`; `ContractService` render/approve/reject/withdraw đổi sang hằng

## Phase 2 — BE: hành động + API
- [x] `ContractService::returnRenderSupply(Contract, string $reason)` · `withdrawRenderedSupply(Contract)` · `resetRenderedSupply(Contract)` (private, reset cột chung) · `renderSupplyHistory(Contract)`; `renderSupply()` xóa `supply_return_*`
- [x] `ReturnRenderSupplyContractRequest` (`reason` required|string|max:1000)
- [x] Route + action: `POST /supply/rendered-contracts/{contract}/return` → `RenderedContractController::returnContract` · `PUT /category/contracts/{contract}/withdraw-rendered-supply` → `ContractController::withdrawRenderedSupply` · `GET /category/contracts/{contract}/render-supply-history` → `ContractController::renderSupplyHistory`
- [x] Resource: `ContractResource` + `ContractDetailResource` thêm `can_withdraw_rendered_supply`, `can_return_render_supply`, `supply_return_reason`, `supply_returned_at`; `RenderedContractResource` thêm `can_return`

## Phase 3 — BE: siết hàm dùng chung (user đồng ý 26/10/2026)
- [x] `SupplyProposalService::assertContractHasRemaining()` đọc HĐ `lockForUpdate()` (chỉ khi đang trong transaction — prefill / cờ danh sách đọc thường)
- [~] ~~`store()`/`update()` suy HĐ nguồn từ `products[].contract_id` khi header rỗng~~ — **BỎ**: `contractGoodsPool()` cho phiếu lập tay chọn hàng của HĐ status 3/9/10/11 (cả HĐ chưa kết xuất) → suy ra rồi kiểm `supply_rendered_at` sẽ chặn nhầm mọi phiếu tay bám HĐ chưa kết xuất. HĐ bị trả lại về 3 thì lập phiếu tay như mọi HĐ đã duyệt khác (đúng nghiệp vụ hiện tại); đường lập từ màn kết xuất (header `contract_id`) vẫn bị chặn
- [x] `RenderedContractService::receive()` update thêm `where status = 9` + `whereNotNull supply_rendered_at`; `cancelReceive()` giữ nguyên (cố ý không xét status; sau trả lại `supply_received_by` đã null nên tự chặn)
- [x] `php -l` + script transaction rollback 9 ca §9 spec — 26/26 PASS + ca (3) giả lập phiếu chết PASS

## Phase 4 — FE
- [x] `pages/supply/contract_render/components/ReturnContractModal.vue` (V2BaseModal, `V2BaseLabel required` + V2BaseTextarea, formValidateMixin, lỗi 422) + `RenderSupplyHistoryModal.vue` (V2BaseModal, bảng lịch sử)
- [x] `pages/supply/contract_render/index.vue`: row action **Trả lại** (`can_return`) + **Lịch sử kết xuất**
- [x] `pages/contract/contract/_id/index.vue`: nút **Trả lại** cạnh Tiếp nhận (cờ `can_return` thêm vào API `receive-info`), xong về `/supply/contract_render`
- [x] `pages/contract/contract/index.vue`: nút **Thu hồi** fa-undo cho `can_withdraw_rendered_supply` + confirm; dropdown **Lịch sử kết xuất** (status 3/9/10/11) dùng modal style cũ `components/RenderSupplyHistoryModal.vue`
- [x] `pages/contract/contract/_id/render.vue`: banner đỏ trả lại (`status == 3 && supply_return_reason`)
- [x] Compile check các file .vue (vue-template-compiler + @babel/parser — 7/7 OK)

## Phase 5 — Wrap
- [x] Cập nhật checkpoint + STATUS.md, báo user test (migrate + build client + hard refresh)
- [x] Spec §5.6 + §9 + design.md ghi nhận bỏ ý suy HĐ từ dòng hàng

## Phase 6 — Test kỹ (user yêu cầu 26/10/2026)
- [x] Chạy lại script BE rollback (t_return + t_dead) — PASS
- [x] Test HTTP thật qua API :8001 (token): quyền/route, 422 lý do trống/quá dài, 400 trạng thái, thu hồi bởi người khác, lịch sử — snapshot + khôi phục dữ liệu HĐ test — 43/43 PASS
- [x] Test UI bằng Playwright MCP: màn HĐ đã kết xuất (nút Trả lại / Lịch sử, popup lý do, validate), chi tiết HĐ, danh sách HĐ (Thu hồi, Lịch sử kết xuất), banner render.vue — OK
- [x] Khôi phục dữ liệu test (HĐ 170/179/193/216 về status 9, xóa history/notifications/jobs phát sinh), ghi kết quả
- [x] Fix phát sinh khi test: người lập = người tiếp nhận (vd HĐ 193) thu hồi thì tự báo cho chính mình → chặn tự báo ở `withdrawRenderedSupply` + `returnRenderSupply` (ContractService, inline, không sửa helper chung)
- [x] Fix phát sinh khi test: banner lý do trả lại ở render.vue mất xuống dòng → span `.supply-return-reason` + `white-space: pre-line`

### Checkpoint — 26/10/2026 (test xong)
Vừa hoàn thành: Phase 6 — test BE/HTTP/UI đều đạt, sửa 2 lỗi phát sinh, đã khôi phục dữ liệu test
Đang làm dở: —
Bước tiếp theo: đã push master (API 90d50310, client 2a50e962) — chạy migrate 2026_10_26_000001 trên server + build client
Blocked:

### Checkpoint — 26/10/2026
Vừa hoàn thành: Phase 1–4 (BE + FE) + cập nhật spec/design
Đang làm dở: —
Bước tiếp theo: user test UI (migrate đã chạy; build lại client + hard refresh) → commit
Blocked: 
