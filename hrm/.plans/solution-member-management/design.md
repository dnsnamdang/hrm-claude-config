# Design — Quản lý nhân sự giải pháp: Cập nhật / Khóa / Xóa (Redmine #11354)

Người phụ trách: @junfoke · Nhánh: `task_11354` (cả `hrm-api` và `hrm-client`, rẽ từ `tpe-develop-assign`)

## Mục tiêu

Tab **Nhân sự** của màn Quản lý giải pháp hiện mới chỉ **Thêm** được thành viên. Bổ sung 3 thao tác
còn thiếu: **Cập nhật**, **Khóa** (kèm chặn khi còn việc tồn đọng), **Xóa** (chặn khi đã phát sinh
dữ liệu liên đới).

## Hiện trạng (rà ngày 15/09/2026)

### Thành viên nằm ở 2 bảng, rẽ theo `solutions.has_modules`

`SolutionService::addMember()` tự rẽ nhánh:

| Loại giải pháp | Bảng | Prod (`hrm_prod_09_26`) |
| --- | --- | --- |
| `has_modules = 0` | `solution_members` | 37/39 GP · **48 dòng** |
| `has_modules = 1` | `solution_module_members` | 2/39 GP · **0 dòng** |

Phải làm cả 2 nhánh, nhưng chỉ nhánh `solution_members` có dữ liệu thật để verify.

### Tab Nhân sự là danh sách ẢO ghép từ 4 nguồn

`SolutionService::getHumanResources()` gộp:

| # | Dòng hiển thị | Nguồn | Có bản ghi thành viên? |
| --- | --- | --- | --- |
| 1 | PM làm giải pháp | `solutions.pm_id` | KHÔNG |
| 2 | Leader hạng mục | `solution_modules.leader_id` | KHÔNG |
| 3 | Thành viên hạng mục | `solution_module_members` | Có |
| 4 | Thành viên giải pháp | `solution_members` | Có |

Trên prod **5/5 hạng mục đều có `leader_id`** → dòng Leader chắc chắn xuất hiện.

3 vấn đề phải sửa trước khi làm được bất kỳ thao tác nào:

1. **Response không trả khóa bản ghi**: mọi dòng trả `'id' => $employee->id` (id NHÂN VIÊN), nên FE
   không có gì để gọi `PUT/DELETE .../members/{id}`.
2. **Một người có thể ra 2 dòng**: Leader được push ở bước 2.1, nếu cũng có bản ghi trong
   `solution_module_members` thì bị push tiếp ở 2.2 — code không loại trừ.
3. **`status` hard-code `'Active'`** và **`end_date` lấy từ giải pháp/hạng mục**, không phải của
   thành viên — đúng 2 cột spec yêu cầu quản lý thì hiện chỉ là giá trị trang trí.

### Tài sản dùng lại được

- `Solution::getMyRole()` trả sẵn đúng 3 vai trò spec cần: `Trưởng phòng giải pháp` (= `created_by`),
  `PM` (= `pm_id`), `Leader hạng mục` (= `solution_modules.leader_id`).
- Module Bàn giao (`Handover` + `HandoverItem`) — CHỈ ĐỌC, xem mục quyết định 2.

## Quyết định đã chốt (user chốt 15/09/2026)

### 1. Đối tượng thao tác: CHỈ thành viên thường

Nút Cập nhật / Khóa / Xóa **chỉ hiện ở dòng thành viên** (nguồn 3 và 4). Dòng **PM** và
**Leader hạng mục** ẩn hết nút — chúng không phải bản ghi trong bảng thành viên, đổi chúng là đổi
`solutions.pm_id` / `solution_modules.leader_id`, tức sửa cấu trúc giải pháp, đã có chức năng
Phân công (`AssignManagerModal`) lo. Hai đường sửa cùng một dữ liệu là nguồn gây lệch.

Căn cứ: spec ghi "Leader hạng mục chỉ có quyền thao tác trên **các thành viên** thuộc hạng mục mình
phụ trách" — đối tượng là thành viên.

### 2. KHÔNG lập phiếu bàn giao hộ

Người khóa (PM/Trưởng phòng GP/Leader) **chỉ XEM** danh sách việc tồn đọng rồi nhắc thành viên tự
vào màn `/assign/handover` bàn giao. Hệ quả:

- **KHÔNG sửa `HandoverService`** — `store()` và `getAvailableItems()` đang hard-code
  `auth()->user()->id`, giữ nguyên. Tránh giẫm chân đợt fix bug đang diễn ra ở màn Bàn giao.
- **Không cần theo dõi trạng thái phiếu bàn giao.** "Hết tồn đọng" = đếm lại Task/Issue còn
  `assignee_id` = thành viên đó và đang mở. Phiếu chờ duyệt thì `assignee_id` chưa đổi → vẫn còn
  tồn đọng → chưa khóa được (đúng bản chất). Người nhận tiếp nhận xong → `assignee_id` đổi → đếm
  về 0 → khóa được.

### 3. "Đang mở" = đúng tập mà màn Bàn giao cho bàn giao

Lấy cùng một tập để không sinh 2 ca hỏng:
- rộng hơn tập bàn giao được → có việc tính là tồn đọng nhưng không bàn giao được → **kẹt vĩnh viễn**;
- hẹp hơn → khóa được trong khi còn việc phải bàn giao → **việc treo vô chủ**.

| Đối tượng | Trạng thái tính là ĐANG MỞ |
| --- | --- |
| Task | 2 Chờ phê duyệt triển khai · 3 Chờ bắt đầu · 4 Đang thực hiện · 5 Tạm dừng · 6 Hoàn thành - Chờ duyệt · 7 Từ chối kết quả · 10 Từ chối triển khai |
| Task — KHÔNG tính | 1 Nháp · 8 Hoàn thành · 9 Huỷ |
| Issue | `assigned` Đã phân công · `in_progress` Đang xử lý · `resolved` Đã xử lý xong · `reopened` Mở lại · `completed` Hoàn thành · `rejected` Từ chối |
| Issue — KHÔNG tính | `new` Mới ghi nhận · `closed` Đã đóng |

⚠️ **Chỉ mượn điều kiện TRẠNG THÁI.** `getAvailableItems()` còn lọc thêm "chưa nằm trong phiếu bàn
giao nào đang dở" — điều kiện đó để tránh bàn giao trùng, **KHÔNG được dùng cho việc đếm tồn đọng**:
bê sang thì thành viên vừa lập phiếu (còn chờ duyệt, `assignee_id` chưa đổi) sẽ bị đếm ra 0 và PM
khóa được ngay, trong khi việc chưa sang tay ai.

### 4. CHẤP NHẬN 2 chỗ lệch, không sửa (user chốt: "kệ đi, có gì lỗi báo sau")

- **Issue `Đã xử lý xong` / `Hoàn thành` / `Từ chối` vẫn tính là tồn đọng.** Thành viên làm xong
  sạch việc vẫn bị chặn khóa. Muốn bỏ thì phải sửa `getAvailableItems()` = đổi hành vi màn Bàn giao
  đang chạy thật → không làm trong đợt này.
- **Cột đếm task trên tab Nhân sự dùng `Task::listInProgress()` = `[2,3,4,5,6,7]`, thiếu trạng thái
  10.** Nên có ca tab hiện 0 task mà bấm Khóa lại báo còn 1 việc tồn đọng. **KHÔNG đưa trạng thái
  Từ chối vào `listInProgress()`** (user chốt) — hằng đó nhiều chỗ khác đang dùng. Đợt này tạo hằng
  RIÊNG cho phần tồn đọng, giữ `listInProgress()` nguyên vẹn.

## Phạm vi đợt này

Làm: migration 2 cột · sửa `getHumanResources()` · gate quyền 3 vai trò · Cập nhật · Xóa có ràng
buộc · Khóa (cả ca tồn đọng = 0 và > 0, popup chỉ đọc).

KHÔNG làm: lập phiếu bàn giao hộ · sửa bất cứ thứ gì trong `HandoverService`.

## Còn treo

- Nút "Nhắc bàn giao" bắn thông báo cho thành viên (skill `notification-convention`) — chờ user quyết.
- #11282 (phân loại nhân sự chính/CTV/đối tác) sẽ xây tiếp trên tab này, làm sau khi #11354 xong.
