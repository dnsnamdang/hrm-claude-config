# Plan — Quản lý nhân sự giải pháp (Redmine #11354)

Nhánh: `task_11354` (cả 2 repo, rẽ từ `tpe-develop-assign`). Design: [design.md](design.md)

## Phần 1 — Nền: DB + chuẩn hóa API danh sách

- [x] Migration: `solution_members` + `solution_module_members` thêm `end_date` (date, null) và
      `status` (tinyint, mặc định 1 = Active); backfill 48 dòng hiện có về Active
- [x] `solution_module_members` bổ sung cột audit `created_by` / `updated_by` (đang thiếu, không
      theo convention `BaseModel`)
- [x] Entity `SolutionMember` + `SolutionModuleMember`: hằng `STATUS_ACTIVE` / `STATUS_INACTIVE`,
      `$fillable` đủ cột mới
- [x] `getHumanResources()` trả thêm `member_row_id` + `source`
      (`pm` | `module_leader` | `module_member` | `solution_member`) — FE cần khóa này để gọi API
      và để quyết định ẩn/hiện nút
- [x] `getHumanResources()` trả `status` + `end_date` THẬT của thành viên (bỏ hard-code `'Active'`)
- [x] `getHumanResources()` gộp dòng trùng: Leader đồng thời là thành viên hạng mục → 1 dòng, vai
      trò ghép lại, `source` lấy theo bản ghi thành viên

## Phần 2 — Phân quyền thao tác

- [x] Helper xác định quyền thao tác trên 1 dòng thành viên, bám `Solution::getMyRole()`:
      Trưởng phòng GP (`created_by`) và PM (`pm_id`) thao tác mọi thành viên; Leader hạng mục chỉ
      thao tác thành viên thuộc hạng mục mình phụ trách
- [x] Gate ở BE cho cả 3 endpoint (chốt chặn thật), FE chỉ ẩn nút

## Phần 3 — Cập nhật thành viên

- [x] `PUT assign/solutions/{solution}/manager/members/{member}` — sửa hạng mục phụ trách, vai trò,
      ngày bắt đầu, ngày kết thúc, mô tả
- [x] Đổi hạng mục ở GP có hạng mục = chuyển bản ghi sang `solution_module_id` khác
- [x] FE: popup Sửa (khuôn popup Thêm sẵn có), validate ngày kết thúc >= ngày bắt đầu

## Phần 4 — Xóa có ràng buộc

- [x] Đếm dữ liệu liên đới của thành viên trong phạm vi giải pháp: đã tạo BOM / Task / Issue, hoặc
      đang được giao việc
- [x] Chưa phát sinh gì → cho xóa; đã phát sinh → chặn, báo đúng câu spec:
      "Thành viên đã phát sinh dữ liệu (BOM/Task/Issue). Vui lòng sử dụng chức năng Khóa để bảo
      toàn dữ liệu hệ thống."
- [x] FE: dùng `base-confirm-modal` sẵn có, không dựng popup xác nhận riêng

## Phần 5 — Khóa thành viên

- [x] Hằng RIÊNG cho "đang mở" (KHÔNG đụng `Task::listInProgress()`): Task `[2,3,4,5,6,7,10]`,
      Issue `[assigned, in_progress, resolved, reopened, completed, rejected]`
- [x] Đếm tồn đọng theo `assignee_id` + trạng thái — KHÔNG lọc theo "đã nằm trong phiếu bàn giao"
      (xem design.md mục 3, đây là cái bẫy làm khóa được sớm khi việc chưa sang tay)
- [x] Tồn đọng = 0 → xác nhận rồi chuyển `status` sang Inactive
- [x] Tồn đọng > 0 → CHẶN, mở popup "Bàn giao công việc tồn đọng trước khi khóa thành viên" liệt kê
      Task/Issue (CHỈ ĐỌC) + lối sang `/assign/handover`
- [x] Popup hiện thêm trạng thái bàn giao từng dòng (đọc `handover_items`: "đã nằm trong phiếu
      BG-xxx, đang chờ duyệt") — không có thì người khóa nhắc xong quay lại vẫn thấy y nguyên danh
      sách, tưởng thành viên chưa làm gì
- [x] Thành viên Inactive: chặn truy cập/tạo mới BOM, Task, Issue trong phạm vi giải pháp

## Phần 6 — Verify

- [x] Playwright: 3 thao tác × 2 nhánh (`solution_members` / `solution_module_members`)
- [x] Kiểm ẩn nút đúng: dòng PM và Leader hạng mục không có nút nào
- [x] Kiểm Leader hạng mục chỉ thao tác được thành viên hạng mục mình phụ trách

## Việc KHÔNG làm trong đợt này

- Lập phiếu bàn giao hộ người khác (user chốt 15/09: người khóa chỉ xem và nhắc)
- Sửa bất cứ thứ gì trong `HandoverService` — màn Bàn giao đang có bug chưa fix, tránh giẫm chân
- Sửa `Task::listInProgress()`

### Checkpoint — 2026-09-15

Vừa hoàn thành: **toàn bộ Phần 1-5, cả BE lẫn FE**, đã verify tay trên dev server.

Commit — `hrm-api`: `fc70dcef5` (nền) · `31cde31c1` (service + endpoint) · `bbe24b77a` (payload popup Sửa);
`hrm-client`: `2a6b1ae93` (cột Thao tác + 2 popup).

⚠️ Nhánh ban đầu lỡ rẽ từ `tpe-develop-assign`, đã dựng lại từ `tpe` và cherry-pick — xem
memory `feedback_branch_base_tpe`.

Verify trên GP#2 (đang mở, đặt tạm DNS Admin làm PM):
- dòng PM ẩn hết nút, 6 dòng thành viên có đủ 3 nút ✔
- Sửa: đổi ngày kết thúc -> toast + bảng cập nhật ngay ✔
- Khóa (0 việc tồn): badge chuyển "Đã khóa" xám, nút đổi sang Mở khóa ✔
- Khóa (2 task đang mở): CHẶN, popup liệt kê đúng 2 task kèm mã/tên/hạn ✔
- Xóa (đã có task): chặn, toast ra ĐÚNG NGUYÊN VĂN câu spec ✔
- Xóa (chưa phát sinh gì): xóa được, danh sách còn 6 dòng ✔
- Giải pháp ĐÃ ĐÓNG (GP#1): ẩn hết nút, khớp với nút Phân công sẵn có ✔

Đã dọn sạch dữ liệu test trên DB local (task mượn trả về chỗ cũ, pm_id trả nguyên, thành viên
hạng mục test đã xóa, thành viên bị khóa/bị xóa khi verify đã khôi phục).

Bước tiếp theo: chờ user quyết nút "Nhắc bàn giao"; làm nốt 2 mục còn treo ở Phần 5 và Phần 6.

Blocked: không có.

### Lỗi CÓ SẴN phát hiện khi verify (chưa sửa, ngoài phạm vi)

`HumanResourceTab.vue` truyền `variant` không hợp lệ cho `V2BaseBadge` (`info` / `secondary` /
`warning` — chỉ nhận `muted` / `brand` / `required` / `status-draft` / `status-ok` / `null`) và
`V2BaseButton variant="brand"` (component này dùng prop `primary`/`secondary` + `status`).
Console đỏ mỗi lần mở tab, có từ trước đợt này.

### Checkpoint — 2026-09-16 (XONG toàn bộ)

User chốt 3 điểm còn treo: (1) chặn Inactive **cả XEM** giải pháp, không chỉ tạo mới;
(2) **có** nút Nhắc bàn giao; (3) **sửa luôn** lỗi variant có sẵn.

Commit thêm — `hrm-api` `76296d6f1`, `hrm-client` `9f1f3ebee`.

**Chặn thành viên đã khóa** — middleware `CheckSolutionMemberActive` (alias `solutionMemberActive`):
gắn cho cả nhóm route `/assign/solutions` (44 route) và 3 route tạo Task/Issue/BOM.
Đặt ở ROUTE chứ không trong controller vì 3 controller kia nhận FormRequest.
Verify: `POST` task vào GP bị khóa -> **403**, vào GP không khóa -> **422** (qua middleware rồi
mới dừng ở validate) — chứng minh đúng thứ tự; `GET` GP không bị khóa vẫn 200, không chặn oan.

**Nhắc bàn giao** — thông báo thật đã sinh và kiểm nội dung trong DB:
`[BGCV] Nhắc báo cáo: <b>Triển khai chương trình nâng cao kiến thức kỹ t...</b>. Còn 2 công việc
cần bàn giao. DNS Admin nhắc.` — tên cắt 50 ký tự, in đậm, deep-link kèm `solution_id`.

**Trạng thái bàn giao trong popup** — verify với 1 phiếu Chờ duyệt dựng tay:
task 1 ra "Đã nằm trong phiếu BG-TEST-11354 — Chờ duyệt", task 2 ra "Chưa bàn giao",
và **vẫn đếm là tồn đọng** (2) vì `assignee_id` chưa đổi — đúng thiết kế.

Đã dọn sạch dữ liệu test: task mượn trả chỗ cũ, `pm_id` GP#2 trả nguyên, phiếu bàn giao test và
thông báo test đã xóa, nv13 gỡ khỏi GP#3, mọi thành viên bị khóa lúc verify đã mở lại.

### ⚠️ Cần người viết yêu cầu xác nhận 1 điểm

Nhóm hành động của thông báo nhắc đang là **"Nhắc báo cáo"** — skill `notification-convention`
chỉ cho dùng 14 nhóm cố định và cấm tự chế nhóm mới; "Nhắc báo cáo" là nhóm mang nghĩa NHẮC duy
nhất, nhưng đọc lên không khớp hẳn với việc nhắc bàn giao. Hai hướng: giữ nguyên, hoặc bổ sung
nhóm "Nhắc bàn giao" vào skill (phải sửa tài sản chung, cần PR).

Blocked: không có.

## Test case

- [x] Sinh 48 TC cho #11354 — `gen_testcase.py` -> `testcase - 11354 Quan ly nhan su giai phap.xlsx`

⚠️ KHÁC khuôn mặc định của skill `testcase-documenter`: lần này TC phải **chèn tiếp vào tab
"Testcase _ Quản lý chi tiết GP"** của Google Sheets "Testcase _Quản lý dự án" mà team đang dùng,
nên file chỉ chứa đúng phần dòng dữ liệu theo **19 cột sẵn có của tab đó** — không kèm khối 9 mục
mô tả và 2 khối TEST SUMMARY, để khỏi phá bố cục cũ.

Bám quy ước của tab: cột Module = "Quản lý giải pháp"; mã TC nối tiếp TC-ROLE-91 (mã cuối đang có)
nên chạy từ **TC-ROLE-92 → TC-ROLE-139**; dòng tiêu đề nhóm chỉ điền cột "Chức năng".

6 nhóm: quyền thao tác · cập nhật phân công · khóa và mở khóa · xóa có ràng buộc ·
hiệu lực của trạng thái Đã khóa · hiển thị và dữ liệu bảng. P0 chiếm 72%.

⚠️ Công cụ Google Drive trong phiên làm việc **chỉ đọc được** bảng tính (chức năng cập nhật chỉ
đổi được tên file / thư mục), nên không ghi thẳng vào sheet được — bàn giao bằng file .xlsx để
người phụ trách tự dán xuống cuối tab.

## Hướng dẫn test

- [x] Sinh tài liệu Word `Huong dan test - 11354 Quan ly nhan su giai phap.docx` bằng
      `gen_huong_dan_test.py` (dùng chung `hdsd_engine.py` của skill `hdsd-documenter`).
      Nội dung: phạm vi test · tài khoản 4 vai trò cần chuẩn bị · dữ liệu cần dựng (cả 2 loại
      giải pháp) · bảng trạng thái tính là "đang mở" · 8 mục thao tác click-by-click ·
      3 điểm đã biết không phải lỗi · dọn dữ liệu sau test · đối chiếu TC-ROLE-92→139.
      CHƯA có ảnh chụp thật: code nằm ở nhánh `task_11354`, working tree đang ở
      `tpe-develop-assign` nên không dựng được màn để chụp.
