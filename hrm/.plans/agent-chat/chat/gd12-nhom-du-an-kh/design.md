# GĐ12 — Nhóm trao đổi gắn Dự án KH (Dự án TKT / Xây dựng GP)

> Trạng thái: thiết kế đã chốt nội dung (14/11/2026), chờ user duyệt. Chưa code. Thay phương án N2p cũ ở
> `.plans/gop-db/phan-he-cong-viec/plan.md:152` (giữ màn cũ + thêm tab chat).

## 1. Mục đích

Đội dự án hiện trao đổi ở Nhóm trao đổi (Chat), còn việc của dự án (nhiệm vụ, vấn đề, meeting, nhân
sự) nằm ở màn manager. Muốn: **nhóm trao đổi gắn được với đúng 1 dự án KH**, việc tạo trong nhóm tự
về màn manager, thành viên nhóm tự bám theo nhân sự dự án.

Thực tế tổ chức (user chốt): Dự án TKT do **phòng sale** phụ trách; bước làm GP do **phòng GP** làm với
đội riêng ⇒ **mỗi bước 1 nhóm riêng**, không gộp 1 nhóm xuyên suốt.

## 2. Phạm vi

**Làm:** nhóm gắn **Dự án TKT** và nhóm gắn **Xây dựng GP**.

**Không làm đợt này:** nhóm gắn **Hợp đồng** (HĐ chưa có màn manager — để đợt sau, cùng lúc làm màn
manager HĐ). Không đụng luồng nghiệp vụ TKT → YC GP → GP → Báo giá → HĐ (trạng thái, dữ liệu, duyệt):
nhóm chỉ là lớp gắn thêm.

**Anti-goal:** nhóm làm thay đổi trạng thái / dữ liệu của dự án, GP; một dự án có 2 nhóm cùng loại;
người ngoài dự án tự gắn nhóm vào dự án để kéo nhân sự / đẩy việc lên màn manager.

## 3. Quyết định đã chốt với user

| # | Nội dung | Chốt |
|---|---|---|
| Q1 | Gắn vào bước nào | Tách: nhóm TKT (sale) và nhóm GP (phòng GP) riêng |
| Q2 | Đồng bộ nhân sự | **Chỉ 1 lần lúc tạo nhóm** (đổi 14/11, thay "đồng bộ liên tục"). Sau đó Quản lý nhóm tự thêm / gỡ; thay đổi ở manager KHÔNG tự vào nhóm |
| Q3 | Vai trò khi đồng bộ vào | Tất cả = **Thành viên**; người tạo nhóm là Quản lý, tự nâng quyền người khác |
| Q4 | Hợp đồng | Để đợt sau |
| Q5 | Vấn đề ở nhóm TKT | Nhóm TKT **không có** tab Vấn đề; chỉ nhóm GP có |
| Q6 | Dự án / GP đóng | Không tự đóng nhóm; gửi 1 tin hệ thống vào nhóm |
| Q7 | Ai được gắn | Chỉ người phụ trách: **NVKD chính** (`main_sale_employee_id`) với Dự án TKT; **PM** (`solutions.pm_id`) với GP |
| Q8 | Dự án cha – con | Chỉ gắn dự án con và dự án thường; **dự án cha không có nhóm** |
| Q10 | Ai tạo việc đẩy lên manager | Mọi Quản lý / Thành viên nhóm, kể cả người thêm tay |
| Q11 | Tab Nhiệm vụ / Meeting trong nhóm | Hiện toàn bộ việc của dự án / GP (cả việc tạo ở manager) |
| Q12 | Tab Vấn đề nhóm GP | Tách đợt sau; GĐ12 chỉ Nhiệm vụ + Meeting |
| Q14 | Thành viên khác công ty | Cho phép, áp cho MỌI loại nhóm (§4.6) |
| Q15 | Số GP / dự án | Đúng 1 |
| Q13 | ~~Bị gỡ ở nguồn mà còn việc dở~~ | Bỏ — không còn đồng bộ liên tục (Q2) |
| Q9 | Chỗ tạo | Form tạo nhóm trong Chat có ô "Là dự án KH"; màn manager TKT / GP có nút "Nhóm trao đổi" (mở nhóm nếu có, chưa có thì mở form tạo điền sẵn — chỉ hiện với người phụ trách). Không gắn nhóm cũ có sẵn vào dự án |

## 4. Hành vi

### 4.1 Tạo nhóm "Là dự án KH"
- Form tạo nhóm (`components/chat/workspace/CreateWorkspaceModal.vue`) thêm công tắc **"Là dự án KH"**.
  Bật ⇒ chọn loại **Dự án TKT / Xây dựng GP** (segmented) + ô chọn đối tượng.
- Ô chọn chỉ liệt kê đối tượng mà người tạo là **người phụ trách** (Q7), **chưa có nhóm**, **chưa đóng**,
  và (với TKT) **không phải dự án cha** (Q8).
- **1 đối tượng tối đa 1 nhóm** (call của Claude — tránh 2 nhóm sale cùng 1 dự án). BE chặn trùng.
- Nhóm lưu `workspaces.type` = `TYPE_PROSPECTIVE_PROJECT` (2) / `TYPE_SOLUTION` (3), `source_type` /
  `source_id` trỏ đối tượng — các hằng và cột **đã có sẵn** trong `Workspace` (chưa dùng).
- Đã gắn thì **không đổi / gỡ liên kết** được (call của Claude — đổi liên kết làm lệch việc đã đẩy lên
  manager). Tên nhóm gợi ý sẵn "`<mã> – <tên dự án/GP>`", sửa được.
- Tab chức năng vẫn tuỳ chọn như nhóm thường; tab Vấn đề chưa có ở GĐ12 (Q5, Q12).

### 4.2 Việc tạo trong nhóm về màn manager
| Tạo trong nhóm | Nhóm TKT | Nhóm GP |
|---|---|---|
| Nhiệm vụ | gắn `project_id` = dự án ⇒ hiện tab Nhiệm vụ manager TKT | gắn `solution_id` = GP (và `project_id` của GP nếu luồng tạo nhiệm vụ GP hiện có ghi) ⇒ hiện tab Nhiệm vụ manager GP, và tab Nhiệm vụ manager TKT (đã gom việc GP) |
| Meeting | ghi thêm dòng `prospective_project_meetings` ⇒ hiện tab Meeting manager TKT | ghi `prospective_project_meetings` có `solution_id` ⇒ hiện tab Meeting manager GP |
| Vấn đề | — (không có tab) | **đợt sau** (Q12) — tab Vấn đề của nhóm chưa có |

- **Bỏ luật loại trừ** `WorkspaceTaskRules::MSG_EXCLUSIVE` ("Nhiệm vụ đã gắn Giải pháp / Dự án, không
  gắn nhóm được") **cho nhóm dự án KH**, với điều kiện dự án / GP của nhiệm vụ **trùng** đối tượng của
  nhóm. Nhóm thường giữ nguyên luật.
- Nhiệm vụ tạo trong nhóm dự án KH tự điền dự án / GP theo nhóm, không cho đổi sang dự án khác.
- Việc tạo ở màn manager **không** gắn `workspace_id` (giữ hành vi màn manager như cũ), NHƯNG tab
  Nhiệm vụ / Meeting **trong nhóm dự án KH hiện TOÀN BỘ việc của dự án / GP** (Q11), gồm cả việc tạo ở
  manager. Nhóm TKT: lọc như tab Nhiệm vụ / Meeting manager TKT; nhóm GP: như manager GP.
- **Ai được tạo việc từ nhóm** (Q10): mọi Quản lý / Thành viên của nhóm, kể cả người thêm tay — giống
  nhóm thường.

### 4.3 Đồng bộ nhân sự (Q2, Q3)
| Nhóm | Nguồn nhân sự | Cột "Chức vụ ở màn manager" |
|---|---|---|
| Dự án TKT | `main_sale_employee_id` + `solution_employee_id` + `prospective_project_support_department_employees` | nhãn suy ra: "NVKD chính" / "Phụ trách GP" / "Hỗ trợ – <bộ phận>" |
| GP | `solution_members` đang hiệu lực + `solution_module_members` đang hiệu lực + `pm_id` | `project_role_name` (nhiều chức vụ ⇒ nối bằng dấu phẩy; người ở hạng mục ghi kèm tên hạng mục) |

- **Chỉ đồng bộ 1 lần, lúc tạo nhóm** (Q2): mọi người ở nguồn vào nhóm vai trò **Thành viên** (Q3),
  `added_via` mới = "Từ dự án"; người tạo nhóm là Quản lý. Đi qua `WorkspaceMemberService::add` như
  thêm thường (có tin hệ thống thêm thành viên).
- Sau đó **không tự đồng bộ**: đổi nhân sự ở manager không đụng nhóm; Quản lý nhóm tự thêm / gỡ.
- NV ở nguồn khác công ty với nhóm vẫn được thêm (xem §4.6).
- Danh sách thành viên nhóm (`MembersPanel.vue`) thêm cột **"Chức vụ ở màn manager"** — tính LÚC ĐỌC
  từ nguồn hiện tại, nên luôn khớp màn manager; người không còn / chưa từng ở nguồn ⇒ trống. Vai trò
  nhóm (Quản lý / Thành viên / Xem) độc lập với cột này.

### 4.4 Dự án / GP đóng (Q6)
- Dự án TKT sang `STATUS_DONG_DU_AN` / `STATUS_KET_THUC_VA_LUU_TRU` hoặc có `closed_at`; GP sang
  `STATUS_DONG` ⇒ gửi 1 tin hệ thống: "Dự án TKT `<mã>` đã đóng – `<lý do nếu có>`". Mở lại ⇒ tin
  "đã mở lại". Không tự đóng nhóm.

### 4.5 Nút "Nhóm trao đổi" ở màn manager (Q9)
- `pages/assign/prospective-projects/_id/manager.vue` và `pages/assign/solutions/_id/manager.vue`.
- Có nhóm ⇒ mở nhóm đó (ai là thành viên nhóm thì mở được; không là thành viên ⇒ ẩn nút).
- Chưa có nhóm ⇒ chỉ người phụ trách thấy nút, bấm mở form tạo nhóm đã bật "Là dự án KH" và điền
  sẵn đối tượng.

### 4.6 Nhóm cho phép thành viên KHÁC CÔNG TY — áp cho MỌI loại nhóm (Q14, user chốt 14/11)
- Hiện `WorkspaceMemberService::eligibleIds($companyId, …)` chỉ nhận NV đang làm việc **và thuộc
  `company_employees` của công ty nhóm**; FE (`CreateWorkspaceModal.vue`, `MembersPanel.vue`) lấy danh
  sách NV theo `current_company`. Đổi thành: **mọi NV đang làm việc, mọi công ty**; vẫn loại NV nghỉ việc.
- Ô chọn NV hiện theo khuôn chung `Tên - Mã phòng - Mã NV`; NV khác công ty với nhóm ghi kèm tên công ty
  (call của Claude, để phân biệt người trùng tên).
- "Lấy từ phòng ban / bộ phận": thêm ô chọn công ty, mặc định công ty của nhóm (call của Claude).
- `workspaces.company_id` giữ nguyên ý nghĩa "công ty sở hữu nhóm" (dùng cho danh sách nhóm của công ty,
  cài nhóm tiếp nhận YC hỗ trợ GĐ11…). Không đổi.
- Ảnh hưởng cần rà khi làm: chỗ khác dùng `eligibleIds` (`add`, `previewFromDepartments`,
  `ensureAssigneeForHandover` — phiếu bàn giao đang bỏ qua NV khác công ty), test GĐ1–GĐ11 đang khẳng
  định "khác công ty bị loại" phải sửa theo hành vi mới; NV khác công ty mở nhóm / nhiệm vụ / meeting
  của công ty khác — kiểm quyền xem không vướng chọn-công-ty trong session.

## 5. Phát hiện từ code (đã kiểm, `origin/gop_db` + DB local)

- Chuỗi: `request_solutions.project_key` → TKT (NOT NULL); `solutions.prospective_project_id` → TKT
  (NOT NULL); `quotations.project_id`, `hrm_contracts.project_id` nullable (báo giá tự lập).
- `tasks` có `project_id`, `solution_id`, `workspace_id`; `issues` có `project_id`, `solution_id`,
  **không có** `workspace_id`; `meetings` có `workspace_id`, nối dự án qua `prospective_project_meetings`.
- Tab Vấn đề / Files ở manager TKT chỉ hiện khi đã có GP (`IssueTab` nhận `solution`).
- Manager TKT **không có** tab Nhân sự; manager GP có (`HumanResourceTab`, `solution_members` có
  `project_role_id/name`, `status`, `end_date`).
- **Tab Vấn đề của Nhóm trao đổi CHƯA được làm** ("Vấn đề / File làm đợt sau" — `WorkspaceView.vue`).
  ⇒ Vấn đề trong nhóm GP là phần **làm mới**, không chỉ là gắn thêm (xem §7).
- DB local ít dữ liệu (0 HĐ, mỗi TKT ≤1 YC GP / ≤1 GP). User xác nhận nghiệp vụ: 1 dự án chỉ có 1 GP.

## 6. Để lại cho người làm
- Giao diện cụ thể công tắc, ô chọn, cột chức vụ — theo khuôn hrm-client, mockup trước khi code.

## 7. Call của Claude sau builder check (user soát lại)
- **Công ty:** nhóm lấy `company_id` của dự án / GP; ô chọn đối tượng chỉ liệt kê đối tượng thuộc công
  ty đang làm của người tạo. Thành viên được khác công ty (§4.6).
- **Version GP:** việc tạo từ nhóm GP gắn version đang hiệu lực của GP (`current_version_id`), không bắt
  chọn (cột `solution_version_id` ở `tasks`/`issues` nullable — đã kiểm DB local). Không gắn hạng mục.
- **1 TKT = đúng 1 GP** (user xác nhận 14/11 — nghiệp vụ). Nhóm GP và nhóm TKT của cùng dự án là 2 nhóm.
- **Đổi người phụ trách:** không tự vào nhóm (Q2); Quản lý nhóm thêm tay. Nút "Nhóm trao đổi" ở
  manager hiện cho mọi thành viên nhóm.
- **Quyền tạo nhóm:** route tạo nhóm hiện không gắn quyền ⇒ không phát sinh gì thêm.
- **Dự án / GP đã đóng:** nhóm không cho tạo việc MỚI gắn đối tượng đó (theo đúng màn manager đang chặn
  tạo khi đã đóng); trao đổi vẫn bình thường.

## 8. Còn hỏi user
- Không còn. User bỏ mockup (14/11). Bước tiếp: duyệt plan.
