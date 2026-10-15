# Task 10 — Brief: FE API layer + list page + menu (Yêu cầu xuất bán hàng mượn)

> Đây là **requirements của bạn** — dùng ĐÚNG giá trị verbatim ghi ở đây. Repo: `hrm-client` (Nuxt 2.14 / Vue 2 / Bootstrap-Vue). Nhánh: `gop_db` (đừng đổi nhánh).
> Feature khuôn để COPY cấu trúc + CSS: `pages/finance/product-import-requests/`. Đọc `index.vue` của khuôn TRƯỚC, bám sát 100% cách nó dựng bảng/filter/phân trang/nút hành động.
> KHÔNG commit (Step 5 chỉ khi user yêu cầu — ở đây KHÔNG commit).

## Bối cảnh 1 dòng
Màn danh sách "Yêu cầu xuất bán hàng mượn" (mã phiếu **PYCXBHM**) — tiêu thụ 11 endpoint BE đã xong ở Task 8. Phase 1: chỉ list + filter + nút hành động theo cờ quyền. KHÔNG kế toán, KHÔNG kho. Trang create/detail/print là Task 11-12 (KHÔNG làm ở task này) — chỉ cần nút "Tạo phiếu" điều hướng `/finance/borrow-sell-requests/create` và mã phiếu link sang `/finance/borrow-sell-requests/{id}` (route chưa tồn tại là bình thường).

---

## FILE PHẢI TẠO / SỬA

1. **Create** `hrm-client/pages/finance/borrow-sell-requests/api.js` — module bọc endpoint (code đầy đủ bên dưới, dùng VERBATIM).
2. **Create** `hrm-client/pages/finance/borrow-sell-requests/index.vue` — màn danh sách (adapt từ khuôn).
3. **Modify** `hrm-client/components/subsystem-menu/finance.js` dòng 169.

---

## FILE 1 — `api.js` (dùng verbatim)

Codebase KHÔNG có lớp service riêng; mọi call đi qua shared Vuex action (`store/actions.js`): `apiGetMethod(ctx, url)`, `apiPostMethod(ctx, {url, payload})`, base cố định `/api/v1/`. Ta gói 11 endpoint Task 8 vào 1 module mỏng để T10/T11/T12 dùng chung. Mỗi hàm nhận `dispatch` làm tham số đầu (Vuex `dispatch` đã được bind sẵn → truyền `this.$store.dispatch` an toàn).

```js
// hrm-client/pages/finance/borrow-sell-requests/api.js
// Lớp gọi API cho màn "Yêu cầu xuất bán hàng mượn" (PYCXBHM).
// Base /api/v1/ do apiGetMethod/apiPostMethod tự thêm → chỉ truyền path từ 'finance/...'.
const BASE = 'finance/borrow-sell-requests'

// Build query string từ object params (bỏ null/undefined/'' để URL sạch)
function qs(params = {}) {
  const parts = []
  Object.keys(params).forEach((key) => {
    const val = params[key]
    if (val === null || val === undefined || val === '') return
    if (Array.isArray(val)) {
      val.forEach((v) => {
        if (v !== null && v !== undefined && v !== '') {
          parts.push(`${encodeURIComponent(key)}[]=${encodeURIComponent(v)}`)
        }
      })
    } else {
      parts.push(`${encodeURIComponent(key)}=${encodeURIComponent(val)}`)
    }
  })
  return parts.length ? `?${parts.join('&')}` : ''
}

export const list = (dispatch, params = {}) =>
  dispatch('apiGetMethod', `${BASE}${qs(params)}`)

export const getContracts = (dispatch, params = {}) =>
  dispatch('apiGetMethod', `${BASE}/contracts${qs(params)}`)

export const getBorrowSellData = (dispatch, id, params = {}) =>
  dispatch('apiGetMethod', `${BASE}/contracts/${id}/borrow-sell-data${qs(params)}`)

export const store = (dispatch, payload) =>
  dispatch('apiPostMethod', { url: BASE, payload })

export const show = (dispatch, id) =>
  dispatch('apiGetMethod', `${BASE}/${id}`)

export const deny = (dispatch, id, comment) =>
  dispatch('apiPostMethod', { url: `${BASE}/${id}/deny`, payload: { comment } })

export const managerApprove = (dispatch, id) =>
  dispatch('apiPostMethod', { url: `${BASE}/${id}/manager-approve`, payload: {} })

export const switchBoardOfManager = (dispatch, id) =>
  dispatch('apiPostMethod', { url: `${BASE}/${id}/switch-board-of-manager`, payload: {} })

export const boardOfManagerApprove = (dispatch, id) =>
  dispatch('apiPostMethod', { url: `${BASE}/${id}/board-of-manager-approve`, payload: {} })

export const printData = (dispatch, id) =>
  dispatch('apiGetMethod', `${BASE}/${id}/print-data`)
```

Trong component: `import * as api from './api'` rồi gọi `api.list(this.$store.dispatch, params)`, `api.deny(this.$store.dispatch, id, comment)`, v.v.

---

## FILE 2 — `index.vue` (adapt từ khuôn)

**Cách làm:** Đọc `pages/finance/product-import-requests/index.vue` (35KB) làm khuôn — COPY nguyên cấu trúc `<template>`, mixin, khối `<style lang="scss">` (CSS `status-pill`, `v2-cell-link`, ...), rồi thay data-binding sang contract BE dưới đây. Giữ nguyên: `V2BaseDataTable`, `V2BaseSmartFilterPanel`, `V2BaseRowActions`, các mixin `filterStateMixin`/`columnCustomizationMixin`/`DedupeLoadMixin`, cách map phân trang thủ công.

### Endpoint & response (từ Task 8 — verbatim)
- List: `api.list(this.$store.dispatch, params)` → **GET** `api/v1/finance/borrow-sell-requests`.
- Response shape (meta phẳng ở cấp 1 qua `additional()`, KHÔNG lồng trong `meta`):
  ```
  {
    data: [ <row>, ... ],
    total, lastPage, currentPage, perPage,
    canViewAllCompany, canViewCompany, canViewDepartment, isKeToanKho, isTP, isBGD
  }
  ```
- **Row fields:** `id, code, type, type_name, contract_code, customer_name, creator_name, status, status_name, created_at` + 6 cờ **`is_can_view, is_can_edit, is_can_approve, is_can_deny, is_can_manager_approve, is_can_board_approve`**.

### Filter params (searchByFilter BE hỗ trợ — chỉ gửi field này)
| FE filter | param gửi BE | ghi chú |
|---|---|---|
| Mã phiếu | `code` | LIKE |
| Mã hợp đồng | `contract_code` | LIKE (tìm cả firm + wr_service) |
| Khách hàng | `customer` | = customer_id |
| Loại phiếu | `export_type` | 1=HĐ hãng, 2=HĐ dịch vụ |
| Trạng thái | `status` | xem status map |
| Từ ngày | `startDate` | |
| Đến ngày | `endDate` | |
| Người tạo | `created_by` | (tuỳ chọn, nếu khuôn có filter người tạo) |
| Tab loại | `type` | `all`/`accounting`/`waiting_approve`; thiếu→chỉ phiếu mình tạo |

Ngoài ra BE còn nhận `company`, `department`, `approver`, `productName`, `productCode`, `order`, `contract_id`, `contract_type` — chỉ thêm vào filter UI nếu khuôn có sẵn field tương ứng; KHÔNG bắt buộc.

### Status map (badge)
```
1 => 'Đã duyệt'      (success/xanh)
2 => 'Chờ duyệt'     (warning/vàng)
3 => 'Đang tạo'      (draft/xám)
4 => 'Không duyệt'   (danger/đỏ)
10 => 'Chờ TP duyệt' (warning/vàng)
11 => 'Chờ BGD duyệt'(warning/vàng)
```
Dùng `status_name` BE trả để hiển thị text; class badge tự map theo `status` số theo quy ước khuôn (success→active, danger→lock, còn lại→draft). BE đã trả `status_name` nên KHÔNG cần hard-code map text ở FE — nhưng map class theo số `status`.

### Type map
`type` 1 => 'HĐ hãng', 2 => 'HĐ dịch vụ' (BE đã trả `type_name`).

### Cột bảng (đề xuất, theo khuôn)
Mã phiếu (`code`, link `v2-cell-link` → `/finance/borrow-sell-requests/{id}`) · Loại (`type_name`) · Mã HĐ (`contract_code`) · Khách hàng (`customer_name`) · Người tạo (`creator_name`) · Trạng thái (badge theo `status`/`status_name`) · Ngày tạo (`created_at`) · Thao tác (`V2BaseRowActions`).

### Nút hành động cấp dòng (V2BaseRowActions — map cờ is_can_*)
`getRowActions(item)` trả mảng, mỗi action có `key`, `label`, `interactable` (= cờ BE, fail-closed):
- `{ key: 'view', label: 'Xem', interactable: !!item.is_can_view }` → điều hướng detail.
- `{ key: 'edit', label: 'Sửa', interactable: !!item.is_can_edit }` → `/finance/borrow-sell-requests/{id}/edit`.
- `{ key: 'manager_approve', label: 'TP duyệt', interactable: !!item.is_can_manager_approve }` → `api.managerApprove`.
- `{ key: 'switch_board', label: 'Chuyển BGD', interactable: !!item.is_can_manager_approve }` → `api.switchBoardOfManager` (TP có quyền duyệt thì cũng có quyền chuyển lên BGD).
- `{ key: 'board_approve', label: 'BGD duyệt', interactable: !!item.is_can_board_approve }` → `api.boardOfManagerApprove`.
- `{ key: 'deny', label: 'Từ chối', interactable: !!item.is_can_deny }` → mở modal nhập comment → `api.deny(dispatch, id, comment)`.
`@action` emit **CHUỖI** `action.key`. Nếu cờ = false → action ẩn/mờ (đừng render nút bật).
**TUYỆT ĐỐI KHÔNG** khởi tạo bất kỳ cờ nào = `true`; đọc thẳng từ `item.is_can_*` (mặc định falsy nếu thiếu).

### Nút cấp trang
- "Tạo phiếu" → `this.$router.push('/finance/borrow-sell-requests/create')`. (Hiện luôn — tạo phiếu của mình không gate ở FE, giống khuôn.)

### Phân trang (map thủ công — GOTCHA)
```js
this.pagination.currentPage = Number(response.currentPage ?? response.current_page) || this.pagination.currentPage
this.pagination.pageSize    = Number(response.perPage ?? response.per_page) || this.pagination.pageSize
this.pagination.total       = Number(response.total) || 0
this.pagination.totalPages  = Number(response.lastPage ?? response.last_page) || 1
```
⚠️ KHÔNG fallback `currentPage`/`pageSize` về `|| 1` (đọc nhầm tên field meta → ép về trang 1 → watcher DataTable tưởng đổi trang → gọi lại API → vòng lặp/nhảy trang). Fallback về giá trị hiện tại như trên.

### Modal từ chối (comment)
Dùng modal comment (theo khuôn hoặc `BaseConfirmModal` có ô nhập). Bắt buộc `comment` (BE Task 6/8 validate `comment` required|max:255 — nếu thiếu BE trả 422). Sau khi `api.deny` thành công → toast + `loadData()` refresh.

### Sau mọi action duyệt/từ chối thành công
Gọi lại `loadData()` để refresh danh sách + cờ quyền mới. Bắt lỗi 403 → toast "Không đủ quyền"; 422 → toast lỗi validate.

---

## FILE 3 — `finance.js` menu (sửa 1 dòng)

Dòng **169** hiện tại:
```js
            { label: 'Yêu cầu xuất bán hàng mượn' },
```
Đổi thành:
```js
            { label: 'Yêu cầu xuất bán hàng mượn', link: '/finance/borrow-sell-requests' },
```
KHÔNG thêm gate quyền/isShow (file này không gate subItem theo permission — BE scope dữ liệu qua searchByFilter). Format `{ label, link }` khớp các sibling (dòng 49/53/57).

---

## RÀNG BUỘC BẮT BUỘC (CLAUDE.md — không vi phạm)
- **Fail-closed:** KHÔNG bao giờ gán cờ quyền = `true`. Mọi `is_can_*` đọc trực tiếp từ BE row/meta; mặc định falsy.
- FE Select trong modal/popup phải dùng `V2BaseSelectInModal` (task này ít khả năng có select-in-modal; nếu có thì tuân thủ).
- Tuân thủ style list của module (bám khuôn product-import-requests).
- KHÔNG commit/push. KHÔNG đọc `node_modules/`.
- KHÔNG tự sửa hàm dùng chung (`store/actions.js`, V2Base*). Chỉ tạo/sửa 3 file nêu trên.

## VERIFY (bắt buộc, ghi vào report)
1. `cd hrm-client && npx eslint pages/finance/borrow-sell-requests/api.js pages/finance/borrow-sell-requests/index.vue` (hoặc lệnh lint repo dùng) — 0 error. Nếu repo không có eslint chạy được thì `node --check` cho api.js + báo rõ đã kiểm cú pháp cách nào.
2. Xác nhận `index.vue` import đúng `api.js` + các V2Base component tồn tại (grep path).
3. Xác nhận menu dòng 169 đã có `link`.
4. (Không cần chạy dev server — nếu môi trường không build được, ghi rõ trong report thay vì bịa PASS runtime.)

## REPORT
Ghi report đầy đủ vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-10-report.md`. Trả về controller CHỈ: status (DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED), danh sách file tạo/sửa, 1 dòng tóm tắt verify, concerns. KHÔNG tự dispatch subagent nào (không helper, không reviewer).
