# In phiếu đề nghị thanh toán công tác phí (tóm tắt)

- **Người phụ trách:** @khoipv
- **Ngày:** 2026-06-18
- **Spec chi tiết:** `docs/superpowers/specs/2026-06-18-request-payment-working-fee-print-design.md`

## Mục tiêu
Thêm chức năng in phiếu đề nghị thanh toán công tác phí theo mẫu "GIẤY ĐỀ NGHỊ THANH TOÁN". Liệt kê đầy đủ từng phiếu công tác (nội dung, thời gian, bảng nội dung công tác phí đủ cột — đề xuất + duyệt + số hóa đơn) rồi bảng tổng hợp cuối.

## Quyết định lớn
- Pattern theo màn in phiếu công tác `business_trip_assigns/_id/print.vue`.
- Điểm vào: dropdown-item "In" ở `index.vue` (`:to=".../{id}/print"`).
- Người đề nghị + công ty lấy theo **người tạo** (`created_by`).
- **Hướng A:** BE thêm block `requester { full_name, position, department, company_name, company_province }` vào `DetailRequestPaymentWorkingFeeResource` (resolve `created_by` → info→department/workPosition, companies→province). `Province` = `App\Models\Province`.
- **In bằng modal popup** (giống `BusinessTripDecisionPrintModal`): component `components/modal/RequestPaymentWorkingFeePrintModal.vue`, mở qua `$refs.printModal.open(id)` từ dropdown danh sách; nội dung: header 2 cột → người đề nghị → lặp từng phiếu (bảng đủ cột) → bảng tổng hợp → lý do trễ hạn → khối ký. Nút In trong footer modal dùng `window.open` + `getPrintStyles()` (CSS inline đầy đủ) rồi `print()`. (Không dùng trang route `_id/print.vue`.)
- Cột duyệt luôn in; chưa duyệt = 0/trống. Dùng `window.print()`.

## Scope ngoài
Không xuất PDF server-side; không sửa nghiệp vụ lưu/duyệt; không thêm route BE (dùng lại GET detail).
