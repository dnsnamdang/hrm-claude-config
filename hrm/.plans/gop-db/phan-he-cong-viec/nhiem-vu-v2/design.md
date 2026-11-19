# Design — Nhiệm vụ v2 (web panel + app NV2) · phân hệ Công việc

> Folder con của `.plans/gop-db/phan-he-cong-viec/`. Tạo 08/11/2026.
> Nguồn thiết kế đã chốt:
> - **Web:** `gop-db/phan-he-cong-viec/gd0-mockup/screens/03-phong-nhiem-vu.html` + `_build/td.js` (U20–U21, U27, U32–U34, U39) — panel trượt phải thay `CreateTaskModal` + `ImportResultModal`.
> - **App:** `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen` nhóm ⑤…⑩ — NV2-01…NV2-37 (bảng màn: `.plans/app-cong-viec-nhiem-vu-van-de/design.md` mục "Đợt 2").

## Quyết định đã chốt (08/11/2026)

| # | Chốt |
|---|---|
| N1 | Panel web mới **thay toàn bộ 20 chỗ** đang gọi `CreateTaskModal` / `ImportResultModal`; xoá hẳn 2 popup cũ. Panel giữ đúng API công khai cũ (`create(defaults)`, `edit(task, commentId)`, `view(task, commentId, options)`, `open(...)` của nhập kết quả; sự kiện `saved` / `reload`) ⇒ chỗ gọi chỉ đổi import. |
| N2 | **Đề nghị gia hạn làm luôn** (bảng mới + API + thông báo + web + app). |
| N3 | **Thêm API PATCH sửa 1 trường** (kiểm `canEdit`, ghi lịch sử) **+ vá PUT**: kiểm `canEdit`, `POST` chỉ nhận trạng thái Nháp/2/3/4, `start_date` trống ⇒ BE điền ngày giao, xoá được giá trị về rỗng. |
| N4 | **Bỏ qua Không gian / Dự án-Nhóm / gom nhóm theo không gian** (thuộc GĐ1). Form giữ khối "Gắn với" như hiện tại: Giải pháp → Dự án, Hạng mục, Meeting. |
| N5 | (08/11, Phase 2) Footer form Tạo theo **skill button-convention**: [Lưu nháp] [Giao việc] [Giao và tiếp tục] [Hủy] (mockup ghi "Giao & tạo tiếp", "Huỷ", Lưu nháp đứng thứ 3 — lệch skill). |
| N6 | (08/11) Nút 👁 Theo dõi ở header panel: **thêm API** `POST assign/tasks/{task}/watch` — ai mở được nhiệm vụ cũng tự theo dõi / bỏ theo dõi chính mình, ghi lịch sử. |
| N7 | (08/11) Tạo ở trạng thái Đang thực hiện (4) **chỉ khi tự giao cho mình** — chặn cả API (422) lẫn form (công tắc "Bắt đầu ngay" chỉ hiện khi người làm là mình). |
| N8 | (08/11) Rà theo mockup: chỗ nào mockup lệch V2Base thì **giữ V2Base** (user chốt sau khi tự rà nút) — nút nguy hiểm nền đỏ, `V2BaseIconButton` có viền, tab `V2BaseTabNavigation`, `V2BaseFile` thanh dài, `V2BaseQuickAddButton` xanh lá; ô nhập checklist `V2BaseInput`, trạng thái nhiệm vụ con `V2BaseBadge`. Chỉ đè kiểu trong panel khi user yêu cầu riêng (chip ưu tiên). |

Kế thừa từ hồ sơ app (không hỏi lại): U27 (bỏ Đơn giản/Nâng cao), U28 (3 tab + 💬 riêng), U29 (chạm trường → sửa 1 trường, chỉ người giao), U31b (công tắc Cần duyệt triển khai + Bắt đầu ngay), U32 (chip ưu tiên màu BE), U33 (hạn mặc định 17:30), U34 (Thiết lập, bỏ KPI), U39 (Ngày bắt đầu không bắt buộc). Web **giữ Lặp lại + Liên kết nhiệm vụ** và nút "Giao & tạo tiếp" riêng; app không có Lặp lại (chỉ dòng đọc), không có Liên kết (U4/U5).

## Phạm vi theo repo

| Repo · nhánh | Việc |
|---|---|
| `hrm-api` · `gop_db` | vá PUT/POST, PATCH 1 trường, đề nghị gia hạn (migration mới), cờ quyền mới trong DetailTaskResource |
| `hrm-client` · `gop_db` | `TaskPanel` (xem 4 tab: Chi tiết · Kết quả & tiến độ · Bình luận · Lịch sử; form Tạo/Sửa; Báo kết quả; Cập nhật tiến độ; đổi hạn / đề nghị gia hạn) → thay 20 chỗ gọi |
| `TPE_APP` · `develop` | NV2-01…37 trên nền `ui/work/task/*` đã có (trừ phần Không gian) |

## Đề nghị gia hạn — thiết kế dữ liệu (đề xuất, chốt khi viết migration)

Bảng `task_extension_requests`: `id, task_id, requested_by, old_due_date, old_due_time, new_due_date, new_due_time, reason (text, bắt buộc), status (1 chờ · 2 đồng ý · 3 từ chối · 4 huỷ), decided_by, decided_at, reject_reason, timestamps`. Index `(task_id, status)`.
Luật: chỉ người làm gửi; 1 đề nghị chờ / nhiệm vụ; chỉ người giao (`canEdit`) quyết; đồng ý ⇒ cập nhật hạn + ghi lịch sử "đổi hạn theo đề nghị"; thông báo cho người giao khi gửi, cho người làm khi quyết. Không áp cho trạng thái Nháp / Hoàn thành / Huỷ.

## Rủi ro đã biết
- 20 chỗ gọi khác ngữ cảnh (modal lồng modal ở PendingApproval/TaskUpcoming; z-index panel trong `b-modal`) — kiểm Playwright từng chỗ.
- App gọi API local `gop_db`; một số API meeting của app chỉ có trên `develop` ([[hrm-api-develop-di-truoc-gop-db]]) — phần Nhiệm vụ không phụ thuộc.

## Quyết định Phase 3 (app, 08/11/2026)
- N9: Danh sách app bỏ 4 nút icon vai trò → nhóm "Vai trò của tôi" trong bảng lọc; menu phạm vi Tất cả · Của tôi ·
  Quá hạn · Chờ tôi duyệt (BE thêm `overdue=1`).
- N10: "Cách xem" lưu `human/filter-customizations` bảng `tasks_view`, dạng `{key,isVisible}` (`group:` / `sort:` /
  `field:`) vì request bắt buộc khuôn đó — không thêm API.
- N11: Luật L2 (nộp trước hạn không tính quá hạn) tính ở app cho dòng + số nhóm; số "n quá hạn" đầu danh sách vẫn của BE.
- N12: Nút hành động nhanh trên dòng = `TaskResource.quick_action` (1 bước tiến tới theo vai trò, không gọi hasAnyResult).
- N13: ~~Dòng hệ thống trong luồng bình luận~~ — 08/11 user chốt BỎ (trùng tab Lịch sử): luồng bình luận chỉ có
  bình luận người dùng; đã gỡ BE (`system_events`), web `CommentThread.vue`, app `task_comments_page.dart`, e2e ca 7,
  và sửa ghi chú + xoá dòng hệ thống trong Pen NV2-12.
- N14: Form app không gửi `recurring` / `linked` (U30) để BE giữ nguyên; Cập nhật tiến độ tự cộng giờ hôm nay vào
  `actual_hours` (BE không cộng).
