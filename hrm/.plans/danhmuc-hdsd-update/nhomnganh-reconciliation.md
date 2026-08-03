# Đối chiếu code vs HDSD cũ — Màn "Nhóm ngành" (industry-groups = scopes)

> Agent Opus 2026-07-16. Doc cũ: `scratchpad_doc_nhomnganh.txt`. Ảnh: `hdsd_nhomnganh_shots/`. Template KHÔNG có Caption/List Bullet/Light Grid Accent 1 → generator kiểu gen_ungdung.py.

## Kết luận: doc cũ KHỚP phần lớn; chỉ sửa văn bản/quy tắc nhỏ.
FE `/assign/industry-groups`; BE gọi là `scope` (bảng scopes, API `/assign/scopes`). Con = Nhóm giải pháp (industries) + Ứng dụng (applications).

## Cột danh sách (7, KHỚP): STT — Mã nhóm ngành - Tên nhóm ngành (+Người tạo/Ngày tạo + nút Xem/Sửa/Xóa) — Số nhóm giải pháp (link tab mới sang solution-groups?scope_id) — Số ứng dụng (link sang application?scope_id) — Mô tả — Cập nhật (sort) — Trạng thái (pill + khóa/mở khóa).
## Toolbar: Tạo mới (canManage) · Import Excel (canManage) · Xuất Excel (luôn hiện). Nút dòng: Xem (luôn) · Sửa (disabled khi Khóa) · Xóa (disabled khi industries_count>0 || applications_count>0, tooltip "Không thể xóa bản ghi...") · Khóa/Mở khóa (khóa disabled khi còn NGP con active, tooltip "Bạn cần khóa hết các danh mục con trước...").
## Bộ lọc (8, KHỚP): Tìm nhanh (BE chỉ name+code) · Mã nhóm ngành · Tên nhóm ngành · Trạng thái · Người tạo · Người cập nhật · Cập nhật từ · Cập nhật đến. Auto-search.
## Quyền: "Quản lý danh mục nhóm ngành" (id 983) / "Xem danh mục nhóm ngành" (id 998).

## Form Tạo/Sửa/Xem (AddScopeModal)
| Trường | Control | Bắt buộc | Mặc định | Khóa |
|---|---|---|---|---|
| Mã nhóm ngành * | V2BaseCodeInput prefix "NN." + Nhập 4 ký tự | Có | rỗng | disabled khi Xem (KHÔNG disable khi Sửa; chặn đổi mã ở lưu nếu đã có con) |
| Tên nhóm ngành * | V2BaseInput | Có | rỗng | disabled khi Xem |
| Trạng thái | V2BaseSelectInModal | Không | Hoạt động | disabled khi Xem hoặc còn NGP con active |
| Mô tả | V2BaseTextarea | Không | rỗng | disabled khi Xem (form KHÔNG giới hạn 1000; chỉ import ≤1000) |
| Số nhóm giải pháp / Số ứng dụng | input disabled | — | 0 | CHỈ hiện ở chế độ Xem |
- Nút: Tạo = Lưu / Lưu & Tiếp tục / Đóng; Sửa = Lưu / Đóng; Xem = chỉ Đóng.
- Toast: **"Thêm mới thành công" / "Cập nhật thành công"** (doc cũ ghi sai "Thao tác thành công").
- Validation: name required, max 255, unique, **not_regex "không được chứa ký tự dấu phẩy (,) và dấu hai chấm (:)"**; code required, size:7 "Vui lòng nhập 4 ký tự", regex "Chỉ cho phép: Chữ cái không dấu(A-Z,a-z), chữ số (0-9) và dấu gạch dưới (_).", unique, prohibited (đổi mã khi đã có con) "Không thể sửa mã khi đã có dữ liệu nhóm giải pháp hoặc ứng dụng liên quan.". Không mã tự sinh.

## Popup xóa/khóa (câu chữ thật)
- Xóa: "Xác nhận xóa — Bạn có chắc muốn xóa nhóm ngành '…'?" (Hủy/Xóa).
- Khóa: "Xác nhận khoá — Bạn có chắc muốn khoá nhóm ngành '…'?" (Hủy/Khoá).

## Import (Mau_import_NhomNganh.xlsx)
Cột Code*/Name*/Status*/Description. Bắt buộc: Code, Name, Status. Code import regex `NN.[A-Z0-9]{4}` (KHÔNG chấp nhận gạch dưới, khác form). Status active/inactive. Chống trùng trong file + DB.

## Xuất Excel
File `danh_sach_nhom_nganh.xls` theo bộ lọc.

## Bảng lệch chính cần sửa doc
- Toast "Thao tác thành công" → "Thêm mới/Cập nhật thành công".
- Tìm nhanh: bỏ "người tạo, người cập nhật" (BE chỉ name+code).
- Bổ sung: Tên cấm `,` `:`; Mô tả form không giới hạn 1000 (chỉ import); mã Sửa không bị khóa ô mà chặn ở lưu; import Status bắt buộc.
- Xem chi tiết hiện thêm Số nhóm giải pháp + Số ứng dụng.

## Ảnh (hdsd_nhomnganh_shots/): 01 danh-sách, 02 bộ-lọc, 03 thêm-mới, 04 sửa, 05 xem-chi-tiết, 06 popup-xóa, 07 popup-khóa, 08 import.
