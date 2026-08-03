# Task 6 — Store `warehouse-dashboard` — Report

## Trạng thái
Done.

## File thay đổi
- Tạo mới: `nhatlinh-client/store/warehouse-dashboard.js`

## Nội dung
```js
// Store namespace 'warehouse-dashboard' — Dashboard Kho
// Action gọi qua apiGetMethod root dispatch.

export const state = () => ({})

export const mutations = {}

export const actions = {
    async get({ dispatch }, query) {
        return await dispatch('apiGetMethod', `warehouse/dashboard${query || ''}`, { root: true })
    },
}

export const getters = {}
```

## Pattern đã khớp
Khớp `nhatlinh-client/store/sale-dashboard.js` (và cùng convention với `store/warehouse-report.js`):
- KHÔNG gọi trực tiếp `this.$axios.$get` như snippet gợi ý trong plan — dự án dùng root action `apiGetMethod` (định nghĩa tại `store/actions.js:1359`), tự thêm prefix `/api/v1/` + `getCommonOptions` (token, headers...).
- `apiGetMethod` trả nguyên `{ code, message, data }` (không unwrap `.data` trong store) — page tiêu thụ (`pages/sale/dashboard/index.vue:578-587`) mới là nơi đọc `response.data`. Vì vậy action `get` ở đây cũng trả nguyên response, KHÔNG `return res.data`, để đồng nhất — Task 7 (trang dashboard kho) sẽ đọc `response.data` giống `sale-dashboard`.
- Tham số truyền vào action là `query` — một **chuỗi query string đã build sẵn** (vd `?granularity=month&top_from=...`), không phải object `params`. Việc build chuỗi này do page thực hiện bằng helper `buildQueryString` (`utils/url-action.js`), giống cách `pages/sale/dashboard/index.vue` làm ở dòng 570-576. Task 7 cần làm theo đúng cách này khi dispatch `warehouse-dashboard/get`.
- Giữ nguyên cấu trúc tối thiểu `state/mutations/actions/getters` rỗng theo YAGNI — không thêm state thừa vì action `get` không cần lưu cache trong store (page tự quản lý `data()`).

## Verify
Đọc lại file, cú pháp export ES module hợp lệ (state/mutations/actions/getters), tên action `get` và path `warehouse/dashboard` đúng endpoint `GET /v1/warehouse/dashboard` (prefix `/api/v1/` do `apiGetMethod` tự thêm) — không chạy `npm build` theo ràng buộc Node cũ.

## Concerns
- Plan Task 6 (snippet mẫu) mô tả `get({ commit }, params)` gọi `this.$axios.$get` trực tiếp và `return res.data` — đã CHỦ ĐỘNG lệch khỏi snippet này để khớp convention thực tế của dự án (`sale-dashboard.js`, `warehouse-report.js`) theo đúng chỉ dẫn ưu tiên "đọc sale-dashboard.js để khớp, giữ đồng nhất". Cần lưu ý khi viết Task 7: dispatch với `query` dạng string (không phải object `params`), và đọc `response.data` ở page thay vì kỳ vọng store đã unwrap sẵn.
- Chưa verify được bằng cách chạy thực tế (không build được do Node cũ) — sẽ verify end-to-end ở Task 7 khi có trang gọi thử.
