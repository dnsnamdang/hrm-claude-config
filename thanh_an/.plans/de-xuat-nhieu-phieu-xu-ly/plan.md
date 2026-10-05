# 1 đề xuất cung ứng → nhiều phiếu xử lý

**Phụ trách:** @khoipv
**Ngày bắt đầu:** 24/09/2026
**Loại:** sửa logic vòng đời trạng thái (bounded)

## Mục tiêu

Đề xuất cung ứng đang bị lật sang "Đã xử lý" (9) ngay khi có 1 PXL → rơi khỏi inbox →
thực tế chỉ lập được 1 phiếu xử lý. Mở lại để nhiều người trong nhóm quyền
`Xử lý cung ứng hàng hóa` cùng lập PXL trên 1 đề xuất.

## Quyết định đã chốt với user

- Thêm **4 Đang xử lý** (có ≥1 PXL, chưa đóng) và **5 Bị trả lại**.
- Đóng phiếu: **đủ SL tự đóng** (giữ cơ chế cũ) HOẶC **Xác nhận hoàn thành** thủ công
  (ghi chú tùy chọn). Đóng tay ghi `closed_at` → xóa PXL sau đó KHÔNG mở lại.
- **Từ chối** đổi nghĩa: chỉ **ẩn khỏi inbox của riêng người bấm**, không lý do,
  không đổi trạng thái phiếu. Trạng thái 8 (Từ chối xử lý) ngừng dùng, giữ nhãn cho data cũ.
- **Trả lại người tạo**: chỉ khi CHƯA có PXL nào, bắt buộc lý do → status 5, người tạo
  sửa & gửi lại (gửi lại thì xóa sạch dấu từ chối cá nhân).
- Không có nút mở lại phiếu đã đóng, không hoàn tác "Không liên quan",
  không báo người tạo khi cả nhóm từ chối.
- `deadStatuses()` giữ nguyên [7, 8] — phiếu Bị trả lại vẫn giữ chỗ SL trên HĐ.

## Phase 1 — Backend

- [x] T1. Migration: bảng `supply_proposal_dismissals` (unique proposal+employee, chỉ index)
      + cột `closed_by` / `closed_at` / `close_note` ở `supply_proposals`
- [x] T2. `SupplyProposal`: hằng STATUS_DANG_XU_LY=4 / STATUS_BI_TRA_LAI=5, STATUSES,
      quan hệ `dismissals()`, accessor `is_can_*`, coi status 5 như Nháp (sửa/xóa/gửi)
- [x] T3. `SupplyProposalService::syncHandledStatus()` viết lại (3 / 4 / 9, bỏ qua khi đã đóng tay)
- [x] T4. `SupplyProposalService::inbox()` lấy status 3+4, loại phiếu user đã dismiss
- [x] T5. `dismiss()` thay `reject()`; thêm `returnToOwner()` + `complete()`; gửi lại xóa dismissals
- [x] T6. Controller + routes: `/dismiss`, `/return`, `/complete`
- [x] T7. Resource: `can_dismiss` / `can_complete` / `can_return` thay `can_reject`
- [x] T8. `SupplyHandlingService::store()` + `update()` chấp nhận đề xuất ở status 3 hoặc 4
- [x] T9. `viewHistory()` trả thêm cờ đã từ chối của từng NV

## Phase 2 — Frontend

- [x] T10. `supply_proposals/constants.js`: 2 trạng thái mới + màu
- [x] T11. `inbox.vue`: 4 nút (Tạo PXL / Không liên quan / Xác nhận hoàn thành / Trả lại) + popup
- [x] T12. `index.vue`: badge + bộ lọc trạng thái mới, phiếu 5 thao tác như Nháp
- [x] T13. `add.vue`: hiện khối lý do khi status = 5
- [x] T14. Popup Lịch sử xem phiếu: cột đánh dấu ai đã bấm "Không liên quan"

## Phase 3 — Kiểm thử

- [x] T15. Tinker trên `thanhan_stag_07052026` (chạy trong transaction rồi rollback, 15/15 case đạt):
      inbox lọc theo người dismiss · dismiss 2 lần không nhân bản · đóng tay rồi xóa PXL không mở lại
      · complete lần 2 báo lỗi · trả lại → gửi lại xóa sạch dismissals · PXL nháp không đổi trạng thái
      · chưa đủ SL → 4 · đủ SL → 9 · xóa PXL → 3 · có PXL thì chặn trả lại
- [ ] T16. User verify UI (⚠️ chạy migration + build lại client + hard refresh)
- [x] T17. Test E2E Playwright — **12/12 pass** trên client :3001 + API :8001, DB `thanhan_stag_07052026`.
      Workspace `dns/e2e/` (Node 24): `auth/auth.setup.js` nạp JWT từ `.env` vào localStorage →
      `.auth/user.json`; POM `pages/SupplyProposalPage.js`; helper `utils/api.js` + `utils/db.js`.
      - `tests/supply/de-xuat-nhieu-phieu-xu-ly.spec.js` (8 case, chỉ đọc): inbox chỉ trả status 3+4 ·
        phiếu đã có PXL vẫn nằm trong hàng đợi với "Đang xử lý" · lưới khớp API · dropdown đủ
        3 thao tác mới · có PXL thì không cho Trả lại · popup Hoàn thành bấm "Không" không đổi gì ·
        popup Trả lại bắt lý do · bộ lọc trạng thái có Đang xử lý / Bị trả lại.
      - `tests/supply/dismiss-flow.spec.js` (1 case có ghi dữ liệu, tự dọn ở afterEach): bấm
        "Không liên quan" → phiếu rời inbox của mình, tổng giảm 1, API không trả nữa,
        **status phiếu giữ nguyên**, đúng 1 dòng `supply_proposal_dismissals`.

## Phase 4 — Ghi nhận đã xem cho thao tác ngoài lưới (25/09/2026)

Vấn đề user phát hiện: bấm "Không liên quan" thẳng ngoài màn danh sách thì popup
Lịch sử xem phiếu vẫn hiện **"Chưa xem"** (dismiss không ghi `supply_proposal_views`).
Chốt: cả 3 thao tác ngoài lưới đều tính là đã xem, giữ nguồn riêng để còn phân biệt.

- [x] T18. `SupplyProposalView`: thêm `SOURCE_DISMISS=3` / `SOURCE_COMPLETE=4` / `SOURCE_RETURN=5`
      + helper `sources()`; `markViewed()` nhận cả 5 nguồn
- [x] T19. `dismiss()` / `complete()` / `returnToOwner()` gọi `markViewed()` với nguồn tương ứng
- [x] T20. Migration đổi comment cột `supply_proposal_views.source` cho đủ 5 nguồn
- [x] T21. FE `constants.js`: `VIEW_SOURCE` thêm 3 nguồn (đồng bộ tài liệu, FE không gọi trực tiếp)
- [x] T22. E2E: sau khi bỏ qua phiếu thì view-history trả `viewed_at` cho chính người đó
- [x] T23. Sửa docblock `markViewed()` (còn ghi "chỉ 2 thao tác") + chạy lại TOÀN BỘ suite E2E
- [x] T24. Sửa 3 case E2E bị đứt khi inbox > 10 phiếu (thiếu `showAllRows()` → phiếu đích ở trang sau)

## Phase 5 — Cột "Phiếu xử lý" ở màn danh sách đề xuất (25/09/2026)

Người tạo đề xuất muốn thấy ngay đề xuất của mình đã được lập những PXL nào mà không phải
mở từng phiếu. API danh sách đã trả sẵn `responses` (đã eager-load `handlings.products`)
nên không phát sinh query mới.
Chốt với user: liệt kê mã PXL trong 1 cột, bấm mã mở phiếu xử lý ở tab mới.

- [x] T25. BE: `buildResponses()` trả thêm `id` của phiếu xử lý (để FE dựng link)
- [x] T26. FE `index.vue`: thêm cột "Phiếu xử lý" — mỗi PXL 1 dòng, chỉ hiện MÃ phiếu
      (user chốt bỏ chú thích "· N dòng"), tooltip người xử lý + ngày lập, rỗng thì "—"
- [x] T27. E2E: case "Màn danh sách hiện mã phiếu xử lý của từng đề xuất" + helper `fetchList()`

## Checkpoint

### Checkpoint — 24/09/2026 (khởi tạo)
Vừa hoàn thành: brainstorming, chốt design với user
Đang làm dở: chưa bắt đầu code
Bước tiếp theo: T1 — migration
Blocked:

### Checkpoint — 24/09/2026 (xong BE + FE + kiểm thử)
Vừa hoàn thành: T1–T15. Đã chạy migration trên `thanhan_stag_07052026`
(2 migration: bảng `supply_proposal_dismissals`, 3 cột `closed_*` + backfill 9 → 4 cho phiếu
chưa phân bổ đủ SL). BE: state machine 3 → 4 → 9, dismiss theo từng người, returnToOwner,
complete, guard của SupplyHandlingService nhận cả status 4. FE: 2 trạng thái mới, 3 nút mới
ở inbox + màn xem, popup dùng chung `ProposalActionModal.vue`, cột "Bỏ qua phiếu" trong popup
Lịch sử xem phiếu. Template + script của 5 file .vue đã compile/parse sạch.
Đang làm dở: không
Bước tiếp theo: T16 — user build lại client (Node 14) + hard refresh rồi verify UI
Blocked:

### Checkpoint — 25/09/2026 (test E2E Playwright)
Vừa hoàn thành: T17 — dựng bộ E2E trong `dns/e2e/` và chạy headed, **12/12 pass** (3.2 phút).
Xác nhận đúng mục tiêu feature: 3 phiếu đang ở status 4 "Đang xử lý" (đã có PXL) VẪN
nằm trong inbox → người khác lập tiếp PXL được. Bảng `supply_proposal_dismissals` sạch
sau khi test tự dọn (COUNT = 0).
Đang làm dở: không
Bước tiếp theo: T16 — user tự verify UI các luồng ghi còn lại (Xác nhận hoàn thành đóng phiếu,
Trả lại người tạo rồi gửi lại, tạo PXL thứ 2 trên cùng 1 đề xuất)
Blocked:

### Checkpoint — 25/09/2026 (Phase 4 xong, full suite xanh)
Vừa hoàn thành: T18–T24. `dismiss()` / `complete()` / `returnToOwner()` đều ghi
`supply_proposal_views` với nguồn riêng (3 / 4 / 5) → người quyết định ngay ngoài lưới không
còn bị popup Lịch sử xem phiếu báo "Chưa xem" nữa.
Kiểm chứng:
- Full suite Playwright **13/13 pass** (3.3 phút, headed).
- E2E dismiss: DB có dòng view `source = 3`, API `/view-history` trả cả `viewed_at` lẫn
  `dismissed_at` cho người vừa bỏ qua.
- Nguồn 4 / 5 (complete / return) kiểm bằng tinker trong transaction + rollback — `markViewed()`
  ghi đúng `source`, không chạy `complete()`/`returnToOwner()` thật để tránh bắn thông báo
  nhầm cho người tạo trên stag.
- Dữ liệu sạch: chạy lại riêng `dismiss-flow.spec.js` không phát sinh thêm dòng nào
  (`supply_proposal_views` nguồn 3/4/5 = 0). Dòng `supply_proposal_dismissals` id=13 còn lại
  là thao tác thật của employee 22 trên stag, KHÔNG phải rác test → giữ nguyên.
Đang làm dở: không
Bước tiếp theo: T16 — user verify UI 3 luồng ghi còn lại (tạo PXL thứ 2 trên cùng 1 đề xuất,
"Xác nhận hoàn thành" đóng phiếu thật, "Trả lại người tạo" → sửa → gửi lại). Chưa tự động hoá
3 luồng này vì chúng đổi trạng thái phiếu thật + bắn thông báo — chờ user chốt có làm không.
Blocked:

### Checkpoint — 25/09/2026 (cột "Phiếu xử lý" ở màn danh sách)
Vừa hoàn thành: T25–T27. Màn `/supply/supply_proposals` có cột "Phiếu xử lý" (đặt ngay sau
cột Trạng thái), liệt kê mã PXL của từng đề xuất, bấm mã mở phiếu xử lý ở tab mới
(`/supply/supply_handlings/add?mode=show&id={id}` — GET phiếu xử lý không chặn quyền nên
người tạo đề xuất xem được). Hover mã ra tooltip "người xử lý · ngày lập".
Không tốn query mới: `index()` đã eager-load `handlings.products`, resource đã trả `responses`.
Kiểm chứng: xem trực tiếp trên browser (DXCU-2026-0027 hiện đủ PXL-2026-0013 + PXL-2026-0014,
phiếu chưa có PXL hiện "—"), link + tooltip đúng.
Đang làm dở: không
Bước tiếp theo: T16 — user verify UI 3 luồng ghi còn lại. LƯU Ý: user yêu cầu TẠM DỪNG chạy
Playwright, chỉ chạy khi user bảo (test đã viết sẵn, để đó).
Blocked:
