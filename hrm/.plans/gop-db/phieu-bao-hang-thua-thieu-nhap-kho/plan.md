# Phiếu báo hàng thừa, thiếu nhập kho — Plan

Người phụ trách: @khoipv
Màn: `hrm-client/pages/warehouse/exc-shortage-imports/` · BE: `Modules/Finance` (`ExcShortageController`, `ExcShortageService`)

## Fix #11850 — Lỗi UI form tạo (2026-10-26)

- [x] FE: ô "Phiếu nhập kho" dùng khuôn `.source-select` của màn mẫu Phiếu nhập kho (bấm cả ô mở popup, icon `ri-search-line` phẳng trong ô) — thay `V2BasePickerField`, import `wi-shared.scss`
- [x] FE: popup Chọn phiếu nhập kho — cột Mã phiếu là link mở chi tiết PNK ở tab mới (không chọn dòng)
- [x] FE dùng chung (user duyệt): `RecordPickerModal` thêm tuỳ chọn cột `href(item)` — chỉ màn khai báo mới bật, các màn khác giữ nguyên
- [x] FE: sort cột Mã phiếu, Ngày tạo trong popup
- [x] BE: `queueQuery` nhận `sort_by` (popup) ngoài `sort_field` (màn danh sách)

### Checkpoint — 2026-10-26
Vừa hoàn thành: fix #11850 (3 ý), PHP lint + compile template/script FE OK, kiểm SQL order by với sort_by
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm `/warehouse/exc-shortage-imports/create`
Blocked:
