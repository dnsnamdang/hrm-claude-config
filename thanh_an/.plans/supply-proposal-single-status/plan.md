# Plan — Đề xuất cung ứng gộp 1 luồng trạng thái

**@khoipv · 2026-08-01**

## Backend
- [x] BE1. `SupplyProposal.php`: đổi hằng số (STATUS_TU_CHOI→STATUS_BGD_KHONG_DUYET, +STATUS_TU_CHOI_XU_LY=8), cập nhật STATUSES; xóa HANDLE_*/HANDLE_STATUSES/getHandleStatus*/rejections().
- [x] BE2. Migration `2026_08_01_..._single_status_supply_proposals`: +cột rejected_by/rejected_at; drop bảng supply_proposal_rejections; backfill status=9 cho phiếu đã đủ SL.
- [x] BE3. Xóa entity `SupplyProposalRejection.php`.
- [x] BE4. `SupplyProposalService.php`: reject() terminal (guard chưa có PXL); rejectByBoard() label mới; inbox() bỏ whereRaw→lọc status; buildResponses() bỏ nhánh rejection; index/inbox bỏ eager-load rejections; +syncHandledStatus().
- [x] BE5. `SupplyHandlingService.php`: gọi syncHandledStatus sau store/destroy/rejectApprove.
- [x] BE6. `SupplyProposalResource` + `DetailSupplyProposalResource`: bỏ 3 field handle_status; can_reject = DA_GUI & chưa có PXL & perm.

## Frontend
- [x] FE1. `constants.js`: STATUS + STATUS_OPTIONS bộ mới (+HANDLER_STATUS_OPTIONS cho inbox).
- [x] FE2. `index.vue`: statusBadge() chỉ dùng status_name/color.
- [x] FE3. `inbox.vue`: filter handle_status→status; cột status; bỏ nhánh rejection ở responses; bỏ dead code modal/showReason/viewReason.
- [x] FE4. `add.vue`: alert lý do cho status 7 & 8; dọn nhánh rejection ở responses timeline.
- [x] FE5. `purchase_orders/components/SupplyDocDetailModal.vue`: bỏ dòng handle_status_name (trạng thái đã có ở dòng trên).
- [x] FE6. `supply_handlings/add.vue`: responseText() bỏ nhánh rejection chết.

## Verify
- [x] V1. `php -l` 6 file BE (đều clean); migrate OK (batch 257); bảng rejections đã drop, cột rejected_by/rejected_at đã thêm, không phiếu nào kẹt (status 3=8, 7=1).
- [x] V2. Grep FE sạch handle_status/HANDLE_STATUS_OPTIONS/viewReason/kind==='rejection'. User E2E qua UI (chờ user).

## Checkpoint
### Checkpoint — 2026-08-01 (khởi tạo)
Vừa hoàn thành: brainstorm + chốt thiết kế + spec.
Đang làm dở: bắt đầu code BE1.
Bước tiếp theo: sửa entity SupplyProposal.
Blocked:

### Checkpoint — 2026-08-01 (đổi nhãn "Đã gửi" → "Chờ xử lý")
User: đổi nhãn trạng thái 3 từ "Đã gửi" thành "Chờ xử lý" (giữ hằng số STATUS_DA_GUI). Sửa: BE `SupplyProposal::STATUSES` name → "Chờ xử lý"; FE `constants.js` STATUS_OPTIONS text → "Chờ xử lý"; `SupplyDocDetailModal.vue` PROPOSAL_STATUS map cập nhật đúng bộ code hiện tại (2/3/7/8/9); 2 message lỗi BE "…phiếu đã gửi" → "…phiếu đang chờ xử lý". php -l clean, tinker xác nhận nhãn = "Chờ xử lý".

### Checkpoint — 2026-08-01 (điều kiện xóa phiếu)
User: đã gửi thì không cho xóa; BGĐ không duyệt / Từ chối xử lý thì cho xóa. Sửa `SupplyProposal::getIsCanDeleteAttribute`: owner + status ∈ {NHAP(1), BGD_KHONG_DUYET(7), TU_CHOI_XU_LY(8)}; bỏ nhánh cũ "Đã gửi & chưa có PXL". BE `destroy()` dùng `is_can_delete` nên tự chặn; FE index.vue gate `item.is_can_delete` sẵn — không cần sửa. Smoke: NHAP/7/8=YES; 2/3/9=no; không owner=no. php -l clean.

### Checkpoint — 2026-08-01 (inbox chỉ hiện phiếu chờ xử lý)
User: inbox chỉ thể hiện phiếu đã gửi chờ xử lý. Sửa BE `inbox()` lọc cứng `status = DA_GUI` (bỏ whereIn 3 trạng thái + bỏ `when($request->status)`). FE `inbox.vue`: bỏ dropdown lọc Trạng thái + cột Trạng thái + `HANDLER_STATUS_OPTIONS`/`statusOptions`/`formFilter.status`. Bỏ `HANDLER_STATUS_OPTIONS` khỏi constants.js. Smoke: inbox trả 4 phiếu đều status=3. php -l clean.

### Checkpoint — 2026-08-01 (gate nút Tạo PXL ở inbox)
User: phiếu "Đã xử lý" vẫn hiện nút Tạo phiếu xử lý. Chốt "1 phiếu, khóa luôn": nút chỉ hiện khi status = Đã gửi (3). Sửa `inbox.vue`: import STATUS + expose data() + `v-if="item.status === STATUS.DA_GUI && hasAPermission(PERM_HANDLE)"`. BE `SupplyHandlingService::store()` đã có guard sẵn (throw nếu status != DA_GUI) — không cần sửa. Chỉ inbox có nút này.

### Checkpoint — 2026-08-01 (điều chỉnh luật "Đã xử lý")
User phản hồi: cứ TẠO PHIẾU XỬ LÝ là để "Đã xử lý", không cần đủ SL. Sửa: thêm `SupplyProposal::hasActiveHandling()` (có ≥1 PXL status != 7); `syncHandledStatus` dùng nó thay `isFullyHandled`; đổi backfill trong migration sang "có ≥1 PXL hiệu lực → 9"; fix data dev (4 phiếu id 1/2/3/11 → 9). php -l 3 file clean. Spec + STATUS cập nhật.

### Checkpoint — 2026-08-01 (thông báo cho người tạo khi bị từ chối)
User: khi từ chối / BGĐ không duyệt có báo về người tạo không? → Trước đó KHÔNG. Đã thêm `notifyProposalCreator($model, $title)` trong `SupplyProposalService` (gửi tới employee_info của người tạo qua `employee_create->employee_info_id`, dùng `EmployeeInfoService::sendToAllNotification`, lý do gộp vào title). Gọi trong `rejectByBoard()` (title "…đã bị BGĐ không duyệt") và `reject()` (title "…đã bị từ chối xử lý"). php -l clean.

### Checkpoint — 2026-08-01 (hoàn tất code)
Vừa hoàn thành: toàn bộ BE1–BE6 + FE1–FE6 + V1/V2. Migration đã chạy (batch 257), bảng rejections drop, cột rejected_by/rejected_at thêm. php -l 6 file BE clean. FE sạch mọi tham chiếu handle_status.
Đang làm dở: không.
Bước tiếp theo: User bật client (Node 14) chạy E2E qua UI: gửi BGĐ→không duyệt (status "BGĐ không duyệt"), người xử lý từ chối khi chưa có PXL (status "Từ chối xử lý"), lập PXL đủ SL→auto "Đã xử lý", xóa PXL→revert "Đã gửi". Sau đó user tự commit.
Blocked:
