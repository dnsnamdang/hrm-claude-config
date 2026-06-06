# Design — Nhập tay Lương thâm niên (accept-personnel) khi không dùng định biên

> Phụ trách: @khoipv · Loại: Feature nhỏ (1 phase, FE thuần) · Ngày: 2026-06-06

## Mục tiêu

Trong bảng **"Lương thâm niên"** ở màn `decision/accept-personnel` (add + edit), khi cấu hình
**"Không dùng định biên"** (`human/settings` → `using_manpower = false`), cho phép **nhập tay**
2 ô **Số tháng** (`seniority_review_period_month`) và **Số tiền** (`seniority_pay`).
Khi **"Dùng định biên"** → giữ hiển thị readonly như hiện tại.

## Hiện trạng

- `human/settings/index.vue`: radio "Dùng định biên nhân sự" (`using_manpower`: `false`/`true`),
  lưu vào `general-regulations`.
- `accept-personnel/components/FormComponent.vue` đã có computed `isUsingManpower`
  (getter `decision/getIsUsingManpower`, fetch qua `decision/fetchIsUsingManpower`).
- Pattern **P1/P2/P3** (dòng 185-199, 252-267, 337-352): khi `isUsingManpower=true` → text readonly,
  `v-else` → `base-currency-input` + `v-validate="'required'"`. **Đây là pattern sẽ copy.**
- Riêng bảng Lương thâm niên (dòng 138-167): **Số tháng** và **Số tiền** hiện **chỉ hiển thị text**,
  chưa cho nhập tay → đây là phần cần sửa.

## Phạm vi

- **CHỈ FE.** Sửa `FormComponent.vue` (dùng chung add/edit/show/approve) + bổ sung default trong `add.vue`.
- Màn `show` (`_id/index.vue`) và `approve` (`_id/approve.vue`) truyền `isShow=true` → input tự disable
  qua `addDisabledToElement()` → **không bị ảnh hưởng** (vẫn readonly). Đúng phạm vi add + edit.
- **BE không đổi**: Service `store`/`update` đã lấy thẳng 2 field từ request
  (`AcceptPersonnelService.php` dòng 202-203, 268-269), không tự tính đè; `AcceptPersonnelRequest`
  đã để **`required`** cả 2 (dòng 24-25).

## Quyết định chốt với user

| Vấn đề | Quyết định |
| --- | --- |
| Phạm vi màn | Cả **add và edit** (show/approve readonly sẵn) |
| Quan hệ 2 ô | **Nhập độc lập**, không tự tính liên động |
| Validate | **required** cả 2 (khớp pattern P1/P2/P3 và rule BE) |

## Thay đổi cụ thể

### 1. `components/FormComponent.vue` — bảng Lương thâm niên

- **Số tháng** (`seniority_review_period_month`):
  - `isUsingManpower=true` → `<span>{{ formSubmit.seniority_review_period_month }}</span>`
  - `v-else` → `base-input-field` (number) + `v-validate="'required'"` + `base-helper-error`
- **Số tiền** (`seniority_pay`):
  - `isUsingManpower=true` → text format `.toLocaleString('en')`
  - `v-else` → `base-currency-input` (unit `(Đ)`, size `small`) + `v-validate="'required'"` + `base-helper-error`

### 2. `add.vue` — default `formSubmit`

Thêm `seniority_review_period_month: 0` và `seniority_pay: 0` (cạnh `p1/p2/p3_salary: 0`)
để input không lỗi khi chưa chọn nhân viên. Khi chọn nhân viên, `Object.assign(formSubmit, employeeInfo)`
vẫn ghi đè như cũ. (Màn edit nạp từ BE đã có sẵn 2 field nên không cần sửa.)

## Edge case & lưu ý

- `v-if/v-else`: khi **dùng định biên**, input không render → veeValidate **không** bắt `required`
  (đúng mong muốn); giá trị vẫn auto-fill từ employee.
- 2 ô nhập **độc lập**, không tự tính liên động.
- Giá trị nhập tay tự chảy vào computed `totalSocialInsuranceSalary` (khi tick "Tham gia bảo hiểm")
  như giá trị cũ — không cần sửa computed.
- Không đụng 2 checkbox "Tham gia bảo hiểm" / "Thuế TNCN" của dòng thâm niên.

## Phase 2 — Áp dụng tương tự cho `decision/salary-change`

> Cùng yêu cầu: không dùng định biên → cho nhập tay Số tháng + Số tiền lương thâm niên.

**File:** `pages/decision/salary-change/components/CurrentIncomeComponent.vue` (khối "new" — Thu nhập mới) + default `salary-change/add.vue`.

**Khác biệt với accept-personnel:**

- **Số tháng** (`new.seniority_review_period_month`) trước đây **luôn là input** (chỉ disable khi `isShow`).
- **Số tiền** (`new.seniority_pay`) trước đây **tự tính** qua computed `newSeniorityPay = p1_salary × tang_tham_nien × floor(tháng/12)` (readonly), computed có *side-effect* ghi `formSubmit.new.seniority_pay`.
- Cả 2 field được auto-fill từ dữ liệu nhân viên khi chọn (`getDetailEmployee` gán `formSubmit.new = newData`).

**Thay đổi (mirror đúng pattern P1/P2/P3 "new" trong cùng file):**

| Ô | Dùng định biên (`isUsingManpower=true`) | Không định biên (`v-else`) |
| --- | --- | --- |
| Số tháng | readonly text | `base-input-field` number + `required` + helper-error, name `new.seniority_review_period_month` |
| Số tiền | giữ auto-tính `newSeniorityPay` (readonly) | `base-currency-input` nhập tay + `required` + helper-error, name `new.seniority_pay` |

**Điểm kỹ thuật quan trọng:** Khi không định biên, ô Số tiền chỉ render input (`v-else`) → **không** tham chiếu computed `newSeniorityPay` → side-effect không chạy → giá trị nhập tay không bị tính đè. Khi dùng định biên giữ nguyên auto-tính.

**BE:** Không đổi. `SalaryChangeService` lưu thẳng `new_seniority_pay` / `new_seniority_review_period_month` (không recompute), `SalaryChangeRequest` không có rule seniority.

**Show/approve:** `addDisabledToElement()` (mounted khi `isShow`) tự disable input → readonly tự nhiên, không cần xử lý thêm.

## Không làm

- Không sửa BE (đã sẵn sàng cả 2 màn).
- Không tự tính số tiền từ số tháng ở chế độ không định biên (nhập độc lập); giữ auto-tính ở chế độ dùng định biên (salary-change).
- Không ràng buộc `> 0` (chỉ `required`, trừ khi user yêu cầu thêm sau).
