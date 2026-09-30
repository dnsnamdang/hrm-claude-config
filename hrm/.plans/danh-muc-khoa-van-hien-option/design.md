# Design — Danh mục bị khoá vẫn hiện ở bản ghi đang dùng

## Mục tiêu
Dropdown danh mục (Giai đoạn dự án, Loại meeting…) chỉ liệt kê bản ghi còn hoạt động, NHƯNG giá trị
mà bản ghi đang giữ thì vẫn phải hiện dù danh mục đã khoá — không thì mở màn Sửa thấy ô trống, lưu
lại là mất dữ liệu. Danh mục khoá phải có dấu 🔒 và biến mất ngay khi đổi sang giá trị khác.

Chi tiết quy tắc: `.claude/skills/select-and-input-state/SKILL.md` mục 1.

## Redmine #11063 — phản hồi #4 của QA (2026-08-20)
QA nêu 4 điểm. Kiểm chứng lại trên nhánh `tpe` ngày 2026-09-16 bằng Playwright:

| # | QA nêu | Kết quả kiểm chứng |
| --- | --- | --- |
| 1 | Lưu dự án lỗi nhưng chỉ báo "kiểm tra lại thông tin", không biết trường nào | **Có thật** → đã sửa (xem dưới) |
| 2 | Xem chi tiết: thêm 🔒 vào ô bị khoá | Đã có 🔒 (`mt-selection-text`) |
| 3 | Dự án TKT: dropdown Giai đoạn dự án khoá chưa có 🔒 | Đã có 🔒 trong dropdown |
| 4 | Đổi sang giai đoạn khác, lưu, vào lại vẫn thấy giai đoạn khoá cũ | Không tái hiện — option khoá biến mất ngay |

Điểm 2–4 do commit `d1dc896c5` (2026-08-20) xử lý, **đúng ngày QA phản hồi** → QA test bản chưa có
commit này.

## Điểm 1 — nguyên nhân và cách sửa
`_id/edit.vue` và `_id/index.vue` bắt lỗi kiểu:

```js
catch (error) { ...; this.$toasted.global.error({ message: 'Vui lòng kiểm tra lại thông tin' }) }
```

Một câu cứng cho MỌI lỗi: 404 (bản ghi vừa bị xoá), 403, 423, và cả 422 mà lỗi rơi vào trường form
không hiển thị — người dùng đi dò từng ô mà không ô nào đỏ.

Sửa: 2 helper dùng chung trong `utils/helpers.js`
- `saveErrorMessage(error)` — phân loại 404/409 · 403 · 423 · 422 · còn lại
- `hasVisibleFieldError()` — trên màn có ô lỗi nào đang hiện thật không

Với 422: chờ section render rồi mới quyết — có ô đỏ thì báo "Bạn chưa nhập đầy đủ thông tin" + cuộn
tới ô lỗi; không có ô nào đỏ thì báo `SAVE_CONFLICT_MESSAGE` = "Dữ liệu đã thay đổi, vui lòng tải lại"
(đúng câu của màn Lịch meeting như QA yêu cầu).
