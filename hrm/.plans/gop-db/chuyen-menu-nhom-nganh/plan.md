# Plan — Chuyển menu "Nhóm ngành" sang phân hệ Danh mục dùng chung

> Phụ trách: @khoipv · Nhánh: `gop_db` (repo `hrm-client`) · Bắt đầu: 2026-08-12
> Design: `.plans/gop-db/chuyen-menu-nhom-nganh/design.md`
> Spec: `docs/superpowers/specs/gop-db/2026-08-12-chuyen-menu-nhom-nganh-design.md`

**Mục tiêu:** mục menu **Nhóm ngành** (`/assign/industry-groups`) rời phân hệ Bán hàng, xuất hiện
ở phân hệ Danh mục dùng chung, giữ nguyên URL và quyền.

**Cách làm:** chỉ sửa 3 file khai báo menu ở `hrm-client/components/subsystem-menu/`.
Route → phân hệ được `resolveSubsystem()` suy **từ chính khai báo menu**, nên chuyển khai báo là
sidebar/hub/tổng quan tự đổi theo — không đụng page, BE, quyền, DB.

**Tech:** Nuxt 2 / Vue 2, menu là các module JS export mảng object.

## Ràng buộc bắt buộc

- Repo `hrm-client` phải đang ở nhánh `gop_db`
- **Không** sửa `pages/assign/industry-groups/*`, **không** sửa BE, **không** sửa
  `PermissionsTableSeeder.php`, **không** viết migration, **không** chạy SQL
- `isShow` phải là **mảng tên quyền** `['Quản lý danh mục nhóm ngành', 'Xem danh mục nhóm ngành']`
  — copy nguyên từ `sale.js:45`. Không dùng `isShow: true`, không hard-code cờ quyền
- Không commit / push (theo quy tắc dự án)

## Bảng file

| File | Việc |
|---|---|
| `hrm-client/components/subsystem-menu/sale-hub.js` | Sửa — bỏ 1 dòng màn khỏi mục "Danh mục chung" |
| `hrm-client/components/subsystem-menu/sale.js` | Sửa — bỏ 1 entry gate quyền đã thành code chết |
| `hrm-client/components/subsystem-menu/master-data.js` | Sửa — thêm 1 mục cấp 1 phẳng |

---

## Phase 1 — Chuyển khai báo menu

### Task 1: Bỏ mục Nhóm ngành khỏi phân hệ Bán hàng

**File:** `hrm-client/components/subsystem-menu/sale-hub.js:205-213`

- [x] **B1.** Xoá dòng 208 trong nhóm `Danh mục` → mục `Danh mục chung`:

```js
{
    title: 'Danh mục chung',
    screens: [
        // XOÁ dòng dưới:
        { n: 'Nhóm ngành', link: '/assign/industry-groups' },
        { n: 'Phiếu thu thập thông tin', link: '/assign/form-templates' },
        ...
```

- [x] **B2.** Kiểm tra mục `Danh mục chung` còn đúng 3 màn, cú pháp mảng không lỗi dấu phẩy.
- [x] **B3.** Xác nhận không sửa gì khác trong file (`sale-hub.js` là nguồn chung của cả hub
  `/sale/dashboard` lẫn cây sidebar `saleItems` qua `sale.js::buildSaleTree`).

### Task 2: Bỏ gate quyền đã chết ở `sale.js`

**File:** `hrm-client/components/subsystem-menu/sale.js:41-56` (`SALE_LINK_PERMISSIONS`)

- [x] **B1.** Xoá dòng 45:

```js
'/assign/industry-groups': ['Quản lý danh mục nhóm ngành', 'Xem danh mục nhóm ngành'],
```

- [x] **B2.** Trước khi xoá, **copy nguyên mảng 2 tên quyền** để dùng ở Task 3 (đây là nguồn
  duy nhất của gate này, xoá xong không tra lại được).
- [x] **B3.** Xác nhận không còn leaf nào trong cây Bán hàng có link `/assign/industry-groups`
  (nếu còn, `toLeaf()` sẽ mất gate → màn lộ cho người không quyền).

### Task 3: Thêm mục Nhóm ngành vào phân hệ Danh mục dùng chung

**File:** `hrm-client/components/subsystem-menu/master-data.js` — chèn giữa mục `Ngân hàng` (dòng 50-55)
và mục `Đối tác` (dòng 56)

- [x] **B1.** Thêm mục cấp 1 phẳng (có `link`, **không** có `subItems` → thành nút rail đi thẳng,
  đúng pattern mục `Ngân hàng`):

```js
{
    label: 'Nhóm ngành',
    icon: 'ri-building-2-line',
    // Route vẫn là route cũ của phân hệ Giao việc: đợt này chỉ chuyển MENU, chưa chuyển code.
    link: '/assign/industry-groups',
    isShow: ['Quản lý danh mục nhóm ngành', 'Xem danh mục nhóm ngành'],
},
```

- [x] **B2.** Kiểm tra thứ tự cuối cùng: Tổng quan → Địa lý → Ngân hàng → **Nhóm ngành** → Đối tác.
- [x] **B3.** Kiểm tra `isShow` là **mảng**, khớp từng ký tự với 2 tên quyền copy ở Task 2.

### Task 4: Kiểm tra tĩnh trước khi giao user test

- [x] **B1.** Grep toàn `hrm-client` chuỗi `industry-groups` → chỉ còn **1** chỗ khai menu
  (`master-data.js`); `sale-hub.js` và `sale.js` sạch.
- [x] **B2.** Parse 3 file bằng babel để chắc không lỗi cú pháp
  (không dùng ESLint — repo không có config chạy được trên Node 14, xem `[[hrm_client_no_eslint_config]]`).
- [x] **B3.** Xác nhận `git status` chỉ có đúng 3 file menu thay đổi trong `hrm-client`,
  không đụng `pages/`, không đụng repo `hrm-api`.

---

## Phase 2 — Verify trên trình duyệt (Playwright, 2026-08-12)

Tài khoản đang đăng nhập trên máy dev: **Trần Thị Ngọc Mai — có 0 quyền**
(`store.state.permissions = []`, lấy từ chính API đã trả `employees`/`companies` có dữ liệu
→ đúng là tài khoản không được gán quyền, không phải nạp hụt). Vì vậy mọi màn có gate quyền
đều bị `middleware/checkPermission.js:56` đẩy về `/pages/extras/404` — **kể cả màn không đụng tới**
(`/assign/solution-groups` cũng 404 y hệt) → chặn này là hành vi sẵn có, không do đợt sửa này.

- [x] **V1.** Dev server đã nạp code mới (không cần restart tay): menu gốc phân hệ `master-data`
  đọc trong app = `Tổng quan | Địa lý | Ngân hàng | Nhóm ngành | Đối tác` — đúng thứ tự thiết kế.
- [x] **V3.** `/sale/dashboard` → `sb.subsystem.key = 'sale'`;
  `Danh mục › Danh mục chung = ['Phiếu thu thập thông tin', 'Loại tài liệu', 'Loại giảm giá']` (3 mục);
  `JSON.stringify(menu).includes('Nhóm ngành') = false`.
- [x] **V4 (phần menu).** Trên trang thuộc phân hệ Danh mục chung, sau khi nạp tạm quyền
  `Xem danh mục nhóm ngành` vào store (chỉ trong bộ nhớ trình duyệt, KHÔNG ghi dữ liệu):
  `navLinks = ['Ngân hàng → /human/banks', 'Nhóm ngành → /assign/industry-groups']`.
- [x] **V5.** Khi store 0 quyền: `navLinks = ['Ngân hàng']` → mục Nhóm ngành bị ẩn đúng như gate.
- [x] **Không vỡ menu**: `/human/banks` mở bình thường, sidebar "DANH MỤC CHUNG" render đủ
  (Tổng quan, Ngân hàng, Địa lý, Đối tác), 0 lỗi console.

### User tự test nốt bằng tài khoản có quyền — báo XONG 2026-08-12

- [x] **V2.** Mở `/assign/industry-groups` → sidebar là **Danh mục dùng chung**, màn chạy bình thường.
- [x] **V6.** Màn Phân quyền: 2 quyền vẫn nằm tab **Giao việc › Danh mục** (đúng như đã chốt).

⚠️ Ghi chú kỹ thuật khi test: **không** bơm quyền vào `store.state.permissions` rồi chụp màn —
thao tác này làm route re-eval và văng sang trang 404 (đọc được giá trị trả về nhưng không chụp
được ảnh sạch). Muốn có ảnh thật thì phải đăng nhập bằng tài khoản có quyền.

---

### Checkpoint — 2026-08-12

Vừa hoàn thành: Phase 1 (Task 1-4) — 3 file menu đã sửa xong, kiểm tra tĩnh pass.

Bằng chứng (chạy thật, script node + babel require-hook nạp đúng `subsystems.js` của repo):

```
/assign/industry-groups      -> master-data      (trước: sale)
/human/banks                 -> master-data      (không đổi)
/assign/form-templates       -> sale             (không đổi)
/assign/customers            -> master-data      (không đổi)

hubNavLinksFor(master-data, [có quyền Xem])  : Ngân hàng | Nhóm ngành /assign/industry-groups
hubNavLinksFor(master-data, [])              : Ngân hàng            → gate quyền còn hiệu lực
sale > Danh mục > Danh mục chung             : Phiếu thu thập thông tin | Loại tài liệu | Loại giảm giá
JSON.stringify(sale.menu).includes('industry-groups') = false
```

Babel parse 3 file: OK. `git status` (hrm-client): đúng 3 file menu thay đổi trong đợt này
(các file `V2BaseImportTable.vue`, `DocumentTable.vue`, `EquipmentTab.vue`,
`pages/assign/customers/index.vue`, `utils/assign/customer-print-header.js` là thay đổi có sẵn
từ trước, KHÔNG thuộc đợt này). Repo `hrm-api`: không đụng.

Đang làm dở: không có.

Bước tiếp theo: user chạy Phase 2 (V1-V6) trên trình duyệt.

Blocked:

### Checkpoint — 2026-08-12 (kết thúc)

Vừa hoàn thành: Phase 2 — user báo đã test xong toàn bộ, gồm cả V2 và V6 (phần cần tài khoản
có quyền `Quản lý/Xem danh mục nhóm ngành`).

Đang làm dở: không có. Feature **HOÀN THÀNH**, đã chuyển sang mục "Hoàn thành" ở
`.plans/gop-db/STATUS.md`.

Bước tiếp theo: chưa commit (theo quy tắc dự án) — khi cần thì commit 3 file menu ở `hrm-client`
và merge về `gop_db`.

Blocked:

---

## Nợ kỹ thuật (đã chốt chấp nhận)

1. Quyền 983/998 vẫn `type = 4`, `group = 'Danh mục'` → màn Phân quyền xếp ở phân hệ Giao việc.
   Muốn dọn phải đổi **cả `group` lẫn `type`** và tác động DB đang chạy (xem spec mục 2.1).
2. Code màn vẫn ở `pages/assign/` + `Modules/Assign` → URL còn tiền tố `/assign`.
   Chuyển thật thì theo quy trình 7 bước ở `.plans/gop-db/chuyen-code-phan-he/design.md`
   (lưu ý đợt trước đã bị revert).
