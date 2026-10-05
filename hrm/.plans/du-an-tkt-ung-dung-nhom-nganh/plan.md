# Plan — Ràng buộc Ứng dụng ↔ Nhóm ngành (dự án TKT)

## Phase 1 — BE
- [x] `GET assign/applications/for-selection`: KHÔNG cần sửa — `ApplicationService::index()` đã có sẵn filter `scope_id`, chỉ cần FE truyền lên
- [x] `ScopeService::getAll()`: nhận thêm `application_id` (lọc `application_scopes`) và `parent_project_id` (giao nhóm ngành của cha, qua helper `parentScopeIds()`)
- [x] `ProspectiveProjectRequest::scopeBelongsToApplicationRule()` — chặn scope không thuộc ứng dụng (bỏ qua dự án cha)
- [x] `ProspectiveProjectRequest::scopeBelongsToParentRule()` — scope con phải nằm trong scope của cha (cha chưa khai thì không chặn)
- [x] Giữ nguyên `scopeConflictRule()` hiện có (chặn trùng nhóm ngành với dự án mở khác của cùng KH)

## Phase 2 — FE (`ProjectInfoSection.vue`)
- [x] `loadApplications()` gửi kèm `scope_id`; `loadScopes()` gửi kèm `application_id` + `parent_project_id`
- [x] `onScopeChange()` (đổi Nhóm ngành) + `dropScopeIfInvalid()` (đổi Ứng dụng) — hỏi `$confirm` rồi mới xoá bên kia
- [x] Huỷ popup → trả select về giá trị cũ
- [x] Lỗi 2 rule mới trả về field `scope_id` → form đã có sẵn chỗ hiện `formError.scope_id`

## Phase 3 — Kiểm thử
- [ ] Dự án độc lập: chọn xuôi/ngược, đổi qua lại, huỷ popup
- [ ] Dự án con: nhóm ngành ngoài danh sách của cha → bị chặn
- [ ] Dự án cha: vẫn chọn nhiều nhóm ngành tự do
- [ ] Gọi thẳng API bỏ qua giao diện với cặp lệch → BE trả 422
- [ ] Dự án cũ đang có cặp lệch: mở màn Sửa không mất dữ liệu, chỉ chặn khi lưu

## Phase 4 — Yêu cầu làm giải pháp (mục đích cuối)
- [x] `RequestSolutionForm.populateTktFormFromProject()`: chọn dự án TKT → điền luôn Nhóm ngành + Nhóm giải pháp theo dự án; màn Sửa chỉ điền khi đang trống, không đè giá trị đã lưu
- Ghi chú: màn YCLGP vốn đã kế thừa Ứng dụng (readonly) và lọc Nhóm ngành theo scopes của ứng dụng — chính chỗ này làm lộ ra dự án TKT đang thiếu ràng buộc

### Checkpoint — 2026-09-16
Vừa hoàn thành: BE (ScopeService + 2 rule ở ProspectiveProjectRequest) và FE (ProjectInfoSection lọc 2 chiều + confirm; RequestSolutionForm prefill nhóm ngành/nhóm giải pháp). Code trên nhánh `tpe` (worktree tpe-api / tpe-client), CHƯA commit.
Đang làm dở: chưa chạy thử trên trình duyệt (Phase 3).
Bước tiếp theo: user xác nhận rồi test luồng ở cổng 3005.
Blocked: (không có)

## Phase 3 — Kết quả kiểm thử (2026-09-16, local FE :3005 / BE :8005, nhánh tpe)
BE (gọi thẳng API, bỏ qua giao diện):
- [x] `scopes/getAll?application_id=1` → đúng 3 nhóm ngành của ứng dụng (1, 10, 20); không lọc → 41 nhóm
- [x] `applications/for-selection?...&scope_id=1` → có UD.0001; `scope_id=2` → 0 ứng dụng
- [x] `scopes/getAll?parent_project_id=234` → đúng tập nhóm ngành của cha; kết hợp `application_id` → giao 2 tập
- [x] Lưu dự án con với nhóm ngành lệch ứng dụng → 422 "Nhóm ngành ... không thuộc ứng dụng ..."
- [x] Lưu dự án con có cha, nhóm ngành ngoài cha → 422 "... không nằm trong nhóm ngành của dự án cha"
- [x] Nhóm ngành hợp lệ (thuộc ứng dụng + chưa bị dự án khác chiếm) → lưu 200
- [x] Dự án CHA chọn nhóm ngành tự do (kể cả nhóm không thuộc ứng dụng nào) → 200
- [x] YCLGP gửi Nhóm giải pháp lệch ứng dụng → 422 (rule có sẵn từ trước)

FE (Playwright, tài khoản namdangit@gmail.com):
- [x] Màn Sửa dự án: `scopes/getAll` gửi kèm `application_id`; danh sách Nhóm ngành chỉ còn nhóm của ứng dụng
- [x] Chọn Nhóm ngành trước (chưa có ứng dụng) → `applications/for-selection` gửi kèm `scope_id`, ứng dụng bị lọc đúng
- [x] Đổi ứng dụng làm nhóm ngành lệch → popup xác nhận; **Hủy** giữ nguyên ứng dụng cũ + nhóm ngành cũ
- [x] **Tiếp tục** → đổi ứng dụng, xoá nhóm ngành, hiện dòng cảnh báo nêu lý do
- [x] YCLGP: chọn dự án → Ứng dụng kế thừa, **Nhóm ngành + Nhóm giải pháp tự điền theo dự án**; danh sách Nhóm giải pháp chỉ 8 mục của ứng dụng (tổng hệ thống 518)

Sửa phát sinh trong lúc test (2 lỗi thật):
- Lọc cứng hai chiều gây KẸT: mỗi ô chỉ còn 1 lựa chọn, không đổi ứng dụng được → chỉ lọc ứng dụng theo nhóm ngành KHI CHƯA CHỌN ứng dụng
- Đổi ứng dụng làm nhóm ngành bị xoá ÂM THẦM (list rỗng thì `dropScopeIfInvalid` thoát sớm) → chuyển sang hỏi TRƯỚC KHI ĐỔI trong `onApplicationChange()`, thêm `fetchScopeOptions()` và dòng cảnh báo lý do dưới ô Nhóm ngành

Dữ liệu test đã trả về nguyên trạng (#274 scope_id=2, #234 xoá nhóm ngành, không để lại YCLGP rác).

## Phase 4 — Rút gọn câu chữ khi ô Nhóm ngành trống (2026-09-17)
- [x] Giữ NGUYÊN luật chống trùng nhóm ngành (#11142) — user cân nhắc lại, không gỡ
- [x] FE `ProjectInfoSection.vue`: dòng cảnh báo dưới ô Nhóm ngành + message popup đổi Ứng dụng rút còn đúng "Chưa khai báo nhóm ngành hoặc nhóm ngành đang thuộc dự án khác."

## Phase 5 — Gỡ bế tắc dự án con (2026-09-19, nhánh `tpe`, worktree tpe-api/tpe-client)
- [x] BE `ScopeService::occupiedScopeIds()` nhận `parent_project_id`: dự án CHA + các con cùng cha không tính là "đang chiếm" nhóm ngành
- [x] BE `ProspectiveProjectRequest::scopeConflictRule()` bỏ qua cha + anh em cùng cha khi payload có `parent_id`
- [x] FE `ProjectInfoSection.fillScopeFromParent()`: cha chỉ có 1 nhóm ngành → tự điền cho con; cha nhiều nhóm → để user chọn
- [x] Kiểm thử trình duyệt tại `127.0.0.1:3005` — 6 ca (cha 1 nhóm tự điền / cha 3 nhóm để chọn / lưu nháp con / con thứ 2 trùng nhóm / màn Sửa giữ giá trị / dự án độc lập vẫn bị chặn). Dữ liệu test #359 #360 đã xoá
- Ghi chú: luật "con nằm trong nhóm ngành của cha" là quyết định nội bộ 16/09, KHÔNG có trong Redmine #11142; #11142 chỉ quy định cha chọn nhiều / con chọn 1 + chống trùng theo khách hàng
