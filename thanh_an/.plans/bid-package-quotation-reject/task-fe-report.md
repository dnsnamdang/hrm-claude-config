# FE Report — Task 7 & Task 8: Từ chối lập gói thầu

> Ngày: 2026-06-23
> Người thực hiện: agent (theo chỉ đạo @khoipv)

---

## Tóm tắt

Đã hoàn thành Phase 2 Frontend — Task 7 và Task 8 theo plan `2026-06-23-bid-package-quotation-reject.md`.

---

## Task 7 — `hrm-thanhan-client/pages/bid_package/quotation/index.vue`

### Template

1. **Nút "Từ chối lập gói thầu"** (dòng ~189–197 sau chỉnh sửa)
   - Vị trí: trong `<template v-slot:cell(actions)>`, ngay sau nút "Tạo gói thầu"
   - `v-if="item.can_reject_bid"`, `@click="showRejectModal(item.id)"`
   - Icon: `<i class="fas fa-times text-danger"></i>`, variant secondary, tooltip đúng

2. **Modal `id="modal-reject-bid"`** (dòng ~234–245)
   - Vị trí: ngay trước `<confirm-delete-selected ...>`
   - Có `b-form-textarea v-model="rejectReason"`, hiển thị lỗi `rejectError`
   - Sự kiện `@ok="handleRejectBid"`, nút "Xác nhận" / "Hủy"

### Data

Thêm 3 field cạnh `deleteId` (dòng ~363–365):
```js
rejectReason: '',
rejectError: '',
rejectId: undefined,
```

Thêm `{ id: 20, text: 'Từ chối lập gói thầu' }` vào `statuses`.

Thêm `20: 'status-pill pj-status-rose'` vào `statusColorMap`.

### Methods

- `getStatusClass(item)`: thêm nhánh `item.status == 20` → `'badge-danger badge'`
- `getStatusText(item)`: thêm nhánh `item.status == 20` → `'Từ chối lập gói thầu'`
- `showRejectModal(id)`: reset `rejectReason`/`rejectError`, gán `rejectId`, mở modal
- `handleRejectBid(bvModalEvent)`: validate trống, `bvModalEvent.preventDefault()` nếu lỗi; gọi `apiPutMethod` với URL `category/quotations/${this.rejectId}/reject-bid`, toast thành công, `getData()`

---

## Task 8 — `hrm-thanhan-client/pages/sale/project/index.vue`

Chỉ thêm nhãn, KHÔNG thêm nút/action.

1. **`statusOptions`** (dòng ~599–602): thêm `{ id: 19, text: 'Từ chối lập gói thầu' }` sau `id: 18`
2. **`statusColorMap`** (dòng ~680): thêm `19: 'status-pill pj-status-red'`
3. **`getStatusText(item)`** (dòng ~939–941): thêm nhánh `item.status == 19` → `'Từ chối lập gói thầu'`

---

## Concerns / Điểm lưu ý

1. **`sale/project` đã có `rejectId` và `showRejectModal`** cho luồng từ chối phân công (modal riêng `modal-reject-assignment`). Hai luồng này tách biệt hoàn toàn — không xung đột vì dùng modal id khác nhau và đây là Task 8 chỉ bổ sung nhãn, không thêm hành động.

2. **`statusColorMap` của quotation/index.vue**: status 19 (Hủy hợp đồng) và status 20 (Từ chối lập gói thầu) cùng dùng class `pj-status-rose` — đúng theo plan (spec ghi "tái dùng class của status 19").

3. **`statuses` trên quotation/index.vue**: danh sách này không được dùng trong filter hiện tại (không có dropdown lọc status) — chỉ thêm để đủ tập dữ liệu, không ảnh hưởng behavior.

4. **`getStatusClass` trên quotation/index.vue**: hàm này có nhưng template dùng `BaseStatusColor` với `statusColorMap` để hiển thị — `getStatusClass` không được gọi trực tiếp trong template, chỉ giữ lại để tương thích. Thêm nhánh 20 theo plan, không gây lỗi.

5. **Endpoint đã đối chiếu**: `category/quotations/${this.rejectId}/reject-bid` khớp đúng backend `PUT category/quotations/{id}/reject-bid`.

---

## Kết luận

STATUS: **DONE** — không có blocker, không có lệch so với plan. Các concerns trên đều là quan sát về context hiện tại, không ảnh hưởng tính đúng đắn của implementation.
