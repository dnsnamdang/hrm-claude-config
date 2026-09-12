# Design (tóm tắt) — Báo cáo Kết quả meeting theo thị trường

> Spec đầy đủ: `docs/superpowers/specs/2026-08-16-meeting-by-market-design.md`
> Branch: `meeting-schedule` (api + client) · @dnsnamdang · 2026-08-16
> Phase 13 (06/09/2026): nhánh `bao_cao_meeting_thi_truong` tách từ `origin/tpe`, đã merge về `tpe` **local, chưa push**.

## Mục tiêu
Báo cáo **độc lập** liệt kê meeting **có gắn khách hàng**, nhóm **Thị trường (Tỉnh của KH) → Khách hàng → Meeting**, bám mockup tab 3 (`.plans/gop-db/ke-hoach-phat-trien-thi-truong/ke-hoach-phat-trien-thi-truong-mockup-meeting.html`). Tách khỏi màn Lịch meeting / Todo.

## Quyết định đã chốt
- **Vị trí:** trang mới `pages/assign/report/meeting-by-market/` (index + print + components), layout `default-sidebar`, thêm menu Báo cáo. BE: route group `assign/report/meeting-by-market` + Controller + Service riêng (không nhồi ReportController).
- **Phạm vi meeting:** chỉ meeting có `customer_id`; trạng thái Lên lịch/Chốt lịch/Hoàn thành/Hủy (bỏ Đang tạo).
- **Thị trường = Tỉnh của KH:** `meeting.customer_id → ERP customers.province_id → provinces.name` (qua `mysql2`, batch 2 connection, không join xuyên DB). KH không tỉnh → "Chưa xác định thị trường".
- **Cấu trúc bảng (Phase 13, 06/09/2026 — thay bản 13 cột rowspan ban đầu):** Thị trường và Khách hàng KHÔNG còn là cột, mà là **2 cấp DÒNG CHA** trải hết bề ngang; đánh số ở cột STT riêng `I` / `1` / `1.1` (không dấu `/`), số KH đếm lại theo từng thị trường. Bảng = **STT + 12 cột**: Tên meeting (link → panel chi tiết) · Loại · Thời gian · Địa điểm · Người chủ trì · **Phòng chủ trì** · TP công ty · TP KH · Trạng thái · Biên bản/Lý do huỷ · Dự án TKT · Phiếu công tác/Chấm công.
  Lý do đổi: bản cũ gộp bằng `rowspan` (Hà Nội `rowspan=10`) nên 9 dòng dưới không có ô thị trường, cuộn xuống là mất ngữ cảnh.
- **Style:** port khối `.rsum-tb` của báo cáo CSKH tiềm năng (`potential-customer-care/components/CareTrackingTable.vue`) — thead teal uppercase, 2 thanh cuộn mảnh trên+dưới, caret nút SVG, `white-space: nowrap` (giữ nguyên, đừng lược — bỏ đi là cột Địa điểm bị bóp còn ~70px). Nhãn nhóm `position: sticky; left` để cuộn ngang vẫn thấy thị trường.
- **Cột thành phần:** chỉ hiện 1 người + chip `+N` bấm được → popup `MeetingMembersModal` (không gọi thêm API).
- **Chi tiết meeting:** panel `MeetingDetailDrawer` (dùng lại của màn Lịch của tôi) — KHÔNG mở tab mới nữa (bỏ hành vi Phase 11).
- **Xem biên bản:** popup xem trước bản in dùng chung `reportPrintPreviewMixin` + `ReportPrintPreviewModal`; đã xoá `MeetingMinutesModal.vue` tự chế.
- **Summary:** 4 khối trên **1 hàng ngang, tràn thì cuộn**; item trong từng khối vẫn chia cột. Có thêm khối **Theo phòng chủ trì** (`by_host_department`).
- **Bộ lọc:** Kỳ + cascade Công ty→Phòng ban→Bộ phận→Nhân viên (`V2BaseCompanyDepartmentFilter`) + Thị trường + Trạng thái + Loại meeting + Xuất Excel.
- **Phân quyền fail-closed:** 3 quyền mới (tổng công ty/công ty/phòng ban) trong `PermissionsTableSeeder`; không quyền → chỉ meeting mình tạo/mình dự. FE cờ quyền mặc định `false` (KHÔNG `|| true`). Route KHÔNG chặn cứng — scoping trong service để giữ fallback "của chính mình".
- **Popup:** Biên bản từ `MeetingReport` (content/solution/proposer/executor/deadline + conclusion); Chấm công GPS từ `timesheets` (job_type=`new_business_trip`, job_id=assign_request.id).

## Phụ thuộc bắt buộc (đã chốt)
- Thêm cột `assign_requests.meeting_id` (nullable) + sửa `AssignBusinessForm.vue` & BE store để **lưu meeting_id** khi tạo phiếu công tác từ meeting. Không hồi tố phiếu cũ.

## Lưu ý
- Bug tham chiếu: `meeting-by-projects/index.vue:501-504` dùng `hasAPermission(...) || true` (fail-open) — KHÔNG copy.
- Nhánh `meeting-schedule` (không phải gop_db) → `mysql2` dùng bình thường.

## Cảnh báo môi trường (Phase 13)
- Worktree `hrm-api`: **KHÔNG symlink `vendor/`** — autoload resolve `$baseDir` qua symlink về checkout chính, sửa BE trong worktree vô tác dụng mà không báo lỗi. Dùng `cp -Rc`.
- `HRM/e2e/` không phải git repo → 17 ca `meeting-by-market-grouping.spec.ts` không theo code lên git.
- Spec phải chạy `--workers=1`; token `.auth/user.json` hết hạn ~1 ngày, làm mới bằng `--project=setup --no-deps`.
- File Excel (`MeetingByMarketExport.php`) **chưa cập nhật theo Phase 13**: vẫn dạng cột phẳng cũ và thiếu cột "Phòng chủ trì".
