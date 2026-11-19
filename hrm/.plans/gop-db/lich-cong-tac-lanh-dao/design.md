# Lịch công tác lãnh đạo (mở rộng Nhắc việc cá nhân — Mytodo)

> Brainstorm 05/11/2026 với user. Nhánh `gop_db` (hrm-api, hrm-client) · TPE_APP nhánh `develop` (hỏi lại nhánh trước khi sửa).
> Mockup app (Pencil): `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen` — **Nhóm ⑮ Lịch công tác lãnh đạo** — từ 07/11/2026 nằm trong khu **VIỆC CỦA TÔI (APP)** (x 22000, y 4050; 11 màn LCT-00…LCT-10; trước đó ở x 15600 y 21946 khu Công việc). Khu "Bản cũ" đã dời xuống +1850. Backup trước khi sửa: `meeting-mobile.backup-20261105-truoc-lich-cong-tac.pen`.
> Mockup so 3 phương án (HTML): `HRM/.plans/mytodo-lich-cong-tac-lanh-dao/.superpowers/brainstorm/44933-1793875696/content/man-lich-lanh-dao.html`
> **User DUYỆT 05/11/2026** (9 màn LCT-00…08 + 10 điểm mục 3.6 + câu đổi/huỷ đề xuất ở LCT-08).
> Chưa có lệnh code — mọi bước code / migration / quyền phải xin phép riêng (CLAUDE.md gốc).

## 1. Vì sao làm

Nhân viên cần biết **người ký hồ sơ của mình có ở công ty vào ngày định trình ký không**. Hiện phải gọi hỏi
phòng hành chính — bất tiện. Ban lãnh đạo ~8 người, là người ký hồ sơ giấy tờ quan trọng. Nhân viên thường đã
biết rõ sếp nào ký cho mình → cần dò đúng hàng của sếp đó trong tuần.

Bản chất: **lịch VẮNG MẶT của người ký**. Lãnh đạo chỉ báo khi phải đi khỏi công ty, không ghi mọi lịch làm việc.

## 2. Mục tiêu / Không làm / Thất bại nếu

- **Mục tiêu**: lãnh đạo tự báo lịch vắng bằng chính nhắc việc cá nhân của mình (web + app); cả công ty nhận
  thông báo; mọi nhân viên xem được bảng vắng mặt của ban lãnh đạo trên app.
- **Không làm**: màn xem lịch trên **web** (user: "web không cần làm"); duyệt lịch; lịch làm việc chi tiết trong
  ngày; thông báo sang công ty khác.
- **Thất bại nếu**: nhân viên thường cũng bắn được thông báo toàn công ty; lộ mô tả / các bước riêng của nhắc việc
  lãnh đạo; bảng hiện sai ngày (lịch đã huỷ / đã về sớm vẫn còn).

## 3. Quyết định đã chốt (user)

### 3.1 Quyền
- **Q1 — "Báo lịch công tác lãnh đạo"**: gán cho các lãnh đạo. Chỉ người có quyền này (tại công ty đang chọn)
  mới **thấy** ô tuỳ chọn trên form nhắc việc. Không có quyền → ẩn hẳn (không disable). BE kiểm lại khi lưu.
- **Q2 — "Cấu hình lịch công tác lãnh đạo"**: người có quyền sắp thứ tự lãnh đạo (màn web, mục 3.5).
  *(Claude chốt — user trả lời "ok" với đề xuất; ai được gán do quản trị quyết.)*
- Cả 2 quyền khai trong **danh mục mã** `app/Support/Permissions/Catalog/assign.php` (gop_db đã bỏ seeder tên cũ —
  kiểm 05/11): Q1 `assign.lich_cong_tac_lanh_dao.announce`, Q2 `assign.lich_cong_tac_lanh_dao.configure`. Xem `plan.md`.

### 3.2 Form nhắc việc cá nhân (web `TodoFormModal.vue` + app `personal_todo_form_page.dart`)
- Thêm ô tick **"Báo lịch công tác lãnh đạo"** (chỉ hiện khi có Q1). Có cả ở form Tạo và Sửa, cả web lẫn app.
- Tick → hiện thêm **Ngày bắt đầu** + **Giờ bắt đầu**. Khi đó **bắt buộc Ngày bắt đầu và Ngày hạn**; Giờ bắt đầu
  / Giờ hạn không bắt buộc. Không tick → form như hiện tại.
- **Lưu** (tạo hoặc sửa có tick) → confirm: *"Nhắc việc này sẽ được thông báo cho toàn Công ty, bạn chắc chắn lưu?"*
  (web dùng `base-confirm-modal` / `this.$confirm`).
- Người tạo lịch = chính lãnh đạo (tạo cho mình). Chức danh lấy trong hồ sơ của người tạo.

### 3.3 Thông báo
- Người nhận: **mọi nhân viên của công ty mà lãnh đạo đang làm** (công ty của nhắc việc — `personal_todos.company_id`),
  không gửi sang công ty khác.
- **Câu chữ GIỮ NGUYÊN theo user** (user chọn lệch chuẩn `notification-convention`, chấp nhận bị cắt trên màn khoá):
  - Tiêu đề: `Ông/bà: {Họ tên} - {Chức danh} có lịch công tác từ {ngày bắt đầu} đến {ngày hạn}`
  - Nội dung: `{Tiêu đề nhắc việc}` + `Đề nghị các phòng ban, bộ phận sắp xếp công việc phù hợp với lịch làm việc của lãnh đạo!`
  - Gợi ý kỹ thuật: `EmployeeInfoService::sendNotification` đã nhận `push_title` / `push_body` riêng — khớp đúng
    cấu trúc tiêu đề / nội dung trên.
- **Đổi ngày giờ hoặc huỷ → báo lại toàn công ty** (user chốt). Huỷ gồm: xoá nhắc việc, bỏ tick ô "Báo lịch công tác".
- **Tick Hoàn thành trước Ngày hạn → cắt ngắn lịch đến ngày tick** (theo thực tế), coi như đổi lịch → báo lại.
- Bấm thông báo (app) → mở màn Lịch công tác lãnh đạo ở đúng tuần của lịch.

### 3.4 Màn app "Lịch công tác lãnh đạo"
- Vị trí: **Phân hệ Công việc** trên app → thêm mục menu "Lịch công tác lãnh đạo" (thanh dưới đã đủ 5 ô → đặt trong
  drawer, cạnh "Vấn đề" — Claude đoán).
- **3 chế độ xem, mặc định A** (user chốt), chuyển bằng nút gạt trên đầu màn:
  - **A. Bảng tuần**: hàng = lãnh đạo, cột = 7 ngày (T2–CN), ô cam = ngày vắng, ô sọc = vắng một phần ngày (có giờ);
    ‹ › / vuốt đổi tuần; chạm ô → hiện tên, chức danh, khoảng ngày giờ, tiêu đề nhắc việc.
  - **B. Theo ngày**: dải 7 ngày, chọn ngày → "N vắng · M có mặt"; người vắng lên đầu kèm lý do + "Vắng đến …";
    người có mặt thu gọn, ghi "sắp vắng dd/mm" nếu có.
  - **C. Dòng thời gian**: nhóm Đang vắng → Sắp tới → Đã qua.
- **Hàng trong bảng**: mọi người đang có Q1 tại công ty, **kể cả tuần đó không đi đâu** (hàng trống = có mặt).
  Bị gỡ quyền → tự biến khỏi bảng.
- Ai xem: mọi nhân viên của công ty (không cần quyền riêng — Claude đoán, user chưa phản đối).
- Nhân viên chỉ thấy: họ tên, chức danh, khoảng ngày giờ, tiêu đề. **Không** thấy mô tả, các bước, danh sách của
  nhắc việc (Claude đoán, user xác nhận "đúng rồi" ở bản tóm tắt).
- Không có màn này trên web.

### 3.5 Màn web "Cấu hình lịch công tác lãnh đạo"
- Nằm trong **Phân hệ Công việc trên web**, gate Q2.
- Liệt kê người đang có Q1 theo **từng công ty**; kéo thả sắp thứ tự (chức danh hiện chưa có cấp nên không suy ra được).
- Người mới được cấp Q1 → tự nằm cuối cho tới khi sắp lại.

## 3.6 Claude tự chốt sau builder check (user đã duyệt 05/11)
1. Bỏ tick Hoàn thành → trả lại Ngày hạn gốc + báo "thay đổi lịch" (cần lưu ngày hạn gốc).
2. Tick hết bước con (cha tự Hoàn thành) = tick Hoàn thành → cắt lịch.
3. Tick Hoàn thành trước Ngày bắt đầu → coi là huỷ.
4. Tick đúng / sau Ngày hạn → không báo.
5. "Mọi nhân viên của công ty" = NV đang làm việc thuộc công ty đó (kể cả kiêm nhiệm), bỏ nghỉ việc / tài khoản khoá. Người tạo không nhận thông báo của chính mình.
6. Lãnh đạo bị gỡ Q1 → hàng biến khỏi bảng; sửa nhắc việc cũ thì giữ nguyên lịch, không huỷ ngầm, không bắn thông báo.
7. Công ty của lịch cố định = công ty lúc tạo (`personal_todos.company_id`).
8. Người có Q2 chỉ sắp thứ tự cho công ty mình có Q2.
9. Chức danh theo hồ sơ ở công ty của lịch; màn app hiện chức danh hiện tại, thông báo giữ chức danh lúc gửi.
10. Màn app thêm (mockup): khối "Hôm nay vắng" dưới bảng tuần; chế độ C có ô tìm theo tên + nhóm Đã qua 30 ngày; sheet chi tiết có "Lịch sắp tới" của người đó (30 ngày); form có khối xem trước câu thông báo.

## 3.7 Câu đổi / huỷ (user duyệt cùng mockup 05/11) + việc còn hỏi
- **Câu thông báo khi đổi lịch / huỷ lịch** (đã vẽ ở LCT-08):
  - Đổi: `Ông/bà: {Họ tên} - {Chức danh} thay đổi lịch công tác: từ ngày … đến ngày …` + nội dung như lần đầu.
  - Huỷ: `Ông/bà: {Họ tên} - {Chức danh} huỷ lịch công tác từ ngày … đến ngày …` + tiêu đề nhắc việc.
- Nhánh hrm-api cho API app (`develop` hay `gop_db`) — hỏi khi xin phép code.

## 4. Để lại cho người làm (builder)
- Lược đồ lưu (cột mới trên `personal_todos` hay bảng riêng), cách lưu thứ tự, cách tìm người có Q1 theo công ty
  (`employeeIdsHoldingPermission`), deep-link app.
- Gửi thông báo cho cả công ty: `sendToAllNotification` hiện lặp đồng bộ từng người → nên đẩy queue job.
- Lịch qua nửa đêm / nhiều tuần hiển thị trên bảng A; múi giờ theo server.

## 5. Liên quan
- [[mytodo-mobile-design]] · `.plans/gop-db/phan-he-cong-viec/` (thiết kế app Công việc, `meeting-mobile.pen`)
- Form web: `hrm-client/pages/assign/my-todo/components/TodoFormModal.vue` · API `Modules/Assign/Routes/api.php:1531`
  (`/assign/my-todo/todos`) · model `Modules/Assign/Entities/MyTodo/PersonalTodo.php`
- Form app: `TPE_APP/app/lib/ui/my_todo/personal_todo_form_page.dart`

## 6. Bổ sung sau khi code (user chốt 05/11/2026)
- **Xác nhận chỉ hỏi 1 lần, lúc BẬT lịch** ("Đã chọn khi tạo rồi thì ko cần hỏi lại ở các bước sau"): tạo có tick / tick lên
  nhắc việc chưa là lịch. Lịch có sẵn: đổi ngày giờ, bỏ tick (huỷ), tick bước / Hoàn thành → không hỏi, hệ thống tự báo.
  Nút hộp xác nhận app: [Đồng ý] · [Huỷ] một hàng.
- **Tuỳ chọn "Gửi kèm tiêu đề nhắc việc"** (hiện khi bật Báo lịch, mặc định CHỌN; cột `personal_todos.leader_show_title`):
  bỏ chọn → thông báo không có tiêu đề nhắc việc (mới/đổi: chỉ câu "Đề nghị…"; huỷ: không nội dung) và màn Lịch công tác chỉ
  hiện thời gian vắng (ẩn dòng nội dung ở mọi chế độ xem). Đổi riêng ô này trên lịch có sẵn: không gửi thông báo.
- Mockup: LCT-05 (sửa), LCT-07 (sửa), LCT-08 (sửa), LCT-09 + LCT-10 (mới) trong `meeting-mobile.pen` nhóm ⑮.

## 7. Sửa 07/11/2026 (user)
- **Đổi tên tính năng → "Lịch làm việc lãnh đạo"** (màn app, mục menu, ô tick "Báo lịch làm việc lãnh đạo", tên quyền hiển thị). Mockup Nhóm ⑮ đã đổi hết (28 chữ + 5 tên node). **Câu thông báo ĐỔI** (user chốt 07/11): tiêu đề `Ông/bà: {Họ tên} - {Chức danh} vắng mặt tại công ty từ ngày {d/m/Y} đến ngày {d/m/Y}`; đổi lịch `… thay đổi lịch vắng mặt tại công ty: từ ngày … đến ngày …`; huỷ `… huỷ lịch vắng mặt tại công ty từ ngày … đến ngày …`. Nội dung (tiêu đề nhắc việc + câu "Đề nghị…") giữ như §3.3. Thay cho câu ở §3.3/§3.7.
- **LCT-01 Bảng tuần vẽ lại**: mỗi ngày 1 ô chia 2 buổi (trái sáng, phải chiều). XANH = buổi có ca, có mặt tại công ty · VÀNG = vắng mặt trong buổi có ca · XÁM = ngoài ca. **Ngày/buổi làm việc** (user chốt 07/11): T2–T6 + CN và giờ ca lấy theo BẢNG PHÂN CA của chính lãnh đạo (`shift_detail_employee_dates` + `working_shifts.start_at/end_at`; ca kết thúc ≤ 12:00 → chỉ buổi sáng; bắt đầu ≥ 13:00 → chỉ chiều). **Thứ 7: mọi lãnh đạo luôn làm CẢ NGÀY**, không xét T7 chẵn/lẻ của bảng phân ca. Lãnh đạo KHÔNG có bảng phân ca → dùng **Ca mặc định** (cấu hình MỚI, xem dưới). Lịch phủ ngày nghỉ thì ngày nghỉ vẫn xám. **Vắng một phần ngày làm tròn theo buổi** (chạm buổi sáng trước 12:00 → vắng cả sáng; chạm từ 13:00 → vắng cả chiều) — bỏ ô sọc. **Dưới dải luôn ghi tên lịch** (tiêu đề nhắc việc) từ buổi vắng đầu tiên, cắt "…"; lịch bỏ "Gửi kèm tiêu đề" ghi "Vắng mặt". Khối "Hôm nay vắng", LCT-03, LCT-04 ghi "Vắng sáng / Vắng chiều" thay giờ lẻ. Áp cho cả nền LCT-02, LCT-10.
- **Ô "Danh sách" của form nhắc việc đổi tên "Loại nhắc việc"** (2 loại mặc định Việc cá nhân / Việc công ty, chọn sẵn cá nhân) — độc lập công tắc Báo lịch; xem `my-todo/design.md`.
- **Ảnh hưởng code (CHƯA làm — cần xin phép riêng):** app đã có tên cũ ở 10 file TPE_APP (`leader_schedule/*`, `module_menus.dart`, `personal_todo_form_page.dart`, `leader_schedule_section.dart`, `notification_router.dart`, `my_todo_api_service.dart`, `work_item.dart`, `notification.dart`) + tên quyền ở catalog `assign.php` (hrm-api) + web form. Logic ô: `leader_schedule_controller.cellState()` đang trả `none|full|partial` → đổi thành 2 buổi `am/pm` theo luật làm tròn; tuần view thêm dải xanh + nhãn tên lịch.
- **Cấu hình mới — "Ca mặc định cho lịch làm việc lãnh đạo"** (user chốt 07/11): đặt NGAY TRONG màn web xếp thứ tự lãnh đạo "Cấu hình lịch làm việc lãnh đạo" (§3.5, quyền Q2 — user chốt 07/11), 1 ô chọn bảng phân ca có sẵn; **mỗi công ty 1 giá trị riêng** (theo công ty đang chọn, giống thứ tự lãnh đạo). Dùng cho lãnh đạo không có bảng phân ca. Chưa cấu hình → **T2–T7 08:30–12:00 / 13:00–17:30** (user chốt 07/11). Đổi tên chỉ chữ hiển thị, giữ mã quyền/route/tên code (user chốt 07/11). Plan: `plan-sua-0711.md`. Hệ thống hiện KHÔNG có khái niệm "ca mặc định công ty" (đã kiểm hrm-api + hrm-client 07/11) ⇒ cần 1 cột/bảng cấu hình mới — migration, xin phép riêng khi code.

## 8. Sửa 09/11/2026 (user) — xem lịch theo công ty trong HỒ SƠ
- **API xem lịch `GET v1/assign/leader-schedules` lấy lãnh đạo theo công ty trong hồ sơ NV** (`employee_infos.company_id`), KHÔNG theo công ty đang chọn (`company_role`). Áp cho cả `leaders`, `schedules`, `days`. Hồ sơ thiếu công ty → lùi về công ty đang chọn.
- **`meta` (quyền báo lịch, chức danh của tôi) và `orders` (màn cấu hình thứ tự + ca mặc định) GIỮ theo công ty đang chọn** (user chốt 09/11).
- Lý do: app KHÔNG có chỗ đổi công ty, nhưng `company_role` lưu ở DB — NV nhiều công ty đổi công ty trên web là app cũng đổi theo, thấy lãnh đạo công ty khác.
- Hệ quả: lãnh đạo hồ sơ ở A mà đang chọn B thì xem lịch thấy lãnh đạo A (kể cả khi vừa tạo lịch ở B). DB local: 44 NV đang làm nhiều công ty, 2 người đang chọn khác công ty hồ sơ.
