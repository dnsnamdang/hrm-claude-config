# Phiếu đề nghị thu tiền (ERP → HRM) — design tóm tắt

> Phụ trách: @khoipv · Bắt đầu: 2026-08-13 · Nhánh: `gop_db` (cả 2 repo)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-13-finance-bill-income-request-design.md`

## Mục tiêu

Port màn ERP **"Phiếu đề nghị thu tiền"** (`admin/income-expenditure/bill_income_requests`,
mã `{cty}.DNTT{mmyy}.{5 số}`, 6 trạng thái) sang HRM **phân hệ Tài chính**.
Chứng từ do kinh doanh lập để đề nghị kế toán thu tiền theo một hợp đồng; kế toán duyệt rồi lập Phiếu thu.

## Quyết định đã chốt (user 2026-08-13)

1. **Dùng chung bảng ERP** `bill_income_requests` + `bill_income_request_details` — 2 cổng song song,
   không đổi schema, không tạo bảng `hrm_*`.
2. **Giữ nguyên logic ERP 1:1**, chỉ đổi nguồn hợp đồng: `firm_contracts` → **`hrm_contracts`**.
3. "Số tiền còn nợ" **vẫn đọc sổ cái** `account_details` TK 1311/3311. Hợp đồng HRM chưa có bút toán
   nên hiển thị 0 cho tới khi có luồng hạch toán — user chấp nhận.
4. Phạm vi: **đầy đủ trừ phiếu thu** — 1 màn danh sách gộp + màn chờ duyệt + tạo/sửa/xóa nháp +
   gửi duyệt + chi tiết + Không duyệt + In. **Màn Phiếu thu sẽ port sang HRM ở feature sau**,
   nên đợt này không có nút "Tạo phiếu thu".
5. **Giữ cả 2 loại thu**: Thu bán hàng (`hrm_contracts` + HĐ đầu kỳ + HĐ bảo dưỡng) và
   Thu nhà cung cấp (giữ nguyên 5 nguồn hợp đồng mua của ERP).
6. **Bỏ hẳn** nhánh HĐ nguyên tắc: checkbox "Thu dư nợ đầu kỳ" + bảng phân bổ theo phiếu YCXH
   (bên ERP nhánh này đang không kích hoạt được, DB xác nhận 0 dòng dùng tới).
7. **Quyền mới trong `PermissionsTableSeeder` HRM**, tên giữ y hệt ERP (5 quyền, id 1148–1152, guard `api`).
8. **Không đụng repo ERP** — rủi ro đã biết, xem mục dưới.

## Điểm kỹ thuật chính

- BE `Modules/Finance`, routes `/v1/finance/bill-income-requests`. Không `mysql2`.
- Phải khai **9 entity hợp đồng** trong morphMap (8 read-only của ERP — gồm `FirmContract` chỉ để đọc
  6.877 dòng phiếu cũ — + `Assign\Contract`), nếu không HRM không hiển thị nổi 2.411 phiếu ERP có sẵn.
- FE bám base UI màn khách hàng `pages/assign/customers/index.vue`
  (`V2BaseFilterPanel` + `V2BaseDataTable`); skill bắt buộc: `button-convention`, `modal-popup`,
  `form-validate`, `unsaved-changes`, `list-page`, `print-page`.
- Cờ quyền FE fail-closed, khởi tạo `false`, chỉ lấy từ `$store.state.permissions`.
- Menu Tài chính: slot xám `finance.js:46` + `:82` → danh sách; `:403` → màn chờ duyệt.
- 5 lỗi của ERP mà HRM chủ động sửa: `delete()` không kiểm tra quyền/trạng thái · sinh mã không khóa ·
  hook `created` lưu 2 lần · `update()` dùng nhầm StoreRequest · catch `Exception` nuốt lỗi validate.

## ⚠️ Rủi ro đã chấp nhận

`objectable_type` lưu **tên class PHP**; repo ERP không có class nào trỏ `hrm_contracts` và không đăng ký
`morphMap` → phiếu do HRM tạo vẫn hiện trong danh sách ERP nhưng **mở chi tiết / in bên ERP sẽ lỗi
`Class not found`**. User chốt không sửa ERP; dặn kế toán xử lý phiếu đề nghị thu trên HRM.
Rủi ro tự hết khi feature Phiếu thu HRM hoàn tất. (Nếu đổi ý: chỉ cần thêm 1 model shim
`App\Model\Sale\HrmContract` + morphMap bên ERP, không phải sửa logic.)

## Điểm đã chốt lúc review spec (không còn để mở)

1. Popup hợp đồng HRM chỉ lấy `status ∈ {6, 8, 9, 10, 11, 12}` (Có hiệu lực trở lên) — đã cài + verify.
2. Màn chờ duyệt đợt này chỉ có nút **Không duyệt** (bước Duyệt nằm ở màn Phiếu thu, port sau).

---

## Tình trạng — XONG 7/7 PHASE (2026-08-14)

**Backend** (`hrm-api`, 20 file mới + 5 file sửa): 9 entity hợp đồng read-only + `Supplier` +
`AccountDetail` · `BillIncomeRequest` + `BillIncomeRequestDetail` · trait `ChecksEmployeePermission` ·
`BillIncomeDebtService` + `BillIncomeRequestService` · 2 Resource · 3 FormRequest · Controller ·
morphMap trong `FinanceServiceProvider` · 8 route · 5 quyền id 1148-1152 · seeder dữ liệu test.

**Frontend** (`hrm-client`, 9 file mới + 1 file sửa): danh sách (dùng chung cho màn chờ duyệt qua prop
`pendingMode`) · thêm/sửa · chi tiết + modal Không duyệt · in · 3 popup chọn dữ liệu · menu Tài chính.

**5 chỗ spec/plan ghi sai đã sửa khi làm:** bảng `Supplier` (là `customers` + `is_supplier=1`, không phải
`suppliers`) · model khách hàng (`App\Models\TpCustomer`) · không dùng middleware `checkPermission` cho
nhánh kế toán (spatie bỏ sót role gán từ ERP) · filter `customer_name` của ERP là code chết ·
`wr_service_contracts` CÓ cột tiền `total_after_vat`.

**2 lỗi tự phát hiện & sửa:** `canView()` fail-open khi chưa đăng nhập · Super admin bị FE đá về 404 ở
màn chờ duyệt do thiếu 5 quyền mới trong role 18.

**Còn nợ (cần user hỗ trợ):** đối chiếu trực tiếp trên giao diện ERP · test đủ 4 tài khoản 4 cấp quyền ·
quyết định gộp trait quyền dùng chung với `ProductTransferRequest`.

---

## Cập nhật sau nghiệm thu — 2026-08-18 (Phase 8 — user test xong, đã commit `bb4863e0e` / `dde97025c`)

1. **Bộ lọc lặp nhãn "Nhà cung cấp"** — slot `#field-supplier_id` tự render `<V2BaseLabel>` trong khi
   `V2BaseSmartFilterPanel` đã render nhãn từ schema. Quy tắc: slot chỉ tự đặt nhãn khi field khai
   `hideLabel: true` (thường đi kèm `wrapperClass: 'd-contents'` cho slot nhiều cột).
2. **Popup "Cấu hình cột hiển thị"** — gắn `columnCustomizationMixin`, khoá `finance_bill_income_requests`
   (màn chờ duyệt dùng chung khoá vì cùng bộ cột). Lưu qua `human/column-customizations` → **không migration**.
   `locked: true` chỉ cho STT / Mã phiếu / Hành động. Bộ cột mặc định **giữ nguyên bản nghiệm thu** —
   user chốt không ẩn bớt cột nào.
3. **2 cột mới Người / Ngày cập nhật** — BE thêm quan hệ `employee_update()`, eager load `employee_update.info`,
   resource trả `updated_by_name` + `updated_at`. Cột **có sắp xếp** (thêm `updatedAt`/`updated_at` vào
   whitelist `applySort`). DB: 2.473 phiếu, 0 phiếu NULL `updated_by` nên cột không rỗng.
4. **Định dạng ngày** — `created_at` của danh sách đổi `d/m/Y` → `d/m/Y H:i` cho khớp Ngày cập nhật
   (resource chi tiết vốn đã có giờ). Cột nới 110px → 140px.
5. **Nới cột chữ dài** — `reason` 280px, `departmentName` 200px, kèm `objectName` 240px: khai thiếu 1 cột
   thì auto-layout lấy chỗ đúng từ cột đó.
