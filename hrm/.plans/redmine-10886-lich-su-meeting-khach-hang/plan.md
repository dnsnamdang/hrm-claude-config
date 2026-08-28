# Redmine #10886 — Nút + popup "Lịch sử meeting với khách hàng"

Nhánh: `tpe-develop-assign_fix` (cả API và Client)
Màn: Meetings → Lịch meeting → Tạo mới / Cập nhật / Xem chi tiết
Khuôn popup: `pages/assign/prospective-projects/components/SolutionListModal.vue` ("Xem danh sách giải pháp")

## Đã rà
- Cờ "Có khách hàng" của loại meeting = `meeting_types.has_customer` (ảnh trong task). FE đã có computed `hasCustomer` ở `MeetingForm.vue` + `GeneralInfo.vue`.
- Người tham gia = `meeting_employees` với `type = 1` (quan hệ `company_members`).
- Dự án TKT gắn meeting qua bảng `prospective_project_meetings`.
- Trạng thái meeting: 0 Đang tạo · 1 Lên lịch · 2 Chốt lịch · 3 Hoàn thành · 4 Hủy. Task liệt kê 4 trạng thái sau → **loại bản nháp (0)**.

## Phase 1 — BE
- [ ] Endpoint `GET assign/meeting/customer-history`: lọc theo `customer_id`, chỉ meeting QUÁ KHỨ (`start_date < now()`), trạng thái 1–4, và **người tạo phải nằm trong danh sách tham gia**; sắp xếp `start_date` giảm dần
- [ ] Bộ lọc: keyword (mã/tên), trạng thái, ngày họp từ/đến, hình thức (`mode_id`), loại meeting, dự án TKT
- [ ] Trả cột: thời gian, mã–tên, loại meeting, dự án, có biên bản / lý do hủy, trạng thái

## Phase 2 — FE
- [ ] `components/assign/meeting/CustomerMeetingHistoryModal.vue` bám khuôn `SolutionListModal`
- [ ] Nút "Lịch sử meeting" ngang hàng ô Khách hàng trong `GeneralInfo.vue`, chỉ hiện khi loại meeting có khách hàng VÀ đã chọn khách hàng (cả 3 màn tạo/sửa/chi tiết)
- [ ] Click tên meeting → mở tab mới `/assign/meeting/{id}/show`

## Kết quả

### BE (`hrm-api`)
- [x] `GET assign/meeting/customer-history` (`MeetingController::customerMeetingHistory`) — đặt TRƯỚC route wildcard `/{id}`
  - Điều kiện cố định: đúng khách hàng · `start_date < now()` · bỏ trạng thái Đang tạo · `whereExists` người tạo nằm trong `meeting_employees type = 1` của chính cuộc họp
  - Sắp xếp `start_date` giảm dần, rồi `id` giảm dần
  - Bộ lọc: keyword (mã/tên), `status`, `mode_id`, `meeting_type_id`, `from_date`, `to_date`, `prospective_project_id`
  - Tên dự án join `prospective_projects` (bảng nối chỉ lưu tên MEETING, không phải tên dự án)
  - Nạp dự án + số biên bản theo lô (`whereIn` + `groupBy`), không N+1 trong `map()`

### FE (`hrm-client`)
- [x] `components/assign/meeting/CustomerMeetingHistoryModal.vue` — bám khuôn `SolutionListModal` (V2BaseFilterPanel + V2BaseDataTable), 7 cột theo task, badge trạng thái dùng 9 mã màu chuẩn
- [x] Nút **"Lịch sử meeting"** (`V2BaseButton secondary` + `ri-history-line`) ngang hàng nhãn Khách hàng trong `GeneralInfo.vue`; điều kiện `hasCustomer && form.customer_id` nên tự đúng ở cả 3 màn tạo/sửa/chi tiết
- [x] Cột "Biên bản / Lý do hủy": trạng thái Hủy hiện lý do, còn lại là link `Biên bản` mở tab mới; chưa có biên bản thì ghi rõ

### Kiểm thử — 46 case, 0 FAIL
- [x] BE 18 case: điều kiện cố định (loại nháp, loại meeting tương lai, sắp xếp giảm dần, lấy cả trạng thái Hủy kèm lý do) · 5 bộ lọc · nghịch (thiếu `customer_id` → 422, chưa đăng nhập bị chặn, khách hàng không có meeting → rỗng)
- [x] UI 28 case: AC1 loại meeting nội bộ → nút ẩn · AC2 bỏ trống khách hàng → nút ẩn · AC3 nút hiện · AC4 popup đủ 7 cột + 6 bộ lọc, đúng thứ tự thời gian, không lẫn nháp · AC5 link `target="_blank"` mở đúng tab mới · màn Xem chi tiết cũng có nút · không lỗi JS

### Ghi chú
- Test AC1 lần đầu FAIL do tôi chọn nhầm dữ liệu: meeting id 17 tên là "Test phân loại họp nội bộ" nhưng loại meeting của nó lại là "Meeting với khách hàng" (`has_customer = 1`). Đổi sang meeting id 26 (loại "Meeting nội bộ về kỷ luật nhân sự") thì đúng.
## Hồi quy các luồng liên quan (2026-08-27) — 88 case, 0 FAIL

Chạy sau khi hoàn thành #10898 + #10886, phủ cả #11044 và #11209.

**BE 36 case**
- Tính lại cấp duyệt của **toàn bộ 64 báo giá** bằng logic cũ (`max L1,L2`) và mới (`max L1,L2,L3`): 61 giữ nguyên · 3 tăng cấp · **0 giảm cấp** · báo giá KHÔNG có hàng tạm giữ nguyên 100%
- `calculateTotals` còn đủ 12 key cũ; `calculateLevel` không rò key nội bộ `_profit_margin_raw` / `_temp_product_margin_raw`
- `DetailQuotationResource` còn đủ key cũ (cả cấp header lẫn từng dòng hàng) + 2 key mới
- User CÓ quyền giá vốn không bị siết nhầm: `can_view_cost_price = true`, vẫn xem được giá nhập hàng ERP
- 16 query cho 1 lần dựng Resource (Resource chỉ dùng cho 1 bản ghi ở show/store/update, không dùng cho danh sách → không N+1)

**API smoke 35 case** — meeting (danh sách, chi tiết, lịch, chọn nhân sự + lọc Chức vụ + `get_all`, chọn KH, `customer-history`, khảo sát), báo giá (danh sách, chi tiết, `calculate-level` POST, `preview-submit`), cấu hình duyệt giá + lịch sử, dự án TKT + giải pháp. Kiểm route `/assign/meeting/{id}` **không bị `/customer-history` nuốt**.

**UI smoke 38 case** — 14 màn của cả 4 task đều render, có nội dung mong đợi, **không lỗi JS**.

**Hồi quy thao tác GHI 15 case** — nút "Thêm nhanh khách hàng" và ô chọn khách hàng vẫn mở popup sau khi sửa template; 2 nút căn giữa cùng hàng (tâm dọc trùng nhau); **lưu meeting HTTP 200**, giữ nguyên khách hàng / trạng thái / số dòng biên bản; lưu cả khối cấu hình cũ lẫn khối mới đều 200.

### Phát hiện đáng lưu ý (không phải lỗi)
1. **3 báo giá sẽ đổi cấp duyệt từ Cấp 1 → Cấp 3** khi gửi duyệt lại: `BG-2026-00002`, `BG-2026-00003`, `BG-2026-00144` — do có dòng hàng tạm **chưa nhập giá vốn** nên tỷ suất tính là 0%, đúng theo quyết định đã chốt. Không báo giá nào bị hạ cấp.
2. Meeting dùng loại meeting **đã khoá** (`meeting_types` id 1, `status = 2`) bị BE chặn `423` khi lưu — chốt chặn nghiệp vụ có sẵn, không liên quan thay đổi của 2 task này.
