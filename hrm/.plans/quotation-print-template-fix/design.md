# quotation-print-template-fix — Tóm tắt

**Màn hình:** Quản lý dự án TKT → Quản lý báo giá → In báo giá / Xuất PDF (modal QuotationPrintPreview).

**Scope:** FE only, 3 file:
- `components/assign/quotation/QuotationPrintPreview.vue`
- `pages/assign/quotations/index.vue` (luồng in từ danh sách)
- `pages/assign/quotations/_id/index.vue` (luồng in từ chi tiết)

**4 thay đổi:**
1. **Bỏ cột "Thành tiền nhập"** (kèm tổng tiền nhập dòng V) khỏi bảng "Tổng hợp giá trị" (breakdown-summary-table). Dữ liệu `summary_breakdown.*.nhap` BE vẫn trả, chỉ không hiển thị.
2. **Hiệu lực báo giá:** root cause — template đọc `item.validity_days` nhưng migration `2026_05_28_000002` đã đổi cột thành `validity_date` (date) → luôn rỗng. Fix: hiển thị `Đến ngày dd/mm/yyyy` từ `validity_date`.
3. **Đại diện kinh doanh/ Email:** root cause — 2 màn lấy `emp.name` từ `store.state.employees` (=`Employee::getAll()` trả `CONCAT(departments.code,' - ',fullname)`) và không có email. Fix FE: map fullname từ `store.state.list_employee_infos` (theo `employee_id` → fallback `employee_info_id`), email từ `employees.email`; thêm prop `salesEmployeeEmail`, computed `salesInfo` = `Tên / Email`. Chữ ký "ĐẠI DIỆN KINH DOANH" cuối trang chỉ hiện họ tên. Không đụng BE.
4. **Thông số kỹ thuật dính liền:** root cause — `stripHtml()` lấy `textContent` nên mất `<br>`/`</p>`. Fix: convert `<br>` + đóng thẻ block (`p/div/li/ul/ol/tr/h1-6/blockquote/pre`) → `\n` trước khi strip, dọn nbsp/`\n` thừa; cột specification thêm class `cell-spec` với `white-space: pre-line` (khai báo ở cả style component lẫn CSS inline của cửa sổ in `printContent()`).

**Verify:** Playwright headless (token-inject, BG-2026-00001): 4/4 AC PASS cả 2 luồng in. Không migration/permission/git.
