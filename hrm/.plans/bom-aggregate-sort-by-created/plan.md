# Plan — Tổng hợp BOM: sắp xếp hàng hoá/dịch vụ theo created_at BOM thành phần (tăng dần)

Màn: QLDA TKT → Tạo BOM list tổng hợp → bước "Tổng hợp bom".

Yêu cầu: hàng hoá + dịch vụ gộp từ các BOM thành phần phải sắp theo NGÀY TẠO của BOM thành phần (cũ → mới), giữ đúng cả trên UI và khi lưu DB.

## Truy vết
- Gộp ở FE `BomBuilderEditor.applySubBomSelection`: fetch từng BOM con (`assign/bom-lists/{id}`) theo thứ tự user CHỌN (Promise.all giữ thứ tự selectedBomIds) rồi forEach đẩy products/service_items vào allGroups/allServiceItems → thứ tự hiện tại = thứ tự chọn, KHÔNG theo created_at.
- Lưu DB: `buildSavePayload` gửi `groups` theo thứ tự mảng `this.groups`; BE `syncProducts` insert theo thứ tự payload; `products()` không orderBy → đọc lại theo id (thứ tự chèn). ⇒ chỉ cần FE sort đúng là DB + UI đều đúng.
- `created_at` API `bom-lists/{id}` trả dạng `d/m/Y H:i:s` (Human Helper) → parse khi sort; tiebreaker theo `id`.

## Phase 1 — FE
- [x] `applySubBomSelection`: sau khi fetch `details`, sort theo created_at BOM con tăng dần (parse d/m/Y H:i:s, tiebreaker id) TRƯỚC các vòng forEach gộp. Là nơi DUY NHẤT gọi mergeSubBomGroups (trigger @apply nút "Tổng hợp").

## Verify
- [x] Playwright drive applySubBomSelection thật với stub 3 BOM con created_at lộn xộn, chọn [3,1,2] (mới→cũ→giữa):
  - productOrder = [A-OLDEST, B-MIDDLE, C-NEWEST] (01/07→03/07→05/07) ✓ AC2
  - serviceOrder = [SVC-A, SVC-B, SVC-C] ✓ (dịch vụ cũng đúng)
- [x] DB: code-trace — buildSavePayload gửi groups theo this.groups (đã sort) → BE syncProducts insert theo thứ tự payload → products() không orderBy → đọc lại theo id/insertion ⇒ DB giữ đúng thứ tự created_at.

### Checkpoint — 2026-07-09
Vừa hoàn thành: CODE DONE + VERIFIED. FE-only, không migration/BE/git.
File: hrm-client BomBuilderEditor.vue applySubBomSelection (+ sort details theo created_at)

### Checkpoint 2 — 2026-07-09 (FULL E2E TEST theo yêu cầu user)
Tạo 3 BOM thành phần THẬT với created_at NGƯỢC thứ tự id (id4=Jul1 OLDEST, id5=Jul5 NEWEST, id6=Jul3 MIDDLE) → để phân biệt sort theo created_at vs id.
- UI (REAL API, không stub): chọn lộn xộn ids [5,4,6] → applySubBomSelection → productOrder=[OLDEST-Jul1, MIDDLE-Jul3, NEWEST-Jul5] = created_at tăng dần (không theo id/thứ tự chọn) ✓ AC2. Vì id≠created_at, chứng minh sort đúng theo created_at.
- DB (REAL BE): tạo BOM tổng hợp throwaway, gọi thật BomListService::syncProducts với payload sort [OLDEST,MIDDLE,NEWEST] → đọc lại qua products() (không orderBy) = ["OLDEST-Jul1","MIDDLE-Jul3","NEWEST-Jul5"] → DB giữ đúng thứ tự ✓
- Dọn sạch: xoá 3 BOM test + throwaway; còn đúng 3 BOM gốc, 0 sót.
KẾT LUẬN: created_at ASC đúng ở cả UI (real API) lẫn DB (real BE persistence).
Đang làm dở: không
Bước tiếp: (tuỳ chọn) user verify trên browser bằng thao tác tay đầy đủ
Blocked:
