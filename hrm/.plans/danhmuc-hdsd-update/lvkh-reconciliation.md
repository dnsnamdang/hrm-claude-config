# Đối chiếu code vs HDSD cũ — Màn "Lĩnh vực khách hàng" → nay "Lĩnh vực kinh doanh khách hàng" (customer-scopes)

> Agent Opus 2026-07-16. Doc cũ dump: `scratchpad_doc_lvkh.txt`. Ảnh: `hdsd_lvkh_shots/`. Template doc CÓ Caption/List Bullet/Light Grid Accent 1 → dùng generator kiểu gen_phieu.py.

## Thay đổi lớn nhất
- **Đổi tên toàn bộ**: "Lĩnh vực khách hàng" → **"Lĩnh vực kinh doanh khách hàng"**; menu "Lĩnh vực kinh doanh KH".
- **Mã đổi tiền tố**: LVKH.XXXX (9 ký tự) → **LVKDKH.XXXX (11 ký tự, size:11)**.
- **Cha đổi tên**: "Nhóm lĩnh vực khách hàng" → **"Loại hình hoạt động khách hàng"** (customer-scope-groups).
- **Nút Xóa & Khóa/Mở khóa nay LUÔN BẬT**: BE `CustomerScope::isCanLockUpdate()` hardcode `return true` → `is_can_lock_update` luôn true. Doc cũ "chỉ bật khi không còn dữ liệu liên kết" KHÔNG còn đúng. Xóa là hard delete, không check ràng buộc.
- **Tên cấm ký tự** `,` và `:` (not_regex).

## Route & bản đồ màn
- `/assign/customer-scopes`. Tạo/Sửa/Xem trong modal `AddScopeModal.vue` (add-scope). Tiêu đề màn "Danh sách lĩnh vực kinh doanh khách hàng".
- Cột: 1 STT — 2 **Mã - Tên lĩnh vực kinh doanh khách hàng** (kèm Người tạo/Ngày tạo + 3 nút Xem/Sửa/Xóa) — 3 **Loại hình hoạt động khách hàng** (danh sách tên cha) — 4 Mô tả — 5 Cập nhật (sort) — 6 Trạng thái (pill + nút khóa/mở khóa).
- Toolbar: Tạo mới (canManage) — Xuất Excel (**luôn hiện**, kể cả quyền Xem, nhưng route BE export cần quyền Quản lý → user Xem bấm sẽ 403 im lặng) — Import Excel (canManage) — Tìm kiếm nâng cao.
- Nút dòng: Xem (luôn) — Sửa (disabled khi status=2 Khóa) — Xóa (luôn bật) — Khóa/Mở khóa (luôn bật).

## Bộ lọc (7 tiêu chí + tìm nhanh)
Tìm nhanh (BE chỉ lọc **name + code**, dù placeholder ghi cả người tạo/cập nhật) — Mã lĩnh vực kinh doanh KH — Lĩnh vực kinh doanh khách hàng (tên) — Trạng thái — Người tạo — Người cập nhật — Cập nhật từ — Cập nhật đến. Auto-search.

## Quyền
- `Quản lý danh mục lĩnh vực khách hàng` (id 996): store/update/delete/lock/unlock/export/import/validate.
- `Xem danh mục lĩnh vực khách hàng` (id 1006): index (OR). Route show/getAll không middleware.

## Form Tạo/Sửa/Xem (AddScopeModal)
| Trường | Control | Bắt buộc | Mặc định | Khóa |
|---|---|---|---|---|
| Mã lĩnh vực kinh doanh KH * | V2BaseCodeInput prefix "LVKDKH." + Nhập 4 ký tự | Có | rỗng | disabled khi Xem; BE cấm sửa mã nếu đã có application liên kết |
| Lĩnh vực kinh doanh khách hàng * | V2BaseInput (VD: Công nghệ thông tin) | Có | rỗng | disabled khi Xem |
| Trạng thái | V2BaseSelectInModal (allowClear=false) | luôn có giá trị | Hoạt động | disabled khi Xem |
| Loại hình hoạt động khách hàng * | V2BaseSelectInModal **multiple** | ≥1 | [] | disabled khi Xem; options chỉ nhóm đang Hoạt động |
| Mô tả | V2BaseTextarea | Không | rỗng | disabled khi Xem (form KHÔNG giới hạn 1000; chỉ import ≤1000) |
- Nút: Tạo mới = Lưu / Lưu & Tiếp tục / Đóng; Sửa = Lưu / Đóng; Xem = chỉ Đóng. Toast "Thêm mới thành công"/"Cập nhật thành công".
- Validation BE: code size:11 "Vui lòng nhập 4 ký tự"; code regex "Chỉ cho phép: Chữ cái không dấu(A-Z,a-z), chữ số (0-9) và dấu gạch dưới (_)."; code prohibited "Không thể sửa mã khi đã có dữ liệu phát sinh liên quan."; code/name unique; name not_regex "không được chứa ký tự dấu phẩy (,) và dấu hai chấm (:)"; customer_scope_group_ids required min:1 "Vui lòng chọn ít nhất 1 loại hình hoạt động khách hàng"; nếu nhóm bị khóa: "Loại hình hoạt động khách hàng \"…\" đã bị khoá, vui lòng chọn loại hình khác". Không có mã tự sinh.

## Popup xóa / khóa (câu chữ thật)
- Xóa: "Xác nhận xóa — Bạn có chắc muốn xóa lĩnh vực kinh doanh khách hàng '…'?" (Hủy/Xóa).
- Khóa: "Xác nhận khoá — Bạn có chắc muốn khoá lĩnh vực kinh doanh khách hàng '…'?" (Hủy/Khoá); mở khóa tương tự "Xác nhận mở khoá".

## Import Excel (file mẫu Mau_import_LVKH.xlsx)
Cột: Code (Mã LVKDKH.XXXX, bắt buộc) — Name (tên, bắt buộc, ≤255, không `,` `:`) — GroupCode (Mã loại hình hoạt động KH, **tùy chọn**, nhiều mã ngăn dấu phẩy, VD LHHDKH.0001; nhóm phải Hoạt động) — Status (bắt buộc, Hoạt động/Khóa hoặc active/inactive) — Description (≤1000). Bắt buộc: Code, Name, Status. Validate 2 bước. LƯU Ý: cha bắt buộc ở FORM nhưng tùy chọn khi IMPORT.

## Xuất Excel
9 cột: Mã lĩnh vực, Tên lĩnh vực kinh doanh khách hàng, Loại hình hoạt động khách hàng, Mô tả, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật. File `danh_sach_linh_vuc_kinh_doanh_khach_hang.xls`.

## Ảnh (hdsd_lvkh_shots/)
01 danh-sách, 02 bộ-lọc, 03 thêm-mới, 04 sửa, 05 xem-chi-tiết, 06 popup-xóa, 07 popup-khóa, 08 import.
