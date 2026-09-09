# Chuẩn hoá màn Danh sách ứng dụng theo skill `list-page`

- **Người phụ trách:** @khoipv
- **Nhánh:** `gop_db` (cả `hrm-api` + `hrm-client`)
- **Màn:** `/assign/application` — `hrm-client/pages/assign/application/index.vue`
- **Ngày:** 2026-09-05 · Màn thứ 3 sau [solutions](../solution-list-page-standard/design.md) và [industry-groups](../industry-group-list-page-standard/design.md)

## Phạm vi (giữ đúng như 2 màn trước)

FE đầy đủ theo skill `list-page` + `button-convention`, BE tối thiểu (whitelist sort, tên người tạo,
popup chọn trường xuất Excel). **KHÔNG làm lịch sử thay đổi** — không thuộc phạm vi user giao.

## Hiện trạng lệch chuẩn

| Điểm | Hiện tại | Chuẩn |
| --- | --- | --- |
| Panel lọc | `V2BaseFilterPanel` + `title`/`subtitle` riêng, 9 ô hard-code trong slot | `V2BaseSmartFilterPanel` + schema `filterFields` |
| Cột định danh | 1 cột gộp `Mã - Tên`, chứa luôn 3 nút thao tác | Tách `Mã` (button `.v2-cell-link` mở modal Xem) / `Tên` |
| Hành động | Xem / Sửa / Xóa nhét dưới tên, disable + tooltip | Cột "Hành động" cuối, `V2BaseRowActions`, bỏ "Xem", ẩn thay vì disable |
| Nút Khóa/Mở khóa | Nằm TRONG ô Trạng thái | Chuyển sang cột Hành động (menu `⋮`) |
| Trạng thái | `v-html` + `status-pill` tự dựng | `V2BaseBadge` `variant` brand/required |
| Người tạo / Ngày tạo | Là dòng phụ trong cột gộp | Cột riêng, bắt buộc |
| Cấu hình cột | không có | `columnCustomizationMixin` |
| Giữ bộ lọc khi quay lại | không có | `filterStateMixin` |
| Xuất Excel | tải thẳng cả bảng, `$nuxt.$loading` | Popup chọn trường + `$safeLoading` |
| Sort | BE whitelist chỉ có `updatedAt` | Mã / Tên / Ngày tạo / Ngày cập nhật |
| Thứ tự request | `await` 4 request danh mục xong mới gọi danh sách | `loadData()` bắn đầu tiên, danh mục hoãn tới khi mở panel |
| Import Excel | `secondary` trắng | `secondary status="warning"` + icon `ri-upload-line` |
| Ô rỗng | in `—` | Để trống |

## Quyết định

- **Giữ nguyên chọn nhiều dòng + Xóa hàng loạt** — đây là chức năng thật của màn, không thuộc diện
  chuẩn hoá. Cột ô chọn khai `sticky` + `locked` cùng nhóm với STT / Mã (`getStickyColumnStyle` cộng
  dồn `width` các cột sticky đứng trước nên cột này bắt buộc có `width` = `minWidth`).
- **Link `?scope_id=` / `?industry_id=`** từ màn Nhóm ngành và Nhóm giải pháp bấm sang: giữ nguyên,
  áp SAU khi khôi phục bộ lọc đã lưu để đường link thắng bộ lọc lần trước (skill mục 3d), và chỉ nhận
  đúng 2 khoá đã biết.
- **Bộ cột mặc định 7 cột + ô chọn**: Chọn · STT · Mã ứng dụng · Tên ứng dụng · Người tạo · Ngày tạo ·
  Trạng thái · Hành động. Nhóm ngành, Nhóm giải pháp, Loại hình hoạt động KH, Lĩnh vực kinh doanh KH,
  Mô tả, Người/Ngày cập nhật khai đủ nhưng mặc định ẩn.
- **Không làm lịch sử thay đổi.**
