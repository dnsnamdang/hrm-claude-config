# Plan — Nhập tay Lương thâm niên (accept-personnel) khi không dùng định biên

> Phụ trách: @khoipv · FE thuần · Design: `./design.md`

## Phase 1 — FE: cho nhập tay Số tháng & Số tiền lương thâm niên

### FE — `hrm-client/pages/decision/accept-personnel`

- [x] **T1.** `components/FormComponent.vue` — bảng Lương thâm niên (dòng ~138-167):
  - [x] Ô **Số tháng**: `v-if="isUsingManpower"` → `<span>{{ formSubmit.seniority_review_period_month }}</span>`;
        `v-else` → `base-input-field` (type number) `name="seniority_review_period_month"`
        `v-model="formSubmit.seniority_review_period_month"` `v-validate="'required'"` + `base-helper-error`.
  - [x] Ô **Số tiền**: `v-if="isUsingManpower"` → text `.toLocaleString('en')`;
        `v-else` → `base-currency-input` unit `(Đ)` size `small` `name="seniority_pay"`
        `v-model="formSubmit.seniority_pay"` `v-validate="'required'"` + `base-helper-error`.
  - [x] Giữ nguyên 2 checkbox "Tham gia bảo hiểm" / "Thuế TNCN" của dòng.
- [x] **T2.** `add.vue` — thêm `seniority_review_period_month: 0`, `seniority_pay: 0`
        vào `formSubmit` mặc định (cạnh `p1/p2/p3_salary: 0`).

### Kiểm thử thủ công

- [x] **T3.** `human/settings` chọn **"Không dùng định biên"** → vào `accept-personnel/add`:
  - [x] 2 ô Số tháng / Số tiền lương thâm niên hiện input, nhập tay được.
  - [x] Bỏ trống → submit → hiện lỗi inline (viền đỏ + invalid-feedback) ở đúng ô.
  - [x] Nhập giá trị → lưu thành công, mở lại edit thấy đúng giá trị đã nhập.
  - [x] Tick "Tham gia bảo hiểm" dòng thâm niên → Tổng lương BHXH cộng đúng số nhập tay.
- [x] **T4.** `human/settings` chọn **"Dùng định biên"** → vào add/edit:
  - [x] 2 ô hiển thị readonly (text), auto-fill từ nhân viên như cũ, không bắt required.
- [x] **T5.** Màn `show` + `approve`: 2 ô vẫn readonly (disabled), không lỗi.

## Phase 2 — Áp dụng tương tự cho `decision/salary-change`

### FE — `hrm-client/pages/decision/salary-change`

- [x] **T6.** `components/CurrentIncomeComponent.vue` — khối "new" Lương thâm niên (dòng ~420-455):
  - [x] Ô **Số tháng**: `v-if="isUsingManpower"` → text; `v-else` → `base-input-field` number
        name `new.seniority_review_period_month` + `v-validate="'required'"` + helper-error.
  - [x] Ô **Số tiền**: `v-if="isUsingManpower"` → giữ auto-tính `newSeniorityPay` (readonly);
        `v-else` → `base-currency-input` name `new.seniority_pay` + `v-validate="'required'"` + helper-error.
        (Khi v-else không tham chiếu `newSeniorityPay` → side-effect không ghi đè giá trị nhập tay.)
- [x] **T7.** `add.vue` — thêm `seniority_review_period_month: 0`, `seniority_pay: 0` vào `formSubmit.new`.

### Kiểm thử thủ công (salary-change)

- [x] **T8.** Không định biên → `salary-change/add`: 2 ô (new) nhập tay được, bỏ trống → lỗi inline, lưu + mở edit đúng giá trị.
- [x] **T9.** Dùng định biên → Số tháng readonly, Số tiền auto-tính `p1 × tang_tham_nien × floor(tháng/12)` như cũ.
- [x] **T10.** Show/approve: 2 ô readonly (disabled), không lỗi.

## Phase 3 — Áp dụng tương tự cho `decision/transfer-personnel`

> Giống hệt accept-personnel (Số tháng + Số tiền "new" là text tĩnh, KHÔNG có auto-tính như salary-change).

### FE — `hrm-client/pages/decision/transfer-personnel`

- [x] **T11.** `components/CurrentIncomeComponent.vue` — khối "new" Lương thâm niên (dòng ~414-421):
  - [x] Ô **Số tháng**: `v-if="isUsingManpower"` → text; `v-else` → `base-input-field` number
        name `new.seniority_review_period_month` + `v-validate="'required'"` + helper-error.
  - [x] Ô **Số tiền**: `v-if="isUsingManpower"` → text; `v-else` → `base-currency-input`
        name `new.seniority_pay` + `v-validate="'required'"` + helper-error.
- [x] **T12.** `add.vue` — thêm `seniority_review_period_month: 0`, `seniority_pay: 0` vào `formSubmit.new`.

### Kiểm thử thủ công (transfer-personnel)

- [x] **T13.** Không định biên → `transfer-personnel/add`: 2 ô (new) nhập tay được, bỏ trống → lỗi inline, lưu + mở edit đúng.
- [x] **T14.** Dùng định biên → 2 ô readonly (text), auto-fill từ nhân viên như cũ.
- [x] **T15.** Show/approve: 2 ô readonly (disabled), không lỗi.

## Ghi chú

- BE: **không sửa** cả 3 màn (accept-personnel: rule đã `required`; salary-change + transfer-personnel: lưu thẳng, không recompute, không rule seniority).
- accept-personnel + transfer-personnel: nhập độc lập cả 2 ô (số tiền là text tĩnh).
- salary-change: dùng định biên giữ auto-tính số tiền; không định biên nhập tay độc lập.

---

### Checkpoint — 2026-06-06
Vừa hoàn thành: VERIFIED DONE — cả 3 phase code + user verify browser PASS (accept-personnel T1-T5, salary-change T6-T10, transfer-personnel T11-T15).
Đang làm dở: Không.
Bước tiếp theo: Chờ merge (cả API và Client — thực tế chỉ FE hrm-client).
Blocked:
