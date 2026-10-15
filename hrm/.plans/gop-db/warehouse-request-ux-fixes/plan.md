# Plan — Sửa UX màn Đề nghị nhập/xuất kho (Redmine feedback)

Nguồn: ảnh mô tả task Redmine (2026-09-18), 2 việc.

## Việc 1 — Lập đề nghị kho xong phải về màn DANH SÁCH, không về màn chi tiết
- [x] `pages/finance/warehouse-import-requests/create.vue` — sau khi lưu thành công đang
      `$router.push('/finance/warehouse-import-requests/${newId}')` (chi tiết) → đổi về
      danh sách `/finance/warehouse-import-requests`. Đúng quy ước CLAUDE.md "Thao tác xong
      QUAY VỀ MÀN DANH SÁCH".
- [x] `pages/finance/warehouse-export-requests/create.vue` — cùng anti-pattern (item 1 ghi
      chung "đề nghị kho"), đổi tương tự về `/finance/warehouse-export-requests`.
- Vẫn giữ `uploadPendingFiles(newId)` trước khi điều hướng (cần id vừa tạo để đính kèm file).
- [x] `pages/finance/warehouse-import-requests/_id/edit.vue:318` — sau khi LƯU (PUT) cũng đang
      push chi tiết `${this.id}` → đổi về danh sách (user chốt "sửa luôn" 2026-09-18). `goBack()`
      giữ nguyên (nút "Quay lại" là điều hướng riêng).
- [x] `pages/finance/warehouse-export-requests/_id/edit.vue:391` — tương tự, về danh sách.

## Việc 2 — Nút "Tạo đề nghị nhập kho" đổi sang màu xanh
- [x] `pages/finance/product-import-requests/_id/index.vue` — nút "Tạo đề nghị nhập kho" đang
      `secondary` (trắng) → đổi `primary` (teal `#1abc9c` = "xanh" theo skill button-convention).
      Đồng bộ với nút sibling "Lập đề nghị xuất kho" ở `product-export-requests/_id/index.vue`
      vốn đã là `primary`. Nút "Tạo phiếu nhập hàng" (tầng 3, mở ERP) giữ `secondary`.

## Việc 4 — Popup "Từ chối đề nghị nhập kho" không giống các màn khác
Nguồn: ảnh feedback #4 "Popup confirm từ chối đang không giống như các màn khác" + 2 chú thích
("popup nằm cao hơn ở khoảng general-info", "2 nút đang đảo vị trí").
Chẩn đoán: `pages/finance/warehouse-import-requests/_id/index.vue` tự dựng `<b-modal>` cho popup
Từ chối (vi phạm modal-popup §3a), còn nút Hủy dùng `$bvModal.msgBoxConfirm()` (cũng bị cấm) →
2 popup này trông khác toàn hệ thống. Chuẩn: dùng chung `base-confirm-modal` như sibling
`borrow-sell-requests/_id/index.vue`.
- [x] Thay `<b-modal>` Từ chối bằng `<BaseConfirmModal id="deny-warehouse-import-request">`:
      `show-input` + `input-type="textarea"` + `required-input` (bắt buộc lý do, giữ popup mở +
      lỗi inline khi rỗng), `:message="denyMessage"`, `text-accept="Từ chối"`
      `accept-icon="ri-close-circle-line"` `:danger="true"`, `text-close="Đóng"`.
- [x] Thay `$bvModal.msgBoxConfirm()` của nút Hủy bằng `<BaseConfirmModal
      id="cancel-warehouse-import-request">` (`text-accept="Hủy đề nghị"` `:danger="true"`).
- [x] Script: bỏ import `V2BaseLabel`/`V2BaseTextarea` + data `denyComment`/`denyError`; thêm
      import + đăng ký `BaseConfirmModal`; thêm computed `denyMessage`/`cancelMessage`;
      `openDenyModal`/`confirmCancel` → `$bvModal.show(id)`; `submitDeny(comment)` nhận payload
      emit; thêm `submitCancel()`; cả 2 lệnh POST bọc `$safeLoadingStart/Finish` (button-convention §6b).
- Về chú thích "2 nút đảo vị trí": `base-confirm-modal` render **nút hành động (Từ chối) TRÁI /
  Đóng PHẢI** — đúng button-convention §5 và khớp mọi màn khác (borrow-sell). Không đảo nút; việc
  dùng component chung tự cho đúng header/icon + vị trí + thứ tự = "giống các màn khác".
- [x] Verify Playwright 127.0.0.1:3000.

## Việc 5 — Nút "Từ chối" ở màn chi tiết Đề nghị nhập kho (PDNNK)
Nguồn: ảnh feedback #5 "Chỉ Từ chối/duyệt đề nghị nhập kho đang ở trạng thái 'Chờ duyệt'" + chú thích
"Vậy nút Từ chối ở màn chi tiết nhập kho đang k có ý nghĩa gì => Bỏ" (ảnh PDNNK-08541, Chờ duyệt).
Kiểm tra logic bên ERP (user yêu cầu "kiểm tra lại logic này bên erp"):
- ERP **CÓ** nút Từ chối ở màn chi tiết PDNNK (`warehouse_import_requests/show.blade.php:171`:
  `@if ($req->canApprove() && $req->type != 11)`), route `POST warehouseImportRequest/{id}/deny`
  → `WarehouseImportRequestsController@deny` (WIR 2→3, YCNH nguồn→7, bắt buộc `comment`, thủ kho +
  Chờ duyệt). ⇒ Nút **CÓ ý nghĩa**, HRM đang khớp ERP. Kết luận: **KHÔNG bỏ nút** (user chốt "giữ
  nguyên" 2026-09-18).
- Khác biệt thật: HRM `is_can_deny = $isWaiting && $isStocker` **thiếu** loại trừ `type != 11`
  (ERP ẩn Từ chối với `MUA_HANG_NUOC_NGOAI_MOI` = "Nhập hàng mua nước ngoài (mới)"/nhập khẩu).
- [x] `WarehouseImportRequestResource.php` — thêm `&& (int) $this->type !==
      ProductImportRequest::MUA_HANG_NUOC_NGOAI_MOI` vào `is_can_deny` (import
      `Modules\Finance\Entities\ProductImportRequest\ProductImportRequest`), cập nhật docblock.
      `php -l` sạch, file LF (0 CR). Không đụng FE (nút đã bind `detail.is_can_deny`).

## Checkpoint
### Checkpoint — bắt đầu (2026-09-18)
Vừa hoàn thành: định vị 3 file + đọc skill button-convention.
Đang làm: sửa 3 chỗ (2 router.push + 1 màu nút).
Bước tiếp theo: verify Playwright 127.0.0.1:3000.
Blocked: không

### Checkpoint — ĐÃ commit + push (2026-09-18)
Vừa hoàn thành: commit 5 file hrm-client lên nhánh `gop_db`.
- Commit `96caca5a8` — "fix(finance): đề nghị nhập/xuất kho lưu xong về màn danh sách + nút
  Tạo đề nghị nhập kho màu xanh". 5 files changed, 9 insertions(+), 13 deletions(-).
- Rebase lên `origin/gop_db` (up to date, không có commit teammate mới) → push sạch
  `e21791d84..96caca5a8`. hrm-api KHÔNG có thay đổi (không cần commit).
Bước tiếp theo: xong task. Chờ QA nghiệm thu.
Blocked: không

### Checkpoint — Việc 4: popup Từ chối/Hủy chuẩn hoá (2026-09-18)
Vừa hoàn thành: `warehouse-import-requests/_id/index.vue` — thay `<b-modal>` Từ chối tự dựng +
`$bvModal.msgBoxConfirm()` của Hủy bằng 2 `<BaseConfirmModal>` dùng chung (`deny-...` có
`required-input` textarea, `cancel-...` không ô nhập). Bỏ import/data thừa, thêm computed
`denyMessage`/`cancelMessage`, methods dùng `$bvModal.show(id)` + `submitDeny(comment)`/`submitCancel`
bọc `$safeLoadingStart/Finish`.
Verify Playwright (PDNNK-01886, ép mở modal qua `$bvModal.show`, không đổi DB):
- Popup Từ chối: header icon cảnh báo đỏ + tiêu đề "Từ chối đề nghị nhập kho" + X; body
  "Phiếu **PDNNK-01886** sẽ bị từ chối." + ô "Lý do từ chối *" (textarea); footer **Từ chối (đỏ,
  trái x=649) / Đóng (phải x=744)** = đúng button-convention §5; dialog nằm cao (top=28) đúng chú
  thích feedback. Bấm Từ chối khi rỗng → popup GIỮ mở + viền đỏ + lỗi inline "Vui lòng nhập lý do
  từ chối." (required-input).
- Popup Hủy: "Xác nhận hủy" + "Phiếu **PDNNK-01886** sẽ bị hủy." + **Hủy đề nghị (trái) / Đóng
  (phải)**, không ô nhập. Screenshot đã chụp + xem đạt.
File LF (0 CRLF). CHƯA commit/push (chờ user yêu cầu).
Bước tiếp theo: chờ user chốt commit.
Blocked: không

### Checkpoint — XONG code + verify (2026-09-18)
Vừa hoàn thành: cả 3 sửa đổi + verify.
- Việc 2 (VERIFY THẬT TRÊN UI): mở màn chi tiết PYCNH-14032, ép tạm `is_can_approve=true`
  trong bộ nhớ component (không gọi API, không đổi DB) → nút "Tạo đề nghị nhập kho" render
  class `v2-btn--primary`, nền `rgb(26,188,156)` = `#1abc9c` (teal/xanh), chữ trắng. ĐẠT.
- Việc 1 (VERIFY CODE + COMPILE): sửa `warehouse-import-requests/create.vue:340` và
  `warehouse-export-requests/create.vue:395` từ push chi tiết `${newId}` → push danh sách.
  Màn create load + compile sạch (không có nuxt error overlay). CHƯA tạo bản ghi ĐNNK thật
  để test redirect runtime (tránh ghi rác vào erp_new) — có thể chạy live nếu user muốn.
- File đều LF, không đụng CRLF. Chưa commit/push (chờ yêu cầu).
Bước tiếp theo: chờ user chốt có mở rộng sang 2 màn edit (`_id/edit.vue`) không.
Blocked: không

### Checkpoint — Fix title tab trình duyệt ĐNNK (2026-10-09)
Vừa hoàn thành: thêm `head()` cho 4 màn `finance/warehouse-import-requests` để title tab khớp tên màn.
- Nguyên nhân: các màn chỉ có `PageTitleMixin` (chỉ commit `pageTitle` vào Vuex cho header trong app),
  THIẾU `head()` của Nuxt → tab lấy title mặc định ("Tân Phát…").
- Fix:
  - `index.vue`, `create.vue`, `_id/edit.vue`: thêm `head() { return { title: this.pageTitle } }`
    (pageTitle là chuỗi plain) — khớp pattern các màn finance khác.
  - `_id/index.vue`: `pageTitle` dùng `buildStatusTitle` TRẢ HTML (badge `<span>`) → KHÔNG dùng
    `this.pageTitle` (sẽ lòi nguyên thẻ ra tab). Thay bằng title plain kèm mã:
    `Chi tiết đề nghị nhập kho: <code>` theo convention "Chi tiết <đối tượng>: <mã>".
- Verify Playwright (127.0.0.1:3000): List="Danh sách đề nghị nhập kho" · Create="Lập đề nghị nhập kho"
  · Detail="Chi tiết đề nghị nhập kho: PDNNK-08539" (sạch, không HTML) · Edit="Sửa đề nghị nhập kho". ĐẠT.
File LF. CHƯA commit/push (chờ user yêu cầu).
Bước tiếp theo: chờ user chốt commit.
Blocked: không

### Checkpoint — Đồng bộ header chi tiết kèm mã phiếu (2026-10-09)
Vừa hoàn thành: `_id/index.vue` `pageTitle` ghép mã theo convention "Chi tiết <đối tượng>: <mã>"
(trước: chỉ "Chi tiết đề nghị nhập kho"). Dùng `this.detail.code`, giữ badge trạng thái qua buildStatusTitle.
Verify Playwright: header trong app = "Chi tiết đề nghị nhập kho: PDNNK-08539" + badge; tab = plain cùng chuỗi. ĐẠT.
File LF. CHƯA commit/push.
Blocked: không

### Checkpoint — Chuẩn hoá popup Hủy đề nghị + Không duyệt (2026-10-09)
Vừa hoàn thành: sửa 2 popup theo skill button-convention (màu · icon · thứ tự nút).
- `warehouse-export-requests/_id/index.vue` `confirmCancel()`: GỠ `$bvModal.msgBoxConfirm` (popup
  bootstrap mặc định sai kiểu) → dùng `$confirm()` (render `base-confirm-modal` dùng chung).
  Kết quả: "Hủy đề nghị" đỏ (#dc2626) + icon xoá ở TRÁI, "Đóng" tertiary + icon mũi tên ở PHẢI.
  Thêm `textClose: 'Đóng'` (mặc định component là "Hủy" → trùng với "Hủy đề nghị", gây rối).
- `warehouse-export-requests/index.vue` `confirmCancel()`: thêm `textClose: 'Đóng'` cho đồng bộ
  (cùng popup, trước đó nút đóng hiện "Hủy").
- `bill-income-requests/components/BillIncomeRequestForm.vue` popup "Không duyệt phiếu":
  icon + thứ tự nút (Không duyệt đỏ TRÁI, Đóng PHẢI) ĐÃ đúng sẵn. Sửa:
  - dòng mã phiếu subtitle `.text-muted` (hrm-client ép đỏ #dc3545 → user tưởng lỗi) → xám #6b7280.
  - typo `::rows="3"` → `:rows="3"` trên V2BaseTextarea.
- Verify Playwright (127.0.0.1:3000): chụp cả 2 popup — màu/icon/thứ tự ĐẠT; subtitle bill-income
  color computed = rgb(107,114,128). ĐẠT.
File LF. CHƯA commit/push (chờ user yêu cầu).
Bước tiếp theo: chờ user chốt commit.
Blocked: không
