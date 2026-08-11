# Design — Tuỳ chỉnh cột màn khách hàng (`/assign/customers`)

- Nhánh: `gop_db` (cả `hrm-api` + `hrm-client`) · Phụ trách: @khoipv · Ngày: 2026-08-10
- **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-08-10-customer-column-config-design.md`

## Mục tiêu

Nút **Cấu hình cột hiển thị** cho màn danh sách KH — ẩn/hiện + kéo thả đổi thứ tự cột,
lưu theo từng user. Tương đương nút "Tùy chỉnh cột" của ERP.

## Scope

- Dùng lại hạ tầng sẵn có: modal chung `column-customization-modal.vue` + API `human/column-customizations`
- BE: 1 migration (thêm cột JSON `customers` vào `column_customizations`) + cast Entity
  + bổ sung 4 join/subquery vào `CustomerService::index()` + 8 field vào `CustomerListResource`
- FE: đổi `tableColumns` sang pattern 3 tầng `allColumns → defaultTableColumns → tableColumns`,
  thêm nút + modal + 8 template cell

## Quyết định lớn

| # | Quyết định |
| --- | --- |
| 1 | Bộ cột = 10 cột hiện có **+ 8 cột ẩn của ERP** (Tên đơn vị, Tên viết tắt, Địa chỉ xuất HĐ, Công ty mẹ, Hãng xe, Cấp đại lý, Người tạo, Người sửa) — 8 cột mới mặc định ẩn |
| 2 | Lưu **theo user** qua `column_customizations` (ERP dùng localStorage theo máy) |
| 3 | **Khoá** `STT` + `Mã KH - Tên khách hàng` (cột 2 chứa nút thao tác) |
| 4 | Cách khoá: **không truyền 2 cột đó vào modal** → không phải sửa component dùng chung của 20+ màn |
| 5 | Cột **Nhóm KH** giữ nguyên `'—'` — tách việc khác |
| 6 | File xuất CSV/Excel **giữ cột cố định**, không theo cấu hình |

## Kết quả đo → đã gate

`index()` dùng chung với popup chọn KH. 5 leftJoin làm `COUNT` phân trang chậm ~3,7 lần
(42.077 KH: 0,12s → 0,43s), `paginate(10)` chậm thêm ~19% (0,468s → 0,555s).

→ Gate sau cờ **`with_extra_columns`**: popup không gửi; màn danh sách chỉ gửi khi user thực sự
bật ≥1 trong 4 cột cần join (`needsExtraColumns`); `exportQuery()` tự join, không phụ thuộc cờ.

## Bẫy đã dính và xử lý

Modal chung dùng `b-form-checkbox :value="column.key"` → cột hiện mặc định **phải** khai
`isVisible: '<đúng key>'`. Để `undefined` thì modal hiện bỏ tích hết, bấm OK là ẩn sạch bảng.

## Ghi nhận, không sửa

`ColumnCustomizationService` nhét thẳng `$request->table` vào tên cột SQL, không whitelist →
bề mặt SQL injection. Service dùng chung 20+ màn, chờ user duyệt mới vá riêng.

## Không đụng tới

`column-customization-modal.vue` · `ColumnCustomizationController/Service` · 2 class export ·
luật che SĐT của `CustomerListResource`
