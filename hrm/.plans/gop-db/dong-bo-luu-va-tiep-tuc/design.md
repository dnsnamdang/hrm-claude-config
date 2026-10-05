# Design — Đồng bộ nút "Lưu và tiếp tục" (Redmine #11177)

Nhánh: `gop_db` · @junfoke · Bắt đầu 2026-09-05
Issue: http://quanly.dnsmedia.vn/issues/11177 — *Đồng bộ thêm nút lưu và tiếp tục*

## Mục tiêu

Mọi màn **Tạo mới** (popup danh mục lẫn trang tạo phiếu) đều có nút **"Lưu và tiếp tục"**:
lưu bản ghi xong **ở lại màn Tạo**, form về trắng để nhập bản ghi kế tiếp — thay vì phải quay ra
danh sách rồi bấm "Tạo mới" lại.

## Quyết định đã chốt

1. **Phạm vi** (user chốt 2026-09-05): 3 popup danh mục còn thiếu + **toàn bộ trang `create.vue`
   của phân hệ Tài chính và CSKH**, kể cả màn không nằm trong danh sách issue (đồng bộ luôn một thể).
2. **Hành vi ở trang tạo phiếu**: lưu xong → toast thành công → **reset trắng, ở lại trang tạo**
   (không điều hướng về danh sách như nút Lưu thường).
3. **Nút "Lưu và tiếp tục" chỉ hiện ở chế độ TẠO MỚI** (`mode === 'create'`, popup thì `!id`) —
   màn Sửa/Xem không có.
4. **Kiểu nút**: `secondary` (nút phụ), đứng **sau** nút Lưu chính. Popup dùng
   `V2BaseButton secondary`; trang dùng cờ `menu.submit_and_continue` của `V2Footer` (component
   đã render sẵn đúng vị trí/màu, xem `components/V2Footer.vue:92`).
5. **Phiếu có 2 nút lưu** (Lưu nháp / Lưu và gửi duyệt): "Lưu và tiếp tục" lưu theo nhánh
   **Lưu nháp** — người dùng còn muốn nhập tiếp thì phiếu vừa lưu để nháp là an toàn nhất,
   muốn gửi duyệt thì đã có nút riêng.
6. **Cách reset form ở trang phiếu**: KHÔNG viết `resetForm()` thủ công cho từng form (30 form,
   mỗi form một mớ state/ref/option riêng → dễ sót). Form `$emit('savedAndContinue')`, trang vỏ
   `create.vue` tăng `formKey` → Vue **remount** component form ⇒ toàn bộ state, validate, dòng
   hàng hoá, option về mặc định y như vừa vào màn. Trước khi remount phải `markFormSaved()` để
   guard "chưa lưu" không chặn.

## Nguồn pattern (copy, không tự phát minh)

| Loại màn | Copy từ |
| --- | --- |
| Popup danh mục | `components/modal/customer-care/level-modal.vue` (footer + `saveItem(true)` + `resetModal()`) |
| Trang tạo mới | `pages/assign/questions/add.vue` (`menu.submit_and_continue` + `@submitAndContinue`) |

ERP (`TanPhatDev`) **không có** nút này — đây là quy ước riêng của HRM, không phải port từ ERP.

## Ngoài phạm vi

- **Cập nhật nhanh giá dịch vụ**, **Danh sách hàng giữ**, **Danh mục serial thiết bị làm dịch vụ**:
  không có chức năng Tạo mới → không có chỗ gắn nút.
- Các modal tìm kiếm/chọn dữ liệu (`*SearchModal`, `*PickerModal`) và modal từ chối
  (`RejectModal`) — không phải popup Tạo mới.

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-05-dong-bo-luu-va-tiep-tuc-design.md`
