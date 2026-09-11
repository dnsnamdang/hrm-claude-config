# Plan — BOM List: In bản ghi

## Phase 1 — In BOM List

### BE
- [x] `BomListService::loadDetail()` eager load `prospectiveProject`, `solution`, `solutionModule`, `employee_create.info.department`
- [x] `DetailBomListResource` trả thêm `prospective_project_code/name`, `solution_code/name`, `solution_module_name`, `bom_list_type_name`, `department_name`

### FE
- [x] Tạo `pages/assign/bom-list/components/BomPrintConfigModal.vue` — chọn cột + "Hiện hàng hoá cấp con"
- [x] Tạo `pages/assign/bom-list/components/BomPrintPreview.vue` — popup xem trước + nút In (iframe ẩn), 1 nguồn CSS
- [x] Tạo `utils/mixins/bomPrintMixin.js` — nạp chi tiết BOM, mở cấu hình → xem trước
- [x] `pages/assign/bom-list/index.vue` — thêm row action In
- [x] `pages/assign/bom-list/_id/index.vue` — thêm nút In ở footer

### Checkpoint — 2026-08-27
Vừa hoàn thành: toàn bộ Phase 1 (BE trả tên hiển thị + 3 file FE mới + wiring 2 màn)
Đang làm dở: không
Bước tiếp theo: user test trên UI (in từ danh sách và từ màn chi tiết)
Blocked:

## Phase 2 — Sửa sau khi test UI (2026-08-27)

- [x] Backtick trong chú thích nằm trong template literal của `bomPrintStyle.js` → đứt chuỗi, webpack báo lỗi parse. Bỏ backtick
- [x] `th` xem trước 12px / bản in 10px (CSS toàn cục HRM thắng thừa kế) → khai `font-size` thẳng trên `th, td`
- [x] `line-height` bảng: xem trước 16.25px / bản in `normal` → khai `line-height: 1.25` cho `table/thead/tbody/tr/th/td`
- [x] `b`/`strong` xem trước 500 / bản in 700 → khai `font-weight: 700`
- [x] `img` vertical-align lệch → khai `middle`
- [x] Đo lại bằng iframe: **0 lệch / 152 phần tử** trên 13 thuộc tính hình thức

### Checkpoint — 2026-08-27 (sau test)
Vừa hoàn thành: test UI đầy đủ trên :3000, sửa 5 lỗi phát hiện lúc test
Đang làm dở: không
Bước tiếp theo: chờ user nghiệm thu
Blocked:
