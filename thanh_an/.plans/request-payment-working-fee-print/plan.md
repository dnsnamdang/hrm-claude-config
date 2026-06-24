# Plan — In phiếu đề nghị thanh toán công tác phí

- **Người phụ trách:** @khoipv
- **Spec:** `docs/superpowers/specs/2026-06-18-request-payment-working-fee-print-design.md`
- **Design tóm tắt:** `.plans/request-payment-working-fee-print/design.md`

**Goal:** Trang in "GIẤY ĐỀ NGHỊ THANH TOÁN" liệt kê từng phiếu công tác (bảng đủ cột đề xuất + duyệt + số hóa đơn) + bảng tổng hợp; nút In ở danh sách.

**Global constraints:** font Times New Roman; `@media print { .no-print { display:none } }`; dùng `window.print()`; cột duyệt luôn in; `Province` = `App\Models\Province`; người đề nghị/công ty theo `created_by`.

---

## Phase 1 — Backend (`hrm-thanhan-api`)

- [x] **T1. Block `requester` trong `DetailRequestPaymentWorkingFeeResource`**
  - File: `Modules/Timesheet/Transformers/RequestPaymentWorkingFeeResource/DetailRequestPaymentWorkingFeeResource.php`
  - Thêm `'requester' => $this->buildRequester(),` vào mảng trả về của `toArray`.
  - Thêm 2 private method `buildRequester()` và `cleanProvinceName($name)` đúng như code trong spec mục 4.1.
    - `buildRequester`: `Employee::with(['info.department','info.workPosition'])->find($this->created_by)`; lấy `info.fullname`, `optional($info->workPosition)->name`, `optional($info->department)->name`; company = `$employee->companies()->first()` (fallback `Company::find($info->company_id)`); province = `App\Models\Province::where('id',$company->province_id)` → `cleanProvinceName`.
    - Trả về key: `full_name, position, department, company_name, company_province`.
    - Trường hợp không tìm thấy employee → trả 5 key rỗng `''`.
  - Import/dùng FQCN: `\Modules\Human\Entities\Employee`, `\Modules\Human\Entities\Company`, `\App\Models\Province`.

---

## Phase 2 — Frontend: nút In (`hrm-thanhan-client`)

- [x] **T2. Dropdown-item "In" ở danh sách**
  - File: `pages/timesheet/request-payment-working-fee/index.vue`
  - Trong `<b-dropdown>` hành động, sau mục "Lịch sử duyệt", thêm:
    ```html
    <b-dropdown-item :to="`/timesheet/request-payment-working-fee/${data.id}/print`">
        <i class="fa fa-angle-right"></i> In
    </b-dropdown-item>
    ```

---

## Phase 3 — Frontend: trang in (`hrm-thanhan-client`)

File mới: `pages/timesheet/request-payment-working-fee/_id/print.vue` (tham khảo `business_trip_assigns/_id/print.vue`)

- [x] **T3. Khung trang + load dữ liệu**
  - Template: header thao tác `.no-print` (nút Quay lại `backToList()` + nút In `onclick="window.print()"`) + khối `.print-data` nền trắng chữ đen.
  - `data() { return { data: {} } }`.
  - `mounted()`: `this.$store.dispatch('apiGet','timesheet/request-payment-working-fee/'+this.$route.params.id).then(r => { if(r.data) this.data = r.data.data })`.
  - Computed: `requester` (=`data.requester||{}`), `companyName` (=`requester.company_name||'………………………………'`), `companyProvince` (=`requester.company_province||'……'`), `trips` (=`data.list_business_trip_assigns||[]`).
  - Method `backToList()` → push `/timesheet/request-payment-working-fee`.
  - CSS: copy `@media print`, `.qd-header/.qd-footer` (flex space-between), `table td,th{border:1px solid #000}`, font Times New Roman từ print.vue phiếu công tác.

- [x] **T4. Header + tiêu đề + người đề nghị**
  - Header 2 cột (`qd-header`): trái `{{companyName}}` + `=====o0o=====`; phải Quốc hiệu/Tiêu ngữ + `{{companyProvince}}, ngày…. tháng…. năm 202…`.
  - Tiêu đề giữa: `GIẤY ĐỀ NGHỊ THANH TOÁN`.
  - `Kính gửi: Giám đốc Công ty {{ companyName }}`.
  - `Người đề nghị: {{ requester.full_name }}` / `Chức vụ: {{ requester.position }}` / `Đang làm việc tại: {{ requester.department }}` (trống → `……`).

- [x] **T5. Lặp từng phiếu công tác + bảng chi tiết đủ cột**
  - `v-for="(trip,ti) in trips"`:
    - `Phiếu công tác: {{ trip.code }}` (đậm) / `Nội dung công việc: {{ trip.description }}` / `Thời gian: từ {{ trip.from_time }} đến {{ trip.to_time }}`.
    - `<table>` border, cột: TT | Nội dung | Số hóa đơn | ĐVT | Đơn giá đề xuất | Số tiền đề xuất | ĐVD | Đơn giá duyệt | Số tiền duyệt | Ghi chú.
    - Body `v-for="(d,i) in trip.dataTableSubmit"`: TT=`i+1`, `d.content`, `d.invoice_number`, `d.unit`, `formatNumber(d.payment_unit_price)`, `formatNumber(d.total_payment_unit_price)`, `d.unit_approve`, `formatNumber(d.payment_unit_price_approve)`, `formatNumber(d.total_payment_unit_price_approve)`, `d.note`.
    - Dòng tổng phiếu: ô "Tổng hợp" `colspan="5"` → ô tổng đề xuất `formatNumber(sumProposed(trip))`, 2 ô (ĐVD, Đơn giá duyệt) trống, ô tổng duyệt `formatNumber(sumApprove(trip))`, ô Ghi chú trống.
  - Methods: `formatNumber(v)`, `sumProposed(trip)`, `sumApprove(trip)` đúng spec mục 5.2.

- [x] **T6. Bảng tổng hợp + lý do + khối ký**
  - Bảng tổng hợp: cột STT | Mã phiếu | Số tiền đề xuất | Số tiền duyệt; body lặp `trips` (`sumProposed`/`sumApprove`); dòng cuối "Tổng hợp" + `totalProposed` + `totalApprove` (computed cộng toàn bộ).
  - `Lý do thanh toán trễ hạn quá 10 ngày (không tính thứ Bảy, Chủ nhật và các ngày lễ) sau thời gian công tác trở về (nếu có): ……` (chấm chấm).
  - Dòng ngày (text-right, nghiêng): `{{ companyProvince }}, ngày…. tháng…. năm 202…`.
  - Khối ký 3 cột (flex space-between, text-center): Giám đốc | Duyệt thanh toán | Người đề nghị.

---

## Phase 4 — Verify thủ công

- [ ] **T7. Verify**
  - Phiếu có 2+ phiếu công tác: in đủ từng phiếu (nội dung, thời gian, bảng riêng) + bảng tổng hợp đúng tổng.
  - Số tiền đề xuất/duyệt + số hóa đơn hiển thị đúng; chưa duyệt → cột duyệt 0/trống.
  - Công ty/tỉnh/chức vụ/đơn vị đúng theo người tạo phiếu.
  - `window.print()` ẩn đúng phần `.no-print`, bố cục A4 gọn.

---

## Checkpoint

### Checkpoint — 2026-06-18 (khởi tạo)
Vừa hoàn thành: brainstorming + spec + plan
Đang làm dở: chưa code
Bước tiếp theo: T1 — block requester ở BE
Blocked:

### Checkpoint — 2026-06-18 (code xong T1-T6)
Vừa hoàn thành: T1-T6. BE: block `requester` trong DetailRequestPaymentWorkingFeeResource (đã fix null province bằng optional()). FE: nút In ở index.vue + trang _id/print.vue đầy đủ (header, người đề nghị, lặp phiếu + bảng 10 cột, bảng tổng hợp, lý do, ký). BE & FE đã review subagent (Approved). Đã trace end-to-end: route GET {id} → show → DetailResource có requester; FE apiGet render đúng.
Đang làm dở: không
Bước tiếp theo: T7 — user verify UI (in thử phiếu nhiều công tác)
Blocked: chờ user verify UI

### Checkpoint — 2026-06-18 (đổi sang modal popup)
Theo yêu cầu user "làm popup giống phiếu công tác": chuyển từ trang route `_id/print.vue` sang **modal** `components/modal/RequestPaymentWorkingFeePrintModal.vue` (pattern BusinessTripDecisionPrintModal). Dropdown danh sách đổi sang `@click="$refs.printModal.open(data.id)"` + đăng ký component. Đã XÓA `_id/print.vue`. Nút In trong footer modal dùng window.open + getPrintStyles (CSS inline gồm border bảng, Times New Roman) + print(). Đã review subagent: Approved (3 Minor không block, ĐVD = Đơn vị duyệt đúng chủ đích). BE giữ nguyên (requester).
Bước tiếp theo: T7 — user verify UI bằng modal
Blocked: chờ user verify UI

### Checkpoint — 2026-06-22 (fix header/footer khi in)
- [x] **T8. Bỏ header/footer trình duyệt khi in (ngày giờ, tiêu đề, about:blank)**
  - File: `components/modal/RequestPaymentWorkingFeePrintModal.vue` > `getPrintStyles()`
  - Nguyên nhân: in bằng `window.open('', ...)` → trình duyệt chèn ngày giờ + title + URL (about:blank) vào vùng lề trang in.
  - Fix: thêm `@page { size: A4; margin: 0; }` vào CSS in → không còn vùng lề để vẽ header/footer; nội dung giữ lề nhờ padding body/.print-data.
Bước tiếp theo: user in thử lại xác nhận đã hết header/footer
Blocked: chờ user verify

### Checkpoint — 2026-06-23 (fix bảng dính mép + cắt đôi hàng khi in)
- [x] **T9. Sửa lỗi bảng dính mép trang & hàng bị cắt đôi khi tách trang**
  - File: `components/modal/RequestPaymentWorkingFeePrintModal.vue` > `getPrintStyles()`
  - Nguyên nhân: `@page { margin: 0 }` (T8) bỏ lề mọi trang → trang 2,3 dính sát mép trên; + thiếu quy tắc page-break → 1 hàng bị cắt làm đôi tại mép trang.
  - Fix (thuần CSS in, theo xác nhận user — cho tách + lặp tiêu đề, thêm lề trên-dưới mọi trang):
    - `@page { size: A4; margin: 15mm 0 }` — lề trên-dưới lặp ở MỌI trang (padding body chỉ tạo lề trang đầu nên không đủ). Trái-phải 0, lề ngang dùng `body { padding: 0 50px }`.
    - Header/footer trình duyệt (ngày giờ, title, about:blank): KHÔNG tắt được bằng CSS khi @page margin>0 → hướng dẫn user bỏ chọn "Đầu trang và chân trang" trong hộp thoại in.
    - `.ctp-table { page-break-inside: auto }`, `.ctp-table tr { page-break-inside: avoid }`, `.ctp-table thead { display: table-header-group }`.
Bước tiếp theo: user in thử lại xác nhận hết dính mép + không cắt đôi hàng
Blocked: chờ user verify
