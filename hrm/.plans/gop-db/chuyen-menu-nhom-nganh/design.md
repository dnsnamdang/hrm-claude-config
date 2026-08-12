# Chuyển menu "Nhóm ngành" sang phân hệ Danh mục dùng chung

> Phụ trách: @khoipv · Bắt đầu: 2026-08-12 · Nhánh: `gop_db` · Trạng thái: đã chốt design
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-12-chuyen-menu-nhom-nganh-design.md`

## Mục tiêu

Đưa mục menu **Nhóm ngành** (`/assign/industry-groups`) từ phân hệ **Bán hàng**
(Danh mục → Danh mục chung) sang phân hệ **Danh mục dùng chung** (`master-data`).

## Phạm vi — CHỈ menu (user chốt 2026-08-12)

Không chuyển route, không chuyển code FE/BE, **không đụng quyền / seeder / DB**.

Lý do không đổi `type` quyền 983/998: `Permission.vue` gom khối **chỉ theo tên `group`**,
mà 983/998 dùng chung `group = 'Danh mục'` với 29 quyền Giao việc → đổi mỗi `type` là vô ích
hoặc kéo nhầm cả 29 quyền sang tab khác. Muốn đổi phải đổi cả `group` + tác động DB đang chạy.
Thêm nữa đợt chuyển phân hệ trước đã bị revert (`2026_08_07_000002_revert_chuyen_code_phan_he_permissions.php`).

## Thay đổi — 3 file, đều ở `hrm-client`

| File | Việc |
|---|---|
| `components/subsystem-menu/sale-hub.js:208` | Xoá mục Nhóm ngành → "Danh mục chung" của Bán hàng còn 3 màn |
| `components/subsystem-menu/sale.js:45` | Xoá gate quyền `/assign/industry-groups` (thành code chết) |
| `components/subsystem-menu/master-data.js` | Thêm mục cấp 1 phẳng sau "Ngân hàng", giữ nguyên link + 2 tên quyền cũ |

## Vì sao 3 file là đủ

- `resolveSubsystem()` map route → phân hệ **theo link khai trong menu**, không theo prefix URL
- `default-sidebar.vue` chọn sidebar hub theo `HUB_SUBSYSTEMS`, `master-data` đã có sẵn → tự đổi
- `deriveHubNavLinks()` biến mục cấp 1 phẳng có link thành nút rail (pattern "Ngân hàng")
- Giữ nguyên 2 tên quyền ở `isShow` → không ai mất/được thêm quyền

## Kết quả người dùng thấy

Bán hàng mất mục Nhóm ngành; Danh mục dùng chung có thêm nút Nhóm ngành; mở màn thì sidebar
đổi sang Danh mục dùng chung. URL cũ vẫn vào được. Màn Phân quyền **không đổi**.

## Nợ kỹ thuật

1. Quyền 983/998 vẫn nằm tab Giao việc › Danh mục ở màn Phân quyền
2. Code vẫn ở `pages/assign/` + `Modules/Assign` → route còn tiền tố `/assign`;
   nếu chuyển thật thì theo quy trình 7 bước ở `.plans/gop-db/chuyen-code-phan-he/design.md`
