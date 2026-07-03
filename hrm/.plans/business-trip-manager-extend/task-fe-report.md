# Báo cáo Task FE — Manager gia hạn/kết thúc sớm phiếu công tác

**Ngày:** 2026-06-24
**Repo:** hrm-client
**STATUS:** DONE_WITH_CONCERNS

## File tạo/sửa

### 1. `store/actions.js` (sửa, +5 dòng)
Thêm action `managerFinishExtendTrip(context, payload)` ngay sau `finishExtendTrip`.
Map `type=='1'` → `manager/finish`, ngược lại → `manager/extend`. Dùng helper `apiPost` y như action self.

### 2. `components/modal/manager-finish-trip-modal.vue` (tạo mới, ~210 dòng)
Modal mới, KHÔNG đụng `finish-trip-modal.vue` self.
- Prop `id` (Number) = business_trip_assign_id.
- `@show` → `onModalShow()`: reset form + `dispatch('apiGet', 'timesheet/business_trip_assigns/' + id)` → đọc `response.data.data.business_trip_employees` → đổ vào `employee_options` (value = `item.id` = employee_info_id, text = `fullname (code)`).
- Field: **Nhân sự** (b-form-select, required), **Loại** (1=Kết thúc, 2=Gia hạn — khớp self), **Thời gian** (date-picker datetime, value-type `YYYY-MM-DD H:mm:ss`, required), **Ghi chú** (input text).
- Validate inline: `is-invalid` + `invalid-feedback` + flag `touched` (chỉ hiện sau submit đầu) cho Nhân sự + Thời gian. `submitSave` set `touched=true`, chặn nếu `!validate()`.
- Submit → `dispatch('managerFinishExtendTrip', {...data, id})`. Success → toast success + `$emit('event')` + hide modal. Lỗi → toast `message_mobile || message`.

### 3. `pages/timesheet/business_trip_assigns/index.vue` (sửa)
- Import + register `ManagerFinishTripModal` (tiện thể register luôn `AddResultModal` vốn được render nhưng chưa register — pre-existing thiếu sót).
- Thêm data `managerExtendId: null`.
- Cột Actions: thêm nút `<b-button class="fas fa-calendar-plus edit">` tooltip "Gia hạn/Kết thúc sớm", `v-if="canManagerExtend()"`, `@click="openManagerExtend(item)"` (bám đúng style các nút Actions hiện có trong file: b-button + class FontAwesome `edit`).
- Render `<manager-finish-trip-modal @event="getData" :id="managerExtendId">` (event success → `getData` reload DS).
- Method `canManagerExtend()`: duyệt `this.permissions` tìm name `'Gia hạn, kết thúc sớm phiếu công tác'` (mirror `isBusinessTripManager`).
- Method `openManagerExtend(item)`: set `managerExtendId = item.id` rồi `$nextTick` → `$bvModal.show('manager-finish-trip-modal')`.

## Kết quả lint
KHÔNG có ESLint trong dự án (không có file `.eslintrc*`, không có script `lint`, không có `node_modules/.bin/eslint`). Đã rà cú pháp thủ công bằng `node --check` trên từng script block:
- Modal mới: PARSE OK sạch.
- index.vue / actions.js: chỉ báo lỗi ở các dòng **pre-existing** dùng `??` / `?.` (Node cục bộ cũ không hiểu, Nuxt build qua Babel vẫn OK); code mới thêm vào đều parse sạch.

## Điểm nghi ngờ / quyết định

1. **Path response show:** Xác minh qua `add/_id.vue` (dòng 638) → đúng là `response.data.data.business_trip_employees`. Mỗi item dùng `id/fullname/code/department/telephone/image` (dòng 327-336). Khớp contract (`id` = employee_info_id).

2. **V2Base vs b-form (QUYẾT ĐỊNH):** modal-popup SKILL yêu cầu V2Base + `b-modal hide-footer` + button-convention. NHƯNG module business_trip_assigns hiện tại (cả `finish-trip-modal.vue` self lẫn các nút Actions trong index.vue) KHÔNG dùng V2Base — dùng `b-form-select`/`date-picker`/`b-button`+FontAwesome. Theo CLAUDE.md "Tuân thủ style list của module đang triển khai" + ưu tiên đồng nhất trong module, tôi bám style self modal (b-form + date-picker, footer ok/cancel mặc định của b-modal) thay vì V2Base, để đồng nhất. Vẫn thêm validate inline `is-invalid`/`invalid-feedback`/`touched` theo nguyên tắc bắt buộc của dự án.
   → Nếu chủ ý là phải tuân thủ tuyệt đối modal-popup SKILL (V2Base + custom footer), cần refactor cả self modal cho đồng bộ — ngoài phạm vi task (cấm sửa self modal). Cần xác nhận hướng nào.

3. **Nút Actions:** button-convention khuyến nghị `V2BaseIconButton` (icon `ri-*`) cho table action. Nhưng toàn bộ Actions trong index.vue đang là `b-button` + `fas fa-*`. Đã bám theo style hiện có của file để nhất quán (giống concern #2).

4. **Validate date-picker:** đã truyền `:input-class` để gắn `is-invalid` vào input bên trong vue2-datepicker; cộng thêm `invalid-feedback d-block` hiển thị tách biệt để chắc chắn lỗi luôn hiện (vì datepicker bọc input, `is-invalid` sibling-selector của Bootstrap có thể không kích hoạt).
