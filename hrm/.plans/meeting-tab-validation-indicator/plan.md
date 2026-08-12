# Plan — Đánh dấu tab chứa lỗi validate (màn Tạo/Sửa cuộc họp)

Phụ trách: @namdangit

## Mục tiêu
Khi Lưu cuộc họp mà thiếu field bắt buộc ở nhiều tab: tiêu đề tab chứa lỗi hiển thị đỏ + icon cảnh báo; tự nhảy tới tab lỗi đầu tiên và focus field lỗi; badge tự mất khi hết lỗi (sau khi sửa và Lưu lại).

## Phạm vi
CHỈ FE. 2 file:
- `hrm-client/components/V2BaseTabNavigation.vue` (dùng chung — sửa cộng thêm, opt-in)
- `hrm-client/pages/assign/meeting/components/MeetingForm.vue`
Không BE / migration / permission / git.

## Quyết định
- Kiểu hiển thị: chữ đỏ + icon cảnh báo (`ri-error-warning-fill`). Tab lỗi đang active: nền xanh + viền đỏ.
- Dò tab lỗi bằng DOM: quét mỗi panel có `.v2-error` (marker của V2BaseError) → tự khớp field lỗi thuộc tab nào, không cần map key thủ công.
- `formError` (Vuex `paymentProfile`) chỉ refresh khi Lưu → badge mất sau lần Lưu kế tiếp (nhất quán với lỗi inline hiện tại). Live-clear theo từng phím gõ = task riêng nếu cần.

## Task

### FE — V2BaseTabNavigation.vue
- [x] Thêm hỗ trợ `tab.hasError`: class `has-error` + icon cảnh báo, opt-in (màn khác không truyền → giữ nguyên)
- [x] CSS trạng thái lỗi: chữ đỏ khi không active, viền đỏ khi active

### FE — MeetingForm.vue
- [x] Thêm ref cho panel Điểm danh (`meetingAttendance`) + Biên bản (`meetingReport`)
- [x] Computed `formError` (map từ store), data `tabErrorFlags`
- [x] `tabs` computed gắn `hasError` từng tab
- [x] Methods: `getPanelEl`, `recomputeTabErrors` (quét `.v2-error`), `jumpToFirstError`, `focusFirstError`
- [x] Watch `formError` deep → recompute cờ + nhảy tab lỗi đầu + focus
- [ ] Verify E2E: submit thiếu field ở nhiều tab → tab đỏ + nhảy tab + focus; sửa xong Lưu lại → badge mất (cần dev server FE + tài khoản)

### Fix — 2026-07-24
- [x] Bug popup thêm nhanh KH: trường "Công ty mẹ" (V2BaseSelectRemote) không search được trong modal → set `dropdownParent` về `.modal-content` (xem plan meeting-quick-add-customer)

### Checkpoint — 2026-07-24
Vừa hoàn thành: Toàn bộ code 2 file (tab error indicator + auto-jump + focus).
Đang làm dở: chưa verify trên browser.
Bước tiếp theo: user bật FE dev server → verify luồng submit thiếu field nhiều tab.
Blocked: cần môi trường FE chạy để verify.

### Fix phản hồi Redmine #10874 — 2026-08-12
Hiện tượng: tab "Dự án tiền khả thi" thiếu field bắt buộc → bấm Lưu nháp / Lưu và lên lịch / Lưu và chốt lịch ở tab Thông tin, tab không đỏ.
Nguyên nhân: cờ lỗi chỉ dò bằng DOM (`.v2-error`), mà panel dự án chỉ render dự án con đang mở và key lỗi BE `projects.N.address` không khớp key UI `project_address` → không có marker nào trên DOM.
- [x] `MeetingForm.vue`: `recomputeTabErrors` suy tab từ chính key lỗi BE (`tabForErrorKey`) rồi mới hợp thêm kết quả quét DOM
- [x] `MeetingForm.vue`: `jumpToFirstError` gọi `focusFirstErrorProject()` để mở đúng dự án con đang lỗi
- [x] `MeetingForm.vue`: `pruneResolvedErrors` + `snapshotErrorValues` — user sửa field nào thì bỏ lỗi field đó, cờ đỏ tự tắt realtime (cờ `suppressJumpOnce` chặn nhảy tab khi đang gõ)
- [x] `MeetingProject.vue`: map lỗi BE `address` → `project_address` (lỗi "Địa điểm triển khai" trước đây không bao giờ hiện)
- [x] `MeetingProject.vue`: sub-tab "Dự án N" chứa lỗi hiển thị đỏ + icon, thêm `hasProjectError` / `focusFirstErrorProject`
- [ ] Verify E2E (cần dev server + tài khoản)

Ghi chú gửi lại tester/BA: một số field ProjectInfoSection gắn nhãn bắt buộc nhưng BE KHÔNG validate (`projects.*.name`, `application_id`, `implementation_type`) → bỏ trống vẫn lưu thành công, không phát sinh lỗi nên cũng không có tab đỏ. Cần chốt có thêm rule BE hay bỏ nhãn bắt buộc ở FE.

### Fix UI — 2026-08-12
- [x] Màn `/assign/meeting/{id}/show`: bỏ `min-vh-100` trên `b-container` gốc của `MeetingForm.vue` — khối form luôn cao tối thiểu 100vh nên block "Lịch sử" (`SystemInfoSection`) bị đẩy xuống rất xa khi tab đang mở ít nội dung (vd tab Điểm danh). V2Footer là `position: fixed` nên không bị ảnh hưởng.
- [x] Thu hẹp tiếp khoảng cách card ↔ "Lịch sử": `show.vue` override `.system-info-section.meeting-history` margin-top 16px → 4px (scoped `::v-deep`, không ảnh hưởng màn chi tiết khác), margin-bottom 64px chuyển từ inline style sang CSS

### BE — bổ sung rule thiếu cho dự án TKT trong meeting — 2026-08-12
Các field FE gắn dấu * nhưng BE để `nullable` → bỏ trống vẫn lưu, không có lỗi nên cũng không có tab đỏ.
- [x] `MeetingCreateApiRequest` + `MeetingUpdateApiRequest`: `projects.*.name` required|max:255, `projects.*.application_id` required
- [x] Loại hình / Lĩnh vực khách hàng theo điều kiện hiển thị: `customer_scope_group_id` + `customer_scope_id` dùng `required_unless:projects.*.is_intermediary_customer,1`; `customer_benefit_scope_group_id` + `customer_benefit_scope_id` dùng `required_if:...,1` (khối KH thụ hưởng cuối chỉ hiện khi bật "KH thương mại dịch vụ")
- [x] Message tiếng Việt cho từng rule (key wildcard `projects.*.<field>.<rule>`)
- [x] Verify bằng tinker: wildcard trong tham số `required_unless/required_if` được thay đúng index, message custom khớp

Còn tồn: `projects.*.address` chỉ required ở Create, Update không có → màn Sửa bỏ trống "Địa điểm triển khai" vẫn lưu được. Chờ chốt có đồng bộ không.
- [x] Fix màn Sửa meeting không fill lại "Ứng dụng": `MeetingService::getDataForShow` chỉ trả `app_id` / `customer_application_id`, thiếu `application_id` (key mà `ProjectInfoSection` bind) → select trống. Bổ sung `application_id` + `application_name` (định dạng "MÃ - Tên" khớp options FE). Verify tinker meeting 20 → 101 / "UD.0101 - Gara tổng hợp (trung tâm chăm sóc xe)"

### Test E2E toàn luồng meeting — 2026-08-12
Chạy Playwright trên FE :3000 / BE :8000, tài khoản DNS Admin.
- [x] Tạo mới, Lưu nháp khi trống → tab "Thông tin" đỏ, 4 lỗi inline
- [x] Gõ Tên meeting → lỗi `name` biến mất realtime, các lỗi khác giữ nguyên
- [x] KỊCH BẢN PHẢN HỒI #10874: dự án TKT trống, đứng ở tab Thông tin bấm Lưu nháp → auto nhảy sang tab "Dự án tiền khả thi" (đỏ + icon), sub-tab "Dự án 1" đỏ, đủ 7 lỗi BE
- [x] Điền đủ dự án → cả 7 lỗi + cờ đỏ tự tắt, KHÔNG cần lưu lại
- [x] Lưu nháp → meeting 21 status 0, prospective_project 104 ghi đúng
- [x] Sửa → Lưu và Lên lịch (status 1) → Lưu và Chốt lịch (status 2)
- [x] Hoàn thành khi thiếu biên bản → chặn, không gọi API, nhảy tab Biên bản
- [x] Thêm biên bản + điểm danh đủ → Hoàn thành (status 3), conclusion lưu đúng
- [x] Xoá meeting nháp (22) → xoá khỏi DB
- [x] Huỷ meeting đã lên lịch (23) → status 4 + cancel_reason
- [x] Màn chi tiết: gap card ↔ "Lịch sử" = 2px ở cả tab Thông tin (card cao 1376) lẫn Điểm danh (card cao 398)
- [x] Sửa meeting 20 + 21: select "Ứng dụng" fill đúng "UD.0101 - Gara tổng hợp (trung tâm chăm sóc xe)"
- [x] Console: không có TypeError / 500; chỉ còn Vue warn prop-type có sẵn từ trước

Fix phát sinh trong lúc test:
- [x] `focusFirstError` không focus được: chọn trúng input ẩn của select2/CspSingleSelect. Sửa: bỏ qua element ẩn, nhận diện thêm `.select2-selection` / `.csp-control`, loại element trong `<label>`, gán `tabIndex=-1` cho widget div để focus được bằng code

Ghi chú: log BE 10:48 hôm nay có `Integrity constraint violation: Column 'name' cannot be null` khi insert prospective_projects — đúng lỗi 500 mà rule `projects.*.name required` vừa thêm sẽ chặn từ tầng validate.
Dữ liệu test còn lại trong DB local: meeting 21 (Hoàn thành) + 23 (Huỷ).
