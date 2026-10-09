# Final Fix Report — YCCGKH (task_10696)

**Status tổng thể:** DONE — 4/4 fixes áp dụng thành công  
**Branch:** `task_10696`  
**Commit:** `20ba036159`  
**Thời gian:** 2026-07-04

---

## Fix A — Excel trạng thái (CustomerHandoverRequestExport.php)

**Status: DONE**

`STATUSES` là array of objects `[{id, name, type}, ...]`, KHÔNG phải keyed map.  
Sửa từ `STATUSES[$item->status] ?? ''` (luôn trả object, không phải tên)  
sang `collect(STATUSES)->firstWhere('id', $item->status)['name'] ?? ''`.

---

## Fix B — Menu top bar "Phiếu YC chuyển giao khách hàng" (topmenubar.blade.php)

**Status: DONE**

Đổi `route('customerHandover.index')` → `route('customerHandover.all')`.  
`all` route render tất cả phiếu (màn dành cho approver), phù hợp làm link trên menu.

---

## Fix C — Xóa approve.blade.php orphan

**Status: DONE — FILE ĐÃ XÓA**

`approve.blade.php` (433 dòng) không có bất kỳ GET route nào render.  
Controller `approve()` là POST action trả JSON. Không có tham chiếu nào trong routes/controllers.  
→ Dead code, đã xóa sạch.

---

## Fix D — Validate CustomerHandoverStoreRequest

**Status: DONE**

Thêm 2 rules:
- `new_customer_data.delivery_place_id` => `required` → "Địa chỉ giao/sửa là bắt buộc."
- `new_customer_data.deputy_id` => `required_unless:new_customer_data.customer_type,1` → "Người đại diện là bắt buộc đối với khách hàng doanh nghiệp."

`Customer::CA_NHAN = 1` là Cá nhân, các loại DN là 2/3/4. Rule handle đúng: bắt buộc deputy khi type != 1.

---

## Fix E — Market/Thị trường check trong store()

**Status: DEFERRED**

Grep tìm thấy `marketDivisionContract()` / `marketDivisionCustomerContract()` trong `FirmQuotationService`, nhưng không có cơ chế nào reusable rõ ràng cho CustomerHandoverRequest. Cần spec từ BA/PO.

---

## Concerns

- `required_unless` với nested key `new_customer_data.customer_type`: valid Laravel 6. Nếu FE gửi customer_type là string thay vì integer → cần FE đảm bảo gửi integer.
- Worktree branch không liên quan đến commit này; patch đã apply trực tiếp vào main checkout `task_10696`.
