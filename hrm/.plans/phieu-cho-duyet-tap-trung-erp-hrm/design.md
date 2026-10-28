# Thiết kế — Phiếu chờ duyệt tập trung ERP + HRM (đợt 1: nghiệp vụ)

Ngày: 22/10/2026 · Trạng thái: **đã duyệt 22/10** (thứ tự: màn Chờ duyệt trước, màn khác + báo cáo sau) · Quyết định gốc: [README.md](README.md) ·
Danh mục luồng: [flows-dot1.md](flows-dot1.md) · Kiểm kê: [inventory-erp.md](inventory-erp.md), [inventory-hrm.md](inventory-hrm.md)

## 1. Mục tiêu

Một **hộp duyệt chung** gom mọi việc đang chờ một người xử lý — duyệt/không duyệt, tiếp nhận, lập chứng từ kế
tiếp — của cả ERP và HRM. Xem được ở **cả 2 hệ thống**, cùng một danh sách cho cùng một người. Bấm phiếu mở đúng
**nơi làm trọn bước đó**. Có **báo cáo phê duyệt** (thời gian chờ/duyệt từng cấp).

Bối cảnh: ERP đang chuyển dần sang HRM, giai đoạn gần chạy song song; ERP + HRM dùng **1 DB gộp**. Nhiều bảng ERP
(34 luồng) hiện được ghi trạng thái từ cả 2 hệ thống.

**Thành công khi:**
- Một phiếu vào trạng thái chờ ở bất kỳ hệ thống nào → hiện trong hộp của đúng người có thể xử lý, ở cả 2 màn.
- Phiếu rời trạng thái chờ (dù xử lý ở ERP, HRM) → biến khỏi hộp ở cả 2 màn; không có phiếu kẹt.
- Không ai thấy phiếu mà bấm vào không có nút xử lý; không ai có nút xử lý mà phiếu không hiện trong hộp.
- Badge chỉ đếm phiếu trong hạn (chờ ở cấp hiện tại ≤ 30 ngày).

**Ngoài phạm vi đợt 1:** nhân sự (Timesheet, Decision, Training, Payroll, Human) — đợt 2, spec riêng; Assign legacy
(AS16–AS20, AS22); sửa lỗi phân quyền gốc phát hiện khi kiểm kê (ghi ở README, xử lý riêng); thay đổi luồng nghiệp vụ
gốc; khoá phía ERP.

## 2. Dữ liệu — registry dùng chung

Hai bảng trên DB gộp. **Migration nằm ở `hrm-api`** (ERP không có migration cho 2 bảng này).

### 2.1 `approval_inbox` — 1 dòng / 1 phiếu nguồn

Giữ schema ERP bản `develop_01` (gồm cả các migration bổ sung partner, `document_date` DATETIME, `submitted_at`),
thay đổi:

| Thay đổi | Lý do |
|---|---|
| Khoá duy nhất `(source_table, source_id)` (bỏ `source_system` khỏi khoá) | 34 bảng được ghi từ 2 hệ thống — phiếu là 1 dòng dù ai thao tác |
| `source_system` = hệ thống **sở hữu bảng** (`erp` / `hrm`) | Không phải hệ thống vừa ghi |
| + `handler_system` (`erp`/`hrm`) và `handler_path` (đường dẫn tương đối) theo cấp hiện tại | Nơi làm trọn bước; màn mỗi bên tự dựng URL tuyệt đối |
| + `gate_type` (`permission`/`approver`/`role`/`dept_manager`/`room_manager`/`warehouse_stocker`/`assigned_buyer`/`source_creator`/`support_department`) + `gate_params` JSON | Biểu diễn gate thật; `required_permission` giữ cho loại `permission` |
| + `required_guard` (`web`/`api`) | Quyền xét theo guard của `handler_system` |
| Bỏ `approve_route`, `approve_params` | Thay bằng `handler_path` |
| Index `(status, company_id, required_guard, required_permission)`, `(status, approver_id)`, `(status, level_started_at)` | Truy vấn hộp + badge + Quá hạn |

`status`: 1 PENDING · 2 APPROVED · 3 REJECTED · 4 CANCELED · 5 CLOSED (rời chờ không xác định được kết quả — ví dụ
phiếu bị xoá, hoặc prune).

### 2.2 `approval_inbox_logs` — 1 dòng / 1 cấp đã kết thúc

Giữ nguyên ERP. Thêm `handler_system` (cấp đó xử lý ở đâu) để báo cáo tách được.

## 3. Khai báo luồng

- Mỗi hệ thống có file `config/approval_inbox.php` khai các **doc_type mà hệ thống đó ghi trạng thái được** (một
  luồng ghi từ 2 nơi thì khai ở cả 2 file với **cùng nội dung các trường dùng chung**).
- Mỗi doc_type: `label`, `group`, `table`, `model`, `owner` (`erp`/`hrm`), hàm/định nghĩa `pending_levels`: danh sách
  cấp, mỗi cấp = điều kiện trạng thái chờ + `step` (duyệt/tiếp nhận/lập chứng từ) + `handler_system` + `handler_path`
  + `gate_type` + `gate_params` + phạm vi (`company`/`department`/`part`); và `payload` (mã, tiêu đề, người YC,
  công ty/phòng/bộ phận, đối tác, số tiền, ngày chứng từ, `submitted_at`).
- Nội dung cụ thể từng doc_type: [flows-dot1.md](flows-dot1.md).
- **Test so khớp 2 file**: một lệnh/test đọc config cả 2 repo (đường dẫn repo kia qua biến môi trường khi chạy CI
  local) và báo lệch ở các trường dùng chung của doc_type khai ở cả 2 nơi.

## 4. Cơ chế đẩy — `sync()` idempotent, 2 bản tương đương

Mỗi hệ thống có `ApprovalInboxService` (ERP: `app/Services/ApprovalInbox/`; HRM: module dùng chung, đề xuất
`Modules/Assign/Services/ApprovalInbox/` hoặc `app/Services/ApprovalInbox/` theo convention hiện hành — chốt ở plan).

`sync(string $docType, int $id, ?int $actorId = null)`:
1. Đọc phiếu nguồn (kể cả đã xoá mềm). Tính cấp chờ hiện tại theo `pending_levels` → `null` nếu không chờ.
2. Đọc dòng registry theo `(table, id)` — `SELECT … FOR UPDATE` trong transaction.
3. Đối chiếu:

| Registry | Nguồn | Hành động |
|---|---|---|
| không có / đã đóng | đang chờ cấp L | Tạo/mở lại dòng PENDING (mở lại thì `round + 1`), `level_started_at = now` |
| PENDING cấp L | đang chờ cấp L | Cập nhật payload (tiêu đề, số tiền…) — không đổi `level_started_at` |
| PENDING cấp L | đang chờ cấp L' ≠ L | Ghi log cấp L (`approve`, actor), chuyển sang L', `level_started_at = now` |
| PENDING | không chờ | Ghi log cấp L với kết quả suy từ trạng thái nguồn (approve/reject/cancel), đóng dòng |
| không có / đã đóng | không chờ | Không làm gì |

4. Gọi lặp bao nhiêu lần cũng ra cùng kết quả. Lỗi trong `sync()` được bắt và ghi log, **không làm hỏng giao dịch
   nghiệp vụ** (chạy sau commit: `DB::afterCommit` / dispatch sau transaction).

**Điểm gọi:**
- **Model event `saved` + `deleted`** trên model nguồn của mỗi doc_type, ở cả ERP và HRM (34 bảng trùng: gắn ở cả 2
  model). Một trait dùng chung `SyncsApprovalInbox` (khai `approvalInboxDocType()`).
- **Chỗ ghi bằng query-builder** `->update()` (bỏ qua model event): gọi `sync()` tường minh ngay sau đó. Danh sách chỗ
  gọi lấy từ mục 4 của [flows-dot1.md](flows-dot1.md).
- **Lưới an toàn**: lệnh `approval-inbox:backfill [--prune]` (chuyển từ ERP, chạy ở cả 2 hệ thống cho phần khai báo
  của mình) — duyệt toàn bộ nguồn, gọi `sync()` cho từng phiếu chờ, đóng (CLOSED) dòng PENDING không còn chờ ở nguồn.
  Cron 30 phút ở **cả 2** hệ thống.

## 5. Ai thấy phiếu nào

Một dòng PENDING hiện cho user U khi **U bấm được bước đó ở `handler_system`**:

- **Tập quyền**: mỗi request tính quyền của U **tại công ty đang làm** cho guard `web` và `api` bằng SQL thẳng:
  vai trò của U (`employee_has_roles`, mọi `model_type`) ⋈ `role_has_permissions` với `company_id` = công ty đang làm.
  Không dùng spatie `can()` (khe `model_type = App\Employee` làm HRM không thấy quyền). **Không ngoại lệ Super Admin.**
- **Công ty**: `company_id` = công ty đang làm hoặc NULL.
- Lọc theo `gate_type`:
  - `permission`: `required_permission` ∈ tập quyền của guard `required_guard`; phạm vi `department`/`part` thì
    `department_id`/`part_id` ∈ phòng/bộ phận U quản lý (như ERP `permission_scopes`).
  - `approver`: `approver_id = U`.
  - `role`: U có vai trò `gate_params.roles` tại công ty đang làm.
  - `dept_manager`: `department_id` ∈ phòng U quản lý.
  - `room_manager`: `gate_params.room_id` ∈ phòng họp U quản lý.
  - `warehouse_stocker`: U là thủ kho của kho trên phiếu (`warehouse_stockers`).
  - `assigned_buyer`: U là NV mua hàng được phân công hãng của phiếu.
  - `source_creator`: U là người tạo đối tượng gốc (ví dụ người tạo giải pháp duyệt hồ sơ trình duyệt).
  - `support_department`: phòng hỗ trợ của phiếu ∈ phòng U quản lý.
  Định nghĩa chính xác từng loại + doc_type dùng: §0 [flows-dot1.md](flows-dot1.md).
- Bộ giải viết 1 lần mỗi bên (cùng thuật toán), có **test dùng chung bộ ca** (cùng dữ liệu → 2 bên ra cùng tập id).

**Quá hạn**: `level_started_at < now − N ngày`, N = `config('approval_inbox.overdue_days', 30)`. Badge chỉ đếm trong hạn.

**Dữ liệu hiển thị**: chỉ cột tóm tắt trong registry. Không lưu giá vốn. Số tiền chỉ ghi khi màn gốc cho người duyệt
bước đó thấy số tiền.

## 6. Màn hình

### ERP (Blade) — chuyển từ `develop_01`
- **Phiếu chờ duyệt** (`approvalInbox.index`) và **Báo cáo phê duyệt** (`approvalInbox.report`) + xuất Excel.
- Đổi: đọc qua bộ giải §5; tab Trong hạn / Quá hạn; link theo `handler_system` (`erp` → route nội bộ; `hrm` → tab mới
  `HRM_URL + handler_path` qua SSO); badge menu. Giữ UX đã duyệt tháng 8. Menu "Chờ duyệt" cũ giữ trạng thái comment.

### HRM (Nuxt, khuôn V2) — mới
- **`/approval-inbox`**: `SmartFilterPanel` + `V2BaseDataTable`, bảng theo mẫu MISA; lọc Loại phiếu (có số đếm),
  Phòng/BP/Người YC trong phạm vi, khoảng ngày, tab Trong hạn/Quá hạn; xuất Excel; mã phiếu → trang HRM trong app hoặc
  `erpUrl(handler_path)` tab mới.
- **`/approval-inbox/report`**: báo cáo phê duyệt từ logs, khuôn `report-styles`.
- **my-job › Chờ duyệt**: thay placeholder — 10 phiếu trong hạn mới nhất, badge thật, "Xem tất cả".
- **Menu**: mục "Phiếu chờ duyệt" có badge.
- **Mockup HTML**: [mockup.html](mockup.html) (đo style từ app thật 22/10) → user duyệt trước khi code.

### Quyền
`Xem phiếu chờ duyệt tập trung`, `Xem báo cáo phê duyệt` — khai ở cả `ERP PermissionsTableSeeder` (guard web) và
`hrm-api PermissionsTableSeeder` (guard api), kiểu `$this->perm([...])` đồng bộ theo tên. Không có quyền xem → không
vào màn; quyền xem chỉ mở màn, **danh sách phiếu luôn lọc theo §5**.

## 7. Lỗi & trường hợp biên

| Trường hợp | Xử lý |
|---|---|
| `sync()` lỗi (thiếu cột, phiếu hỏng) | Bắt + ghi log; giao dịch nghiệp vụ không bị ảnh hưởng; prune 30' sửa lại |
| Phiếu xoá cứng | Event `deleted` → đóng CLOSED; prune bắt phần còn sót |
| Phiếu bị trả về rồi gửi lại | Mở lại dòng, `round + 1`, log giữ lịch sử vòng trước |
| 2 hệ thống `sync()` cùng lúc 1 phiếu | `FOR UPDATE` trên dòng registry; kết quả cuối theo trạng thái nguồn |
| Khai báo 2 bên lệch | Test so khớp §3 chặn |
| Loại có gate "mọi người" | Không đăng ký (danh sách chờ nghiệp vụ trong flows-dot1.md) |
| Màn HRM gate qua spatie guard api (khe `App\Employee`) — 7 dòng ⚠ flows-dot1 §7 | Người duyệt thật thấy phiếu trong hộp nhưng bấm vào bị 403. **Chốt 22/10: sửa các gate đó sang trait CEP ngay trong feature** (bước 3), rồi khai handler = HRM |

## 8. Triển khai — worktree & các bước

- Worktree `websites/wt-phieu-cho-duyet/{TanPhatDev,hrm-api,hrm-client}`, nhánh `gop_db-phieu-cho-duyet-tap-trung` từ
  `origin/gop_db` ở cả 3 repo. `hrm-api` `composer install` riêng (không symlink vendor). Cổng server riêng.
- DB local: chốt khi xin phép chạy migration (mặc định `hrm_erp_21_10_prod`, chỉ thêm 2 bảng mới).
- Các bước (hồ sơ con tạo khi bắt đầu từng bước):
  1. **Nền**: migration (hrm-api), model, `sync()`, bộ giải quyền, trait, lệnh backfill — 2 bên; test so khớp.
  2. **ERP**: khai báo + gắn event/sync cho các doc_type có `Ghi được từ` ERP; bổ sung cấp thiếu; luồng mới đăng ký.
  3. **HRM**: sửa gate các màn ⚠ (flows-dot1 §7) sang trait CEP; khai báo + gắn event/sync cho doc_type ghi từ HRM (34 bảng trùng + Assign/Finance/CSKH/MasterData/Meeting).
  4. **Màn hình**: mockup HRM → duyệt → code HRM; chuyển 2 màn ERP.
  5. **Kiểm thử** (§9).
- Deploy **1 lần** sau khi xong đợt 1, thứ tự HRM → ERP: migrate, `permission:sync` 2 bên, backfill 2 bên, gán quyền xem
  cho vai trò, bật cron. Hỏi riêng trước khi làm.
- Mọi bước đụng source/DB: hỏi user kèm phạm vi, chờ câu "làm".

## 9. Kiểm thử

- **PHPUnit `sync()`** mỗi bên: vào chờ, giữ cấp (cập nhật payload), chuyển cấp, đóng duyệt/từ chối/huỷ, xoá, gửi lại
  (round), gọi lặp không sinh log trùng. Mỗi doc_type 1 ca khói: tạo phiếu ở trạng thái chờ → `sync` → có dòng đúng cấp/
  handler/gate.
- **Bộ giải quyền**: cùng bộ ca chạy ở 2 bên ra cùng tập; ca có quyền / không quyền; quyền ở công ty khác không thấy;
  Super Admin không quyền không thấy; role `App\Employee` thấy được.
- **Kiểm chéo hệ thống**: duyệt 1 phiếu ở HRM → dòng đóng trên màn ERP; ngược lại.
- **Playwright** 2 màn HRM + 2 màn ERP: đo số dòng/badge từ DOM khớp DB, link mở đúng hệ thống, tab Quá hạn, xuất Excel,
  ca không quyền vào màn bị chặn.
- Chạy e2e theo yêu cầu user (`--workers=1`); kiểm bằng Playwright MCP mỗi task UI.
