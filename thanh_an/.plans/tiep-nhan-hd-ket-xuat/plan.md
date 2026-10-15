# Plan — Tiếp nhận thông tin HĐ đã kết xuất (Cung ứng)

> @khoipv — Bắt đầu 05/10/2026
> Design: [design.md](design.md) · Spec: [docs/superpowers/specs/2026-10-05-tiep-nhan-hd-ket-xuat-design.md](../../docs/superpowers/specs/2026-10-05-tiep-nhan-hd-ket-xuat-design.md)

**Mục tiêu:** mỗi HĐ đã kết xuất có 1 người tiếp nhận (tự hủy được), lưu lịch sử; thao tác ở màn HĐ đã kết xuất + màn chi tiết HĐ (`?from=supply_render`).

## Ràng buộc chung
- Migration chỉ index, KHÔNG khóa ngoại; cột `supply_received_by` = `bigint unsigned`
- Không quyền, không phạm vi; không ghi chú; không thông báo; không bộ lọc
- Tiếp nhận / hủy dùng `DB::table('contracts')` update có điều kiện → không đổi `updated_at` HĐ, chống bấm đồng thời
- FE màn cũ: cột Thao tác theo button-convention Phần B (≤ 3 nút hiện hết), nút đổi trạng thái phải hỏi xác nhận
- Không commit / push

## Điểm cần soi kỹ khi review
1. 2 người tiếp nhận cùng lúc → chỉ 1 người thành công, người kia nhận message rõ ràng + FE tải lại thấy tên người nhận
2. Người không phải người nhận gọi thẳng `cancel-receive` → 400, không xóa người nhận
3. Màn chi tiết HĐ vào từ phân hệ Hợp đồng (không có `?from=supply_render`) → không đổi gì, không gọi `receive-info`
4. `contracts.updated_at` giữ nguyên sau tiếp nhận / hủy
5. Danh sách không phát sinh N+1 khi lấy tên người nhận

## Phase 0 — Brainstorming
- [x] Khảo sát màn HĐ đã kết xuất + màn chi tiết HĐ + pattern lịch sử sẵn có
- [x] Chốt yêu cầu với user (1 người/HĐ, tự hủy được, ai cũng nhận, không ghi chú, không ràng buộc phiếu đề xuất)
- [x] Viết spec + design.md
- [x] User review spec

## Phase 1 — BE (`hrm-thanhan-api`)
- [x] **Task 1 — Migration + entity**
  - `Modules/Supply/Database/Migrations/2026_10_05_000001_add_supply_receive_columns_to_contracts.php`
  - `Modules/Supply/Database/Migrations/2026_10_05_000002_create_contract_supply_receive_histories_table.php`
  - `Modules/Supply/Entities/ContractSupplyReceiveHistory.php` (hằng `TIEP_NHAN = 1`, `HUY_TIEP_NHAN = 2`, `ACTION_NAMES`)
  - Chạy `php artisan migrate` trên DB stag, kiểm tra cột + index
- [x] **Task 2 — Contract: quan hệ + accessor**
  - `Modules/Category/Entities/Contract/Contract.php`: `supplyReceiver()`, `canSupplyReceive()`, `canCancelSupplyReceive()`
- [x] **Task 3 — Service + controller + route**
  - `RenderedContractService`: `receive(Contract)`, `cancelReceive(Contract)`, `receiveInfo(Contract): array`, ghi lịch sử qua `logReceiveHistory(Contract, int $action)`; `getList()` thêm `supplyReceiver.info`
  - `RenderedContractController`: `receive`, `cancelReceive`, `receiveInfo` (bọc `DB::transaction`, lỗi → 400 + message)
  - `Modules/Supply/Routes/api.php`: `POST /{contract}/receive`, `POST /{contract}/cancel-receive`, `GET /{contract}/receive-info`
- [x] **Task 4 — Resource danh sách**
  - `RenderedContractResource`: `supply_received_by`, `supply_receiver_name`, `supply_received_at`, `can_receive`, `can_cancel_receive`
- [x] **Task 5 — Test BE**
  - `php -l` các file sửa
  - Script tinker bọc transaction + rollback trên 1 HĐ status 9: A nhận → B nhận bị chặn → B hủy bị chặn → A hủy → B nhận được; lịch sử 3 dòng mới nhất lên đầu; `updated_at` HĐ không đổi; `receiveInfo()` trả đúng cờ theo người đăng nhập

## Phase 2 — FE (`hrm-thanhan-client`)
- [x] **Task 6 — Popup lịch sử dùng chung**
  - `pages/supply/contract_render/components/ReceiveHistoryModal.vue` (mẫu `HistoryApproveModal.vue`): props `id`, `contractId`; mở popup → gọi `supply/rendered-contracts/{id}/receive-info`
- [x] **Task 7 — Màn HĐ đã kết xuất**
  - Logic xác nhận → gọi API → toast tách ra `pages/supply/contract_render/receive-mixin.js` (dùng chung 2 màn, cờ `receiveLoading` chống bấm 2 lần)
  - `constants.js`: cột `supply_receiver` "Người tiếp nhận" sau `supply_rendered_at`
  - `index.vue`: slot cột (tên + giờ / `—` + link "Lịch sử"); `rowActions` thêm Tiếp nhận / Hủy tiếp nhận; link Xem + mã HĐ thêm `?from=supply_render`; `onReceive` / `onCancelReceive` (swal → loading → API → toast → `getData()`, lỗi vẫn `getData()`, chặn bấm 2 lần)
- [x] **Task 8 — Màn chi tiết HĐ**
  - `pages/contract/contract/_id/index.vue`: computed `fromSupplyRender`; khi true: gọi `receive-info`, breadcrumb Cung ứng, khối "Người tiếp nhận", nút Tiếp nhận / Hủy tiếp nhận / Lịch sử tiếp nhận cạnh nút Hủy, dùng `ReceiveHistoryModal`
- [x] **Task 9 — Kiểm tra FE**
  - Compile check các file `.vue` sửa (vue-template-compiler + babel)
  - Prettier/eslint theo cấu hình repo nếu có

## Phase 3 — Chỉnh sửa sau kiểm tra
- [x] **Task 10 — Bỏ cột "Số dòng hàng"** ở màn HĐ đã kết xuất (`constants.js` xóa field `sum_product_qty`; BE giữ nguyên key trong resource, không ảnh hưởng)
- [x] **Task 11 — Màn chi tiết HĐ: bỏ dòng "Chưa có người tiếp nhận"** — khối người tiếp nhận chỉ hiện khi đã có người nhận (`pages/contract/contract/_id/index.vue`)
- [x] **Task 12 — Màn chi tiết HĐ: bỏ nút "Lịch sử tiếp nhận"** — xóa nút, `ReceiveHistoryModal` + `openReceiveHistory()` khỏi `pages/contract/contract/_id/index.vue` (popup lịch sử vẫn dùng ở màn HĐ đã kết xuất)
- [x] **Task 13 — Màn chi tiết HĐ (từ màn kết xuất): thêm nút "Lập phiếu đề xuất"**
  - BE `RenderedContractService::receiveInfo()` trả thêm `can_create_supply_proposal` = `canCreateSupplyProposal()` && HĐ còn SL chưa đề xuất (tận dụng `SupplyProposalService::assertContractHasRemaining()`) — cùng điều kiện nút ở màn danh sách
  - FE `pages/contract/contract/_id/index.vue`: nút "Lập phiếu đề xuất" → `/supply/supply_proposals/add?contract_id={id}`
  - `php -l` + prettier
- [x] **Task 14 — Popup xác nhận tiếp nhận / hủy tiếp nhận dùng `ConfirmModal` (b-modal base) thay `$swal`**
  - `receive-mixin.js`: `askSupplyReceive()` mở popup (id mặc định `modal-confirm`, không sửa component dùng chung) → `confirmSupplyReceive()` gọi API → màn tự định nghĩa `afterSupplyReceive()` để tải lại
  - Đặt `<ConfirmModal>` ở `pages/supply/contract_render/index.vue` + `pages/contract/contract/_id/index.vue` (chỉ khi `fromSupplyRender`)
  - Câu hỏi nêu mã HĐ; compile check + prettier
- [x] **Task 15 — Màn HĐ đã kết xuất: đổi cột "Người tiếp nhận" → "Tiếp nhận thông tin"**
  - `constants.js` đổi label; `index.vue` slot hiện badge Đã tiếp nhận (xanh) / Chưa tiếp nhận (xám), tooltip tên + giờ người nhận
  - Bỏ link "Lịch sử" trong cột → thêm action "Lịch sử tiếp nhận" vào cột Thao tác (cuối danh sách, >3 nút thì vào bánh răng)
- [x] **Task 16 — Bộ lọc "Tiếp nhận thông tin" (Đã / Chưa tiếp nhận)**
  - BE `RenderedContractService::getList()`: tham số `receive_status` (1 = đã tiếp nhận → `supply_received_by` NOT NULL, 2 = chưa → NULL); hằng `RECEIVE_STATUS_*` ở service
  - FE `pages/supply/contract_render/index.vue`: ô `base-select2` (allowClear) trong bộ lọc, `initialStateForm.receive_status`; option ở `constants.js`
  - `php -l` + compile check + prettier

### Checkpoint — 05/10/2026 17:35
Vừa hoàn thành: Task 1–9 (BE + FE tiếp nhận thông tin HĐ đã kết xuất). BE test bằng script có rollback: A nhận → B bị chặn nhận/hủy → A hủy → B nhận; lịch sử 3 dòng mới nhất lên đầu; `updated_at` HĐ không đổi; HĐ chưa kết xuất bị chặn. FE compile check + prettier OK.
Đang làm dở: —
Bước tiếp theo: user kiểm tra trên trình duyệt (màn HĐ đã kết xuất: cột Người tiếp nhận, nút Tiếp nhận/Hủy, popup Lịch sử; màn chi tiết HĐ khi vào từ màn kết xuất). Deploy nhớ chạy 2 migration `2026_10_05_00000{1,2}` của module Supply.
Blocked:
