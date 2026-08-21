# Plan — Redmine #10841 Hủy yêu cầu làm giải pháp + trả dự án về "Thu thập thông tin"

Nguồn: http://quanly.dnsmedia.vn/issues/10841 — nhánh `tpe-develop-assign`. Cùng họ với [#10845](../redmine-10845-tu-choi-yeu-cau-giai-phap/plan.md) (Từ chối), tái dùng nguyên pattern đó.

Chốt với user:
- **Trạng thái mới** `STATUS_DA_HUY = 5` "Đã hủy" (id 5 và 7 đang trống, DB không có bản ghi nào dùng).
- **Quyền**: KHÔNG tạo quyền mới — *tạm thời chỉ NGƯỜI TẠO yêu cầu được hủy*. (Vế "người được phân quyền hủy" trong task tạm gác; muốn mở rộng sau thì thêm quyền + giới hạn theo phạm vi xem, xem ghi chú cuối file.)
- **Điều kiện trạng thái**: chỉ hủy khi **chưa tiếp nhận** — Nháp (1), Chờ tiếp nhận (2), Yêu cầu bổ sung (9).
- **Thông báo** theo `.claude/skills/notification-convention`: `[YCG] Hủy: <b>{Tên}</b>. Người thực hiện: {tên}` — gửi cho phòng tiếp nhận + người có quyền "Tiếp nhận yêu cầu làm giải pháp" (tái dùng hàm gửi sẵn có).
- "Mở khóa sửa dự án" **không cần code thêm**: FE đã cho sửa khi dự án ở trạng thái Đang tạo / Thu thập thông tin (`ProjectInfoSection.isEditableByProjectStatus`), nên đưa dự án về trạng thái 2 là tự mở.

## BE
- [x] Entity: `STATUS_DA_HUY = 5` + thêm vào `STATUSES` (tên "Đã hủy", màu `#9CA3AF`)
- [x] Migration `2026_08_15_120000_...`: `cancel_reason`, `cancelled_by`, `cancelled_at` — đã chạy local
- [x] `RequestSolution::isCanCancel()` — người tạo + trạng thái chưa tiếp nhận
- [x] `RequestSolutionCancelRequest` — `reason_deny` bắt buộc, max 1000
- [x] `RequestSolutionService::cancel()` — đổi trạng thái, lưu lý do/người/thời điểm, trả dự án về "Thu thập thông tin dự án"
- [x] `RequestSolutionController::cancel()` — `lockForUpdate`; sai người → **403**, sai trạng thái → **409**
- [x] Route `PUT /{requestSolution}/cancel`
- [x] Tách `resolveReceiveDeptNotifyTargets()` (dùng chung với luồng thông báo khi tạo YCGP) + `sendRequestSolutionCancelledNotification()`
- [x] Resource danh sách + chi tiết trả `cancel_reason`, `cancelled_at`, `is_can_cancel`

## FE
- [x] `request-solution/index.vue` — nút Hủy ở cột Hành động (ẩn hẳn khi `is_can_cancel = false`)
- [x] `request-solution/pending.vue` — nút Hủy (cùng cờ)
- [x] `request-solution/_id/index.vue` — nút Hủy ở `V2Footer #custom-actions`, sau khi hủy nạp lại cả form con
- [x] Dùng lại `components/modal/V2BaseRejectApproveModal.vue` (label "Lý do hủy")
- [x] `RequestTab.vue` — hiện Lý do hủy (chỉ đọc) khi phiếu đã hủy

## Kiểm thử — BE 39/39 pass (`scratchpad/test_10841.php`) + HTTP + UI 3 màn
- [x] Trạng thái mới: id 5 không trùng, tên/màu đúng
- [x] AC1: người khác → `is_can_cancel = false`; gọi API bằng token người khác → **403** "Chỉ người tạo yêu cầu mới được hủy"
- [x] Điều kiện trạng thái (8 case): Nháp / Chờ tiếp nhận / Yêu cầu bổ sung → hủy được; Đã tiếp nhận / Đang thực hiện / Đã chốt GP / Từ chối / Đã hủy → không
- [x] AC2: nút hiện ở **cả 3 màn**; bỏ trống lý do → popup giữ nguyên + lỗi inline "Vui lòng nhập lý do hủy"; >1000 ký tự → 422
- [x] AC3: hủy qua UI ở màn danh sách và màn chi tiết → trạng thái "Đã hủy", lý do lưu đúng, lưu người + thời điểm
- [x] AC4: dự án 105 về "Thu thập thông tin dự án"; mở lại `/prospective-projects/105/edit` → các ô nhập mở khoá, có nút Lưu
- [x] Thông báo: gửi đủ 11 người của phòng tiếp nhận, nội dung `[YCG] Hủy: <b>{tên}</b>. Người thực hiện: …`, deep-link kèm ID
- [x] Hủy lần 2 → **409**; danh sách/chi tiết tự cập nhật, nút Hủy biến mất, hiện Lý do hủy
- [x] Không phá dữ liệu khác (lý do từ chối #10845, giai đoạn dự án #11016, tiêu đề)

## Vòng kiểm tra bổ sung (24/24 pass — `scratchpad/test_regression_ycgp.php`)
Phát hiện + sửa thêm 1 lỗi:
- [x] **Bộ lọc "Tiến trình YC" hardcode danh sách trạng thái** ⇒ thiếu "Đã hủy", và "Từ chối" (#10845) còn đang bị comment ⇒ 2 trạng thái mới không lọc được. Đã bổ sung vào cả `statusOptions` lẫn `progressOptions` của `request-solution/index.vue`, kiểm lại trên UI: lọc "Đã hủy" ra đúng 1 phiếu.
- [x] **Regression sau refactor** `sendRequestSolutionNotification()` (đã tách `resolveReceiveDeptNotifyTargets`): gọi lại hàm gốc → vẫn gửi được thông báo cho người nhận (số bản ghi tăng đúng 1)
- [x] Regression 3 nghiệp vụ trên cùng 1 phiếu: Tiếp nhận → Từ chối → Hủy, không nghiệp vụ nào ghi đè trường của nghiệp vụ kia (`reject_reason` và `cancel_reason` độc lập)
- [x] Bảng trạng thái: 10 trạng thái cũ + mới đều trả đúng tên, id lạ → "Không xác định"
- [x] Export Excel dùng `getStatusName()` (không hardcode) ⇒ tự có "Đã hủy", không phải sửa

## AC1 — đã kiểm TRỰC TIẾP trên giao diện bằng tài khoản thứ hai
Đổi mật khẩu tạm NV id 25 (`cannt.kd1@tanphat.com` — không phải người tạo, không có quyền tiếp nhận) trên DB local, test xong **đã trả lại hash cũ** (xác nhận mật khẩu tạm không còn dùng được).
- [x] Màn **chi tiết** phiếu đang Chờ tiếp nhận: chỉ còn nút "Quay lại" — không có Hủy / Từ chối / Tiếp nhận
- [x] Màn **danh sách YCGP**: không thấy phiếu của người khác, không có nút Hủy ở bất kỳ đâu
- [x] Màn **Phê duyệt** (`/pending`): bị chặn, đá về trang 404
- [x] Gọi thẳng API bằng token tài khoản đó: `cancel` → **403** "Chỉ người tạo yêu cầu mới được hủy"; `reject` → **403**; `receive` → **403**; trạng thái phiếu **không đổi** (vẫn = 2, lý do vẫn NULL)

## Chưa test được
- Chỉ chạy local, chưa chạy trên dev-hrm.eteksofts.com; chưa kiểm push/socket realtime

### Checkpoint — 2026-08-15
Vừa hoàn thành: toàn bộ BE + FE #10841 và test BE/HTTP/UI.
Bước tiếp theo: chờ user xác nhận dọn dữ liệu test và chuyển Redmine sang "Code xong chờ test".
Blocked:

## Ghi chú để mở rộng sau
Nếu TPE muốn "người được phân quyền hủy" (không chỉ người tạo): thêm quyền `Hủy yêu cầu làm giải pháp` (id 1011 đang trống) và gate = `là người tạo OR (có quyền AND phiếu nằm trong phạm vi xem theo cấp)` — tái dùng `checkPermissionListWithColumn`, KHÔNG để quyền hủy phẳng toàn hệ thống.
