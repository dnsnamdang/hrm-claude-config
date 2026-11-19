# Design — Vấn đề v2 (web panel) + tab Vấn đề trong Nhóm trao đổi · phân hệ Công việc

> Folder con của `.plans/gop-db/phan-he-cong-viec/`, cạnh `nhiem-vu-v2/`. Tạo 17/11/2026.
> Khởi nguồn: user muốn thêm tab **Vấn đề** vào Nhóm trao đổi (Chat). Kiểm code thấy Vấn đề vẫn dùng popup cũ
> `CreateIssueModal` trong khi Nhiệm vụ đã lên `TaskPanel` ⇒ user chọn làm **Vấn đề v2 trước**, rồi mới làm tab trong nhóm
> (hồ sơ tab nhóm: `.plans/agent-chat/chat/gd34-tab-van-de/`, Phase 3 dưới đây).
>
> Nguồn đã chốt (không hỏi lại):
> - Mockup web GĐ0 màn `gd0-mockup/screens/19-phong-van-de.html` + `_build/td.js` (phần `isI`) — panel + form Vấn đề.
> - U36, U37, U38 ở `.plans/app-cong-viec-nhiem-vu-van-de/design.md` (Đợt 3) + màn app VD2-01…16.
> - Khuôn web Nhiệm vụ v2: `nhiem-vu-v2/design.md` (N1–N8) + code `hrm-client/components/assign/task/panel/*`.
> - Khảo sát code Vấn đề: `.plans/app-cong-viec-nhiem-vu-van-de/khao-sat-web-van-de.md` (29/10, có `file:dòng`; dưới đây gọi "KS").

## 1. Mục đích

Người dùng mở / tạo / xử lý Vấn đề bằng **cùng một khuôn panel** với Nhiệm vụ (panel trượt phải, sửa tại chỗ, nút hành
động theo vai trò), thay popup b-modal 1,707 dòng mà mọi chuyển trạng thái phải chọn ô rồi bấm Lưu. Panel là nền để dựng
tab Vấn đề trong Nhóm trao đổi đồng bộ với tab Nhiệm vụ đang có.

**Thành công** = 13 chỗ đang gọi popup chuyển sang panel không sót hành vi; luồng Tạo → Phân công → Nhận xử lý → Báo đã
xử lý → Xác nhận / Từ chối → Đóng / Mở lại chạy bằng nút; đề nghị gia hạn chạy như Nhiệm vụ; tab Vấn đề trong nhóm hiện
đúng vấn đề của nhóm.

**Phản mục tiêu:** mất trường dữ liệu đang có (vấn đề cũ mở ra thiếu thông tin); người không đủ vai trò vẫn đổi trạng
thái được qua API; lệch khuôn với TaskPanel (2 kiểu panel trong cùng phân hệ).

## 2. Quyết định đã chốt

| # | Chốt | Ai |
|---|---|---|
| V1 | Làm Vấn đề v2 **trước**, tab Vấn đề trong nhóm làm **sau** trên nền panel mới | user 17/11 |
| V2 | **`IssuePanel` mới theo khuôn `TaskPanel`** (không gộp chung 1 panel, không giữ popup cũ đổi ruột). Giữ API công khai cũ của popup ⇒ 13 chỗ gọi chỉ đổi import; xoá `CreateIssueModal.vue` | user 17/11 |
| V3 | Trang `/assign/issues` **giữ dạng bảng** như `/assign/tasks` (2 trang chính đổi sang gom nhóm cùng nhau ở đợt sau). Danh sách gom nhóm chỉ dựng cho tab Vấn đề trong nhóm | user 17/11 |
| V4 | **Có đề nghị gia hạn** cho Vấn đề (như N2 Nhiệm vụ) | user 17/11 |
| V13 | **Phân công** vấn đề Mới ghi nhận / Mở lại: **người tạo + trưởng đơn vị xử lý** (trưởng bộ phận `parts.part_lead_id`, không có thì trưởng phòng `departments.department_lead_id` — đúng người đang nhận thông báo "Tạo mới") (§4.3) | user 17/11 (builder check) |
| V14 | **Thêm thông báo các bước chính** (§4.8) | user 17/11 |
| V15 | **Đổi người phụ trách ⇒ về Đã phân công**; người tạo, trưởng đơn vị xử lý và **người phụ trách tự chuyển** đều đổi được (§4.9) | user 17/11 |
| V18 | Form tạo: Loại / Mức độ ảnh hưởng / Nguồn phát hiện **để trống** (bỏ mặc định bug/personal/self của popup cũ) | user 17/11 |
| V5–V12, V16–V17 | Các mục §4 đánh dấu *(Claude)* — user soát khi duyệt hồ sơ | Claude |

## 3. Phạm vi theo repo

| Phase | Repo · nhánh | Việc |
|---|---|---|
| 1 | `hrm-api` · nhánh mới từ `origin/gop_db` | vá store/PUT, PATCH 1 trường, PATCH status nhận dữ liệu bước, đề nghị gia hạn, theo dõi, cờ quyền mới trong resource, migration |
| 2 | `hrm-client` · cùng tên nhánh | `IssuePanel` + form + hộp bước; thay 13 chỗ gọi; xoá popup cũ; e2e |
| 3 | `hrm-api` + `hrm-client` | tab Vấn đề trong Nhóm trao đổi (§6) |
| — | `TPE_APP` | **ngoài phạm vi** — app VD2 đã có thiết kế, code phải hỏi riêng |

Worktree: `websites/wt-nhom-trao-doi` (đang sạch, nhánh `gop_db-chat-roi-nhom` đã deploy). Tên nhánh đề xuất
`gop_db-van-de-v2`. Theo [[feature-moi-nhanh-rieng-merge-khi-user-bao]]: không tự merge gop_db.

## 4. Hành vi

### 4.1 Panel xem (thay chế độ Xem + Xử lý của popup)

- Khung, kích thước, z-index, backdrop, `above-modal` (mở từ trong b-modal) **giống TaskPanel**; dùng lại
  `task-panel.scss` (tách phần chung nếu cần, không nhân bản CSS).
- Header: icon 🐞 + mã `ISS-…` · pill trạng thái (màu `Issue::STATUS_DATA`, BE trả — **không** map màu ở FE, sửa KS #14) ·
  tên vấn đề · nút 👁 Theo dõi (V9) · ⋯ (Lịch sử, Xoá khi `can_delete`) · Đóng.
- Dải nút hành động theo `allowed_next_statuses` + vai trò (bảng §4.3). Không có quyền thì ghi lý do ("Chờ X xác nhận
  hoàn thành"), như VD2-09.
- 4 tab (mockup): **Chi tiết** · **Kết quả xử lý** · **Bình luận** (dùng lại `comment-thread type="issue"`, đếm) ·
  **Lịch sử** (dùng lại nguồn `system-logs/issue`, đếm).
- **Chi tiết**: các khối theo nhóm trường §4.4; người có `can_edit` bấm vào giá trị ⇒ popover sửa 1 trường (khuôn
  `TaskFieldPopover`) ⇒ PATCH 1 trường. Người khác chỉ đọc.
- **Kết quả xử lý**: người báo đã xử lý, thời điểm, Nhóm nguyên nhân, Cách xử lý, tệp chứng cứ; khi Từ chối thì hiện lý do
  từ chối; khi Đóng hiện lý do đóng. Chưa có ⇒ dòng trống "Chưa báo xử lý".
- Bấm **hạn**: người có `can_edit` ⇒ đổi hạn (PATCH 1 trường); người phụ trách ⇒ **Đề nghị gia hạn** (§4.5). Hiện đề nghị
  đang chờ ngay dưới hạn, người quyết có nút Đồng ý / Từ chối (khuôn TaskPanel).
- Deep link `?open_issue={id}&comment_id={cid}` giữ nguyên (mở panel, cuộn tới bình luận).

### 4.2 Form Tạo / Sửa (panel chế độ form, rộng như TaskPanel `wide`)

Bố cục theo mockup, **giữ đủ mọi trường đang có** (KS §2) — mockup lược bớt, phần lược dời vào Thiết lập *(Claude, V5)*:

1. **Gắn với** (giống N4 Nhiệm vụ — chưa có ô Không gian): Giải pháp → Dự án tự điền → Hạng mục (bắt buộc khi GP có hạng
   mục). Mở từ GP / Hạng mục / nhóm thì điền sẵn + khoá như hiện tại (`lockSolution`, `lockModule`, `lockProject`) — **không
   ghi vào prop** (sửa KS #18).
2. **Tên vấn đề** *.
3. Hàng: **Loại vấn đề** * · **Mức độ ảnh hưởng** * · **Nguồn phát hiện** * (giá trị BE như hiện tại, 9/8/7 giá trị — không
   theo giá trị mẫu của mockup).
4. **Mức độ ưu tiên** * — chip tô màu `PRIORITY_DATA` (khuôn chip TaskForm).
5. Hàng: **Người phụ trách xử lý** (placeholder "Để trống — trưởng bộ phận phân công", có lối tắt "Giao cho tôi" đang có) ·
   **Phòng ban xử lý** + **Bộ phận xử lý** (bộ phận khoá khi chưa chọn phòng ban, đổi phòng ban xoá bộ phận — giữ luật cũ).
   Dưới hàng: dòng báo trước (U36) "Gửi xong → **Đã phân công**: X nhận thông báo…" / "→ **Mới ghi nhận**: trưởng bộ phận Y
   nhận thông báo…" / "Chọn Người phụ trách hoặc Phòng ban xử lý".
6. Hàng: **Người duyệt đóng** (placeholder "Không có — báo xong là Hoàn thành") · **Người báo** (chỉ đọc = người tạo).
7. **Hạn xử lý** + **Giờ hạn** (mặc định 17:30 — U33, thay 17:00) + chọn nhanh Hôm nay / Ngày mai / Thứ 6 này / +1 tuần.
   Hạn không bắt buộc (như hiện tại).
8. **Mô tả** *.
9. Hàng thêm: **+ Tệp** (bảng tệp/chứng cứ hiện tại: loại tài liệu + tệp, luật đuôi/20MB giữ nguyên).
10. **Thiết lập** (thu gọn, "n mục đang dùng"): Người theo dõi · Người phối hợp · Thẻ · SLA xử lý · Nhiệm vụ chính liên kết
    (sửa picker: hiện `code – name`, tìm theo tên — KS #11) · Người phát hiện + Ngày giờ phát hiện (gửi giờ địa phương, không
    `toISOString` — KS #23) · Ảnh hưởng tiến độ / chất lượng / khách hàng + Ghi chú ảnh hưởng · Kế hoạch xử lý · Điều kiện
    đóng. Mỗi mục 1 dòng giải thích ngắn như Thiết lập TaskForm.

- **Không có ô Trạng thái** (U36). Tạo: có Người phụ trách ⇒ gửi `assigned`; không có ⇒ `new` (phải có Phòng ban). Sửa:
  trạng thái chỉ đổi bằng nút hành động (§4.3), form Sửa không có ô trạng thái *(Claude, V6 — khác TaskForm Sửa vẫn có;
  lý do: U2 "Màn Sửa vẫn giữ ô Trạng thái" là của app Nhiệm vụ, còn Vấn đề mọi bước chuyển đều đã có nút + hộp nhập riêng)*.
- Form **Sửa**: ô Người phụ trách chỉ đọc (đổi người qua hộp §4.9 để giữ đúng trạng thái + thông báo) *(Claude)*; PUT bỏ
  qua `assignee_id`. Phòng ban / Bộ phận xử lý vẫn sửa được (đổi khi chưa có người phụ trách ⇒ báo trưởng đơn vị mới như
  hiện tại).
- Nhóm nguyên nhân **không** ở form (chỉ nhập khi Báo đã xử lý — U37).
- Footer Tạo: **[Gửi vấn đề]** **[Gửi & tạo tiếp]** **[Huỷ]** *(Claude, V7 — mockup chỉ có Gửi vấn đề; thêm Gửi & tạo
tiếp theo khuôn button-convention N5 vì popup cũ có nút Làm mới để nhập liên tiếp)*. Footer Sửa: **[Lưu thay đổi]**
**[Huỷ]**. Không có Lưu nháp (Vấn đề không có trạng thái nháp).
- Validate báo đồng thời mọi ô ([[validate-form-bao-dong-thoi]]); 422 BE gắn vào đúng ô.

### 4.3 Nút hành động & hộp bước *(Claude, V8 — theo mockup `td.js:79` + VD2-02…08)*

| Trạng thái hiện | Người | Nút (→ trạng thái) | Hộp nhập |
|---|---|---|---|
| Mới ghi nhận | người tạo · trưởng đơn vị xử lý (V13) | **Phân công** (→ assigned) | chọn Người phụ trách * |
| Mới ghi nhận | người phụ trách | **Nhận xử lý** (→ in_progress) — sửa KS #7 | — |
| Đã phân công / Mở lại | người phụ trách | **Nhận xử lý** (→ in_progress) | — |
| Mở lại | người tạo · trưởng đơn vị xử lý (V13) | **Phân công** (→ assigned) | chọn Người phụ trách * |
| Đã phân công / Đang xử lý / Từ chối / Mở lại | người tạo · trưởng đơn vị xử lý · người phụ trách | **Đổi người phụ trách** (→ assigned, §4.9) | Người phụ trách mới * · lý do (tuỳ chọn) |
| Đang xử lý | người phụ trách | **Báo đã xử lý** (→ resolved nếu có người duyệt, completed nếu không) | Cách xử lý * · Nhóm nguyên nhân * · tệp chứng cứ (U37) |
| Đã xử lý xong | người duyệt | **Xác nhận hoàn thành** (→ completed) · **Từ chối kết quả** (→ rejected) | Từ chối: lý do * |
| Từ chối | người phụ trách | **Xử lý lại** (→ in_progress) | — |
| Hoàn thành | người tạo / người phụ trách | **Mở lại** (→ reopened) | lý do (tuỳ chọn, VD2-08) |
| mọi trạng thái chưa đóng/hoàn thành | người tạo / người phụ trách | **Đóng vấn đề** (→ closed, nút đỏ, ở cuối dải) | lý do (tuỳ chọn) — ghi `closed_reason` (sửa KS #10) |

- Mọi nút gọi **`PATCH assign/issues/{id}/status`** (đã có, đã kiểm `allowed_next_statuses`) — mở rộng nhận `assignee_id`
  (Phân công), `resolution` + `root_cause_group` + `attachments` (Báo đã xử lý), `reason` (Từ chối / Đóng / Mở lại).
- Nút chỉ hiện khi trạng thái đích nằm trong `allowed_next_statuses` BE trả **và** đúng vai trò ở bảng — FE không tự suy
  luật ngoài cờ BE (C2 hồ sơ app). Cần BE trả kèm mỗi bước `requires` (assignee / resolution / reason) hoặc FE map cố định
  theo mã trạng thái *(để builder chọn)*.

### 4.4 Ai làm gì (giữ luật BE hiện tại, vá chỗ hở)

- `can_edit` (người tạo, chưa closed/completed) ⇒ sửa form + sửa tại chỗ + đổi hạn + quyết đề nghị gia hạn.
- `can_delete` (người tạo, đang `new`) ⇒ Xoá (giữ xoá cứng như hiện tại — KS #19 ngoài phạm vi).
- `can_handle` ⇒ các nút ở §4.3.
- **Vá BE** *(Claude, V10 — tương đương N3 Nhiệm vụ)*:
  - Store chỉ nhận `status ∈ {new, assigned}`; `assigned` bắt buộc `assignee_id`; bỏ các trường mốc (`completed_at`,
    `resolved_at`, …) khỏi dữ liệu tạo (KS #5).
  - PUT: chỉ người `can_edit`; **không** nhận `status` nữa (trạng thái chỉ qua PATCH status) — KS #3. Người chỉ có
    `can_handle` gọi PUT ⇒ 403 thay vì ghi một phần + sync watcher/tag/tệp (KS #4).
  - `canHandle` thêm trạng thái `new` cho người phụ trách (KS #7).
  - Store validate `due_date`, `detected_at`, `approver_id exists`, `watcher_ids.*`, `supporter_ids.*` (KS #24).
  - Migration: `issues.resolution` string → **text** (U37).
- Quyền xem chi tiết (KS #1–#2) **ngoài phạm vi** — thuộc đợt vá quyền đọc ([[va-lo-hong-quyen-doc-dot-1]], nhánh
  `gop_db-va-quyen-xem-task-issue`, đang ở bước ghi log).

### 4.5 Đề nghị gia hạn (V4) *(chi tiết là Claude, V11 — sao khuôn Nhiệm vụ)*

- Bảng mới `issue_extension_requests`: `id, issue_id, requested_by, old_due_date, old_due_time, new_due_date,
  new_due_time, reason (text, bắt buộc), status (1 chờ · 2 đồng ý · 3 từ chối · 4 huỷ), decided_by, decided_at,
  reject_reason, timestamps`; index `(issue_id, status)`. Cùng dạng `task_extension_requests`.
- Ai gửi: **người phụ trách** (`assignee_id`) khi trạng thái ∈ {assigned, in_progress, rejected, reopened} và vấn đề **có
  hạn**. Tối đa 1 đề nghị chờ / vấn đề. Người gửi huỷ được đề nghị của mình.
- Ai quyết: người `can_edit` (người tạo). Đồng ý ⇒ cập nhật `due_date/due_time` + lịch sử "đổi hạn theo đề nghị". Từ chối
  ⇒ lý do bắt buộc.
- Đề nghị đang chờ tự **huỷ** khi vấn đề sang resolved / completed / closed *(Claude)*.
- Thông báo (`sendNotification`, url `/assign/issues?open_issue={id}`): gửi đề nghị ⇒ người tạo; quyết ⇒ người gửi.
- API theo khuôn task: `POST assign/issues/{issue}/extension-requests`, `POST assign/issues/extension-requests/{ext}/approve|reject|cancel`.
  Chi tiết vấn đề trả `pending_extension` + cờ `can_request_extension`, `can_decide_extension`.

### 4.6 Theo dõi *(Claude, V9 — như N6)*

`POST assign/issues/{issue}/watch` — ai mở được vấn đề cũng tự theo dõi / bỏ theo dõi chính mình (bảng `issue_watchers`
đang có), ghi lịch sử. Chi tiết trả `is_watching`.

### 4.8 Thông báo (V14) — theo skill `notification-convention`, url `/assign/issues?open_issue={id}`

| Sự kiện | Người nhận (trừ chính người bấm) | Ghi chú |
|---|---|---|
| Tạo có Người phụ trách / Phân công / Đổi người phụ trách | người phụ trách mới | **mới** (KS #9) |
| Tạo / đổi đơn vị xử lý khi chưa có người phụ trách | trưởng đơn vị xử lý | **đã có** (`notifyHandlingDepartmentLead`) |
| Nhận xử lý | người tạo | **mới** |
| Đã xử lý xong (có người duyệt) | người duyệt | **đã có** |
| Hoàn thành (người duyệt xác nhận, hoặc báo xong khi không có người duyệt) | người tạo + người phụ trách | **mới** |
| Từ chối kết quả | người phụ trách (kèm lý do) | **đã có** |
| Đóng · Mở lại | người tạo + người phụ trách (+ người duyệt nếu có) | **mới** |
| Đề nghị gia hạn / quyết đề nghị | §4.5 | **mới** |

Không báo người theo dõi / phối hợp ở đợt này *(Claude)* — giữ như hiện tại, tránh nhiễu.

### 4.9 Đổi người phụ trách (V15)

- Ai: người tạo, trưởng đơn vị xử lý (V13), người phụ trách hiện tại (tự chuyển việc — giữ khả năng popup cũ đang có).
- Khi nào: trạng thái ∈ {assigned, in_progress, rejected, reopened}. Mới ghi nhận ⇒ dùng nút Phân công. Đã xử lý xong /
  Hoàn thành / Đã đóng ⇒ không đổi được.
- Kết quả: trạng thái về **Đã phân công** (người mới phải bấm Nhận xử lý); xoá `rejected_at/rejected_reason` nếu đang Từ
  chối *(Claude)*; ghi lịch sử kèm lý do (tuỳ chọn); thông báo người mới (§4.8). Đề nghị gia hạn đang chờ của người cũ tự
  huỷ *(Claude)*.
- Đi qua `PATCH status` (bước → assigned kèm `assignee_id`), **không** qua PATCH 1 trường: ô Người phụ trách ở tab Chi tiết
  không sửa tại chỗ, bấm vào mở hộp Đổi người phụ trách *(Claude)*. Cần BE cho phép bước assigned → assigned (đổi người) —
  hiện `getAllowedNextStatuses` chưa có.

### 4.10 Tệp đính kèm sau khi tạo *(Claude, V16 — builder check)*

- Người tạo + người phụ trách + trưởng đơn vị xử lý thêm / xoá tệp bất cứ lúc nào (khi chưa Đóng / Hoàn thành) qua API riêng
  `POST assign/issues/{issue}/attachments` · `DELETE …/attachments/{file}` (người khác chỉ xoá tệp mình thêm) — thay
  đường PUT cũ (V10 chặn PUT với người chỉ có `can_handle`).
- Tệp chứng cứ lúc **Báo đã xử lý** lưu bảng `files` với `table='issue_resolutions'` (cùng `table_id` = id vấn đề) ⇒ tab
  Kết quả xử lý hiện riêng; `syncForTable('issues', …)` khi Sửa không đụng tới.

### 4.11 Lớp kiểm truy cập `IssueAccess` *(Claude, V17 — builder check)*

- Mới, theo khuôn `TaskAccess` (`Modules/Assign/Services/Task/TaskAccess.php`): `assertView` = vấn đề nằm trong phạm vi xem
  (dùng lại `IssueService::applyPermissionScope` lọc theo id) ⇒ 403 nếu không.
- Gắn cho **API mới** của đợt này: watch, PATCH 1 trường, PATCH status, gia hạn, thêm/xoá tệp. Chặn trường hợp tự theo dõi
  một vấn đề bất kỳ để kéo nó vào danh sách của mình (tầng 1 phạm vi có `watchers`).
- **Không** gắn cho `GET /{id}`, bình luận, lịch sử — thuộc đợt vá quyền đọc ([[va-lo-hong-quyen-doc-dot-1]]); ghi sang
  danh sách việc của đợt đó.

### 4.12 Thay 13 chỗ gọi (V2)

`issues/index.vue` · `my-job/components/IssuesTab.vue` · `my-todo/index.vue` · `agent/AgentWorkspace.vue` ·
`handover/add.vue` · `handover/_id/index.vue` · `handover/_id/receive.vue` · `report/employee-work-performance/components/WorkDrillModal.vue` ·
`solutions/components/manager/IssueTab.vue` · `…/manager/FilesTab.vue` · `…/manager/IssueUpcomingModal.vue` ·
`solution-modules/_id/components/IssueTab.vue` · `…/FilesTab.vue`.

- `IssuePanel` giữ đúng chữ ký `open(issue, readOnly, isHandling, initialData, commentId, options)` + sự kiện popup cũ đang
  phát (builder đọc từ `CreateIssueModal.vue` và từng chỗ gọi) **và thêm** `view(issue, commentId)` (sửa KS #12 —
  `IssueUpcomingModal` đang gọi `view` không tồn tại). `open(item, true, true)` (chế độ Xử lý cũ) ⇒ mở panel xem, dải nút
  hành động sẵn.
- Chỗ mở từ trong b-modal (`IssueUpcomingModal`, `WorkDrillModal`, handover) ⇒ `above-modal` như TaskPanel; kiểm
  Playwright từng chỗ.
- `IssueHistoryModal` (menu ⋮ Lịch sử ở danh sách) giữ nguyên — không thuộc popup.

## 5. Ràng buộc

- Không đổi API danh sách / xuất Excel / cấu hình cột của `/assign/issues` (V3).
- PATCH status giữ tương thích: app TPE_APP chưa dùng Vấn đề, nhưng tham số cũ (`status`, `reason`) phải chạy như cũ.
- Nhãn hiển thị "Vấn đề", mã/API giữ chữ `issue`.
- e2e: theo CLAUDE.md, đổi FE ⇒ kiểm Playwright đo DOM + ca e2e mới + chạy lại toàn bộ spec màn bị đụng (bộ `serial`, đọc
  dòng tổng kết). Tài khoản namdangit (NV 13). Có ca không quyền ([[always-test-permission-cases]]).

## 6. Phase 3 — Tab Vấn đề trong Nhóm trao đổi

Đã chốt với user 17/11 (lượt trước, user không phản đối):
- Nhóm thường + nhóm GP có tab Vấn đề, bật/tắt ở form tạo nhóm + Cấu hình → Tab sử dụng. **Nhóm TKT không có** (GĐ12 Q5).
- Nhóm thường: hiện vấn đề tạo từ nhóm ⇒ migration `issues.workspace_id` (nullable + index). Nhóm GP: hiện mọi vấn đề của
  GP (như tab Nhiệm vụ nhóm KH — GĐ12 Q11).
- Danh sách gom nhóm theo khuôn `TaskGroupListView` (gom Trạng thái / Người xử lý / Hạn / Dự án), bấm dòng ⇒ `IssuePanel`,
  "+ Vấn đề" ⇒ panel tạo điền sẵn nhóm (và GP nếu nhóm GP).
- Xem / tạo: mọi Quản lý + Thành viên nhóm (kể cả khác công ty); sửa / xử lý theo cờ của Vấn đề.
- Bỏ chặn `issues` cho nhóm GP ở `StoreWorkspaceRequest` / `UpdateWorkspaceRequest` (giữ chặn cho TKT).
- Ngoài phạm vi: tin hệ thống trạng thái vấn đề vào nhóm (kiểu GĐ23), tự nạp tab (kiểu GĐ27), tạo vấn đề từ tin nhắn.

Chi tiết + plan riêng ở `.plans/agent-chat/chat/gd34-tab-van-de/` khi bắt đầu Phase 3.

## 7. Để lại cho người làm

- Tách CSS chung TaskPanel ↔ IssuePanel thế nào (đổi tên lớp hay dùng lại `tkp-*`).
- Cách FE biết bước nào cần hộp nhập (§4.3 cuối).
- Chia component: `IssuePanel` / `IssueForm` / `IssueDetailTab` / `IssueResultTab` / hộp bước — theo khuôn thư mục
  `components/assign/task/panel/` ⇒ `components/assign/issue/panel/`.
- Dữ liệu e2e (vấn đề ở từng trạng thái cho từng vai trò).
