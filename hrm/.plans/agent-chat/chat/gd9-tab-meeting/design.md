# GĐ9 — Tab Meeting trong Nhóm trao đổi

- **Ngày:** 14/11/2026 · **Phụ trách:** @namdangit · **Mockup:** `mockup.html` (cùng thư mục)
- **Nguồn spec gốc:** `docs/superpowers/specs/gop-db/2026-11-02-phan-he-cong-viec-design.md` §5.1 "Tab Meeting chung" (dòng ~382)
  — bản đó ghi bảng nối nhiều–nhiều [C]; **14/11 user chốt lại: 1 meeting thuộc tối đa 1 nhóm** (xem Q1).
- **Trạng thái:** design + mockup, CHƯA có lệnh code.

## Mục tiêu
Nhóm trao đổi có thêm mục **Meeting** cạnh Nhiệm vụ: xem mọi cuộc họp của nhóm, tạo meeting ngay từ nhóm (điền sẵn
nhóm + mời nhanh thành viên), và nhóm chat được báo khi lịch họp thay đổi. Nghiệp vụ meeting (biên bản, điểm danh,
phòng họp, đổi trạng thái) **giữ nguyên** — tab chỉ là lối vào theo nhóm.

## Quyết định đã chốt (user 14/11: "Cả 3 đều chọn theo đề xuất")
- **Q1 — 1 meeting thuộc tối đa 1 nhóm:** cột `meetings.workspace_id` (nullable, index), giống `tasks.workspace_id`.
  Không bảng nối.
- **Q2 — Ai thấy:** mọi thành viên nhóm thấy mọi meeting của nhóm (gate = thành viên, như tab Nhiệm vụ). Meeting
  **Đang tạo (nháp)** chỉ người tạo + chủ trì thấy (giữ luật nháp hiện có của `MeetingCriteria`).
  Mở chi tiết meeting từ tab: `Meeting::canView()` phải cho thành viên nhóm xem meeting thuộc nhóm (bổ sung 1 nhánh).
- **Q3 — Chưa cho gắn meeting có sẵn:** chỉ meeting TẠO TỪ NHÓM mới vào tab. Để sau: nút "Gắn meeting có sẵn".

## Thiết kế (Claude đề xuất, user duyệt hướng 14/11 — chi tiết xem mockup)
1. **Bật / tắt:** ⚙ Cấu hình › "Tab sử dụng" thêm công tắc **Meeting** (chỉ Quản lý nhóm), mặc định tắt. BE đã có sẵn
   `'meetings'` trong `Workspace::OPTIONAL_TABS` + validate `enabled_tabs`. Tắt khi còn meeting sắp họp ⇒ hỏi xác nhận
   (như Nhiệm vụ); meeting vẫn giữ `workspace_id`, bật lại là hiện.
2. **Dải tab:** `Nhiệm vụ · Meeting · Thành viên` (+ ⚙). Màu Meeting `#7C3AED`, icon `ri-calendar-event-line`.
   Số trên tab = **số cuộc sắp họp** (Lên lịch + Chốt lịch, `start_date >= hôm nay`) mà người xem thấy được.
3. **Danh sách** (`?panel=meetings`): thanh công cụ cùng khuôn tab Nhiệm vụ — ô tìm (mã, tên), chip nhanh
   `Sắp họp · Đã họp · Đã huỷ · Tất cả`, nút **Tạo meeting** (primary). Gom 3 nhóm:
   - **Sắp họp**: Lên lịch / Chốt lịch, chưa qua giờ kết thúc — sớm nhất lên đầu; dòng hôm nay có nhãn "Hôm nay".
   - **Đã họp**: Hoàn thành + (Lên lịch / Chốt lịch đã qua giờ kết thúc, hiện "Chưa cập nhật kết quả") — mới nhất lên đầu.
   - **Đã huỷ**: thu gọn mặc định.
   - Nháp (Đang tạo) của mình: nằm đầu "Sắp họp" với badge Đang tạo.
   Mỗi dòng: khối ngày (thứ + ngày) · tên + mã · giờ bắt đầu–kết thúc · hình thức (Trực tiếp: phòng / địa điểm;
   Online: nhãn Online) · chủ trì (avatar) · số người dự · badge trạng thái (`status_name` + `status_color` từ BE) ·
   biểu tượng biên bản (có / chưa). Bấm dòng ⇒ `/assign/meeting/{id}/show?from=workspace&workspace_id=…`, Quay lại về tab.
   Phân trang theo nhóm (20 dòng/nhóm, "Xem thêm").
4. **Tạo meeting từ nhóm:** nút Tạo meeting ⇒ trang tạo hiện có `/assign/meeting/create?workspace_id=…&from=workspace`.
   - Form hiện ô **Nhóm trao đổi** (điền sẵn, khoá, chỉ hiện khi đi từ nhóm) cạnh tiêu đề.
   - Khối "Thành phần tham dự" có nút **Mời tất cả thành viên nhóm (N)** — thêm 1 lần, bỏ người đã có; vẫn sửa tay được.
   - Lưu xong (mọi kiểu lưu) ⇒ về `/assign/workspaces/{id}?panel=meetings`.
   - BE `store`: nhận `workspace_id`, chỉ chấp nhận khi người tạo là thành viên nhóm + nhóm đang mở; còn lại bỏ qua/422.
   - Sửa meeting: KHÔNG đổi được nhóm (Q1/Q3 — không gắn/chuyển nhóm ở đợt này).
5. **Báo trong chat** (tin hệ thống, dùng `MessageService::system` có sẵn, meta `{meeting_id}`; bấm ⇒ mở meeting):
   - Tạo với trạng thái Lên lịch / Chốt lịch: `📅 A đã lên lịch họp: <Tên> — 14:00 15/11`
   - Chuyển Chốt lịch: `✅ A đã chốt lịch họp: <Tên> — 14:00 15/11`
   - Đổi giờ họp (meeting chưa diễn ra): `🕑 A đã dời họp <Tên> sang 09:00 16/11`
   - Huỷ: `✖ A đã huỷ họp: <Tên>`
   - Nháp (Đang tạo) KHÔNG báo. Hoàn thành KHÔNG báo ở đợt này.

## Ngoài phạm vi đợt này
Gắn meeting có sẵn vào nhóm · chuyển meeting sang nhóm khác · thẻ meeting dạng card trong chat · tab Meeting ở app
mobile · nhắc họp trong chat trước giờ họp · tab Meeting cho Dự án KH (đang dùng tab riêng của TKT/GP).

## Ảnh hưởng
- `MeetingController::store/update/changeStatus` (+ service) — thêm `workspace_id` + bắn tin hệ thống.
- `MeetingCriteria` KHÔNG đổi (màn danh sách meeting chung giữ nguyên quyền). Tab dùng API riêng
  `GET workspaces/{id}/meetings` (middleware `CheckWorkspaceAccess:member`), giống `WorkspaceTaskController`.
- `Meeting::canView()` thêm nhánh: thành viên nhóm của meeting (không áp cho nháp).
- `MeetingForm.vue` (1.867 dòng, dùng chung tạo/sửa) — thêm ô nhóm khoá + nút mời; chỉ hiện khi có `workspace_id`.
- Migration mới: `add_workspace_id_to_meetings_table` (cột + index), không đổi dữ liệu cũ.

## Phạm vi code dự kiến (hỏi riêng trước khi làm)
hrm-api + hrm-client · nhánh mới tách từ `gop_db-chat-giao-dien` (GĐ8 chưa lên gop_db) · 1 migration chạy vào
`db_gop_6_11` · PHPUnit + e2e spec mới `workspace-meetings.spec.ts` (có ca không quyền: người ngoài nhóm 403,
thành viên không thấy nháp người khác).
