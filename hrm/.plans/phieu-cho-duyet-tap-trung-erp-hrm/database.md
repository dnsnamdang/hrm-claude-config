# Thiết kế database — Phiếu chờ duyệt tập trung (HRM) — @cuong61n

Ngày 13/11/2026. Dựa trên: code `hrm-api` đang chạy, kết quả khảo sát từng loại phiếu (`danh-gia-tung-phieu.md`), và bảng registry cũ bên ERP `develop_01` (chỉ để tham khảo — nhánh đó không có trên `gop_db` / prod). ERP sẽ bỏ nên bảng nằm hoàn toàn ở HRM, migration ở `hrm-api`, KHÔNG dùng `mysql2`.

## 1. Vì sao cần bảng gom (registry) thay vì gom lúc mở màn
- Có khoảng 55 loại phiếu ở ~50 bảng khác nhau; mỗi loại có trạng thái, cấp duyệt và cách xác định "ai duyệt" riêng (quyền mã mới, tên quyền cũ, người duyệt đích danh, quản lý phòng, thủ kho, NV mua hàng được phân công…). Gom lúc mở màn = mỗi lần mở chạy hàng chục truy vấn khác nhau, và không thể đếm số phiếu theo phân hệ cho badge menu.
- Registry là **bảng tóm tắt**, mỗi phiếu đang chờ 1 dòng, được cập nhật mỗi khi phiếu nguồn đổi trạng thái. Danh sách, số đếm và badge đều đọc từ đây (1 truy vấn có index).
- KHÔNG lưu nội dung nghiệp vụ của từng loại (đã bỏ xem nhanh): chỉ lưu những cột chung mà danh sách hiện.

## 2. Bảng `approval_inbox_items` — 1 dòng / 1 phiếu đang ở 1 cấp
| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| id | bigint PK | |
| doc_type | varchar(64) | khoá loại phiếu (vd `bill_payment_request`, `attendance`) |
| doc_type_label | varchar(191) | tên hiển thị = tên màn trong menu HRM (snapshot) |
| subsystem_key | varchar(32) | phân hệ chủ (`finance`, `assign`, `timesheet`, `training`, `operation`, `insurance`, `transport`, `customer-care`…) — dùng cho nhóm / chip |
| source_table, source_id | varchar(64), bigint | phiếu gốc |
| code | varchar(64) | mã phiếu |
| partner_type, partner_id, partner_name | tinyint null (1 KH, 2 NCC), bigint null, varchar(255) null | đối tác (snapshot tên) |
| requester_id | bigint | người yêu cầu = `employees.id` (tên lấy bằng subquery, không join) |
| company_id, department_id, part_id | bigint null | cấp tổ chức theo quy ước dự án |
| document_date | datetime null | ngày tạo phiếu |
| submitted_at | datetime null | ngày gửi duyệt |
| step | tinyint | cấp thứ mấy trong luồng của loại phiếu |
| status_code | int | status ở bảng nguồn |
| status_text, status_color | varchar(191), char(7) | **đúng chữ + màu BE của phiếu trả** (cột "Cấp duyệt") — snapshot để khỏi join 50 bảng |
| level_started_at | datetime | lúc phiếu vào cấp hiện tại (cột "Đã chờ", mặc định ẩn) |
| amount, currency_code | decimal(20,2) null, varchar(8) null | chỉ loại phiếu có tiền; cột tuỳ chọn |
| amount_permission | varchar(191) null | nếu có: người không có quyền này không thấy số tiền |
| gate_type | varchar(24) | `permission` · `approver` · `dept_manager` · `assignee_list` |
| required_permission | varchar(191) null | mã quyền (hoặc TÊN quyền cũ) cần có |
| permission_kind | varchar(8) | `code` hay `name` — vì nhiều màn còn dùng tên quyền tiếng Việt |
| alt_permissions | json null | quyền thay thế (điều kiện HOẶC, vd Yêu cầu nhập hàng TP/BKS) |
| gate_scope | varchar(12) | `company` · `department` · `part` · `none` — phạm vi áp quyền |
| handler_path | varchar(255) | đường dẫn FE mở phiếu, vd `/finance/bill-payment-requests/123` |
| state | tinyint | 1 chờ · 2 đã duyệt · 3 từ chối · 4 huỷ · 5 đóng (không xác định được kết quả) |
| round | tinyint | lần gửi (gửi lại sau khi bị trả về thì +1) |
| resolved_at, resolved_by | datetime null, bigint null | khi rời trạng thái chờ |
| created_by, updated_by, timestamps | | theo quy ước (sync hệ thống để null) |

Index: `unique(doc_type, source_id)` · `(state, company_id, subsystem_key)` · `(state, requester_id)` · `(state, required_permission, company_id)` · `(state, department_id)` · `(subsystem_key, doc_type, state)`.

## 3. Bảng `approval_inbox_assignees` — chỉ cho gate đích danh
Dùng khi người duyệt là **một người cụ thể**: `approver_id` trên phiếu, thủ kho của kho trên phiếu, NV mua hàng được phân công, người lập phiếu gốc. Cột: `id`, `item_id`, `employee_id`, `role varchar(24)`. `unique(item_id, employee_id)`, index `(employee_id, item_id)`.
Gate theo quyền / quản lý phòng KHÔNG đổ thành từng dòng (sẽ nổ hàng nghìn dòng khi đổi vai) — lọc bằng cột `required_permission` + `gate_scope` + `manageDepartmentIdsOf()`.

## 4. Bảng `approval_inbox_logs` — mỗi cấp đã kết thúc 1 dòng
`id`, `item_id`, `doc_type`, `source_id`, `code` (giữ lại dù item bị đóng), `round`, `step`, `status_text`, `actor_id`, `action` (`submit` · `approve` · `reject` · `cancel` · `return`), `started_at`, `ended_at`, `note varchar(1000)`. Index `(item_id)`, `(actor_id, ended_at)`, `(doc_type, source_id)`.
Phục vụ: popup "Lịch sử duyệt", chế độ "Tôi đã xử lý", và báo cáo thời gian chờ từng cấp.

## 5. Ai thấy phiếu nào (truy vấn "chờ tôi duyệt")
```
state = 1 AND (company_id IS NULL OR company_id = <công ty đang làm>)
AND ( EXISTS assignee(employee_id = tôi)
   OR (gate_type='permission' AND required_permission IN (<quyền của tôi>) AND <khớp gate_scope>)
   OR (gate_type='dept_manager' AND department_id IN manageDepartmentIdsOf(tôi, công ty)) )
```
- "Quyền của tôi" lấy từ tầng phân quyền hiện có (mã quyền theo Catalog + tên quyền cũ), đệm trong `RequestCache` cho 1 request.
- Quyền xem màn `admin.phieu_cho_duyet.view` (khai trong `app/Support/Permissions/Catalog/admin.php`, không seeder) chỉ mở màn; **danh sách luôn lọc theo gate ở SQL**, FE không quyết định gì.
- Chế độ "Phiếu tôi gửi" = `state=1 AND requester_id = tôi`; "Tôi đã xử lý" = đọc `approval_inbox_logs` theo `actor_id = tôi`.
- Số đếm theo phân hệ: 1 truy vấn `GROUP BY subsystem_key` cùng điều kiện trên.

## 6. Cập nhật dữ liệu (không làm hỏng nghiệp vụ gốc)
- Mỗi loại phiếu có 1 lớp **Definition** viết bằng code (không phải cấu hình): trả về cấp hiện tại, status_text/color, gate, đối tác, người yêu cầu… vì trạng thái và cách xác định người duyệt mỗi loại khác nhau (đã khảo sát).
- Trait `SyncsApprovalInbox` gắn vào model nguồn: sự kiện `saved` + `deleted` gọi `ApprovalInboxService::sync($docType, $id)` **sau khi commit**; lỗi chỉ ghi log, không làm hỏng giao dịch gốc. Chỗ nào ghi bằng query-builder (`->update()`) thì gọi `sync()` tường minh.
- `sync()` **idempotent**: tính cấp hiện tại → so với dòng registry → tạo / giữ (cập nhật cột chung) / chuyển cấp (ghi 1 dòng log cho cấp cũ) / đóng. Gọi lặp không sinh log trùng.
- Lệnh `approval-inbox:backfill` chạy 30 phút/lần quét lại mọi loại phiếu đang chờ, sửa dòng lệch và đóng dòng thừa (lưới an toàn khi sự kiện bị bỏ sót).
- Tên bảng cố ý khác bảng cũ `approval_inbox` của ERP `develop_01` để khỏi đụng nhau nếu nhánh đó có lúc được gộp.

## 7. Dùng lại, không tạo mới
- Cột hiển thị theo người dùng: bảng `user_column_settings` (`columnScreenKey = approval_inbox`).
- Bố cục bộ lọc theo người dùng: bảng `filter_customizations` (`table = approval_inbox`).

## 8. Tuỳ chọn — chỉ làm nếu giữ các tính năng tương ứng
- `approval_inbox_reminders` (item_id, from_employee_id, created_at): giới hạn "Nhắc duyệt" 1 lần/phiếu/ngày.
- `approval_inbox_user_states` (employee_id, item_id, pinned, snooze_until): ghim / nhắc lại sau.
- Bộ lọc đã lưu: dùng lại cơ chế cài đặt bộ lọc hiện có.

## 9. Rủi ro và cách xử lý
- **Lệch dữ liệu** giữa registry và phiếu gốc → `backfill` định kỳ + lệnh đối soát đếm số phiếu chờ của từng loại so với bảng nguồn.
- **Lộ phiếu cho người không có quyền** (một số màn `type=waiting` hiện trả cả phiếu của chính người xem) → registry lọc bằng gate ở SQL, không tái dùng các endpoint đó.
- **Mở phiếu** vẫn bị kiểm quyền lại ở endpoint của từng module; registry chỉ quyết định "hiện trong danh sách hay không".
- **Chữ trạng thái đổi** → snapshot được làm mới mỗi lần `sync()`; muốn đổi hàng loạt thì chạy `backfill`.
- Loại phiếu nào chưa viết Definition thì chưa có trong màn (làm dần theo nhóm: Tài chính, Công việc, Chấm công… ).
