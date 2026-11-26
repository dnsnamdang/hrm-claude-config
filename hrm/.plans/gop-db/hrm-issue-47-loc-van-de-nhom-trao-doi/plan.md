# Tab Vấn đề trong Nhóm trao đổi: bổ sung bộ lọc nâng cao (HRM issue #47, ISS-202611-0047) — @cuong61n

Nguồn: vấn đề ISS-202611-0047 trên prod (chị Nguyễn Thị Thu Huyền báo 25/11/2026, từ tin nhắn nhóm trao đổi
"Vấn đề HRM"): danh sách vấn đề trong nhóm trao đổi chỉ có ô tìm + Lọc nhanh, cần lọc theo **người xử lý,
người duyệt đóng, loại vấn đề (lỗi phần mềm…), ngày tạo, người tạo, hạn hoàn thành, trạng thái**.

Màn: Nhóm trao đổi → tab **Vấn đề** (`components/assign/issue/group-list/*`, API `GET assign/workspaces/{id}/issues`).
GĐ34 (`.plans/agent-chat/chat/gd34-tab-van-de/design.md` C3) cố ý bỏ "Lọc nâng cao" ở đợt đầu — nay bổ sung.

## Quyết định
- **Copy đúng khuôn tab Nhiệm vụ cùng nhóm** (`TaskGroupToolbar.vue` nút `Lọc (n)` + popover 2 cột "Lọc nâng cao"
  dùng `V2BaseFloatingField` + `V2BaseFilterFieldControl`; `TaskGroupListView.vue` hàng chip điều kiện đang lọc +
  nút Xoá lọc). Không tự chế kiểu mới, không gộp 2 toolbar (lý do như GĐ34 C4).
- Ô lọc (thứ tự trong popover): Trạng thái · Loại vấn đề · Người xử lý · Người duyệt đóng · Người tạo ·
  Ngày tạo (khoảng) · Hạn xử lý (khoảng). Chọn nhiều cho 5 ô select.
- Nguồn người để chọn: thành viên nhóm (API members có sẵn, tải khi mở popover) + người đang gắn trên các dòng
  (người xử lý / tạo / duyệt có thể ngoài nhóm — Q1 GĐ34). Nhãn `Tên - Mã phòng - Mã NV`.
- Trạng thái / loại vấn đề: hằng FE có sẵn (`Issue::STATUS_DATA` tên ↔ `ISSUE_STATUS`, `ISSUE_TYPE_OPTIONS`).
- Bộ lọc áp cho cả số nhóm, đếm Lọc nhanh và "Xem thêm" (cùng `baseQuery` như ô tìm).

## Task
### BE (hrm-api, nhánh gop_db-main)
- [x] 26/11 `WorkspaceIssueListRequest`: thêm `assignee_ids[] creator_ids[] approver_ids[]` (int, ≤200), `statuses[]`
  (in STATUS_DATA), `issue_types[]` (string ≤50), `due_from/due_to`, `created_from/created_to` (Y-m-d).
- [x] 26/11 `WorkspaceIssueListService::baseQuery`: whereIn 5 mảng + khoảng `due_date` + khoảng `created_at`
  (ngày tạo so theo ngày: `>= from 00:00:00`, `<= to 23:59:59`).
- [x] 26/11 Test `WorkspaceIssueListTest::test_loc_nang_cao` (7 ô, đếm nhóm + quick_counts đi theo lọc).
### FE (hrm-client, nhánh gop_db-main)
- [x] 26/11 `IssueGroupToolbar.vue`: nút Lọc (n) + popover (copy TaskGroupToolbar :39-95), export `EMPTY_FILTERS`.
- [x] 26/11 `IssueGroupListView.vue`: state `filters`, `filterFields`, `peopleOptions`, chips + Xoá lọc, gửi tham số,
  `loadMembers` khi mở popover, emptyText tính cả lọc nâng cao.
- [x] 26/11 `utils/assign/workspaceIssueApi.js`: thêm `members()` (cùng endpoint tab Nhiệm vụ).
### Kiểm
- [x] 26/11 Test BE: `phpunit WorkspaceIssueListTest` 24/24 pass (test mới 28 assertion); template 2 file Vue compile sạch.
- [x] 26/11 User xem UI trên :3002, yêu cầu thêm vạch `|` trước nút Lọc cho giống tab Nhiệm vụ → đã thêm.
- [x] 26/11 Push `origin/gop_db`: api `c83b2f0ef`, client `fb15260f1`. Deploy PROD tpe bằng `~/build_tpe.sh` (nhánh gop_db).
- [ ] Đóng ISS-202611-0047 trên nhóm trao đổi (user tự làm hoặc bảo tôi).

Trạng thái: 26/11/2026 đã push gop_db (api `c83b2f0ef`, client `fb15260f1`), đã deploy PROD tpe 26/11 (build_tpe.sh xong, FE commit fb15260f1 đang chạy). Code làm ở worktree `worktrees/gop_db-*`, bản repo chính `gop_db-main` đã gỡ để tránh trùng.
