# #12041 — PNK luồng mua: cho phép bỏ tích "Cần giữ" ở tab Phân bổ hàng giữ (HRM)

Redmine: http://quanly.dnsmedia.vn/issues/12041 — bám ERP (cùng ticket, ERP/.plans/bo-tich-phan-bo-hang-giu).
HRM tab "Phân bổ hàng giữ" có ở loại 2/15 (importTypeConfig holdAllocation).

## Hiện trạng
- `ProductImportForm.vue` cột "Cần giữ": `<V2BaseCheckbox :value="c.allocation" :disabled="true" />`, header không có ô tích tất cả.
- BE `ProductImportService` lưu `$customer->allocation`, `ProductImport` chỉ prepick khi allocation → KHÔNG sửa BE.

## Tasks
- [x] Ô tích từng dòng cho bấm; bỏ tích → `$confirm` "Bạn chắn chắn không phân bổ giữ <tên hàng>?"; Hủy → giữ tích
- [x] Header "Cần giữ" thêm ô tích tất cả; bỏ tích → `$confirm` "Bạn chắn chắn không phân bổ giữ tất cả mục hàng?"
- [x] Tích lại mà Hạn giữ trống → điền mặc định
- [x] Nút popup theo chuẩn HRM "Xác nhận / Hủy" (user chốt 10/11, xem design.md)
- [x] Chặn "tiếng vọng": b-form-checkbox phát `input` cả khi prop đổi từ code → bỏ tích 1 dòng làm ô "tất cả" hỏi nhầm. Handler bỏ qua khi giá trị trùng trạng thái hiện tại
- [x] Playwright (client worktree chạy cổng 3001): tạo PNK loại 15 từ ĐNNK 8910 — dòng Hủy/Xác nhận/tích lại, header Hủy/Xác nhận/tích lại đều đúng; payload Lưu nháp `allocation:0, expire_prepick_date:null` (request bị chặn, không ghi DB)
- Ghi chú (không có dữ liệu thử): chưa thử màn Sửa + loại 2 (cùng component, không có dữ liệu sẵn)

### Checkpoint — 10/11/2026
Vừa hoàn thành: FE + Playwright tạo loại 15
Đang làm dở: —
Bước tiếp theo: chờ user cho commit/push develop (worktree hrm-client-12041, nhánh fix/12041-bo-tich-phan-bo-giu)
Blocked:

