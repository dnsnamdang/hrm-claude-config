# Plan — Cột "Số hóa đơn" Nội dung công tác phí

- **Người phụ trách:** @khoipv
- **Spec:** `docs/superpowers/specs/2026-06-18-working-fee-invoice-number-column-design.md`
- **Design tóm tắt:** `.plans/working-fee-invoice-number-column/design.md`

**Goal:** Thêm cột text "Số hóa đơn" (không bắt buộc) vào bảng Nội dung công tác phí, sau cột "Nội dung", cả người tạo & người duyệt sửa được.

**Field:** `invoice_number` (string, nullable)

---

## Phase 1 — Backend (`hrm-thanhan-api`)

- [x] **T1. Migration thêm cột**
  - Tạo `database/migrations/2026_06_18_xxxxxx_add_invoice_number_to_request_payment_working_fee_details_table.php`
  - `up()`: `$table->string('invoice_number')->nullable()->comment('số hóa đơn')->after('content');`
  - `down()`: `$table->dropColumn('invoice_number');`
  - Chạy `php artisan migrate` → kiểm tra cột xuất hiện trong DB.

- [x] **T2. Service — lưu field (3 chỗ)**
  - File: `Modules/Timesheet/Services/RequestPaymentWorkingFreeService.php`
  - Thêm `'invoice_number' => $detail['invoice_number'] ?? null,` vào **cả 3** `RequestPaymentWorkingFeeDetail::create([...])` (dòng ~63, ~108, ~268).

- [x] **T3. Resource — trả field**
  - File: `Modules/Timesheet/Transformers/RequestPaymentWorkingFeeResource/RequestPaymentWorkingFeeDetailResource.php`
  - Thêm `'invoice_number' => $this->invoice_number,` vào `toArray`.

---

## Phase 2 — Frontend (`hrm-thanhan-client`)

File: `pages/timesheet/request-payment-working-fee/components/RequestPaymentWorkingFeeForm.vue`

- [x] **T4. Header bảng**
  - Thêm `<b-th>Số hóa đơn</b-th>` ngay sau `<b-th>Nội dung ...</b-th>`, trước `<b-th>ĐVT</b-th>`.

- [x] **T5. Ô input trong thân bảng**
  - Thêm `<b-td>` ngay sau ô chứa `base-select2` (cột Nội dung), pattern giống cột "Ghi chú":
    ```html
    <b-td class="align-middle">
        <input
            class="form-control non-disabled"
            v-model="data.invoice_number"
            autocomplete="off"
            :disabled="isShow && !dataSubmit.canApprove"
        />
    </b-td>
    ```

- [x] **T6. Default dòng mới**
  - Trong `addDataTableSubmit()`, thêm `invoice_number: undefined,` vào object push.

- [x] **T7. Sửa colspan dòng Tổng hợp**
  - Trong `<b-tbody>` nền xám, đổi `<b-td colspan="4" ...>Tổng hợp</b-td>` → `colspan="5"`.

---

## Phase 3 — Verify thủ công

- [ ] **T8. Verify luồng đầy đủ**
  - Add: nhập số hóa đơn vài dòng → Lưu → mở lại (show/edit) thấy đúng số hóa đơn.
  - Thêm dòng mới → ô số hóa đơn trống, nhập được.
  - Bảng không lệch cột (dòng Tổng hợp thẳng hàng).
  - Màn duyệt: người duyệt sửa được số hóa đơn, lưu giữ đúng.
  - Phiếu cũ (trước migration): ô số hóa đơn trống, không lỗi.

---

## Checkpoint

### Checkpoint — 2026-06-18 (khởi tạo)
Vừa hoàn thành: brainstorming + spec + plan
Đang làm dở: chưa bắt đầu code
Bước tiếp theo: T1 — tạo migration
Blocked:

### Checkpoint — 2026-06-18 (code xong T1-T7)
Vừa hoàn thành: T1-T7 (BE migration + service 3 chỗ + resource; FE header/input/default/colspan). Cả BE & FE đã qua review subagent (Approved). Đã trace end-to-end: lưu (add/edit gửi nguyên dataTableSubmit) + load lại (BusinessTripAssignsResource/OvertimeAssignmentsResource → RequestPaymentWorkingFeeDetailResource có invoice_number). Field nhất quán BE↔FE.
Đang làm dở: không
Bước tiếp theo: T8 — user chạy `php artisan migrate` (trong hrm-thanhan-api) rồi verify UI: thêm → lưu → xem/sửa/duyệt giữ đúng số hóa đơn
Blocked: chờ user chạy migrate + verify UI
