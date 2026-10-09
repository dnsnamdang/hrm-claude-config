# Task P2-10b Brief — FE wiring phiếu xuất bán hàng mượn (api.js + nút "Lập phiếu bán" + menu)

> **ĐỌC FILE NÀY TRƯỚC — requirements đầy đủ, dùng giá trị exact verbatim.** Giao tiếp tiếng Việt.
> Repo FE: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client` (Nuxt 2.14 / Vue 2). Nhánh `gop_db`.
> Feature `xuat-ban-hang-muon` Phase 2 (phiếu BÁN thực tế BorrowSell, code `PXBHM-`).

## Bối cảnh 1 dòng

Phase 1 (phiếu YÊU CẦU xuất bán = borrow-sell-requests) FE đã xong. Task này nối dây tối thiểu để mở đường sang Phase 2: (1) lớp gọi API cho màn phiếu bán, (2) nút "Lập phiếu bán" trên màn chi tiết phiếu YC, (3) link menu. **Chưa tạo màn list/create/detail** (đó là T11-T13). Chỉ 3 việc dưới đây.

## ⚠️ QUY TẮC GIT ĐẶC BIỆT — KHÔNG COMMIT

FE repo này để thay đổi ở dạng **working-tree/staged, KHÔNG commit** (nhất quán với toàn bộ Phase 1 FE hiện cũng đang uncommitted). **TUYỆT ĐỐI KHÔNG chạy `git commit`.** Chỉ tạo/sửa file. Có thể `git add <path cụ thể>` để stage nếu muốn, nhưng KHÔNG bắt buộc. KHÔNG `git add -A`. Controller sẽ review qua working-tree diff.

## Ràng buộc chung (BẮT BUỘC)
- Cờ quyền fail-closed: KHÔNG hard-code `= true` cho bất kỳ cờ quyền nào (pattern cấm `can[A-Za-z]*\s*=\s*true`).
- Nút bấm tuân skill `button-convention` (đã tóm tắt phần liên quan bên dưới — không cần đọc lại file skill).
- KHÔNG đọc `node_modules/`. KHÔNG spawn subagent.
- KHÔNG sửa file nào ngoài 3 file liệt kê dưới.

---

## Việc 1 — Tạo `pages/finance/borrow-sells/api.js`

Tạo MỚI file `pages/finance/borrow-sells/api.js`. Mirror y hệt cấu trúc `pages/finance/borrow-sell-requests/api.js` (helper `qs()` + gọi qua `apiGetMethod`/`apiPostMethod`), nhưng BASE khác và chỉ 4 hàm. Dùng ĐÚNG nội dung sau (copy nguyên):

```js
// hrm-client/pages/finance/borrow-sells/api.js
// Lớp gọi API cho màn "Phiếu xuất bán hàng mượn" (PXBHM) — Phase 2.
// Base /api/v1/ do apiGetMethod/apiPostMethod tự thêm → chỉ truyền path từ 'finance/...'.
const BASE = 'finance/borrow-sells'

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

// Danh sách phiếu xuất bán (getBorrowSells) — params: filter + page + per_page.
export const list = (dispatch, params = {}) =>
  dispatch('apiGetMethod', `${BASE}${qs(params)}`)

// Chi tiết 1 phiếu xuất bán (getBorrowSell) — kèm khối hạch toán.
export const show = (dispatch, id) =>
  dispatch('apiGetMethod', `${BASE}/${id}`)

// Lập phiếu xuất bán (storeBorrowSell) — payload qty-only, BE tự tính tiền.
export const store = (dispatch, payload) =>
  dispatch('apiPostMethod', { url: BASE, payload })

// Dữ liệu in phiếu (getBorrowSellPrint).
export const printData = (dispatch, id) =>
  dispatch('apiGetMethod', `${BASE}/${id}/print-data`)
```

Endpoint BE thật (đã tồn tại — T9): `GET /api/v1/finance/borrow-sells`, `POST /api/v1/finance/borrow-sells`, `GET /api/v1/finance/borrow-sells/{id}`, `GET /api/v1/finance/borrow-sells/{id}/print-data`. KHÔNG cần chỉnh gì thêm cho khớp — path trên đã đúng.

---

## Việc 2 — Nút "Lập phiếu bán" trên màn chi tiết phiếu YC

File: `pages/finance/borrow-sell-requests/_id/index.vue`.

Trong `<div class="export-actionbar__btns">` (hiện có các nút: Quay lại, Lịch sử, In, Từ chối, TP duyệt, Chuyển BGD, BGD duyệt — dòng ~190-217), **THÊM 1 nút** "Lập phiếu bán":

```vue
<V2BaseButton v-if="data.is_can_create_borrow_sell" primary size="sm" @click="goCreateSell">
    <template #prefix><i class="ri-shopping-cart-2-line" style="font-size: 15px"></i></template>
    Lập phiếu bán
</V2BaseButton>
```

- **Vị trí đặt:** ngay SAU nút "In" và TRƯỚC nút "Từ chối" (nhóm action chính, tách khỏi nhóm duyệt). Đặt đúng thứ tự này.
- **Gate:** `v-if="data.is_can_create_borrow_sell"` — cờ do BE trả (T10a đã thêm vào `BorrowSellRequestDetailResource`, fail-closed: undefined lúc chưa load = falsy = ẩn nút, đúng chuẩn Phase 1 dùng `data.is_can_*`). KHÔNG khởi tạo cờ này `= true` ở bất kỳ đâu.
- **Variant:** `primary` (action chính, đúng button-convention). Icon `ri-shopping-cart-2-line`.

Thêm method `goCreateSell` vào phần `methods` của component (đặt cạnh `goBack`/`printRequest`):

```js
goCreateSell() {
    this.$router.push(`/finance/borrow-sells/create?request_id=${this.requestId}`)
},
```

- Dùng biến id sẵn có của component. File này đã có `requestId` (dùng ở `BorrowSellRequestHistoryModal :id="requestId"`). Nếu tên biến id thực tế khác (`this.id`, `this.$route.params.id`), dùng đúng biến đang có — kiểm tra trong file trước khi viết. Ưu tiên `this.requestId` nếu tồn tại; nếu không, `this.$route.params.id`.

**Lưu ý:** màn create (`/finance/borrow-sells/create`) CHƯA tồn tại (T12 sẽ tạo). Nút vẫn thêm giờ — điều hướng sẽ 404 tạm thời cho tới khi T12 xong. Đó là chủ ý (nối dây trước). KHÔNG tạo màn create trong task này.

---

## Việc 3 — Link menu

File: `components/subsystem-menu/finance.js`.

Dòng ~170 hiện có placeholder KHÔNG link:
```js
{ label: 'Phiếu xuất bán hàng mượn' },
```
Sửa thành (thêm `link`, giữ nguyên label):
```js
{ label: 'Phiếu xuất bán hàng mượn', link: '/finance/borrow-sells' },
```
KHÔNG tạo entry mới, KHÔNG đổi label. Chỉ thêm thuộc tính `link` vào object đã có.

---

## button-convention (tóm tắt phần liên quan)
- Mọi `V2BaseButton` phải có icon qua slot `#prefix`, luôn khai `size="sm"`.
- Action chính (Lập phiếu bán = tạo phiếu) → prop `primary` (KHÔNG `type="primary"`).
- Icon Remix (`ri-*`). "Lập phiếu bán" ~ tạo phiếu bán → dùng `ri-shopping-cart-2-line`.

## Kiểm tra trước khi báo cáo
- `node -c pages/finance/borrow-sells/api.js` (check cú pháp JS thuần) — phải PASS.
- Nếu có eslint config: chạy `npx eslint pages/finance/borrow-sells/api.js pages/finance/borrow-sell-requests/_id/index.vue components/subsystem-menu/finance.js` (nếu lệnh không có/không chạy được thì bỏ qua, ghi rõ trong report). KHÔNG chạy `nuxt build` (nặng, không cần).
- Đọc lại `_id/index.vue` xác nhận không phá cấu trúc template (số `<V2BaseButton>` mở = đóng), method `goCreateSell` nằm đúng object `methods`.

## Report contract
- KHÔNG commit. Ghi report vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-10b-report.md`.
- Trả về ngắn: status; danh sách 3 file đã tạo/sửa; biến id thực tế đã dùng trong goCreateSell; kết quả `node -c`/eslint; concerns nếu có.
