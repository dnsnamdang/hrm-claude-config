# Design — Danh sách Nhu cầu khách hàng (Redmine #11386)

> Feature: `customer-demand-list` · Phụ trách: @junfoke · Nhánh `task_11386` (tách từ `tpe`, cả 2 repo)

## Mục tiêu

Thêm màn **Meetings → Nhu cầu khách hàng**: danh sách nhu cầu đầu tư thu thập từ biên bản meeting
(`meeting_investment_demands`), kèm phân quyền 5 cấp, hạn xử lý + cảnh báo, đóng nhu cầu thủ công
và bàn giao cho người khác.

## Hiện trạng (rà trên `tpe` ngày 12/09/2026 — SAU khi team đẩy code mới)

| Thứ | Trạng thái |
| --- | --- |
| Bảng `meeting_investment_demands` | ✅ có `status` / `prospective_project_id` / `closed_at`, 3 trạng thái + màu |
| Cron tự đóng nhu cầu | ✅ **ĐÃ CÓ, ĐANG CHẠY** — `assign:close-expired-customer-demands`, 01:20 hằng ngày |
| Quy tắc đóng hiện hành | Quá `expected_start_date` mà chưa gắn dự án -> "Không tiếp tục". `closed_at` = CHÍNH `expected_start_date` (không phải ngày chạy cron) |
| Cột "N ngày" trên Lĩnh vực Cty kinh doanh | ❌ chưa có — `internal_business_scopes` chỉ có `code` / `name` / `status` |
| Tham số cảnh báo chung | ⏳ chưa có, nhưng đã có chỗ chuẩn: `general_regulations` (đang chứa `task_due_days`, `issue_due_days`, `meeting_due_days`, `solution_due_days`) |
| Chủ sở hữu nhu cầu | ❌ không có cột — "Kinh doanh chủ trì" suy từ `meetings.host_employee_id` |
| Picker nhân sự cho Bàn giao | ✅ `PopupStaff` dùng chung (đúng thứ spec mô tả) |
| ID quyền mới | bắt đầu từ **1184** (max hiện tại 1183) |

## Quyết định (user chốt 14/09/2026)

1. **Mốc tính hạn: CHỜ KHÁCH.** Hệ thống đang đóng theo `expected_start_date` — luật đã chốt trước
   đây và Báo cáo CSKH tiềm năng đang đếm theo đó. Spec #11386 lại bắt tính theo
   *ngày hoàn thành meeting + N ngày cấu hình ở Lĩnh vực*. Đổi là mọi nhu cầu đang mở bị tính lại hạn
   và báo cáo đổi số. **Phần 2 dừng chờ khách trả lời**, các phần khác làm trước.

2. **Làm từng phần, commit dần** theo thứ tự: (1) Danh sách + phân quyền → (2) Hạn + cảnh báo (chờ
   khách) → (3) Đóng thủ công → (4) Bàn giao.

3. ~~Giữ nhãn trạng thái hiện tại~~ → **THAY BẰNG PHẢN HỒI CỦA KHÁCH (14/09/2026)**:
   trạng thái 3 đổi tên `Không tiếp tục` → **`Đóng`**, ý nghĩa MỞ RỘNG thành
   *"Đóng do hệ thống hoặc do user chủ động đóng"*. Trạng thái 1 và 2 giữ nguyên tên.
   Đã đổi đồng bộ cả Báo cáo CSKH tiềm năng (bảng, Excel, bản in, KPI) để không màn nào gọi khác.
   Hằng PHP `KHONG_TIEP_TUC` → `DA_DONG` (giá trị vẫn là 3, KHÔNG đụng dữ liệu đã lưu).
   Commit: `hrm-api` c99f75eb6, `hrm-client` 6315b9e5a.

4. **Được phép** chạy migration còn thiếu + `assign:seed-care-demo` trên DB local `hrm_prod_30_3_26`.

## Quyết định đã chốt — đối chiếu MÔ TẢ MỚI của #11386 (user chốt 15/09/2026)

Khách đã sửa lại mô tả task. Rà toàn bộ với code đã làm: **Phần 1, 2, 4 không phải sửa gì về
nghiệp vụ** (13 cột, công thức `T + N`, cảnh báo M ngày, 5 cấp phân quyền, bàn giao giữ nguyên mốc T
+ dịch data scope + lưu vết + push thông báo — đều khớp).

Ba điểm mô tả mới lệch với code/skill, user chốt:

| # | Mô tả mới ghi | Chọn | Lý do |
| --- | --- | --- | --- |
| 1 | Trạng thái `Đã đóng` | **Giữ `Đóng`** | Chữ khách duyệt riêng ngày 14/09 mới nhất, mô tả task viết trước đó |
| 2 | Trạng thái `Đã lập dự án` | **Giữ `Đã lập dự án TKT`** | Khớp tên cột "Dự án TKT" trên cùng bảng |
| 3 | Push: `Bạn vừa được bàn giao xử lý Nhu cầu [KH] từ [Người bàn giao]. Hạn xử lý còn lại: [X] ngày.` | **Theo skill `notification-convention`** | CLAUDE.md: skill thắng spec về hình thức. Ra `[NCKH] Cập nhật: {KH - Nhóm ngành}. Bàn giao từ X. Còn Y ngày xử lý.` — nghiệp vụ y hệt |

**Menu ngữ cảnh 3 chấm (⋮): HOÃN** (user chốt 15/09/2026). Mô tả yêu cầu gom hành động vào menu ⋮,
nhưng nhánh này chưa có `V2BaseRowActions` và mọi màn V2 khác đều xếp icon phẳng — dựng riêng cho
một màn là đẻ thêm kiểu thứ ba. Giữ icon phẳng (Xem meeting · Bàn giao · Đóng · Lịch sử), chấp nhận
4 icon/dòng vượt mức "tối đa 3" của skill `list-page`. Làm menu ⋮ khi có component dùng chung.

**Chốt được câu hỏi số 3 đang treo ở mục dưới**: mô tả mới ghi rõ popup đóng nhu cầu chỉ có
**Textarea "Ghi chú chi tiết" (bắt buộc nhập)** — KHÔNG chọn từ danh mục. Vậy Phần 3 nhập tay,
và việc dừng #11465 (danh mục Lý do thất bại) là đúng hướng.

Kèm theo, đã sửa 2 vi phạm quy tắc mới của CLAUDE.md trong code đã viết:
`pages/assign/customer-demands/index.vue` dùng `toLocaleString('en-US')`, và
`components/assign/CustomerDemandHandoverModal.vue` dựng nhãn nhân viên bằng `utils/employeeOptionText.js`.

## Lệch giữa spec và quy ước project — bám cái nào

| Điểm | Spec #11386 | Quy ước project (skill `list-page`) | Chọn |
| --- | --- | --- | --- |
| Vị trí cột Trạng thái | thứ 9/13, trước Dự án TKT | ngay trước cột Hành động | **Theo spec** — khách chỉ đích danh thứ tự 13 cột |
| Cột Người tạo / Ngày tạo | không nhắc | BẮT BUỘC có | **Khai đủ nhưng ẩn mặc định** — giữ được cả hai |
| Hành động "Lịch sử" | chỉ nhắc ở phần Bàn giao | BẮT BUỘC ở mọi màn danh sách | Làm ở **Phần 4** cùng lúc với lưu vết bàn giao |

## Việc cần hỏi khách (soạn sẵn, user gửi)

1. **Mốc tính hạn nhu cầu** — giữ `expected_start_date` hay đổi sang *meeting + N ngày*? Nếu đổi:
   nhu cầu đang mở có tính lại hạn theo công thức mới không, hay chỉ áp cho nhu cầu phát sinh từ nay?
2. **Màn chi tiết nhu cầu**: spec nhắc "tab Lịch sử cập nhật của Nhu cầu" nhưng không mô tả màn chi
   tiết. Lịch sử hiện ở popup ngay trên danh sách, hay cần dựng hẳn màn chi tiết?
3. **Danh mục "Lý do đóng nhu cầu"**: khách tự khai trong danh mục hay hệ thống chốt cứng 4 lựa chọn
   như ví dụ trong spec?

## Quyết định đã chốt — 2026-10-05

| Vấn đề | Chốt | Lý do |
| --- | --- | --- |
| Nhu cầu được ghi nhận khi nào | **Chỉ khi meeting nguồn Hoàn thành** — trước đó không hiện ở màn danh sách lẫn tab Công việc của tôi | Phản hồi QA 05/10 (meeting 1244). Spec #11386/#11390 không nói, code cũ ghi nhận ngay lúc lưu biên bản |
| Dòng lịch sử "Tạo mới" | Ghi **lúc Hoàn thành**; sửa biên bản trước đó không sinh lịch sử | User chốt 05/10 |
| Popup Lịch sử | Khuôn chung `entity-history`: `V2BaseModal` + `SystemInfoSection`, type `customer-demand` trong `SystemLogService` | Bảng 4 cột tự dựng lệch khuôn đã chốt; user đồng ý thêm type vào service dùng chung |

## Quyết định đã chốt — 2026-09-23

| Vấn đề | Chốt | Lý do |
| --- | --- | --- |
| Cột "Thời gian hết hạn nhu cầu" của nhu cầu đã Đóng / đã lập dự án | **Vẫn hiện ngày hạn**, chỉ bỏ ghi chú đếm ngược. "Không thời hạn" chỉ dành cho N = 0 (từ 05/10/2026 nhu cầu của cuộc họp chưa Hoàn thành không còn hiện trên danh sách) | Cron đóng nhu cầu ngay trong ngày hết hạn → dùng chung `dueDate()` thì cột về null, người xem không phân biệt được "hết hạn rồi" với "không có hạn" (phản hồi user #11386). Tách `deadlineDate()` (hiển thị) khỏi `dueDate()` (nghiệp vụ) |
| Tên khách hàng ở cột Khách hàng | **Là hyperlink sang `/assign/customers/{id}`**, kèm `?from=...&tab=...` để nút Quay lại về đúng màn đi vào | Yêu cầu user 2026-09-23; quy ước `url-back` động của project |
| Khách hàng NGOÀI phạm vi xem của user | **Ẩn link, để chữ thường** (cờ BE `can_view_customer`) | User chốt 2026-09-23. `CustomerController::show` trả 403 với KH ngoài phạm vi → nếu vẫn để link thì bấm vào bị đá ngược về danh sách KH, trông như lỗi. Hệ quả: tài khoản không có cấp xem KH nào sẽ không thấy link nào — đúng ý đồ, không phải bug |
