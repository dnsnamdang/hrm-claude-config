# Plan — Redmine #10845 Từ chối Yêu cầu làm giải pháp + gửi thông báo

Nguồn: http://quanly.dnsmedia.vn/issues/10845 — nhánh `tpe-develop-assign`.

Chốt với user trước khi làm:
- **Phạm vi màn**: chỉ làm màn (1) Phê duyệt YCGP và (3) Chi tiết YCGP. Màn (2) `my-job > tab Chờ duyệt` hiện là danh sách RỖNG hardcode (`approvals = []`, chưa có API) → để nguyên, ghi chú lại cho TPE.
- **Quyền**: dùng lại quyền sẵn có `Tiếp nhận yêu cầu làm giải pháp` (không tạo quyền mới).
- **Thông báo**: theo convention team (`.claude/skills/notification-convention`), không theo nguyên văn mẫu trong task — `[YCG] Từ chối: <b>{Tên yêu cầu}</b>. Lý do: {lý do}`, tên ≤ 50 ký tự, tổng ≤ 120, deep-link kèm ID.

## BE
- [x] Migration `2026_08_15_110000_...`: `request_solutions` thêm `reject_reason`, `rejected_by`, `rejected_at` — đã chạy local
- [x] `RequestSolutionRejectRequest` — `reason_deny` bắt buộc, max 1000, message tiếng Việt
- [x] `RequestSolutionService::reject()` — set status Từ chối + lưu lý do/người/thời điểm + `responded_date`, đồng bộ dự án về "Thu thập thông tin dự án"
- [x] `RequestSolutionController::reject()` — `lockForUpdate` chống double-submit (409 nếu phiếu đã xử lý), gửi thông báo ngoài transaction
- [x] Route `PUT /{requestSolution}/reject` + middleware `checkPermission:Tiếp nhận yêu cầu làm giải pháp`
- [x] `RequestSolution::isCanReject()` — 1 nguồn điều kiện (uỷ quyền sang `isCanReceive`), dùng cho cả 2 màn
- [x] Resource danh sách **và** resource chi tiết trả `reject_reason`, `rejected_at`, `is_can_reject`
  ⚠️ `DetailRequestSolutionResource` extends `ApiResource` (KHÔNG extends resource danh sách) → phải khai lại field, không kế thừa được

## FE
- [x] `pending.vue` — nút Từ chối ở cột Hành động, ẩn hẳn khi `is_can_reject = false`
- [x] `_id/index.vue` — nút Từ chối ở `V2Footer #custom-actions`, cùng cờ `is_can_reject`; sau khi từ chối nạp lại cả form con để hiện ngay trạng thái + lý do
- [x] Dùng component chung `components/modal/V2BaseRejectApproveModal.vue` (không dựng popup mới)
- [x] `RequestTab.vue` — hiện Lý do từ chối (chỉ đọc) khi phiếu đã bị từ chối

## Kiểm thử — BE 20/20 pass (`scratchpad/test_10845.php`, chạy trong transaction + rollback) + UI end-to-end
- [x] AC1: nhân viên không có quyền → `is_can_reject = false` ở cả 2 resource ⇒ nút ẩn hẳn; route còn chặn thêm bằng middleware `checkPermission`
- [x] AC2: có quyền → nút hiện ở cả 2 màn; bấm → popup có ô Lý do bắt buộc; để trống + Đồng ý → popup giữ nguyên, lỗi inline "Vui lòng nhập lý do từ chối"
- [x] AC3: nhập lý do + Đồng ý → YCGP #12 và #10 chuyển "Từ chối", lưu đúng lý do + người + thời điểm
- [x] AC4: dự án 105 và 29 đều về trạng thái 2 "Thu thập thông tin dự án"
- [x] AC5: thông báo gửi đúng người tạo (`employee_info` 6 và 15), nội dung `[YCG] Từ chối: <b>{tên}</b>. Lý do: …`, tên cắt 50 ký tự, tổng ≤ 120, deep-link `/assign/request-solution/{id}`
- [x] Validate độ dài lý do > 1000 ký tự → chặn

## Kiểm thử vòng 2 — case mép (17/17 pass, `scratchpad/test_10845b.php`)
- [x] Lý do toàn khoảng trắng → 422 (TrimStrings + rule required)
- [x] Từ chối 2 lần → lần 2 trả **409**; Tiếp nhận phiếu đã từ chối → **409**
- [x] Phiếu Nháp / Đã tiếp nhận / Đang thực hiện → `is_can_reject = false`
- [x] Phiếu của phòng KHÔNG do mình quản lý → `is_can_reject = false`
- [x] Từ chối không phá dữ liệu khác (tiêu đề, ghi chú, giai đoạn dự án #11016, dự án gắn phiếu) và có ghi `responded_date`
- [x] Dự án đang ở trạng thái cao hơn (Đã duyệt giải pháp) vẫn bị kéo về "Thu thập thông tin dự án"
- [x] Phiếu trỏ tới dự án không tồn tại → không văng lỗi, phiếu vẫn chuyển Từ chối
- [x] Regression luồng Tiếp nhận vẫn chạy đúng, không ghi nhầm lý do từ chối

## Kiểm thử qua HTTP thật
- [x] 422 khi thiếu lý do / toàn khoảng trắng / > 1000 ký tự (message tiếng Việt đúng)
- [x] 401 khi không có token
- [x] **403 khi tài khoản không có quyền** (token thật của NV id 25) — AC1 được chặn ở cả FE lẫn BE
- [x] 200 khi hợp lệ, response trả `status_text = "Từ chối"`, `is_can_reject = false`
- [x] 409 double-submit

## Hiển thị thông báo (phát hiện + xử lý thêm)
- [x] Màn `/timesheet/notifications` và dropdown chuông `AssignMenu.vue` render title bằng `{{ }}` ⇒ thẻ `<b>` hiện thành **text thô**. Đã đổi 2 chỗ sang `v-html` (đúng như `BasicSubsystem.vue` vốn làm) — user đã đồng ý vì là file dùng chung.
- [x] BE `htmlspecialchars` tên phiếu + lý do trước khi bọc `<b>` — chặn XSS qua tên phiếu (đã thử `<img src=x onerror=...>` → bị escape)
- [x] Kiểm tra lại trên UI: tên đối tượng in đậm thật, không còn thẻ thô, các thông báo cũ (Meeting…) cũng hiển thị đúng

## Chưa test được (nêu rõ để không hiểu nhầm là đã phủ)
- Đăng nhập UI bằng tài khoản KHÔNG có quyền (không có mật khẩu tài khoản đó) → thay bằng chứng minh 2 lớp: resource trả `is_can_reject = false` + API trả 403
- Chỉ chạy trên môi trường local (:3000 ↔ :8000), chưa chạy trên dev-hrm.eteksofts.com
- Chưa kiểm push/socket realtime, chỉ kiểm bản ghi thông báo + hiển thị ở danh sách và dropdown chuông

### Checkpoint — 2026-08-15
Vừa hoàn thành: toàn bộ BE + FE #10845, test BE 20/20 và test UI AC1–AC5.
Lỗi đã bắt được khi test: resource chi tiết thiếu `is_can_reject` (nút không hiện ở màn chi tiết) → đã sửa; form con không tự nạp lại sau khi từ chối → đã gọi `loadRequestSolution()`.
Bước tiếp theo: chờ user xác nhận chuyển Redmine sang "Đang tiến hành"/"Code xong chờ test" và dọn dữ liệu test.
Blocked:
