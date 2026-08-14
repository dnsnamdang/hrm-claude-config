# Plan — Đồng nhất ký tự "không có dữ liệu" ở màn Danh sách khách hàng

Nhánh: `gop_db` (worktree `HRM/worktrees/gop_db-api` + `gop_db-client`)
Màn: `/assign/customers` + popup chọn KH (`ChooseErpCustomerModal`)

## Hiện trạng (bug)

Ô trống mỗi cột hiển thị mỗi kiểu:

- Mọi cột FE (`tax_code`, `short_name`, `email`, `group_names`, `address`, `province_name`, 8 cột cấu hình…)
  đều dùng `{{ item.xxx || '—' }}` → gạch dài **—** (em dash).
- Riêng **SĐT** hiển thị gạch ngắn **-** vì BE tự chèn sẵn:
  `CustomerListResource:34` → `'mobile' => $isMine ? ($this->mobile ?: '-') : '-'`
  → FE nhận chuỗi `'-'` (khác rỗng) nên `|| '—'` không chạy.
- Trong popup chọn KH, các cột không có template riêng render thẳng giá trị → `null` ra **ô trắng**,
  còn `mobile` ra **-**.

## Phase 1 — BE

- [x] `Modules/Assign/Transformers/CustomerResource/CustomerListResource.php`:
      `mobile` trả `null` (cả khi trống lẫn khi bị che vì không phải KH của mình) thay vì `'-'`.
      Ký tự hiển thị do FE quyết định, BE không chèn placeholder.
- [x] Sửa comment ownership cho khớp (bỏ chữ "che '-'").
- [x] `php -l` PASS.

## Phase 2 — FE

- [x] `components/modals/ChooseErpCustomerModal.vue`: thêm slot fallback `#cell()` →
      giá trị `null`/`undefined`/`''` hiển thị `—`. Áp cho cả 7 cột không có template riêng
      (Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP), không đụng `index` / `customerInfo`.
- [x] Màn danh sách `pages/assign/customers/index.vue`: giữ nguyên, đã dùng `|| '—'` đồng nhất.

## Ghi chú / quyết định

- **SĐT bị che và SĐT trống nhìn giống hệt nhau** — đúng như hành vi cũ (trước đây cả 2 đều ra `'-'`),
  chỉ đổi ký tự. Không lộ thêm thông tin, không mất thông tin.
- **File xuất (CSV/Excel) GIỮ NGUYÊN `'-'`**: `app/ExcelExport/CustomerExportFormatter.php::taxCodeOrMobile()`
  theo đúng mẫu ERP, đây là ngữ cảnh khác (file bàn giao), không phải màn hình.
- Không migration, không đổi API contract (chỉ đổi giá trị `mobile` từ `'-'` → `null`).
- Đã rà: không chỗ nào FE so sánh `mobile === '-'`.

## Còn lại

- [ ] User test trình duyệt: màn `/assign/customers` (cả 18 cột, bật/tắt ở Cấu hình cột hiển thị)
      + popup chọn KH → mọi ô trống đều là `—`.

### Checkpoint — 2026-08-12
Vừa hoàn thành: Phase 1 + Phase 2 (2 file), `php -l` PASS.
Đang làm dở: không.
Bước tiếp theo: user test trình duyệt rồi commit trên nhánh `gop_db`.
Blocked:
