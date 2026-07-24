# Đối chiếu code hiện tại vs HDSD cũ — Màn "Ứng dụng" (application)

> Agent Opus đọc code FE+BE 2026-07-16. Doc cũ dump: `scratchpad_doc_ungdung.txt`. Ảnh: `hdsd_ungdung_shots/`.

## Thay đổi lớn nhất
- **Nhóm ngành KHÔNG còn tự suy** từ nhóm giải pháp → giờ chọn trực tiếp theo **CẶP "Nhóm ngành : Nhóm giải pháp"** (CascadePairSelect, nhiều cặp).
- **Trường form MỚI BẮT BUỘC**: cặp **"Loại hình hoạt động khách hàng : Lĩnh vực kinh doanh khách hàng"** (≥1 cặp). Trước chỉ là tiêu chí lọc.
- **2 cột danh sách mới**: Loại hình hoạt động KH, Lĩnh vực kinh doanh KH.
- **Tên ứng dụng** cấm ký tự `,` và `:` (vì import dùng làm dấu phân tách cặp).
- Chặn **Khóa** khi ứng dụng đã có dữ liệu liên kết (không chỉ chặn Xóa).

## Route thật
- Danh sách: `/assign/application` (Tạo/Sửa/Xem đều trong modal `application-modal.vue`, không có trang riêng).
- API: `GET assign/applications` (quyền Quản lý|Xem); `GET .../{id}` (không middleware); `POST assign/applications` (updateOrCreate, quyền Quản lý); `GET .../{id}/lock`, `.../unlock`; `DELETE .../{id}`; `POST .../delete_by_ids`; `GET .../export` (file `danh_sach_ung_dung.xls`); `POST .../import/validate`, `POST .../import`.

## Cột danh sách (9 cột + checkbox)
1. Checkbox (chỉ tick dòng is_can_delete) — 2. STT — 3. Mã ứng dụng - Tên ứng dụng (kèm Người tạo/Ngày tạo + **nút Xem/Sửa/Xóa nằm trong ô này**) — 4. Nhóm ngành (scope_names) — 5. Nhóm giải pháp (hiển thị cặp `Nhóm ngành : Nhóm giải pháp`) — 6. **Loại hình hoạt động khách hàng** (MỚI) — 7. **Lĩnh vực kinh doanh khách hàng** (MỚI, cặp `Loại hình : Lĩnh vực`) — 8. Mô tả — 9. Cập nhật (sort) — 10. Trạng thái (pill + nút khóa/mở khóa).

## Nút toolbar
- Tạo mới (chỉ khi có quyền Quản lý) — Import Excel (chỉ Quản lý) — Xuất Excel (luôn hiện ở FE) — khu chọn nhiều: "Đã chọn N dòng" + Xóa (bulk) + Bỏ chọn.

## Nút từng dòng
- Xem (luôn) — Sửa (disabled khi !is_can_edit, chỉ bật khi Hoạt động) — Xóa (disabled khi !is_can_delete, tooltip "Không thể xóa bản ghi... đã có dữ liệu liên kết").
- Khóa/Mở khóa (cột Trạng thái): Khóa disabled khi !is_can_delete (tooltip "Bạn cần khóa hết các danh mục con trước..."); Mở khóa disabled khi !is_can_unlock_update (tooltip "Vui lòng mở khóa danh mục cấp cha trước...").

## Bộ lọc (10 tiêu chí, tự search)
Tìm nhanh (tên/mã) — Nhóm ngành — Nhóm giải pháp (lọc theo Nhóm ngành) — Loại hình hoạt động KH (MỚI) — Lĩnh vực kinh doanh KH (lọc theo Loại hình, MỚI) — Trạng thái — Người tạo — Người cập nhật gần nhất — Cập nhật từ — Đến.

## Form Tạo/Sửa/Xem (modal)
| Trường | Control | Bắt buộc | Mặc định | Khóa |
|---|---|---|---|---|
| Mã ứng dụng * | V2BaseCodeInput prefix "UD." + Nhập 4 ký tự | Có | trống | cấm sửa (BE prohibited) khi đã có dự án tiềm năng |
| Tên ứng dụng * | V2BaseInput | Có | trống | — |
| Trạng thái | V2BaseSelectInModal (Hoạt động/Khóa) | Không | **Hoạt động** | disabled khi !is_can_delete |
| Nhóm ngành : Nhóm giải pháp * | CascadePairSelect (chọn nhiều cặp) | ≥1 cặp | rỗng | — |
| Loại hình hoạt động KH : Lĩnh vực kinh doanh KH * (MỚI) | CascadePairSelect | ≥1 cặp | rỗng | — |
| Mô tả | V2BaseTextarea | Không | trống | — |
- Tooltip: cha Loại hình = "Là tập hợp cùng loại hình hoạt động sản xuất kinh doanh tương đồng về mặt công nghệ."; con Lĩnh vực = "Khách hàng sản xuất kinh doanh sản phẩm dịch vụ cụ thể."
- Tạo mới có nút **Lưu / Lưu & Tiếp tục / Đóng**; Sửa/Xem chỉ **Lưu / Đóng** (Xem: chỉ Đóng). Toast "Thêm mới thành công"/"Cập nhật thành công".
- Validation BE: code size:7 "Vui lòng nhập 4 ký tự"; code regex "Chỉ cho phép: Chữ cái không dấu(A-Z,a-z), chữ số (0-9) và dấu gạch dưới (_)."; code prohibited "Không thể sửa mã khi đã có dữ liệu phát sinh liên quan."; code/name unique; **name not_regex `/[,:]/` "không được chứa ký tự dấu phẩy (,) và dấu hai chấm (:)"**; industry_pairs min:1 "Vui lòng chọn ít nhất 1 Nhóm giải pháp"; customer_scope_pairs min:1 "Vui lòng chọn ít nhất 1 Lĩnh vực kinh doanh khách hàng"; cross-check "Nhóm giải pháp không thuộc Nhóm ngành đã chọn" / "Lĩnh vực không thuộc Loại hình đã chọn".

## Quyền
- `Quản lý danh mục ứng dụng` (id 985): create/update, import, import/validate, export, lock, unlock, destroy, delete_by_ids.
- `Xem danh mục ứng dụng` (id 1000): route index (OR với Quản lý).

## Import Excel
- Popup "Import Ứng dụng — Chỉ nhập theo code • Validate xong dòng hợp lệ sẽ bị khoá". Nút: Chọn file Excel, Tải file mẫu, Load lên bảng, Validate, Import, Chỉ dòng lỗi, Đóng, Làm mới, Tổng: N.
- Cột file: Mã ƯD, Tên ƯD, Nhóm giải pháp (cặp `MãNhómNgành:MãNhómGiảiPháp`, ngăn dấu phẩy), Lĩnh vực KD KH (cặp `MãLoạiHình:MãLĩnhVực`, optional), Trạng thái (bắt buộc active/inactive), Mô tả. Bắt buộc: Code, Name, CatCode (Nhóm giải pháp), Status. File mẫu `Mau_Import_UngDung_FN.xlsx`. Validate 2 bước, tối đa 1000 dòng/lần.

## Ảnh đã chụp (hdsd_ungdung_shots/)
01 danh-sách, 02 bộ-lọc, 03 thêm-mới, 04 sửa, 05 xem-chi-tiết, 06 popup-xóa, 07 popup-khóa, 08 import.
(Xuất Excel = tải file, mô tả text; không chụp step import populated để tránh tạo dữ liệu thật.)

## Điểm KHỚP (giữ nguyên)
Điều kiện Sửa (chỉ Hoạt động), điều kiện Xóa (chưa gắn dự án tiềm năng), điều kiện Mở khóa (còn ≥1 nhóm giải pháp & tất cả active), Trạng thái mặc định Hoạt động, Mã UD.XXXX, 2 quyền, Xuất Excel theo lọc.
