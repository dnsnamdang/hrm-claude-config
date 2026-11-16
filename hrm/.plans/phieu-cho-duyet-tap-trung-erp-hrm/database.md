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
| source_subsystem | varchar(32) | phân hệ NGUỒN của phiếu (đổi tên từ `subsystem_key` 16/11/2026 để khỏi lẫn với phân hệ "Trung tâm phê duyệt"; `finance`, `assign`, `timesheet`, `training`, `operation`, `insurance`, `transport`, `customer-care`…) — dùng cho nhóm / chip |
| source_table, source_id | varchar(64), bigint | phiếu gốc |
| code | varchar(64) | mã phiếu |
| partner_type, partner_id, partner_name | tinyint null (1 KH, 2 NCC), bigint null, varchar(255) null | đối tác (snapshot tên) |
| requester_id | bigint | người yêu cầu = `employees.id` (tên lấy bằng subquery, không join) |
| company_id, department_id, part_id | bigint null | cấp tổ chức theo quy ước dự án |
| submitted_at | datetime | **Ngày gửi duyệt** — ngày DUY NHẤT hiện ở danh sách (cột, lọc, sắp xếp). Bỏ hẳn "Ngày tạo" (user chốt 15/11/2026). Lấy từ cột ngày gửi của bảng nguồn; loại nào không có thì lấy lúc `sync()` thấy phiếu vào trạng thái chờ lần đầu |
| step | tinyint | cấp thứ mấy trong luồng của loại phiếu |
| status_code | int | status ở bảng nguồn |
| status_text, status_color | varchar(191), char(7) | **đúng chữ + màu BE của phiếu trả** (cột "Cấp duyệt") — snapshot để khỏi join 50 bảng |
| level_started_at | datetime | lúc phiếu vào cấp hiện tại (cột "Đã chờ", mặc định ẩn) |
| amount, currency_code | decimal(20,2) null, varchar(8) null | số tiền chính, **nguyên tệ** + mã tiền (VND/USD). Loại đã là VND quy đổi thì currency_code = VND. `sync()` tính sẵn (nhiều loại phải SUM từ bảng dòng, hoặc lấy cột theo cấp — xem `cot-gia-tri.md`). Điểm công khoán KHÔNG lưu vào đây. Không sắp xếp / không cộng tổng cột này |
| amount_label | varchar(64) null | nhãn con số này của riêng loại phiếu ("Số tiền đề nghị", "Giá trị hợp đồng"…) để rê chuột / dòng phụ không gây hiểu nhầm |
| amount_permission, amount_scope | varchar(191) null, varchar(12) null | nếu có: người xem không có quyền này (trong phạm vi) thì BE trả `amount = null` + `amount_hidden = true` (FE hiện `*****`). Hiện chỉ Hợp đồng TKT (`hide_price`, quyền `sale.hop_dong_an_gia.view`); giá vốn / biên lãi báo giá che riêng |
| gate_note | varchar(255) null | mô tả ngắn điều kiện duyệt của cấp này (vd "mã don_xin_nghi.approve + quản lý phòng người đề nghị") — chỉ để gỡ lỗi / hiện tooltip, KHÔNG dùng để lọc (16/11/2026: bỏ 5 cột gate cũ `gate_type`, `required_permission`, `permission_kind`, `alt_permissions`, `gate_scope` vì gate thật là AND/OR nhiều điều kiện, không khai được bằng cột) |
| gate_blocker | varchar(191) null | rào chắn tính theo NGƯỜI bấm chứ không theo phiếu (chặn trưởng phòng còn hàng quá hạn `checkDueConfigsManager`, trần giờ làm thêm/tháng…) — chỉ để cảnh báo, không loại phiếu khỏi danh sách |
| handler_path | varchar(255) | đường dẫn FE mở phiếu, vd `/finance/bill-payment-requests/123` |
| state | tinyint | 1 chờ · 2 đã duyệt · 3 từ chối · 4 huỷ · 5 đóng (không xác định được kết quả) |
| round | tinyint | lần gửi (gửi lại sau khi bị trả về thì +1) |
| resolved_at, resolved_by | datetime null, bigint null | khi rời trạng thái chờ |
| created_by, updated_by, timestamps | | theo quy ước (sync hệ thống để null) |

Index: `unique(doc_type, source_id)` · `(state, approvable, company_id, source_subsystem)` · `(source_subsystem, doc_type, state)`.

## 3. Bảng `approval_inbox_assignees` — DANH SÁCH NGƯỜI ĐƯỢC DUYỆT cấp hiện tại (sửa 16/11/2026)
Sau khi đọc code quyền duyệt của từng màn (6 báo cáo ở `quyen-duyet/`), gate thật là tổ hợp **AND / OR** của: mã quyền (hoặc TÊN quyền cũ), quản lý phòng của người đề nghị / của phiếu (4 kiểu tính "quản lý" khác nhau), người đích danh (`approver_id`, thủ kho, NV mua hàng, người phụ trách phòng họp), kiểm công ty… Không khai được bằng vài cột. Nên **mọi** loại phiếu dùng 1 cơ chế duy nhất: lúc `sync()`, Definition tính ra CHÍNH XÁC những ai đang duyệt được phiếu ở cấp này và ghi vào bảng này.
- Cột: `id`, `item_id`, `employee_id` (= `employees.id`, KHÔNG phải `employee_infos.id`), `role varchar(24)` (`approver` · `manager` · `named` …, chỉ để hiển thị). `unique(item_id, employee_id)`, index `(employee_id, item_id)`.
- Cách tính trong Definition: `approvers($item)` trả danh sách `employees.id` — dùng ĐÚNG logic của cờ `can_approve` ở Entity của loại đó (nguồn duy nhất, FE/BE/`authorize()` đều dùng), với các công cụ có sẵn: `PermissionChecker::holders(mã, công ty)` (người giữ quyền), `employee_manage_departments` (+ cờ `all_department`) cho "quản lý phòng", cột `approver_id` / bảng thủ kho… Kiểu "quản lý" và kiểu "công ty" mỗi loại khai riêng (strict / cộng phòng mình / công ty gốc).
- Quy mô ước tính: ~2.200 phiếu đang chờ × vài đến vài chục người duyệt = hàng chục nghìn dòng, chấp nhận được; đổi lại danh sách, số đếm và badge đều chính xác bằng 1 JOIN, không phải đoán quyền lúc đọc.
- Làm mới: (1) mỗi lần phiếu đổi (`sync()`), (2) khi đổi vai trò / quyền / `employee_manage_departments` / kiêm nhiệm → sync lại các phiếu đang chờ bị ảnh hưởng (hook vào chỗ ghi `role_permission_history` và màn Quản lý phòng), (3) `backfill` 30 phút là lưới an toàn. Lệch tối đa 30 phút nếu sót sự kiện. **Chốt thật vẫn ở lúc bấm duyệt**: endpoint của từng loại kiểm lại `can_approve` — registry chỉ quyết định "hiện hay không".
- Rào chắn theo người (`checkDueConfigsManager`, trần giờ OT) KHÔNG loại phiếu khỏi danh sách; hiện cảnh báo khi bấm (cột `gate_blocker`).

## 4. Bảng `approval_inbox_logs` — mỗi cấp đã kết thúc 1 dòng
`id`, `item_id`, `doc_type`, `source_id`, `code` (giữ lại dù item bị đóng), `round`, `step`, `status_text`, `actor_id`, `action` (`submit` · `approve` · `reject` · `cancel` · `return`), `started_at`, `ended_at`, `note varchar(1000)` (= **nhận xét khi duyệt** / lý do từ chối), `changes json null` (**thông tin người duyệt đã sửa khi duyệt**: `[{field, old, new}]`, vd Số tiền duyệt 5,000,000 → 4,500,000; dùng đúng dạng cũ→mới của lịch sử chung). Index `(item_id)`, `(actor_id, ended_at)`, `(doc_type, source_id)`.
Phục vụ: popup "Lịch sử duyệt" và báo cáo thời gian chờ từng cấp. (Đã bỏ chế độ "Tôi đã xử lý" — user chốt 15/11/2026.)

## 5. Ai thấy phiếu nào (truy vấn "chờ tôi duyệt")
```
SELECT i.* FROM approval_inbox_items i
JOIN approval_inbox_assignees a ON a.item_id = i.id AND a.employee_id = <tôi>
WHERE i.state = 1 AND i.approvable = 1
  AND (i.company_id IS NULL OR i.company_id = <công ty đang làm>)
```
- Màn CHỈ có chế độ "Chờ tôi duyệt" (user chốt 15/11/2026). `requester_id` chỉ để hiện cột Người yêu cầu / lọc.
- Quyền xem màn `approval_center.phieu_cho_duyet.view` (Catalog `approval_center.php`, cấp rộng cho mọi vai trò — user chốt 16/11/2026) chỉ mở màn; danh sách luôn lọc ở SQL theo bảng assignees.
- Số đếm theo phân hệ: cùng JOIN + `GROUP BY source_subsystem`.
- **Một người giữ nhiều cấp của cùng 1 phiếu**: registry chỉ giữ cấp HIỆN TẠI. Duyệt xong cấp 1 → `sync()` chuyển phiếu sang cấp 2 → nếu người đó cũng giữ cấp 2 thì phiếu lại hiện trong danh sách của họ (đúng hành vi các màn hiện tại: phải bấm lần lượt). Ngoại lệ tự nhảy cấp do chính code nguồn (Hợp đồng TKT khi TP giữ thêm quyền BGĐ, Tra soát công khi có cả `confirm` + `approve`, Kế hoạch NV khi người lập là trưởng phòng): registry không can thiệp, chỉ đọc trạng thái mới. Duyệt hàng loạt gọi hàm duyệt lẻ ĐÚNG 1 lần cho mỗi phiếu và báo kết quả "phiếu đã sang cấp tiếp theo" — không lặp qua nhiều cấp.
- **Người tạo tự duyệt**: code hiện tại KHÔNG chặn ở hầu hết loại (chỉ Kế hoạch NV chặn). Chờ user chốt registry có loại phiếu do chính người xem tạo ra khỏi danh sách "chờ tôi duyệt" hay không.

## 6. Cập nhật dữ liệu (không làm hỏng nghiệp vụ gốc)
- Mỗi loại phiếu có 1 lớp **Definition** viết bằng code (không phải cấu hình): trả về cấp hiện tại, status_text/color, danh sách người duyệt (`approvers()`), đối tác, người yêu cầu… vì trạng thái và cách xác định người duyệt mỗi loại khác nhau (đã khảo sát).
- Trait `SyncsApprovalInbox` gắn vào model nguồn: sự kiện `saved` + `deleted` gọi `ApprovalInboxService::sync($docType, $id)` **sau khi commit**; lỗi chỉ ghi log, không làm hỏng giao dịch gốc. Chỗ nào ghi bằng query-builder (`->update()`) thì gọi `sync()` tường minh.
- `sync()` **idempotent**: tính cấp hiện tại → so với dòng registry → tạo / giữ (cập nhật cột chung) / chuyển cấp (ghi 1 dòng log cho cấp cũ) / đóng. Gọi lặp không sinh log trùng.
- Lệnh `approval-inbox:backfill` chạy 30 phút/lần quét lại mọi loại phiếu đang chờ, sửa dòng lệch và đóng dòng thừa (lưới an toàn khi sự kiện bị bỏ sót).
- Tên bảng cố ý khác bảng cũ `approval_inbox` của ERP `develop_01` để khỏi đụng nhau nếu nhánh đó có lúc được gộp.

## 7. Dùng lại, không tạo mới
- Cột hiển thị theo người dùng: bảng `user_column_settings` (`columnScreenKey = approval_inbox`).
- Bố cục bộ lọc theo người dùng: bảng `filter_customizations` (`table = approval_inbox`).

## 8. Tuỳ chọn — chỉ làm nếu giữ các tính năng tương ứng
- ~~`approval_inbox_reminders`~~ — BỎ (nút Nhắc duyệt thuộc chế độ "Phiếu tôi gửi" đã bỏ).
- `approval_inbox_user_states` (employee_id, item_id, pinned, snooze_until): ghim / nhắc lại sau.
- Bộ lọc đã lưu: dùng lại cơ chế cài đặt bộ lọc hiện có.

## 9. Rủi ro và cách xử lý
- **Lệch dữ liệu** giữa registry và phiếu gốc → `backfill` định kỳ + lệnh đối soát đếm số phiếu chờ của từng loại so với bảng nguồn.
- **Lộ phiếu cho người không có quyền** (một số màn `type=waiting` hiện trả cả phiếu của chính người xem) → registry lọc bằng gate ở SQL, không tái dùng các endpoint đó.
- **Mở phiếu** vẫn bị kiểm quyền lại ở endpoint của từng module; registry chỉ quyết định "hiện trong danh sách hay không".
- **Chữ trạng thái đổi** → snapshot được làm mới mỗi lần `sync()`; muốn đổi hàng loạt thì chạy `backfill`.
- Loại phiếu nào chưa viết Definition thì chưa có trong màn (làm dần theo nhóm: Tài chính, Công việc, Chấm công… ).

## 10. Khả năng của từng loại phiếu (khai trong lớp Definition — bằng code, không phải cột DB)
Quyết định 15/11/2026 sau nhận xét của người dùng: ~55 loại có cách duyệt khác nhau nên khả năng duyệt phải khai THEO LOẠI, không đoán chung.
- `approve_mode`: `inline` = duyệt ngay ở danh sách được (không phải nhập / chọn thêm) · `open` = khi duyệt phải nhập/sửa thêm (tiền từng cấp, công khoán, chọn PM, trùng lịch…) → chỉ có nút "Xem & duyệt" mở phiếu trên HRM.
- `reject_mode`: `reason` (bắt buộc lý do — hầu hết) · `open` (từ chối cũng phải vào phiếu).
- `bulk`: bool — chỉ bật khi `approve_mode = inline` VÀ endpoint duyệt của loại đó ĐÃ kiểm quyền + phòng/công ty ở BE (xem các lỗ hổng trong `danh-gia-tung-phieu.md`). Mới thêm loại vào danh sách bulk sau khi vá.
- `comment_field` / `reason_field`: tên trường nhận xét / lý do trên bảng nguồn (mỗi loại một tên: note, comment, reason, approver_comment…) → `sync()` đọc ra điền `approval_inbox_logs.note`.
- Duyệt hàng loạt: `POST approval-center/inbox/bulk` `{action, doc_type, ids[≤50], comment}`; mỗi phiếu đi qua ĐÚNG hàm duyệt lẻ của loại đó (kiểm lại gate từng phiếu), trả kết quả từng phiếu; phiếu lỗi không chặn phiếu khác. Một lô chỉ chứa MỘT loại.

- Cột Giá trị: chi tiết từng loại (bảng · cột · đơn vị · quyền che) ở `cot-gia-tri.md`. Phạm vi giai đoạn 1 chờ user chốt (xem mục 5 file đó).

## 11. Phân hệ riêng "Trung tâm phê duyệt" (user chốt 16/11/2026)
- Không còn nằm trong Quản trị hệ thống. Khai mới trong `components/subsystems.js`: key/slug `approval-center`, layout `default-sidebar`, menu `subsystem-menu/approval-center.js`, `permissionType` = số tiếp theo sau số lớn nhất hiện có (đang thấy 29 → 30, kiểm lại khi làm). Nhóm: đề xuất VĂN PHÒNG SỐ, xếp đầu (chờ user xác nhận).
- Menu giai đoạn 1: **Tổng quan** (`/approval-center/dashboard`) và **Phiếu chờ duyệt** (`/approval-center/inbox`, kèm số đếm theo phân hệ nguồn). Báo cáo thời gian duyệt để giai đoạn sau (đọc từ `approval_inbox_logs`).
- Mã quyền mới: `approval_center.phieu_cho_duyet.view`; API tiền tố `approval-center/…`. Tên bảng `approval_inbox_*` giữ nguyên.
- Badge tổng số phiếu chờ trên topbar + thẻ phân hệ ở màn chọn phân hệ: 1 endpoint đếm có cache.
- Mở phiếu sang phân hệ gốc theo `handler_path`; nút Quay lại về Trung tâm phê duyệt (query `from=approval-center`).
- App TPE_APP: thêm phân hệ thứ 6 (màu riêng, tab đáy, header gradient theo skill `app-module-shell`).

## 12. Số liệu màn Tổng quan (dashboard) — sửa 16/11/2026 theo dữ liệu có thật
Nguyên tắc (user chốt: vẽ phải làm được với code đang chạy): chỉ vẽ khối nào tính được từ `approval_inbox_items` của các phiếu ĐANG chờ. Mọi khối cần lịch sử duyệt đã bỏ, vì HRM chưa có nơi nào lưu "ai duyệt lúc nào" thống nhất cho ~55 loại; `approval_inbox_logs` chỉ đầy dần từ ngày go-live.
- **Cột mới `approvable` (tinyint) + `blocked_reason` (varchar 191 null)** ở `approval_inbox_items`: Definition tính phiếu còn duyệt được không. Có thật trong code: Đăng ký làm thêm, Phiếu yêu cầu làm thêm, Đi muộn về sớm và Đơn nghỉ đã quá mốc thì BE không cho duyệt nhưng phiếu vẫn "chờ" (prod 21/10: làm thêm 131 + 212, đi muộn 28). Nhóm này KHÔNG tính vào "Chờ tôi duyệt", hiện ở dải cảnh báo + thẻ "Không còn duyệt được" để đóng/huỷ. (Chờ user chốt: có tự đóng không.)
- **Không có khái niệm "quá hạn / trễ hạn"**: HRM không có hạn duyệt chung cho phiếu. Chỉ hiện số ngày đã chờ (từ `level_started_at`), chia 4 khoảng bằng dải màu xanh nhạt → đậm, không dùng cam/đỏ, không đặt mốc.
- **Chờ tôi duyệt / Mới gửi hôm nay / Chờ trung bình / Chờ lâu nhất / Thời gian đã chờ**: `approval_inbox_items` (`state=1 AND approvable=1`, gate như mục 5). ⚠ Đúng chỉ khi `submitted_at` và `level_started_at` lấy ĐÚNG cột ngày của bảng nguồn từng loại (Definition phải khai). Loại nào không có cột ngày thì backfill lần đầu sẽ gán cùng 1 giờ → "Chờ lâu nhất" sai; loại đó hiện "—" ở khối này cho tới khi có dữ liệu thật (cần rà từng loại trước khi làm).
- **Phiếu chờ theo phân hệ**: `GROUP BY source_subsystem`. **Loại phiếu chờ nhiều nhất**: `GROUP BY doc_type` top 6. **Phiếu chờ lâu nhất**: top 5 `ORDER BY level_started_at`; cột Giá trị theo `cot-gia-tri.md` (không có tiền → "—", bị che → `*****`); "Cấp duyệt" = `status_text`/`status_color` BE trả.
- **Có thể duyệt hàng loạt**: `GROUP BY doc_type` chỉ với loại có `bulk = true` (mục 10) — ví dụ khả dĩ theo `danh-gia-tung-phieu.md`: Đặt phòng họp, Gia hạn dự án TKT, Đơn kết thúc nghỉ phép / đi muộn (loại "N", không phải nhập thêm). Làm thêm / Đơn nghỉ là "N*" (BE có thể trả 422) và nhiều loại BE chưa kiểm quyền (mục 8, mục 7.6 của file đó) → chưa bật bulk cho tới khi vá.
- **ĐÃ BỎ khỏi bản vẽ** (không tính được lúc go-live): Đã duyệt 30 ngày, đường xu hướng "gửi đến / đã duyệt", "so với hôm qua", sparkline, duyệt nhanh nhất, ô chọn 7 ngày / 30 ngày / Quý, "Theo cấp duyệt" (chữ trạng thái mỗi module một kiểu: "Gửi TP duyệt" ≠ "Chờ TP duyệt" nên gộp sẽ vỡ). Làm lại ở giai đoạn sau khi `approval_inbox_logs` đã tích đủ dữ liệu và biết chắc người duyệt của từng loại.
- Gộp 1 endpoint `GET approval-center/dashboard` (cache ngắn theo người dùng) để màn chỉ gọi 1 API.

## 13. Kết quả đọc code quyền duyệt từng màn (16/11/2026)
6 báo cáo chi tiết (có file:dòng) ở `quyen-duyet/00..05-*.md`. Điểm chốt cho thiết kế:
- Quyền Duyệt **không có phạm vi** (chỉ quyền Xem có 1–4). "Phạm vi" của việc duyệt là điều kiện AND nằm trong code từng màn: mã quyền AND quản lý phòng; hoặc `approver_id` đích danh (khi có thì chỉ người đó duyệt, không cần mã); hoặc quyền riêng theo kho / phòng họp / thương hiệu.
- "Quản lý phòng" = bảng `employee_manage_departments` (+ `all_department`), không phân biệt trưởng/phó/giám đốc, không kế thừa phòng con; có 3–4 cách tính khác nhau giữa các màn.
- Cờ `can_approve` / `can_reject` ở Entity là nguồn duy nhất ở nhóm Chấm công/Nhân sự, dùng cho nút FE + `FormRequest::authorize()`; Definition của registry phải gọi lại đúng logic này.
- Các điểm không khai được bằng cột và phải tính trong `approvers()`: Hạch toán bổ sung loại 7, KT kho của Yêu cầu nhập hàng, Điều chuyển kho, Điều chuyển hàng giữ (phòng người nhận), Kế hoạch NV, từ chối đơn nghỉ ở cấp NSHC (cần 2 mã), đặt phòng họp (mã HOẶC người phụ trách phòng), HĐ sửa chữa (`approver_id` loại trừ quyền), chuỗi tính giá (XNK tra động theo thương hiệu × hãng).
- Danh sách "chờ duyệt" hiện có ở nhiều màn lệch với người duyệt được (rộng hơn: borrow-sell-requests, Phiếu nhập kết quả, đăng ký khoá học, `/decision/waiting-approve`; hẹp hơn: Phiếu thu/chi, Thưởng năm, Kiểm kê vị trí; hoặc ẩn: người chỉ có quyền NSHC không thấy menu Đơn nghỉ). Registry lấy theo `can_approve` thật chứ không theo danh sách cũ.
- BE chưa chốt quyền (phải vá trước khi bật duyệt từ trung tâm / hàng loạt): Giao việc (update / approveResult / deny), Yêu cầu điều chỉnh giải pháp, Biên bản sự cố, Kế hoạch đào tạo, đăng ký khoá học, điểm danh, Bảo hiểm (duyệt), Phiếu giao việc / phiếu công tác / gia hạn kết thúc công tác, Biên bản bàn giao sơ bộ (ai cũng duyệt được); nhóm route job-assignment thiếu `auth:api` (`' middleware'` thừa dấu cách).
- `approvable = 0` thật sự: Đơn nghỉ quá ngày 05 tháng sau; phiếu Khoá học / Đề xuất mở khoá học quá `from_time` (422); phiếu thiếu mẫu in phụ lục HĐ. **Đi muộn về sớm KHÔNG còn hạn ngày** (đính chính `inventory-hrm.md`); Làm thêm: chưa tổng hợp lại, cần xem mục riêng ở `03-cham-cong-nhan-su.md`.
- Tài liệu cũ đã lỗi thời: Super Admin vượt quyền (không còn), khe `model_type` (không còn), quyền chỉ có guard web (đã chuyển mã). Các số dòng trong `inventory-hrm.md` đã lệch.

## 14. Cập nhật REALTIME, không phải chạy lệnh (16/11/2026)
User chốt: "không muốn phải chạy command, muốn realtime". Cách làm trong `Modules/ApprovalCenter`:
- **Phiếu nguồn đổi** → trait `SyncsApprovalInbox` sync ngay sau commit (đã có).
- **Vai trò / quyền / quản lý phòng / hồ sơ nhân viên đổi** → `ApprovalInboxRefresher::listen()` nghe mọi câu SQL GHI của HRM (`DB::listen`), nhận ra bảng liên quan (`employee_has_roles`, `role_has_permissions`, `roles`, `permissions`, `employee_manage_departments`, `company_employees`, `employee_infos` — chỉ UPDATE đổi `department_id`/`company_id`/`status`, lấy được id nhân viên thì chỉ sync phiếu của người đó) và sync lại các phiếu đang chờ bị ảnh hưởng: ngay sau commit (request web: ngay sau khi trả response). Vì bắt ở tầng SQL nên không cần gắn sự kiện vào từng chỗ ghi (`EmployeeRoleService`, `RoleManagementService`, `Employee`, import…). Mỗi Definition khai `watchedTables()`.
- **Hạn duyệt** → cột `approvable_until`, lọc lúc ĐỌC (`NULL hoặc >= NOW()`): phiếu quá hạn biến khỏi "Chờ tôi duyệt" đúng giây, không job nào cần chạy.
- **Lần đầu triển khai / thêm loại phiếu / đổi logic Definition** → `ensureBootstrapped()` tự nạp: có phiếu chờ ở nguồn mà bảng gom chưa có dòng nào, hoặc còn dòng `def_version` thấp hơn `Definition::version()`. Chạy khi người dùng mở màn / gọi API và mỗi phút trong lịch Laravel (có khoá chống nạp trùng). Đổi logic Definition thì chỉ cần tăng `version()`.
- **Lưới an toàn** cho phần ngoài tầm HRM (ERP ghi thẳng DB): `approval-inbox:backfill` tự chạy trong lịch mỗi 15 phút — không phải ai gõ.
- **Trình duyệt** tự cập nhật không cần bấm Làm mới: nghe thông báo realtime sẵn có (`$root` `realtime-notification`), tải lại khi quay lại tab, và tải nền mỗi 15 giây khi tab đang hiện.
- Giới hạn còn lại: thay đổi do ERP ghi thẳng bảng phân quyền chỉ vào bảng gom ở lần quét 15 phút; thông báo realtime chỉ có ở loại phiếu vốn đã gửi thông báo.
