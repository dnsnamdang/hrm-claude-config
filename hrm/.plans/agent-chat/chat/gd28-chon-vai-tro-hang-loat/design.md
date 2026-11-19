# GĐ28 — Chọn thành viên nhóm theo vai trò (nhóm đông)

Mockup đã duyệt: `mockup.html` (bản v2 gọn, user "ok" 16/11/2026). Dựng trên markup + CSS thật :3080.

## 1. Vì sao

User 16/11/2026: tạo nhóm ~600 người (20 Quản lý · 200 Thành viên · 380 Xem) hiện **không khả thi**:
- Popup Tạo nhóm chỉ có ô Quản lý + Thành viên (`CreateWorkspaceModal.vue`); popup Thêm thành viên luôn ra Thành viên
  (`AddMembersModal.vue`); không chỗ nào thêm thẳng vai trò **Xem**.
- Đổi vai trò chỉ ở tab Thành viên, menu ⋮ từng dòng, API `PUT workspaces/{id}/members/{memberId}` 1 người/lần
  (`WorkspaceMemberService::changeRole`) ⇒ 380 lần bấm.

Hai kiểu chia thực tế (user): (1) theo phòng — Ban giám đốc = Quản lý, vài phòng = Thành viên, còn lại = Xem;
(2) quản lý rải ở nhiều phòng khác nhau.

**Thành công** = cả 2 kiểu làm xong trong vài chục cú bấm trên 1 popup; nhóm đã có chỉnh vai trò cả khối người 1 lần.
**Không làm** (anti-goal): bảng tạm 600 dòng trong popup; bung 600 chip người; đồng bộ tự động theo phòng ban (vẫn "lấy 1 lần").

## 2. Phương án

| | Phương án | Đánh đổi |
|---|---|---|
| **1 (CHỌN)** | 3 dòng theo vai trò; mỗi dòng chọn người lẻ + lấy phòng ban + cả công ty | Gọn, dùng lại component; chỉnh sau cần thêm đổi hàng loạt |
| 2 | Bảng tạm có cột vai trò + gán hàng loạt | Linh hoạt nhất nhưng popup 600 dòng, nặng cho kiểu (1) |
| 3 | Vai trò mặc định + chọn ngoại lệ | Thực chất là 1, khó hiểu hơn |

## 3. Chốt của user (16/11/2026)

- **Q1** Một người có ở nhiều dòng ⇒ **giữ vai trò cao hơn** (Quản lý > Thành viên > Xem), không bắt chọn lại.
- **Q2** **Làm luôn** đổi vai trò hàng loạt ở tab Thành viên.
- **Q3** **Có nút tắt "Cả công ty"** ở mỗi dòng vai trò.
- **UI v2 gọn**: mỗi vai trò 1 dòng; người lẻ + phòng/cả công ty chung 1 ô; 2 link "Phòng ban" · "Cả công ty" cuối dòng;
  quyền vai trò + "lấy 1 lần" vào tooltip; cảnh báo trùng gom ở dòng tổng; thanh hàng loạt phẳng 1 dòng.

## 4. Giao diện (theo mockup)

### 4.1 Khối "Thành viên *" — dùng chung cho Tạo nhóm và Thêm thành viên
Component mới `components/chat/workspace/RoleMemberPicker.vue` thay ô "Quản lý" + "Thành viên" của `CreateWorkspaceModal` và ô
chọn của `AddMembersModal`.
- 3 dòng: `[badge vai trò] [số người]` │ ô chọn │ `Phòng ban · Cả công ty`. Badge màu theo `ROLE_COLORS` (MembersPanel), rê chuột ⇒
  tooltip quyền (Quản lý: quản trị nhóm · Thành viên: gửi tin, nhận nhiệm vụ · Xem: chỉ đọc tin).
- Ô chọn chứa 3 loại thẻ: **người** (chip như select hiện nay), **phòng ban/bộ phận** (icon phòng + tên + số người), **Cả công ty**
  (icon + số người). Gõ trong ô = tìm người (dữ liệu `employeeOptions`, như hiện nay). Nhiều chip người ⇒ gom "+n người".
- Tạo nhóm: người tạo nằm sẵn ở dòng Quản lý, không có × (luật cũ). Thêm thành viên: không dòng nào bắt buộc.
- Dòng tổng: "Tổng N người · Quản lý a · Thành viên b · Xem c" (đếm SAU khi gộp trùng) + "k người có ở nhiều dòng ⇒ giữ vai trò cao
  hơn · Xem" (bấm Xem ⇒ danh sách k người + vai trò cuối).
- Icon ⓘ cạnh nhãn: tooltip "Phòng ban / cả công ty chỉ lấy danh sách 1 lần lúc tạo…".
- Thêm thành viên (nhóm có sẵn): người đã ở trong nhóm bị bỏ qua, **không đổi vai trò** (luật cũ — đổi ở tab Thành viên).

### 4.2 Popup "Lấy từ phòng ban" (`DepartmentPickModal.vue`, có sẵn)
- Nhận prop `role` ⇒ tiêu đề "Lấy người làm [badge] từ phòng ban / bộ phận"; ghi chú "Người lấy vào sẽ là <vai trò>…";
  nút "Thêm n người làm <vai trò>".
- Người đang ở dòng vai trò cao hơn (trong popup cha) ⇒ cột Kết quả "Đã là Quản lý — giữ", bỏ tick sẵn. Người ở dòng thấp hơn ⇒
  "Sẽ thêm" (lên vai trò cao hơn, dòng cũ giữ thẻ nhưng tổng đếm theo vai trò cuối).
- Xác nhận ⇒ dòng nhận 1 thẻ cho mỗi lần lấy (tên các phòng đã chọn, gộp tên nếu nhiều) — giữ danh sách id đã tick bên trong thẻ.

### 4.3 "Cả công ty"
- Bấm ⇒ thêm ngay thẻ "Cả công ty · N" (không mở popup). N = nhân sự đang làm việc của **công ty của nhóm** (Tạo nhóm: công ty đang
  chọn, như `companyId` hiện nay). Công ty khác ⇒ dùng "Phòng ban" (popup có ô Công ty, GĐ12). *(Claude chọn — xem §7)*
- Đã có thẻ Cả công ty ở dòng đó thì link mờ đi.

### 4.4 Tab Thành viên — đổi vai trò hàng loạt (`MembersPanel.vue`)
- Thêm cột ô tích (chỉ Quản lý, nhóm đang chạy — như nút Thêm thành viên) + ô lọc **Phòng ban / Bộ phận** cạnh ô lọc vai trò.
- Ô tích đầu cột = chọn **toàn bộ người đang lọc** (danh sách đã nạp hết ở máy, phân trang trên máy — GĐ24), không chỉ trang hiện tại.
  Đổi bộ lọc ⇒ bỏ chọn.
- Có chọn ⇒ 1 dòng phẳng trên bảng: "Đã chọn **n** người đang lọc · Bỏ chọn" … `[Đổi vai trò ▾]` (2–3 vai trò đích) ·
  `[Mời ra khỏi nhóm]`. Mỗi thao tác hỏi xác nhận 1 lần (`$confirm`), nêu số người.
- Kết quả: toast "Đã đổi n người"; người không đổi được hiện ở khối báo lỗi có sẵn (`blocked`) dạng danh sách
  (tên + lý do + link "Xem nhiệm vụ của người này" khi do việc dở).

## 5. API (hrm-api, Modules/Assign)

### 5.1 Tạo nhóm / Thêm thành viên — thêm vai trò cho từng nguồn
- Request mới (giữ trường cũ để không vỡ client cũ): `role_groups: [{ role: 1|2|3, member_ids: [], department_member_ids: [],
  department_names: [], whole_company: bool }]` (tối đa 3 phần tử, mỗi role ≤ 1 lần). `department_member_ids` ≤ 2000/nhóm vai trò.
- `whole_company: true` ⇒ BE tự lấy nhân sự đang làm việc của công ty nhóm (không tin danh sách FE gửi) — dùng chung truy vấn của
  `previewFromDepartments` (bỏ điều kiện phòng).
- Gộp: mỗi người lấy **vai trò cao nhất** trên mọi nhóm vai trò; `added_via` = MANUAL nếu người đó được chọn lẻ ở dòng thắng, ngược lại
  FROM_DEPARTMENT. Người tạo luôn Quản lý. Nhóm KH (GĐ12): seed nhân sự dự án vẫn chạy SAU (lựa chọn tường minh thắng).
- Thêm vào nhóm có sẵn: người đã là thành viên ⇒ bỏ qua (trả `skipped`), không đổi vai trò.
- Tin hệ thống: **1 tin** cho cả lượt: "X đã thêm 600 người: 20 Quản lý · 200 Thành viên · 380 Xem" (payload `members_added` thêm
  `role_counts`), thay vì mỗi nguồn 1 tin.
- API xem trước "Cả công ty": `GET/POST …/members/preview-departments` nhận `whole_company=1` ⇒ trả số người (+ danh sách) để FE
  hiện N và tính dòng tổng/trùng.

### 5.2 Đổi vai trò hàng loạt — `PUT workspaces/{id}/members/roles`
- Body `{ member_ids: [] (≤ 2000), role }`. Quyền: Quản lý, nhóm đang chạy (middleware hiện có).
- Từng người theo luật `changeRole` hiện nay: hạ xuống Xem mà còn việc dở ⇒ không đổi (lý do + `assignee_id`); sau khi đổi nhóm phải
  còn ≥ 1 Quản lý (xét theo cả lô).
- **Đổi phần được, báo phần bị chặn** (không huỷ cả lô) *(Claude đề xuất — xem §7)*. Trả `{changed_count, blocked: [{employee_id,
  name, reason, open_task_count?}], members}`.
- 1 tin hệ thống: "X đã đổi vai trò 94 người sang Thành viên" (≤ 3 người thì nêu tên như hiện nay).

### 5.3 Mời ra hàng loạt — `POST workspaces/{id}/members/bulk-remove` (body `member_ids`)
- Luật như `remove` hiện nay (Quản lý cuối, việc dở…), cùng kiểu trả về 5.2, 1 tin hệ thống.

## 6. Ràng buộc
- Không đổi luật vai trò/phân quyền hiện có; chỉ thêm đường làm theo lô. Không migration (bảng `workspace_members` đủ cột).
- Nhóm 600+ người: thêm/đổi trong 1 transaction, `WorkspaceAccess::forget` 1 lần, 1 sự kiện realtime `conversation.updated`.
- App mobile chưa có màn tạo nhóm/đổi vai trò ⇒ không đụng; trường cũ của API vẫn nhận.
- Chỉ cổng TPE trước (memory `chi-lam-cong-tpe-truoc`).

## 7. Để lại cho người làm / Claude tự chọn (user soát)
- (Claude) "Cả công ty" = công ty của nhóm; công ty khác đi qua popup Phòng ban.
- (Claude) Đổi/mời hàng loạt: đổi phần được, báo danh sách bị chặn.
- (Claude) Thêm vào nhóm có sẵn: người đã có thì bỏ qua, không nâng vai trò.
- Tooltip: icon ⓘ theo skill `info-icon-tooltip` (`b-popover` `custom-class="info-popover"`, không `title=""`); tooltip vai trò
  dùng cùng kiểu. Popup theo `modal-popup` (V2BaseModal, V2BaseSelectInModal), nút theo `button-convention` (`mr-2 mb-2`),
  xác nhận dùng `$confirm`.
- Builder: cách dựng ô chọn trộn thẻ phòng + chip người (bọc V2BaseSelectInModal hay ô tự dựng) — miễn nhìn như mockup, dùng style chung.
- Kiểm: PHPUnit gộp vai trò cao nhất / whole_company / đổi hàng loạt có người bị chặn / Quản lý cuối; e2e tạo nhóm 3 dòng + đổi hàng loạt
  (có quyền + không quyền — memory `always-test-permission-cases`); Playwright đo DOM theo mockup.

## 8. Sau builder check (16/11/2026)
- (Claude) `member_ids` của API hàng loạt = `workspace_members.id` (khớp route cũ `members/{memberId}`); `blocked[]` trả cả `member_id` +
  `employee_id` + `name` + `reason` (+ `open_task_count`).
- (Claude) "Cả công ty": API xem trước trả **danh sách id** (FE cần để tính dòng tổng / trùng), trần 3.000 người/nhóm vai trò (như
  `department_member_ids` nâng từ 2.000); BE thêm trong 1 transaction, insert theo lô 500 dòng.
- (Claude) Tin hệ thống / realtime: 1 `WorkspaceActivity` loại mới `members_bulk` (payload: action add|role|remove, đếm theo vai trò,
  ≤ 3 tên) ⇒ 1 tin + 1 `conversation.updated`; các loại cũ giữ nguyên cho thao tác 1 người.
- **User chốt ("ok" 16/11/2026, phương án đề xuất)**: lô đổi vai trò / mời ra chứa MỌI Quản lý ⇒ **giữ lại người đang thao tác**
  làm Quản lý (vào `blocked` lý do "Nhóm phải còn ít nhất 1 Quản lý"), đổi / mời những người còn lại. Người thao tác chỉ tự hạ / tự
  rời được khi ngoài lô còn Quản lý khác.
- User xác nhận 3 điểm Claude chọn ở §7 (Cả công ty = công ty của nhóm · đổi phần được + báo bị chặn · thêm người đã có thì bỏ qua).
