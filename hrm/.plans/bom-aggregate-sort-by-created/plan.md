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

## Testcase
- [x] Viết 16 testcase (TC_15.001→016) cho task #10564 → `.plans/bom-aggregate-sort-by-created/testcase-issue-10564.csv` (+ script `.py`), đã chèn vào Google Sheet `Testcase _Quản lý dự án` tab `22.1 BOM list update` mục "XV. TỔNG HỢP BOM — SẮP XẾP..." (dòng 167–183)
- [x] 24/09/2026: Viết lại 19 testcase (TC-BOM-SORT-01→19) theo khuôn khối UPDATE, chèn vào Google Sheet `Testcase _Quản lý dự án` tab `Update_3107_BomList` (gid 1896896388) dòng 231–250 "UPDATE TESTCASE 24/09- Task: …/issues/10564" — script `gen_testcase_update_3107.py`. (Bộ TC_15 cũ không thấy trong tab 22.1 nên thay bằng bộ này.)

## Phản hồi #8 Redmine #10564 (2026-10-17, nhánh develop)
TPE: gộp BOM con có nhóm trùng tên ("Thiết bị mạng" ở BL-A và BL-C) → 2 nhóm phải TÁCH RIÊNG, xếp theo thời gian tạo BOM con, KHÔNG gộp thành 1. User chốt chỉ xử lý đúng ý này (không đụng cây nhóm 2 cấp).
- [x] `BomBuilderEditor.vue → applySubBomSelection()`: bỏ đoạn gộp nhóm theo tên — mỗi nhóm của BOM con là 1 nhóm mới, sort_order nối tiếp theo thứ tự BOM con (cũ → mới)
- [x] Test: 3 BOM con có nhóm trùng tên → Gộp → thứ tự nhóm A1, B1, C1 → Lưu → mở lại vẫn đúng
  - Kết quả 17/10 (local, BOM tổng hợp 18 dự án 110; tạm đưa BOM 15 sang status 5 để chọn được): tick BOM 16 trước, BOM 15 sau → Gộp → I. Nhóm thiết bị (BOM 15) · II. Nhóm dịch vụ (BOM 15) · III. Nhóm thiết bị (BOM 16), không gộp nhóm trùng tên, đúng thứ tự ngày tạo. Lưu nháp (bằng người tạo id 260) → DB 3 nhóm sort 0/1/2, hàng đúng nhóm; mở lại màn chi tiết đúng thứ tự. Ảnh: test-phan-hoi-8/
  - Đã khôi phục: BOM 18 (nhóm/hàng/liên kết/log từ bản sao lưu), BOM 15 status 1, mật khẩu id 260; không phát sinh log/thông báo khác
- Ghi nhận (chưa sửa, ngoài phạm vi): gộp BOM con chưa giữ cây nhóm 2 cấp (`parent_id`) — nhóm cấp 2 thành cấp 1; Lưu BOM bằng người không phải người tạo → BE 400 "Chỉ người tạo BOM mới được phép sửa" nhưng FE không hiện thông báo
