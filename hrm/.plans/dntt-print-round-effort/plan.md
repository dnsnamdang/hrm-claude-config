# Plan — Mẫu in ĐNTT làm tròn số công

## Phase 1 — Fix hiển thị mẫu in

- [x] Điều tra nguồn số công lệch (so sánh `WrAssignTaskList.vue` / `PrintTab.vue` với `_id/print.vue`)
- [x] Viết SQL tra `wr_assign_tasks.summary` trên prod, xác nhận DB lưu sẵn `10.129999999999999`
- [x] FE: thêm `| formatNumber` cho 3 dòng công trong `pages/assign/payment_business_request/_id/print.vue`
      (Tổng định mức công / Tổng công khoán phụ / Tổng công khoán — dòng 256, 264, 272)
- [x] FE: thêm `| formatNumber` cho các cột số ngày/đêm cùng rủi ro (dòng 171, 178, 185, 200, 216)
- [x] FE: đồng bộ tab **In** (`components/PrintTab.vue`) — 3 cột số ngày công tác phí cũng thiếu filter (dòng 187, 194, 201)
- [x] Kiểm `git diff --stat` = 8 insertions / 8 deletions, file giữ nguyên CRLF
- [ ] User verify trên môi trường thật với ĐNTT của PGV `TPSG.PGV.2026016101`

### Checkpoint — 09/09/2026
Vừa hoàn thành: sửa 8 dòng ở `_id/print.vue`, khôi phục CRLF sau khi `sed` phá line ending.
Đang làm dở: không có.
Bước tiếp theo: user mở mẫu in ĐNTT của PGV TPSG.PGV.2026016101 xác nhận hiện 10.13.
Blocked:

### Checkpoint — 09/09/2026 (bổ sung)
Vừa hoàn thành: rà toàn bộ `pages/assign` tìm binding số công/ngày thiếu `formatNumber`; sửa tiếp 3 dòng ở `components/PrintTab.vue` (tab In) cho khớp `_id/print.vue`.
Đang làm dở: không có.
Bước tiếp theo: user verify. Ngoài phạm vi đợt này — màn **chi tiết PGV** `pages/assign/assign_tasks/_id/show.vue` có ~19 chỗ in thẳng `rate_effort` / `sum_rate_effort_*` không qua filter, cùng nguồn `summary` nên cũng sẽ lộ đuôi float; `assign_tasks/index.vue:147` dùng `.toFixed(2)` (khác chuẩn, không có dấu phân cách nghìn). Chờ user quyết định có sửa không.
Blocked:
