# Cột "Số hóa đơn" — Nội dung công tác phí (tóm tắt)

- **Người phụ trách:** @khoipv
- **Ngày:** 2026-06-18
- **Spec chi tiết:** `docs/superpowers/specs/2026-06-18-working-fee-invoice-number-column-design.md`

## Mục tiêu
Thêm cột nhập **"Số hóa đơn"** (text, không bắt buộc) vào bảng "Nội dung công tác phí" trên màn `timesheet/request-payment-working-fee`, ngay sau cột "Nội dung". Cả người tạo & người duyệt đều sửa được.

## Quyết định lớn
- Tên field: `invoice_number` (string, nullable).
- BE: migration thêm cột + bổ sung field vào 3 chỗ `RequestPaymentWorkingFeeDetail::create` trong service + trả về ở `RequestPaymentWorkingFeeDetailResource`.
- FE: thêm cột vào `RequestPaymentWorkingFeeForm.vue` (header + ô input pattern "Ghi chú" + default trong `addDataTableSubmit` + sửa `colspan` dòng Tổng hợp).
- Không lọc/tìm kiếm, không Excel, không validate.

## Scope ngoài
Báo cáo `ReportService` (chỉ cộng tiền), FormRequest — giữ nguyên.
